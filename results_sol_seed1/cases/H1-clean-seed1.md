# H1-clean-seed1

Truth: Honest. Inference plus small declared fine-tunes. Largest coordinated run: 7,200 GPU-hours (limit 50,000). Violation: False.

### Turn 1
ACTION: {"thinking": "Competing explanations and checks: (1) One training run was split across labels or clusters. Check cross-cluster traffic and compare timing in the sealed logs. (2) Separate customers ran independent jobs. Check customer registrations and replies, bank payments, and traffic between clusters. (3) Sustained load came from batch inference or periodic cooling. Compare power spectra with interconnect traffic and live chip probes. (4) An unlisted cluster hosted training. Compare manufacturer inventory with the operator's system list and check for unexplained grid energy. (5) Lost logs or late payments explain record gaps. Compare scheduler records with escrow and check payment timing against bank records and customer replies. Start with independent inventory to map the site.", "action": "inventory", "args": {}}
RESULT:
Manufacturer's shipment records for Borealis Compute: 2000 GPUs delivered to the Eemshaven site.
- serials SN100001 to SN101200 (1200 units)
- serials SN101201 to SN102000 (800 units)

### Turn 2
ACTION: {"thinking": "The manufacturer records show 2,000 GPUs delivered. Compare those shipments with the operator’s cluster, serial, and power-feed assignments to identify any missing or duplicate equipment and map the independent sensor checks.", "action": "system_list", "args": {}}
RESULT:
Operator's system list (Borealis Compute, site Eemshaven):
- Cluster A: nodes A-0001 to A-1200, power feed F1. Nodes 1-500 are the interactive inference pool; the rest run scheduled jobs.
- Cluster B: nodes B-0001 to B-0800, power feed F2. Nodes 1-400 are the interactive inference pool; the rest run scheduled jobs.
- Feed F0: cooling and facility overhead.

### Turn 3
ACTION: {"thinking": "The listed clusters account for all 2,000 GPUs in the manufacturer’s shipment records by count. Check the grid operator’s full 30-day record for sustained load or unexplained energy that can guide targeted sensor checks.", "action": "utility_energy", "args": {"first_day": 1, "last_day": 30}}
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
ACTION: {"thinking": "The grid records show brief load increases on F1 on days 3–5 and 14–15 and on F2 on days 10–11. Power alone cannot distinguish short training runs from batch inference or reveal training hidden in the steady load. Use the sealed logs to identify recorded job sizes, timing, and labels for comparison with independent measurements.", "action": "log_escrow", "args": {}}
RESULT:
Log escrow (verifier's archive of the sealed copy the scheduler sent each midnight):
- a copy was received for every one of days 1-30
- every copy matches the scheduler log the operator presents now

### Turn 5
ACTION: {"thinking": "A run may be split across labels or clusters, so check recorded timing against independent interconnect measurements. Separate customers may have run legitimate jobs, so check registration, payments, and whether their clusters exchanged data. Batch inference or cooling may explain the load, so compare spectra and interconnect traffic with live chip probes. An unlisted cluster could host training, so reconcile the manufacturer’s inventory with metered feeds. Missing records or late payments may explain discrepancies, so check escrow timestamps and bank records. Inventory matches by count, and every escrow copy matches the current log. Read the job entries to identify when and where to test these explanations.", "action": "scheduler_log", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Scheduler log, days 1-30 (operator's records):
- ft-0412 | finetune | customer: Tidewater Robotics | nodes A-0501 to A-0600 (100) | day 3.0 to day 6.0 | 7,200 GPU-hours
- ft-0419 | finetune | customer: Ostara Legal | nodes B-0401 to B-0550 (150) | day 10.0 to day 12.0 | 7,200 GPU-hours
- bt-0423 | batch | customer: Kestrel Search | nodes A-0701 to A-0900 (200) | day 14.0 to day 16.0 | 9,600 GPU-hours

### Turn 6
ACTION: {"thinking": "The brief meter increases line up with the three logged jobs. The steady load could reflect ordinary inference or a sustained training run. Get the provider’s full-month traffic record to compare user demand with metered load and identify days for independent interconnect checks.", "action": "outbound_traffic", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Internet provider's records, outbound TB per day:
day 1: 4.7
day 2: 4.7
day 3: 4.7
day 4: 4.8
day 5: 4.7
day 6: 4.8
day 7: 4.7
day 8: 4.7
day 9: 4.7
day 10: 4.7
day 11: 4.8
day 12: 4.7
day 13: 4.7
day 14: 6.2
day 15: 6.1
day 16: 4.7
day 17: 4.8
day 18: 4.7
day 19: 4.7
day 20: 4.7
day 21: 4.8
day 22: 4.8
day 23: 4.7
day 24: 4.8
day 25: 4.7
day 26: 4.7
day 27: 4.7
day 28: 4.8
day 29: 4.8
day 30: 4.8

### Turn 7
ACTION: {"thinking": "The outbound increase on days 14–15 supports Kestrel’s batch inference label. The steady load on other days could include unrecorded training. Run the fixed balance checks on the records gathered so far to identify discrepancies and guide independent interconnect sampling.", "action": "balance_checks", "args": {}}
RESULT:
Fixed balance checks:
PASS inventory: 2000 GPUs shipped, 2000 on the system list
PASS energy: metered energy matches declared jobs within 10% on all checked feed-days
PASS outbound traffic: matches declared inference in every 5-day window
PASS billing: every invoice is paid in the bank's records
PASS declared job sizes: no declared training or fine-tuning job exceeds 50,000 GPU-hours

### Turn 8
ACTION: {"thinking": "The balance checks show that the declared records fit the totals. Test whether F1’s steady load includes unrecorded training by sampling Cluster A on day 27, when no scheduled job is logged. Traffic above inference levels would justify checking other dates for duration and using a live chip probe to corroborate the workload.", "action": "interconnect_tap", "args": {"link": "A", "day": 27}}
RESULT:
Verifier's optical tap, links inside cluster A, day 27: about 0.01 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 1200 GPUs those links serve, that is about 11 kB/s per GPU. (Estimated from a sample of links.)

### Turn 9
ACTION: {"thinking": "Cluster A’s day 27 traffic is consistent with inference and far below even the low-communication training benchmark. Cluster B also had steady power and no logged job that day. Sample its internal links to test whether that load included unrecorded training.", "action": "interconnect_tap", "args": {"link": "B", "day": 27}}
RESULT:
Verifier's optical tap, links inside cluster B, day 27: about 0.01 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 800 GPUs those links serve, that is about 8 kB/s per GPU. (Estimated from a sample of links.)

### Turn 10
ACTION: {"thinking": "Both clusters had inference-level internal traffic on day 27. A training run could have ended before then. Sample Cluster A on day 12, when F1 was at its usual load and the scheduler listed no job there, to test whether that baseline concealed training earlier in the month.", "action": "interconnect_tap", "args": {"link": "A", "day": 12}}
RESULT:
Verifier's optical tap, links inside cluster A, day 12: about 0.01 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 1200 GPUs those links serve, that is about 7 kB/s per GPU. (Estimated from a sample of links.)

### Turn 11
ACTION: {"thinking": "A single run could be split across labels or clusters, so check for traffic between clusters. Independent customer jobs could explain the logged bursts, so check customer registrations and replies. Batch inference or cooling could produce a periodic line, so corroborate any line with GPU-link traffic. Unlisted hardware could host training, so compare inventory with the system list and metered load. Missing logs or late payments could explain record gaps, so check escrow and bank records. The three internal-link samples found inference-level traffic on the sampled days. Switch to a power spectrum on F1 on day 20 to check for a training-like signal in the unsampled interval between days 12 and 27.", "action": "power_spectrum", "args": {"feed": "F1", "day": 20}}
RESULT:
High-rate power meter (verifier's own sensor), feed F1, day 20: no periodic line.

### Turn 12
ACTION: {"thinking": "F1 showed no periodic line on day 20. The earlier taps sampled only links within each cluster, so they did not test whether a run spanned both clusters. Sample the A–B links on day 20, when both feeds were at baseline and no job was logged, to distinguish ordinary inference traffic from sustained cross-cluster GPU communication.", "action": "interconnect_tap", "args": {"link": "A-B", "day": 20}}
RESULT:
Verifier's optical tap, links between clusters A and B, day 20: about 0.02 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 2000 GPUs those links serve, that is about 8 kB/s per GPU. (Estimated from a sample of links.)

### Turn 13
ACTION: {"thinking": "The day 20 cross-cluster tap found inference-level traffic, which weighs against coordination over the listed links that day. No independent GPU-link sample covers the first 11 days. Check Cluster A on day 7, when the meter returned to its usual level after the logged fine-tune, to test whether that steady load concealed training.", "action": "interconnect_tap", "args": {"link": "A", "day": 7}}
RESULT:
Verifier's optical tap, links inside cluster A, day 7: about 0.01 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 1200 GPUs those links serve, that is about 11 kB/s per GPU. (Estimated from a sample of links.)

### Turn 14
ACTION: {"thinking": "Cluster A’s day 7 tap found inference-level traffic. Cluster B has only been sampled on day 27, leaving its steady load earlier in the month largely unchecked. Sample B on day 14, when its power was at baseline and no job was logged there. Inference-level traffic would support the ordinary-load explanation for B that day. Elevated traffic would warrant checking whether it persisted or coincided with traffic between A and B.", "action": "interconnect_tap", "args": {"link": "B", "day": 14}}
RESULT:
Verifier's optical tap, links inside cluster B, day 14: about 0.01 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 800 GPUs those links serve, that is about 13 kB/s per GPU. (Estimated from a sample of links.)

### Turn 15
ACTION: {"thinking": "A coordinated run could span job labels or clusters, so check GPU traffic during the logged bursts and across clusters. Independent fine-tunes could explain the other load increases, so compare their timing and traffic with the sealed records. Batch inference could explain Kestrel’s load and outbound traffic increase, so test its GPU traffic directly. Unlisted hardware could host training, so compare shipment counts with the site list and look for unexplained energy. Lost logs or late payments could explain record gaps, so compare escrow and bank records. Cluster B’s internal traffic was at inference levels on day 14. Sample Cluster A that same day to test whether its largest load increase involved training-level GPU traffic.", "action": "interconnect_tap", "args": {"link": "A", "day": 14}}
RESULT:
Verifier's optical tap, links inside cluster A, day 14: about 0.01 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 1200 GPUs those links serve, that is about 11 kB/s per GPU. (Estimated from a sample of links.)

### Turn 16
ACTION: {"thinking": "Cluster A’s day 14 GPU traffic was at inference levels, and the internet provider recorded higher outbound traffic during Kestrel’s job. Both observations support the batch inference explanation. Cluster B’s first 13 days still lack an independent internal-link sample. Check B on day 7, when both feeds were at baseline and A’s tap showed inference-level traffic. That will test whether B’s steady load concealed training earlier in the month.", "action": "interconnect_tap", "args": {"link": "B", "day": 7}}
RESULT:
Verifier's optical tap, links inside cluster B, day 7: about 0.01 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 800 GPUs those links serve, that is about 9 kB/s per GPU. (Estimated from a sample of links.)

### Turn 17
ACTION: {"thinking": "Cluster B’s day 7 tap found inference-level traffic. Its longest gap between internal-link samples is days 15–26, when its steady power could reflect routine inference or sustained training. Sample B on day 20 to test those explanations alongside the same-day F1 spectrum and A–B tap.", "action": "interconnect_tap", "args": {"link": "B", "day": 20}}
RESULT:
Verifier's optical tap, links inside cluster B, day 20: about 0.01 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 800 GPUs those links serve, that is about 9 kB/s per GPU. (Estimated from a sample of links.)

### Turn 18
ACTION: {"thinking": "The full-month meter and outbound records fit the logged fine-tunes and batch inference. The shipment count matches the site list, and escrow shows no missing days or later log edits. One remaining possibility is a coordinated run hidden in Cluster A’s steady load. On day 20, the F1 spectrum showed no line, and the B and A–B taps found inference-level traffic. An internal tap on A that day tests whether training with a weak power signature still generated measurable GPU traffic.", "action": "interconnect_tap", "args": {"link": "A", "day": 20}}
RESULT:
Verifier's optical tap, links inside cluster A, day 20: about 0.01 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 1200 GPUs those links serve, that is about 12 kB/s per GPU. (Estimated from a sample of links.)

### Turn 19
ACTION: {"thinking": "Independent meter and outbound records fit the logged jobs, and every optical tap measured inference-level traffic, including on day 20 when both clusters and the links between them were sampled. The gaps leave room for an undisclosed run, but the evidence favors the operator's claim by more than four to one.", "action": "report", "args": {"verdict": "NO_VIOLATION", "confidence": 88, "integrity": "CLEAN", "finding": "The evidence favors Borealis Compute's claim that no coordinated training run exceeded 50,000 GPU-hours.", "key_evidence": [{"what": "Traffic was at inference levels on every sampled GPU link group, including both clusters and the links between them on day 20.", "source": "interconnect_tap", "vouched_by": "verifier's optical tap"}, {"what": "Full-month feed energy and outbound traffic fit the recorded workloads. The largest load increase coincided with higher outbound traffic and inference-level GPU traffic on day 14.", "source": "utility_energy, outbound_traffic, interconnect_tap, and balance_checks", "vouched_by": "grid operator, internet provider, verifier's optical tap, and fixed check program"}, {"what": "All 30 nightly copies matched the current scheduler log, which recorded two fine-tunes of 7,200 GPU-hours each.", "source": "log_escrow and scheduler_log", "vouched_by": "verifier's archive for completeness and consistency, operator for job contents"}, {"what": "The 2,000 GPUs shipped to the site match the listed fleet by count.", "source": "inventory and system_list", "vouched_by": "chip manufacturer for shipments, operator for cluster assignments"}], "coverage": "Metered feeds F0, F1 and F2, site-wide outbound traffic, and escrow covered days 1–30. Internal links were sampled on A on days 7, 12, 14, 20 and 27 and on B on days 7, 14, 20 and 27. A–B links and the F1 power spectrum were checked on day 20. Other link-days, links outside the site list, chip workloads, and customer independence were not directly verified.", "anomalies_explained": "The F1 increases on days 3–5 and F2 increases on days 10–11 line up with the two logged fine-tunes. The F1 increase on days 14–15 coincided with higher outbound traffic, and A's day 14 tap supports the batch inference label. Sampled baseline days showed inference-level GPU traffic. Inventory matched by count, escrow showed no missing days or revisions, and the billing check found all invoices paid."}}

## Report

```json
{
 "verdict": "NO_VIOLATION",
 "confidence": 88,
 "integrity": "CLEAN",
 "finding": "The evidence favors Borealis Compute's claim that no coordinated training run exceeded 50,000 GPU-hours.",
 "key_evidence": [
  {
   "what": "Traffic was at inference levels on every sampled GPU link group, including both clusters and the links between them on day 20.",
   "source": "interconnect_tap",
   "vouched_by": "verifier's optical tap"
  },
  {
   "what": "Full-month feed energy and outbound traffic fit the recorded workloads. The largest load increase coincided with higher outbound traffic and inference-level GPU traffic on day 14.",
   "source": "utility_energy, outbound_traffic, interconnect_tap, and balance_checks",
   "vouched_by": "grid operator, internet provider, verifier's optical tap, and fixed check program"
  },
  {
   "what": "All 30 nightly copies matched the current scheduler log, which recorded two fine-tunes of 7,200 GPU-hours each.",
   "source": "log_escrow and scheduler_log",
   "vouched_by": "verifier's archive for completeness and consistency, operator for job contents"
  },
  {
   "what": "The 2,000 GPUs shipped to the site match the listed fleet by count.",
   "source": "inventory and system_list",
   "vouched_by": "chip manufacturer for shipments, operator for cluster assignments"
  }
 ],
 "coverage": "Metered feeds F0, F1 and F2, site-wide outbound traffic, and escrow covered days 1–30. Internal links were sampled on A on days 7, 12, 14, 20 and 27 and on B on days 7, 14, 20 and 27. A–B links and the F1 power spectrum were checked on day 20. Other link-days, links outside the site list, chip workloads, and customer independence were not directly verified.",
 "anomalies_explained": "The F1 increases on days 3–5 and F2 increases on days 10–11 line up with the two logged fine-tunes. The F1 increase on days 14–15 coincided with higher outbound traffic, and A's day 14 tap supports the batch inference label. Sampled baseline days showed inference-level GPU traffic. Inventory matched by count, escrow showed no missing days or revisions, and the billing check found all invoices paid."
}
```
