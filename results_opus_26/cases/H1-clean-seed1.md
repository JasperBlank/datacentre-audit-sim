# H1-clean-seed1

Truth: Honest. Inference plus small declared fine-tunes. Largest coordinated run: 7,200 GPU-hours (limit 50,000). Violation: False.

### Turn 1
ACTION: {"thinking": "Competing explanations: (H1) Honest: no run exceeded 50,000 GPU-hours. Logs, energy and inventory agree. Check: utility_energy against inventory and scheduler totals, plus balance_checks. (H2) Honest but messy: lost log days, late payments, or a non-replying customer create gaps but no large run. Check: log_escrow against scheduler_log, and register entries from customer_check. (H3) Split run: one coordinated training run is labelled as several jobs or customers (possibly shell customers) so each piece stays under the threshold. Check: interconnect_tap on A-B and within clusters for ~1 GB/s per GPU coupling, customer_check register entries, and bank_payments for shared payers. (H4) Hidden hardware: GPUs exist (inventory) that are missing from system_list, or links missing from the site list, running training off the books. Check: inventory vs system_list, utility_energy vs listed GPU power. (H5) Disguised training: training relabelled as batch inference, or low-communication training built to look like inference. Check: power_spectrum lines, chip_probe live, interconnect_tap (10 MB/s vs 10 kB/s), outbound_traffic (inference sends to users). (H6) Retroactive log edits: the scheduler log was edited after the fact. Check: log_escrow vs current scheduler_log. Start by mapping systems: inventory (manufacturer-vouched) first.", "action": "inventory", "args": {}}
RESULT:
Manufacturer's shipment records for Borealis Compute: 2000 GPUs delivered to the Eemshaven site.
- serials SN100001 to SN101200 (1200 units)
- serials SN101201 to SN102000 (800 units)

### Turn 2
ACTION: {"thinking": "Inventory from the manufacturer shows 2000 GPUs: 1200 + 800, which could correspond to clusters A and B. Next I map what the operator lists with system_list, then compare node counts against inventory to test H4 (hidden hardware).", "action": "system_list", "args": {}}
RESULT:
Operator's system list (Borealis Compute, site Eemshaven):
- Cluster A: nodes A-0001 to A-1200, power feed F1. Nodes 1-500 are the interactive inference pool; the rest run scheduled jobs.
- Cluster B: nodes B-0001 to B-0800, power feed F2. Nodes 1-400 are the interactive inference pool; the rest run scheduled jobs.
- Feed F0: cooling and facility overhead.

### Turn 3
ACTION: {"thinking": "The system list matches the inventory. Cluster A has 1200 nodes and cluster B has 800, which equals the 2000 GPUs the manufacturer shipped. No hidden GPUs appear at the hardware level, which weakens H4, though unlisted links or feeds remain possible. Scheduled-job capacity is 700 GPUs in A and 400 in B, 1100 in total. A run exceeding 50,000 GPU-hours needs about 70 GPUs for 30 days, or 700 GPUs for about 72 hours, so a single cluster's batch pool could do it alone. Next I want grid-vouched energy for days 1-30 to bound total GPU activity and spot flat high-power periods.", "action": "utility_energy", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Utility meter, daily MWh per feed (grid operator's records):
day | F0 | F1 | F2
1 | 2.8 | 7.9 | 5.7
2 | 2.8 | 7.9 | 5.8
3 | 3.0 | 9.4 | 5.8
4 | 3.1 | 9.5 | 5.8
5 | 3.0 | 9.4 | 5.8
6 | 2.7 | 8.0 | 5.7
7 | 2.8 | 7.9 | 5.8
8 | 2.7 | 7.9 | 5.8
9 | 2.7 | 8.0 | 5.8
10 | 3.2 | 7.9 | 8.0
11 | 3.2 | 8.0 | 8.0
12 | 2.7 | 8.0 | 5.8
13 | 2.8 | 8.0 | 5.8
14 | 3.3 | 10.9 | 5.8
15 | 3.3 | 10.8 | 5.8
16 | 2.7 | 7.9 | 5.8
17 | 2.7 | 8.0 | 5.8
18 | 2.8 | 8.0 | 5.7
19 | 2.8 | 7.9 | 5.8
20 | 2.7 | 7.9 | 5.7
21 | 2.7 | 8.0 | 5.7
22 | 2.7 | 7.9 | 5.8
23 | 2.8 | 8.0 | 5.7
24 | 2.8 | 7.9 | 5.7
25 | 2.7 | 7.9 | 5.8
26 | 2.8 | 8.0 | 5.8
27 | 2.8 | 8.0 | 5.8
28 | 2.7 | 8.0 | 5.8
29 | 2.8 | 8.0 | 5.8
30 | 2.7 | 8.0 | 5.8

### Turn 4
ACTION: {"thinking": "The grid-metered energy shows short bumps on F1 (days 3-5 and 14-15) and on F2 (days 10-11), with steady baselines otherwise. A steady baseline could still hide a long, modest run, so energy alone can't settle the claim. Next I'll compare the operator's scheduler log with the sealed escrow copy and check the logged jobs against the energy bumps.", "action": "scheduler_log", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Scheduler log, days 1-30 (operator's records):
- ft-0412 | finetune | customer: Tidewater Robotics | nodes A-0501 to A-0600 (100) | day 3.0 to day 6.0 | 7,200 GPU-hours
- ft-0419 | finetune | customer: Ostara Legal | nodes B-0401 to B-0550 (150) | day 10.0 to day 12.0 | 7,200 GPU-hours
- bt-0423 | batch | customer: Kestrel Search | nodes A-0701 to A-0900 (200) | day 14.0 to day 16.0 | 9,600 GPU-hours

### Turn 5
ACTION: {"thinking": "The grid-metered energy bumps match the logged jobs. Each estimate is extra draw above idle multiplied by GPUs and hours:\n- ft-0412: 100 GPUs x (0.8 - 0.15) kW x 24 h is about +1.56 MWh/day on F1 for days 3-5, against an observed +1.5.\n- ft-0419: 150 x 0.65 kW x 24 h is about +2.3 MWh/day on F2 for days 10-11, against an observed +2.2.\n- bt-0423: 200 x (0.75 - 0.15) kW x 24 h is about +2.9 MWh/day on F1 for days 14-15, against an observed +2.9.\n\nLogged jobs are therefore consistent with metered energy, and all are far below 50,000 GPU-hours. The open risk is a long, modest run hidden in the flat baselines: about 70 GPUs over 30 days would add only about 1.1 MWh/day and look like baseline. Next I'll check whether the operator's log was edited after the fact (H6) by comparing it with my sealed escrow copies. This costs 1 point.", "action": "log_escrow", "args": {}}
RESULT:
Log escrow (verifier's archive of the sealed copy the scheduler sent each midnight):
- a copy was received for every one of days 1-30
- every copy matches the scheduler log the operator presents now

### Turn 6
ACTION: {"thinking": "The escrow copies match the current scheduler log, so H6 (after-the-fact log edits) is unlikely. The energy baselines also look consistent with the listed hardware. F2 is about 400 idle scheduled GPUs (about 1.4 MWh/day) plus 400 interactive GPUs averaging about 0.45 kW (about 4.3 MWh/day), roughly 5.8 MWh/day. F1 is about 700 idle GPUs (about 2.5 MWh/day) plus 500 interactive GPUs (about 5.4 MWh/day), roughly 7.9 MWh/day. So there is no obvious unlogged load in the flat periods, although a modest long run hiding inside the interactive pool can't yet be excluded. Next I'll run the fixed balance checks across the records gathered so far (cost 1). Any flag will be a lead to follow with my own instruments: power_spectrum on baseline days, outbound_traffic, and interconnect_tap.", "action": "balance_checks", "args": {}}
RESULT:
Fixed balance checks:
PASS inventory: 2000 GPUs shipped, 2000 on the system list
PASS energy: metered energy matches declared jobs within 10% on all checked feed-days
PASS outbound traffic: matches declared inference in every 5-day window
PASS billing: every invoice is paid in the bank's records
PASS declared job sizes: no declared training or fine-tuning job exceeds 50,000 GPU-hours

### Turn 7
ACTION: {"thinking": "The balance checks pass, the escrow matches the scheduler log, and metered energy matches the logged jobs. A pass is not proof, though. The main untested risk is a long, modest run (about 70 or more GPUs for 30 days) hidden in a flat baseline or inside the interactive pool, where energy alone cannot separate it from inference. So far everything rests on records. Next I use my own instruments. A power-spectrum line on a quiet day, when no job is logged, would point to unlogged training. I start with F1, the larger cluster, on day 20, which falls in a flat stretch.", "action": "power_spectrum", "args": {"feed": "F1", "day": 20}}
RESULT:
High-rate power meter (verifier's own sensor), feed F1, day 20: no periodic line.

### Turn 8
ACTION: {"thinking": "F1 on day 20 shows no periodic line, which is evidence against hidden training on cluster A that day. The sensor finds a line on about 96% of active training days. Cluster B (feed F2) is still unchecked on quiet days. Its flat baseline of about 5.8 MWh/day could still hold a modest hidden run of about 70 or more GPUs inside the interactive pool or the idle scheduled pool. So I check F2 on the same quiet day (day 20) with my own sensor. If F2 is also clean, I'll sample other quiet days on both feeds and then use chip_probe and interconnect_tap live in days 26-30, which test disguised or low-communication training directly.", "action": "power_spectrum", "args": {"feed": "F2", "day": 20}}
RESULT:
High-rate power meter (verifier's own sensor), feed F2, day 20: no periodic line.

### Turn 9
ACTION: {"thinking": "F1 and F2 both show no periodic line on day 20, so there is no sign of hidden training on that quiet day. A single day is only a sample, and low-communication or step-varying training can produce a weak line. I'll switch to a different instrument for the live window. My own optical tap on link A on day 27 (no jobs logged) should read about 10 kB/s per GPU if cluster A carries only inference and idle nodes. A reading near 1 GB/s or 10 MB/s per GPU would point to hidden training. Afterwards I plan to tap link B and the A-B link, and to probe chips in the interactive pools.", "action": "interconnect_tap", "args": {"link": "A", "day": 27}}
RESULT:
Verifier's optical tap, links inside cluster A, day 27: about 0.01 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 1200 GPUs those links serve, that is about 11 kB/s per GPU. (Estimated from a sample of links.)

### Turn 10
ACTION: {"thinking": "The tap on cluster A's internal links on day 27 reads about 11 kB/s per GPU, which is inference level. No ordinary training (about 1 GB/s per GPU) or low-communication training (about 10 MB/s per GPU) of meaningful size is running inside cluster A. Even 70 low-communication GPUs would add about 0.7 GB/s, far above the 0.01 GB/s total measured, and a 30% error cannot hide that.\n\nThe grid-metered baselines on F1 and F2 stay flat from day 1 to day 30 apart from the logged bumps. So any hidden steady load in days 1-25 would also appear in the live window, which makes live checks informative for the whole period.\n\nNext I tap the links inside cluster B on the same quiet day (day 27). Afterwards I plan to tap the A-B link, to rule out a run split across clusters, and to probe chips in the interactive pools.", "action": "interconnect_tap", "args": {"link": "B", "day": 27}}
RESULT:
Verifier's optical tap, links inside cluster B, day 27: about 0.01 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 800 GPUs those links serve, that is about 8 kB/s per GPU. (Estimated from a sample of links.)

### Turn 11
ACTION: {"thinking": "Cluster B's internal links read about 8 kB/s per GPU on day 27, which is inference level, just like cluster A. The remaining route for a hidden run in the live window is a run split across both clusters that talks mainly over the A-B link, so I tap that link on the same quiet day. After that, the main gap is days 1-25. Flat metered energy limits hidden load there to a swap inside existing activity, such as training replacing inference at similar power. I will test that with grid-independent sources: power_spectrum on more quiet days and outbound_traffic from the internet provider.", "action": "interconnect_tap", "args": {"link": "A-B", "day": 27}}
RESULT:
Verifier's optical tap, links between clusters A and B, day 27: about 0.02 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 2000 GPUs those links serve, that is about 11 kB/s per GPU. (Estimated from a sample of links.)

### Turn 12
ACTION: {"thinking": "The A-B link reads about 11 kB/s per GPU, which is inference level. The live window (day 27) therefore shows no training of any kind, whether ordinary, low-communication or split across clusters. My own sensor found no periodic line on F1 or F2 on day 20. Grid-metered energy is flat on every feed for days 1-30 apart from three bumps, and those match the three logged jobs. A hidden steady run large enough to pass 50,000 GPU-hours would need about 70 or more GPUs for 30 days, or more GPUs for fewer days. If it had stopped before the live window, it would have left a step in the metered energy, and there is none. If it continued into the window, the taps would have seen it. The escrow matches the scheduler log, so the log was not edited after the fact. Even if all three logged jobs were one coordinated run, the total would be 24,000 GPU-hours, below the threshold. Inventory matches the system list, so no hardware is hidden. The independent evidence strongly favours compliance, so I am closing without spending more budget.", "action": "report", "args": {"verdict": "NO_VIOLATION", "confidence": 90, "integrity": "CLEAN", "finding": "No training run exceeded 50,000 GPU-hours; the three logged jobs (24,000 GPU-hours combined) match metered energy, and the verifier's own instruments show no hidden training.", "key_evidence": [{"what": "2000 GPUs shipped, matching the 2000 nodes on the system list", "source": "inventory", "vouched_by": "chip manufacturer"}, {"what": "Daily energy is flat apart from bumps on F1 days 3-5, F2 days 10-11 and F1 days 14-15, each within about 5% of the matching logged job; no step change anywhere in days 1-30", "source": "utility_energy", "vouched_by": "grid operator"}, {"what": "The sealed midnight copies for all 30 days match the current scheduler log", "source": "log_escrow", "vouched_by": "verifier's archive"}, {"what": "Inter-GPU traffic on day 27 is about 8-11 kB/s per GPU on links A, B and A-B, which is inference level; no ordinary, low-communication or cross-cluster training", "source": "interconnect_tap", "vouched_by": "verifier's own optical tap"}, {"what": "No periodic power line on F1 or F2 on day 20 (a quiet day)", "source": "power_spectrum", "vouched_by": "verifier's own sensor"}], "coverage": "All 2000 GPUs and both clusters. Energy was checked for days 1-30 on all feeds. The escrow covers days 1-30. Interconnect taps covered every listed link on day 27 only. Power spectra covered day 20 on F1 and F2 only. Chip probes, customer checks and spectra for the job days were not used. Days 1-25 are covered indirectly: flat metered energy with no step means any hidden steady load would have persisted into the live window, where none was seen.", "anomalies_explained": "Energy bumps on F1 days 3-5, F2 days 10-11 and F1 days 14-15 are explained by logged jobs ft-0412 (7,200 GPU-hours), ft-0419 (7,200) and bt-0423 (9,600), and each matches the expected power within about 5%. Even if these three jobs were one disguised coordinated run, the total is 24,000 GPU-hours, below the threshold. The balance checks raised no other anomalies."}}

## Report

```json
{
 "verdict": "NO_VIOLATION",
 "confidence": 90,
 "integrity": "CLEAN",
 "finding": "No training run exceeded 50,000 GPU-hours; the three logged jobs (24,000 GPU-hours combined) match metered energy, and the verifier's own instruments show no hidden training.",
 "key_evidence": [
  {
   "what": "2000 GPUs shipped, matching the 2000 nodes on the system list",
   "source": "inventory",
   "vouched_by": "chip manufacturer"
  },
  {
   "what": "Daily energy is flat apart from bumps on F1 days 3-5, F2 days 10-11 and F1 days 14-15, each within about 5% of the matching logged job; no step change anywhere in days 1-30",
   "source": "utility_energy",
   "vouched_by": "grid operator"
  },
  {
   "what": "The sealed midnight copies for all 30 days match the current scheduler log",
   "source": "log_escrow",
   "vouched_by": "verifier's archive"
  },
  {
   "what": "Inter-GPU traffic on day 27 is about 8-11 kB/s per GPU on links A, B and A-B, which is inference level; no ordinary, low-communication or cross-cluster training",
   "source": "interconnect_tap",
   "vouched_by": "verifier's own optical tap"
  },
  {
   "what": "No periodic power line on F1 or F2 on day 20 (a quiet day)",
   "source": "power_spectrum",
   "vouched_by": "verifier's own sensor"
  }
 ],
 "coverage": "All 2000 GPUs and both clusters. Energy was checked for days 1-30 on all feeds. The escrow covers days 1-30. Interconnect taps covered every listed link on day 27 only. Power spectra covered day 20 on F1 and F2 only. Chip probes, customer checks and spectra for the job days were not used. Days 1-25 are covered indirectly: flat metered energy with no step means any hidden steady load would have persisted into the live window, where none was seen.",
 "anomalies_explained": "Energy bumps on F1 days 3-5, F2 days 10-11 and F1 days 14-15 are explained by logged jobs ft-0412 (7,200 GPU-hours), ft-0419 (7,200) and bt-0423 (9,600), and each matches the expected power within about 5%. Even if these three jobs were one disguised coordinated run, the total is 24,000 GPU-hours, below the threshold. The balance checks raised no other anomalies."
}
```
