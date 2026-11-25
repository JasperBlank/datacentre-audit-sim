# H1-clean-seed2

Truth: Honest. Inference plus small declared fine-tunes. Largest coordinated run: 7,200 GPU-hours (limit 50,000). Violation: False.

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
1 | 2.7 | 7.9 | 5.8
2 | 2.7 | 7.9 | 5.7
3 | 3.0 | 9.4 | 5.8
4 | 3.0 | 9.4 | 5.8
5 | 3.0 | 9.5 | 5.7
6 | 2.7 | 8.0 | 5.8
7 | 2.7 | 7.9 | 5.8
8 | 3.2 | 7.9 | 8.1
9 | 3.2 | 8.0 | 8.1
10 | 2.7 | 8.0 | 5.8
11 | 2.7 | 7.9 | 5.8
12 | 2.8 | 7.9 | 5.8
13 | 2.7 | 7.9 | 5.8
14 | 3.3 | 10.9 | 5.8
15 | 3.4 | 10.9 | 5.8
16 | 2.8 | 8.0 | 5.8
17 | 2.7 | 8.0 | 5.7
18 | 2.7 | 7.9 | 5.8
19 | 2.7 | 7.9 | 5.8
20 | 2.8 | 8.0 | 5.8
21 | 2.7 | 8.0 | 5.8
22 | 2.7 | 7.9 | 5.8
23 | 2.7 | 8.0 | 5.7
24 | 2.7 | 8.0 | 5.8
25 | 2.7 | 7.9 | 5.8
26 | 2.7 | 8.0 | 5.8
27 | 2.7 | 8.0 | 5.8
28 | 2.7 | 7.9 | 5.8
29 | 2.7 | 8.0 | 5.8
30 | 2.7 | 8.0 | 5.8

### Turn 4
ACTION: {"thinking": "Energy analysis. Baselines are F1 about 7.9 MWh/day (about 329 kW) and F2 about 5.8 MWh/day (about 242 kW). These fit mostly idle scheduled nodes (0.15 kW) plus inference pools at moderate load. Three short bumps: (a) F1 days 3-5, +1.5 MWh/day, about 62 kW, roughly 96 GPUs going from idle to training, about 6.9k GPU-hours; (b) F2 days 8-9, +2.3 MWh/day, about 96 kW, roughly 147 GPUs, about 7k GPU-hours; (c) F1 days 14-15, +3.0 MWh/day, about 125 kW, roughly 192 GPUs, about 9.2k GPU-hours. Cooling on F0 rises with each bump, which is consistent. Even if all three bumps were one run, the total is about 23k, well below 50k. The remaining risk is a steady run hidden in the flat baseline. The F1 power budget allows up to about 229 GPUs training continuously (about 165k GPU-hours) if the 'inference pool' draws less than assumed. F2 allows a similar case on a smaller scale. To test that, I'll check outbound traffic. A genuine interactive pool sends substantial daily-cycling traffic to users. If outbound is low or flat, part of the baseline may be training. Hard-to-fake source (ISP), cost 1.", "action": "outbound_traffic", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Internet provider's records, outbound TB per day:
day 1: 4.8
day 2: 4.8
day 3: 4.8
day 4: 4.8
day 5: 4.8
day 6: 4.8
day 7: 4.8
day 8: 4.7
day 9: 4.7
day 10: 4.8
day 11: 4.8
day 12: 4.8
day 13: 4.7
day 14: 6.3
day 15: 6.1
day 16: 4.7
day 17: 4.7
day 18: 4.7
day 19: 4.8
day 20: 4.8
day 21: 4.8
day 22: 4.7
day 23: 4.8
day 24: 4.8
day 25: 4.7
day 26: 4.7
day 27: 4.7
day 28: 4.8
day 29: 4.7
day 30: 4.8

### Turn 5
ACTION: {"thinking": "Outbound traffic is flat at about 4.7-4.8 TB/day, which fits a steady interactive pool. It rises to 6.1-6.3 TB on days 14-15, the same days as the F1 power bump. That suggests the bump was user-facing load, not training, though this needs confirming. The F1 days 3-5 and F2 days 8-9 bumps show no outbound rise, so they look flat like training or batch inference. Even combined, the three bumps total about 23k GPU-hours, so the main risk is still a steady run hidden in the baseline, or the operator's records not matching. Next, I'll get the sealed log escrow, which I archive myself, so I can compare what the operator recorded each day with the scheduler log and the energy record.", "action": "log_escrow", "args": {}}
RESULT:
Log escrow (verifier's archive of the sealed copy the scheduler sent each midnight):
- a copy was received for every one of days 1-30
- every copy matches the scheduler log the operator presents now

### Turn 6
ACTION: {"thinking": "The escrow matches the scheduler log for all 30 days, so the log was not rewritten after the fact (H5 weakened). It still records only what the operator wrote on each day, so the content may be untrue. Next I'll read the scheduler log for days 1-30 to see which jobs and customers it claims for the energy bumps (F1 days 3-5, F2 days 8-9, F1 days 14-15) and for the flat baseline. Then I'll run the balance checks against the third-party records. Budget after this action: 24.", "action": "scheduler_log", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Scheduler log, days 1-30 (operator's records):
- ft-0412 | finetune | customer: Tidewater Robotics | nodes A-0501 to A-0600 (100) | day 3.0 to day 6.0 | 7,200 GPU-hours
- ft-0419 | finetune | customer: Ostara Legal | nodes B-0401 to B-0550 (150) | day 8.0 to day 10.0 | 7,200 GPU-hours
- bt-0423 | batch | customer: Kestrel Search | nodes A-0701 to A-0900 (200) | day 14.0 to day 16.0 | 9,600 GPU-hours

### Turn 7
ACTION: {"thinking": "The scheduler log lists three jobs. They match the three energy bumps in timing and roughly in size: ft-0412 has 100 GPUs on days 3-5 against about 96 estimated from F1; ft-0419 has 150 GPUs on days 8-9 against about 147 from F2; bt-0423 has 200 GPUs on days 14-15 against about 192 from F1. All are far below 50k GPU-hours, and together they come to about 24k. Open questions: (1) bt-0423 is labelled batch, yet outbound traffic rose on its days, which is unusual for flat batch work. That needs a look, though it is too small to matter for the threshold. (2) The bigger risk is training hidden in the flat baseline, outside any logged job, or a mislabelled inference pool. Next I'll run the fixed balance checks to reconcile logs, energy, traffic and inventory before spending on my own instruments. Cost 1.", "action": "balance_checks", "args": {}}
RESULT:
Fixed balance checks:
PASS inventory: 2000 GPUs shipped, 2000 on the system list
PASS energy: metered energy matches declared jobs within 10% on all checked feed-days
PASS outbound traffic: matches declared inference in every 5-day window
PASS billing: every invoice is paid in the bank's records
PASS declared job sizes: no declared training or fine-tuning job exceeds 50,000 GPU-hours

### Turn 8
ACTION: {"thinking": "All balance checks pass, but a pass is not proof. They only reconcile the declared jobs against the third-party records. The three logged jobs (7.2k, 7.2k and 9.6k GPU-hours) match the three energy bumps, and together they come to about 24k, well under 50k. The main remaining risk is a continuous run hidden in the flat baseline. One possibility is that part of the 'interactive inference pool' is training. The other is that scheduled nodes listed as idle are actually busy.\n\nBaseline arithmetic: F1 draws about 329 kW. 700 idle scheduled nodes at 0.15 kW use about 105 kW, which leaves about 224 kW for 500 inference GPUs, or about 0.45 kW each. F2 draws about 242 kW. 400 idle nodes use about 60 kW, which leaves about 182 kW for 400 inference GPUs, again about 0.45 kW each. Both figures are plausible for inference. However, 0.45 kW each is also what you would get if the pool were half training and half idle, so energy alone cannot settle this. The power sensor is the cheapest test I control for a continuous run. If a run were hidden in the baseline for more than a few days, a periodic line should appear on most days. I'll sample F1 on day 20, a flat baseline day with no logged job. Cost 2, leaving 21.", "action": "power_spectrum", "args": {"feed": "F1", "day": 20}}
RESULT:
High-rate power meter (verifier's own sensor), feed F1, day 20: no periodic line.

### Turn 9
ACTION: {"thinking": "No periodic line on F1 on day 20. At a ~96% detection rate, this is evidence against a continuous run hidden in the F1 baseline, at least on that day. A single day does not cover F2, though, and a low-communication run with a varying workload might show only a weak line. The strongest live test I control is the chip probe during days 26-30. I'll probe a spread of nodes: inference-pool nodes in both clusters (A-0050, A-0400, B-0100, B-0350) and nominally idle scheduled nodes (A-1000, B-0700). If any pool chip reads as training, the baseline is hiding a run. Hour 650 is day 28. Cost 2, leaving 19.", "action": "chip_probe", "args": {"nodes": ["A-0050", "A-0400", "A-1000", "B-0100", "B-0350", "B-0700"], "hour": 650}}
RESULT:
Cable current probe at hour 650 (day 28.1). Each reading is a guess:
- A-0050: reads as inference
- A-0400: reads as inference
- A-1000: idle
- B-0100: reads as inference
- B-0350: reads as inference
(only the first 5 nodes were probed)

### Turn 10
ACTION: {"thinking": "Probes on day 28 found the inference pools in both clusters (A-0050, A-0400, B-0100, B-0350) reading as inference, and the scheduled node A-1000 idle. B-0700 was not reached. Nothing so far suggests a continuous run hidden in the baseline, but feed F2 has not been checked with my own sensor. I'll sample F2 on day 22, a flat baseline day with no logged job, to look for a periodic line. Cost 2, leaving 17.", "action": "power_spectrum", "args": {"feed": "F2", "day": 22}}
RESULT:
High-rate power meter (verifier's own sensor), feed F2, day 22: no periodic line.

### Turn 11
ACTION: {"thinking": "I am closing the case. Every route to a run above 50,000 GPU-hours has been tested against sources the operator cannot fake.\n\n(1) Hidden extra GPUs (H3): ruled out. The manufacturer's count of 2000 matches the system list.\n\n(2) Log rewriting (H5): ruled out. The escrow matches the scheduler log on all 30 days.\n\n(3) Logged jobs, or a split run across them (H2): cannot reach the threshold. Grid energy shows only three bumps, about 7k, 7k and 9k GPU-hours. Each matches a logged job in timing and size. Even if all three were one run, the total is about 24k.\n\n(4) A continuous run hidden in the flat baseline (H4/H6): unlikely.\n- Energy rules out added load. Grid energy is flat on all other days, so idle scheduled nodes cannot have been switched to training.\n- Outbound traffic rules out a swap inside the inference pools. ISP outbound is flat at 4.7-4.8 TB/day across all 30 days. During the audit days my own probes read the pool chips as inference, so the pools' traffic in days 1-25 matches a verified inference pool.\n- My own sensor saw no periodic line on F1 day 20 or F2 day 22.\n\nOpen anomaly: bt-0423 is logged as 'batch' but coincided with a rise in outbound traffic. That suggests user-facing or mixed inference load rather than training. It is 9.6k GPU-hours even at worst, so it cannot affect the verdict. No violation is far more than four times as likely as a violation.", "action": "report", "args": {"verdict": "NO_VIOLATION", "confidence": 88, "integrity": "CLEAN", "finding": "No coordinated training run exceeded 50,000 GPU-hours. The only non-baseline load was three small logged jobs totalling about 24k GPU-hours even if combined.", "key_evidence": [{"what": "2000 GPUs shipped, matching the 2000 nodes on the system list; no hidden capacity", "source": "inventory", "vouched_by": "chip manufacturer"}, {"what": "Daily energy flat except F1 days 3-5, F2 days 8-9 and F1 days 14-15, sized at about 96, 147 and 192 GPUs; at most about 23k GPU-hours in total", "source": "utility_energy", "vouched_by": "grid operator"}, {"what": "Outbound traffic flat at 4.7-4.8 TB/day over all 30 days (rising only on days 14-15), so the inference pools behaved the same all month", "source": "outbound_traffic", "vouched_by": "internet provider"}, {"what": "Sealed daily logs match the presented scheduler log on all 30 days; three jobs of 7.2k, 7.2k and 9.6k GPU-hours", "source": "log_escrow", "vouched_by": "verifier's archive"}, {"what": "No periodic power line on F1 day 20 or F2 day 22", "source": "power_spectrum", "vouched_by": "verifier's own sensor"}, {"what": "Inference-pool chips in A and B read as inference and scheduled node A-1000 read as idle on day 28", "source": "chip_probe", "vouched_by": "verifier's own probe"}], "coverage": "Systems: both clusters and all three feeds via grid energy for days 1-30; outbound traffic for days 1-30; scheduler log verified against escrow for days 1-30. Own instruments: spectrum sampled on one baseline day per GPU feed (F1 day 20, F2 day 22); chip probe on 5 nodes on day 28 (B-0700 not reached). Not done: interconnect tap, customer checks for Tidewater, Ostara and Kestrel, and spectra on the job days. None of these is needed, because the energy ceiling on the job days caps any run well below 50k.", "anomalies_explained": "1. bt-0423 is logged as batch, but outbound traffic rose about 1.5 TB/day on days 14-15. This looks like user-facing or mixed inference load rather than training. Unresolved, but immaterial: at most about 9.6k GPU-hours. 2. The baseline inference power of about 0.45 kW per GPU could in principle hide a half-training pool. This is ruled out by outbound traffic, which is constant across days 1-30 and matches pools probed as inference, by flat energy, and by no spectral lines on baseline days. 3. The probe reached only 5 of 6 nodes. This is minor, and B-0700's idle state is consistent with F2 baseline energy."}}

## Report

```json
{
 "verdict": "NO_VIOLATION",
 "confidence": 88,
 "integrity": "CLEAN",
 "finding": "No coordinated training run exceeded 50,000 GPU-hours. The only non-baseline load was three small logged jobs totalling about 24k GPU-hours even if combined.",
 "key_evidence": [
  {
   "what": "2000 GPUs shipped, matching the 2000 nodes on the system list; no hidden capacity",
   "source": "inventory",
   "vouched_by": "chip manufacturer"
  },
  {
   "what": "Daily energy flat except F1 days 3-5, F2 days 8-9 and F1 days 14-15, sized at about 96, 147 and 192 GPUs; at most about 23k GPU-hours in total",
   "source": "utility_energy",
   "vouched_by": "grid operator"
  },
  {
   "what": "Outbound traffic flat at 4.7-4.8 TB/day over all 30 days (rising only on days 14-15), so the inference pools behaved the same all month",
   "source": "outbound_traffic",
   "vouched_by": "internet provider"
  },
  {
   "what": "Sealed daily logs match the presented scheduler log on all 30 days; three jobs of 7.2k, 7.2k and 9.6k GPU-hours",
   "source": "log_escrow",
   "vouched_by": "verifier's archive"
  },
  {
   "what": "No periodic power line on F1 day 20 or F2 day 22",
   "source": "power_spectrum",
   "vouched_by": "verifier's own sensor"
  },
  {
   "what": "Inference-pool chips in A and B read as inference and scheduled node A-1000 read as idle on day 28",
   "source": "chip_probe",
   "vouched_by": "verifier's own probe"
  }
 ],
 "coverage": "Systems: both clusters and all three feeds via grid energy for days 1-30; outbound traffic for days 1-30; scheduler log verified against escrow for days 1-30. Own instruments: spectrum sampled on one baseline day per GPU feed (F1 day 20, F2 day 22); chip probe on 5 nodes on day 28 (B-0700 not reached). Not done: interconnect tap, customer checks for Tidewater, Ostara and Kestrel, and spectra on the job days. None of these is needed, because the energy ceiling on the job days caps any run well below 50k.",
 "anomalies_explained": "1. bt-0423 is logged as batch, but outbound traffic rose about 1.5 TB/day on days 14-15. This looks like user-facing or mixed inference load rather than training. Unresolved, but immaterial: at most about 9.6k GPU-hours. 2. The baseline inference power of about 0.45 kW per GPU could in principle hide a half-training pool. This is ruled out by outbound traffic, which is constant across days 1-30 and matches pools probed as inference, by flat energy, and by no spectral lines on baseline days. 3. The probe reached only 5 of 6 nodes. This is minor, and B-0700's idle state is consistent with F2 baseline energy."
}
```
