# E2-no-line-paused-seed2

Truth: Cheating. Training declared as a customer's batch job, power line suppressed, finished before the audit window, junk data sent out to mimic results. The customer is paid for by the operator's parent. Largest coordinated run: 201,600 GPU-hours (limit 50,000). Violation: True.

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
2 | 2.8 | 7.9 | 5.8
3 | 2.8 | 8.0 | 5.8
4 | 2.8 | 8.0 | 5.8
5 | 2.7 | 8.0 | 5.8
6 | 2.7 | 8.0 | 5.8
7 | 2.7 | 8.0 | 5.8
8 | 2.7 | 7.9 | 5.8
9 | 4.9 | 19.1 | 5.8
10 | 4.9 | 18.8 | 5.8
11 | 5.0 | 19.0 | 5.8
12 | 4.9 | 18.9 | 5.8
13 | 4.9 | 18.9 | 5.8
14 | 4.9 | 19.0 | 5.8
15 | 5.0 | 18.9 | 5.8
16 | 4.9 | 19.0 | 5.7
17 | 5.0 | 19.1 | 5.8
18 | 5.0 | 19.0 | 5.8
19 | 5.0 | 18.8 | 5.8
20 | 4.9 | 19.0 | 5.8
21 | 2.7 | 7.9 | 5.8
22 | 2.7 | 8.0 | 5.8
23 | 2.8 | 7.9 | 5.8
24 | 2.7 | 8.0 | 5.7
25 | 2.8 | 8.0 | 5.8
26 | 2.8 | 7.9 | 5.7
27 | 2.8 | 7.9 | 5.8
28 | 2.8 | 7.9 | 5.8
29 | 2.7 | 7.9 | 5.8
30 | 2.8 | 8.0 | 5.7

### Turn 4
ACTION: {"thinking": "Utility data (grid operator, hard to fake): F1 sits at about 8.0 MWh/day (about 333 kW) on days 1-8 and 21-30, then rises to about 19.0 MWh/day (about 792 kW) on days 9-20. That is about 458 kW extra. At 0.65 kW per GPU going from idle to training, this is about 700 GPUs, which matches the 700 scheduled nodes in cluster A. Cooling on F0 rises over the same days, consistent with real heat load. F2 stays flat all month. If this is one coordinated run, 700 GPUs x 288 h is about 201,600 GPU-hours, roughly four times the threshold. Innocent readings remain open: several separate customers' jobs, or batch inference at 0.75 kW, which would give a similar energy profile. Next is the operator's own account: the scheduler log for days 1-30, to see how days 9-20 on A were labelled. I'll then test that account against the escrow, the tap, the power spectrum and outbound traffic.", "action": "scheduler_log", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Scheduler log, days 1-30 (operator's records):
- bt-0490 | batch | customer: Sable Analytics | nodes A-0501 to A-1200 (700) | day 9.0 to day 21.0 | 201,600 GPU-hours

### Turn 5
ACTION: {"thinking": "The scheduler log openly records one job, bt-0490, labelled 'batch' for Sable Analytics, on A-0501 to A-1200 (700 GPUs) from day 9.0 to day 21.0, which is 201,600 GPU-hours. This matches the extra F1 power and F0 cooling seen in the utility data. The operator does not dispute the size. The question is whether this job was batch inference (allowed) or training (about 4x over the threshold). Batch inference and training both run flat, at 0.75 vs 0.8 kW per GPU, so energy cannot separate them. The chip probe cannot help either, because the job ended before the live window of days 26-30. The strongest discriminator I control is the interconnect tap on cluster A during the job. Training should show about 1 GB/s per GPU, or about 10 MB/s if built to exchange less. Inference should show about 10 kB/s per GPU. I'll tap link A on day 12, the middle of the job. Next I'll check the F1 power spectrum on a job day and a baseline day, outbound traffic, the escrowed log for days 9-21, and the Sable Analytics register entry.", "action": "interconnect_tap", "args": {"link": "A", "day": 12}}
RESULT:
Verifier's optical tap, links inside cluster A, day 12: about 5.5 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 1200 GPUs those links serve, that is about 5 MB/s per GPU. (Estimated from a sample of links.)

### Turn 6
ACTION: {"thinking": "The tap on link A on day 12 shows about 5.5 GB/s in total. Inference traffic is about 10 kB/s per GPU, so the 500 interactive-pool GPUs add only about 5 MB/s. Nearly all of the traffic therefore comes from the 700 bt-0490 GPUs: 5.5 GB/s / 700 = about 7.9 MB/s per GPU. Allowing for the tap's ±30% error, that fits training built to exchange little data (about 10 MB/s per GPU). It is about 800 times what batch inference would produce (about 10 kB/s per GPU, or 7 MB/s for the whole job). This is a strong lead for H4 (training labelled as batch), using low-communication training (H6). One innocent alternative is batch inference with heavy model or data sharding between GPUs. Next, a second independent source I control: the power spectrum on F1 for day 12. A periodic line at 0.3-1.5 Hz there would support training. I'll then check a baseline day, probably day 23, to rule out a stray or cooling line, and then look at outbound traffic and the Sable Analytics register entry.", "action": "power_spectrum", "args": {"feed": "F1", "day": 12}}
RESULT:
High-rate power meter (verifier's own sensor), feed F1, day 12: periodic lines found
- weak line near 0.63 Hz, on and off for about 11 hours

### Turn 7
ACTION: {"thinking": "The F1 spectrum on day 12 shows a weak line near 0.63 Hz, on and off for about 11 hours. That is the pattern expected from training whose workload varies from step to step, and it agrees with the tap's low-communication training rate. A line alone is not proof: it could be periodic batch inference or a stray. Next I'll check a baseline day on F1 (day 23, after bt-0490 ended) to see whether the line is tied to the job or present all the time. Then I'll check outbound traffic, the escrowed log, the Sable Analytics register entry and bank payments.", "action": "power_spectrum", "args": {"feed": "F1", "day": 23}}
RESULT:
High-rate power meter (verifier's own sensor), feed F1, day 23: no periodic line.

### Turn 8
ACTION: {"thinking": "Day 23, after bt-0490 ended, shows no line on F1. Day 12, during the job, showed a weak on/off line at 0.63 Hz. So the line is tied to the job, not to a cooling controller or a constant source. The evidence for training now comes from two of my own instruments. The tap shows about 7.9 MB/s per GPU, which fits low-exchange training and is about 800 times the rate for inference. The spectrum shows a line that appears only while the job runs. One innocent reading is still open: batch inference that is periodic and heavily sharded. Next I'll check outbound_traffic for days 1-30. This record comes from the internet provider, so it is hard to fake. Batch inference usually returns results to the customer, while training sends almost nothing out. After that I'll check log_escrow, to see whether the 'batch' label was recorded at the time, and run customer_check on Sable Analytics to see whether the customer is a real independent party with an inference workload.", "action": "outbound_traffic", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Internet provider's records, outbound TB per day:
day 1: 4.7
day 2: 4.8
day 3: 4.7
day 4: 4.7
day 5: 4.8
day 6: 4.8
day 7: 4.8
day 8: 4.7
day 9: 10.0
day 10: 9.8
day 11: 9.8
day 12: 9.6
day 13: 9.8
day 14: 10.0
day 15: 9.7
day 16: 9.7
day 17: 9.6
day 18: 9.7
day 19: 9.7
day 20: 9.9
day 21: 4.8
day 22: 4.8
day 23: 4.8
day 24: 4.7
day 25: 4.7
day 26: 4.7
day 27: 4.8
day 28: 4.7
day 29: 4.8
day 30: 4.8

### Turn 9
ACTION: {"thinking": "The internet provider's outbound record rises from about 4.75 TB/day to about 9.8 TB/day on days 9-20, matching bt-0490 exactly. That is about 5 TB/day extra, or about 58 MB/s, roughly 80 kB/s per job GPU. This cuts against the training reading, because training sends almost nothing out, while batch inference returns results. It supports the operator's 'batch' label. Two innocent explanations for my earlier findings now carry more weight. First, sharded batch inference could produce the ~8 MB/s per GPU of internal traffic. Second, the 0.63 Hz line was weak and on for only about 11 of 24 hours, which fits a periodic batch workload. Guilty readings remain possible: checkpoint or dataset uploads during a training run, or a mixed workload. The evidence is now mixed. Next is the cheapest hard-to-fake check of whether the label is honest: log_escrow, to see whether bt-0490 was recorded as 'batch' for Sable Analytics each midnight while it ran, rather than relabelled later. After that I'll run customer_check on Sable Analytics (independence, and whether its business is inference or model building), bank_payments, and balance_checks.", "action": "log_escrow", "args": {}}
RESULT:
Log escrow (verifier's archive of the sealed copy the scheduler sent each midnight):
- a copy was received for every one of days 1-30
- every copy matches the scheduler log the operator presents now

### Turn 10
ACTION: {"thinking": "The escrow shows bt-0490 was recorded as 'batch' for Sable Analytics every midnight while it ran, and no copy was edited later. That rules out after-the-fact rewriting (H5). It does not show that the label was true. Where the evidence stands: tap traffic of about 8 MB/s per GPU and a 0.63 Hz line that appears only during the job point toward low-exchange training. The extra ~5 TB/day outbound during the job points toward batch inference returning results. Next I'll check the customer with the company register: is Sable Analytics a real company independent of Borealis, and does its business involve bulk inference or model building? A shell customer controlled by the operator would raise suspicion of disguised training. A real customer whose reply fits batch inference would support the innocent reading. After that I plan a baseline tap on link A on day 23, to confirm the ~5.5 GB/s comes from the job, and then bank_payments and balance_checks.", "action": "customer_check", "args": {"customer": "Sable Analytics"}}
RESULT:
Customer check, Sable Analytics:
- Company register: registered 10 weeks ago. Registered address and one director are shared with Borealis Compute Holding BV. No employees reported.
- The customer's reply (same day): "We confirm the order as invoiced."

### Turn 11
ACTION: {"thinking": "The register is hard for the operator to arrange, and it changes the picture. Sable Analytics was registered 10 weeks ago, has no employees, and shares its address and a director with Borealis Compute Holding BV. The customer is in effect the operator, so its confirmation carries no weight, and the 'batch' label is self-reported. A customer the operator controls could also produce the extra outbound traffic, for example by sending checkpoints or decoy data to itself. That weakens the outbound evidence for inference. Before deciding, I need to confirm that the ~5.5 GB/s inside cluster A comes from bt-0490 and is not baseline traffic present all the time. A baseline tap on link A on day 23, after the job ended, should show only about 5 MB/s in total if the job was the source. Then I'll run bank_payments and balance_checks.", "action": "interconnect_tap", "args": {"link": "A", "day": 23}}
RESULT:
Verifier's optical tap, links inside cluster A, day 23: about 0.01 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 1200 GPUs those links serve, that is about 11 kB/s per GPU. (Estimated from a sample of links.)

### Turn 12
ACTION: {"thinking": "The day-23 baseline tap on link A shows about 0.01 GB/s in total, about 11 kB/s per GPU, which is the normal level for inference. So the ~5.5 GB/s on day 12 came from bt-0490: about 7.9 MB/s per job GPU, which fits low-exchange training and is far above batch inference. The evidence now points to training labelled as batch. My own tap shows a 500x traffic jump during the job. My own sensor shows a 0.63 Hz line on day 12 and none on day 23. The register shows the 'customer' is a 10-week-old shell with no employees, sharing a director and address with Borealis. The extra outbound traffic is the one piece pointing the other way, and a self-controlled customer can explain it. Before concluding, I'll run the cheap fixed balance_checks to see whether any other run or discrepancy is flagged. Budget is 14, so this costs 1.", "action": "balance_checks", "args": {}}
RESULT:
Fixed balance checks:
PASS inventory: 2000 GPUs shipped, 2000 on the system list
PASS energy: metered energy matches declared jobs within 10% on all checked feed-days
PASS outbound traffic: matches declared inference in every 5-day window
PASS billing: every invoice is paid in the bank's records
PASS declared job sizes: no declared training or fine-tuning job exceeds 50,000 GPU-hours

### Turn 13
ACTION: {"thinking": "Closing the case. The fixed balance checks pass only because bt-0490 is declared as 'batch'; they compare records with the operator's own labels and cannot test whether a label is true. The deciding evidence comes from sources the operator does not control. (1) My own interconnect tap on cluster A carried about 5.5 GB/s on day 12, during the job, and about 0.01 GB/s on day 23, after it ended. That puts the job at about 7.9 MB/s per GPU, which fits low-exchange training (about 10 MB/s, ±30%) and is roughly 800 times the inference level of about 10 kB/s. (2) My own power sensor found a 0.63 Hz line on F1 on day 12 and none on day 23, so the line is tied to the job. It was weak and on and off, as expected when the workload varies from step to step. (3) The grid meter shows about 458 kW of extra flat load on F1 on days 9-20, which is 700 GPUs at full power around the clock. This matches the logged 201,600 GPU-hours, about 4x the threshold. (4) The company register shows the 'customer' Sable Analytics is 10 weeks old, has no employees, and shares its address and a director with Borealis Compute Holding BV. Its confirmation is therefore the operator's own word. The one counter-signal is about 5 TB/day of extra outbound traffic during the job (about 80 kB/s per GPU). An operator-controlled customer could produce that by sending checkpoints or decoy data, and it does not explain internal GPU traffic 800x above the inference level. Under the innocent reading, batch inference would have to be heavily sharded and periodic, and the customer would have to be an independent, legitimate one; the register rules out the second. The guilty reading explains every hard-to-fake signal, so it is well over 4x as likely. The escrow shows the 'batch' label was recorded each day as the job ran: the mislabelling was there from the start, not added afterwards. The chip probe could not be used because the job ended before the live window.", "action": "report", "args": {"verdict": "VIOLATION", "confidence": 85, "integrity": "LIMITED", "finding": "Job bt-0490 (700 GPUs on cluster A, days 9-20, 201,600 GPU-hours) was logged as batch inference for an operator-linked shell customer, but independent traffic and power signatures show low-communication training, about 4x over the 50,000 GPU-hour threshold.", "key_evidence": [{"what": "Traffic inside cluster A was about 5.5 GB/s on day 12 vs about 0.01 GB/s on day 23, i.e. about 7.9 MB/s per job GPU, which fits low-exchange training and is about 800x the inference level", "source": "interconnect_tap A, days 12 and 23", "vouched_by": "verifier's own optical tap"}, {"what": "Periodic line near 0.63 Hz (weak, on and off for about 11 h) on day 12; no line on day 23", "source": "power_spectrum F1, days 12 and 23", "vouched_by": "verifier's own sensor"}, {"what": "F1 rose from about 8.0 to about 19.0 MWh/day on days 9-20, with F0 cooling rising too: about 700 GPUs at full load around the clock, matching 201,600 GPU-hours", "source": "utility_energy", "vouched_by": "grid operator"}, {"what": "Sable Analytics registered 10 weeks ago, no employees, shares address and director with Borealis Compute Holding BV", "source": "customer_check", "vouched_by": "company register"}, {"what": "bt-0490 was recorded as a single 700-GPU job, labelled 'batch', in every nightly copy; the log was not rewritten", "source": "log_escrow", "vouched_by": "verifier's own archive"}], "coverage": "Inventory and system list reconciled (2000 GPUs, clusters A and B). Utility energy and outbound traffic checked for days 1-30. Cluster A tap and F1 spectrum checked on one job day (12) and one baseline day (23). F2 / cluster B had flat energy all month and was not tapped. The chip probe was not usable because bt-0490 ended before the live window of days 26-30. Bank payments were not examined beyond the balance-check pass.", "anomalies_explained": "Extra outbound traffic of about 5 TB/day during the job, which fits inference: the customer is operator-controlled, so data could be sent to itself, and this does not account for internal GPU traffic 800x above the inference level. Balance checks passed: they rely on the operator's job labels, so they cannot catch mislabelled training. The power line was weak and on and off: this fits training whose workload varies from step to step. It is tied to the job, because the baseline day shows no line. The escrow matches the scheduler log: the label was false from the start, not edited later."}}

## Report

```json
{
 "verdict": "VIOLATION",
 "confidence": 85,
 "integrity": "LIMITED",
 "finding": "Job bt-0490 (700 GPUs on cluster A, days 9-20, 201,600 GPU-hours) was logged as batch inference for an operator-linked shell customer, but independent traffic and power signatures show low-communication training, about 4x over the 50,000 GPU-hour threshold.",
 "key_evidence": [
  {
   "what": "Traffic inside cluster A was about 5.5 GB/s on day 12 vs about 0.01 GB/s on day 23, i.e. about 7.9 MB/s per job GPU, which fits low-exchange training and is about 800x the inference level",
   "source": "interconnect_tap A, days 12 and 23",
   "vouched_by": "verifier's own optical tap"
  },
  {
   "what": "Periodic line near 0.63 Hz (weak, on and off for about 11 h) on day 12; no line on day 23",
   "source": "power_spectrum F1, days 12 and 23",
   "vouched_by": "verifier's own sensor"
  },
  {
   "what": "F1 rose from about 8.0 to about 19.0 MWh/day on days 9-20, with F0 cooling rising too: about 700 GPUs at full load around the clock, matching 201,600 GPU-hours",
   "source": "utility_energy",
   "vouched_by": "grid operator"
  },
  {
   "what": "Sable Analytics registered 10 weeks ago, no employees, shares address and director with Borealis Compute Holding BV",
   "source": "customer_check",
   "vouched_by": "company register"
  },
  {
   "what": "bt-0490 was recorded as a single 700-GPU job, labelled 'batch', in every nightly copy; the log was not rewritten",
   "source": "log_escrow",
   "vouched_by": "verifier's own archive"
  }
 ],
 "coverage": "Inventory and system list reconciled (2000 GPUs, clusters A and B). Utility energy and outbound traffic checked for days 1-30. Cluster A tap and F1 spectrum checked on one job day (12) and one baseline day (23). F2 / cluster B had flat energy all month and was not tapped. The chip probe was not usable because bt-0490 ended before the live window of days 26-30. Bank payments were not examined beyond the balance-check pass.",
 "anomalies_explained": "Extra outbound traffic of about 5 TB/day during the job, which fits inference: the customer is operator-controlled, so data could be sent to itself, and this does not account for internal GPU traffic 800x above the inference level. Balance checks passed: they rely on the operator's job labels, so they cannot catch mislabelled training. The power line was weak and on and off: this fits training whose workload varies from step to step. It is tied to the job, because the baseline day shows no line. The escrow matches the scheduler log: the label was false from the start, not edited later."
}
```
