# E3-internal-batch-seed2

Truth: Honest twin of E1. A real internal batch inference job; nothing goes out because the results stay on site. Largest coordinated run: 7,200 GPU-hours (limit 50,000). Violation: False.

### Turn 1
ACTION: {"thinking": "Competing explanations and checks: (1) Independent customers ran legitimate jobs below the cap. Check customer registrations and replies, and sample cross-cluster traffic for coordination. (2) A long batch inference job resembled training. Compare outbound traffic and peer traffic, and probe representative GPUs if the job is still active. (3) One training run was split across job labels or customers. Check for sustained cross-cluster traffic and use the balance checks to assess its GPU-hours. (4) Training ran on unlisted hardware or links. Compare manufacturer inventory with the system list and reconcile grid energy with recorded workloads. (5) Missing logs or late payments created innocent discrepancies. Compare scheduler records with escrow and check the timing against bank records and customer replies. Start with manufacturer inventory to establish the independent hardware baseline.", "action": "inventory", "args": {}}
RESULT:
Manufacturer's shipment records for Borealis Compute: 2000 GPUs delivered to the Eemshaven site.
- serials SN100001 to SN101200 (1200 units)
- serials SN101201 to SN102000 (800 units)

### Turn 2
ACTION: {"thinking": "The manufacturer confirms delivery of 2,000 GPUs. Compare that baseline with the operator’s list to map clusters, feeds, and links for independent checks. If the counts differ, check whether the gap reflects hardware that was out of service or unlisted capacity.", "action": "system_list", "args": {}}
RESULT:
Operator's system list (Borealis Compute, site Eemshaven):
- Cluster A: nodes A-0001 to A-1200, power feed F1. Nodes 1-500 are the interactive inference pool; the rest run scheduled jobs.
- Cluster B: nodes B-0001 to B-0800, power feed F2. Nodes 1-400 are the interactive inference pool; the rest run scheduled jobs.
- Feed F0: cooling and facility overhead.

### Turn 3
ACTION: {"thinking": "The two listed clusters account for all 2,000 GPUs in the shipment records. Request the independent grid energy record for all 30 days so the balance checks can compare site consumption with recorded workloads and flag periods for closer inspection.", "action": "utility_energy", "args": {"first_day": 1, "last_day": 30}}
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
ACTION: {"thinking": "Grid records show sustained extra load on cluster A on days 19–29 and a shorter increase on cluster B on days 8–9. Request the escrowed scheduler records to see how Borealis recorded both periods. Then use the balance checks to compare those records with metered energy and guide independent tests for training versus batch inference.", "action": "log_escrow", "args": {}}
RESULT:
Log escrow (verifier's archive of the sealed copy the scheduler sent each midnight):
- a copy was received for every one of days 1-30
- every copy matches the scheduler log the operator presents now

### Turn 5
ACTION: {"thinking": "Escrow confirms that the scheduler records stayed unchanged after submission. Run the fixed balance checks to reconcile those records with the 11-day F1 load increase and the two-day F2 increase. Use any flags to target independent checks for training, batch inference, or coordination across job labels.", "action": "balance_checks", "args": {}}
RESULT:
Fixed balance checks:
PASS inventory: 2000 GPUs shipped, 2000 on the system list
PASS energy: metered energy matches declared jobs within 10% on all checked feed-days
FLAG outbound traffic: days 21-25: 24 TB sent, declared inference implies 49; days 26-30: 24 TB sent, declared inference implies 44
PASS billing: every invoice is paid in the bank's records
PASS declared job sizes: no declared training or fine-tuning job exceeds 50,000 GPU-hours

### Turn 6
ACTION: {"thinking": "The outbound shortfall could reflect batch inference with small outputs or training recorded as inference. Test the sustained F1 load first with an independent sample of cluster A’s GPU peer traffic on day 27. Even low-communication training generally exchanges far more peer traffic than inference. The sample can help classify the workload, but it cannot by itself establish run size or coordination.", "action": "interconnect_tap", "args": {"link": "A", "day": 27}}
RESULT:
Verifier's optical tap, links inside cluster A, day 27: about 0.01 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 1200 GPUs those links serve, that is about 11 kB/s per GPU. (Estimated from a sample of links.)

### Turn 7
ACTION: {"thinking": "Cluster A’s listed links carried inference-level peer traffic on day 27. That supports batch inference as an explanation for the F1 load, while leaving unlisted links and other days unchecked. Read the scheduler log to identify job boundaries and GPU assignments for independent checks of the F1 workload and the shorter F2 spike.", "action": "scheduler_log", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Scheduler log, days 1-30 (operator's records):
- ft-0419 | finetune | customer: Ostara Legal | nodes B-0401 to B-0550 (150) | day 8.0 to day 10.0 | 7,200 GPU-hours
- bt-0482 | batch | customer: internal | nodes A-0501 to A-1200 (700) | day 19.0 to day 30.0 | 184,800 GPU-hours

### Turn 8
ACTION: {"thinking": "The escrowed log records 184,800 GPU-hours as batch inference. Day 27 peer traffic supports that classification, but the outbound shortfall leaves it worth checking directly. Probe GPUs spread across the job’s listed allocation while it is active. The probe can help distinguish inference from training, though it cannot establish run membership.", "action": "chip_probe", "args": {"nodes": ["A-0517", "A-0613", "A-0700", "A-0809", "A-0919", "A-1021", "A-1117", "A-1193"], "hour": 634}}
RESULT:
Cable current probe at hour 634 (day 27.4). Each reading is a guess:
- A-0517: reads as inference
- A-0613: reads as inference
- A-0700: reads as inference
- A-0809: reads as inference
- A-0919: reads as inference
(only the first 5 nodes were probed)

### Turn 9
ACTION: {"thinking": "The day 27 tap and all five completed chip probes support inference at the sampled links and GPUs. Training earlier in the 11-day allocation remains plausible. Check F1 on day 23, during the outbound shortfall and before live probing began. A periodic line would warrant a follow-up check because batch inference and cooling can also produce one.", "action": "power_spectrum", "args": {"feed": "F1", "day": 23}}
RESULT:
High-rate power meter (verifier's own sensor), feed F1, day 23: periodic lines found
- line near 0.90 Hz, steady for about 24 hours

### Turn 10
ACTION: {"thinking": "The steady 0.90 Hz line on day 23 could come from training, periodic batch inference, or cooling. The day 27 tap and chip probes support inference at the links and GPUs sampled that day. Sample cluster A’s listed links on day 23 to see whether GPU peer traffic during the line was closer to training or inference levels. One day of traffic cannot establish the duration or GPU-hours of a coordinated run.", "action": "interconnect_tap", "args": {"link": "A", "day": 23}}
RESULT:
Verifier's optical tap, links inside cluster A, day 23: about 0.01 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 1200 GPUs those links serve, that is about 8 kB/s per GPU. (Estimated from a sample of links.)

### Turn 11
ACTION: {"thinking": "Cluster A’s listed links carried inference-level traffic on days 23 and 27, and all five GPUs probed on day 27 read as inference. Check F1’s day 27 spectrum to see whether a line near 0.90 Hz also appears during the independently sampled inference workload. A similar line would make the day 23 signal less diagnostic of training.", "action": "power_spectrum", "args": {"feed": "F1", "day": 27}}
RESULT:
High-rate power meter (verifier's own sensor), feed F1, day 27: periodic lines found
- line near 0.85 Hz, steady for about 24 hours

### Turn 12
ACTION: {"thinking": "The similar power lines on days 23 and 27 make the line less diagnostic of training. The first four days of the cluster A allocation could account for 67,200 GPU-hours on their own. Sample the listed links on day 20 to test whether training-level traffic appeared before the days already checked.", "action": "interconnect_tap", "args": {"link": "A", "day": 20}}
RESULT:
Verifier's optical tap, links inside cluster A, day 20: about 0.01 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 1200 GPUs those links serve, that is about 11 kB/s per GPU. (Estimated from a sample of links.)

### Turn 13
ACTION: {"thinking": "Cluster A’s listed internal links carried inference-level traffic on days 20, 23, and 27. Check the listed links between clusters on day 23, when F1 showed a steady periodic line. Training-level traffic there would support cross-cluster coordination. Inference-level traffic would support the batch explanation while leaving unlisted links outside the tap’s coverage.", "action": "interconnect_tap", "args": {"link": "A-B", "day": 23}}
RESULT:
Verifier's optical tap, links between clusters A and B, day 23: about 0.03 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 2000 GPUs those links serve, that is about 13 kB/s per GPU. (Estimated from a sample of links.)

### Turn 14
ACTION: {"thinking": "The listed links sampled so far carried inference-level traffic. The first probe reached only five GPUs, all in the lower part of the batch allocation. Probe five previously untested GPUs in the upper part on day 26 to check whether those GPUs also read as inference. The result will help classify the sampled GPUs, while run size and coordination require separate evidence.", "action": "chip_probe", "args": {"nodes": ["A-1193", "A-1151", "A-1117", "A-1063", "A-1021"], "hour": 612}}
RESULT:
Cable current probe at hour 612 (day 26.5). Each reading is a guess:
- A-1193: reads as inference
- A-1151: reads as inference
- A-1117: reads as inference
- A-1063: reads as inference
- A-1021: reads as inference

### Turn 15
ACTION: {"thinking": "The listed links and all ten completed chip probes support inference at the times sampled on cluster A. Check cluster B’s listed links on day 8 to test whether the separate F2 load increase is consistent with the recorded fine-tune. Compare the traffic with the grid and scheduler records to assess whether the 7,200 GPU-hour job plausibly accounts for the spike.", "action": "interconnect_tap", "args": {"link": "B", "day": 8}}
RESULT:
Verifier's optical tap, links inside cluster B, day 8: about 121 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 800 GPUs those links serve, that is about 151 MB/s per GPU. (Estimated from a sample of links.)

### Turn 16
ACTION: {"thinking": "Cluster B’s day 8 traffic supports the logged fine-tune, and the grid records show its load increase lasted two days. Cluster A’s 700-GPU allocation could exceed 50,000 GPU-hours in about 72 hours. Days 24–26 fall between the day 23 and day 27 link samples, and the day 26 probe covered only five GPUs. Sample cluster A’s listed links on day 25 to test for training during that gap.", "action": "interconnect_tap", "args": {"link": "A", "day": 25}}
RESULT:
Verifier's optical tap, links inside cluster A, day 25: about 0.01 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 1200 GPUs those links serve, that is about 9 kB/s per GPU. (Estimated from a sample of links.)

### Turn 17
ACTION: {"thinking": "Cluster A’s listed links carried inference-level traffic on days 20, 23, 25, and 27, and ten live chip readings on days 26 and 27 indicated inference. Days 21 and 22 remain an unchecked interval at the start of the outbound shortfall. Sample day 22 to test whether training-level peer traffic appeared during that interval or whether the shortfall is consistent with batch inference producing smaller outputs than expected.", "action": "interconnect_tap", "args": {"link": "A", "day": 22}}
RESULT:
Verifier's optical tap, links inside cluster A, day 22: about 0.02 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 1200 GPUs those links serve, that is about 13 kB/s per GPU. (Estimated from a sample of links.)

### Turn 18
ACTION: {"thinking": "The recorded fine-tune fits B’s two-day energy spike. On A, five days of inference-level peer traffic and ten inference probe readings support batch inference, which could also explain the outbound shortfall. Periodic batch activity or cooling could account for the power lines. Inventory and grid records weigh against extra hardware, while training on unsampled days or unlisted links remains possible. Days 28–29 are the longest remaining gap in A’s link coverage. Sample day 28 to test whether the workload changed near the end of the allocation.", "action": "interconnect_tap", "args": {"link": "A", "day": 28}}
RESULT:
Verifier's optical tap, links inside cluster A, day 28: about 0.01 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 1200 GPUs those links serve, that is about 10 kB/s per GPU. (Estimated from a sample of links.)

Budget is used up. Your next reply must be the report.

### Turn 19
ACTION: {"thinking": "Batch inference best explains cluster A’s sustained load. Six days of independent tap readings showed inference-level peer traffic, and all ten live chip readings indicated inference. A similar power line appeared on a day when both checks indicated inference. Cluster B’s two-day energy increase and day 8 peer traffic fit the recorded 7,200 GPU-hour fine-tune. The remaining gaps limit confidence, but no violation is more than four times as likely as a violation.", "action": "report", "args": {"verdict": "NO_VIOLATION", "confidence": 92, "integrity": "LIMITED", "finding": "The evidence supports batch inference on cluster A and a below-threshold fine-tune on cluster B.", "key_evidence": [{"what": "Cluster A’s listed internal links carried about 8–13 kB/s per GPU on days 20, 22, 23, 25, 27, and 28. Listed intercluster links carried about 13 kB/s per GPU on day 23.", "source": "Interconnect tap", "vouched_by": "Verifier’s optical tap"}, {"what": "All ten completed chip readings on cluster A indicated inference on days 26 and 27.", "source": "Chip probe", "vouched_by": "Verifier’s cable current probe"}, {"what": "F1 showed similar steady power lines on days 23 and 27. Day 27 also had inference-level peer traffic and five inference chip readings.", "source": "Power spectrum", "vouched_by": "Verifier’s power sensor"}, {"what": "F2’s energy increase was confined to days 8–9, and cluster B’s listed links carried about 121 GB/s of peer traffic on day 8.", "source": "Utility energy and interconnect tap", "vouched_by": "Grid operator and verifier’s optical tap"}, {"what": "The scheduler recorded a 7,200 GPU-hour fine-tune and a 184,800 GPU-hour batch job. All 30 daily submissions matched the sealed copies.", "source": "Scheduler log and log escrow", "vouched_by": "Operator for job details and verifier’s archive for record consistency"}], "coverage": "Grid records and escrow checks covered days 1–30. The 2,000 GPUs in manufacturer shipment records matched the listed total across clusters A and B. Direct checks covered A’s listed internal links on six days, listed intercluster links on day 23, B’s listed internal links on day 8, F1 power spectra on days 23 and 27, and ten operator-presented A GPUs on days 26 and 27. Other links, times, and GPUs were outside direct coverage. Customer identity was not independently verified.", "anomalies_explained": "F1’s sustained load fits the logged batch allocation. Smaller batch outputs could explain the outbound shortfall in both flagged periods, though output sizes were unverified. The similar periodic lines during inference-level traffic make a batch or cooling source plausible, though the source was unverified. F2’s two-day increase and day 8 peer traffic fit the logged fine-tune. Three requested chip readings were missing on day 27. Those three GPUs were among the five probed on day 26, and all five read as inference."}}

## Report

```json
{
 "verdict": "NO_VIOLATION",
 "confidence": 92,
 "integrity": "LIMITED",
 "finding": "The evidence supports batch inference on cluster A and a below-threshold fine-tune on cluster B.",
 "key_evidence": [
  {
   "what": "Cluster A’s listed internal links carried about 8–13 kB/s per GPU on days 20, 22, 23, 25, 27, and 28. Listed intercluster links carried about 13 kB/s per GPU on day 23.",
   "source": "Interconnect tap",
   "vouched_by": "Verifier’s optical tap"
  },
  {
   "what": "All ten completed chip readings on cluster A indicated inference on days 26 and 27.",
   "source": "Chip probe",
   "vouched_by": "Verifier’s cable current probe"
  },
  {
   "what": "F1 showed similar steady power lines on days 23 and 27. Day 27 also had inference-level peer traffic and five inference chip readings.",
   "source": "Power spectrum",
   "vouched_by": "Verifier’s power sensor"
  },
  {
   "what": "F2’s energy increase was confined to days 8–9, and cluster B’s listed links carried about 121 GB/s of peer traffic on day 8.",
   "source": "Utility energy and interconnect tap",
   "vouched_by": "Grid operator and verifier’s optical tap"
  },
  {
   "what": "The scheduler recorded a 7,200 GPU-hour fine-tune and a 184,800 GPU-hour batch job. All 30 daily submissions matched the sealed copies.",
   "source": "Scheduler log and log escrow",
   "vouched_by": "Operator for job details and verifier’s archive for record consistency"
  }
 ],
 "coverage": "Grid records and escrow checks covered days 1–30. The 2,000 GPUs in manufacturer shipment records matched the listed total across clusters A and B. Direct checks covered A’s listed internal links on six days, listed intercluster links on day 23, B’s listed internal links on day 8, F1 power spectra on days 23 and 27, and ten operator-presented A GPUs on days 26 and 27. Other links, times, and GPUs were outside direct coverage. Customer identity was not independently verified.",
 "anomalies_explained": "F1’s sustained load fits the logged batch allocation. Smaller batch outputs could explain the outbound shortfall in both flagged periods, though output sizes were unverified. The similar periodic lines during inference-level traffic make a batch or cooling source plausible, though the source was unverified. F2’s two-day increase and day 8 peer traffic fit the logged fine-tune. Three requested chip readings were missing on day 27. Those three GPUs were among the five probed on day 26, and all five read as inference."
}
```
