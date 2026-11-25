"""Do the results depend on the numbers that have no source?

    python sweep.py            # prints the tables and writes sweep.png

Each setting below is one I chose myself, or one a paper gives for a different setup. The sweep changes one at
a time, leaves the rest at their defaults, and scores the three rule-based methods on the same 200 generated
sites (tidy recipe, and the messy one for the script). No model is called.

Not swept: the chip probe's accuracy. Neither rule nor the script reads the probe, so it cannot change these
numbers. See README.md for what the two probe papers say.
"""
import sys

import gen
import rule
import script
import world

N = 200
SETTINGS = [
    # name in world.py, label, values (default marked by position in DEFAULT)
    ("P_BATCH_CYCLE", "Share of batch inference jobs that are periodic", [0.0, 0.2, 0.5, 0.8, 1.0]),
    ("WANDER", "Day-to-day wander of the line's frequency (Hz)", [0.0, 0.02, 0.04, 0.08, 0.15]),
    ("TAP_NOISE", "Error of the traffic tap's estimate (share)", [0.0, 0.15, 0.30, 0.60]),
    ("LIGHT_COMMS", "Traffic of a low-communication run, against normal training", [0.001, 0.01, 0.05, 0.2]),
    ("P_LINE_DAY_HIDDEN", "Days on which a hidden run's line is still found", [0.5, 0.7, 0.87, 0.95]),
]


def flagged(judge_one, worlds):
    v = [judge_one(w) for w in worlds]
    cheats = sum(1 for w in worlds if w.violation)
    return (sum(a for a, w in zip(v, worlds) if w.violation), cheats,
            sum(a for a, w in zip(v, worlds) if not w.violation), len(worlds) - cheats)


def measure():
    tidy, tidy_noext, messy = gen.cases(N), gen.cases(N, ext=False), gen.cases(N, mess=True)
    return {"Sensor rule": flagged(lambda w: rule.judge(w, 30)["verdict"] == "VIOLATION", tidy_noext),
            "Tap rule": flagged(lambda w: rule.judge(w, 30)["verdict"] == "VIOLATION", tidy),
            "Script": flagged(lambda w: script.judge(w)["verdict"] == "VIOLATION", tidy),
            "Script, messy sites": flagged(lambda w: script.judge(w)["verdict"] == "VIOLATION", messy)}


def main():
    out = {}
    for name, label, values in SETTINGS:
        default = getattr(world, name)
        print("\n%s (default %s)" % (label, default))
        print("| Value | " + " | ".join("%s: caught, accused" % m for m in ("Sensor rule", "Tap rule", "Script", "Script, messy sites")) + " |")
        print("|---|---|---|---|---|")
        out[name] = []
        for v in values:
            setattr(world, name, v)
            res = measure()
            out[name].append((v, res))
            print("| %s%s | " % (v, " (default)" if v == default else "") +
                  " | ".join("%d of %d, %d of %d" % r for r in res.values()) + " |")
            sys.stdout.flush()
        setattr(world, name, default)
    plot(out)


def plot(out):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return
    methods = ["Sensor rule", "Tap rule", "Script", "Script, messy sites"]
    colours = ["#b3541e", "#2a6fbb", "#1c7a4a", "#7a5cc2"]
    fig, axes = plt.subplots(2, len(SETTINGS), figsize=(3.4 * len(SETTINGS), 6.2), sharey="row")
    for col, (name, label, values) in enumerate(SETTINGS):
        default = getattr(world, name)
        xs = list(range(len(values)))
        for row, (idx, title) in enumerate(((0, "Cheaters caught (%)"), (2, "Honest sites accused (%)"))):
            ax = axes[row][col]
            for m, c in zip(methods, colours):
                ax.plot(xs, [100 * r[m][idx] / r[m][idx + 1] for _, r in out[name]], marker="o", lw=2, color=c, label=m)
            if default in values:
                ax.axvline(values.index(default), color="#999999", lw=1, ls=":")
            ax.set_xticks(xs)
            ax.set_xticklabels([str(v) for v in values])
            ax.set_ylim(-3, 103)
            ax.grid(axis="y", color="#dddddd", lw=0.6)
            for s in ("top", "right"):
                ax.spines[s].set_visible(False)
            if col == 0:
                ax.set_ylabel(title)
            if row == 0:
                import textwrap
                ax.set_title("\n".join(textwrap.wrap(label, 30)), fontsize=9)
    axes[0][0].legend(fontsize=8, frameon=False, loc="lower left")
    fig.suptitle("One setting changed at a time, 200 generated sites. Dotted line: the value used everywhere else.", fontsize=10)
    fig.tight_layout()
    fig.savefig("sweep.png", dpi=140)


if __name__ == "__main__":
    main()
