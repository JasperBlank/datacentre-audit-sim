"""Generated cases: sites sampled from a recipe, so nobody hand-picks which signal decides a case.

    python gen.py --n 200            # score the model-free methods on 200 generated cases
    python gen.py --n 5 --show       # print the truth of five cases

Uses the World class and its channels unchanged. world.scenarios() and its 13 hand-built cases are untouched.
Every number in the recipe is my choice (Claude, 23 Nov 2026); none has a source.

A case is honest with probability 1/2. Every case gets ordinary background work. On top of that:
  honest sites may carry one thing that looks like cheating (a big batch job, several fine-tunes that add up,
    two fine-tunes at the same frequency) and one piece of mess (lost logs, a late payer);
  cheating sites carry one training run over the limit, hidden in one of five ways.
"""
import argparse
import random

import world
from world import CLUSTERS, DAYS, THRESHOLD, World, gpu_hours, job

PARENT = "Borealis Compute Holding BV"
CUSTOMERS = ["Tidewater Robotics", "Ostara Legal", "Halcyon Bio", "Meridian Analytics", "Kestrel Search",
             "Vireo Logistics", "Sundial Media", "Arden Genomics", "Pike & Lathe", "Calloway Maps"]
SHELLS = ["Corvid Labs", "Pallas Systems", "Brightwater AI", "Fennec Data", "Quillon Tech", "Marram Software",
          "Sable Analytics", "Tern Compute"]
CONCEAL = ["relabel-internal", "relabel-shell", "split", "omit", "hidden-cluster"]
LOOKALIKE = [None, "big-batch", "adds-up", "same-frequency"]


class Site:
    """Places jobs on free nodes of a cluster's scheduled pool, so no two jobs share a GPU."""

    def __init__(self, r, snap=False):
        self.r, self.jobs, self.k, self.snap = r, [], r.randint(400, 480), snap

    def new_id(self, prefix):
        self.k += self.r.randint(1, 9)
        return "%s-%04d" % (prefix, self.k)

    def place(self, kind, customer, cluster, n, start_day, days, prefix=None, **kw):
        c = CLUSTERS[cluster]
        lo, hi = (c["inf"] + 1, c["n"]) if cluster != "C" else (1, c["n"])
        if self.snap:          # half-day steps, so the scheduler log's one decimal shows a job's times exactly
            start_day, days = round(start_day * 2) / 2, max(0.5, round(days * 2) / 2)
        j = job(self.new_id(prefix or {"finetune": "ft", "batch": "bt", "training": "run"}[kind]), kind, customer,
                cluster, lo, n, start_day, days, **kw)
        busy = sorted((o["first"], o["first"] + o["n"]) for o in self.jobs
                      if o["cluster"] == cluster and o["start"] < j["end"] and j["start"] < o["end"])
        first = lo
        for a, b in busy:
            if first + n <= a:
                break
            first = max(first, b)
        if first + n - 1 > hi or j["end"] <= j["start"]:
            return None
        j["first"] = first
        self.jobs.append(j)
        return j


RESELLER = "Nordlys Cloud Resale BV"


def case(index, seed=0, real=True, ext=True, mess=False):
    r = random.Random("gen-%d-%d" % (seed, index))
    site, kw, staff = Site(r, snap=mess), {}, {}
    hz = lambda: round(r.uniform(0.35, 1.3), 2)
    cheat = r.random() < 0.5

    # The thing that matters is placed first, so it always gets its nodes.
    truth_only, decl_only, tags = [], [], []
    if cheat:
        how = r.choice(CONCEAL)
        hidden_line = r.random() < 0.4                      # a run built to hide its power line and exchange less
        f = None if hidden_line else hz()
        days = r.uniform(4, 26)
        start = r.uniform(1, DAYS + 1 - days)
        # Hiding has a price: 93 to 267% more compute for the same training (Kimpson, Baker and Graham 2026).
        # So a hidden run is that much larger than the smallest run worth hiding.
        size = THRESHOLD * 1.2 * (r.uniform(1.93, 3.67) if hidden_line else 1.0)
        tags = [how, "hidden line" if hidden_line else "plain line",
                "runs into the audit window" if start + days > 26 else "ends before the audit window"]
        if how == "hidden-cluster":
            if size / (days * 24) > 600:
                days = min(29.0, size / 600 / 24 + 0.5)
                start = r.uniform(1, DAYS + 1 - days)
            n = r.randint(min(600, max(150, int(size / (days * 24)) + 1)), 600)
            run = [site.place("training", "internal", "C", n, start, days, hz=f)]
            kw["has_c"] = True
            staff["inventory|shipped|600|serial|2600|2,600"] = ("We resold 600 units to a partner. The paperwork is "
                                                                "still with their legal team.")
            staff["f3|cooling|storage|expansion"] = "F3 feeds the new cooling plant and a storage hall."
        else:
            where = r.choice(["A", "B", "AB"])
            cap = {"A": 700, "B": 400, "AB": 1100}[where]
            need = int(size / (days * 24)) + 1
            if need > cap:
                days = min(29.0, size * 1.25 / cap / 24)
                start, need = r.uniform(1, DAYS + 1 - days), min(cap, int(size / (days * 24)) + 1)
            n = r.randint(need, cap)
            if where == "AB":
                nb = min(400, max(50, int(n * r.uniform(0.25, 0.45))))
                na = min(700, n - nb)
                run = [site.place("training", "internal", "A", na, start, days, hz=f),
                       site.place("training", "internal", "B", nb, start, days, hz=f)]
                run[1]["fp"] = run[0]["fp"]
            else:
                run = [site.place("training", "internal", where, n, start, days, hz=f)]
            kw["fake_switch"] = tuple(sorted({j["cluster"] for j in run}))
        truth_only = list(run)
        if how == "relabel-internal":
            decl_only = [dict(j, id=site.new_id("bt"), kind="batch") for j in run]
            staff["batch|internal|synthetic|traffic|" + "|".join(j["id"] for j in decl_only)] = (
                "That work is internal: we're generating synthetic evaluation data. It stays on our own storage, "
                "so nothing goes out.")
        elif how == "relabel-shell":
            shell = r.choice(SHELLS)
            decl_only = [dict(j, id=site.new_id("bt"), kind="batch", customer=shell) for j in run]
            kw["payers"] = {shell: PARENT}
            kw["bulk"] = {}
            for j in run:                                        # junk data sent out to mimic results
                for d in range(j["start"] // 24 + 1, (j["end"] - 1) // 24 + 2):
                    hours = len([h for h in world.day_hours(d) if j["start"] <= h < j["end"]])
                    kw["bulk"][d] = kw["bulk"].get(d, 0) + j["n"] * hours * world.TB_PER_BATCH_GPU_HOUR
            staff["holding|batch|" + shell.split()[0].lower()] = (
                "%s is a document-processing client that came through our reseller programme. The holding company "
                "handles payments for that programme." % shell)
        elif how == "split":
            names = r.sample(SHELLS, len(SHELLS))
            for j in run:
                parts = max(2, -(-gpu_hours(j) // int(THRESHOLD * 0.8)))
                size, first = j["n"] // parts, j["first"]
                for p in range(parts):
                    m = size if p < parts - 1 else j["n"] - size * (parts - 1)
                    decl_only.append(dict(j, id=site.new_id("ft"), kind="finetune", customer=names[len(decl_only) % len(names)],
                                          first=first, n=m, hz=None))
                    first += m
            for d in decl_only:
                d["fp"] = d["id"]
            if any(gpu_hours(d) > THRESHOLD for d in decl_only):
                return case(index * 7919 + 1, seed, real, ext, mess)   # a part still over the limit: draw again
            kw["payers"] = {d["customer"]: PARENT for d in decl_only}
            staff["holding|same|together|reseller|" + "|".join(sorted({d["customer"].split()[0].lower() for d in decl_only}))] = (
                "Those customers came through one reseller programme, which is why they started together. The holding "
                "company handles payments for that programme.")
        elif how == "omit":
            staff["power|energy|meter|day"] = ("We ran a cooling stress test with load banks for a while this month, "
                                               "and the meters were recalibrated around then.")
    else:
        look = r.choice(LOOKALIKE)
        tags = [look or "plain"]
        if look == "big-batch":
            internal = r.random() < 0.5
            days = r.uniform(5, 14)
            b = site.place("batch", "internal" if internal else r.choice(CUSTOMERS), r.choice("AB"), r.randint(300, 400),
                           r.uniform(1, DAYS + 1 - days), days)
            if r.random() < 0.6 or internal:                     # results stay on site, or leave in one transfer
                kw["no_stream"] = (b["id"],)
                if not internal:
                    kw["bulk"] = {(b["end"] - 1) // 24 + 1: gpu_hours(b) * world.TB_PER_BATCH_GPU_HOUR}
                staff["batch|traffic|transfer|internal|" + b["id"]] = (
                    "That job's results went onto our own storage." + ("" if internal else " The customer pulled "
                    "everything in one go when it finished."))
        elif look in ("adds-up", "same-frequency"):
            same = hz() if look == "same-frequency" else None
            start = r.uniform(2, 24)
            for c, cust in zip(r.sample(["A", "B", "A"], 3)[:r.choice([2, 3])], r.sample(CUSTOMERS, 3)):
                days = r.uniform(2.5, 4)
                n = min(380, int(THRESHOLD * r.uniform(0.6, 0.95) / (days * 24)))
                site.place("finetune", cust, c, n, start if same else r.uniform(2, 26), days, hz=same or hz())
            if same:
                staff["same|frequency|together"] = ("Those customers use the same open-source training stack with its "
                                                    "default settings. They don't know each other as far as we can tell.")

    # Ordinary background work on every site.
    for _ in range(r.randint(1, 4)):
        days = r.uniform(1, 4)
        n = min(r.randint(50, 300), int(THRESHOLD * 0.9 / (days * 24)))
        site.place("finetune", r.choice(CUSTOMERS), r.choice("AB"), n, r.uniform(1, DAYS + 1 - days), days, hz=hz())
    for _ in range(r.randint(0, 2)):
        days = r.uniform(1, 4)
        site.place("batch", r.choice(CUSTOMERS), r.choice("AB"), r.randint(80, 250), r.uniform(1, DAYS + 1 - days), days)

    # Mess that honest and cheating sites share.
    if r.random() < 0.25:
        d = r.randint(2, DAYS - 4)
        kw["log_gap"] = tuple(range(d, d + r.randint(2, 4)))
        staff["log|storage|" + "|".join(map(str, kw["log_gap"]))] = (
            "The logging server's disk died on day %d. The jobs themselves kept running; we just lost the records "
            "for those days." % d)
        tags.append("lost logs")
    truth = [j for j in site.jobs if j]
    hidden_ids = {id(j) for j in truth_only}
    declared = [j for j in truth if id(j) not in hidden_ids] + decl_only
    if r.random() < 0.25:
        late = r.choice(["Northwind Apps", "Lumen Health", "Kestrel Search"])
        kw["unpaid"] = (late,)
        staff["unpaid|late|" + late.split()[0].lower()] = "%s always pays about six weeks late. We've chased them." % late
        tags.append("late payer")

    # Instruments can fail on any site; a cheater may blind one or withhold chips. Added 24 Nov 2026.
    inst = [("power", f) for f in ["F0", "F1", "F2"] + (["F3"] if kw.get("has_c") else [])] + [("tap", l) for l in ("A", "B", "A-B")]
    outage, tamper, seals, refuse = {}, set(), set(), []
    why = "Those racks are in a firmware maintenance window this week."
    if r.random() < 0.2:                                        # an honest failure, logged by the instrument itself
        d = r.randint(1, DAYS - 3)
        outage[r.choice(inst)] = set(range(d, d + r.randint(1, 3)))
        tags.append("instrument outage")
    if cheat:
        own = [("power", CLUSTERS[j["cluster"]]["feed"]) for j in run] + [("tap", j["cluster"]) for j in run if j["cluster"] != "C"]
        if r.random() < 0.3:
            k = r.choice(own)
            tamper.add(k)
            if k[0] == "tap" and len(run) == 2:
                tamper.add(("tap", "A-B"))
            if r.random() < 0.7:                                 # blinding an instrument usually breaks its seal
                seals.add(k)
            tags.append("blinded %s %s%s" % (k[0], k[1], "" if k in seals else " without breaking the seal"))
        live = [j for j in run if j["cluster"] != "C" and j["end"] > world.WINDOW[0]]
        if live and r.random() < 0.5:
            refuse = [(j["cluster"], j["first"], j["first"] + j["n"] - 1, why) for j in live]
            tags.append("withholds chips")
    else:
        if r.random() < 0.05:
            seals.add(r.choice(inst))
            tags.append("seal broken by accident")
        if r.random() < 0.15:
            c = r.choice("AB")
            a = r.randint(CLUSTERS[c]["inf"] + 1, CLUSTERS[c]["n"] - 150)
            refuse = [(c, a, a + r.randint(40, 150), why)]
            tags.append("chips in maintenance")
    kw.update(custody=True, outage=outage, tamper=tamper, seals=seals, probe_refuse=refuse)

    # Mess (mess=True), added 24 Nov 2026. It breaks two things the tidy recipe guarantees: that a shell customer is
    # always paid for by the operator's parent, and that an honest site has no load its records don't explain.
    # Drawn from its own random stream, so case N is the same site with and without mess (job times aside).
    if mess:
        rm = random.Random("mess-%d-%d" % (seed, index))
        cl = lambda: rm.choice("AB")
        # Who pays. Shells may pay from their own account or through a reseller, and may look ordinary in the
        # register. Real customers may be paid for by a reseller, and one may be an affiliate of the operator.
        shells, payers = set(kw.get("payers", {})), dict(kw.get("payers", {}))
        if shells:
            how_paid = rm.random()
            if how_paid < 0.35:
                payers = {}
                tags.append("shells pay for themselves")
            elif how_paid < 0.55:
                payers = {s: RESELLER for s in shells}
                tags.append("shells paid via a reseller")
            if rm.random() < 0.4:
                kw["clean_shells"] = set(shells)
                tags.append("shells look ordinary")
        real_c = sorted({j["customer"] for j in declared if j["customer"] != "internal" and j["customer"] not in shells})
        if len(real_c) >= 2 and rm.random() < 0.35:
            for c in rm.sample(real_c, min(len(real_c), rm.randint(2, 3))):
                payers[c] = RESELLER
            tags.append("customers paid via a reseller")
        if real_c and rm.random() < 0.1:
            payers[rm.choice(real_c)] = PARENT
            tags.append("an affiliate is a customer")
        if RESELLER in payers.values() or PARENT in payers.values():
            staff["reseller|nordlys|holding|pays|payment"] = (
                "Some customers buy through Nordlys Cloud Resale, which pays us on their behalf, and the holding "
                "company settles the bills of group companies.")
        kw["payers"], kw["shells"] = payers, shells
        # Load the records don't explain, on honest and cheating sites alike.
        burn = "We burned in a batch of replacement GPUs that week. Acceptance tests don't go through the scheduler."
        if rm.random() < 0.25:
            j = site.place("burnin", "internal", cl(), rm.randint(100, 400), rm.uniform(1, 25), rm.choice([1, 1.5, 2, 3, 4, 5]), prefix="bi")
            if j:
                truth.append(j)
                staff["burn|acceptance|replacement|power|energy|meter"] = burn
                tags.append("burn-in")
        if rm.random() < 0.12:
            days = rm.choice([1, 2, 3])
            j = site.place("finetune", "internal", cl(), min(rm.randint(100, 350), int(THRESHOLD * 0.8 / (days * 24))),
                           rm.uniform(1, 27), days, prefix="adhoc", hz=hz())
            if j:
                truth.append(j)
                staff["adhoc|ssh|engineer|unlogged|outside the scheduler"] = (
                    "One of our engineers ran a test fine-tune directly on the nodes, outside the scheduler. "
                    "We've told him not to.")
                tags.append("unlogged test run")
        if cheat and how == "omit" and rm.random() < 0.5:      # a cheater can borrow the honest excuse
            staff = {k: v for k, v in staff.items() if not k.startswith("power|energy|meter|day")}
            staff["burn|acceptance|replacement|power|energy|meter"] = burn
        # The site itself.
        if rm.random() < 0.15:
            f, d = rm.choice(["F1", "F2"]), rm.randint(5, 25)
            kw["meter_step"] = {f: (d, rm.uniform(1.03, 1.06))}
            staff["recalibrat|swap|meter %s|%s" % (f.lower(), f.lower())] = "The grid operator swapped the meter on %s around day %d." % (f, d)
            tags.append("meter swapped")
        if rm.random() < 0.2:
            d = rm.randint(2, 24)
            kw["surge"] = {cl(): (d, d + rm.randint(2, 6), rm.uniform(1.2, 1.5))}
            staff["surge|launch|demand|inference"] = "One of our inference customers launched a product that week and demand jumped."
            tags.append("inference surge")
        if rm.random() < 0.15:
            d = rm.randint(2, 27)
            kw["downtime"] = {cl(): (d, d + rm.randint(0, 2), rm.uniform(0.2, 0.5))}
            staff["shutdown|repair|cooling|down"] = "We took part of a cluster down for a cooling repair for a day or two."
            tags.append("partial shutdown")
        # Logs that are slightly wrong: a job ran half a day or a day off from what the scheduler recorded.
        for i, j in enumerate(declared):
            if any(j is t for t in truth) and rm.random() < 0.15:
                shift = rm.choice([-24, -12, 12, 24])
                if j["start"] + shift >= 0 and j["end"] + shift <= world.HOURS:
                    declared[i] = dict(j, start=j["start"] + shift, end=j["end"] + shift)
                    tags.append("a log time is off")

    note = ("Cheating: " if cheat else "Honest: ") + ", ".join(tags) + "."
    return World(("M%04d" if mess else "G%04d") % index, seed, truth, declared, violation=cheat, note=note, staff=dict(staff, **world.BASE_STAFF),
                 real=real or ext, ext=ext, **kw)


def cases(n, seed=0, real=True, ext=True, mess=False):
    return [case(i, seed, real, ext, mess) for i in range(n)]


def main():
    import rule
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--budget", type=int, default=30)
    ap.add_argument("--show", action="store_true", help="print each case's truth")
    ap.add_argument("--mess", action="store_true", help="the messy recipe: see the mess block in case()")
    args = ap.parse_args()
    m = args.mess
    methods = {"Fixed checks over the records": lambda i: case(i, args.seed, mess=m).balance_checks()[1],
               "Sensor rule (realistic sensor)": lambda i: rule.judge(case(i, args.seed, ext=False, mess=m), args.budget)["verdict"] == "VIOLATION",
               "Tap rule": lambda i: rule.judge(case(i, args.seed, mess=m), args.budget)["verdict"] == "VIOLATION"}
    ws = cases(args.n, args.seed, mess=m)
    answers = {m: [f(i) for i in range(args.n)] for m, f in methods.items()}
    if args.show:
        for i, w in enumerate(ws):
            print("%s | %-70s | largest run %7s | %s" % (w.name, w.note, format(w.largest_run, ","),
                  " ".join("%s=%s" % (m.split()[0], "V" if answers[m][i] else "-") for m in methods)))
    cheats = [i for i, w in enumerate(ws) if w.violation]
    honest = [i for i, w in enumerate(ws) if not w.violation]
    print("%d generated cases, seed %d: %d cheating, %d honest" % (args.n, args.seed, len(cheats), len(honest)))
    print("| Method | Cheaters caught | Honest sites wrongly accused |\n|---|---|---|")
    for m, a in answers.items():
        print("| %s | %d of %d | %d of %d |" % (m, sum(a[i] for i in cheats), len(cheats), sum(a[i] for i in honest), len(honest)))
    print("\nBy kind of case (flagged / cases):")
    kinds = {}
    for i, w in enumerate(ws):
        kinds.setdefault(w.note.split(",")[0].rstrip("."), []).append(i)
    for k in sorted(kinds):
        print("  %-32s %s" % (k, " | ".join("%s %d/%d" % (m.split()[0], sum(answers[m][i] for i in kinds[k]), len(kinds[k]))
                                             for m in methods)))


if __name__ == "__main__":
    main()
