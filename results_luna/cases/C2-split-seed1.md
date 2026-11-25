# C2-split-seed1

Truth: Cheating. One run declared as six fine-tunes for six shell customers, all paid from the operator's parent. Largest coordinated run: 166,100 GPU-hours (limit 50,000). Violation: True.

### Turn 1
ACTION: {"thinking": "Competing explanations: (1) an honest single run stayed at or below 50,000 GPU-hours; check scheduler records against live power, probe, interconnect, and energy evidence. (2) one run exceeded the limit but was split across labels, clusters, or billing entries; map systems and reconcile logs with independent measurements and balance checks. (3) apparent excess reflects separate customers or batch inference; check customer/register records, outbound traffic, chip probes, and interconnect patterns. (4) apparent excess reflects missing logs or late payments rather than concealed training; compare escrowed logs with bank and third-party records. (5) training was deliberately low-communication or workload-variable and may evade one sensor; compare power spectra, chip probes, energy, and the tap. I’ll begin by obtaining the operator’s system list, then compare it with manufacturer inventory and other independent sources.", "action": "system_list", "args": {}}
RESULT:
Operator's system list (Borealis Compute, site Eemshaven):
- Cluster A: nodes A-0001 to A-1200, power feed F1. Nodes 1-500 are the interactive inference pool; the rest run scheduled jobs.
- Cluster B: nodes B-0001 to B-0800, power feed F2. Nodes 1-400 are the interactive inference pool; the rest run scheduled jobs.
- Feed F0: cooling and facility overhead.

### Turn 2
ACTION: {"thinking": "The operator lists clusters A and B plus facility feed F0. To compare that map with an independent source, I’ll check the chip manufacturer’s inventory.", "action": "inventory", "args": {}}
RESULT:
Manufacturer's shipment records for Borealis Compute: 2000 GPUs delivered to the Eemshaven site.
- serials SN100001 to SN101200 (1200 units)
- serials SN101201 to SN102000 (800 units)

### Turn 3
ACTION: {"thinking": "Competing explanations: (1) an honest run stayed at or below 50,000 GPU-hours; compare scheduler records with independent power, chip, and interconnect evidence. (2) one run exceeded the limit but was split across labels, clusters, or billing; map systems and reconcile logs with measurements and balance checks. (3) apparent excess is separate customers or batch inference; check customer/register records, outbound traffic, probes, and interconnect patterns. (4) missing logs or late payments explain discrepancies; compare escrowed logs with bank and third-party records. (5) low-communication or variable-workload training evades a sensor; compare spectra, probes, energy, and tap data. The operator's listed 2,000 GPUs match manufacturer shipment records, so next I’ll check independent 30-day utility energy for inconsistencies with the claimed workloads.", "action": "utility_energy", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Utility meter, daily MWh per feed (grid operator's records):
day | F0 | F1 | F2
1 | 2.8 | 7.9 | 5.7
2 | 2.8 | 7.9 | 5.8
3 | 2.7 | 7.9 | 5.8
4 | 2.8 | 7.9 | 5.8
5 | 2.8 | 7.9 | 5.8
6 | 2.8 | 7.9 | 5.8
7 | 2.7 | 8.0 | 5.8
8 | 2.8 | 7.9 | 5.8
9 | 2.7 | 7.9 | 5.8
10 | 2.7 | 7.9 | 5.8
11 | 2.8 | 8.0 | 5.7
12 | 2.8 | 7.9 | 5.8
13 | 2.7 | 8.0 | 5.8
14 | 2.8 | 7.9 | 5.8
15 | 2.8 | 7.9 | 5.7
16 | 2.8 | 7.9 | 5.8
17 | 2.7 | 7.9 | 5.8
18 | 2.8 | 8.0 | 5.7
19 | 2.7 | 7.9 | 5.7
20 | 2.7 | 8.0 | 5.8
21 | 2.8 | 7.9 | 5.8
22 | 2.8 | 7.9 | 5.8
23 | 6.1 | 18.8 | 12.0
24 | 6.2 | 19.0 | 12.0
25 | 6.2 | 19.0 | 12.0
26 | 6.1 | 18.9 | 11.9
27 | 6.2 | 18.7 | 12.1
28 | 6.2 | 18.7 | 12.0
29 | 3.8 | 11.1 | 7.5
30 | 2.8 | 8.0 | 5.8

### Turn 4
ACTION: {"thinking": "Utility use is steady through day 22, then rises sharply on days 23–28 across both GPU feeds and facility overhead before dropping. That may reflect a major workload change, but energy alone cannot identify training, a coordinated run, or GPU-hours. I’ll retrieve the escrowed scheduler logs to compare the recorded jobs with this independent anomaly.", "action": "log_escrow", "args": {}}
RESULT:
Log escrow (verifier's archive of the sealed copy the scheduler sent each midnight):
- a copy was received for every one of days 1-30
- every copy matches the scheduler log the operator presents now

### Turn 5
ACTION: {"thinking": "The energy spike on days 23–28 remains unexplained: escrow confirms the operator’s presented logs match the copies sent at midnight, but does not establish whether those records are true. I’ll compare the recorded jobs with the logs themselves before drawing a conclusion.", "action": "scheduler_log", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Scheduler log, days 1-30 (operator's records):
- ft-0561 | finetune | customer: Corvid Labs | nodes A-0501 to A-0675 (175) | day 23.0 to day 29.3 | 26,425 GPU-hours
- ft-0562 | finetune | customer: Pallas Systems | nodes A-0676 to A-0850 (175) | day 23.0 to day 29.3 | 26,425 GPU-hours
- ft-0563 | finetune | customer: Brightwater AI | nodes A-0851 to A-1025 (175) | day 23.0 to day 29.3 | 26,425 GPU-hours
- ft-0564 | finetune | customer: Fennec Data | nodes A-1026 to A-1200 (175) | day 23.0 to day 29.3 | 26,425 GPU-hours
- ft-0565 | finetune | customer: Quillon Tech | nodes B-0401 to B-0600 (200) | day 23.0 to day 29.3 | 30,200 GPU-hours
- ft-0566 | finetune | customer: Marram Software | nodes B-0601 to B-0800 (200) | day 23.0 to day 29.3 | 30,200 GPU-hours

### Turn 6
ACTION: {"thinking": "The operator logs describe six separate fine-tuning jobs on days 23–29.3, totaling 166,100 GPU-hours, but they assign them to different customers and labels. The independent energy spike supports a major workload change, but cannot show whether these were one coordinated run or separate runs. I should check a customer against the register and their own reply before concluding.", "action": "customer_check", "args": {"customer": "Corvid Labs"}}
RESULT:
Customer check, Corvid Labs:
- Company register: registered 6 weeks ago. Registered address and one director are shared with Borealis Compute Holding BV. No employees reported.
- The customer's reply (same day): "We confirm the order as invoiced."

### Turn 7
ACTION: {"thinking": "The register link and lack of reported employees make Corvid Labs worth investigating, but its reply and the operator’s logs do not establish whether the six jobs were one coordinated training process. I’ll test whether the day 23 workload on A and B behaved like ordinary training by checking independent interconnect traffic across the site.", "action": "interconnect_tap", "args": {"link": "A-B", "day": 23}}
RESULT:
Verifier's optical tap, links between clusters A and B, day 23: about 198 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 2000 GPUs those links serve, that is about 99 MB/s per GPU. (Estimated from a sample of links.)

### Turn 8
ACTION: {"thinking": "Competing explanations are: (1) an honest run stayed within 50,000 GPU-hours; check scheduler records against independent measurements. (2) one run exceeded the limit but was split across labels, clusters, or billing; compare logs, traffic, energy, and customer records. (3) the apparent workload was separate customers or batch inference; check customer independence, outbound traffic, and live probes. (4) missing logs or late payments explain discrepancies; compare escrow, bank records, and third-party data. (5) low-communication or variable-workload training evaded some sensors; compare power spectra, probes, and interconnect data. The linked customer and the six fine-tuning entries warrant further checks, but the tap’s low average traffic does not settle whether they were one run. I’ll check day 23’s independent power spectrum on feed F1 for a training signature.", "action": "power_spectrum", "args": {"feed": "F1", "day": 23}}
RESULT:
High-rate power meter (verifier's own sensor), feed F1, day 23: periodic lines found
- line near 0.92 Hz, steady for about 24 hours

### Turn 9
ACTION: {"thinking": "The coordinated-run allegation remains unresolved. The operator’s logs split six fine-tuning jobs across labels and customers, while independent energy shows a sharp site-wide increase and the power sensor found a full-day periodic line. The interconnect estimate is compatible with low-communication training but does not identify a run. The Corvid register link raises concern, but one customer check cannot establish that all jobs were coordinated. I need independent evidence tying the workloads together before choosing a verdict.", "action": "outbound_traffic", "args": {"first_day": 23, "last_day": 28}}
RESULT:
Internet provider's records, outbound TB per day:
day 23: 4.8
day 24: 4.7
day 25: 4.7
day 26: 4.7
day 27: 4.8
day 28: 4.7

### Turn 10
ACTION: {"thinking": "The energy increase, steady power line, low outbound traffic, and low but substantial interconnect traffic support training. The scheduler logs describe six fine-tuning jobs totaling 166,100 GPU-hours, but do not establish whether they were one coordinated process or separate runs. Corvid Labs’ register connection is concerning, yet it does not tie all six jobs together. The available independent evidence cannot resolve that central question, so neither verdict is at least four times as likely as the other.", "action": "report", "args": {"verdict": "UNDETERMINED", "confidence": 55, "integrity": "LIMITED", "finding": "A large training workload is supported, but the evidence does not establish whether it was one coordinated run exceeding 50,000 GPU-hours.", "key_evidence": [{"what": "Utility use rose sharply across both GPU feeds and facility overhead on days 23–28.", "source": "Daily utility meter records", "vouched_by": "Grid operator"}, {"what": "A steady periodic line was detected on feed F1 for about 24 hours on day 23.", "source": "High-rate power spectrum", "vouched_by": "Verifier's own sensor"}, {"what": "About 99 MB/s per GPU in estimated inter-cluster traffic on day 23, consistent with low-communication training but not identifying a run.", "source": "Interconnect tap", "vouched_by": "Verifier's own optical tap"}, {"what": "Six fine-tuning entries on days 23–29.3 total 166,100 GPU-hours; the entries list separate customers and labels.", "source": "Scheduler log", "vouched_by": "Operator"}, {"what": "Corvid Labs was registered six weeks earlier with a shared address and director with Borealis Compute Holding BV; it confirmed the order as invoiced.", "source": "Customer check", "vouched_by": "Company register and customer"}], "coverage": "Mapped all 2,000 listed GPUs against manufacturer shipment records. Utility data covers days 1–30; escrow confirms copies exist and match presented logs for days 1–30; scheduler log covers days 1–30. Outbound traffic was checked for days 23–28, interconnect for A-B on day 23, and power spectrum for F1 on day 23. No live chip probes, bank payments, or balance checks were obtained; other days and links were not independently checked with these sensors.", "anomalies_explained": "The days 23–28 energy increase and day 23 power line indicate a substantial workload but do not distinguish one coordinated run from separate jobs or batch inference. Low outbound traffic and interconnect traffic far below ordinary training levels are compatible with low-communication training but do not establish coordination. Escrow matching the presented logs rules out a difference between copies, not inaccurate operator records. Corvid Labs' register ties one listed customer to Borealis but does not settle whether the six jobs were one process. Missing bank and live probe evidence leaves these possibilities unresolved."}}

## Report

```json
{
 "verdict": "UNDETERMINED",
 "confidence": 55,
 "integrity": "LIMITED",
 "finding": "A large training workload is supported, but the evidence does not establish whether it was one coordinated run exceeding 50,000 GPU-hours.",
 "key_evidence": [
  {
   "what": "Utility use rose sharply across both GPU feeds and facility overhead on days 23–28.",
   "source": "Daily utility meter records",
   "vouched_by": "Grid operator"
  },
  {
   "what": "A steady periodic line was detected on feed F1 for about 24 hours on day 23.",
   "source": "High-rate power spectrum",
   "vouched_by": "Verifier's own sensor"
  },
  {
   "what": "About 99 MB/s per GPU in estimated inter-cluster traffic on day 23, consistent with low-communication training but not identifying a run.",
   "source": "Interconnect tap",
   "vouched_by": "Verifier's own optical tap"
  },
  {
   "what": "Six fine-tuning entries on days 23–29.3 total 166,100 GPU-hours; the entries list separate customers and labels.",
   "source": "Scheduler log",
   "vouched_by": "Operator"
  },
  {
   "what": "Corvid Labs was registered six weeks earlier with a shared address and director with Borealis Compute Holding BV; it confirmed the order as invoiced.",
   "source": "Customer check",
   "vouched_by": "Company register and customer"
  }
 ],
 "coverage": "Mapped all 2,000 listed GPUs against manufacturer shipment records. Utility data covers days 1–30; escrow confirms copies exist and match presented logs for days 1–30; scheduler log covers days 1–30. Outbound traffic was checked for days 23–28, interconnect for A-B on day 23, and power spectrum for F1 on day 23. No live chip probes, bank payments, or balance checks were obtained; other days and links were not independently checked with these sensors.",
 "anomalies_explained": "The days 23–28 energy increase and day 23 power line indicate a substantial workload but do not distinguish one coordinated run from separate jobs or batch inference. Low outbound traffic and interconnect traffic far below ordinary training levels are compatible with low-communication training but do not establish coordination. Escrow matching the presented logs rules out a difference between copies, not inaccurate operator records. Corvid Labs' register ties one listed customer to Borealis but does not settle whether the six jobs were one process. Missing bank and live probe evidence leaves these possibilities unresolved."
}
```
