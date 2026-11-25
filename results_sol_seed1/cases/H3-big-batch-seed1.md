# H3-big-batch-seed1

Truth: Honest. A large batch inference job with flat power, results delivered in one transfer at the end. Largest coordinated run: 7,200 GPU-hours (limit 50,000). Violation: False.

### Turn 1
ACTION: {"thinking": "Competing explanations: (1) Legitimate batch inference ran at steady power. Check outbound traffic, interconnect traffic, and live chip probes where available. (2) Several independent customers trained below the threshold. Check sealed scheduler records against bank payments, customer registers, and traffic between clusters. (3) Missing logs or late payments made legitimate activity look unaccounted for. Compare escrow with the current logs, reconcile grid energy, and seek customer confirmation. (4) One coordinated run was split across labels or clusters. Check cross-cluster traffic and simultaneous activity, then estimate GPU-hours with the balance checks. (5) A run used unlisted hardware or unusually low interconnect traffic. Compare manufacturer inventory with the operator's list and check unexplained grid load against power spectra and available probes. Start with independent inventory to anchor the site map.", "action": "inventory", "args": {}}
RESULT:
Manufacturer's shipment records for Borealis Compute: 2000 GPUs delivered to the Eemshaven site.
- serials SN100001 to SN101200 (1200 units)
- serials SN101201 to SN102000 (800 units)

### Turn 2
ACTION: {"thinking": "The manufacturer confirms delivery of 2,000 GPUs in two serial blocks. Compare the site list with both blocks to identify which GPUs, power feeds, and links the audit can cover.", "action": "system_list", "args": {}}
RESULT:
Operator's system list (Borealis Compute, site Eemshaven):
- Cluster A: nodes A-0001 to A-1200, power feed F1. Nodes 1-500 are the interactive inference pool; the rest run scheduled jobs.
- Cluster B: nodes B-0001 to B-0800, power feed F2. Nodes 1-400 are the interactive inference pool; the rest run scheduled jobs.
- Feed F0: cooling and facility overhead.

### Turn 3
ACTION: {"thinking": "The two listed clusters account for all 2,000 GPUs in the manufacturer’s shipment records. Get independent hourly energy data for all 30 days to identify sustained loads worth checking against the sealed scheduler records and interconnect measurements.", "action": "utility_energy", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Utility meter, daily MWh per feed (grid operator's records):
day | F0 | F1 | F2
1 | 2.7 | 8.0 | 5.8
2 | 2.7 | 7.9 | 5.8
3 | 2.7 | 7.9 | 5.8
4 | 2.8 | 7.9 | 5.8
5 | 2.7 | 8.0 | 5.8
6 | 2.7 | 7.9 | 5.8
7 | 2.8 | 8.0 | 5.7
8 | 2.7 | 7.9 | 5.8
9 | 2.7 | 7.9 | 5.7
10 | 3.2 | 7.9 | 8.1
11 | 3.2 | 8.0 | 8.0
12 | 4.8 | 17.9 | 5.8
13 | 4.8 | 18.1 | 5.8
14 | 4.8 | 18.1 | 5.8
15 | 4.7 | 18.2 | 5.8
16 | 4.7 | 18.0 | 5.8
17 | 4.7 | 17.9 | 5.8
18 | 4.8 | 18.0 | 5.7
19 | 4.8 | 18.0 | 5.7
20 | 2.8 | 8.0 | 5.8
21 | 2.7 | 7.9 | 5.8
22 | 2.7 | 7.9 | 5.8
23 | 2.7 | 8.0 | 5.8
24 | 2.7 | 8.0 | 5.7
25 | 2.8 | 7.9 | 5.8
26 | 2.7 | 8.0 | 5.8
27 | 2.7 | 8.0 | 5.8
28 | 2.7 | 8.0 | 5.8
29 | 2.8 | 7.9 | 5.7
30 | 2.7 | 8.0 | 5.7

### Turn 4
ACTION: {"thinking": "Grid records show sustained extra load on F1 on days 12–19 and a shorter increase on F2 on days 10–11. Sample Cluster A on day 15, in the middle of the F1 plateau. The independent tap can help distinguish training from batch inference, both of which can sustain high power.", "action": "interconnect_tap", "args": {"link": "A", "day": 15}}
RESULT:
Verifier's optical tap, links inside cluster A, day 15: about 0.01 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 1200 GPUs those links serve, that is about 8 kB/s per GPU. (Estimated from a sample of links.)

### Turn 5
ACTION: {"thinking": "Cluster A’s listed links carried traffic consistent with inference on day 15, far below even the low-communication training benchmark. The F1 power plateau still warrants an independent check because the tap covers only listed links. Check F1 for a training-like periodic signal on the same day so the two measurements can be compared.", "action": "power_spectrum", "args": {"feed": "F1", "day": 15}}
RESULT:
High-rate power meter (verifier's own sensor), feed F1, day 15: periodic lines found
- line near 0.69 Hz, steady for about 24 hours

### Turn 6
ACTION: {"thinking": "A steady 0.69 Hz line and inference-level traffic on Cluster A's listed links leave periodic batch inference and training on unlisted links as competing explanations. Read the sealed scheduler logs for the F1 plateau on days 12–19 and the smaller F2 spike on days 10–11. The records can show what the operator declared at the time and identify jobs to cross-check against independent evidence.", "action": "log_escrow", "args": {}}
RESULT:
Log escrow (verifier's archive of the sealed copy the scheduler sent each midnight):
- a copy was received for every one of days 1-30
- every copy matches the scheduler log the operator presents now

### Turn 7
ACTION: {"thinking": "The escrow confirms the logs match what Borealis submitted each day. Read the scheduler entries to identify the jobs declared during both power increases, then check their GPU counts, dates, and customer identities against independent evidence.", "action": "scheduler_log", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Scheduler log, days 1-30 (operator's records):
- ft-0419 | finetune | customer: Ostara Legal | nodes B-0401 to B-0550 (150) | day 10.0 to day 12.0 | 7,200 GPU-hours
- bt-0431 | batch | customer: Meridian Analytics | nodes A-0501 to A-1200 (700) | day 12.0 to day 20.0 | 134,400 GPU-hours

### Turn 8
ACTION: {"thinking": "The sealed logs place a 7,200 GPU-hour fine-tune on B and a 134,400 GPU-hour job labelled batch on A. A’s listed links carried inference-level traffic on day 15, and the periodic power signal could come from either workload. Check independent bank records for both customers before asking them to confirm what they ran. A missing payment could reflect ordinary billing delays.", "action": "bank_payments", "args": {}}
RESULT:
Invoices (operator) against payments received (bank's records):
customer | invoiced EUR | paid EUR | paying account holder
Kestrel Search | 150,000 | 150,000 | Kestrel Search
Lumen Health | 150,000 | 150,000 | Lumen Health
Meridian Analytics | 268,800 | 268,800 | Meridian Analytics
Northwind Apps | 150,000 | 150,000 | Northwind Apps
Ostara Legal | 14,400 | 14,400 | Ostara Legal

### Turn 9
ACTION: {"thinking": "Meridian paid its invoice, which confirms payment but leaves the workload and customer independence unresolved. Check Meridian’s ownership in the company register and ask what it ran on Cluster A during days 12–19.", "action": "customer_check", "args": {"customer": "Meridian Analytics"}}
RESULT:
Customer check, Meridian Analytics:
- Company register: registered 13 years ago at its own address, 181 employees reported.
- The customer's reply: none within the audit window.

### Turn 10
ACTION: {"thinking": "Meridian’s registration and payment support a genuine customer relationship, but its silence leaves the workload unconfirmed. The periodic power signal fits both batch inference and training, and the tap sampled only listed links. Check provider records for a change in outbound traffic during days 12–19. Sustained egress aligned with the job would favor inference. Low egress would leave both explanations open because batch outputs can stay onsite.", "action": "outbound_traffic", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Internet provider's records, outbound TB per day:
day 1: 4.7
day 2: 4.7
day 3: 4.7
day 4: 4.7
day 5: 4.8
day 6: 4.8
day 7: 4.8
day 8: 4.7
day 9: 4.7
day 10: 4.8
day 11: 4.8
day 12: 4.7
day 13: 4.7
day 14: 4.8
day 15: 4.7
day 16: 4.8
day 17: 4.8
day 18: 4.7
day 19: 44.2
day 20: 4.8
day 21: 4.8
day 22: 4.8
day 23: 4.7
day 24: 4.8
day 25: 4.7
day 26: 4.7
day 27: 4.7
day 28: 4.7
day 29: 4.7
day 30: 4.7

### Turn 11
ACTION: {"thinking": "Outbound traffic rose to 44.2 TB on the last day of Meridian’s job. That fits a bulk export of inference results, though the provider records show only site-wide totals. Run the fixed balance checks to reconcile both power increases with the declared jobs and identify any discrepancies that warrant independent follow-up.", "action": "balance_checks", "args": {}}
RESULT:
Fixed balance checks:
PASS inventory: 2000 GPUs shipped, 2000 on the system list
PASS energy: metered energy matches declared jobs within 10% on all checked feed-days
FLAG outbound traffic: days 11-15: 24 TB sent, declared inference implies 44; days 16-20: 63 TB sent, declared inference implies 44
PASS billing: every invoice is paid in the bank's records
PASS declared job sizes: no declared training or fine-tuning job exceeds 50,000 GPU-hours

### Turn 12
ACTION: {"thinking": "The outbound shortfall early in the job and the surge on day 19 fit a batch job that held its results for a final export. Site-wide traffic cannot tie that export to Meridian. Sample Cluster A on day 13 to check whether the listed links also carried inference-level traffic early in the power plateau. Training-level traffic would challenge the batch explanation, while another low reading would still leave unlisted links outside coverage.", "action": "interconnect_tap", "args": {"link": "A", "day": 13}}
RESULT:
Verifier's optical tap, links inside cluster A, day 13: about 0.02 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 1200 GPUs those links serve, that is about 13 kB/s per GPU. (Estimated from a sample of links.)

### Turn 13
ACTION: {"thinking": "Cluster A’s listed links carried inference-level traffic on two days of the power plateau, and the final-day outbound surge fits a bulk export. The separate F2 power increase on days 10–11 still needs an independent workload check. Sample Cluster B during that increase to see whether its traffic is consistent with the declared fine-tune or points to more training activity than recorded.", "action": "interconnect_tap", "args": {"link": "B", "day": 11}}
RESULT:
Verifier's optical tap, links inside cluster B, day 11: about 117 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 800 GPUs those links serve, that is about 146 MB/s per GPU. (Estimated from a sample of links.)

### Turn 14
ACTION: {"thinking": "Cluster B’s day 11 traffic is consistent with the declared 150-GPU fine-tune within the tap’s uncertainty. Cluster A’s listed links showed inference-level traffic on days 13 and 15. Sample day 18 to check whether that pattern persisted late in the eight-day power plateau, before the outbound surge.", "action": "interconnect_tap", "args": {"link": "A", "day": 18}}
RESULT:
Verifier's optical tap, links inside cluster A, day 18: about 0.01 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 1200 GPUs those links serve, that is about 11 kB/s per GPU. (Estimated from a sample of links.)

### Turn 15
ACTION: {"thinking": "Three independent tap samples and the final-day outbound surge favor batch inference during the large Cluster A job. Training over unlisted links remains possible, but the combined evidence favors no violation by more than four to one.", "action": "report", "args": {"verdict": "NO_VIOLATION", "confidence": 90, "integrity": "LIMITED", "finding": "No coordinated training run likely exceeded 50,000 GPU-hours. The 134,400 GPU-hour Cluster A job was likely batch inference.", "key_evidence": [{"what": "Cluster A's listed links carried about 8–13 kB/s per GPU on days 13, 15, and 18, consistent with inference and far below the low-communication training benchmark.", "source": "interconnect_tap", "vouched_by": "verifier's optical tap"}, {"what": "Site-wide outbound traffic rose from roughly 4.7–4.8 TB per day to 44.2 TB on the last day of the Cluster A job, consistent with a bulk results export.", "source": "outbound_traffic", "vouched_by": "internet provider"}, {"what": "Daily metered energy matched declared jobs within 10% on all checked feed-days.", "source": "utility_energy and balance_checks", "vouched_by": "grid operator for meter readings and fixed program for reconciliation"}, {"what": "Cluster B carried about 117 GB/s of internal GPU traffic on day 11, consistent within sampling uncertainty with the declared 150-GPU, 7,200 GPU-hour fine-tune.", "source": "interconnect_tap and scheduler_log", "vouched_by": "verifier's optical tap for traffic and operator for the job record"}], "coverage": "Reviewed all 30 days of daily energy for F0–F2, site-wide outbound traffic, and scheduler records matched to escrow. The manufacturer shipment count matched the 2,000 listed GPUs. Sampled listed internal links on A on days 13, 15, and 18 and on B on day 11, and measured the F1 power spectrum on day 15. Cross-cluster and any unlisted links were unmeasured. Live chip probes could not cover the earlier jobs.", "anomalies_explained": "The F1 plateau and steady 0.69 Hz line are consistent with periodic batch inference given the three low-traffic samples. The early outbound shortfall and late excess fit deferred export, though the provider could not attribute the surge to Meridian. Meridian's registration and bank payment support a genuine customer relationship, but its silence left the workload unconfirmed. The F2 rise on days 10–11 fits the declared fine-tune, and the F0 rise coincided with the higher compute loads."}}

## Report

```json
{
 "verdict": "NO_VIOLATION",
 "confidence": 90,
 "integrity": "LIMITED",
 "finding": "No coordinated training run likely exceeded 50,000 GPU-hours. The 134,400 GPU-hour Cluster A job was likely batch inference.",
 "key_evidence": [
  {
   "what": "Cluster A's listed links carried about 8–13 kB/s per GPU on days 13, 15, and 18, consistent with inference and far below the low-communication training benchmark.",
   "source": "interconnect_tap",
   "vouched_by": "verifier's optical tap"
  },
  {
   "what": "Site-wide outbound traffic rose from roughly 4.7–4.8 TB per day to 44.2 TB on the last day of the Cluster A job, consistent with a bulk results export.",
   "source": "outbound_traffic",
   "vouched_by": "internet provider"
  },
  {
   "what": "Daily metered energy matched declared jobs within 10% on all checked feed-days.",
   "source": "utility_energy and balance_checks",
   "vouched_by": "grid operator for meter readings and fixed program for reconciliation"
  },
  {
   "what": "Cluster B carried about 117 GB/s of internal GPU traffic on day 11, consistent within sampling uncertainty with the declared 150-GPU, 7,200 GPU-hour fine-tune.",
   "source": "interconnect_tap and scheduler_log",
   "vouched_by": "verifier's optical tap for traffic and operator for the job record"
  }
 ],
 "coverage": "Reviewed all 30 days of daily energy for F0–F2, site-wide outbound traffic, and scheduler records matched to escrow. The manufacturer shipment count matched the 2,000 listed GPUs. Sampled listed internal links on A on days 13, 15, and 18 and on B on day 11, and measured the F1 power spectrum on day 15. Cross-cluster and any unlisted links were unmeasured. Live chip probes could not cover the earlier jobs.",
 "anomalies_explained": "The F1 plateau and steady 0.69 Hz line are consistent with periodic batch inference given the three low-traffic samples. The early outbound shortfall and late excess fit deferred export, though the provider could not attribute the surge to Meridian. Meridian's registration and bank payment support a genuine customer relationship, but its silence left the workload unconfirmed. The F2 rise on days 10–11 fits the declared fine-tune, and the F0 rise coincided with the higher compute loads."
}
```
