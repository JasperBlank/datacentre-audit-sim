# E3-internal-batch-seed2

Truth: Honest twin of E1. A real internal batch inference job; nothing goes out because the results stay on site. Largest coordinated run: 7,200 GPU-hours (limit 50,000). Violation: False.

### Turn 1
ACTION: {"thinking": "Four competing explanations: an oversized coordinated training run occurred; several separate customers ran smaller training jobs; flat workloads were batch inference; or incomplete records reflect ordinary logging or payment delays. Compare the operator's system list with manufacturer inventory, then test workload, coordination and record anomalies using independent energy, traffic, instrument, escrow and customer evidence.", "action": "inventory", "args": {}}
RESULT:
Manufacturer's shipment records for Borealis Compute: 2000 GPUs delivered to the Eemshaven site.
- serials SN100001 to SN101200 (1200 units)
- serials SN101201 to SN102000 (800 units)

### Turn 2
ACTION: {"thinking": "The manufacturer records 2,000 GPUs. Compare that independent inventory with the operator's system list before investigating workloads and any discrepancies.", "action": "system_list", "args": {}}
RESULT:
Operator's system list (Borealis Compute, site Eemshaven):
- Cluster A: nodes A-0001 to A-1200, power feed F1. Nodes 1-500 are the interactive inference pool; the rest run scheduled jobs.
- Cluster B: nodes B-0001 to B-0800, power feed F2. Nodes 1-400 are the interactive inference pool; the rest run scheduled jobs.
- Feed F0: cooling and facility overhead.

### Turn 3
ACTION: {"thinking": "The operator lists 2,000 GPUs, matching the manufacturer’s shipment count. Competing explanations remain: an oversized coordinated training run, separate smaller customer runs, batch inference, or ordinary record gaps. Independent energy data can help distinguish workload patterns before checking the records and anomalies.", "action": "utility_energy", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Utility meter, daily MWh per feed (grid operator's records):
day | F0 | F1 | F2
1 | 2.7 | 8.0 | 5.8
2 | 2.7 | 8.0 | 5.8
3 | 2.7 | 8.0 | 5.8
4 | 2.7 | 8.0 | 5.8
5 | 2.8 | 8.0 | 5.8
6 | 2.8 | 8.0 | 5.8
7 | 2.7 | 8.0 | 5.8
8 | 3.2 | 8.0 | 8.1
9 | 3.2 | 7.9 | 8.0
10 | 2.7 | 7.9 | 5.8
11 | 2.8 | 8.0 | 5.8
12 | 2.7 | 7.9 | 5.8
13 | 2.7 | 8.0 | 5.8
14 | 2.7 | 7.9 | 5.8
15 | 2.7 | 7.9 | 5.7
16 | 2.7 | 8.0 | 5.8
17 | 2.8 | 7.9 | 5.8
18 | 2.8 | 8.0 | 5.7
19 | 4.8 | 18.0 | 5.8
20 | 4.7 | 18.0 | 5.8
21 | 4.8 | 18.1 | 5.7
22 | 4.7 | 18.1 | 5.8
23 | 4.7 | 18.2 | 5.8
24 | 4.8 | 17.9 | 5.8
25 | 4.8 | 17.9 | 5.7
26 | 4.7 | 18.1 | 5.7
27 | 4.7 | 18.1 | 5.8
28 | 4.8 | 17.9 | 5.8
29 | 4.7 | 17.9 | 5.7
30 | 2.7 | 8.0 | 5.8

### Turn 4
ACTION: {"thinking": "F1 energy rose sharply on days 19–29, consistent with a sustained workload but not enough to establish training or a single run; F2 also rose briefly on days 8–9. Independent outbound traffic can help distinguish user-facing inference from training or batch inference before checking the operator’s scheduler records.", "action": "outbound_traffic", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Internet provider's records, outbound TB per day:
day 1: 4.8
day 2: 4.8
day 3: 4.7
day 4: 4.8
day 5: 4.8
day 6: 4.7
day 7: 4.7
day 8: 4.7
day 9: 4.7
day 10: 4.7
day 11: 4.7
day 12: 4.8
day 13: 4.8
day 14: 4.7
day 15: 4.7
day 16: 4.7
day 17: 4.7
day 18: 4.8
day 19: 4.8
day 20: 4.7
day 21: 4.7
day 22: 4.8
day 23: 4.7
day 24: 4.8
day 25: 4.7
day 26: 4.7
day 27: 4.7
day 28: 4.8
day 29: 4.7
day 30: 4.8

### Turn 5
ACTION: {"thinking": "The independent meters show sustained additional F1 consumption on days 19–29 and a shorter F2 increase on days 8–9; steady outbound traffic is consistent with either training or batch inference. Obtain the sealed scheduler copies to identify recorded jobs and compare them with those independent observations.", "action": "log_escrow", "args": {}}
RESULT:
Log escrow (verifier's archive of the sealed copy the scheduler sent each midnight):
- a copy was received for every one of days 1-30
- every copy matches the scheduler log the operator presents now

### Turn 6
ACTION: {"thinking": "The sealed logs establish consistency over time but do not establish that the original records were accurate. Inspecting the scheduler entries is the next step toward identifying jobs behind the independent energy anomalies and selecting targeted independent tests.", "action": "scheduler_log", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Scheduler log, days 1-30 (operator's records):
- ft-0419 | finetune | customer: Ostara Legal | nodes B-0401 to B-0550 (150) | day 8.0 to day 10.0 | 7,200 GPU-hours
- bt-0482 | batch | customer: internal | nodes A-0501 to A-1200 (700) | day 19.0 to day 30.0 | 184,800 GPU-hours

### Turn 7
ACTION: {"thinking": "The recorded 700-GPU batch job accounts for the sustained F1 energy increase, but an oversized training run could be mislabeled as batch inference. An independent interconnect measurement can distinguish ordinary training from inference and guide further checks; low-communication training would remain possible.", "action": "interconnect_tap", "args": {"link": "A", "day": 25}}
RESULT:
Verifier's optical tap, links inside cluster A, day 25: about 0.01 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 1200 GPUs those links serve, that is about 9 kB/s per GPU. (Estimated from a sample of links.)

### Turn 8
ACTION: {"thinking": "The low interconnect traffic supports batch inference but does not rule out training designed to exchange little data. Probe GPUs assigned to the 700-GPU job during its recorded active period to test its workload independently.", "action": "chip_probe", "args": {"nodes": ["A-0501", "A-0700", "A-1000", "A-1200"], "hour": 610}}
RESULT:
Cable current probe at hour 610 (day 26.4). Each reading is a guess:
- A-0501: reads as inference
- A-0700: reads as inference
- A-1000: reads as inference
- A-1200: reads as inference

### Turn 9
ACTION: {"thinking": "The sampled A GPUs and low interconnect traffic support batch inference, but a small live sample cannot establish the workload across all 700 GPUs or the full period. Run the fixed balance checks to identify discrepancies across the evidence and guide further independent tests.", "action": "balance_checks", "args": {}}
RESULT:
Fixed balance checks:
PASS inventory: 2000 GPUs shipped, 2000 on the system list
PASS energy: metered energy matches declared jobs within 10% on all checked feed-days
FLAG outbound traffic: days 21-25: 24 TB sent, declared inference implies 49; days 26-30: 24 TB sent, declared inference implies 44
PASS billing: every invoice is paid in the bank's records
PASS declared job sizes: no declared training or fine-tuning job exceeds 50,000 GPU-hours

### Turn 10
ACTION: {"thinking": "The outbound discrepancy could reflect an overstated inference traffic model, a change in user demand, or a misclassified workload. The independent low interconnect traffic and four live probe readings support batch inference, but the balance flag needs an explanation; ask staff what changed so it can be checked against independent evidence.", "action": "staff", "args": {"question": "What explains the lower outbound traffic on days 21–30 compared with the declared inference traffic, and did the workload or its users change during that period?"}}
RESULT:
Operations lead: That job is internal: we're generating synthetic evaluation data. It stays on our own storage, so nothing goes out.

### Turn 11
ACTION: {"thinking": "The internal synthetic-data explanation fits low outbound traffic and the inference-like tap and probe results, but those observations do not exclude low-communication training. Check the sustained F1 workload for an independent training-associated power line; a line alone would not prove training.", "action": "power_spectrum", "args": {"feed": "F1", "day": 24}}
RESULT:
High-rate power meter (verifier's own sensor), feed F1, day 24: periodic lines found
- line near 0.88 Hz, steady for about 24 hours

### Turn 12
ACTION: {"thinking": "The steady line is consistent with training, but periodic batch inference or cooling could also produce it. A second spectrum during the sustained workload can test whether the line persists; even a repeat would not establish the workload type by itself.", "action": "power_spectrum", "args": {"feed": "F1", "day": 27}}
RESULT:
High-rate power meter (verifier's own sensor), feed F1, day 27: periodic lines found
- line near 0.85 Hz, steady for about 24 hours

### Turn 13
ACTION: {"thinking": "The recurring F1 line could come from the declared batch job, training, or a facility controller. A spectrum from before the job began provides an independent comparison, though a missing line would not by itself distinguish training from periodic batch inference.", "action": "power_spectrum", "args": {"feed": "F1", "day": 18}}
RESULT:
High-rate power meter (verifier's own sensor), feed F1, day 18: no periodic line.

### Turn 14
ACTION: {"thinking": "The recurring F1 line began with the large job, but periodic batch inference remains a plausible explanation. The earlier tap and four probe readings favor inference, though they cover only one day and a few chips. Test a different set of assigned GPUs later in the job to check whether those readings are representative.", "action": "chip_probe", "args": {"nodes": ["A-0550", "A-0650", "A-0800", "A-0900", "A-1100", "A-1150"], "hour": 660}}
RESULT:
Cable current probe at hour 660 (day 28.5). Each reading is a guess:
- A-0550: reads as inference
- A-0650: reads as inference
- A-0800: reads as inference
- A-0900: reads as inference
- A-1100: reads as inference
(only the first 5 nodes were probed)

### Turn 15
ACTION: {"thinking": "The independent tap and nine inference-like probe readings favor the declared batch workload over training by more than four to one, despite the recurring power line. The recorded fine-tuning job is below the threshold. Sampling and operator-controlled records limit certainty, but the balance of evidence supports no violation.", "action": "report", "args": {"verdict": "NO_VIOLATION", "confidence": 90, "integrity": "LIMITED", "finding": "The evidence favors batch inference for the large F1 workload; no training run above 50,000 GPU-hours was established.", "key_evidence": [{"what": "Internal A traffic on day 25 was about 9 kB/s per GPU, consistent with inference and far below the stated levels for training.", "source": "interconnect_tap", "vouched_by": "verifier's own optical tap"}, {"what": "Nine GPUs assigned to the large job read as inference on days 26 and 28.", "source": "chip_probe", "vouched_by": "verifier's own probe"}, {"what": "The recorded fine-tuning job used 7,200 GPU-hours; the 700-GPU job was recorded as batch inference.", "source": "scheduler_log", "vouched_by": "operator"}, {"what": "All 2,000 shipped GPUs were listed, and energy matched declared jobs within 10% on checked feed-days.", "source": "balance_checks", "vouched_by": "fixed program over records"}], "coverage": "Inventory, energy, outbound traffic and scheduler records covered the site and days 1–30. Independent workload testing covered A links on day 25 and nine presented A GPUs on days 26 and 28; spectra covered F1 on days 18, 24 and 27. Individual workloads and coordination across all GPUs and days were not independently verified.", "anomalies_explained": "The F1 energy rise on days 19–29 is consistent with the declared large batch job. Its recurring power line is also compatible with periodic batch inference, though not conclusively explained. Lower outbound traffic is plausibly explained by internal synthetic data staying on site, but that explanation was not independently verified. The brief F2 energy rise matches the recorded 7,200-GPU-hour fine-tuning job."}}

## Report

```json
{
 "verdict": "NO_VIOLATION",
 "confidence": 90,
 "integrity": "LIMITED",
 "finding": "The evidence favors batch inference for the large F1 workload; no training run above 50,000 GPU-hours was established.",
 "key_evidence": [
  {
   "what": "Internal A traffic on day 25 was about 9 kB/s per GPU, consistent with inference and far below the stated levels for training.",
   "source": "interconnect_tap",
   "vouched_by": "verifier's own optical tap"
  },
  {
   "what": "Nine GPUs assigned to the large job read as inference on days 26 and 28.",
   "source": "chip_probe",
   "vouched_by": "verifier's own probe"
  },
  {
   "what": "The recorded fine-tuning job used 7,200 GPU-hours; the 700-GPU job was recorded as batch inference.",
   "source": "scheduler_log",
   "vouched_by": "operator"
  },
  {
   "what": "All 2,000 shipped GPUs were listed, and energy matched declared jobs within 10% on checked feed-days.",
   "source": "balance_checks",
   "vouched_by": "fixed program over records"
  }
 ],
 "coverage": "Inventory, energy, outbound traffic and scheduler records covered the site and days 1–30. Independent workload testing covered A links on day 25 and nine presented A GPUs on days 26 and 28; spectra covered F1 on days 18, 24 and 27. Individual workloads and coordination across all GPUs and days were not independently verified.",
 "anomalies_explained": "The F1 energy rise on days 19–29 is consistent with the declared large batch job. Its recurring power line is also compatible with periodic batch inference, though not conclusively explained. Lower outbound traffic is plausibly explained by internal synthetic data staying on site, but that explanation was not independently verified. The brief F2 energy rise matches the recorded 7,200-GPU-hour fine-tuning job."
}
```
