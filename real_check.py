"""Do the simulator's two physical tests work on real GPU traces?

    python -I real_check.py        # reads real_traces/data, prints one row per phase

Data: Hausenloy and Li's public traces (huggingface.co/datasets/jasminexli/verifier-challenge-traces, CC-BY-4.0),
two rented hosts with two H100s each, eight phases per host, three of them mislabelled on purpose. Only the small
files are used: nvidia-smi at about 1 Hz, NIC counters, NCCL logs, and the labels.

The simulator's script rests on two physical claims:
  A. the traffic tap: training exchanges far more data between GPUs than inference does;
  B. the power sensor: training leaves a periodic line in power; inference follows demand.
Here each is turned into the nearest thing these traces allow, with a threshold set from the simulator's own
reasoning, not fitted to these phases. The truth labels are read only to score.
"""
import csv
import glob
import gzip
import json
import os
import statistics

import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "real_traces", "data", "runs")


def power(path):
    """Per-GPU power series and the sampling interval, from nvidia-smi's CSV."""
    series, times = {}, {}
    with open(path, newline="") as f:
        rows = csv.reader(f)
        next(rows)
        for r in rows:
            if len(r) < 8:
                continue
            try:
                h, m, s = r[0].strip().split(" ")[1].split(":")
                series.setdefault(r[1].strip(), []).append(float(r[7]))
                times.setdefault(r[1].strip(), []).append(int(h) * 3600 + int(m) * 60 + float(s))
            except ValueError:
                continue
    dt = statistics.median(np.diff(times[min(times)])) if times else float("nan")
    return series, dt


def line(series, dt):
    """Strongest periodic line between 0.05 Hz and Nyquist: (frequency, height over the median of the band)."""
    best = (0.0, 0.0)
    for x in series.values():
        x = np.array(x[len(x) // 10:])            # skip the start-up
        if len(x) < 200:
            continue
        x = x - np.convolve(x, np.ones(61) / 61, mode="same")      # remove the slow drift
        spec = np.abs(np.fft.rfft(x * np.hanning(len(x)))) ** 2
        freq = np.fft.rfftfreq(len(x), dt)
        band = freq > 0.05
        k = np.argmax(spec[band])
        ratio = spec[band][k] / np.median(spec[band])
        if ratio > best[1]:
            best = (float(freq[band][k]), float(ratio))
    return best


def nccl_bytes(folder):
    """Size of the NCCL logs, unpacked: how much the two GPUs' processes talked to each other."""
    total = 0
    for p in glob.glob(os.path.join(folder, "nccl_*.log.gz")):
        try:
            with gzip.open(p, "rb") as f:
                while True:
                    chunk = f.read(1 << 20)
                    if not chunk:
                        break
                    total += len(chunk)
        except OSError:
            pass
    return total


def main():
    rows = []
    for run in sorted(os.listdir(ROOT)):
        labels = {}
        for ln in open(os.path.join(ROOT, run, "workload_labels.jsonl"), encoding="utf-8"):
            e = json.loads(ln)
            if e.get("event") == "start":
                labels[e["phase_id"]] = e
        for phase, e in labels.items():
            folder = os.path.join(ROOT, run, "phases", phase)
            if not os.path.exists(os.path.join(folder, "nvsmi.csv")):
                continue
            series, dt = power(os.path.join(folder, "nvsmi.csv"))
            watts = statistics.mean(statistics.mean(x[len(x) // 10:]) for x in series.values())
            swing = statistics.mean(statistics.pstdev(x[len(x) // 10:]) for x in series.values())
            f, ratio = line(series, dt)
            secs = max(len(x) for x in series.values()) * dt
            rows.append({"run": run[-6:], "phase": phase, "truth": e["truth"]["op_type"], "claimed": e["claimed"]["op_type"],
                         "lie": e["truth"] != e["claimed"], "watts": watts, "swing": swing, "dt": dt, "hz": f, "ratio": ratio,
                         "nccl_kb_s": nccl_bytes(folder) / 1000 / secs})
    print("| Host | Phase | Truth | Claimed | W per GPU | Swing (W) | NCCL log kB/s | Strongest line | A: talks like training | B: has a line |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    ok_a = ok_b = 0
    for r in rows:
        a = r["nccl_kb_s"] > 1.0            # inference: the GPUs' processes have nothing to say to each other
        b = r["ratio"] > 50                 # a line that stands 50 times over the band's median
        train = r["truth"] == "training"
        ok_a += a == train
        ok_b += b == train
        print("| %s | %s | %s | %s%s | %.0f | %.0f | %.1f | %.2f Hz, x%.0f | %s | %s |" % (
            r["run"], r["phase"], r["truth"], r["claimed"], " (a lie)" if r["lie"] else "", r["watts"], r["swing"],
            r["nccl_kb_s"], r["hz"], r["ratio"], "yes" if a else "no", "yes" if b else "no"))
    print("\nSampling interval: %.2f s. Test A right on %d of %d phases; test B right on %d of %d."
          % (statistics.median(r["dt"] for r in rows), ok_a, len(rows), ok_b, len(rows)))


if __name__ == "__main__":
    main()
