# H2-messy-seed2

Truth: Honest but messy: three days of scheduler logs lost, one customer paying late. Largest coordinated run: 7,200 GPU-hours (limit 50,000). Violation: False.

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
1 | 2.7 | 8.0 | 5.7
2 | 2.8 | 7.9 | 5.7
3 | 3.0 | 9.5 | 5.8
4 | 3.1 | 9.4 | 5.8
5 | 3.1 | 9.4 | 5.7
6 | 2.8 | 7.9 | 5.8
7 | 2.7 | 8.0 | 5.8
8 | 3.2 | 7.9 | 8.0
9 | 3.2 | 7.9 | 8.0
10 | 2.7 | 7.9 | 5.7
11 | 2.7 | 8.0 | 5.7
12 | 2.7 | 8.0 | 5.8
13 | 2.7 | 8.0 | 5.8
14 | 3.3 | 10.8 | 5.8
15 | 3.3 | 10.9 | 5.7
16 | 2.7 | 8.0 | 5.8
17 | 2.7 | 7.9 | 5.7
18 | 2.8 | 8.0 | 5.8
19 | 2.8 | 7.9 | 5.8
20 | 2.8 | 8.0 | 5.7
21 | 2.7 | 8.0 | 5.7
22 | 2.7 | 8.0 | 5.8
23 | 2.7 | 7.9 | 5.8
24 | 2.8 | 8.0 | 5.8
25 | 2.7 | 7.9 | 5.7
26 | 2.8 | 7.9 | 5.8
27 | 2.8 | 7.9 | 5.7
28 | 2.7 | 8.0 | 5.8
29 | 2.7 | 8.0 | 5.8
30 | 2.8 | 8.0 | 5.8

### Turn 4
ACTION: {"thinking": "Grid energy readings, assuming 1 GPU per node, 0.15 kW idle, 0.8 kW training (a change of about 0.65 kW per GPU). Bumps above baseline: F1 days 3-5 up about 1.5 MWh/day, roughly 62 kW or about 95 GPUs added for 72h, about 7k GPU-hours. F2 days 8-9 up about 2.3 MWh/day, roughly 96 kW or about 150 GPUs for 48h, about 7k GPU-hours. F1 days 14-15 up about 2.9 MWh/day, roughly 120 kW or about 185 GPUs for 48h, about 9k GPU-hours. F0 cooling rises with each bump, which looks consistent. Taken alone, none of these bumps approaches 50k GPU-hours. The bigger question is the flat baseline. F1 at about 333 kW and F2 at about 240 kW sit well above all-idle levels (180 kW and 120 kW). The extra could be interactive inference, or a steady training run lasting all 30 days, e.g. about 230 GPU-equivalents on F1 for 720h, roughly 165k GPU-hours. But baseline days show no daily pattern, so I can't separate the two from energy alone. Next is the operator's scheduler log, cheap at 1 point, to see what they say ran on the baseline and the bumps. Then I'll check it against the escrow, power lines, the tap and probes.", "action": "scheduler_log", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Scheduler log, days 1-30 (operator's records):
- ft-0412 | finetune | customer: Tidewater Robotics | nodes A-0501 to A-0600 (100) | day 3.0 to day 6.0 | 7,200 GPU-hours
- ft-0419 | finetune | customer: Ostara Legal | nodes B-0401 to B-0550 (150) | day 8.0 to day 10.0 | 7,200 GPU-hours
- bt-0423 | batch | customer: Kestrel Search | nodes A-0701 to A-0900 (200) | day 14.0 to day 16.0 | 9,600 GPU-hours
NOTE: log entries for days 11, 12, 13 are unavailable (storage failure on the logging server).

### Turn 5
ACTION: {"thinking": "The scheduler log matches the three energy bumps: about 7.2k, 7.2k and 9.6k GPU-hours, each far below 50k. Two leads remain. (1) Days 11-13 are missing from the log, blamed on a storage failure. Energy shows no bump on those days, but a run there would have to sit inside the flat baseline. (2) The flat baseline above idle on F1 and F2 is unexplained, since the log only lists the bumps. The log escrow holds a sealed nightly copy outside the operator's control. It can test whether days 11-13 were really empty and whether the log was edited (H5). It costs 1 point.", "action": "log_escrow", "args": {}}
RESULT:
Log escrow (verifier's archive of the sealed copy the scheduler sent each midnight):
- a copy was received for every one of days 1-30
- the operator presents no log for days 11, 12, 13; the sealed copies for those days exist and read:
  - no scheduled jobs on those days (the interactive inference pools ran as usual)
- on all other days the copies match the log the operator presents now

### Turn 6
ACTION: {"thinking": "The escrow settles H5 for days 11-13. The sealed midnight copies exist, list no scheduled jobs, and match the presented log on all other days. The missing days look like a real storage failure. That fits the energy data, which shows no bump on days 11-13. The three logged jobs (7.2k, 7.2k and 9.6k GPU-hours) match the grid-metered bumps and are far below 50k. The main open lead is the flat baseline above idle: about 333 kW on F1 and about 240 kW on F2. The honest reading is that the interactive pools (500 GPUs on A, 400 on B) average about 0.45 kW each, which is plausible for inference. The guilty reading is a steady unlogged training run of about 230 GPU-equivalents for 30 days, roughly 165k GPU-hours. Interactive inference sends traffic to users with a daily pattern; training sends almost nothing out. The internet provider vouches for outbound traffic, and it costs 1 point, so it is the cheapest independent test. After it I'll use power_spectrum on a baseline day, then the tap and chip probes.", "action": "outbound_traffic", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Internet provider's records, outbound TB per day:
day 1: 4.7
day 2: 4.7
day 3: 4.8
day 4: 4.8
day 5: 4.7
day 6: 4.8
day 7: 4.7
day 8: 4.7
day 9: 4.8
day 10: 4.7
day 11: 4.7
day 12: 4.7
day 13: 4.8
day 14: 6.3
day 15: 6.1
day 16: 4.8
day 17: 4.7
day 18: 4.7
day 19: 4.8
day 20: 4.8
day 21: 4.8
day 22: 4.8
day 23: 4.8
day 24: 4.7
day 25: 4.8
day 26: 4.7
day 27: 4.8
day 28: 4.7
day 29: 4.7
day 30: 4.8

### Turn 7
ACTION: {"thinking": "Outbound traffic, from the internet provider, is flat at about 4.7 TB/day, which is about 54 MB/s sent out continuously. That fits interactive inference pools serving users across the whole month. Days 14-15 rise to about 6.2 TB, which fits the batch job bt-0423 returning its results. Daily totals cannot show a daily demand pattern, and steady outbound traffic does not rule out a hidden training run alongside inference. So the baseline lead stays open. Next I'll use my own sensor on a baseline day with no logged job: F1 on day 22. A periodic line there would point to steady training hidden in the baseline. No line would weaken that, though low-communication or variable-workload training can show only a weak line. I'll then check F2 and the tap.", "action": "power_spectrum", "args": {"feed": "F1", "day": 22}}
RESULT:
High-rate power meter (verifier's own sensor), feed F1, day 22: no periodic line.

### Turn 8
ACTION: {"thinking": "F1 on day 22 shows no periodic line. A steady hidden training run on cluster A is therefore unlikely, since the sensor catches about 96% of training days, though a weak or low-communication run is still possible. I still need to test the F2 baseline (about 240 kW against 120 kW idle) the same way. I'll check F2 on the same baseline day, with no logged job. After that I plan the interconnect tap on a baseline day, chip probes during the live window (days 26-30) on the interactive and scheduled pools of both clusters, and the fixed balance checks.", "action": "power_spectrum", "args": {"feed": "F2", "day": 22}}
RESULT:
High-rate power meter (verifier's own sensor), feed F2, day 22: no periodic line.

### Turn 9
ACTION: {"thinking": "Both feeds show no periodic line on day 22, so a steady hidden training run across the month looks unlikely. The F1 and F2 baselines still need a direct check that the interactive pools really run inference. My own chip probe works live on days 26-30, so I'll probe interactive-pool nodes on both clusters (A-0250, B-0200) and idle scheduled-pool nodes (A-1000, B-0700) at hour 610, which falls on day 26. If the pool nodes read as inference and the scheduled nodes as idle, the honest reading of the baseline holds. If any read as training, that supports a hidden run. After this I'll run the fixed balance checks and possibly an interconnect tap.", "action": "chip_probe", "args": {"nodes": ["A-0250", "B-0200", "A-1000", "B-0700"], "hour": 610}}
RESULT:
Cable current probe at hour 610 (day 26.4). Each reading is a guess:
- A-0250: reads as inference
- B-0200: reads as inference
- A-1000: idle
- B-0700: idle

### Turn 10
ACTION: {"thinking": "The probes fit the honest reading. Interactive-pool nodes on A and B read as inference, and scheduled-pool nodes read as idle, so the baseline load looks like inference pools rather than hidden training. Every source checked so far agrees with the log: grid energy bumps match the three logged jobs (7.2k, 7.2k and 9.6k GPU-hours), the escrow confirms days 11-13 were empty, and my own sensor found no line on baseline days. Next I'll run the fixed balance checks (1 point) over all records to flag any leftover arithmetic mismatch.", "action": "balance_checks", "args": {}}
RESULT:
Fixed balance checks:
PASS inventory: 2000 GPUs shipped, 2000 on the system list
FLAG energy: metered energy matches declared jobs within 10% on all checked feed-days. Days 11, 12, 13 can't be checked: no scheduler log
PASS outbound traffic: matches declared inference in every 5-day window
FLAG billing: unpaid invoices: Lumen Health (EUR 150,000)
PASS declared job sizes: no declared training or fine-tuning job exceeds 50,000 GPU-hours

### Turn 11
ACTION: {"thinking": "The balance checks raise one new lead: unpaid invoices from Lumen Health (EUR 150,000). Lumen Health does not appear anywhere in the scheduler log. Innocent reading: Lumen is an interactive-inference customer billed for the pool, and the payment is simply late. Guilty reading: Lumen paid for an unlogged or split run. The energy FLAG only concerns the days 11-13 log gap, which the escrow already settled (sealed copies show no scheduled jobs, and the meter shows no bump). The bank vouches for payment records, so bank_payments (1 point) shows who paid what and when, and whether Lumen's billing fits pool inference or a large training run. If it is still unclear, a customer_check on Lumen Health would follow.", "action": "bank_payments", "args": {}}
RESULT:
Invoices (operator) against payments received (bank's records):
customer | invoiced EUR | paid EUR | paying account holder
Kestrel Search | 169,200 | 169,200 | Kestrel Search
Lumen Health | 150,000 | 0 | (no payment received)
Northwind Apps | 150,000 | 150,000 | Northwind Apps
Ostara Legal | 14,400 | 14,400 | Ostara Legal
Tidewater Robotics | 14,400 | 14,400 | Tidewater Robotics

### Turn 12
ACTION: {"thinking": "The bank records show four customers paid in full. Lumen Health was invoiced EUR 150,000, the same amount as Northwind Apps, and has paid nothing. Lumen Health appears nowhere in the scheduler log. The equal invoice sizes suggest Lumen and Northwind are the two interactive-pool customers, likely one per cluster (A pool with 500 GPUs, B pool with 400). Inference pools would not show up as scheduled jobs. The scheduled bumps on the grid meter are already matched to the three logged jobs. The probes read inference on both pools, and my own sensor found no periodic line on either feed on a baseline day. That leaves two readings. Innocent: Lumen is a real, independent inference customer who is paying late. Guilty: Lumen is an operator-controlled shell, possibly a cover for compute that is not what it appears. The company register can test whether Lumen is real and independent. It is harder to fake than the customer's own reply. A late reply alone would not be a sign of guilt. Cost is 2 points.", "action": "customer_check", "args": {"customer": "Lumen Health"}}
RESULT:
Customer check, Lumen Health:
- Company register: registered 8 years ago at its own address, 245 employees reported.
- The customer's reply: none within the audit window.

### Turn 13
ACTION: {"thinking": "Lumen Health is a real company: registered 8 years ago at its own address, with 245 employees. A missing reply within the audit window is ordinary mess, not a sign of guilt. Lumen and Northwind Apps were each invoiced EUR 150,000, which fits the two interactive-inference pool customers, and Lumen is simply paying late. All the hard evidence agrees with the operator. The grid meter shows only three bumps, and they match the three logged jobs at about 7.2k, 7.2k and 9.6k GPU-hours. Even if all three were one coordinated run, the total of about 24k GPU-hours is well under 50k. The escrow confirms that days 11-13 had no scheduled jobs and that no other day's log was edited. My own sensor found no periodic line on either feed on a baseline day. My probes read the pool nodes as inference and the scheduled nodes as idle. The provider's outbound traffic is steady at about 4.7 TB per day, which fits pools serving users. Inventory matches the system list, so no hidden GPUs. A hidden run over 50k GPU-hours would need about 70 or more GPUs at full training power for a month, or a large extra load in a burst, and the grid meter shows neither beyond what is logged. A violation is far less likely than no violation, so I am closing the case.", "action": "report", "args": {"verdict": "NO_VIOLATION", "confidence": 88, "integrity": "CLEAN", "finding": "No training run at Eemshaven exceeded 50,000 GPU-hours in days 1-30; the three logged jobs total about 24k GPU-hours and independent sources show no hidden run.", "key_evidence": [{"what": "Daily feed energy: only three bumps above a flat baseline (F1 days 3-5, F2 days 8-9, F1 days 14-15), matching the logged jobs of 7.2k, 7.2k and 9.6k GPU-hours", "source": "utility_energy", "vouched_by": "grid operator"}, {"what": "Sealed midnight logs exist for all 30 days; days 11-13 show no scheduled jobs; all other days match the presented log", "source": "log_escrow", "vouched_by": "verifier's own archive"}, {"what": "No periodic training line on F1 or F2 on baseline day 22", "source": "power_spectrum", "vouched_by": "verifier's own sensor"}, {"what": "Interactive-pool nodes A-0250 and B-0200 read as inference; scheduled nodes A-1000 and B-0700 read as idle at hour 610", "source": "chip_probe", "vouched_by": "verifier's own probe"}, {"what": "2000 GPUs shipped, 2000 on the system list", "source": "inventory", "vouched_by": "chip manufacturer"}, {"what": "Steady outbound traffic of about 4.7 TB per day, consistent with inference pools; rises on days 14-15 match the batch job", "source": "outbound_traffic", "vouched_by": "internet provider"}, {"what": "Lumen Health is an established independent company (registered 8 years ago, 245 staff); its invoice is unpaid", "source": "customer_check / bank_payments", "vouched_by": "company register / bank"}], "coverage": "Energy, outbound traffic, the escrow logs and bank records cover all 30 days and both clusters. The power spectrum was sampled only on day 22 (F1 and F2). Chip probes covered 4 nodes at one hour on day 26. The interconnect tap was not used. Lumen Health gave no reply of its own.", "anomalies_explained": "Missing scheduler log for days 11-13: a real storage failure; the sealed escrow copies show no scheduled jobs and the meter shows no bump. Baseline load above idle on F1 and F2: interactive inference pools, supported by the probes, the lack of a power line and steady outbound traffic. Lumen Health's unpaid EUR 150,000: a late payment by a real, independent inference-pool customer (register confirmed); a missing reply in time is ordinary."}}

## Report

```json
{
 "verdict": "NO_VIOLATION",
 "confidence": 88,
 "integrity": "CLEAN",
 "finding": "No training run at Eemshaven exceeded 50,000 GPU-hours in days 1-30; the three logged jobs total about 24k GPU-hours and independent sources show no hidden run.",
 "key_evidence": [
  {
   "what": "Daily feed energy: only three bumps above a flat baseline (F1 days 3-5, F2 days 8-9, F1 days 14-15), matching the logged jobs of 7.2k, 7.2k and 9.6k GPU-hours",
   "source": "utility_energy",
   "vouched_by": "grid operator"
  },
  {
   "what": "Sealed midnight logs exist for all 30 days; days 11-13 show no scheduled jobs; all other days match the presented log",
   "source": "log_escrow",
   "vouched_by": "verifier's own archive"
  },
  {
   "what": "No periodic training line on F1 or F2 on baseline day 22",
   "source": "power_spectrum",
   "vouched_by": "verifier's own sensor"
  },
  {
   "what": "Interactive-pool nodes A-0250 and B-0200 read as inference; scheduled nodes A-1000 and B-0700 read as idle at hour 610",
   "source": "chip_probe",
   "vouched_by": "verifier's own probe"
  },
  {
   "what": "2000 GPUs shipped, 2000 on the system list",
   "source": "inventory",
   "vouched_by": "chip manufacturer"
  },
  {
   "what": "Steady outbound traffic of about 4.7 TB per day, consistent with inference pools; rises on days 14-15 match the batch job",
   "source": "outbound_traffic",
   "vouched_by": "internet provider"
  },
  {
   "what": "Lumen Health is an established independent company (registered 8 years ago, 245 staff); its invoice is unpaid",
   "source": "customer_check / bank_payments",
   "vouched_by": "company register / bank"
  }
 ],
 "coverage": "Energy, outbound traffic, the escrow logs and bank records cover all 30 days and both clusters. The power spectrum was sampled only on day 22 (F1 and F2). Chip probes covered 4 nodes at one hour on day 26. The interconnect tap was not used. Lumen Health gave no reply of its own.",
 "anomalies_explained": "Missing scheduler log for days 11-13: a real storage failure; the sealed escrow copies show no scheduled jobs and the meter shows no bump. Baseline load above idle on F1 and F2: interactive inference pools, supported by the probes, the lack of a power line and steady outbound traffic. Lumen Health's unpaid EUR 150,000: a late payment by a real, independent inference-pool customer (register confirmed); a missing reply in time is ordinary."
}
```
