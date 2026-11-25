"""Sol's routine written as a fixed script: no model, no judgement, about ten rules.

    python script.py                 # the 26 hand-built cases Sol saw (seeds 1 and 2) and 200 generated cases

It reads only what a detective can read (the channels' text) and pays the same points. Written by Claude on
24 Nov 2026 after reading Sol's 26 transcripts AND knowing how the simulator is built, so it is an upper bound on
what "a simpler script" can do here, not a fair opponent: its author knew the list of cheating methods.

The routine:
  1. Read the shipment list, system list, grid meter, scheduler log, sealed logs, bank records and, where it
     exists, the custody record (6 or 7 points).
  2. A declared training or fine-tuning job over the limit is a violation.
  3. Fine-tunes whose customers are all paid for by one other account count as one run.
  4. A declared batch job over the limit is tapped on one day per cluster. Training-level traffic makes it a run.
  5. Load at the grid meter that no declared job explains is added up per stretch of days and tapped once.
  6. A feed with no listed GPUs but more GPUs shipped than listed: its load is sized and the sensor is read once.
  7. Three spot taps per cluster on days with no declared training look for a run that never stops.
  Where a tap's seal is broken, the power sensor is read in its place and the broken seal counts against the operator.
"""
import re
import statistics

import world

TAP_TRAINING = 0.5      # GB/s above what declared fine-tunes explain: far over inference (0.01 to 0.02 per cluster)
KW_ABOVE_IDLE = {"training": 0.65, "finetune": 0.65, "batch": 0.60}   # from the power levels the detective is told
MIN_RESIDUAL = 2000     # GPU-hours in a day that no declared job explains, before the day counts as unexplained
JOB = re.compile(r"- (\S+) \| (\w+) \| customer: (.+?) \| nodes (\w)-\d+ to \w-\d+ \((\d+)\) \| day ([\d.]+) to day ([\d.]+)")


class Out(Exception):
    pass


def judge(w, budget=30):
    spent, notes = [0], []

    def ask(name, **args):
        cost = w.channels[name][1]
        if budget and spent[0] + cost > budget:
            raise Out
        spent[0] += cost
        return getattr(w, "ch_" + name)(**args)

    def done(verdict, why):
        return {"verdict": verdict, "points": spent[0], "why": why, "notes": notes}

    try:
        # ---- 1. the records
        shipped = int(re.search(r"(\d+) GPUs delivered", ask("inventory")).group(1))
        listed = sum(int(n) for n in re.findall(r"to \w-(\d+), power feed", ask("system_list")))
        rows = ask("utility_energy").split("\n")
        feeds = [f.strip() for f in rows[1].split("|")[1:]]
        energy = {f: {} for f in feeds}
        for row in rows[2:]:
            cells = [c.strip() for c in row.split("|")]
            for f, v in zip(feeds, cells[1:]):
                energy[f][int(cells[0])] = float(v)
        text = ask("scheduler_log") + "\n" + ask("log_escrow")        # sealed copies fill in any days the operator "lost"
        jobs = {}
        for id_, kind, cust, cluster, n, d0, d1 in JOB.findall(text):
            jobs[id_] = {"id": id_, "kind": kind, "customer": cust, "cluster": cluster, "n": int(n), "d0": float(d0), "d1": float(d1)}
        jobs = list(jobs.values())
        for j in jobs:
            j["gh"] = j["n"] * (j["d1"] - j["d0"]) * 24
        payer = {}
        for line in ask("bank_payments").split("\n")[2:]:
            c = [x.strip() for x in line.split("|")]
            payer[c[0]] = c[3] if not c[3].startswith("(") else c[0]
        broken, dark = set(), {}
        if "custody" in w.channels:
            for name, rest in re.findall(r"- (power sensor on feed \w+|optical tap, link [\w-]+): (.*)", ask("custody")):
                key = ("power" if name.startswith("power") else "tap", name.split()[-1])
                if "BROKEN" in rest:
                    broken.add(key)
                m = re.search(r"no data on days? ([\d, ]+)", rest)
                dark[key] = {int(x) for x in m.group(1).split(",")} if m else set()

        def hours(j, d):                       # hours of day d that job j runs
            return max(0.0, min(j["d1"], d + 1) - max(j["d0"], d)) * 24

        def declared_training(cluster, d):     # GPUs' worth of declared training traffic on that cluster-day
            return sum(j["n"] * hours(j, d) / 24 for j in jobs if j["cluster"] == cluster and j["kind"] != "batch")

        feed_of = {"A": "F1", "B": "F2"}

        def training_like(cluster, days):
            """Is there training traffic on this cluster beyond the declared fine-tunes? Tries the given days in order."""
            for d in days:
                d = int(min(world.DAYS, max(1, d)))
                if ("tap", cluster) in broken:  # a tap with a broken seal proves nothing: read the power sensor instead
                    line = "line near" in ask("power_spectrum", feed=feed_of[cluster], day=d)
                    notes.append("tap %s seal broken; sensor day %d: %s" % (cluster, d, "line" if line else "no line"))
                    return line
                if d in dark.get(("tap", cluster), ()):
                    continue
                m = re.search(r"about ([\d.]+) GB/s", ask("interconnect_tap", link=cluster, day=d))
                if m:
                    g = float(m.group(1))
                    notes.append("tap %s day %d: %.2f GB/s (declared fine-tunes explain %.0f)" % (cluster, d, g, declared_training(cluster, d)))
                    return g > declared_training(cluster, d) * 1.4 + TAP_TRAINING
            return False

        def quiet_days(j):                     # full days of the job, those without a declared fine-tune first
            days = [d for d in range(int(j["d0"]) + 1, int(j["d1"])) or [int((j["d0"] + j["d1"]) / 2)]]
            return sorted(days, key=lambda d: (declared_training(j["cluster"], d) > 0, abs(d - (j["d0"] + j["d1"]) / 2)))

        # ---- 2. a declared training job over the limit
        for j in jobs:
            if j["kind"] != "batch" and j["gh"] > world.THRESHOLD:
                return done("VIOLATION", "declared %s job %s is over the limit" % (j["kind"], j["id"]))

        # ---- 3. fine-tunes whose customers share one paying account are one run
        groups = {}
        for j in jobs:
            p = payer.get(j["customer"], j["customer"])
            if j["kind"] != "batch" and p != j["customer"]:
                groups.setdefault(p, []).append(j)
        for p, g in groups.items():
            if sum(j["gh"] for j in g) > world.THRESHOLD:
                return done("VIOLATION", "%d fine-tunes paid for by %s add up to %d GPU-hours" % (len(g), p, sum(j["gh"] for j in g)))

        # ---- 4. declared batch work over the limit: does it exchange data like training?
        batches = {}
        for j in jobs:
            if j["kind"] == "batch":
                batches.setdefault((j["customer"], round(j["d0"])), []).append(j)
        for g in sorted(batches.values(), key=lambda g: -sum(j["gh"] for j in g)):
            if sum(j["gh"] for j in g) > world.THRESHOLD:
                for j in g:
                    if training_like(j["cluster"], quiet_days(j)[:3]):
                        return done("VIOLATION", "batch job %s exchanges data like training" % j["id"])

        # ---- 5. load at the meter that no declared job explains
        blocks = []
        for cluster, feed in feed_of.items():
            base = {d: e * 1000 - sum(j["n"] * hours(j, d) * KW_ABOVE_IDLE[j["kind"]] for j in jobs if j["cluster"] == cluster)
                    for d, e in energy[feed].items()}
            quiet = statistics.median(sorted(base.values())[:5])
            extra = {d: (v - quiet) / KW_ABOVE_IDLE["training"] for d, v in base.items()}
            run = []
            for d in range(1, world.DAYS + 2):
                if extra.get(d, 0) > MIN_RESIDUAL:
                    run.append(d)
                elif run:
                    blocks.append({"cluster": cluster, "days": run, "gh": sum(extra[x] for x in run)})
                    run = []
        blocks.sort(key=lambda b: -b["gh"])
        for b in blocks:
            together = b["gh"] + sum(o["gh"] for o in blocks if o is not b and set(o["days"]) & set(b["days"]))
            if together > world.THRESHOLD:
                mid = sorted(b["days"], key=lambda d: abs(d - statistics.mean(b["days"])))
                if training_like(b["cluster"], mid[:3]):
                    return done("VIOLATION", "about %d GPU-hours of undeclared load on days %d-%d exchange data like training"
                                % (together, b["days"][0], b["days"][-1]))

        # ---- 6. a feed with no listed GPUs, and more GPUs shipped than listed
        if "F3" in energy and shipped > listed:
            low = min(energy["F3"].values())
            up = [d for d, e in energy["F3"].items() if e > 1.05 * low]
            size = sum(energy["F3"][d] - low for d in up) * 1000 / KW_ABOVE_IDLE["training"]
            if size > world.THRESHOLD:
                if ("power", "F3") in broken:
                    return done("VIOLATION", "%d unlisted GPUs, about %d GPU-hours of load on F3, and its sensor's seal is broken"
                                % (shipped - listed, size))
                mid = sorted(up, key=lambda d: abs(d - statistics.mean(up)))
                for d in [x for x in mid if x not in dark.get(("power", "F3"), ())][:2]:
                    if "line near" in ask("power_spectrum", feed="F3", day=d):
                        return done("VIOLATION", "%d unlisted GPUs and about %d GPU-hours of periodic load on F3" % (shipped - listed, size))

        # ---- 7. a run that never stops leaves no quiet day at the meter: spot taps
        for cluster in feed_of:
            if ("tap", cluster) in broken:
                continue
            seen = []
            for target in (5, 15, 25):
                d = min(range(1, world.DAYS + 1), key=lambda x: (declared_training(cluster, x) > 0 or x in dark.get(("tap", cluster), ()), abs(x - target)))
                m = re.search(r"about ([\d.]+) GB/s", ask("interconnect_tap", link=cluster, day=d))
                if m and float(m.group(1)) > declared_training(cluster, d) * 1.4 + TAP_TRAINING:
                    seen.append((d, float(m.group(1))))
            if len(seen) >= 2:
                size = statistics.median(g for _, g in seen) * 24 * world.DAYS * len(seen) / 3
                if size > world.THRESHOLD:
                    return done("VIOLATION", "training traffic on cluster %s on days %s with nothing declared"
                                % (cluster, ", ".join(str(d) for d, _ in seen)))
    except Out:
        return done("NO_VIOLATION", "out of points with nothing found")
    return done("NO_VIOLATION", "nothing over the limit found")


def score(name, worlds, show=False):
    import rule
    res = [judge(w) for w in worlds]
    cheats = [i for i, w in enumerate(worlds) if w.violation]
    honest = [i for i, w in enumerate(worlds) if not w.violation]
    flag = lambda verdicts, idx: sum(verdicts[i] for i in idx)
    methods = {"Fixed checks": [w.balance_checks()[1] for w in worlds],
               "Tap rule": [rule.judge(w, 30)["verdict"] == "VIOLATION" for w in worlds],
               "Script of Sol's routine": [r["verdict"] == "VIOLATION" for r in res]}
    print("\n%s: %d cheating, %d honest" % (name, len(cheats), len(honest)))
    print("| Method | Cheaters caught | Honest sites wrongly accused |\n|---|---|---|")
    for m, v in methods.items():
        print("| %s | %d of %d | %d of %d |" % (m, flag(v, cheats), len(cheats), flag(v, honest), len(honest)))
    print("Script: %.1f points per case on average, at most %d" % (statistics.mean(r["points"] for r in res), max(r["points"] for r in res)))
    if show:
        for w, r in zip(worlds, res):
            ok = (r["verdict"] == "VIOLATION") == w.violation
            print("  %-26s %-12s %s | %2d points | %s" % ("%s-seed%d" % (w.name, w.seed), r["verdict"], "ok   " if ok else "WRONG", r["points"], r["why"]))
    else:
        kinds = {}
        for i, w in enumerate(worlds):
            kinds.setdefault(w.note.split(",")[0].rstrip("."), []).append(i)
        for k in sorted(kinds):
            print("  %-30s flagged %d of %d" % (k, flag(methods["Script of Sol's routine"], kinds[k]), len(kinds[k])))
    return res


def main():
    import gen
    score("Hand-built cases, seeds 1 and 2 (the 26 Sol saw)",
          [w for s in (1, 2) for w in world.scenarios(s, ext=True)], show=True)
    score("The 10 generated cases Sol saw", gen.cases(10), show=True)
    score("200 generated cases", gen.cases(200))
    score("The same 200 with mess", gen.cases(200, mess=True))


if __name__ == "__main__":
    main()
