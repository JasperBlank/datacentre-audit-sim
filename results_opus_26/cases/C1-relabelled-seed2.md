# C1-relabelled-seed2

Truth: Cheating. One training run declared as internal batch inference, still running in the audit window. Largest coordinated run: 151,200 GPU-hours (limit 50,000). Violation: True.

### Turn 1
ACTION: {"thinking": "Competing explanations: (H1) Honest: no run exceeded 50,000 GPU-hours; logs and physical data agree, with ordinary mess such as late payments or gaps. (H2) Split run: one coordinated run labelled as several jobs or customers (shell customers) that together exceed the threshold. Check: interconnect_tap A-B, power_spectrum lines persisting across 'separate' jobs, customer_check register, bank_payments. (H3) Hidden capacity: GPUs that inventory shows but the system_list omits are running training. Check: inventory vs system_list, utility_energy vs scheduler-implied power. (H4) Mislabelled: training logged as batch inference. Check: chip_probe in days 26-30, outbound_traffic (training sends little to the internet), interconnect_tap traffic levels, power spectrum lines. (H5) Log rewriting: scheduler log edited after the fact. Check: log_escrow vs scheduler_log. (H6) Low-communication training spread across clusters to evade the tap. Check: tap at about 10 MB/s, power lines. Plan: start with hard-to-fake sources (inventory, utility_energy), then the operator's map, then the logs and balance checks. First action: inventory from the chip manufacturer, to map what exists.", "action": "inventory", "args": {}}
RESULT:
Manufacturer's shipment records for Borealis Compute: 2000 GPUs delivered to the Eemshaven site.
- serials SN100001 to SN101200 (1200 units)
- serials SN101201 to SN102000 (800 units)

### Turn 2
ACTION: {"thinking": "The inventory shows 2000 GPUs at Eemshaven, in two serial batches of 1200 and 800 units. That fits two clusters, A and B. At most 50,000 GPU-hours means 2000 GPUs could cross the threshold in 25 hours, and a 1200-GPU cluster in about 42 hours, so the threshold is easy to exceed. Next I'll get the operator's system_list and compare it with the inventory, to find any hidden GPUs (H3) and to learn the cluster layout and which links the tap covers.", "action": "system_list", "args": {}}
RESULT:
Operator's system list (Borealis Compute, site Eemshaven):
- Cluster A: nodes A-0001 to A-1200, power feed F1. Nodes 1-500 are the interactive inference pool; the rest run scheduled jobs.
- Cluster B: nodes B-0001 to B-0800, power feed F2. Nodes 1-400 are the interactive inference pool; the rest run scheduled jobs.
- Feed F0: cooling and facility overhead.

### Turn 3
ACTION: {"thinking": "Map check: the system list shows 1200 nodes in cluster A and 800 in cluster B, 2000 in total. That matches the manufacturer's 2000 GPUs, assuming one GPU per node; serial-to-node mapping is still unverified. So nothing is obviously hidden. Scheduled-job capacity is 700 GPUs in A and 400 in B. A run on all 700 A nodes would cross 50,000 GPU-hours in about 72 hours, and one on A plus B scheduled nodes (1100 GPUs) in about 46 hours. Next, a hard-to-fake source: grid energy for days 1-30. It shows when the site drew training-level power, and I can compare it against the scheduler log later.", "action": "utility_energy", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Utility meter, daily MWh per feed (grid operator's records):
day | F0 | F1 | F2
1 | 2.7 | 8.0 | 5.8
2 | 2.8 | 8.0 | 5.8
3 | 2.7 | 8.0 | 5.8
4 | 2.7 | 7.9 | 5.8
5 | 2.7 | 7.9 | 5.8
6 | 2.7 | 8.0 | 5.8
7 | 2.8 | 7.9 | 5.8
8 | 3.2 | 7.9 | 8.1
9 | 3.2 | 7.9 | 8.1
10 | 2.8 | 7.9 | 5.8
11 | 2.8 | 8.0 | 5.8
12 | 2.8 | 8.0 | 5.8
13 | 2.7 | 8.0 | 5.8
14 | 2.7 | 8.0 | 5.8
15 | 2.7 | 7.9 | 5.8
16 | 2.7 | 8.0 | 5.8
17 | 2.8 | 8.0 | 5.8
18 | 2.7 | 7.9 | 5.7
19 | 2.7 | 8.0 | 5.8
20 | 4.9 | 18.8 | 5.8
21 | 5.0 | 19.0 | 5.8
22 | 4.9 | 18.7 | 5.8
23 | 4.9 | 18.7 | 5.8
24 | 4.9 | 19.0 | 5.8
25 | 5.0 | 18.9 | 5.8
26 | 5.0 | 19.0 | 5.8
27 | 4.9 | 18.8 | 5.7
28 | 4.9 | 18.7 | 5.8
29 | 2.7 | 8.0 | 5.8
30 | 2.7 | 7.9 | 5.8

### Turn 4
ACTION: {"thinking": "Grid energy, which is hard to fake, shows the main lead. F1 is about 8.0 MWh/day on days 1-19 and 29-30, and about 18.8 MWh/day on days 20-28. The extra 10.8 MWh/day is about 450 kW. A GPU going from idle (0.15 kW) to training (0.8 kW) adds 0.65 kW, so this is about 690 GPUs, close to the 700 scheduled nodes in cluster A. F0 cooling rises at the same time, which fits real load. If one coordinated run, 700 GPUs x 216 h is about 151,000 GPU-hours, roughly 3x the threshold. It could also be several separate customer jobs, or batch inference at 0.75 kW. F2 also rose on days 8-9 (+2.3 MWh/day, about 150 GPUs for 48 h, about 7,000 GPU-hours), which is under the threshold on its own. Days 26-28 fall in the live window, so the probe and tap can examine this load directly. Next, cheap and verifier-held: the log escrow, to see what the operator recorded each midnight for days 20-28 before any later edits.", "action": "log_escrow", "args": {}}
RESULT:
Log escrow (verifier's archive of the sealed copy the scheduler sent each midnight):
- a copy was received for every one of days 1-30
- every copy matches the scheduler log the operator presents now

### Turn 5
ACTION: {"thinking": "The escrow matches the current scheduler log for all 30 days, so after-the-fact rewriting (H5) is unlikely. A false record made on the day is still possible. Next I'll read the scheduler log for days 1-30 to see how the operator labels the extra load: F1 on days 20-28 (about 690 GPUs) and F2 on days 8-9 (about 150 GPUs). The labels tell me which hypotheses to test. A split across jobs or customers points to H2, and batch inference points to H4. I'll then check them with the live chip probe and interconnect tap during days 26-28.", "action": "scheduler_log", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Scheduler log, days 1-30 (operator's records):
- ft-0419 | finetune | customer: Ostara Legal | nodes B-0401 to B-0550 (150) | day 8.0 to day 10.0 | 7,200 GPU-hours
- bt-0460 | batch | customer: internal | nodes A-0501 to A-1200 (700) | day 20.0 to day 29.0 | 151,200 GPU-hours

### Turn 6
ACTION: {"thinking": "The log labels the F1 load on days 20-28 as bt-0460, an internal batch-inference job on A-0501 to A-1200 (700 GPUs, 151,200 GPU-hours), about 3x the threshold if it is actually training. The Ostara fine-tune (7,200 GPU-hours) matches the F2 rise on days 8-9 and is well under the threshold. Grid energy cannot separate batch inference (0.75 kW) from training (0.8 kW), so the deciding question is H4, mislabelling. Since days 26-28 are in the live window, I can test it with my own instruments. First the interconnect tap on cluster A on day 26: about 1 GB/s per GPU would indicate ordinary training, about 10 MB/s low-communication training, and about 10 kB/s inference. After that I'll run the chip probe on bt-0460 nodes and the power spectrum on F1.", "action": "interconnect_tap", "args": {"link": "A", "day": 26}}
RESULT:
Verifier's optical tap, links inside cluster A, day 26: about 726 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 1200 GPUs those links serve, that is about 605 MB/s per GPU. (Estimated from a sample of links.)

### Turn 7
ACTION: {"thinking": "The tap reads about 726 GB/s inside cluster A. If the 500 interactive-pool GPUs exchange only inference-level traffic (about 10 kB/s each, so negligible), nearly all of it comes from the 700 bt-0460 nodes. That is about 1.04 GB/s per GPU. Allowing for the tap's ±30% error, it still matches ordinary training at about 1 GB/s and is about 100,000 times the inference level. That points strongly to mislabelled training (H4) and to one coordinated process across the 700 nodes, since training-level exchange binds them together. One innocent possibility remains: unusual batch inference with heavy peer exchange, such as model-parallel inference. To test it with my own instrument, I'll probe a spread of bt-0460 nodes at hour 630 (day 27), checking whether the chips draw training-type current.", "action": "chip_probe", "args": {"nodes": ["A-0520", "A-0700", "A-0900", "A-1150"], "hour": 630}}
RESULT:
Cable current probe at hour 630 (day 27.2). Each reading is a guess:
- A-0520: reads as training
- A-0700: reads as training
- A-0900: reads as training
- A-1150: reads as training

### Turn 8
ACTION: {"thinking": "Three independent sources the operator cannot easily fake agree. (1) Grid meter: F1 drew about 10.8 MWh/day extra on days 20-28, about 690 GPUs at full load. Cooling on F0 rose with it. (2) My optical tap on day 26: about 1.04 GB/s per GPU across the 700 bt-0460 nodes, which is the ordinary training signature and about 100,000 times inference traffic. (3) My chip probe at hour 630: all four bt-0460 nodes sampled across the range read as training. At 97% accuracy each, four mistakes in a row is very unlikely. The scheduler, matched by escrow, records this as a single internal job on all 700 nodes, so it is one process, not separate customers. Training-level peer exchange also ties the nodes into one coordinated run. Size: 700 x 216 h = 151,200 GPU-hours, about 3x the threshold. Even if training had only started on day 26, 700 x 72 h = 50,400, still over. The innocent explanation, heavy model-parallel batch inference, does not fit the probe readings. The Ostara fine-tune (7,200 GPU-hours) matches the grid rise on days 8-9 and is fine. The evidence favours a violation by far more than 4:1.", "action": "report", "args": {"verdict": "VIOLATION", "confidence": 92, "integrity": "CLEAN", "finding": "Job bt-0460, logged as internal batch inference on nodes A-0501 to A-1200 (700 GPUs, days 20-29), was a single coordinated training run of about 151,200 GPU-hours, about 3x the 50,000 limit.", "key_evidence": [{"what": "F1 rose from about 8.0 to about 18.8 MWh/day on days 20-28 (about 450 kW extra, about 690 GPUs at training load), with a matching rise in F0 cooling", "source": "utility_energy", "vouched_by": "grid operator"}, {"what": "Day 26 GPU-to-GPU traffic in cluster A of about 726 GB/s, about 1.04 GB/s per bt-0460 GPU, the ordinary training signature (inference is about 10 kB/s)", "source": "interconnect_tap", "vouched_by": "verifier's own optical tap"}, {"what": "All four sampled bt-0460 nodes (A-0520, A-0700, A-0900, A-1150) read as training at hour 630", "source": "chip_probe", "vouched_by": "verifier's own probe"}, {"what": "The operator's own sealed midnight logs record bt-0460 as one job on 700 nodes from day 20.0 to 29.0 (151,200 GPU-hours), unchanged since", "source": "log_escrow / scheduler_log", "vouched_by": "verifier's archive (shows what was recorded at the time)"}, {"what": "2000 GPUs delivered, matching the 2000 nodes listed, so no hidden hardware", "source": "inventory", "vouched_by": "chip manufacturer"}], "coverage": "Checked: grid energy for all feeds on days 1-30; full scheduler log, with escrow integrity for days 1-30; inventory against the system list; tap on cluster A on day 26; chip probe of 4 bt-0460 nodes on day 27. Not checked: tap and probe on days 20-25 (outside the live window; this period is supported by the grid data and the log); cluster B links and the A-B link; power spectrum; customer checks for Ostara Legal. None of these gaps can change the verdict, because the live-window portion alone (700 GPUs x 72 h = 50,400) already exceeds the limit.", "anomalies_explained": "F1 load surge on days 20-28: logged as batch inference, but the tap traffic (about 1 GB/s per GPU) and the probe readings (4 of 4 training) show training, so it was mislabelled. F2 rise on days 8-9: matches the logged Ostara Legal fine-tune (150 GPUs, 7,200 GPU-hours), which is under the limit and not investigated further. Escrow matched the current logs, so there was no after-the-fact rewriting; the mislabel was made at the time the work was recorded."}}

## Report

```json
{
 "verdict": "VIOLATION",
 "confidence": 92,
 "integrity": "CLEAN",
 "finding": "Job bt-0460, logged as internal batch inference on nodes A-0501 to A-1200 (700 GPUs, days 20-29), was a single coordinated training run of about 151,200 GPU-hours, about 3x the 50,000 limit.",
 "key_evidence": [
  {
   "what": "F1 rose from about 8.0 to about 18.8 MWh/day on days 20-28 (about 450 kW extra, about 690 GPUs at training load), with a matching rise in F0 cooling",
   "source": "utility_energy",
   "vouched_by": "grid operator"
  },
  {
   "what": "Day 26 GPU-to-GPU traffic in cluster A of about 726 GB/s, about 1.04 GB/s per bt-0460 GPU, the ordinary training signature (inference is about 10 kB/s)",
   "source": "interconnect_tap",
   "vouched_by": "verifier's own optical tap"
  },
  {
   "what": "All four sampled bt-0460 nodes (A-0520, A-0700, A-0900, A-1150) read as training at hour 630",
   "source": "chip_probe",
   "vouched_by": "verifier's own probe"
  },
  {
   "what": "The operator's own sealed midnight logs record bt-0460 as one job on 700 nodes from day 20.0 to 29.0 (151,200 GPU-hours), unchanged since",
   "source": "log_escrow / scheduler_log",
   "vouched_by": "verifier's archive (shows what was recorded at the time)"
  },
  {
   "what": "2000 GPUs delivered, matching the 2000 nodes listed, so no hidden hardware",
   "source": "inventory",
   "vouched_by": "chip manufacturer"
  }
 ],
 "coverage": "Checked: grid energy for all feeds on days 1-30; full scheduler log, with escrow integrity for days 1-30; inventory against the system list; tap on cluster A on day 26; chip probe of 4 bt-0460 nodes on day 27. Not checked: tap and probe on days 20-25 (outside the live window; this period is supported by the grid data and the log); cluster B links and the A-B link; power spectrum; customer checks for Ostara Legal. None of these gaps can change the verdict, because the live-window portion alone (700 GPUs x 72 h = 50,400) already exceeds the limit.",
 "anomalies_explained": "F1 load surge on days 20-28: logged as batch inference, but the tap traffic (about 1 GB/s per GPU) and the probe readings (4 of 4 training) show training, so it was mislabelled. F2 rise on days 8-9: matches the logged Ostara Legal fine-tune (150 GPUs, 7,200 GPU-hours), which is under the limit and not investigated further. Escrow matched the current logs, so there was no after-the-fact rewriting; the mislabel was made at the time the work was recorded."
}
```
