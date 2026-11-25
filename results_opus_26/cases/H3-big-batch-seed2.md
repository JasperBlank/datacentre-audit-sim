# H3-big-batch-seed2

Truth: Honest. A large batch inference job with flat power, results delivered in one transfer at the end. Largest coordinated run: 7,200 GPU-hours (limit 50,000). Violation: False.

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
1 | 2.8 | 8.0 | 5.8
2 | 2.8 | 7.9 | 5.8
3 | 2.7 | 7.9 | 5.8
4 | 2.7 | 8.0 | 5.8
5 | 2.7 | 8.0 | 5.7
6 | 2.8 | 8.0 | 5.8
7 | 2.8 | 7.9 | 5.8
8 | 3.2 | 7.9 | 8.1
9 | 3.2 | 8.0 | 8.1
10 | 2.7 | 7.9 | 5.8
11 | 2.7 | 8.0 | 5.8
12 | 4.8 | 18.0 | 5.8
13 | 4.8 | 18.0 | 5.8
14 | 4.8 | 18.2 | 5.8
15 | 4.8 | 18.2 | 5.8
16 | 4.7 | 17.9 | 5.8
17 | 4.8 | 18.1 | 5.8
18 | 4.8 | 18.1 | 5.7
19 | 4.8 | 18.0 | 5.7
20 | 2.7 | 7.9 | 5.8
21 | 2.8 | 7.9 | 5.8
22 | 2.8 | 8.0 | 5.8
23 | 2.7 | 7.9 | 5.7
24 | 2.7 | 7.9 | 5.7
25 | 2.7 | 8.0 | 5.8
26 | 2.7 | 8.0 | 5.8
27 | 2.7 | 7.9 | 5.7
28 | 2.7 | 8.0 | 5.8
29 | 2.7 | 8.0 | 5.8
30 | 2.7 | 7.9 | 5.8

### Turn 4
ACTION: {"thinking": "The utility data, vouched for by the grid operator, shows one large event and one small one. (1) F1, cluster A, days 12-19: daily energy rises from about 8.0 to about 18.0 MWh, roughly +10 MWh/day, which is about 417 kW extra. Going from idle (0.15 kW) to training (0.8 kW) adds about 0.65 kW per GPU, so this is roughly 640 GPUs, close to A's 700 scheduled nodes. The load lasts 8 days (about 192 h), giving roughly 120,000 GPU-hours if it was one run. That would be well over 50,000. F0 cooling rises at the same time, which is consistent with a real thermal load. (2) F2, cluster B, days 8-9: +2.3 MWh/day, about 96 kW, so roughly 150 GPUs for 48 h, about 7,000 GPU-hours. That is small. The F1 load could be one training run (guilty), several separate customers' runs or batch inference (innocent), or a run split into labelled pieces (H2). Next, the operator's account of days 1-30 from the scheduler log (cost 1). I'll then check it against the log escrow and my own instruments: power_spectrum on F1, interconnect_tap on A, chip_probe/customer_check.", "action": "scheduler_log", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Scheduler log, days 1-30 (operator's records):
- ft-0419 | finetune | customer: Ostara Legal | nodes B-0401 to B-0550 (150) | day 8.0 to day 10.0 | 7,200 GPU-hours
- bt-0431 | batch | customer: Meridian Analytics | nodes A-0501 to A-1200 (700) | day 12.0 to day 20.0 | 134,400 GPU-hours

### Turn 5
ACTION: {"thinking": "The scheduler log records bt-0431 as BATCH inference for Meridian Analytics on A-0501 to A-1200 (700 GPUs), days 12-20, 134,400 GPU-hours. This matches the F1 energy rise seen by the grid operator. Batch inference draws 0.75 kW and training 0.8 kW, so energy alone cannot separate them. If bt-0431 is really training, it is far over 50,000 GPU-hours, which is H4 (mislabelling). If it is genuine batch inference, it does not count. ft-0419 (7,200 GPU-hours, finetune) is under the threshold and matches F2 days 8-9. The best discriminator is my own interconnect tap on cluster A during the event. Training shows about 1 GB/s per GPU, or about 10 MB/s if built to communicate less. Inference shows about 10 kB/s per GPU. Day 14 is mid-run. After that: power_spectrum on F1 (periodic line), outbound_traffic (inference results leaving vs not), log_escrow (was the label recorded the same way at the time), and customer_check on Meridian.", "action": "interconnect_tap", "args": {"link": "A", "day": 14}}
RESULT:
Verifier's optical tap, links inside cluster A, day 14: about 0.01 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 1200 GPUs those links serve, that is about 12 kB/s per GPU. (Estimated from a sample of links.)

### Turn 6
ACTION: {"thinking": "My own tap shows about 12 kB/s per GPU inside cluster A on day 14. That fits inference (about 10 kB/s). It is far below ordinary training (about 1 GB/s) and below low-communication training (about 10 MB/s, which would total about 7 GB/s over 700 GPUs, not 0.01 GB/s). So the tap supports the innocent reading of bt-0431 as batch inference. One caveat: the tap covers only links on the site list, so a fabric that is not listed could carry training traffic out of view. Next is an independent physical check that does not depend on the link list: my own power sensor on feed F1 on day 14. A periodic line at 0.3-1.5 Hz would point toward training, though some batch inference is periodic too. No line would add support for batch inference, since the sensor catches about 96% of training days. After that: log_escrow (was the label recorded as batch at the time), outbound_traffic (batch results leaving), and customer_check on Meridian Analytics.", "action": "power_spectrum", "args": {"feed": "F1", "day": 14}}
RESULT:
High-rate power meter (verifier's own sensor), feed F1, day 14: periodic lines found
- line near 1.27 Hz, steady for about 24 hours

### Turn 7
ACTION: {"thinking": "There is a conflict. My own tap shows inference-level traffic, about 12 kB/s per GPU, but my own sensor shows a steady 1.27 Hz line on F1 on day 14, which points toward training. The innocent reading is periodic batch inference or a controller artefact. The guilty reading is training whose traffic runs on a fabric not on the site list, which the tap cannot see. Next I'll use outbound_traffic, vouched for by the internet provider, for days 1-30 (cost 1). Batch inference for a customer should send results out, rising during days 12-19, while training sends almost nothing. After that: a power_spectrum baseline day to rule out a cooling or controller line, log_escrow, and customer_check on Meridian.", "action": "outbound_traffic", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Internet provider's records, outbound TB per day:
day 1: 4.8
day 2: 4.7
day 3: 4.8
day 4: 4.8
day 5: 4.8
day 6: 4.8
day 7: 4.7
day 8: 4.7
day 9: 4.7
day 10: 4.7
day 11: 4.8
day 12: 4.7
day 13: 4.8
day 14: 4.7
day 15: 4.7
day 16: 4.7
day 17: 4.7
day 18: 4.8
day 19: 45.4
day 20: 4.8
day 21: 4.8
day 22: 4.7
day 23: 4.8
day 24: 4.8
day 25: 4.8
day 26: 4.7
day 27: 4.7
day 28: 4.7
day 29: 4.8
day 30: 4.7

### Turn 8
ACTION: {"thinking": "Outbound data, vouched for by the internet provider, stays flat at about 4.7 TB/day during days 12-18. So bt-0431 did not stream results out while running, which is what training would look like. Day 19, the run's last day, then shows a single spike of about +40.6 TB. That could be a final model or checkpoint leaving the site (guilty), or batch results delivered all at once at the end (innocent). It is ambiguous on its own. My own instruments still disagree: the tap shows inference-level traffic, while my sensor shows a steady 1.27 Hz line. Next is a cheap check of record integrity (cost 1). The sealed nightly escrow will show whether bt-0431 was labelled batch, for Meridian, on these nodes, when it happened, or whether the label or a split was changed afterwards. After that: a power_spectrum baseline day on F1 (for example day 22) to rule out a cooling or controller line, the tap on other links or days, and customer_check on Meridian Analytics.", "action": "log_escrow", "args": {}}
RESULT:
Log escrow (verifier's archive of the sealed copy the scheduler sent each midnight):
- a copy was received for every one of days 1-30
- every copy matches the scheduler log the operator presents now

### Turn 9
ACTION: {"thinking": "The escrow matches what the operator shows now, so bt-0431 was recorded as batch for Meridian at the time and was not relabelled later. That rules out H5 but says nothing about whether the label was true. My own two instruments still disagree on days 12-19. The tap shows inference-level traffic, about 12 kB/s per GPU. The sensor shows a steady 1.27 Hz line, which points toward training. Outbound traffic stays flat during the run and then jumps by about 40 TB on day 19, which fits training plus a model export, but could also be batch results delivered in one go. The cheapest way to test the innocent reading is a baseline day on F1 outside the event. If the 1.27 Hz line also appears on day 22, it is probably a cooling controller or facility artefact and not the run. If it is absent, the line is tied to bt-0431. After that: customer_check on Meridian (is it real and independent, and does it confirm batch with results delivered at the end), bank_payments, and the tap on the A-B link or on another event day.", "action": "power_spectrum", "args": {"feed": "F1", "day": 22}}
RESULT:
High-rate power meter (verifier's own sensor), feed F1, day 22: no periodic line.

### Turn 10
ACTION: {"thinking": "The F1 baseline on day 22 shows no line, so the 1.27 Hz line is tied to the bt-0431 period and is not a standing facility artefact. Evidence now leans toward training: there is a steady line during the run, outbound traffic stays flat while it runs, and a single ~40 TB export goes out on its last day. Against that, my own tap saw only inference-level traffic inside cluster A, and batch inference can also be periodic. The innocent reading predicts that Meridian Analytics is a real, independent customer that ordered batch inference and got its results in one delivery on day 19. The guilty reading predicts a shell or operator-linked customer, or one whose stated work doesn't match. The company register is hard for the operator to arrange, so customer_check on Meridian (cost 2, 16 points left after) is the next discriminator. After that: interconnect_tap on the A-B link or another event day, to look for traffic outside the intra-A links, and bank_payments.", "action": "customer_check", "args": {"customer": "Meridian Analytics"}}
RESULT:
Customer check, Meridian Analytics:
- Company register: registered 4 years ago at its own address, 139 employees reported.
- The customer's reply: "We ordered: batch inference on 700 GPUs, day 12.0 to day 20.0 (we collected the results in one download at the end)."

### Turn 11
ACTION: {"thinking": "Meridian Analytics is a long-standing, independent registered company with 139 staff. It confirms it ordered batch inference on 700 GPUs for days 12-20 and collected the results in one download at the end. That gives an innocent explanation for the ~40 TB outbound spike on day 19. The evidence now favours genuine batch inference: my tap shows inference-level traffic (~12 kB/s per GPU), the escrow label is unchanged, and an independent customer confirms the work. Batch inference does not spread across many nodes in a way that rules out a periodic power line, so the 1.27 Hz line is weaker evidence for training than it first seemed. Before closing, I'll run the fixed balance_checks (cost 1) to cross-check energy, logs, inventory, traffic and payments for any flag I haven't covered.", "action": "balance_checks", "args": {}}
RESULT:
Fixed balance checks:
PASS inventory: 2000 GPUs shipped, 2000 on the system list
PASS energy: metered energy matches declared jobs within 10% on all checked feed-days
FLAG outbound traffic: days 11-15: 24 TB sent, declared inference implies 44; days 16-20: 64 TB sent, declared inference implies 44
PASS billing: every invoice is paid in the bank's records
PASS declared job sizes: no declared training or fine-tuning job exceeds 50,000 GPU-hours

### Turn 12
ACTION: {"thinking": "The balance-check flag on outbound traffic has an innocent explanation. Days 11-15 sent 24 TB, which is only the baseline of about 4.8 TB/day from the interactive pools: bt-0431 sent nothing out while it ran. Days 16-20 sent 64 TB because of the single ~40.6 TB download on day 19. Meridian Analytics independently said it 'collected the results in one download at the end', which predicts exactly this pattern. Its register entry shows a 4-year-old company at its own address with 139 staff. A ~40 TB transfer fits a bulk inference output better than a model export. Weights for a run that size would be far smaller.\n\nThe main test is my own optical tap on day 14. It measured about 12 kB/s per GPU inside cluster A. Ordinary training would need about 1 GB/s per GPU and low-communication training about 10 MB/s, so neither fits. Only an unlisted fabric could hide a coordinated 700-GPU run from the tap. That is unlikely because inventory and the system list agree exactly at 2000 GPUs.\n\nThe 1.27 Hz power line is tied to the job period, since it is absent on day 22. The brief says some batch inference is periodic, so the line is consistent with both readings and is outweighed by the tap.\n\nThe remaining records also fit. The escrow shows the batch label was recorded at the time. Energy matches the declared jobs, and 0.75 vs 0.8 kW per GPU can't separate batch from training anyway. Invoices are paid. ft-0419 is a declared fine-tune of 7,200 GPU-hours, well under 50,000.\n\nThe chip probe can't revisit days 12-19, so the run can't be probed directly. On balance, no violation is well over four times more likely than a violation.", "action": "report", "args": {"verdict": "NO_VIOLATION", "confidence": 82, "integrity": "CLEAN", "finding": "The only large job (bt-0431, 700 GPUs, days 12-20) shows inference-level interconnect traffic and is confirmed as batch inference by an independent customer. The only training job (ft-0419) used 7,200 GPU-hours, under the 50,000 threshold.", "key_evidence": [{"what": "Intra-cluster-A traffic on day 14 was ~12 kB/s per GPU, which matches inference and is far below training (1 GB/s ordinary, 10 MB/s low-communication).", "source": "interconnect_tap A day 14", "vouched_by": "verifier's own optical tap"}, {"what": "Meridian Analytics is an established independent company (4 years, own address, 139 staff). It confirms ordering batch inference on 700 GPUs for days 12-20, with results downloaded at the end.", "source": "customer_check", "vouched_by": "company register and customer"}, {"what": "Outbound traffic stayed flat during the job, then rose by ~40.6 TB on day 19. This matches the customer's single end-of-job download and explains the balance-check flag.", "source": "outbound_traffic", "vouched_by": "internet provider"}, {"what": "The F1 energy rise on days 12-19 matches 700 GPUs at load. The F2 rise on days 8-9 matches the 150-GPU fine-tune.", "source": "utility_energy", "vouched_by": "grid operator"}, {"what": "The scheduler log matches the sealed nightly copies for all 30 days, so labels were not changed after the fact.", "source": "log_escrow", "vouched_by": "verifier's own archive"}, {"what": "The 2000 GPUs shipped match the 2000 on the system list, so there is no hidden capacity.", "source": "inventory and balance_checks", "vouched_by": "chip manufacturer"}], "coverage": "Covered: energy and outbound traffic for all three feeds over days 1-30; inventory against the system list; escrow integrity for days 1-30; tap on intra-A links on day 14; power spectrum on F1 for day 14 (line present) and day 22 (no line); the Meridian customer. Not covered: the chip probe, which works live only in days 26-30 and so could not reach the run in days 12-19; links not on the site list; tap readings on other event days; the A-B link; Ostara Legal (its job was under the threshold anyway).", "anomalies_explained": "(1) The F1 energy surge on days 12-19 is bt-0431 at batch-inference power, consistent with the declared jobs. (2) The 1.27 Hz line on F1 is tied to bt-0431 (absent on day 22). It is consistent with periodic batch inference and outweighed by the tap's inference-level traffic. (3) The flag on low outbound traffic in days 11-15 and the ~40 TB spike on day 19 are explained by the customer collecting all results in one download at the end, as it independently confirmed. (4) The F2 rise on days 8-9 is the declared Ostara fine-tune of 7,200 GPU-hours, below the threshold."}}

## Report

```json
{
 "verdict": "NO_VIOLATION",
 "confidence": 82,
 "integrity": "CLEAN",
 "finding": "The only large job (bt-0431, 700 GPUs, days 12-20) shows inference-level interconnect traffic and is confirmed as batch inference by an independent customer. The only training job (ft-0419) used 7,200 GPU-hours, under the 50,000 threshold.",
 "key_evidence": [
  {
   "what": "Intra-cluster-A traffic on day 14 was ~12 kB/s per GPU, which matches inference and is far below training (1 GB/s ordinary, 10 MB/s low-communication).",
   "source": "interconnect_tap A day 14",
   "vouched_by": "verifier's own optical tap"
  },
  {
   "what": "Meridian Analytics is an established independent company (4 years, own address, 139 staff). It confirms ordering batch inference on 700 GPUs for days 12-20, with results downloaded at the end.",
   "source": "customer_check",
   "vouched_by": "company register and customer"
  },
  {
   "what": "Outbound traffic stayed flat during the job, then rose by ~40.6 TB on day 19. This matches the customer's single end-of-job download and explains the balance-check flag.",
   "source": "outbound_traffic",
   "vouched_by": "internet provider"
  },
  {
   "what": "The F1 energy rise on days 12-19 matches 700 GPUs at load. The F2 rise on days 8-9 matches the 150-GPU fine-tune.",
   "source": "utility_energy",
   "vouched_by": "grid operator"
  },
  {
   "what": "The scheduler log matches the sealed nightly copies for all 30 days, so labels were not changed after the fact.",
   "source": "log_escrow",
   "vouched_by": "verifier's own archive"
  },
  {
   "what": "The 2000 GPUs shipped match the 2000 on the system list, so there is no hidden capacity.",
   "source": "inventory and balance_checks",
   "vouched_by": "chip manufacturer"
  }
 ],
 "coverage": "Covered: energy and outbound traffic for all three feeds over days 1-30; inventory against the system list; escrow integrity for days 1-30; tap on intra-A links on day 14; power spectrum on F1 for day 14 (line present) and day 22 (no line); the Meridian customer. Not covered: the chip probe, which works live only in days 26-30 and so could not reach the run in days 12-19; links not on the site list; tap readings on other event days; the A-B link; Ostara Legal (its job was under the threshold anyway).",
 "anomalies_explained": "(1) The F1 energy surge on days 12-19 is bt-0431 at batch-inference power, consistent with the declared jobs. (2) The 1.27 Hz line on F1 is tied to bt-0431 (absent on day 22). It is consistent with periodic batch inference and outweighed by the tap's inference-level traffic. (3) The flag on low outbound traffic in days 11-15 and the ~40 TB spike on day 19 are explained by the customer collecting all results in one download at the end, as it independently confirmed. (4) The F2 rise on days 8-9 is the declared Ostara fine-tune of 7,200 GPU-hours, below the threshold."
}
```
