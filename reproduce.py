"""Reproduce every table that needs no model call.

    python reproduce.py            # about two minutes; writes reproduce.log

Needs Python 3.10 or later. matplotlib is optional (the sweep's plot); numpy only for the real-trace check, which is
skipped unless the traces have been downloaded (see README.md).

What it runs:
  1. script.py      the script of seven fixed rules against the fixed checks and the tap rule
  2. gen.py         the sensor rule and tap rule on 200 generated sites, tidy and messy
  3. sweep.py       the same methods with each unsourced setting changed in turn
  4. hub.py         the frozen script and the model-revised scripts on practice and unseen sites
  5. real_check.py  the two physical tests on real GPU traces, if the data is there

The language-model runs are not repeated here: they need a ChatGPT or Claude login and are not deterministic.
Their transcripts are in the results_* folders.
"""
import glob
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = [["script.py"], ["gen.py"], ["gen.py", "--mess"], ["sweep.py"], ["hub.py", "baseline"]]
STEPS += [["hub.py", "score", p.replace("\\", "/")] for p in sorted(glob.glob(os.path.join("hub", "script_r*.py")))]
if os.path.isdir(os.path.join(HERE, "real_traces", "data", "runs")):
    STEPS.append(["real_check.py"])

with open(os.path.join(HERE, "reproduce.log"), "w", encoding="utf-8") as log:
    for step in STEPS:
        head = "\n\n===== python %s =====\n" % " ".join(step)
        print(head.strip())
        p = subprocess.run([sys.executable] + step, cwd=HERE, capture_output=True, text=True, encoding="utf-8")
        log.write(head + p.stdout + (("\n[stderr]\n" + p.stderr) if p.returncode else ""))
        print(p.stdout[-1500:] if p.returncode == 0 else "FAILED:\n" + p.stderr[-1500:])
print("\nFull output: reproduce.log")
