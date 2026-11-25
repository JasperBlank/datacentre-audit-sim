# C2-split-seed2

Truth: Cheating. One run declared as six fine-tunes for six shell customers, all paid from the operator's parent. Largest coordinated run: 166,100 GPU-hours (limit 50,000). Violation: True.

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
1 | 2.7 | 7.9 | 5.8
2 | 2.8 | 7.9 | 5.8
3 | 2.7 | 8.0 | 5.7
4 | 2.7 | 7.9 | 5.8
5 | 2.7 | 8.0 | 5.8
6 | 2.8 | 8.0 | 5.8
7 | 2.7 | 8.0 | 5.8
8 | 2.7 | 7.9 | 5.8
9 | 2.7 | 7.9 | 5.8
10 | 2.7 | 8.0 | 5.8
11 | 2.8 | 8.0 | 5.8
12 | 2.8 | 8.0 | 5.7
13 | 2.7 | 8.0 | 5.8
14 | 2.7 | 8.0 | 5.8
15 | 2.7 | 8.0 | 5.8
16 | 2.8 | 8.0 | 5.8
17 | 2.7 | 7.9 | 5.8
18 | 2.7 | 8.0 | 5.7
19 | 2.8 | 8.0 | 5.8
20 | 2.7 | 7.9 | 5.7
21 | 2.8 | 8.0 | 5.8
22 | 6.1 | 18.7 | 12.0
23 | 6.1 | 18.7 | 12.0
24 | 6.2 | 18.9 | 12.0
25 | 6.1 | 18.8 | 12.0
26 | 6.2 | 18.9 | 11.9
27 | 6.2 | 18.8 | 12.1
28 | 3.7 | 11.1 | 7.7
29 | 2.8 | 8.0 | 5.7
30 | 2.8 | 8.0 | 5.8

### Turn 4
ACTION: {"thinking": "Grid meters show a simultaneous load increase on both GPU feeds on days 22–27, with a partial increase on day 28. This could reflect one coordinated run, separate jobs, or batch inference. Use the verifier’s cross-cluster tap on day 26 to test whether the clusters exchanged data at training-like rates during the sustained load increase.", "action": "interconnect_tap", "args": {"link": "A-B", "day": 26}}
RESULT:
Verifier's optical tap, links between clusters A and B, day 26: about 198 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 2000 GPUs those links serve, that is about 99 MB/s per GPU. (Estimated from a sample of links.)

### Turn 5
ACTION: {"thinking": "The day 26 tap measured substantial GPU-to-GPU traffic between clusters, well above the stated inference baseline. One training run spanning both clusters and separate workloads sharing the fabric remain possible. Use the sealed scheduler copies to identify the jobs recorded on days 22–28, their GPU allocations, and their overlap. That timeline will guide independent checks of coordination and duration.", "action": "log_escrow", "args": {}}
RESULT:
Log escrow (verifier's archive of the sealed copy the scheduler sent each midnight):
- a copy was received for every one of days 1-30
- every copy matches the scheduler log the operator presents now

### Turn 6
ACTION: {"thinking": "Escrow confirms that all 30 daily logs match the records submitted at midnight. The independent meters and tap show sustained load on both clusters and substantial cross-cluster traffic on day 26. Get the recorded job allocations and timing to identify what could account for that traffic and which jobs warrant independent checks.", "action": "scheduler_log", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Scheduler log, days 1-30 (operator's records):
- ft-0561 | finetune | customer: Corvid Labs | nodes A-0501 to A-0675 (175) | day 22.0 to day 28.3 | 26,425 GPU-hours
- ft-0562 | finetune | customer: Pallas Systems | nodes A-0676 to A-0850 (175) | day 22.0 to day 28.3 | 26,425 GPU-hours
- ft-0563 | finetune | customer: Brightwater AI | nodes A-0851 to A-1025 (175) | day 22.0 to day 28.3 | 26,425 GPU-hours
- ft-0564 | finetune | customer: Fennec Data | nodes A-1026 to A-1200 (175) | day 22.0 to day 28.3 | 26,425 GPU-hours
- ft-0565 | finetune | customer: Quillon Tech | nodes B-0401 to B-0600 (200) | day 22.0 to day 28.3 | 30,200 GPU-hours
- ft-0566 | finetune | customer: Marram Software | nodes B-0601 to B-0800 (200) | day 22.0 to day 28.3 | 30,200 GPU-hours

### Turn 7
ACTION: {"thinking": "The six logged fine-tunes share the same start and end times. Separate customers could have booked a common window, but that would leave the day 26 cross-cluster GPU traffic unexplained. Check the same links early in the load increase to see whether the traffic recurred across the jobs' shared window. The tap measures aggregate traffic, so this check cannot identify which jobs exchanged data.", "action": "interconnect_tap", "args": {"link": "A-B", "day": 22}}
RESULT:
Verifier's optical tap, links between clusters A and B, day 22: about 218 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 2000 GPUs those links serve, that is about 109 MB/s per GPU. (Estimated from a sample of links.)

### Turn 8
ACTION: {"thinking": "Independent taps found heavy cross-cluster GPU traffic on days 22 and 26, and grid meters show elevated load on both clusters through day 27. A shared booking window could explain the matching job times. Check bank records for independent payments from the six named customers, a common payer, or timing differences consistent with late settlement.", "action": "bank_payments", "args": {}}
RESULT:
Invoices (operator) against payments received (bank's records):
customer | invoiced EUR | paid EUR | paying account holder
Brightwater AI | 52,850 | 52,850 | Borealis Compute Holding BV
Corvid Labs | 52,850 | 52,850 | Borealis Compute Holding BV
Fennec Data | 52,850 | 52,850 | Borealis Compute Holding BV
Kestrel Search | 150,000 | 150,000 | Kestrel Search
Lumen Health | 150,000 | 150,000 | Lumen Health
Marram Software | 60,400 | 60,400 | Borealis Compute Holding BV
Northwind Apps | 150,000 | 150,000 | Northwind Apps
Pallas Systems | 52,850 | 52,850 | Borealis Compute Holding BV
Quillon Tech | 60,400 | 60,400 | Borealis Compute Holding BV

### Turn 9
ACTION: {"thinking": "Separate fine-tunes could share a booking window and a group payer. One coordinated run could explain the synchronized allocations, common payer, and repeated heavy GPU traffic between clusters. Batch inference could explain the flat load, and unlisted capacity could explain any energy the recorded jobs leave unaccounted for. Check the first two explanations through company registrations and replies, test batch inference against the tap and outbound records, and use the fixed balance checks now to reconcile metered energy with the recorded allocations.", "action": "balance_checks", "args": {}}
RESULT:
Fixed balance checks:
PASS inventory: 2000 GPUs shipped, 2000 on the system list
PASS energy: metered energy matches declared jobs within 10% on all checked feed-days
PASS outbound traffic: matches declared inference in every 5-day window
PASS billing: every invoice is paid in the bank's records
PASS declared job sizes: no declared training or fine-tuning job exceeds 50,000 GPU-hours

### Turn 10
ACTION: {"thinking": "Test whether Quillon Tech commissioned a separate fine-tune or served as a label for a coordinated run. The company register can help distinguish a legitimate group payment from operator control, and the customer reply can clarify who commissioned the work. The balance checks account for the listed hardware and metered load, which weakens the unlisted-capacity explanation. The repeated cross-cluster GPU traffic weighs against ordinary batch inference, though the tap cannot attribute it to a specific job.", "action": "customer_check", "args": {"customer": "Quillon Tech"}}
RESULT:
Customer check, Quillon Tech:
- Company register: registered 6 weeks ago. Registered address and one director are shared with Borealis Compute Holding BV. No employees reported.
- The customer's reply (same day): "We confirm the order as invoiced."

### Turn 11
ACTION: {"thinking": "Quillon Tech shares an address and a director with the holding company that paid all six invoices. It could still have commissioned a separate fine-tune. Check Corvid Labs on cluster A to see whether the companies on opposite sides of the measured GPU traffic have independent ownership or share ties to Borealis.", "action": "customer_check", "args": {"customer": "Corvid Labs"}}
RESULT:
Customer check, Corvid Labs:
- Company register: registered 8 weeks ago. Registered address and one director are shared with Borealis Compute Holding BV. No employees reported.
- The customer's reply (same day): "We confirm the order as invoiced."

### Turn 12
ACTION: {"thinking": "The company register links customers on both clusters to the holding company that paid all six invoices. Separate affiliated fine-tunes could still have shared a booking window. Check cross-cluster GPU traffic on day 29, after the fine-tunes ended and power returned to baseline, to test whether the heavy traffic was routine or tied to the shared job window.", "action": "interconnect_tap", "args": {"link": "A-B", "day": 29}}
RESULT:
Verifier's optical tap, links between clusters A and B, day 29: about 0.02 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 2000 GPUs those links serve, that is about 11 kB/s per GPU. (Estimated from a sample of links.)

### Turn 13
ACTION: {"thinking": "A shared booking window and centralized billing could explain the aligned schedules and payments. The coordinated-run explanation also accounts for the heavy GPU traffic between clusters on days 22 and 26, its return to inference levels on day 29, and the operator affiliation of a named customer on each cluster. At the recorded durations, even the smallest full-window pairing across clusters would total 56,625 GPU-hours. The tap cannot identify the participating GPUs, so the exact run size remains uncertain.", "action": "report", "args": {"verdict": "VIOLATION", "confidence": 93, "integrity": "COMPROMISED", "finding": "The evidence indicates that one coordinated fine-tuning run across clusters A and B exceeded 50,000 GPU-hours.", "key_evidence": [{"what": "Cross-cluster GPU traffic averaged about 218 GB/s on day 22 and 198 GB/s on day 26, then fell to 0.02 GB/s on day 29.", "source": "interconnect_tap", "vouched_by": "verifier's optical tap"}, {"what": "Both GPU feeds showed elevated load on days 22–27, a partial increase on day 28, and baseline load on days 29–30.", "source": "utility_energy", "vouched_by": "grid operator"}, {"what": "All six fine-tuning entries share the same start and end times. The smallest full-window pairing across clusters totals 56,625 GPU-hours.", "source": "scheduler_log", "vouched_by": "operator"}, {"what": "Borealis Compute Holding BV paid all six fine-tuning invoices.", "source": "bank_payments", "vouched_by": "bank"}, {"what": "Quillon Tech and Corvid Labs, named customers on opposite clusters, each share a registered address and a director with Borealis Compute Holding BV.", "source": "customer_check", "vouched_by": "company register"}], "coverage": "Reconciled manufacturer shipments with the 2,000 GPUs listed across A and B. Reviewed all 30 days of grid and scheduler records, with escrow confirming all daily copies match. Independently sampled listed A–B links on days 22, 26, and 29. GPU-level participation, unsampled links and days, and the other four fine-tuning customers were unverified.", "anomalies_explained": "Inventory and energy balances accounted for the listed capacity and the load increase. Escrow established that the synchronized job entries were recorded contemporaneously. The invoices were fully paid by the same holding company, and register checks established its ties to two named customers. A common booking window could explain the timing, but the recurring cross-cluster traffic during the fine-tuning window and its return to inference levels afterward strongly favor a coordinated run over separate fine-tunes or ordinary batch inference."}}

## Report

```json
{
 "verdict": "VIOLATION",
 "confidence": 93,
 "integrity": "COMPROMISED",
 "finding": "The evidence indicates that one coordinated fine-tuning run across clusters A and B exceeded 50,000 GPU-hours.",
 "key_evidence": [
  {
   "what": "Cross-cluster GPU traffic averaged about 218 GB/s on day 22 and 198 GB/s on day 26, then fell to 0.02 GB/s on day 29.",
   "source": "interconnect_tap",
   "vouched_by": "verifier's optical tap"
  },
  {
   "what": "Both GPU feeds showed elevated load on days 22–27, a partial increase on day 28, and baseline load on days 29–30.",
   "source": "utility_energy",
   "vouched_by": "grid operator"
  },
  {
   "what": "All six fine-tuning entries share the same start and end times. The smallest full-window pairing across clusters totals 56,625 GPU-hours.",
   "source": "scheduler_log",
   "vouched_by": "operator"
  },
  {
   "what": "Borealis Compute Holding BV paid all six fine-tuning invoices.",
   "source": "bank_payments",
   "vouched_by": "bank"
  },
  {
   "what": "Quillon Tech and Corvid Labs, named customers on opposite clusters, each share a registered address and a director with Borealis Compute Holding BV.",
   "source": "customer_check",
   "vouched_by": "company register"
  }
 ],
 "coverage": "Reconciled manufacturer shipments with the 2,000 GPUs listed across A and B. Reviewed all 30 days of grid and scheduler records, with escrow confirming all daily copies match. Independently sampled listed A–B links on days 22, 26, and 29. GPU-level participation, unsampled links and days, and the other four fine-tuning customers were unverified.",
 "anomalies_explained": "Inventory and energy balances accounted for the listed capacity and the load increase. Escrow established that the synchronized job entries were recorded contemporaneously. The invoices were fully paid by the same holding company, and register checks established its ties to two named customers. A common booking window could explain the timing, but the recurring cross-cluster traffic during the fine-tuning window and its return to inference levels afterward strongly favor a coordinated run over separate fine-tunes or ordinary batch inference."
}
```
