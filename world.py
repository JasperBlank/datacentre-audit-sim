"""A simulated datacentre with a hidden ground truth.

The operator claims: "In the last 30 days, no single coordinated training run used more than
THRESHOLD GPU-hours." Each scenario fixes what really happened (the truth) and what the operator
declares. Evidence channels are either computed from the truth (the operator can't forge them) or
from the operator's declarations (it can).

Time is in hours, 0..719. Day d covers hours (d-1)*24 .. d*24-1. One node = one GPU.
"""
import hashlib
import math
import random

THRESHOLD = 50_000            # GPU-hours
HOURS, DAYS = 720, 30
WINDOW = (600, 719)           # audit window: memory probes only work in these hours (days 26-30)

CLUSTERS = {
    "A": {"feed": "F1", "n": 1200, "inf": 500, "sn0": 100001},
    "B": {"feed": "F2", "n": 800, "inf": 400, "sn0": 101201},
    "C": {"feed": "F3", "n": 600, "inf": 0, "sn0": 102001},   # exists only in the hidden-cluster scenario
}
# kW per GPU. Training and inference reach similar peaks; inference follows daily demand.
P_IDLE = 0.15
P_KIND = {"training": 0.80, "finetune": 0.78, "batch": 0.75,
          "burnin": 0.80}     # burn-in: new GPUs run flat out for acceptance; no network traffic, not in the scheduler
PARENT = "Borealis Compute Holding BV"
OVERHEAD = 0.20               # cooling etc., as a share of GPU power, on feed F0
TB_PER_INF_GPU_HOUR = 0.0004  # outbound traffic of interactive inference at full load
TB_PER_BATCH_GPU_HOUR = 0.0003
EUR_PER_GPU_HOUR = 2.0
EW_GBPS_PER_TRAIN_NODE = 1.0  # traffic between GPUs during training (inference: about zero)

# Realistic instruments (World(real=True)), added 23 Nov 2026. Sources are in README.md.
P_LINE_DAY = 0.96             # a training run's line is found on this share of its days (paper: at least 96%)
P_LINE_DAY_HIDDEN = 0.87      # same for a run built to hide its line (paper: at least 87% still caught over a day)
HIDDEN_VISIBLE = (0.27, 0.50) # share of the day a hidden run's line shows (paper: hidden in up to 73% of windows)
P_BATCH_CYCLE = 0.5           # share of batch inference jobs that are periodic too (my choice; the paper gives no rate)
P_CONFOUND_DAY = 0.97         # a periodic non-training load shows a line on this share of its days (paper: at least 97%)
WANDER = 0.04                 # the line's frequency moves by up to this many Hz from day to day (my choice; no source)
P_COOLING_DAY = 0.15          # days on which the cooling controller on F0 cycles (my choice)
PROBE_ACC = 0.97              # cable current probe, training against inference (cited as 97%)
PROBE_ACC_DISGUISED = 0.65    # same against a disguised workload (my choice, inside the 43-87% cited for chip telemetry)
KW_PER_GPU = (0.15, 0.75, 0.80)  # idle, batch inference, training: told to the detective in the realistic world

# Extra hard-to-fake signals (World(ext=True)), added 23 Nov 2026.
TAP_NOISE = 0.30              # the tap samples links, so its estimate is within this share (my choice)
LIGHT_COMMS = 0.01            # a hidden run also exchanges 100 times less (DiLoCo figure in the interconnect paper)
INF_GBPS_PER_GPU = 1e-5       # inference traffic between machines, about 10 kB/s per GPU (same paper)
CROSS_SHARE = 0.5             # share of a run's traffic that crosses between two clusters it spans (my choice)
P_NO_REPLY = 0.2              # a real customer doesn't answer in time (my choice)


def inf_load(h):
    return 0.55 + 0.20 * math.sin(2 * math.pi * ((h % 24) - 9) / 24)


def p_inf(h):
    return P_IDLE + 0.55 * inf_load(h)


def day_hours(d):
    return range((d - 1) * 24, d * 24)


def job(id, kind, customer, cluster, first, n, start_day, days, fp=None, hz=None):
    start = int(round((start_day - 1) * 24))
    return {"id": id, "kind": kind, "customer": customer, "cluster": cluster, "first": first, "n": n,
            "start": start, "end": min(HOURS, start + int(round(days * 24))), "fp": fp or id, "hz": hz}


def gpu_hours(j):
    return j["n"] * (j["end"] - j["start"])


class World:
    """Truth plus the operator's declarations for one scenario."""

    def __init__(self, name, seed, truth, declared, violation, note, has_c=False, log_gap=(), unpaid=(),
                 payers=None, bulk=None, staff=None, fake_switch=(), no_stream=(), real=False, ext=False,
                 custody=False, outage=None, tamper=(), seals=(), probe_refuse=(),
                 shells=None, clean_shells=(), meter_step=None, surge=None, downtime=None):
        self.name, self.seed, self.truth, self.declared = name, seed, truth, declared
        self.real = real                     # realistic instruments: weaker power sensor, cable probe
        self.ext = ext                       # plus log escrow, interconnect tap and customer check
        self.channels = CHANNELS_CUSTODY if custody else CHANNELS_EXT if ext else CHANNELS_REAL if real else CHANNELS
        # Added 24 Nov 2026, all off by default. Instruments are named ("power", feed) or ("tap", link).
        self.outage = outage or {}           # instrument -> days on which it gave no data (an honest failure)
        self.tamper = set(tamper)            # instruments the operator has blinded: they read as if nothing ran
        self.seals = set(seals)              # instruments whose seal was found broken at the closing inspection
        self.probe_refuse = tuple(probe_refuse)   # (cluster, first node, last node, reason): chips the operator won't present
        # Mess, added 24 Nov 2026, all off by default.
        self.shells = None if shells is None else set(shells)   # customers the operator controls (None: whoever the parent pays for)
        self.clean_shells = set(clean_shells)     # shells set up with care: their register entry looks ordinary
        self.meter_step = meter_step or {}        # feed -> (day, factor): the grid operator swapped or recalibrated a meter
        self.surge = surge or {}                  # cluster -> (first day, last day, factor): inference demand jumped
        self.downtime = downtime or {}            # cluster -> (first day, last day, share): part of a cluster was switched off
        self.violation, self.note, self.has_c = violation, note, has_c
        self.log_gap = set(log_gap)          # days whose scheduler logs are "lost"
        self.unpaid = set(unpaid)            # customers whose invoice is still open
        self.payers = payers or {}           # customer -> account holder that paid
        self.bulk = bulk or {}               # day -> TB delivered in one transfer
        self.staff = staff or {}
        self.fake_switch = set(fake_switch)  # clusters whose switch counters the operator edited
        self.no_stream = set(no_stream)      # truth job ids that send nothing out while running
        self.clusters = [c for c in CLUSTERS if c != "C" or has_c]
        runs = {}
        for j in truth:
            if j["kind"] in ("training", "finetune"):
                runs[j["fp"]] = runs.get(j["fp"], 0) + gpu_hours(j)
        self.largest_run = max(runs.values(), default=0)
        assert (self.largest_run > THRESHOLD) == violation, (name, self.largest_run)

    # ---------------------------------------------------------------- truth helpers
    def _rng(self, *key):
        return random.Random(hashlib.md5(repr((self.seed, self.name) + key).encode()).hexdigest())

    def state(self, cluster, i, h, jobs=None):
        """What node i (1-based) of a cluster is doing at hour h."""
        for j in (self.truth if jobs is None else jobs):
            if j["cluster"] == cluster and j["first"] <= i < j["first"] + j["n"] and j["start"] <= h < j["end"]:
                return j
        return "inference" if i <= CLUSTERS[cluster]["inf"] else "idle"

    def _feed_kw(self, cluster, h, jobs):
        c = CLUSTERS[cluster]
        busy, kw = 0, 0.0
        for j in jobs:
            if j["cluster"] == cluster and j["start"] <= h < j["end"]:
                busy += j["n"]
                kw += j["n"] * P_KIND[j["kind"]]
        total = kw + c["inf"] * p_inf(h) + (c["n"] - c["inf"] - busy) * P_IDLE
        if jobs is self.truth and (self.surge or self.downtime):   # mess shows in what happened, not in what was declared
            day = h // 24 + 1
            s, dn = self.surge.get(cluster), self.downtime.get(cluster)
            if s and s[0] <= day <= s[1]:
                total += c["inf"] * 0.55 * (min(1.0, inf_load(h) * s[2]) - inf_load(h))
            if dn and dn[0] <= day <= dn[1]:
                total -= dn[2] * (c["inf"] * p_inf(h) + (c["n"] - c["inf"] - busy) * P_IDLE)
        return total

    def feed_mwh(self, cluster, d, jobs=None):
        jobs = self.truth if jobs is None else jobs
        return sum(self._feed_kw(cluster, h, jobs) for h in day_hours(d)) / 1000

    def metered(self, feed, d):
        """Daily MWh at the utility's meter, with 1% noise."""
        noise = 1 + self._rng("meter", feed, d).uniform(-0.01, 0.01)
        step = self.meter_step.get(feed)
        if step and d >= step[0]:
            noise *= step[1]
        if feed == "F0":
            return OVERHEAD * sum(self.feed_mwh(c, d) for c in ("A", "B")) * noise
        cluster = {"F1": "A", "F2": "B", "F3": "C"}[feed]
        return self.feed_mwh(cluster, d) * (1 + OVERHEAD if feed == "F3" else 1) * noise

    def feeds(self):
        return ["F0", "F1", "F2"] + (["F3"] if self.has_c else [])

    def outbound_tb(self, d, jobs=None, declared=False):
        """Daily outbound traffic. With declared=True: what the declared jobs should have produced."""
        jobs = self.truth if jobs is None else jobs
        tb = sum(CLUSTERS[c]["inf"] * inf_load(h) * TB_PER_INF_GPU_HOUR for c in ("A", "B") for h in day_hours(d))
        for j in jobs:
            if j["kind"] == "batch" and (declared or j["id"] not in self.no_stream):
                hours = len([h for h in day_hours(d) if j["start"] <= h < j["end"]])
                tb += j["n"] * hours * TB_PER_BATCH_GPU_HOUR
        if not declared:
            for c, s in self.surge.items():
                if s[0] <= d <= s[1]:
                    tb += sum(CLUSTERS[c]["inf"] * (min(1.0, inf_load(h) * s[2]) - inf_load(h)) * TB_PER_INF_GPU_HOUR for h in day_hours(d))
            tb += self.bulk.get(d, 0)
            tb *= 1 + self._rng("isp", d).uniform(-0.02, 0.02)
        return tb

    def invoices(self):
        """customer -> (invoiced, paid, payer), from the operator's invoices and the bank's records."""
        out = {}
        for cust in ("Northwind Apps", "Lumen Health", "Kestrel Search"):
            out[cust] = 150_000.0
        for j in self.declared:
            if j["customer"] != "internal":
                out[j["customer"]] = out.get(j["customer"], 0) + gpu_hours(j) * EUR_PER_GPU_HOUR
        return {c: (v, 0.0 if c in self.unpaid else v, self.payers.get(c, c)) for c, v in out.items()}

    # ---------------------------------------------------------------- channels
    # Each returns text. `who` in CHANNELS says who vouches for it.
    def ch_system_list(self, **_):
        lines = ["Operator's system list (Borealis Compute, site Eemshaven):"]
        for c in ("A", "B"):
            k = CLUSTERS[c]
            lines.append("- Cluster %s: nodes %s-0001 to %s-%04d, power feed %s. Nodes 1-%d are the interactive "
                         "inference pool; the rest run scheduled jobs." % (c, c, c, k["n"], k["feed"], k["inf"]))
        lines.append("- Feed F0: cooling and facility overhead.")
        if self.has_c:
            lines.append("- Feed F3: cooling and storage expansion, commissioned this month (no GPUs).")
        return "\n".join(lines)

    def ch_scheduler_log(self, first_day=1, last_day=DAYS, **_):
        first_day, last_day = max(1, int(first_day)), min(DAYS, int(last_day))
        lines = ["Scheduler log, days %d-%d (operator's records):" % (first_day, last_day)]
        lo, hi = (first_day - 1) * 24, last_day * 24
        for j in self.declared:
            if j["start"] < hi and j["end"] > lo:
                if all(d in self.log_gap for d in range(j["start"] // 24 + 1, (j["end"] - 1) // 24 + 2)):
                    continue
                lines.append("- %s | %s | customer: %s | nodes %s-%04d to %s-%04d (%d) | day %.1f to day %.1f | %s GPU-hours"
                             % (j["id"], j["kind"], j["customer"], j["cluster"], j["first"], j["cluster"],
                                j["first"] + j["n"] - 1, j["n"], j["start"] / 24 + 1, j["end"] / 24 + 1,
                                format(gpu_hours(j), ",")))
        if len(lines) == 1:
            lines.append("- no scheduled jobs in this range (the interactive inference pools run continuously)")
        gap = sorted(d for d in self.log_gap if first_day <= d <= last_day)
        if gap:
            lines.append("NOTE: log entries for days %s are unavailable (storage failure on the logging server)."
                         % ", ".join(map(str, gap)))
        return "\n".join(lines)

    def ch_staff(self, question="", **_):
        q = question.lower()
        for keys, answer in self.staff.items():
            if any(k in q for k in keys.split("|")):
                return "Operations lead: " + answer
        return "Operations lead: I'd have to check on that. Nothing unusual comes to mind."

    def ch_switch_counters(self, cluster="A", day=1, **_):
        cluster, day = str(cluster).upper(), int(day)
        if cluster not in ("A", "B"):
            return "No switch counters for cluster %r in the operator's monitoring." % cluster
        h = (day - 1) * 24 + 12
        nodes = sum(j["n"] for j in self.truth if j["cluster"] == cluster and j["start"] <= h < j["end"]
                    and j["kind"] in ("training", "finetune"))
        if cluster in self.fake_switch:
            nodes = sum(j["n"] for j in self.declared if j["cluster"] == cluster and j["start"] <= h < j["end"]
                        and j["kind"] in ("training", "finetune"))
        return ("Switch counters, cluster %s, day %d (operator's monitoring): average traffic between GPUs %.1f GB/s."
                % (cluster, day, nodes * EW_GBPS_PER_TRAIN_NODE + self._rng("sw", cluster, day).uniform(0, 0.5)))

    def ch_utility_energy(self, first_day=1, last_day=DAYS, **_):
        first_day, last_day = max(1, int(first_day)), min(DAYS, int(last_day))
        lines = ["Utility meter, daily MWh per feed (grid operator's records):", "day | " + " | ".join(self.feeds())]
        for d in range(first_day, last_day + 1):
            lines.append("%d | %s" % (d, " | ".join("%.1f" % self.metered(f, d) for f in self.feeds())))
        return "\n".join(lines)

    def ch_inventory(self, **_):
        n = sum(CLUSTERS[c]["n"] for c in self.clusters)
        lines = ["Manufacturer's shipment records for Borealis Compute: %d GPUs delivered to the Eemshaven site." % n]
        for c in self.clusters:
            k = CLUSTERS[c]
            lines.append("- serials SN%d to SN%d (%d units)" % (k["sn0"], k["sn0"] + k["n"] - 1, k["n"]))
        return "\n".join(lines)

    def ch_outbound_traffic(self, first_day=1, last_day=DAYS, **_):
        first_day, last_day = max(1, int(first_day)), min(DAYS, int(last_day))
        return "\n".join(["Internet provider's records, outbound TB per day:"] +
                         ["day %d: %.1f" % (d, self.outbound_tb(d)) for d in range(first_day, last_day + 1)])

    def ch_bank_payments(self, **_):
        lines = ["Invoices (operator) against payments received (bank's records):",
                 "customer | invoiced EUR | paid EUR | paying account holder"]
        for c, (inv, paid, payer) in sorted(self.invoices().items()):
            lines.append("%s | %s | %s | %s" % (c, format(int(inv), ","), format(int(paid), ","),
                                               payer if paid else "(no payment received)"))
        return "\n".join(lines)

    def ch_power_spectrum(self, feed="F1", day=1, **_):
        feed, day = str(feed).upper(), int(day)
        if feed not in self.feeds():
            return "No such feed: %s." % feed
        if not 1 <= day <= DAYS:
            return "Day must be 1-%d." % DAYS
        if day in self.outage.get(("power", feed), ()):
            return ("High-rate power meter (verifier's own sensor), feed %s, day %d: no data. The sensor on this feed "
                    "recorded nothing that day." % (feed, day))
        if ("power", feed) in self.tamper:   # a filter fitted between the feed and the sensor
            return "High-rate power meter (verifier's own sensor), feed %s, day %d: no periodic line." % (feed, day)
        if self.real:
            return self._spectrum_real(feed, day)
        lines = []
        cluster = {"F1": "A", "F2": "B", "F3": "C"}.get(feed)
        for j in self.truth:
            if j["cluster"] == cluster and j["hz"]:
                hours = len([h for h in day_hours(day) if j["start"] <= h < j["end"]])
                r = self._rng("spec", feed, day, j["id"])
                if hours >= 12 and r.random() < 0.96:
                    lines.append("- line at %.2f Hz, steady for about %d hours, load consistent with roughly %d GPUs"
                                 % (j["hz"], hours, round(j["n"] * r.uniform(0.85, 1.15), -1)))
        r = self._rng("specfa", feed, day)
        if r.random() < 0.01:
            lines.append("- weak line at %.2f Hz, about 2 hours, roughly 20 GPUs" % r.uniform(0.3, 1.5))
        head = "High-rate power meter (verifier's own sensor), feed %s, day %d: " % (feed, day)
        return head + ("periodic lines found\n" + "\n".join(lines) if lines else
                       "no periodic line. Power varies smoothly or stays flat.")

    # ---- realistic instruments
    def _hidden(self, j):
        """A training run built to hide its line (the scenarios mark it with hz=None)."""
        return j["kind"] not in ("batch", "burnin") and not j["hz"]

    def _cycle(self, j):
        """Frequency of the periodic load cycle a job carries, or None. Some batch inference is periodic too."""
        if j["kind"] == "burnin":
            return None
        if j["kind"] != "batch":
            return j["hz"] or round(self._rng("hz", j["fp"]).uniform(0.5, 1.4), 2)
        periodic = self._rng("cyc", j["id"]).random() < P_BATCH_CYCLE
        return round(self._rng("hz", j["id"]).uniform(0.5, 1.4), 2) if periodic else None

    def _spectrum_real(self, feed, day):
        """A line says 'something periodic ran here'. No GPU count, and the frequency wanders from day to day."""
        lines = []
        cluster = {"F1": "A", "F2": "B", "F3": "C"}.get(feed)
        for j in self.truth:
            hz = self._cycle(j)
            if j["cluster"] != cluster or not hz:
                continue
            hours = len([h for h in day_hours(day) if j["start"] <= h < j["end"]])
            r = self._rng("spec", feed, day, j["id"])
            p = P_LINE_DAY_HIDDEN if self._hidden(j) else P_LINE_DAY if j["kind"] != "batch" else P_CONFOUND_DAY
            if hours >= 12 and r.random() < p:
                f = hz + self._rng("wander", j["fp"], day).uniform(-WANDER, WANDER) + r.uniform(-0.02, 0.02)
                if self._hidden(j):
                    lines.append("- weak line near %.2f Hz, on and off for about %d hours"
                                 % (f, round(hours * r.uniform(*HIDDEN_VISIBLE))))
                else:
                    lines.append("- line near %.2f Hz, steady for about %d hours" % (f, hours))
        r = self._rng("cool", day)
        if feed == "F0" and r.random() < P_COOLING_DAY:
            lines.append("- line near %.2f Hz, steady for about %d hours"
                         % (self._rng("coolhz").uniform(0.3, 0.5) + r.uniform(-0.02, 0.02), r.randint(3, 24)))
        r = self._rng("specfa", feed, day)
        if r.random() < 0.01:
            lines.append("- weak line near %.2f Hz, on and off for about 2 hours" % r.uniform(0.3, 1.5))
        head = "High-rate power meter (verifier's own sensor), feed %s, day %d: " % (feed, day)
        return head + ("periodic lines found\n" + "\n".join(lines) if lines else "no periodic line.")

    def ch_chip_probe(self, nodes=(), hour=WINDOW[0], **_):
        """A current probe on a GPU's power cable: a guess, training or inference. No run fingerprint."""
        hour = int(hour)
        if not WINDOW[0] <= hour <= WINDOW[1]:
            return ("Probes only work live, during the audit window: hours %d-%d (days 26-30). Hour %d is outside it."
                    % (WINDOW[0], WINDOW[1], hour))
        if isinstance(nodes, str):
            nodes = [nodes]
        lines = ["Cable current probe at hour %d (day %.1f). Each reading is a guess:" % (hour, hour / 24 + 1)]
        for ref in list(nodes)[:5]:
            loc = self._node(ref)
            if not loc:
                lines.append("- %s: no such device" % ref)
            elif loc[0] == "C":
                lines.append("- %s: not on the site list. The operator presents no such device to attach a probe to." % ref)
            else:
                no = next((x for x in self.probe_refuse if x[0] == loc[0] and x[1] <= loc[1] <= x[2]), None)
                if no:
                    lines.append("- %s: not presented. The operator declined: \"%s\" Nodes %s-%04d to %s-%04d are "
                                 "withheld for the whole audit window." % (ref, no[3], no[0], no[1], no[0], no[2]))
                    continue
                s = self.state(loc[0], loc[1], hour)
                if s == "idle":
                    lines.append("- %s: idle" % ref)
                    continue
                if s != "inference" and s["kind"] == "burnin":
                    lines.append("- %s: under steady full load; the pattern matches neither training nor inference" % ref)
                    continue
                training = s != "inference" and s["kind"] != "batch"
                if training and self._hidden(s):     # a disguise fools the same chips every time
                    wrong = self._rng("probe", loc) .random() > PROBE_ACC_DISGUISED
                else:
                    wrong = self._rng("probe", loc, hour).random() > PROBE_ACC
                lines.append("- %s: reads as %s" % (ref, "training" if training != wrong else "inference"))
        if len(nodes) > 5:
            lines.append("(only the first 5 nodes were probed)")
        return "\n".join(lines)

    # ---- extra hard-to-fake signals
    def ch_log_escrow(self, **_):
        """Sealed copies of each day's scheduler log, sent to the verifier at midnight. They show what the operator
        recorded on the day, so a log can't be rewritten or 'lost' afterwards. They don't show whether it was true."""
        lines = ["Log escrow (verifier's archive of the sealed copy the scheduler sent each midnight):",
                 "- a copy was received for every one of days 1-%d" % DAYS]
        gap = sorted(self.log_gap)
        if not gap:
            lines.append("- every copy matches the scheduler log the operator presents now")
            return "\n".join(lines)
        lines.append("- the operator presents no log for days %s; the sealed copies for those days exist and read:"
                     % ", ".join(map(str, gap)))
        lo, hi = (gap[0] - 1) * 24, gap[-1] * 24
        jobs = [j for j in self.declared if j["start"] < hi and j["end"] > lo]
        for j in jobs:
            lines.append("  - %s | %s | customer: %s | nodes %s-%04d to %s-%04d (%d) | day %.1f to day %.1f"
                         % (j["id"], j["kind"], j["customer"], j["cluster"], j["first"], j["cluster"],
                            j["first"] + j["n"] - 1, j["n"], j["start"] / 24 + 1, j["end"] / 24 + 1))
        if not jobs:
            lines.append("  - no scheduled jobs on those days (the interactive inference pools ran as usual)")
        lines.append("- on all other days the copies match the log the operator presents now")
        return "\n".join(lines)

    def _tap_nodes(self, j, day):
        """GPUs' worth of training traffic a job puts on the wire on one day (1 = one GPU of ordinary training)."""
        if j["kind"] in ("batch", "burnin"):
            return 0.0
        share =len([h for h in day_hours(day) if j["start"] <= h < j["end"]]) / 24
        return j["n"] * share * (LIGHT_COMMS if self._hidden(j) else 1)

    def ch_interconnect_tap(self, link="A", day=1, **_):
        """The verifier's own optical tap on a sample of links. Replaces trust in the operator's switch counters."""
        link, day = str(link).upper().replace(" ", ""), int(day)
        if not 1 <= day <= DAYS:
            return "Day must be 1-%d." % DAYS
        key = "A-B" if link in ("A-B", "B-A", "AB") else link
        if day in self.outage.get(("tap", key), ()):
            return "Verifier's optical tap, link %s, day %d: no data. The tap recorded nothing that day." % (key, day)
        blind = ("tap", key) in self.tamper      # the operator moved the run's traffic onto links the tap doesn't sample
        if link in ("A", "B"):
            g = sum(self._tap_nodes(j, day) for j in self.truth if j["cluster"] == link and not blind) * EW_GBPS_PER_TRAIN_NODE
            g += CLUSTERS[link]["n"] * INF_GBPS_PER_GPU
            where, gpus = "links inside cluster %s" % link, CLUSTERS[link]["n"]
        elif link in ("A-B", "B-A", "AB"):
            g = 2000 * INF_GBPS_PER_GPU
            for fp in sorted({j["fp"] for j in self.truth}):
                n = [sum(self._tap_nodes(j, day) for j in self.truth if j["fp"] == fp and j["cluster"] == c) for c in "AB"]
                g += 0 if blind else CROSS_SHARE * min(n) * EW_GBPS_PER_TRAIN_NODE
            where, link, gpus = "links between clusters A and B", "A-B", 2000
        else:
            return ("No tap on %r. Taps sit inside cluster A, inside cluster B and on the links between them "
                    "(link: \"A\", \"B\" or \"A-B\"). The verifier can only tap links on the site list." % link)
        g *= 1 + self._rng("tap", link, day).uniform(-TAP_NOISE, TAP_NOISE)
        per = g / gpus * 1e6                                         # kB/s per GPU
        per = "%.0f kB/s" % per if per < 1000 else "%.0f MB/s" % (per / 1e3) if per < 1e6 else "%.1f GB/s" % (per / 1e6)
        return ("Verifier's optical tap, %s, day %d: about %s GB/s in total over all GPU-to-GPU links there, averaged "
                "over the day. Spread over the %d GPUs those links serve, that is about %s per GPU. (Estimated from a "
                "sample of links.)" % (where, day, ("%.0f" if g >= 10 else "%.1f" if g >= 1 else "%.2f") % g, gpus, per))

    def ch_custody(self, **_):
        """The verifier's own record of its instruments: when each was installed, the seal found at the closing
        inspection, and the days it gave no data. A broken seal doesn't say who broke it or why."""
        lines = ["Custody record (verifier's own installation log and closing inspection, day %d):" % DAYS]
        items = [("power", f) for f in self.feeds()] + [("tap", l) for l in ("A", "B", "A-B")]
        for kind, where in items:
            name = "power sensor on feed %s" % where if kind == "power" else "optical tap, link %s" % where
            seal = "seal found BROKEN" if (kind, where) in self.seals else "seal intact"
            off = sorted(self.outage.get((kind, where), ()))
            lines.append("- %s: installed and sealed by the verifier before day 1; %s; %s" % (
                name, seal, "no data on day%s %s" % ("s" if len(off) > 1 else "", ", ".join(map(str, off))) if off
                else "data on all %d days" % DAYS))
        held = ["nodes %s-%04d to %s-%04d (\"%s\")" % (c, a, c, b, why) for c, a, b, why in self.probe_refuse]
        lines.append("- chip probe: the operator presents chips on request" +
                     ("; withheld for the whole audit window: " + "; ".join(held) if held else "; nothing withheld"))
        return "\n".join(lines)

    def ch_customer_check(self, customer="", **_):
        """The company register (hard to arrange) and the customer's own reply (a controlled customer says what suits)."""
        known = {c: c for c in self.invoices()}
        name = next((c for c in known if c.lower() == str(customer).strip().lower()), None)
        if not name:
            return ("No company called %r is invoiced by this operator. Internal jobs have no customer to ask. "
                    "Invoiced customers: %s." % (customer, ", ".join(sorted(known))))
        r = self._rng("cust", name)
        shell = self.payers.get(name, name) != name if self.shells is None else name in self.shells
        if shell and name in self.clean_shells:       # a shell set up with care: nothing in the register gives it away
            return ("Customer check, %s:\n- Company register: registered %d months ago at a serviced-office address, "
                    "%d employees reported.\n- The customer's reply (same day): \"We confirm the order as invoiced.\""
                    % (name, r.randint(7, 30), r.randint(1, 6)))
        if shell:                                     # a shell: the operator's parent stands behind it
            return ("Customer check, %s:\n- Company register: registered %d weeks ago. Registered address and one director "
                    "are shared with %s. No employees reported.\n- The customer's reply (same day): \"We confirm the "
                    "order as invoiced.\"" % (name, r.randint(5, 12), self.payers[name] if self.shells is None else PARENT))
        head = ("Customer check, %s:\n- Company register: registered %d years ago at its own address, %d employees reported."
                % (name, r.randint(3, 15), r.randint(20, 400)))
        if r.random() < P_NO_REPLY:
            return head + "\n- The customer's reply: none within the audit window."
        words = {"finetune": "fine-tuning", "training": "training", "batch": "batch inference"}
        jobs = ["%s on %d GPUs, day %.1f to day %.1f%s" % (words[j["kind"]], j["n"], j["start"] / 24 + 1, j["end"] / 24 + 1,
                " (we collected the results in one download at the end)" if j["id"] in self.no_stream else "")
                for j in self.truth if j["customer"] == name]
        said = "We ordered: " + "; ".join(jobs) + "." if jobs else "We buy interactive inference from this site, nothing else."
        return head + "\n- The customer's reply: \"%s\"" % said

    def _node(self, ref):
        ref = str(ref).strip().upper()
        if ref.startswith("SN"):
            sn = int(ref[2:])
            for c in self.clusters:
                k = CLUSTERS[c]
                if k["sn0"] <= sn < k["sn0"] + k["n"]:
                    return c, sn - k["sn0"] + 1
            return None
        c, _, i = ref.partition("-")
        if c in ("A", "B") and i.isdigit() and 1 <= int(i) <= CLUSTERS[c]["n"]:
            return c, int(i)
        return None

    def ch_memory_probe(self, nodes=(), hour=WINDOW[0], **_):
        hour = int(hour)
        if not WINDOW[0] <= hour <= WINDOW[1]:
            return ("Probes only work live, during the audit window: hours %d-%d (days 26-30). Hour %d is outside it."
                    % (WINDOW[0], WINDOW[1], hour))
        if isinstance(nodes, str):
            nodes = [nodes]
        lines = ["Sealed memory probe at hour %d (day %.1f):" % (hour, hour / 24 + 1)]
        for ref in list(nodes)[:5]:
            loc = self._node(ref)
            if not loc:
                lines.append("- %s: no such device answers" % ref)
                continue
            s = self.state(loc[0], loc[1], hour)
            if s == "idle":
                lines.append("- %s: idle, no model loaded" % ref)
            elif s == "inference":
                lines.append("- %s: inference. Model weights loaded, serving live requests. No optimiser state." % ref)
            elif s["kind"] == "batch":
                lines.append("- %s: inference, batch generation. No optimiser state or gradients." % ref)
            else:
                peers = sum(j["n"] for j in self.truth if j["fp"] == s["fp"] and j["start"] <= hour < j["end"])
                lines.append("- %s: TRAINING. Optimiser state and gradients in memory. Run fingerprint %s. "
                             "Gradient sync with %d GPUs in total." % (ref, hashlib.md5(s["fp"].encode()).hexdigest()[:8], peers))
        if len(nodes) > 5:
            lines.append("(only the first 5 nodes were probed)")
        return "\n".join(lines)

    # ---------------------------------------------------------------- fixed checks (no judgement)
    def balance_checks(self):
        """Arithmetic comparisons of declared data against third-party records. Returns (text, any_flag)."""
        out, flag = [], False

        def line(name, ok, detail):
            nonlocal flag
            flag = flag or not ok
            out.append("%s %s: %s" % ("PASS" if ok else "FLAG", name, detail))

        shipped = sum(CLUSTERS[c]["n"] for c in self.clusters)
        listed = CLUSTERS["A"]["n"] + CLUSTERS["B"]["n"]
        line("inventory", shipped == listed, "%d GPUs shipped, %d on the system list" % (shipped, listed))

        bad, unknown = [], sorted(self.log_gap)
        for d in range(1, DAYS + 1):
            if d in self.log_gap:
                continue
            for feed, c in (("F1", "A"), ("F2", "B")):
                exp, got = self.feed_mwh(c, d, self.declared), self.metered(feed, d)
                if abs(got - exp) / exp > 0.10:
                    bad.append("%s day %d: metered %.1f MWh, declared jobs explain %.1f" % (feed, d, got, exp))
        detail = "metered energy matches declared jobs within 10% on all checked feed-days"
        if bad:
            detail = "%d feed-days off by more than 10%%, e.g. %s" % (len(bad), "; ".join(bad[:3]))
        if unknown:
            detail += ". Days %s can't be checked: no scheduler log" % ", ".join(map(str, unknown))
        if self.has_c:
            detail += ". Feed F3 is declared as non-GPU load, so it isn't checked against jobs"
        line("energy", not bad and not unknown, detail)

        bad = []
        for d0 in range(1, DAYS + 1, 5):
            days = range(d0, d0 + 5)
            got = sum(self.outbound_tb(d) for d in days)
            exp = sum(self.outbound_tb(d, self.declared, declared=True) for d in days)
            if not 0.7 <= got / exp <= 1.3:
                bad.append("days %d-%d: %.0f TB sent, declared inference implies %.0f" % (d0, d0 + 4, got, exp))
        line("outbound traffic", not bad, "; ".join(bad) or "matches declared inference in every 5-day window")

        open_ = ["%s (EUR %s)" % (c, format(int(inv), ",")) for c, (inv, paid, _) in sorted(self.invoices().items()) if paid < inv]
        line("billing", not open_, "unpaid invoices: " + ", ".join(open_) if open_ else "every invoice is paid in the bank's records")

        big = ["%s (%s GPU-hours)" % (j["id"], format(gpu_hours(j), ",")) for j in self.declared
               if j["kind"] in ("training", "finetune") and gpu_hours(j) > THRESHOLD]
        line("declared job sizes", not big, "over the threshold: " + ", ".join(big) if big else
             "no declared training or fine-tuning job exceeds %s GPU-hours" % format(THRESHOLD, ","))
        return "Fixed balance checks:\n" + "\n".join(out), flag


# name -> (who vouches, cost, argument hint, method)
CHANNELS = {
    "system_list":      ("operator", 1, "{}"),
    "scheduler_log":    ("operator", 1, '{"first_day": 1, "last_day": 30}'),
    "staff":            ("operator", 1, '{"question": "..."}'),
    "switch_counters":  ("operator", 1, '{"cluster": "A", "day": 12}'),
    "utility_energy":   ("grid operator", 1, '{"first_day": 1, "last_day": 30}'),
    "inventory":        ("chip manufacturer", 1, "{}"),
    "outbound_traffic": ("internet provider", 1, '{"first_day": 1, "last_day": 30}'),
    "bank_payments":    ("bank", 1, "{}"),
    "power_spectrum":   ("verifier's own sensor", 2, '{"feed": "F1", "day": 12}'),
    "memory_probe":     ("verifier's own sealed probe", 2, '{"nodes": ["A-0700", "SN101300"], "hour": 610}'),
    "balance_checks":   ("fixed program over the records above", 1, "{}"),
}

CHANNELS_REAL = {k: v for k, v in CHANNELS.items() if k not in ("memory_probe", "balance_checks")}
CHANNELS_REAL["chip_probe"] = ("verifier's own probe on a GPU's power cable, live in days 26 to 30 only", 2,
                               '{"nodes": ["A-0700", "B-0450"], "hour": 610}')
CHANNELS_REAL["balance_checks"] = CHANNELS["balance_checks"]

CHANNELS_EXT = {k: v for k, v in CHANNELS_REAL.items() if k != "balance_checks"}
CHANNELS_EXT["log_escrow"] = ("verifier's own archive of the sealed copy sent each midnight", 1, "{}")
CHANNELS_EXT["interconnect_tap"] = ("verifier's own optical tap", 2, '{"link": "A" | "B" | "A-B", "day": 12}')
CHANNELS_EXT["customer_check"] = ("company register, and the customer itself", 2, '{"customer": "Kestrel Search"}')
CHANNELS_EXT["balance_checks"] = CHANNELS["balance_checks"]

# Added 24 Nov 2026 for generated cases: instruments can fail or be blinded, and the operator can withhold chips.
CHANNELS_CUSTODY = {k: v for k, v in CHANNELS_EXT.items() if k != "balance_checks"}
CHANNELS_CUSTODY["custody"] = ("verifier's own installation log and closing inspection", 1, "{}")
CHANNELS_CUSTODY["balance_checks"] = CHANNELS["balance_checks"]


# ---------------------------------------------------------------- scenarios
def first(specific):
    """Scenario-specific answers are matched before the general ones."""
    return dict(specific, **BASE_STAFF)


BASE_STAFF = {
    "power|energy|meter": "Power follows our inference demand, plus whatever scheduled jobs are running.",
    "train": "We don't run large training here. Customers do some fine-tuning, all well under the limit.",
    "customer|pay|invoice": "Our customers are app companies buying inference, plus a few fine-tuning clients.",
}


def scenarios(seed=0, real=False, ext=False):
    """real=True keeps every site and story the same and swaps in the realistic sensor and probe.
    ext=True does that and adds the log escrow, the interconnect tap and the customer check."""
    r = random.Random(seed)
    s = lambda: r.choice([-1, 0, 1]) if seed else 0     # shift start days a little between seeds
    A0, B0 = CLUSTERS["A"]["inf"] + 1, CLUSTERS["B"]["inf"] + 1
    small = [job("ft-0412", "finetune", "Tidewater Robotics", "A", A0, 100, 4 + s(), 3, hz=0.45),
             job("ft-0419", "finetune", "Ostara Legal", "B", B0, 150, 9 + s(), 2, hz=0.62),
             job("bt-0423", "batch", "Kestrel Search", "A", A0 + 200, 200, 15 + s(), 2)]
    W = []

    def add(name, truth, declared=None, **kw):
        kw.setdefault("staff", dict(BASE_STAFF))
        kw["real"], kw["ext"] = real or ext, ext
        W.append(World(name, seed, truth, truth if declared is None else declared, **kw))

    add("H1-clean", small, violation=False, note="Honest. Inference plus small declared fine-tunes.")

    add("H2-messy", small, violation=False, log_gap=(11, 12, 13), unpaid=("Lumen Health",),
        note="Honest but messy: three days of scheduler logs lost, one customer paying late.",
        staff=first({"log|storage|11|12|13": "The logging server's disk died on day 11. We replaced it on day 14. "
                                  "The jobs themselves kept running; we just lost the records for those days.",
                                  "lumen|unpaid|late": "Lumen Health always pays about six weeks late. We've chased them."}))

    d = 12 + s()
    big = job("bt-0431", "batch", "Meridian Analytics", "A", A0, 700, d, 8)
    add("H3-big-batch", [small[1], big], violation=False, bulk={d + 7: 40.0}, no_stream=("bt-0431",),
        note="Honest. A large batch inference job with flat power, results delivered in one transfer at the end.",
        staff=first({"batch|meridian|bt-0431|traffic|transfer": "Meridian had us label their whole document archive. "
                                  "Results went onto our storage and they pulled everything in one go when it finished."}))

    add("H4-three-finetunes",
        [job("ft-0440", "finetune", "Tidewater Robotics", "A", A0, 350, 6 + s(), 3, hz=0.41),
         job("ft-0447", "finetune", "Ostara Legal", "A", A0 + 350, 300, 8 + s(), 3.5, hz=0.55),
         job("ft-0452", "finetune", "Halcyon Bio", "B", B0, 400, 17 + s(), 2.6, hz=0.66)],
        violation=False, note="Honest. Three separate customers fine-tune, each under the limit; together they exceed it.")

    d = 20 + s()
    tr = job("run-x", "training", "internal", "A", A0, 700, d, 9, hz=0.90)
    add("C1-relabelled", [small[1], tr], [small[1], dict(tr, id="bt-0460", kind="batch")], violation=True,
        fake_switch=("A",), note="Cheating. One training run declared as internal batch inference, still running in the audit window.",
        staff=first({"batch|bt-0460|internal|synthetic|traffic": "bt-0460 is internal: we're generating synthetic "
                                  "evaluation data. It stays on our own storage, so nothing goes out."}))

    d = 22 + s()
    truth = [job("run-y-a", "training", "internal", "A", A0, 700, d, 6.3, fp="run-y", hz=0.90),
             job("run-y-b", "training", "internal", "B", B0, 400, d, 6.3, fp="run-y", hz=0.90)]
    names = ["Corvid Labs", "Pallas Systems", "Brightwater AI", "Fennec Data", "Quillon Tech", "Marram Software"]
    decl = [job("ft-05%02d" % (61 + k), "finetune", names[k], "A", A0 + 175 * k, 175, d, 6.3) for k in range(4)] + \
           [job("ft-05%02d" % (65 + k), "finetune", names[4 + k], "B", B0 + 200 * k, 200, d, 6.3) for k in range(2)]
    add("C2-split", truth, decl, violation=True, payers={n: "Borealis Compute Holding BV" for n in names},
        note="Cheating. One run declared as six fine-tunes for six shell customers, all paid from the operator's parent.",
        staff=first({"corvid|pallas|brightwater|fennec|quillon|marram|six|same|holding":
                                  "Those six came through one reseller programme, which is why they started together. "
                                  "The holding company handles payments for that programme."}))

    d = 5 + s()
    side = job("bt-0471", "batch", "Kestrel Search", "A", A0 + 400, 200, 20 + s(), 2)
    truth = [side, job("run-z-a", "training", "internal", "A", A0, 400, d, 12, fp="run-z", hz=0.85),
             job("run-z-b", "training", "internal", "B", B0, 400, d, 12, fp="run-z", hz=0.85)]
    add("C3-paused", truth, [side], violation=True, fake_switch=("A", "B"),
        note="Cheating. A run that ended before the audit window and was left out of the logs.",
        staff=first({"power|energy|meter|day": "We ran a cooling stress test with load banks for about two weeks "
                                  "early in the month, and the meters were recalibrated around then."}))

    tr = job("run-w", "training", "internal", "C", 1, 600, 3 + s(), 25, hz=0.95)
    add("C4-hidden-cluster", small + [tr], small, violation=True, has_c=True,
        note="Cheating. A third cluster missing from the system list; its power feed is declared as cooling and storage.",
        staff=first({"inventory|shipped|600|serial|2600|2,600": "We resold 600 units to a partner. The paperwork "
                                  "is still with their legal team.",
                                  "f3|cooling|storage|expansion": "F3 feeds the new cooling plant and a storage hall."}))

    # ---- Added 23 Nov 2026, after the first results: cases where the power sensor alone gives the wrong answer.
    # Evasion is modelled as "the periodic line is gone" (hz=None). Published work puts its price at 93-267% more
    # compute; that price is not modelled here beyond the runs being large.
    d = 18 + s()
    tr = job("run-q", "training", "internal", "A", A0, 700, d, 11)
    synth = {"batch|bt-048|internal|synthetic|traffic": "That job is internal: we're generating synthetic "
             "evaluation data. It stays on our own storage, so nothing goes out."}
    add("E1-no-line-relabelled", [small[1], tr], [small[1], dict(tr, id="bt-0480", kind="batch")], violation=True,
        fake_switch=("A",), staff=first(synth),
        note="Cheating. Training declared as internal batch inference, with the power line suppressed, still running in the audit window.")

    d = 8 + s()
    tr = job("run-v", "training", "internal", "A", A0, 700, d, 12)
    add("E2-no-line-paused", [tr], [dict(tr, id="bt-0490", kind="batch", customer="Sable Analytics")], violation=True,
        fake_switch=("A",), payers={"Sable Analytics": "Borealis Compute Holding BV"},
        bulk={day: 700 * 24 * TB_PER_BATCH_GPU_HOUR for day in range(d, d + 12)},
        note="Cheating. Training declared as a customer's batch job, power line suppressed, finished before the audit "
             "window, junk data sent out to mimic results. The customer is paid for by the operator's parent.",
        staff=first({"sable|holding|bt-0490|batch": "Sable Analytics is a document-processing client that came through "
                     "our reseller programme. The holding company handles payments for that programme."}))

    bt = job("bt-0482", "batch", "internal", "A", A0, 700, 18 + s(), 11)
    add("E3-internal-batch", [small[1], bt], violation=False, no_stream=("bt-0482",), staff=first(synth),
        note="Honest twin of E1. A real internal batch inference job; nothing goes out because the results stay on site.")

    d = 25 + s()
    add("E4-same-frequency",
        [job("ft-0501", "finetune", "Tidewater Robotics", "A", A0, 500, d, 3.2, hz=0.50),
         job("ft-0502", "finetune", "Halcyon Bio", "B", B0, 400, d, 3.2, hz=0.50)],
        violation=False, note="Honest. Two separate customers fine-tune at the same time with the same power-line "
                              "frequency; each is under the limit, together they exceed it.",
        staff=first({"same|frequency|0.5|tidewater|halcyon|together": "Both customers use the same open-source "
                     "training stack with its default settings. They don't know each other as far as we can tell."}))

    tr = job("run-m", "training", "internal", "B", B0 + 150, 250, 1, 30, hz=0.80)
    add("E5-whole-month", small + [tr], small, violation=True, fake_switch=("B",),
        note="Cheating. An undeclared run on 250 GPUs for the whole 30 days, so no day is quiet enough to compare with.",
        staff=first({"power|energy|meter|baseline|f2|cluster b": "Cluster B is our older hardware. It idles hot, "
                     "so its baseline draw is higher than you'd expect."}))
    return W
