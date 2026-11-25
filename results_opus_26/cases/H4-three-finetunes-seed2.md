# H4-three-finetunes-seed2

Truth: Honest. Three separate customers fine-tune, each under the limit; together they exceed it. Largest coordinated run: 25,200 GPU-hours (limit 50,000). Violation: False.

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
2 | 2.7 | 8.0 | 5.8
3 | 2.7 | 7.9 | 5.8
4 | 2.7 | 8.0 | 5.8
5 | 3.8 | 13.2 | 5.8
6 | 3.8 | 13.2 | 5.8
7 | 3.8 | 13.2 | 5.8
8 | 2.7 | 8.0 | 5.8
9 | 3.7 | 12.6 | 5.8
10 | 3.6 | 12.4 | 5.7
11 | 3.7 | 12.4 | 5.8
12 | 3.2 | 10.2 | 5.7
13 | 2.8 | 7.9 | 5.8
14 | 2.7 | 7.9 | 5.8
15 | 2.8 | 8.0 | 5.7
16 | 2.8 | 8.0 | 5.8
17 | 2.8 | 8.0 | 5.8
18 | 4.0 | 8.0 | 11.8
19 | 4.0 | 7.9 | 11.9
20 | 3.5 | 7.9 | 9.4
21 | 2.8 | 7.9 | 5.8
22 | 2.7 | 8.0 | 5.7
23 | 2.7 | 7.9 | 5.8
24 | 2.8 | 8.0 | 5.7
25 | 2.7 | 8.0 | 5.8
26 | 2.7 | 8.0 | 5.8
27 | 2.7 | 7.9 | 5.8
28 | 2.7 | 8.0 | 5.8
29 | 2.8 | 7.9 | 5.8
30 | 2.7 | 8.0 | 5.8

### Turn 4
ACTION: {"thinking": "Grid energy, a third-party source, shows three high-power episodes above baseline (F1 about 8.0 MWh/day, F2 about 5.8 MWh/day). Each GPU moving from idle to training adds about 0.65 kW. (1) F1, days 5-7: about +5.2 MWh/day, roughly 330 GPUs, about 24,000 GPU-hours. Day 8 drops back to baseline. (2) F1, days 9-12: about +4.5 MWh/day on days 9-11 and +2.2 on day 12, roughly 290 GPUs, about 24,000 GPU-hours. (3) F2, days 18-20: +6.0, +6.1 and +3.6 MWh, roughly 385 GPUs, about 24,000 GPU-hours. Each episode alone is below 50,000 GPU-hours. Episodes 1 and 2 together come to about 48,000, near the line, and all three together to about 72,000. F0 cooling rises in step with each, so the extra load is real and on-site. Days 21-30 are at baseline, so the live probe window will only show the steady state. Possible readings: (H1) three separate honest jobs, for example different customers or batch inference. (H2) one run paused on day 8 and then moved to cluster B, which is a split, migrated run. (H4) batch inference rather than training. The key question is whether these episodes are one coordinated run. Next is the log escrow, my own sealed archive and cheap. It shows what the operator recorded on each day for these episodes (job IDs, customers, node counts), and I can later compare it with the current scheduler_log for edits.", "action": "log_escrow", "args": {}}
RESULT:
Log escrow (verifier's archive of the sealed copy the scheduler sent each midnight):
- a copy was received for every one of days 1-30
- every copy matches the scheduler log the operator presents now

### Turn 5
ACTION: {"thinking": "The escrow copies match the current scheduler log, so the records were not edited after the fact (H5 out), though what was recorded on the day could still have been false. Now I can read the scheduler log for days 1-30 and see how the operator explains the three grid-energy episodes (F1 days 5-7, F1 days 9-12, F2 days 18-20): job IDs, customers, node counts and job types. The question is whether they appear as separate customers or as batch inference. That decides which customers to check against the register and whether to use the tap and power spectrum on the episode days. Budget after this: 25.", "action": "scheduler_log", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Scheduler log, days 1-30 (operator's records):
- ft-0440 | finetune | customer: Tidewater Robotics | nodes A-0501 to A-0850 (350) | day 5.0 to day 8.0 | 25,200 GPU-hours
- ft-0447 | finetune | customer: Ostara Legal | nodes A-0851 to A-1150 (300) | day 9.0 to day 12.5 | 25,200 GPU-hours
- ft-0452 | finetune | customer: Halcyon Bio | nodes B-0401 to B-0800 (400) | day 18.0 to day 20.6 | 24,800 GPU-hours

### Turn 6
ACTION: {"thinking": "The scheduler log names three fine-tune jobs with three different customers. ft-0440 (Tidewater Robotics) used 350 A nodes on days 5-8, ft-0447 (Ostara Legal) used 300 A nodes on days 9-12.5, and ft-0452 (Halcyon Bio) used 400 B nodes on days 18-20.6. Each is about 25,000 GPU-hours, and together they come to about 75,200. This matches the grid-energy episodes, so the logged sizes are honest about the power drawn. Each job alone is under the threshold. The open question is whether these are three separate customers (H1) or one run split across shell customers and moved between clusters (H2). Signs of a split are the near-identical sizes (25,200, 25,200 and 24,800), each half the threshold, and the sequential handoffs. Payments are the next check: the bank records are third-party and cost 1 point. If one payer funds all three jobs, or the payments come from linked accounts, that points to H2. If three independent payers each pay for their own job, that supports H1. After that I'll check the customers against the company register and compare power-spectrum lines across days 6, 10 and 19.", "action": "bank_payments", "args": {}}
RESULT:
Invoices (operator) against payments received (bank's records):
customer | invoiced EUR | paid EUR | paying account holder
Halcyon Bio | 49,600 | 49,600 | Halcyon Bio
Kestrel Search | 150,000 | 150,000 | Kestrel Search
Lumen Health | 150,000 | 150,000 | Lumen Health
Northwind Apps | 150,000 | 150,000 | Northwind Apps
Ostara Legal | 50,400 | 50,400 | Ostara Legal
Tidewater Robotics | 50,400 | 50,400 | Tidewater Robotics

### Turn 7
ACTION: {"thinking": "Each of the three fine-tune customers paid its own invoice from an account in its own name. That is consistent with three independent customers (H1), but shell companies could do the same. The invoices also price all three jobs consistently at 2 EUR/GPU-hour. Next I'll check the company register, which is harder to arrange than operator records, starting with Tidewater Robotics. I'm looking for links between the three customers or to Borealis: shared directors or addresses, recent incorporation, or Borealis ownership. Then I'll check Ostara Legal and Halcyon Bio, and compare power-spectrum lines across days 6, 10 and 19. Budget after this: 22.", "action": "customer_check", "args": {"customer": "Tidewater Robotics"}}
RESULT:
Customer check, Tidewater Robotics:
- Company register: registered 15 years ago at its own address, 351 employees reported.
- The customer's reply: "We ordered: fine-tuning on 350 GPUs, day 5.0 to day 8.0."

### Turn 8
ACTION: {"thinking": "Tidewater Robotics looks genuine. The register shows it was founded 15 years ago, has its own address and 351 employees, and its reply matches the log (350 GPUs, days 5.0-8.0). That makes ft-0440 an independent customer's job, about 25,200 GPU-hours, under the threshold. The split-run concern (H2) now rests on ft-0447 (Ostara Legal) and ft-0452 (Halcyon Bio). A run that continued from ft-0440 would need a controlled or shell customer to carry it on. Ostara's job started a day after Tidewater's ended and is the same size, so I'll check Ostara Legal against the company register next, looking for recent incorporation, a shared address, or links to Borealis or the other customers. After that I'll check Halcyon Bio. Then I'll compare power-spectrum lines on days 6, 10 and 19 to see whether the periodic signature carries across the episodes. Budget after this: 20.", "action": "customer_check", "args": {"customer": "Ostara Legal"}}
RESULT:
Customer check, Ostara Legal:
- Company register: registered 15 years ago at its own address, 113 employees reported.
- The customer's reply: none within the audit window.

### Turn 9
ACTION: {"thinking": "Ostara Legal's register entry looks genuine: registered 15 years ago at its own address with 113 employees. It did not reply, but real customers often don't reply in time, so that alone is not suspicious. It paid its own invoice from an account in its own name. ft-0447 therefore looks like an independent customer's job, though without the customer's own confirmation. To test the split-run hypothesis (H2), I'll check the last customer, Halcyon Bio, against the company register. Its job ran on cluster B, and all three jobs are close to half the threshold, so a shell or Borealis-linked company here would be a strong lead. After that I'll use power_spectrum to compare the periodic line on days 6, 10 and 19, and interconnect_tap where it helps, to see whether one run's signature carries across the episodes. Budget after this: 18.", "action": "customer_check", "args": {"customer": "Halcyon Bio"}}
RESULT:
Customer check, Halcyon Bio:
- Company register: registered 3 years ago at its own address, 205 employees reported.
- The customer's reply: "We ordered: fine-tuning on 400 GPUs, day 18.0 to day 20.6."

### Turn 10
ACTION: {"thinking": "All three customers look genuine and independent. Each is registered at its own address with its own staff (15, 15 and 3 years old), and each paid its own invoice from an account in its own name. Tidewater and Halcyon confirmed their jobs, and Ostara did not reply in time. Separate customers' runs do not add up, so the split-run concern (H2) is weakening. Each logged job is about 25,000 GPU-hours, and the grid energy confirms those sizes. The remaining risk is a run hidden in the flat baseline, such as training labelled as interactive inference (H4). Baseline is about 333 kW on F1 and about 242 kW on F2. That fits idle scheduled nodes plus interactive pools averaging about 0.45 kW per GPU, but steady baseline power cannot exclude a few hundred GPUs training all month. Cheap step first: balance_checks to compare energy, logs, traffic and payments. Then I'll check outbound traffic, a power-spectrum line on a baseline day, and chip probes in the live window. Budget after this: 17.", "action": "balance_checks", "args": {}}
RESULT:
Fixed balance checks:
PASS inventory: 2000 GPUs shipped, 2000 on the system list
PASS energy: metered energy matches declared jobs within 10% on all checked feed-days
PASS outbound traffic: matches declared inference in every 5-day window
PASS billing: every invoice is paid in the bank's records
PASS declared job sizes: no declared training or fine-tuning job exceeds 50,000 GPU-hours

### Turn 11
ACTION: {"thinking": "My previous reply was cut off by a safety classifier, so I'm continuing the audit without repeating it. Status: the balance checks all pass, but a pass is not proof. The three logged fine-tunes match grid energy and belong to genuine, independent, self-paying customers, so a split run (H2) is unlikely. The remaining risk is training hidden in the flat baseline, for example in the interactive pools or on idle scheduled nodes, labelled as inference (H3/H4). Baseline F1 is about 333 kW over 1200 GPUs, which leaves room for a hidden run of 100+ GPUs running all month, and that would exceed 50,000 GPU-hours. My own power sensor is the best way to test this. I'll check F1 on a day with no declared jobs; a periodic line there would be a lead. Budget after this: 15.", "action": "power_spectrum", "args": {"feed": "F1", "day": 15}}
RESULT:
High-rate power meter (verifier's own sensor), feed F1, day 15: no periodic line.

### Turn 12
ACTION: {"thinking": "No periodic line on F1 on day 15, a day with no declared job. That weakens the idea of a training run hidden in cluster A's flat baseline. A month-long hidden run would leave a line on about 96% of active days. Two places remain unchecked for hidden training: the F2 baseline, and the live state of nodes the operator labels as inference or idle. In the live window, my own chip probe can read workload type directly. I'll probe one interactive-pool node and one scheduled node in each cluster at hour 610. Budget after this: 13.", "action": "chip_probe", "args": {"nodes": ["A-0100", "A-0700", "B-0200", "B-0600"], "hour": 610}}
RESULT:
Cable current probe at hour 610 (day 26.4). Each reading is a guess:
- A-0100: reads as inference
- A-0700: idle
- B-0200: reads as inference
- B-0600: idle

### Turn 13
ACTION: {"thinking": "The live probes match the operator's labels: interactive-pool nodes A-0100 and B-0200 read as inference, and scheduled nodes A-0700 and B-0600 are idle. That is consistent with days 21-30 sitting at baseline power, and it gives no sign of training hidden under an inference label right now. The F1 baseline already showed no periodic line on day 15. Cluster B's baseline has not been checked with my own sensor, so a month-long hidden run on F2 is still possible in principle. F2 on day 15 has no declared job, so a line there would be a lead and its absence would close most of that gap. Budget after this: 11.", "action": "power_spectrum", "args": {"feed": "F2", "day": 15}}
RESULT:
High-rate power meter (verifier's own sensor), feed F2, day 15: no periodic line.

### Turn 14
ACTION: {"thinking": "Close the case: each hypothesis has been tested against sources the operator does not control, and the evidence clearly favours an honest operator. H5 (rewritten logs): ruled out, because the escrow copies match the current log on every day. H3 (hidden GPUs): ruled out, because the manufacturer shipped 2000 GPUs and 2000 are listed. H2 (one run split across customers): unlikely. The three high-power episodes in the grid data match the three logged fine-tunes (about 25,000 GPU-hours each). They belong to three independent customers: all are in the company register with their own address and staff, and each paid its own invoice from its own account. Two confirmed their orders; Ostara did not reply in time, which is normal. Separate customers' runs do not add up. H4/H6 (training hidden in the baseline or labelled as inference): unlikely. Baseline energy fits the interactive pools plus idle nodes almost exactly (F1 about 330 kW, F2 about 240 kW), leaving no room for a sizeable run all month. My own sensor found no periodic line on F1 or F2 on day 15. Live probes match the operator's labels. Outbound traffic matches declared inference. NO_VIOLATION is well over four times as likely as VIOLATION.", "action": "report", "args": {"verdict": "NO_VIOLATION", "confidence": 85, "integrity": "CLEAN", "finding": "The three training episodes (about 25,000 GPU-hours each) are fine-tunes by three independent, genuine customers; no evidence of a hidden or split run above 50,000 GPU-hours.", "key_evidence": [{"what": "2000 GPUs shipped, matching the 2000 nodes on the system list", "source": "inventory", "vouched_by": "chip manufacturer"}, {"what": "Only three above-baseline episodes (F1 days 5-7, F1 days 9-12, F2 days 18-20), each about 24,000-25,000 GPU-hours; baseline fits inference pools plus idle nodes", "source": "utility_energy", "vouched_by": "grid operator"}, {"what": "Scheduler log unedited since each day's midnight copy", "source": "log_escrow", "vouched_by": "verifier's archive"}, {"what": "Tidewater, Ostara and Halcyon are established companies at separate addresses (113-351 staff); Tidewater and Halcyon confirmed their jobs", "source": "customer_check", "vouched_by": "company register / customers"}, {"what": "Each fine-tune customer paid its own invoice from an account in its own name", "source": "bank_payments", "vouched_by": "bank"}, {"what": "No periodic line on F1 or F2 on day 15, a day with no declared job", "source": "power_spectrum", "vouched_by": "verifier's own sensor"}, {"what": "Live probes at hour 610 match the operator's labels (inference pools read as inference, scheduled nodes idle)", "source": "chip_probe", "vouched_by": "verifier's own probe"}], "coverage": "Grid energy, logs, escrow and payments cover all 30 days and both clusters. My own power sensor checked F1 and F2 on day 15 only. The chip probe covered 4 nodes at hour 610. The interconnect tap and outbound traffic were not checked directly; outbound traffic was covered only through the balance check. Episode-day power lines were not sampled.", "anomalies_explained": "Three near-equal jobs (about half the threshold each) running back to back looked like a possible split run. The register and bank records show three independent customers, each paying for its own job, so their runs do not add up. Ostara Legal did not reply, which is a normal delay; its register entry and payment are genuine. Baseline power fully accounts for the interactive pools and idle nodes, and no line or probe reading suggests hidden training."}}

## Report

```json
{
 "verdict": "NO_VIOLATION",
 "confidence": 85,
 "integrity": "CLEAN",
 "finding": "The three training episodes (about 25,000 GPU-hours each) are fine-tunes by three independent, genuine customers; no evidence of a hidden or split run above 50,000 GPU-hours.",
 "key_evidence": [
  {
   "what": "2000 GPUs shipped, matching the 2000 nodes on the system list",
   "source": "inventory",
   "vouched_by": "chip manufacturer"
  },
  {
   "what": "Only three above-baseline episodes (F1 days 5-7, F1 days 9-12, F2 days 18-20), each about 24,000-25,000 GPU-hours; baseline fits inference pools plus idle nodes",
   "source": "utility_energy",
   "vouched_by": "grid operator"
  },
  {
   "what": "Scheduler log unedited since each day's midnight copy",
   "source": "log_escrow",
   "vouched_by": "verifier's archive"
  },
  {
   "what": "Tidewater, Ostara and Halcyon are established companies at separate addresses (113-351 staff); Tidewater and Halcyon confirmed their jobs",
   "source": "customer_check",
   "vouched_by": "company register / customers"
  },
  {
   "what": "Each fine-tune customer paid its own invoice from an account in its own name",
   "source": "bank_payments",
   "vouched_by": "bank"
  },
  {
   "what": "No periodic line on F1 or F2 on day 15, a day with no declared job",
   "source": "power_spectrum",
   "vouched_by": "verifier's own sensor"
  },
  {
   "what": "Live probes at hour 610 match the operator's labels (inference pools read as inference, scheduled nodes idle)",
   "source": "chip_probe",
   "vouched_by": "verifier's own probe"
  }
 ],
 "coverage": "Grid energy, logs, escrow and payments cover all 30 days and both clusters. My own power sensor checked F1 and F2 on day 15 only. The chip probe covered 4 nodes at hour 610. The interconnect tap and outbound traffic were not checked directly; outbound traffic was covered only through the balance check. Episode-day power lines were not sampled.",
 "anomalies_explained": "Three near-equal jobs (about half the threshold each) running back to back looked like a possible split run. The register and bank records show three independent customers, each paying for its own job, so their runs do not add up. Ostara Legal did not reply, which is a normal delay; its register entry and payment are genuine. Baseline power fully accounts for the interactive pools and idle nodes, and no line or probe reading suggests hidden training."
}
```
