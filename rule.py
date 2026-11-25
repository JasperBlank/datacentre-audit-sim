"""A stronger baseline: a fixed rule that uses the verifier's power sensor. No model, no judgement.

It reads only what the channels print, the same text the detective sees.

  1. Read the grid operator's daily energy per feed (1 point).
  2. A feed-day is "elevated" if its energy is more than 5% above that feed's quietest day.
  3. Take the power spectrum on elevated feed-days (2 points each). Within a budget, sample every k-th
     elevated day per feed and count each sample for k days.
  4. Lines close in frequency are one run, across feeds and days (within 0.02 Hz; 0.10 Hz with realistic
     instruments, where the frequency wanders).
     Ideal instruments: GPU-hours of a run = sum over feeds of (median GPUs of its line) x (hours the line was seen).
     Realistic instruments: the sensor gives no GPU count, so GPU-hours of a run = the energy above the feed's
     quietest day on the days its line was seen, divided by what one training GPU draws above idle.
  5. VIOLATION if any run is above the threshold.

Extended signals (--instruments extended): the same steps 1 and 2, then the interconnect tap in place of the sensor.
  3. Read the tap inside the feed's cluster on elevated days (2 points each, same sampling). Above TAP_MIN GB/s
     counts as training on that many GPUs, at 1 GB/s per GPU.
  4. Neighbouring sampled days above TAP_MIN on one feed are one run. If the largest run on each feed overlap
     in time, read the tap between the clusters once (2 points); above TAP_MIN joins them into one run.
  5. VIOLATION if any run is above the threshold.

  python rule.py            # 30-point budget, like the detective; adds the rule to results/summary.md
  python rule.py --budget 0 # no budget: every elevated feed-day
  python rule.py --instruments realistic --results results_realistic
"""
import argparse
import json
import math
import os
import re
import statistics

import run
import world

IDEAL_LINE = r"line at ([\d.]+) Hz, (?:steady for )?about (\d+) hours, (?:load consistent with )?roughly (\d+) GPUs"
REAL_LINE = r"line near ([\d.]+) Hz, (?:steady|on and off) for about (\d+) hours"
TAP_MIN = 20.0      # GB/s; below this the tap reading is treated as no training (my choice)


def tap(w, link, day):
    m = re.search(r"about ([\d.]+) GB/s", w.ch_interconnect_tap(link=link, day=day))
    return float(m.group(1)) if m else 0.0


def judge_tap(w, budget, energy, quiet):
    cluster = {"F1": "A", "F2": "B"}
    elevated = {f: [d for d, v in sorted(energy[f].items()) if v > 1.05 * quiet[f]] for f in cluster if f in energy}
    total = sum(len(v) for v in elevated.values())
    max_samples = (budget - 1) // 2 - 1 if budget else total      # one reading is kept for the link between clusters
    stride = max(1, math.ceil(total / max_samples)) if total else 1
    points, best = 1, {}
    for f, days in elevated.items():
        blocks, prev = [], None
        for d in days[::stride]:
            points += 2
            g = tap(w, cluster[f], d)
            if g > TAP_MIN:
                if prev is not None and d - prev <= stride and blocks:
                    blocks[-1].append((d, g))
                else:
                    blocks.append([(d, g)])
                prev = d
            else:
                prev = None
        sized = [(round(sum(g for _, g in b) * 24 * stride / world.EW_GBPS_PER_TRAIN_NODE), b[0][0], b[-1][0]) for b in blocks]
        best[f] = max(sized, default=(0, 0, 0))
    largest, feeds = max((v, [f]) for f, v in best.items()) if best else ((0, 0, 0), [])
    a, b = best.get("F1", (0, 0, 0)), best.get("F2", (0, 0, 0))
    if a[0] and b[0] and a[1] <= b[2] and b[1] <= a[2]:           # both feeds have a run, overlapping in time
        points += 2
        if tap(w, "A-B", (max(a[1], b[1]) + min(a[2], b[2])) // 2) > TAP_MIN:
            largest, feeds = (a[0] + b[0], min(a[1], b[1]), max(a[2], b[2])), ["F1", "F2"]
    return {"verdict": "VIOLATION" if largest[0] > world.THRESHOLD else "NO_VIOLATION", "points": points,
            "largest_estimate": largest[0], "hz": None, "feeds": feeds, "stride": stride, "elevated_feed_days": total}


def judge(w, budget):
    lines = w.ch_utility_energy().split("\n")
    feeds = [f.strip() for f in lines[1].split("|")[1:]]
    energy = {f: {} for f in feeds}
    for row in lines[2:]:
        cells = [c.strip() for c in row.split("|")]
        for f, v in zip(feeds, cells[1:]):
            energy[f][int(cells[0])] = float(v)
    quiet = {f: min(energy[f].values()) for f in feeds}
    if w.ext:
        return judge_tap(w, budget, energy, quiet)
    elevated = {f: [d for d, v in sorted(energy[f].items()) if v > 1.05 * quiet[f]] for f in feeds if f != "F0"}
    total = sum(len(v) for v in elevated.values())
    max_samples = (budget - 1) // 2 if budget else total
    stride = max(1, math.ceil(total / max_samples)) if total else 1
    kw_above_idle = world.KW_PER_GPU[2] - world.KW_PER_GPU[0]
    points, seen = 1, []                      # seen: (hz, feed, gpus, hours) or, realistic, (hz, feed, GPU-hours)
    for f, days in elevated.items():
        for d in days[::stride]:
            points += 2
            text = w.ch_power_spectrum(feed=f, day=d)
            if w.real:
                found = re.findall(REAL_LINE, text)
                for hz, _ in found:           # the day's extra energy is shared between the lines seen that day
                    seen.append((float(hz), f, (energy[f][d] - quiet[f]) * 1000 / kw_above_idle * stride / len(found)))
            else:
                for m in re.finditer(IDEAL_LINE, text):
                    seen.append((float(m.group(1)), f, int(m.group(3)), int(m.group(2)) * stride))
    runs, gap = [], 0.10 if w.real else 0.02   # cluster lines by frequency
    for s in sorted(seen):
        if runs and s[0] - runs[-1][-1][0] <= gap:
            runs[-1].append(s)
        else:
            runs.append([s])
    sizes = []
    for r in runs:
        if w.real:
            gh = sum(x[2] for x in r)
        else:
            gh = sum(statistics.median(g for _, f2, g, _ in r if f2 == f) * sum(h for _, f2, _, h in r if f2 == f)
                     for f in {x[1] for x in r})
        sizes.append((round(gh), r[0][0], sorted({x[1] for x in r})))
    largest = max(sizes, default=(0, None, []))
    return {"verdict": "VIOLATION" if largest[0] > world.THRESHOLD else "NO_VIOLATION", "points": points,
            "largest_estimate": largest[0], "hz": largest[1], "feeds": largest[2], "stride": stride,
            "elevated_feed_days": total}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--budget", type=int, default=30, help="evidence points per case; 0 = no limit")
    ap.add_argument("--seeds", type=int, default=1)
    ap.add_argument("--results", default="results")
    ap.add_argument("--instruments", choices=["ideal", "realistic", "extended"], default="ideal")
    args = ap.parse_args()
    run.RESULTS = os.path.join(run.HERE, args.results)
    real, ext = args.instruments != "ideal", args.instruments == "extended"
    out, score = {}, {"caught": 0, "cheats": 0, "accused": 0, "honest": 0}
    print("Fixed instrument rule, budget %s, %s instruments" % (args.budget or "unlimited", args.instruments))
    for seed in range(args.seeds):
        for w in world.scenarios(seed, real=real, ext=ext):
            r = judge(w, args.budget)
            out["%s-seed%d" % (w.name, seed)] = r
            ok = (r["verdict"] == "VIOLATION") == w.violation
            score["cheats" if w.violation else "honest"] += 1
            score["caught" if w.violation else "accused"] += r["verdict"] == "VIOLATION"
            print("  %-26s %-12s %s | est. largest run %7s GPU-h (true %7s) | %3d points, every %d. day of %d elevated feed-days"
                  % (w.name + "-seed%d" % seed, r["verdict"], "ok   " if ok else "WRONG", format(r["largest_estimate"], ","),
                     format(w.largest_run, ","), r["points"], r["stride"], r["elevated_feed_days"]))
    print("Cheaters caught: %(caught)d of %(cheats)d | honest operators wrongly accused: %(accused)d of %(honest)d" % score)
    path = os.path.join(run.RESULTS, "rows.json")
    if args.budget == 30 and os.path.exists(path):
        data = json.load(open(path, encoding="utf-8"))
        if all(r["case"] in out for r in data["rows"]) and data["meta"].get("instruments", "ideal") == args.instruments:
            for r in data["rows"]:
                r["rule"], r["rule_points"] = out[r["case"]]["verdict"], out[r["case"]]["points"]
            json.dump(data, open(path, "w", encoding="utf-8"), indent=1)
            run.summarize()


if __name__ == "__main__":
    main()
