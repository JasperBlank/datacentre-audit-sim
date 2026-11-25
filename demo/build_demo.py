"""Builds the web demo's data and plots from the simulator and the saved results.

    python demo/build_demo.py        # writes demo/cases.json and demo/plots/*.png

Nothing here calls a model. The plots' numbers are typed in below from HANDOVER.md / README.md (23-24 Nov 2026).
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gen, rule, run, script, world  # noqa: E402

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = os.path.dirname(HERE)


# ------------------------------------------------------------------ cases for "play the detective"
def model_answer(folder, case):
    path = os.path.join(ROOT, folder, "cases", case + ".md")
    if not os.path.exists(path):
        return None
    text = open(path, encoding="utf-8").read()
    report = text.split("## Report")[-1]
    v = re.search(r'"verdict": "(\w+)"', report)
    f = re.search(r'"finding": "(.*?)",?\n', report)
    turns = [t for t in re.split(r"\n(?=### Turn \d+)", text.split("## Report")[0]) if t.startswith("### Turn")]
    steps = []
    for t in turns:
        m = re.search(r"^ACTION: (\{.*\})$", t, re.M)
        if m:
            try:
                a = json.loads(m.group(1))
                steps.append({"think": a.get("thinking", ""), "action": a.get("action"), "args": a.get("args") if a.get("action") != "report" else {}})
            except ValueError:
                pass
        elif "BLOCKED" in t:
            steps.append({"think": "", "action": "blocked", "args": {}})
    return {"verdict": v.group(1) if v else "BLOCKED", "finding": f.group(1) if f else "", "steps": steps}


def export(w, label, blurb, folders):
    case = "%s-seed%d" % (w.name, w.seed)
    out = {"label": label, "blurb": blurb, "case": case,
           "channels": [{"name": n, "who": who, "cost": c} for n, (who, c, _) in w.channels.items()],
           "fixed": {n: getattr(w, "ch_" + n)() for n in ("system_list", "scheduler_log", "utility_energy", "inventory",
                                                           "outbound_traffic", "bank_payments", "log_escrow")},
           "power_spectrum": {f: {d: w.ch_power_spectrum(f, d) for d in range(1, 31)} for f in w.feeds()},
           "interconnect_tap": {l: {d: w.ch_interconnect_tap(l, d) for d in range(1, 31)} for l in ("A", "B", "A-B")},
           "switch_counters": {c: {d: w.ch_switch_counters(c, d) for d in range(1, 31)} for c in ("A", "B")},
           "customer_check": {c: w.ch_customer_check(c) for c in sorted(w.invoices())},
           "chip_probe": {"Five chips across cluster A": w.ch_chip_probe(["A-0501", "A-0700", "A-0900", "A-1100", "A-1200"], 610),
                          "Five chips across cluster B": w.ch_chip_probe(["B-0401", "B-0500", "B-0600", "B-0700", "B-0800"], 610),
                          "A shipped serial that is not on the site list": w.ch_chip_probe(["SN102100"], 610)},
           "staff": {q: w.ch_staff(q) for q in ("Why was the power use raised on some days?", "Do you run large training jobs here?",
                                                "Who are your customers and who pays for them?", "What is the large batch job in the log?",
                                                "What is feed F3 for, and why were more GPUs shipped than listed?",
                                                "Why are some scheduler logs missing?")}}
    out["fixed"]["balance_checks"] = w.balance_checks()[0]
    if "custody" in w.channels:
        out["fixed"]["custody"] = w.ch_custody()
    s = script.judge(w)
    words = lambda j: "%s on %d GPUs in cluster %s, day %.1f to %.1f, %s GPU-hours, for %s" % (
        j["kind"], j["n"], j["cluster"], j["start"] / 24 + 1, j["end"] / 24 + 1, format(world.gpu_hours(j), ","), j["customer"])
    out["truth"] = {"violation": w.violation, "note": w.note, "largest_run": w.largest_run,
                    "jobs": [words(j) for j in w.truth], "declared": [words(j) for j in w.declared]}
    out["answers"] = {"Fixed checks": {"verdict": "VIOLATION" if w.balance_checks()[1] else "NO_VIOLATION", "finding": "Any flag counts as a violation."},
                      "Tap rule": {"verdict": rule.judge(w, 30)["verdict"], "finding": "Reads the traffic tap on days with raised power."},
                      "Script": {"verdict": s["verdict"], "finding": s["why"] + " (%d points)" % s["points"]}}
    for name, folder in folders.items():
        a = model_answer(folder, case)
        if a:
            out["answers"][name] = a
    return out


def build_cases():
    hand = {w.name: w for w in world.scenarios(1, ext=True)}
    models = {"Sol": "results_sol_seed1", "Terra": "results_terra", "Luna": "results_luna", "Opus (told it is a simulation)": "results_opus_26"}
    cases = [export(hand["H3-big-batch"], "Site 1", "A site with one very large job in its log.", models),
             export(hand["C2-split"], "Site 2", "A site with six fine-tuning customers who all started on the same day.", models),
             export(hand["C4-hidden-cluster"], "Site 3", "A site whose paperwork and deliveries don't quite match.", models),
             export(hand["E1-no-line-relabelled"], "Site 4", "A site running a long internal job during the audit.", models),
             export(gen.case(6, mess=True), "Site 5", "A generated site with everyday mess: lost logs, a swapped meter, chips in maintenance.",
                    {"Sol": "results_sol_mess"})]
    run.REAL = run.EXT = True
    data = {"threshold": world.THRESHOLD, "budget": 30, "prompt": run.system_prompt(), "cases": cases,
            "script_doc": script.__doc__, "recipe_doc": gen.__doc__}
    json.dump(data, open(os.path.join(HERE, "cases.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print("cases.json: %d KB" % (os.path.getsize(os.path.join(HERE, "cases.json")) // 1024))


# ------------------------------------------------------------------ plots
THEMES = {"light": {"ink": "#16181D", "ink2": "#3A3F4B", "muted": "#6B7080", "grid": "#D5D9E0", "surface": "#FFFFFF",
                    "good": "#0ca30c", "und": "#B9BEC9", "blocked": "#E9EBF0", "bad": "#d03b3b", "s1": "#2a78d6", "s2": "#eb6834"},
          "dark": {"ink": "#F0EFEC", "ink2": "#C9D1E3", "muted": "#9AA2B5", "grid": "#39415A", "surface": "#232B3D",
                   "good": "#0ca30c", "und": "#6B7388", "blocked": "#39415A", "bad": "#e66767", "s1": "#3987e5", "s2": "#d95926"}}


def style(t):
    plt.rcParams.update({"font.family": ["Inter", "Segoe UI", "DejaVu Sans"], "font.size": 11, "text.color": t["ink"],
                         "axes.labelcolor": t["ink2"], "xtick.color": t["muted"], "ytick.color": t["ink"],
                         "axes.edgecolor": t["grid"], "figure.facecolor": t["surface"], "axes.facecolor": t["surface"],
                         "savefig.facecolor": t["surface"], "hatch.color": t["muted"], "hatch.linewidth": 0.6})


def outcomes(name, t):
    """What each method said on the 26 hand-built cases (seeds 1 and 2, extended instruments)."""
    rows = ["Fixed checks over the records", "Tap rule", "Luna (language model)", "Terra (language model)",
            "Sol (language model)", "Opus (language model, told it is a simulation)", "Script of fixed rules"]
    #            right, undetermined, blocked, wrong, not run
    cheat = [(10, 0, 0, 4, 0), (6, 0, 0, 8, 0), (3, 11, 0, 0, 0), (5, 9, 0, 0, 0), (7, 7, 0, 0, 0), (8, 0, 5, 0, 1), (14, 0, 0, 0, 0)]
    honest = [(6, 0, 0, 6, 0), (12, 0, 0, 0, 0), (0, 12, 0, 0, 0), (9, 3, 0, 0, 0), (12, 0, 0, 0, 0), (9, 0, 1, 0, 2), (12, 0, 0, 0, 0)]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6), sharey=True, gridspec_kw={"width_ratios": [14, 12], "wspace": 0.06})
    parts = [("Right answer", t["good"], None), ("Undetermined", t["und"], None), ("Blocked by the model's safety filter", t["blocked"], "////"),
             ("Wrong answer", t["bad"], None), ("Not run", t["surface"], None)]
    for ax, data, title, total in ((axes[0], cheat, "14 cheating sites", 14), (axes[1], honest, "12 honest sites", 12)):
        for y, row in enumerate(data):
            left = 0
            for (label, color, hatch), v in zip(parts, row):
                if not v:
                    continue
                edge = t["grid"] if label == "Not run" else t["surface"]
                ax.barh(y, v, left=left, height=0.62, color=color, hatch=hatch, edgecolor=edge, linewidth=1.5)
                dark_text = label in ("Undetermined", "Blocked by the model's safety filter", "Not run")
                ax.text(left + v / 2, y, str(v), ha="center", va="center", fontsize=10.5, fontweight="bold",
                        color=t["ink"] if dark_text else "#ffffff")
                left += v
        ax.set_xlim(0, total)
        ax.set_title(title, loc="left", fontsize=12, fontweight="bold", color=t["ink"], pad=8)
        ax.set_xticks([])
        for s in ax.spines.values():
            s.set_visible(False)
        ax.tick_params(length=0)
    axes[0].set_yticks(range(len(rows)))
    axes[0].set_yticklabels(rows)
    axes[0].invert_yaxis()
    handles = [plt.Rectangle((0, 0), 1, 1, facecolor=c, hatch=h, edgecolor=t["grid"]) for _, c, h in parts]
    fig.legend(handles, [p[0] for p in parts], loc="lower center", ncol=5, frameon=False, fontsize=10, bbox_to_anchor=(0.5, -0.04))
    fig.savefig(os.path.join(HERE, "plots", name), dpi=170, bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)


def mess(name, t):
    """The same 200 generated sites, tidy and messy: 108 cheating, 92 honest."""
    rows = ["Fixed checks", "Sensor rule", "Tap rule", "Script of fixed rules"]
    caught = [(86, 101), (91, 91), (41, 40), (104, 98)]
    accused = [(49, 80), (36, 44), (6, 6), (0, 6)]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), sharey=True, gridspec_kw={"wspace": 0.08})
    for ax, data, title, total in ((axes[0], caught, "Cheating sites caught (of 108): higher is better", 108),
                                   (axes[1], accused, "Honest sites wrongly accused (of 92): lower is better", 92)):
        for y, (a, b) in enumerate(data):
            for k, (v, color) in enumerate(((a, t["s1"]), (b, t["s2"]))):
                yy = y + (k - 0.5) * 0.36
                ax.barh(yy, v, height=0.32, color=color, edgecolor=t["surface"], linewidth=1.5)
                ax.text(v + total * 0.012, yy, str(v), va="center", fontsize=10.5, color=t["ink"])
        ax.set_xlim(0, total * 1.08)
        ax.set_title(title, loc="left", fontsize=12, fontweight="bold", color=t["ink"], pad=8)
        ax.set_xticks([0, total // 2, total])
        ax.grid(axis="x", color=t["grid"], linewidth=0.8)
        ax.set_axisbelow(True)
        for s in ax.spines.values():
            s.set_visible(False)
        ax.tick_params(length=0)
    axes[0].set_yticks(range(len(rows)))
    axes[0].set_yticklabels(rows)
    axes[0].invert_yaxis()
    handles = [plt.Rectangle((0, 0), 1, 1, facecolor=t["s1"]), plt.Rectangle((0, 0), 1, 1, facecolor=t["s2"])]
    fig.legend(handles, ["Tidy sites", "The same sites with everyday mess"], loc="lower center", ncol=2, frameon=False,
               fontsize=10, bbox_to_anchor=(0.5, -0.05))
    fig.savefig(os.path.join(HERE, "plots", name), dpi=170, bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)


def main():
    os.makedirs(os.path.join(HERE, "plots"), exist_ok=True)
    build_cases()
    for theme, t in THEMES.items():
        style(t)
        outcomes("outcomes_%s.png" % theme, t)
        mess("mess_%s.png" % theme, t)
    print("plots:", sorted(os.listdir(os.path.join(HERE, "plots"))))


if __name__ == "__main__":
    main()
