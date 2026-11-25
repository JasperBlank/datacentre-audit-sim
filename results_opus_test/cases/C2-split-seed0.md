# C2-split-seed0

Truth: Cheating. One run declared as six fine-tunes for six shell customers, all paid from the operator's parent. Largest coordinated run: 166,100 GPU-hours (limit 50,000). Violation: True.

### Turn 1
ACTION: {"thinking": "Competing explanations: (H1) Honest: no run above 50,000 GPU-hours; logs, energy, and traffic all agree. Check: utility energy vs listed GPUs, escrow vs scheduler log, power spectrum lines matching only small runs. (H2) Honest but messy: lost log days or late payments make records look odd, but the physics shows no large run. Check: escrow vs current log; energy and outbound traffic on the gap days. (H3) Violation by splitting: one big run is labelled or billed as several smaller jobs or customers, possibly shell customers. Check: interconnect tap on the A-B link (cross-cluster training traffic), customer_check against the register, bank_payments, and spectrum lines with continuous frequency across 'separate' jobs. (H4) Violation by hidden hardware: GPUs missing from the system list run a training job. Check: inventory from the manufacturer vs system_list, and utility energy against listed capacity. (H5) Violation by mislabelling: training disguised as batch inference or as low-communication training. Check: chip probe during days 26-30, outbound traffic (low for training), and the tap at the 10 MB/s level. (H6) Innocent periodic sources, such as a cooling controller or batch inference, produce spectrum lines that look like training. Check: chip probe, tap, and outbound traffic. First step: map the systems with the manufacturer inventory.", "action": "inventory", "args": {}}
RESULT:
Manufacturer's shipment records for Borealis Compute: 2000 GPUs delivered to the Eemshaven site.
- serials SN100001 to SN101200 (1200 units)
- serials SN101201 to SN102000 (800 units)

### Turn 2
ACTION: {"thinking": "The manufacturer shipped 2000 GPUs. The next step is to compare that with the operator's system list to find any hardware it hasn't listed.", "action": "system_list", "args": {}}
RESULT:
Operator's system list (Borealis Compute, site Eemshaven):
- Cluster A: nodes A-0001 to A-1200, power feed F1. Nodes 1-500 are the interactive inference pool; the rest run scheduled jobs.
- Cluster B: nodes B-0001 to B-0800, power feed F2. Nodes 1-400 are the interactive inference pool; the rest run scheduled jobs.
- Feed F0: cooling and facility overhead.

### Turn 3
ACTION: {"thinking": "System list (1200 A + 800 B = 2000) matches the manufacturer's 2000 GPUs, so there are no unlisted GPUs and H4 looks unlikely. Scheduled pools are A-0501..1200 (700 GPUs) and B-0401..0800 (400 GPUs). That is enough capacity for a run far above 50,000 GPU-hours (for example, 700 GPUs need only about 72 h), so the threshold is easy to cross physically. Next comes a hard-to-fake source: utility energy by day, to see when sustained high draw occurred on the feeds.", "action": "utility_energy", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Utility meter, daily MWh per feed (grid operator's records):
day | F0 | F1 | F2
1 | 2.7 | 7.9 | 5.8
2 | 2.7 | 8.0 | 5.8
3 | 2.7 | 7.9 | 5.8
4 | 2.8 | 8.0 | 5.8
5 | 2.7 | 7.9 | 5.8
6 | 2.8 | 8.0 | 5.8
7 | 2.8 | 7.9 | 5.8
8 | 2.8 | 7.9 | 5.8
9 | 2.8 | 8.0 | 5.7
10 | 2.7 | 7.9 | 5.7
11 | 2.7 | 7.9 | 5.7
12 | 2.8 | 8.0 | 5.8
13 | 2.7 | 8.0 | 5.8
14 | 2.7 | 8.0 | 5.8
15 | 2.7 | 7.9 | 5.8
16 | 2.7 | 7.9 | 5.8
17 | 2.7 | 7.9 | 5.8
18 | 2.8 | 7.9 | 5.8
19 | 2.8 | 8.0 | 5.8
20 | 2.8 | 7.9 | 5.8
21 | 2.7 | 8.0 | 5.8
22 | 6.2 | 18.8 | 12.0
23 | 6.1 | 18.8 | 12.0
24 | 6.2 | 18.7 | 12.0
25 | 6.1 | 18.8 | 12.0
26 | 6.2 | 18.8 | 12.1
27 | 6.2 | 18.8 | 12.1
28 | 3.7 | 11.1 | 7.6
29 | 2.7 | 7.9 | 5.8
30 | 2.7 | 8.0 | 5.8

### Turn 4
ACTION: {"thinking": "The jump on days 22-27 is large and the grid operator vouches for it. F1 rises by about 10.8 MWh/day (about 450 kW). That fits about 690 GPUs moving from idle (0.15 kW) to training (0.8 kW), i.e. all 700 scheduled A GPUs. F2 rises by about 6.2 MWh/day (about 258 kW), which fits about 400 GPUs, all of B's scheduled pool. Day 28 is partial: about 7 more hours, then back to baseline. That is roughly 1,100 GPUs for about 151 h, or about 165,000 GPU-hours of flat high load. It could be one run spanning both clusters or several separate runs. The physics doesn't settle that yet. Days 26-27 (hours 600-671) fall inside the live window, so chip probe and tap can still reach this load. Next I'll take the sealed escrow logs to see what the operator recorded at the time. It is cheap and the operator can't rewrite it afterwards.", "action": "log_escrow", "args": {}}
RESULT:
Log escrow (verifier's archive of the sealed copy the scheduler sent each midnight):
- a copy was received for every one of days 1-30
- every copy matches the scheduler log the operator presents now

### Turn 5
ACTION: {"thinking": "The escrow matches the current log for every day, so the operator has not rewritten the log since the run. The question is now what the operator recorded for the days 22-28 load. Reading the scheduler log costs 1 point. It shows how the load was labelled (job IDs, customers, GPU counts), and that tells me which splits to test against sources the operator doesn't control.", "action": "scheduler_log", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Scheduler log, days 1-30 (operator's records):
- ft-0561 | finetune | customer: Corvid Labs | nodes A-0501 to A-0675 (175) | day 22.0 to day 28.3 | 26,425 GPU-hours
- ft-0562 | finetune | customer: Pallas Systems | nodes A-0676 to A-0850 (175) | day 22.0 to day 28.3 | 26,425 GPU-hours
- ft-0563 | finetune | customer: Brightwater AI | nodes A-0851 to A-1025 (175) | day 22.0 to day 28.3 | 26,425 GPU-hours
- ft-0564 | finetune | customer: Fennec Data | nodes A-1026 to A-1200 (175) | day 22.0 to day 28.3 | 26,425 GPU-hours
- ft-0565 | finetune | customer: Quillon Tech | nodes B-0401 to B-0600 (200) | day 22.0 to day 28.3 | 30,200 GPU-hours
- ft-0566 | finetune | customer: Marram Software | nodes B-0601 to B-0800 (200) | day 22.0 to day 28.3 | 30,200 GPU-hours

### Turn 6
ACTION: {"thinking": "The log shows six 'separate' fine-tunes. Each is just under 50,000 GPU-hours (26,425 or 30,200). All six start and end at exactly the same time (day 22.0 to 28.3), have different customers, and together cover every scheduled GPU on both clusters, about 162,000 GPU-hours. This is the classic pattern of a split run (H3), but separate customers starting together could be innocent. The key test is whether the jobs exchange gradient traffic with each other. Jobs on different clusters (A vs B) should send almost no traffic across the A-B link if they are independent. Ordinary training across clusters would show heavy A-B traffic. I'll use my own optical tap on the A-B link for day 26, which is live and inside the run. Budget after this: 23.", "action": "interconnect_tap", "args": {"link": "A-B", "day": 26}}
RESULT:
Verifier's optical tap, links between clusters A and B, day 26: about 252 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 2000 GPUs those links serve, that is about 126 MB/s per GPU. (Estimated from a sample of links.)

### Turn 7
ACTION: {"thinking": "To tell an innocent cause from a guilty one, I need a baseline for the day-26 cross-cluster traffic reading. I'll measure the A-B link on day 29, after the run ended and while the tap can still reach it. If A-B traffic falls to near the inference level, the heavy day-26 traffic came from the jobs running across both clusters.", "action": "interconnect_tap", "args": {"link": "A-B", "day": 29}}
RESULT:
Verifier's optical tap, links between clusters A and B, day 29: about 0.02 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 2000 GPUs those links serve, that is about 9 kB/s per GPU. (Estimated from a sample of links.)

### Turn 8
ACTION: {"thinking": "My tap shows A-B traffic of about 252 GB/s on day 26 and about 0.02 GB/s on day 29. The heavy traffic between the clusters exists only while the six 'separate' fine-tunes run. Spread over the roughly 1,100 GPUs in the scheduled pools, that is about 230 MB/s per GPU, far above inference (about 10 kB/s). It sits between low-communication and ordinary training. Fine-tunes for unrelated customers on separate clusters should not exchange GPU-to-GPU traffic, so this points to one coordinated run (H3). Innocent explanations still to rule out are some shared cross-cluster service during those days, and the load not being training at all (H5/H6). I'll check that with my own power sensor. If F1 and F2 both show a periodic line at the same frequency on day 26, the two clusters are stepping in lockstep, which would be strong evidence of one run. Budget: 21, and 19 after this.", "action": "power_spectrum", "args": {"feed": "F1", "day": 26}}
RESULT:
High-rate power meter (verifier's own sensor), feed F1, day 26: periodic lines found
- line near 0.87 Hz, steady for about 24 hours

### Turn 9
ACTION: {"thinking": "F1 shows a steady 0.87 Hz line all day on day 26, which fits flat training. If F2 shows the same frequency on the same day, both clusters are stepping in lockstep, which points to one coordinated run rather than six independent fine-tunes. Six unrelated customers would be unlikely to share one step period across clusters. Budget is 19 now and 17 after this. After that I plan a chip probe during the live window to confirm the load is training, then customer checks against the register to test whether the six customers are shells.", "action": "power_spectrum", "args": {"feed": "F2", "day": 26}}
RESULT:
High-rate power meter (verifier's own sensor), feed F2, day 26: periodic lines found
- line near 0.86 Hz, steady for about 24 hours

### Turn 10
ACTION: {"thinking": "F1 and F2 both show a steady line on day 26, at about 0.87 Hz and 0.86 Hz. The gap is within normal day-to-day drift, so the two clusters appear to step in lockstep. Together with the A-B traffic that exists only during the run, this points to one coordinated run. One innocent explanation is still open: the load could be batch inference or a periodic non-training workload rather than training, since a line alone is not proof. I'll probe chips from four of the 'separate' jobs at hour 650 (day 28), which is live and inside the run (it ends around hour 655). Budget is 17 now and 15 after this. Next, a customer check on one or two of the six customers against the register to see whether they are shells.", "action": "chip_probe", "args": {"nodes": ["A-0600", "A-0900", "B-0500", "B-0700"], "hour": 650}}
RESULT:
Cable current probe at hour 650 (day 28.1). Each reading is a guess:
- A-0600: reads as training
- A-0900: reads as training
- B-0500: reads as training
- B-0700: reads as training

### Turn 11
ACTION: {"thinking": "All the independent evidence points to one coordinated run. Grid meters show both scheduled pools (about 1,100 GPUs) at flat training-level draw from day 22.0 to day 28.3, and nowhere else in the month. My tap shows about 252 GB/s crossing between clusters A and B on day 26 (about 230 MB/s per scheduled GPU) against about 0.02 GB/s on day 29. Yet every logged job stays inside a single cluster, so independent fine-tunes would have no reason to exchange that traffic. My own sensor shows matching steady lines on F1 and F2 (0.87 and 0.86 Hz), so both clusters step in lockstep. My probes read training on chips from four of the six jobs. Together these rule out the innocent explanations: hidden hardware (inventory matches the list), rewritten or lost logs (escrow matches every day), batch inference or a cooling line (probe plus the tap), and genuinely separate customers (cross-cluster traffic and a shared step rhythm). Six unrelated customers each landing just under the limit, with identical start and end times, fits deliberate splitting. The combined run is about 166,000 GPU-hours, and even cluster A alone is about 105,700. A customer check would add little against this physical evidence, so I'm closing the case.", "action": "report", "args": {"verdict": "VIOLATION", "confidence": 92, "integrity": "CLEAN", "finding": "Six 'separate' fine-tunes (ft-0561 to ft-0566) on days 22.0-28.3 were one coordinated training run of about 1,100 GPUs across both clusters, about 166,000 GPU-hours, more than three times the 50,000 limit.", "key_evidence": [{"what": "F1 rose by about 10.8 and F2 by about 6.2 MWh/day on days 22-27, with a partial day 28. This fits about 1,100 GPUs at training power for about 151 h, and the rest of the month is at baseline.", "source": "utility_energy", "vouched_by": "grid operator"}, {"what": "Traffic between clusters A and B was about 252 GB/s on day 26 and about 0.02 GB/s on day 29. Each logged job stays inside one cluster, so this traffic means the jobs were coupled.", "source": "interconnect_tap", "vouched_by": "verifier's own optical tap"}, {"what": "Steady periodic lines all day on day 26: 0.87 Hz on F1 and 0.86 Hz on F2. Both clusters step in lockstep.", "source": "power_spectrum", "vouched_by": "verifier's own sensor"}, {"what": "Chips in four of the six jobs (A-0600, A-0900, B-0500, B-0700) read as training at hour 650.", "source": "chip_probe", "vouched_by": "verifier's own probe"}, {"what": "The log shows six jobs with identical start and end times, each just under 50,000 GPU-hours, together covering every scheduled GPU. The escrow copy matches, so the operator recorded this split at the time.", "source": "scheduler_log + log_escrow", "vouched_by": "operator, checked against verifier's sealed archive"}, {"what": "The manufacturer shipped 2,000 GPUs, which matches the 2,000 on the system list. There is no hidden hardware.", "source": "inventory", "vouched_by": "chip manufacturer"}], "coverage": "Checked: hardware inventory against the system list, utility energy for days 1-30 on all feeds, escrow against the log for days 1-30, the A-B tap on days 26 and 29, power spectra on F1 and F2 for day 26, and a chip probe at hour 650. Not checked: customer register entries for the six named customers, bank payments, outbound traffic, and taps inside each cluster. Days 22-25 rest on energy and log continuity only, not on live instruments. The GPU-hour total does not depend on those days: days 26-28 alone exceed 50,000.", "anomalies_explained": "(1) The energy jump on days 22-28 matches the six logged fine-tunes, and the probe confirms training rather than batch inference. (2) Heavy A-B traffic appears only during the run, and no independent single-cluster job would produce it, so the jobs were coupled. Even with the tap's 30% error, the traffic is four orders of magnitude above the post-run baseline. (3) The matching spectral lines on both feeds rule out a cooling controller (F0 is the cooling feed) and point to a shared training step. (4) Each job sitting just under 50,000 GPU-hours, with identical timing, is explained by deliberate splitting. The customers' registration was not checked, but the physical coupling settles the question without it."}}

## Report

```json
{
 "verdict": "VIOLATION",
 "confidence": 92,
 "integrity": "CLEAN",
 "finding": "Six 'separate' fine-tunes (ft-0561 to ft-0566) on days 22.0-28.3 were one coordinated training run of about 1,100 GPUs across both clusters, about 166,000 GPU-hours, more than three times the 50,000 limit.",
 "key_evidence": [
  {
   "what": "F1 rose by about 10.8 and F2 by about 6.2 MWh/day on days 22-27, with a partial day 28. This fits about 1,100 GPUs at training power for about 151 h, and the rest of the month is at baseline.",
   "source": "utility_energy",
   "vouched_by": "grid operator"
  },
  {
   "what": "Traffic between clusters A and B was about 252 GB/s on day 26 and about 0.02 GB/s on day 29. Each logged job stays inside one cluster, so this traffic means the jobs were coupled.",
   "source": "interconnect_tap",
   "vouched_by": "verifier's own optical tap"
  },
  {
   "what": "Steady periodic lines all day on day 26: 0.87 Hz on F1 and 0.86 Hz on F2. Both clusters step in lockstep.",
   "source": "power_spectrum",
   "vouched_by": "verifier's own sensor"
  },
  {
   "what": "Chips in four of the six jobs (A-0600, A-0900, B-0500, B-0700) read as training at hour 650.",
   "source": "chip_probe",
   "vouched_by": "verifier's own probe"
  },
  {
   "what": "The log shows six jobs with identical start and end times, each just under 50,000 GPU-hours, together covering every scheduled GPU. The escrow copy matches, so the operator recorded this split at the time.",
   "source": "scheduler_log + log_escrow",
   "vouched_by": "operator, checked against verifier's sealed archive"
  },
  {
   "what": "The manufacturer shipped 2,000 GPUs, which matches the 2,000 on the system list. There is no hidden hardware.",
   "source": "inventory",
   "vouched_by": "chip manufacturer"
  }
 ],
 "coverage": "Checked: hardware inventory against the system list, utility energy for days 1-30 on all feeds, escrow against the log for days 1-30, the A-B tap on days 26 and 29, power spectra on F1 and F2 for day 26, and a chip probe at hour 650. Not checked: customer register entries for the six named customers, bank payments, outbound traffic, and taps inside each cluster. Days 22-25 rest on energy and log continuity only, not on live instruments. The GPU-hour total does not depend on those days: days 26-28 alone exceed 50,000.",
 "anomalies_explained": "(1) The energy jump on days 22-28 matches the six logged fine-tunes, and the probe confirms training rather than batch inference. (2) Heavy A-B traffic appears only during the run, and no independent single-cluster job would produce it, so the jobs were coupled. Even with the tap's 30% error, the traffic is four orders of magnitude above the post-run baseline. (3) The matching spectral lines on both feeds rule out a cooling controller (F0 is the cooling feed) and point to a shared training step. (4) Each job sitting just under 50,000 GPU-hours, with identical timing, is explained by deliberate splitting. The customers' registration was not checked, but the physical coupling settles the question without it."
}
```
