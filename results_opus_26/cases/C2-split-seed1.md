# C2-split-seed1

Truth: Cheating. One run declared as six fine-tunes for six shell customers, all paid from the operator's parent. Largest coordinated run: 166,100 GPU-hours (limit 50,000). Violation: True.

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
ACTION: {"thinking": "Grid-vouched energy shows a large step on days 23-28, with day 29 partial. F1 rises by about 11 MWh/day (about 458 kW). At roughly 0.65 kW extra per GPU going from idle to training, that is about 700 GPUs, which is all of cluster A's scheduled pool. F2 rises by about 6.2 MWh/day (about 258 kW), roughly 400 GPUs, all of B's scheduled pool. Facility overhead on F0 roughly doubles too, which fits real heat load. Days 1-22 and 30 are flat at baseline. If the step is one coordinated run on A's pool alone, it comes to about 700 x 24 x 6.4 = 107,000 GPU-hours. If it spans A and B, it comes to about 170,000. Either is far above 50,000. If it is several separate customers' jobs, or batch inference, it could be honest. The key questions are whether this load is training, and whether it is one coordinated process across the pools or clusters. Days 26-28 fall inside the live window, so I can use my own instruments directly. First I'll tap the A-B link on day 26. About 1 GB/s per GPU (or about 10 MB/s per GPU for low-communication training) crossing clusters would show one run spanning both. About 10 kB/s would point to separate or inference workloads.", "action": "interconnect_tap", "args": {"link": "A-B", "day": 26}}
RESULT:
Verifier's optical tap, links between clusters A and B, day 26: about 228 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 2000 GPUs those links serve, that is about 114 MB/s per GPU. (Estimated from a sample of links.)

### Turn 5
ACTION: {"thinking": "The A-B tap shows about 228 GB/s on day 26. That is about 114 MB/s per GPU over all 2000, or about 207 MB/s per GPU if only the 1100 scheduled-pool GPUs carry it (within ±30%). That is far above the inference level (about 10 kB/s per GPU) and above the low-communication training level (about 10 MB/s). It points to heavy GPU-to-GPU coupling across the two clusters during the step, which is evidence for one coordinated job spanning A and B (H3), not separate customers' jobs. It is not yet proof of training: it could in principle be an unusual distributed batch inference or data movement. Next I'll classify the workload with my own live chip probe on day 27 (hour 640), on one node from A's scheduled pool and one from B's. Later checks: a day-30 A-B tap for baseline cross traffic, a power_spectrum line on F1/F2, and outbound traffic to rule out user-facing inference.", "action": "chip_probe", "args": {"nodes": ["A-0700", "B-0600"], "hour": 640}}
RESULT:
Cable current probe at hour 640 (day 27.7). Each reading is a guess:
- A-0700: reads as training
- B-0600: reads as training

### Turn 6
ACTION: {"thinking": "Own probe reads both A-0700 and B-0600 as training at hour 640, which fits the step load. Each reading is about 97% accurate, and they agree. Combined with heavy A-B coupling (about 114-207 MB/s per GPU) and flat grid-metered load on days 23-28, this points to one training run spanning both scheduled pools, roughly 107k-170k GPU-hours. Before testing alternatives I need to see how the operator recorded this load. The sealed escrow copy shows what was logged each day, and it cannot be edited afterwards. If it lists several small jobs or customers, that supports H3 (split run), and I would then check customers and payments. If it lists one big job, the claim is simply false. Later checks: a power_spectrum line on F1/F2 and outbound_traffic, to rule out user-facing inference.", "action": "log_escrow", "args": {}}
RESULT:
Log escrow (verifier's archive of the sealed copy the scheduler sent each midnight):
- a copy was received for every one of days 1-30
- every copy matches the scheduler log the operator presents now

### Turn 7
ACTION: {"thinking": "The escrow received a copy for every day and every copy matches the current scheduler log, so there were no retroactive edits (H6 weakened). The log is still the operator's own record, though, so it shows what was written down, not whether it was true. Next I read the scheduler log for days 22-30 to see how the step load on days 23-29 was recorded: one job, several jobs or customers (H3), or batch inference (H5). That tells me which customers and payments to check against the company register and the bank.", "action": "scheduler_log", "args": {"first_day": 22, "last_day": 30}}
RESULT:
Scheduler log, days 22-30 (operator's records):
- ft-0561 | finetune | customer: Corvid Labs | nodes A-0501 to A-0675 (175) | day 23.0 to day 29.3 | 26,425 GPU-hours
- ft-0562 | finetune | customer: Pallas Systems | nodes A-0676 to A-0850 (175) | day 23.0 to day 29.3 | 26,425 GPU-hours
- ft-0563 | finetune | customer: Brightwater AI | nodes A-0851 to A-1025 (175) | day 23.0 to day 29.3 | 26,425 GPU-hours
- ft-0564 | finetune | customer: Fennec Data | nodes A-1026 to A-1200 (175) | day 23.0 to day 29.3 | 26,425 GPU-hours
- ft-0565 | finetune | customer: Quillon Tech | nodes B-0401 to B-0600 (200) | day 23.0 to day 29.3 | 30,200 GPU-hours
- ft-0566 | finetune | customer: Marram Software | nodes B-0601 to B-0800 (200) | day 23.0 to day 29.3 | 30,200 GPU-hours

### Turn 8
ACTION: {"thinking": "The escrow-matched log splits the step load into six fine-tune jobs under six different customer names. Each job is under 50,000 GPU-hours (26,425 or 30,200), but together they total about 165,500 GPU-hours. They all start and stop at the same times (day 23.0 to 29.3) and fill exactly the scheduled pools of A and B. My own tap shows heavy cross-cluster traffic (about 114-207 MB/s per GPU on A-B). Separate customers' independent fine-tunes would not exchange that much data across clusters. This fits H3, one run split under several labels, but six genuinely separate fine-tunes is the innocent alternative. To tell them apart I'll check who paid. Bank records are hard for the operator to fake: one payer behind several of these customers, or payments looping back to Borealis, would point to a single coordinated run. After that I'll check the company register for a sample of customers, and if needed tap intra-cluster links or check outbound traffic.", "action": "bank_payments", "args": {}}
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
ACTION: {"thinking": "The bank's records show that all six fine-tune 'customers' (Corvid, Pallas, Brightwater, Fennec, Quillon, Marram) were paid for by Borealis Compute Holding BV, the operator's own holding company. The three genuine customers (Kestrel, Lumen, Northwind) paid for themselves. The six jobs therefore have one shared payer that is the operator itself. Every other source agrees on a single coordinated training run:\n- **Grid meter:** a simultaneous step of about 1,100 GPUs at training power on days 23 to 29.3.\n- **Own optical tap:** heavy A-B traffic of about 114 to 207 MB/s per GPU. That is far above inference (about 10 kB/s) and above low-communication training (about 10 MB/s), so the jobs in the two clusters were coupled.\n- **Own chip probe:** read training on both clusters.\n- **Scheduler log:** six jobs with identical start and end times that exactly fill both scheduled pools.\nThe innocent explanation, six independent fine-tunes for real customers, conflicts with both the cross-cluster coupling and the operator-funded payments. Escrow shows the log was not edited afterwards. The split was written into the records from the start. The total is about 165,500 GPU-hours (log) or about 166,000 (energy), more than three times the threshold. The evidence comes from the grid, the bank and my own instruments, none of which the operator controls. A register check would add little, so I am closing with 10 points spent.", "action": "report", "args": {"verdict": "VIOLATION", "confidence": 93, "integrity": "COMPROMISED", "finding": "On days 23-29.3 one coordinated fine-tuning run used about 165,000 GPU-hours on all 1,100 scheduled GPUs across clusters A and B. It was split into six jobs under customer names that the operator's own holding paid for.", "key_evidence": [{"what": "Simultaneous load step on F1 (+~458 kW) and F2 (+~258 kW) for days 23-28, partial on day 29, matching about 1,100 GPUs at training power", "source": "utility_energy", "vouched_by": "grid operator"}, {"what": "About 228 GB/s between clusters A and B on day 26 (about 114-207 MB/s per GPU), training-level coupling that spans both clusters", "source": "interconnect_tap", "vouched_by": "verifier's own optical tap"}, {"what": "A-0700 and B-0600 both read as training at hour 640", "source": "chip_probe", "vouched_by": "verifier's own probe"}, {"what": "All six step-period 'customers' were paid for by Borealis Compute Holding BV; genuine customers paid for themselves", "source": "bank_payments", "vouched_by": "bank"}, {"what": "Six fine-tunes with identical days 23.0-29.3 timing that fill A-0501..1200 and B-0401..0800 and total 165,500 GPU-hours; matches the sealed daily copies", "source": "scheduler_log + log_escrow", "vouched_by": "operator (content), verifier's archive (unedited since each midnight)"}], "coverage": "Hardware fully mapped: inventory (2,000 GPUs) matches the system list. Energy checked for all feeds, days 1-30. Escrow covered all 30 days. Scheduler log read for days 22-30. Tap and probe were live on days 26-27 only. Days 1-22 and 30 are at flat baseline energy, so no large run is plausible there, though they were not probed directly. Not used: power_spectrum, outbound_traffic, switch_counters, customer_check, balance_checks.", "anomalies_explained": "1. Energy step on days 23-29: explained by one training run, confirmed by the probe and tap. 2. Six separate customers whose jobs exchange heavy cross-cluster traffic: they are one coupled process, not independent jobs. 3. Six customers paid for by the operator's holding company: shell or captive labels used to keep each piece under 50,000 GPU-hours. 4. Escrow matches the log: there were no retroactive edits, and the split was recorded that way from the start."}}

## Report

```json
{
 "verdict": "VIOLATION",
 "confidence": 93,
 "integrity": "COMPROMISED",
 "finding": "On days 23-29.3 one coordinated fine-tuning run used about 165,000 GPU-hours on all 1,100 scheduled GPUs across clusters A and B. It was split into six jobs under customer names that the operator's own holding paid for.",
 "key_evidence": [
  {
   "what": "Simultaneous load step on F1 (+~458 kW) and F2 (+~258 kW) for days 23-28, partial on day 29, matching about 1,100 GPUs at training power",
   "source": "utility_energy",
   "vouched_by": "grid operator"
  },
  {
   "what": "About 228 GB/s between clusters A and B on day 26 (about 114-207 MB/s per GPU), training-level coupling that spans both clusters",
   "source": "interconnect_tap",
   "vouched_by": "verifier's own optical tap"
  },
  {
   "what": "A-0700 and B-0600 both read as training at hour 640",
   "source": "chip_probe",
   "vouched_by": "verifier's own probe"
  },
  {
   "what": "All six step-period 'customers' were paid for by Borealis Compute Holding BV; genuine customers paid for themselves",
   "source": "bank_payments",
   "vouched_by": "bank"
  },
  {
   "what": "Six fine-tunes with identical days 23.0-29.3 timing that fill A-0501..1200 and B-0401..0800 and total 165,500 GPU-hours; matches the sealed daily copies",
   "source": "scheduler_log + log_escrow",
   "vouched_by": "operator (content), verifier's archive (unedited since each midnight)"
  }
 ],
 "coverage": "Hardware fully mapped: inventory (2,000 GPUs) matches the system list. Energy checked for all feeds, days 1-30. Escrow covered all 30 days. Scheduler log read for days 22-30. Tap and probe were live on days 26-27 only. Days 1-22 and 30 are at flat baseline energy, so no large run is plausible there, though they were not probed directly. Not used: power_spectrum, outbound_traffic, switch_counters, customer_check, balance_checks.",
 "anomalies_explained": "1. Energy step on days 23-29: explained by one training run, confirmed by the probe and tap. 2. Six separate customers whose jobs exchange heavy cross-cluster traffic: they are one coupled process, not independent jobs. 3. Six customers paid for by the operator's holding company: shell or captive labels used to keep each piece under 50,000 GPU-hours. 4. Escrow matches the log: there were no retroactive edits, and the split was recorded that way from the start."
}
```
