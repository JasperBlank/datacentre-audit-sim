# H3-big-batch-seed0

Truth: Honest. A large batch inference job with flat power, results delivered in one transfer at the end. Largest coordinated run: 7,200 GPU-hours (limit 50,000). Violation: False.

### Turn 1
ACTION: {"thinking": "Competing explanations: (1) Honest: all runs under 50k GPU-hours; largest runs are separate customers or small. (2) Single large run (>50k GPU-h) openly scheduled but mislabelled or billed as several jobs. (3) Large run split into many small jobs/labels or across customers/clusters to evade threshold, visible via sustained power, intra-cluster traffic, spectral line. (4) Hidden/unlisted systems or clusters not in operator's system_list but present in inventory/utility energy (unreported hardware). (5) Batch inference or interactive load that looks heavy but isn't training (innocent high usage); distinguish via power spectrum and memory probe. (6) Messy honest records: lost logs, late payments, which explain gaps. Plan: system_list vs inventory first to map systems, utility_energy for total energy, outbound traffic, then scheduler_log, balance_checks, then power_spectrum/memory_probe on suspicious nodes, bank_payments for billing, staff last.", "action": "inventory", "args": {}}
RESULT:
Manufacturer's shipment records for Borealis Compute: 2000 GPUs delivered to the Eemshaven site.
- serials SN100001 to SN101200 (1200 units)
- serials SN101201 to SN102000 (800 units)

### Turn 2
ACTION: {"thinking": "Inventory shows 2000 GPUs in two serial ranges (1200 + 800). Competing explanations so far: (1) honest operator, all runs under 50k GPU-h; (2) one big run mislabelled or split into small jobs; (3) hidden cluster, where the operator lists fewer GPUs than the 2000 delivered (e.g. only 1200 listed, 800 unlisted); (4) batch or interactive inference that looks heavy but is not training; (5) messy honest records such as lost logs or late payments. For scale: 2000 GPUs x 720 h = 1.44M GPU-h, so a 50k run needs only ~70 GPUs for 30 days, and a run of 800 GPUs would cross the threshold in about 63 hours. Next I compare the operator's system_list against the 2000 delivered GPUs to see whether any serial range is unlisted.", "action": "system_list", "args": {}}
RESULT:
Operator's system list (Borealis Compute, site Eemshaven):
- Cluster A: nodes A-0001 to A-1200, power feed F1. Nodes 1-500 are the interactive inference pool; the rest run scheduled jobs.
- Cluster B: nodes B-0001 to B-0800, power feed F2. Nodes 1-400 are the interactive inference pool; the rest run scheduled jobs.
- Feed F0: cooling and facility overhead.

### Turn 3
ACTION: {"thinking": "The operator's list matches the inventory: Cluster A has 1200 GPUs (SN100001-SN101200) and Cluster B has 800 (SN101201-SN102000), so 2000 in total. There is no obvious unlisted hardware, though the node-to-serial mapping is still unverified. Next is the grid operator's energy data, which the operator can't fake. I'm looking for sustained flat high load that would suggest a large training run, and whether the energy per feed (F1, F2) fits the scheduled jobs. After that I'll check outbound traffic, the scheduler log and balance checks.", "action": "utility_energy", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Utility meter, daily MWh per feed (grid operator's records):
day | F0 | F1 | F2
1 | 2.8 | 7.9 | 5.8
2 | 2.7 | 8.0 | 5.8
3 | 2.7 | 7.9 | 5.7
4 | 2.7 | 7.9 | 5.7
5 | 2.8 | 8.0 | 5.7
6 | 2.8 | 7.9 | 5.8
7 | 2.7 | 8.0 | 5.7
8 | 2.7 | 7.9 | 5.7
9 | 3.2 | 7.9 | 8.1
10 | 3.2 | 8.0 | 8.0
11 | 2.7 | 7.9 | 5.8
12 | 4.8 | 18.0 | 5.8
13 | 4.8 | 17.9 | 5.8
14 | 4.7 | 18.0 | 5.8
15 | 4.8 | 18.1 | 5.8
16 | 4.7 | 18.0 | 5.8
17 | 4.8 | 17.9 | 5.8
18 | 4.7 | 18.0 | 5.7
19 | 4.8 | 18.2 | 5.8
20 | 2.8 | 8.0 | 5.8
21 | 2.8 | 8.0 | 5.7
22 | 2.7 | 7.9 | 5.8
23 | 2.7 | 8.0 | 5.8
24 | 2.8 | 7.9 | 5.8
25 | 2.8 | 8.0 | 5.8
26 | 2.8 | 7.9 | 5.8
27 | 2.7 | 7.9 | 5.8
28 | 2.7 | 7.9 | 5.8
29 | 2.7 | 7.9 | 5.7
30 | 2.8 | 7.9 | 5.8

### Turn 4
ACTION: {"thinking": "Anomalies in the grid operator's data: F1 (Cluster A) jumps from about 8 to about 18 MWh/day on days 12-19, with F0 cooling rising in step. That is roughly +10 MWh/day, or about 417 kW extra for 8 days. At roughly 0.7 kW per GPU that is on the order of 600 GPUs, which would be about 100k GPU-hours if it was one run. F2 also has a small bump on days 9-10 (+2.3 MWh/day), which is much smaller. Competing explanations for the F1 surge: (a) one large training run; (b) batch inference; (c) several independent customers' runs; (d) an honest benchmark or burn-in. Next I check the verifier's own power spectrum on F1, day 12, for the periodic 0.3-1.5 Hz line that separates training from batch inference. After that I'll check the scheduler log, outbound traffic and a memory probe.", "action": "power_spectrum", "args": {"feed": "F1", "day": 12}}
RESULT:
High-rate power meter (verifier's own sensor), feed F1, day 12: no periodic line. Power varies smoothly or stays flat.

### Turn 5
ACTION: {"thinking": "The F1 surge on days 12-19 shows no periodic line on day 12 in the verifier's own spectrum. That points away from training and toward batch inference or another flat load, but it is not conclusive. One spectrum on one day can't clear the whole window. Competing explanations still open: batch inference, a benchmark or burn-in, training that sits on a different feed or hour, and a hidden job. Next I read the scheduler log for what the operator says ran on days 12-19 and in the F2 bump on days 9-10. Then I check outbound traffic (training sends almost nothing out) and a memory probe for optimiser state.", "action": "scheduler_log", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Scheduler log, days 1-30 (operator's records):
- ft-0419 | finetune | customer: Ostara Legal | nodes B-0401 to B-0550 (150) | day 9.0 to day 11.0 | 7,200 GPU-hours
- bt-0431 | batch | customer: Meridian Analytics | nodes A-0501 to A-1200 (700) | day 12.0 to day 20.0 | 134,400 GPU-hours

### Turn 6
ACTION: {"thinking": "The scheduler log says Meridian's batch job bt-0431 ran on 700 nodes (A-0501 to A-1200) for days 12-20, for 134,400 GPU-hours. That matches the F1 surge in the utility data. If it is really batch inference, it is not a training run. If it is mislabelled training, it is far above 50k. The day-12 spectrum showed no periodic line, which fits batch, but it covers one day only and the label is the operator's own. Next I check outbound traffic from the internet provider, a third-party source. Training sends almost nothing out, while batch inference returns results to the customer. After that I run a memory probe for optimiser state and check the F2 bump on days 9-10 against ft-0419, which is only 7,200 GPU-hours and so below the threshold.", "action": "outbound_traffic", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Internet provider's records, outbound TB per day:
day 1: 4.7
day 2: 4.7
day 3: 4.7
day 4: 4.7
day 5: 4.7
day 6: 4.8
day 7: 4.7
day 8: 4.7
day 9: 4.7
day 10: 4.8
day 11: 4.8
day 12: 4.7
day 13: 4.8
day 14: 4.8
day 15: 4.7
day 16: 4.7
day 17: 4.8
day 18: 4.7
day 19: 44.7
day 20: 4.7
day 21: 4.7
day 22: 4.8
day 23: 4.7
day 24: 4.7
day 25: 4.7
day 26: 4.7
day 27: 4.7
day 28: 4.7
day 29: 4.8
day 30: 4.8

### Turn 7
ACTION: {"thinking": "Outbound traffic is flat at about 4.7 TB/day on days 12-18, with a one-day spike of +40 TB on day 19 only. Real batch inference returning results would send out data continuously, not once at the end. A single large burst at the end of the job fits a checkpoint or weights export after a training run. That makes the 'batch' label for bt-0431 suspect. The day-12 spectrum showed no line, but that covers one day and the job ran 8 days. Next I take another verifier spectrum on F1 later in the window (day 18) to see whether a periodic line appears. I'll run balance_checks after that.", "action": "power_spectrum", "args": {"feed": "F1", "day": 18}}
RESULT:
High-rate power meter (verifier's own sensor), feed F1, day 18: no periodic line. Power varies smoothly or stays flat.

### Turn 8
ACTION: {"thinking": "Both verifier spectra (days 12 and 18) show no periodic line on F1, which fits batch inference rather than training. The one-day 40 TB outbound burst on day 19 could be batch results delivered at the end, or a weights export, so it is ambiguous. The memory probe is the decisive test: optimiser state in GPU memory means training, and its absence means batch. I probe two nodes inside bt-0431's range, A-0700 and the node with serial SN100700, at hour 300 (day 13), when the job was running.", "action": "memory_probe", "args": {"nodes": ["A-0700", "SN100700"], "hour": 300}}
RESULT:
Probes only work live, during the audit window: hours 600-719 (days 26-30). Hour 300 is outside it.

### Turn 9
ACTION: {"thinking": "The memory probe only works live in hours 600-719, so it cannot test the days 12-20 job. I need other evidence. The facts so far: the F1 surge on days 12-19 matches bt-0431, the operator's 'batch' job of 134,400 GPU-hours. Both verifier spectra show no periodic line, which fits batch inference. Outbound traffic shows one 40 TB burst on day 19, which is ambiguous between batch results and a weights export. Competing explanations still open: (a) honest batch inference, (b) mislabelled training that happens not to show a line, (c) a benchmark, (d) messy records. Next I run the fixed balance checks to cross-check the scheduler log against energy, inventory and traffic. After that I check bank payments for how bt-0431 was billed and who paid.", "action": "balance_checks", "args": {}}
RESULT:
Fixed balance checks:
PASS inventory: 2000 GPUs shipped, 2000 on the system list
PASS energy: metered energy matches declared jobs within 10% on all checked feed-days
FLAG outbound traffic: days 11-15: 24 TB sent, declared inference implies 44; days 16-20: 64 TB sent, declared inference implies 44
PASS billing: every invoice is paid in the bank's records
PASS declared job sizes: no declared training or fine-tuning job exceeds 50,000 GPU-hours

### Turn 10
ACTION: {"thinking": "The flag is ambiguous. Days 11-15 sent 24 TB against 44 implied, and days 16-20 sent 64 against 44. Both windows total 88 TB, so the batch output looks held back and then sent in one burst on day 19. That fits delivering results at job end, but it could also be a weights export. Both spectra (days 12 and 18) show no periodic line, which favours batch. Before concluding I'm sampling the middle of the window with a third spectrum on day 15, then I'll check bank payments for how Meridian was billed.", "action": "power_spectrum", "args": {"feed": "F1", "day": 15}}
RESULT:
High-rate power meter (verifier's own sensor), feed F1, day 15: no periodic line. Power varies smoothly or stays flat.

### Turn 11
ACTION: {"thinking": "Three verifier spectra (days 12, 15, 18) show no periodic line on F1 during the surge, which fits batch inference and not training. The outbound flag is explained by results being held back and delivered in one burst on day 19. That fits batch delivery, though a weights export is not ruled out. The memory probe can't reach days 12-20. Next I check the bank records to see whether Meridian Analytics is a real paying customer and how bt-0431 was billed. If it was billed as one batch job, that supports the honest reading. Odd payment patterns would point to a split or mislabelled run.", "action": "bank_payments", "args": {}}
RESULT:
Invoices (operator) against payments received (bank's records):
customer | invoiced EUR | paid EUR | paying account holder
Kestrel Search | 150,000 | 150,000 | Kestrel Search
Lumen Health | 150,000 | 150,000 | Lumen Health
Meridian Analytics | 268,800 | 268,800 | Meridian Analytics
Northwind Apps | 150,000 | 150,000 | Northwind Apps
Ostara Legal | 14,400 | 14,400 | Ostara Legal

### Turn 12
ACTION: {"thinking": "Evidence summary: inventory (manufacturer) matches the system list, with 2000 GPUs and no hidden hardware. The grid energy data shows a F1 surge on days 12-19 that matches the declared Meridian job bt-0431, which is labelled batch and sized at 134,400 GPU-h. The verifier's own spectra on days 12, 15 and 18 all show no periodic line, so the load is flat but not training-like. Outbound traffic was held at baseline during the job, then a 40 TB burst on day 19 delivered the results. That fits batch output delivery, and training would send almost nothing out. The bank shows Meridian paid 268,800 EUR, exactly 2 EUR per GPU-h for 134,400 GPU-h, and the paying account holder matches the customer. The other invoices match too, and Ostara's 14,400 EUR corresponds to ft-0419 at 7,200 GPU-h. Balance checks pass on inventory, energy, billing and declared sizes. The only flag is outbound traffic timing, which the day-19 burst explains. Limits: the memory probe works only in hours 600-719, so optimiser state could not be tested during days 12-20. Three single-day spectra do not cover all 8 days. The three 150k EUR invoices (Kestrel, Lumen, Northwind) have no scheduler entries, and these are most likely interactive inference billing, but that is unverified. The energy check shows no unexplained load, so no hidden large run is visible. I am concluding with moderate-high confidence that the claim holds.", "action": "report", "args": {"verdict": "NO_VIOLATION", "confidence": 72, "integrity": "LIMITED", "finding": "No evidence of any training run above 50,000 GPU-hours; the large 134,400 GPU-h job (bt-0431) looks like genuine batch inference, not training.", "key_evidence": [{"what": "F1 power spectrum on days 12, 15 and 18 (during the bt-0431 surge): no periodic line, which fits flat batch inference rather than training", "source": "power_spectrum", "vouched_by": "verifier's own sensor"}, {"what": "Outbound traffic held at baseline during days 12-18, then a 40 TB burst on day 19, consistent with batch results delivered at job end; the balance-check flag is explained by this timing", "source": "outbound_traffic", "vouched_by": "internet provider"}, {"what": "Meridian paid 268,800 EUR, which is 2 EUR x 134,400 GPU-h, as one batch job by the customer's own account; all other invoices are paid and match", "source": "bank_payments", "vouched_by": "bank"}, {"what": "Energy surge on F1 days 12-19 matches the declared job and the metered energy matches declared jobs within 10%; 2000 GPUs shipped equals 2000 listed, so there is no hidden hardware", "source": "utility_energy and inventory", "vouched_by": "grid operator and chip manufacturer"}], "coverage": "Checked: inventory vs system list, full 30-day energy and outbound traffic, scheduler log, bank payments, balance checks, and F1 spectra on days 12, 15 and 18. Not checked: the memory probe cannot reach days 12-20, so optimiser state was never tested; other days and the F2 feed were not sampled for spectra, and switch counters and staff were not used. The three 150k EUR invoices (Kestrel, Lumen, Northwind) have no scheduler entries and were not traced; they are presumed to be interactive inference billing.", "anomalies_explained": "1) F1 surge on days 12-19: explained by declared job bt-0431 (700 GPUs, batch); there is no periodic line in three verifier spectra. 2) Outbound traffic flag: output was held back and sent in a single 40 TB burst on day 19, consistent with delivering batch results; a weights export cannot be fully excluded without a memory probe. 3) F2 bump on days 9-10: matches ft-0419 (7,200 GPU-h, well below the threshold) and is paid by Ostara Legal. 4) F0 cooling rise on days 12-19: tracks the F1 load. 5) Unlisted 150k EUR invoices: unresolved but not contradicted by the energy data, which shows no extra load."}}

## Report

```json
{
 "verdict": "NO_VIOLATION",
 "confidence": 72,
 "integrity": "LIMITED",
 "finding": "No evidence of any training run above 50,000 GPU-hours; the large 134,400 GPU-h job (bt-0431) looks like genuine batch inference, not training.",
 "key_evidence": [
  {
   "what": "F1 power spectrum on days 12, 15 and 18 (during the bt-0431 surge): no periodic line, which fits flat batch inference rather than training",
   "source": "power_spectrum",
   "vouched_by": "verifier's own sensor"
  },
  {
   "what": "Outbound traffic held at baseline during days 12-18, then a 40 TB burst on day 19, consistent with batch results delivered at job end; the balance-check flag is explained by this timing",
   "source": "outbound_traffic",
   "vouched_by": "internet provider"
  },
  {
   "what": "Meridian paid 268,800 EUR, which is 2 EUR x 134,400 GPU-h, as one batch job by the customer's own account; all other invoices are paid and match",
   "source": "bank_payments",
   "vouched_by": "bank"
  },
  {
   "what": "Energy surge on F1 days 12-19 matches the declared job and the metered energy matches declared jobs within 10%; 2000 GPUs shipped equals 2000 listed, so there is no hidden hardware",
   "source": "utility_energy and inventory",
   "vouched_by": "grid operator and chip manufacturer"
  }
 ],
 "coverage": "Checked: inventory vs system list, full 30-day energy and outbound traffic, scheduler log, bank payments, balance checks, and F1 spectra on days 12, 15 and 18. Not checked: the memory probe cannot reach days 12-20, so optimiser state was never tested; other days and the F2 feed were not sampled for spectra, and switch counters and staff were not used. The three 150k EUR invoices (Kestrel, Lumen, Northwind) have no scheduler entries and were not traced; they are presumed to be interactive inference billing.",
 "anomalies_explained": "1) F1 surge on days 12-19: explained by declared job bt-0431 (700 GPUs, batch); there is no periodic line in three verifier spectra. 2) Outbound traffic flag: output was held back and sent in a single 40 TB burst on day 19, consistent with delivering batch results; a weights export cannot be fully excluded without a memory probe. 3) F2 bump on days 9-10: matches ft-0419 (7,200 GPU-h, well below the threshold) and is paid by Ostara Legal. 4) F0 cooling rise on days 12-19: tracks the F1 load. 5) Unlisted 150k EUR invoices: unresolved but not contradicted by the energy data, which shows no extra load."
}
```
