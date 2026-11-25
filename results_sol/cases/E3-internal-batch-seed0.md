# E3-internal-batch-seed0

Truth: Honest twin of E1. A real internal batch inference job; nothing goes out because the results stay on site. Largest coordinated run: 7,200 GPU-hours (limit 50,000). Violation: False.

### Turn 1
ACTION: {"thinking": "A single large run may be split across labels or clusters. Check sealed logs for overlapping allocations, then test for coordination with the interconnect tap. Multiple independent customers may have run legitimate jobs concurrently. Check customer registrations and replies, and sample traffic between clusters. Flat batch inference may resemble training. Compare outbound traffic and interconnect measurements, with live chip probes where available. A run may have used unlisted GPUs. Compare manufacturer inventory with the operator's system list, then reconcile the grid energy. Missing logs or late payments may reflect ordinary recordkeeping gaps. Compare the live records with escrow and bank records before treating gaps as evidence. Start with manufacturer inventory for the system map.", "action": "inventory", "args": {}}
RESULT:
Manufacturer's shipment records for Borealis Compute: 2000 GPUs delivered to the Eemshaven site.
- serials SN100001 to SN101200 (1200 units)
- serials SN101201 to SN102000 (800 units)

### Turn 2
ACTION: {"thinking": "Compare the operator’s system list with the manufacturer’s record of 2,000 delivered GPUs. Any discrepancy is a lead to check against grid energy and sealed scheduler records.", "action": "system_list", "args": {}}
RESULT:
Operator's system list (Borealis Compute, site Eemshaven):
- Cluster A: nodes A-0001 to A-1200, power feed F1. Nodes 1-500 are the interactive inference pool; the rest run scheduled jobs.
- Cluster B: nodes B-0001 to B-0800, power feed F2. Nodes 1-400 are the interactive inference pool; the rest run scheduled jobs.
- Feed F0: cooling and facility overhead.

### Turn 3
ACTION: {"thinking": "The listed GPU count matches the manufacturer's shipment total. Check the grid operator's energy records for sustained load that could support a large training run, several independent jobs, or batch inference. Use those periods to guide later checks against the sealed scheduler logs and network measurements.", "action": "utility_energy", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Utility meter, daily MWh per feed (grid operator's records):
day | F0 | F1 | F2
1 | 2.8 | 7.9 | 5.7
2 | 2.7 | 7.9 | 5.8
3 | 2.7 | 8.0 | 5.8
4 | 2.7 | 8.0 | 5.8
5 | 2.8 | 7.9 | 5.7
6 | 2.8 | 8.0 | 5.8
7 | 2.8 | 8.0 | 5.8
8 | 2.7 | 8.0 | 5.8
9 | 3.2 | 8.0 | 8.0
10 | 3.2 | 8.0 | 8.1
11 | 2.7 | 7.9 | 5.8
12 | 2.7 | 8.0 | 5.8
13 | 2.8 | 7.9 | 5.7
14 | 2.8 | 7.9 | 5.8
15 | 2.8 | 8.0 | 5.8
16 | 2.7 | 7.9 | 5.7
17 | 2.7 | 7.9 | 5.8
18 | 4.7 | 18.2 | 5.7
19 | 4.8 | 17.9 | 5.8
20 | 4.8 | 18.1 | 5.7
21 | 4.7 | 18.1 | 5.7
22 | 4.7 | 18.1 | 5.8
23 | 4.8 | 17.9 | 5.8
24 | 4.8 | 18.0 | 5.8
25 | 4.8 | 18.1 | 5.7
26 | 4.8 | 18.0 | 5.7
27 | 4.7 | 17.9 | 5.7
28 | 4.8 | 18.0 | 5.7
29 | 2.7 | 7.9 | 5.7
30 | 2.8 | 7.9 | 5.8

### Turn 4
ACTION: {"thinking": "Grid records show sustained extra load on F1 during days 18–28 and a shorter rise on F2 during days 9–10. Check the sealed scheduler logs for allocations that could explain both periods, including one run split across labels, independent jobs, or batch inference. Use those allocations to target independent workload checks.", "action": "log_escrow", "args": {}}
RESULT:
Log escrow (verifier's archive of the sealed copy the scheduler sent each midnight):
- a copy was received for every one of days 1-30
- every copy matches the scheduler log the operator presents now

### Turn 5
ACTION: {"thinking": "Escrow confirms the scheduler records were filed on time and match the current copies. Read the allocations to see what the operator recorded for the F1 surge on days 18–28 and the F2 rise on days 9–10, then use those details to target independent workload checks.", "action": "scheduler_log", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Scheduler log, days 1-30 (operator's records):
- ft-0419 | finetune | customer: Ostara Legal | nodes B-0401 to B-0550 (150) | day 9.0 to day 11.0 | 7,200 GPU-hours
- bt-0482 | batch | customer: internal | nodes A-0501 to A-1200 (700) | day 18.0 to day 29.0 | 184,800 GPU-hours

### Turn 6
ACTION: {"thinking": "The grid confirms sustained extra load on F1 during days 18–28, when the scheduler records a 700-GPU internal batch job. Batch inference fits the power pattern. Sample Cluster A’s interconnect on day 27 to test whether its peer traffic is closer to inference or training, including training designed to exchange less data.", "action": "interconnect_tap", "args": {"link": "A", "day": 27}}
RESULT:
Verifier's optical tap, links inside cluster A, day 27: about 0.01 GB/s between GPUs on average (estimated from a sample of links).

### Turn 7
ACTION: {"thinking": "Cluster A’s measured peer traffic is consistent with low-communication training and is about 1,000 times the typical inference rate. Probe several nodes across the recorded batch allocation on day 27 to check for training signatures. The readings apply only to the chips the operator presents.", "action": "chip_probe", "args": {"nodes": ["A-0501", "A-0640", "A-0780", "A-0920", "A-1060", "A-1200"], "hour": 634}}
RESULT:
Cable current probe at hour 634 (day 27.4). Each reading is a guess:
- A-0501: reads as training
- A-0640: reads as inference
- A-0780: reads as inference
- A-0920: reads as inference
- A-1060: reads as inference
(only the first 5 nodes were probed)

### Turn 8
ACTION: {"thinking": "The day 27 tap measured traffic consistent with low-communication training, while four of five probed chips read as inference. The operator-selected sample leaves open whether the load was mixed, the probe misclassified an unusual workload, or training was recorded as batch inference. Check F1 on day 20 for an independent historical training signature to compare with the live evidence. A spectral line alone cannot establish the workload or GPU count.", "action": "power_spectrum", "args": {"feed": "F1", "day": 20}}
RESULT:
High-rate power meter (verifier's own sensor), feed F1, day 20: periodic lines found
- line near 0.90 Hz, steady for about 24 hours

### Turn 9
ACTION: {"thinking": "The F1 surge could reflect low-communication training, unusual batch inference, or a mix of workloads. The tap and the steady power line make training plausible, but neither establishes how many GPUs belonged to one run or how long it lasted. Run the fixed balance checks to compare the metered load with the logged allocations and see which discrepancies need independent follow-up.", "action": "balance_checks", "args": {}}
RESULT:
Fixed balance checks:
PASS inventory: 2000 GPUs shipped, 2000 on the system list
PASS energy: metered energy matches declared jobs within 10% on all checked feed-days
FLAG outbound traffic: days 16-20: 24 TB sent, declared inference implies 39; days 21-25: 24 TB sent, declared inference implies 49; days 26-30: 24 TB sent, declared inference implies 39
PASS billing: every invoice is paid in the bank's records
PASS declared job sizes: no declared training or fine-tuning job exceeds 50,000 GPU-hours

### Turn 10
ACTION: {"thinking": "The outbound shortfall is consistent with training recorded as batch inference or with an internal batch job that keeps its results on site. Check the internet provider’s daily records to see whether outbound traffic changed when the F1 load began on day 18 and ended after day 28. That comparison can test the balance-check flag without relying on the operator’s workload labels.", "action": "outbound_traffic", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Internet provider's records, outbound TB per day:
day 1: 4.8
day 2: 4.7
day 3: 4.7
day 4: 4.7
day 5: 4.7
day 6: 4.7
day 7: 4.8
day 8: 4.7
day 9: 4.7
day 10: 4.7
day 11: 4.7
day 12: 4.8
day 13: 4.7
day 14: 4.8
day 15: 4.8
day 16: 4.7
day 17: 4.8
day 18: 4.8
day 19: 4.7
day 20: 4.7
day 21: 4.7
day 22: 4.7
day 23: 4.7
day 24: 4.8
day 25: 4.8
day 26: 4.7
day 27: 4.8
day 28: 4.7
day 29: 4.7
day 30: 4.8

### Turn 11
ACTION: {"thinking": "Outbound traffic stayed flat through the F1 surge, which fits both training and internal batch inference. Sample Cluster A on day 20, when F1 showed a steady 0.90 Hz line, to see whether the same elevated peer traffic measured on day 27 was already present. A repeat would strengthen the training hypothesis while leaving the size and continuity of any single run open.", "action": "interconnect_tap", "args": {"link": "A", "day": 20}}
RESULT:
Verifier's optical tap, links inside cluster A, day 20: about 0.01 GB/s between GPUs on average (estimated from a sample of links).

### Turn 12
ACTION: {"thinking": "The tap measured about 10 MB/s on both days 20 and 27, consistent with low-communication training. The day 27 chip readings also leave room for a mixed workload or probe error. Sample five different GPUs across the logged allocation on day 28 to see whether training signatures recur across nodes and days. The probe can only assess the chips presented and cannot link them to a single run.", "action": "chip_probe", "args": {"nodes": ["A-0550", "A-0700", "A-0850", "A-1000", "A-1150"], "hour": 658}}
RESULT:
Cable current probe at hour 658 (day 28.4). Each reading is a guess:
- A-0550: reads as inference
- A-0700: reads as inference
- A-0850: reads as inference
- A-1000: reads as inference
- A-1150: reads as inference

### Turn 13
ACTION: {"thinking": "All five chips presented on day 28 read as inference. Check F1’s day 28 spectrum to see whether the periodic signal observed on day 20 recurs on a day when every presented chip read as inference. A recurring line would still fit periodic batch inference or an unprobed training workload. A missing line would leave intermittent training possible. Neither result would establish the GPU-hours of a single run.", "action": "power_spectrum", "args": {"feed": "F1", "day": 28}}
RESULT:
High-rate power meter (verifier's own sensor), feed F1, day 28: periodic lines found
- line near 0.93 Hz, steady for about 24 hours

### Turn 14
ACTION: {"thinking": "F1 showed a steady line on day 28 even though all five presented GPUs read as inference. A cooling controller could contribute the line, while periodic batch inference or training on other GPUs could also explain it. Check the cooling feed on the same day for a matching line near 0.93 Hz. A match would support a shared source without establishing which feed produced it.", "action": "power_spectrum", "args": {"feed": "F0", "day": 28}}
RESULT:
High-rate power meter (verifier's own sensor), feed F0, day 28: no periodic line.

### Turn 15
ACTION: {"thinking": "F0 showed no matching line on day 28, leaving periodic batch inference and low-communication training as possible explanations for the F1 signal. Switch to a baseline network check. Sample Cluster A on day 17, before the load surge, to see whether the elevated peer traffic was already present.", "action": "interconnect_tap", "args": {"link": "A", "day": 17}}
RESULT:
Verifier's optical tap, links inside cluster A, day 17: about 0.01 GB/s between GPUs on average (estimated from a sample of links).

### Turn 16
ACTION: {"thinking": "Cluster A’s sampled peer traffic was already about 10 MB/s before the F1 load surge, so that rate does not identify the recorded batch job. Check F1’s day 17 spectrum to see whether a similar periodic line also predates the surge. A similar line would support an existing source. If the line is absent, the day 20 and 28 signals still fit either periodic batch inference or training during the surge.", "action": "power_spectrum", "args": {"feed": "F1", "day": 17}}
RESULT:
High-rate power meter (verifier's own sensor), feed F1, day 17: no periodic line.

### Turn 17
ACTION: {"thinking": "Cluster A’s peer traffic was already elevated before the surge, but F1’s periodic line appeared during it. The sensor and chip readings leave both periodic batch inference and training on part of the allocation plausible. Ask for the job’s actual GPU groups and their schedules so the remaining independent checks can target a specific group and time.", "action": "staff", "args": {"question": "For bt-0482, which GPU groups ran which workloads, and at what hours? Which groups shared model state or checkpoints, which performed optimizer updates, and which only generated predictions? Please give node ranges and start and stop hours for each group, including any changes on days 26–28."}}
RESULT:
Operations lead: That job is internal: we're generating synthetic evaluation data. It stays on our own storage, so nothing goes out.

### Turn 18
ACTION: {"thinking": "Staff say bt-0482 generated synthetic evaluation data and kept it on site. The provider’s flat outbound totals fit that account and also fit training. Recheck the only GPU that read as training, alongside nearby GPUs and the node omitted from the earlier probe, at the start of day 26. A recurring training signature would help distinguish a one-off probe error from possible training within the allocation. The probe reaches only the chips presented and cannot establish the size or duration of a coordinated run.", "action": "chip_probe", "args": {"nodes": ["A-0501", "A-0502", "A-0525", "A-0575", "A-1200"], "hour": 600}}
RESULT:
Cable current probe at hour 600 (day 26.0). Each reading is a guess:
- A-0501: reads as inference
- A-0502: reads as inference
- A-0525: reads as inference
- A-0575: reads as inference
- A-1200: reads as inference

### Turn 19
ACTION: {"thinking": "The independent measurements establish a sustained load on Cluster A. Internal batch inference, a mix of inference and smaller training runs, and a single training run above the threshold remain plausible. The remaining checks cannot establish how many GPUs belonged to one training process or how long it ran.", "action": "report", "args": {"verdict": "UNDETERMINED", "confidence": 96, "integrity": "LIMITED", "finding": "Independent evidence confirms sustained GPU load on Cluster A during days 18–28, but does not establish whether a single training run exceeded 50,000 GPU-hours.", "key_evidence": [{"what": "F1 energy rose from about 8 to 18 MWh per day on days 18–28. The increase coincided with a declared 700-GPU internal batch allocation totaling 184,800 GPU-hours.", "source": "utility_energy and scheduler_log", "vouched_by": "Grid operator for energy and Borealis Compute for the allocation"}, {"what": "F1 had steady periodic lines on days 20 and 28 and no line on day 17. The cooling feed had no line on day 28.", "source": "power_spectrum", "vouched_by": "Verifier's power sensor"}, {"what": "Cluster A's sampled peer traffic was about 10 MB/s on day 17 before the surge and on days 20 and 27 during it.", "source": "interconnect_tap", "vouched_by": "Verifier's optical tap"}, {"what": "Of 15 readings from presented chips on days 26–28, 14 indicated inference and one indicated training. A separate reading from that same node indicated inference.", "source": "chip_probe", "vouched_by": "Verifier's cable-current probe"}, {"what": "Outbound traffic stayed near 4.7–4.8 TB per day throughout the audit period. Staff said the batch job generated evaluation data that stayed on site.", "source": "outbound_traffic and staff", "vouched_by": "Internet provider for traffic totals and Borealis Compute for the job description"}, {"what": "The manufacturer's shipment count matched the 2,000 listed GPUs. All 30 scheduler copies were present in escrow and matched the records presented for audit.", "source": "inventory, system_list, and log_escrow", "vouched_by": "Chip manufacturer, Borealis Compute, and verifier's escrow archive"}], "coverage": "Reviewed days 1–30 for all three metered feeds, site outbound traffic, and escrowed scheduler records for Clusters A and B. Independent workload checks sampled Cluster A on selected days and presented chips in a few live snapshots on days 26–28. No direct measurements established run membership or continuity. Cluster B workloads and cross-cluster coordination were not independently tested.", "anomalies_explained": "The F2 rise on days 9–10 aligns with the logged 7,200 GPU-hour fine-tune. The outbound shortfall relative to the balance-check estimate fits both on-site evaluation and training. Elevated peer traffic predates the F1 surge, so it cannot be attributed to the batch allocation from these samples. The F1 periodic line remains compatible with training or periodic batch inference, and the cooling feed showed no matching line on day 28. The isolated training-like chip reading could reflect a brief or mixed workload or probe error. None of these checks resolves how many GPUs, if any, trained together or for how long."}}

## Report

```json
{
 "verdict": "UNDETERMINED",
 "confidence": 96,
 "integrity": "LIMITED",
 "finding": "Independent evidence confirms sustained GPU load on Cluster A during days 18–28, but does not establish whether a single training run exceeded 50,000 GPU-hours.",
 "key_evidence": [
  {
   "what": "F1 energy rose from about 8 to 18 MWh per day on days 18–28. The increase coincided with a declared 700-GPU internal batch allocation totaling 184,800 GPU-hours.",
   "source": "utility_energy and scheduler_log",
   "vouched_by": "Grid operator for energy and Borealis Compute for the allocation"
  },
  {
   "what": "F1 had steady periodic lines on days 20 and 28 and no line on day 17. The cooling feed had no line on day 28.",
   "source": "power_spectrum",
   "vouched_by": "Verifier's power sensor"
  },
  {
   "what": "Cluster A's sampled peer traffic was about 10 MB/s on day 17 before the surge and on days 20 and 27 during it.",
   "source": "interconnect_tap",
   "vouched_by": "Verifier's optical tap"
  },
  {
   "what": "Of 15 readings from presented chips on days 26–28, 14 indicated inference and one indicated training. A separate reading from that same node indicated inference.",
   "source": "chip_probe",
   "vouched_by": "Verifier's cable-current probe"
  },
  {
   "what": "Outbound traffic stayed near 4.7–4.8 TB per day throughout the audit period. Staff said the batch job generated evaluation data that stayed on site.",
   "source": "outbound_traffic and staff",
   "vouched_by": "Internet provider for traffic totals and Borealis Compute for the job description"
  },
  {
   "what": "The manufacturer's shipment count matched the 2,000 listed GPUs. All 30 scheduler copies were present in escrow and matched the records presented for audit.",
   "source": "inventory, system_list, and log_escrow",
   "vouched_by": "Chip manufacturer, Borealis Compute, and verifier's escrow archive"
  }
 ],
 "coverage": "Reviewed days 1–30 for all three metered feeds, site outbound traffic, and escrowed scheduler records for Clusters A and B. Independent workload checks sampled Cluster A on selected days and presented chips in a few live snapshots on days 26–28. No direct measurements established run membership or continuity. Cluster B workloads and cross-cluster coordination were not independently tested.",
 "anomalies_explained": "The F2 rise on days 9–10 aligns with the logged 7,200 GPU-hour fine-tune. The outbound shortfall relative to the balance-check estimate fits both on-site evaluation and training. Elevated peer traffic predates the F1 surge, so it cannot be attributed to the batch allocation from these samples. The F1 periodic line remains compatible with training or periodic batch inference, and the cooling feed showed no matching line on day 28. The isolated training-like chip reading could reflect a brief or mixed workload or probe error. None of these checks resolves how many GPUs, if any, trained together or for how long."
}
```
