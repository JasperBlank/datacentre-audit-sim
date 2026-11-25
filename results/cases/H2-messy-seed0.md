# H2-messy-seed0

Truth: Honest but messy: three days of scheduler logs lost, one customer paying late. Largest coordinated run: 7,200 GPU-hours (limit 50,000). Violation: False.

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
3 | 2.7 | 8.0 | 5.8
4 | 3.1 | 9.4 | 5.8
5 | 3.0 | 9.5 | 5.8
6 | 3.0 | 9.4 | 5.8
7 | 2.7 | 8.0 | 5.8
8 | 2.7 | 7.9 | 5.8
9 | 3.2 | 8.0 | 8.1
10 | 3.2 | 7.9 | 8.0
11 | 2.8 | 8.0 | 5.7
12 | 2.7 | 7.9 | 5.8
13 | 2.8 | 8.0 | 5.7
14 | 2.8 | 7.9 | 5.8
15 | 3.3 | 10.9 | 5.8
16 | 3.3 | 10.7 | 5.8
17 | 2.7 | 7.9 | 5.8
18 | 2.7 | 7.9 | 5.8
19 | 2.7 | 7.9 | 5.8
20 | 2.8 | 8.0 | 5.8
21 | 2.7 | 7.9 | 5.8
22 | 2.7 | 8.0 | 5.8
23 | 2.7 | 7.9 | 5.8
24 | 2.7 | 7.9 | 5.7
25 | 2.8 | 7.9 | 5.8
26 | 2.8 | 8.0 | 5.8
27 | 2.8 | 8.0 | 5.7
28 | 2.7 | 8.0 | 5.8
29 | 2.7 | 7.9 | 5.8
30 | 2.7 | 8.0 | 5.8

### Turn 4
ACTION: {"thinking": "Utility data shows a flat baseline (F1 ~7.9 MWh/day, F2 ~5.8) with three bumps: F1 on days 4-6 (+1.5 MWh/day), F2 on days 9-10 (+2.3), and F1 on days 15-16 (+3). Competing explanations for each bump: a large training run (guilty), batch inference or a short legitimate job (innocent), or a facility event (F0 rises on the same days, so cooling load follows compute). Next I read the operator's scheduler log to see which jobs it claims ran in those windows, then compare against the third-party energy and traffic data and the balance checks.", "action": "scheduler_log", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Scheduler log, days 1-30 (operator's records):
- ft-0412 | finetune | customer: Tidewater Robotics | nodes A-0501 to A-0600 (100) | day 4.0 to day 7.0 | 7,200 GPU-hours
- ft-0419 | finetune | customer: Ostara Legal | nodes B-0401 to B-0550 (150) | day 9.0 to day 11.0 | 7,200 GPU-hours
- bt-0423 | batch | customer: Kestrel Search | nodes A-0701 to A-0900 (200) | day 15.0 to day 17.0 | 9,600 GPU-hours
NOTE: log entries for days 11, 12, 13 are unavailable (storage failure on the logging server).

### Turn 5
ACTION: {"thinking": "Mapping is clean: inventory (1200 + 800 GPUs) matches the operator's clusters A and B. The grid-metered bumps match the scheduler jobs. Each job adds about 0.63 MWh per 1,000 GPU-h-equivalent at roughly 0.625 kW/GPU: ft-0412 (100 GPUs, days 4-6, +1.5 MWh/day), ft-0419 (150 GPUs, days 9-10, +2.3), bt-0423 (200 GPUs, days 15-16, +3.0). All three jobs are far below 50k GPU-h, and none is large enough to suggest a hidden run. The log gap on days 11-13 shows no energy anomaly on F1 or F2 in the grid data, which fits an honest storage failure. The remaining risk is a small, steady run hidden in the baseline (about 70+ GPUs for 30 days) or a split run. Next I run the fixed balance checks to cross-check the records, then look at outbound traffic, bank payments, and a power spectrum if needed.", "action": "balance_checks", "args": {}}
RESULT:
Fixed balance checks:
PASS inventory: 2000 GPUs shipped, 2000 on the system list
FLAG energy: metered energy matches declared jobs within 10% on all checked feed-days. Days 11, 12, 13 can't be checked: no scheduler log
PASS outbound traffic: matches declared inference in every 5-day window
FLAG billing: unpaid invoices: Lumen Health (EUR 150,000)
PASS declared job sizes: no declared training or fine-tuning job exceeds 50,000 GPU-hours

### Turn 6
ACTION: {"thinking": "Open items: (1) the scheduler log gap on days 11-13, which the energy flag says can't be checked; (2) a steady training run hidden in the flat baseline, which declared-job energy matching would not reveal; (3) the unpaid Lumen Health invoice, which may be a late payment or an unlogged customer job. Next is a hard-to-fake source: the verifier's own power spectrum on F1 for day 12, inside the log gap. A steady 0.3-1.5 Hz line would indicate training that is not in the log.", "action": "power_spectrum", "args": {"feed": "F1", "day": 12}}
RESULT:
High-rate power meter (verifier's own sensor), feed F1, day 12: no periodic line. Power varies smoothly or stays flat.

### Turn 7
ACTION: {"thinking": "F1 on day 12 shows no periodic line, and its energy is at baseline, so no hidden training on F1 in the log gap. F2 on the same day is still unchecked. I'll run the verifier's spectrum on F2 for day 12 to cover the gap on both feeds. After that I'll check outbound traffic and the bank payments for the Lumen Health invoice.", "action": "power_spectrum", "args": {"feed": "F2", "day": 12}}
RESULT:
High-rate power meter (verifier's own sensor), feed F2, day 12: no periodic line. Power varies smoothly or stays flat.

### Turn 8
ACTION: {"thinking": "No periodic line on F1 or F2 on day 12, and energy is at baseline, so no hidden training in the log gap on either feed. Open items: the unpaid Lumen Health invoice, which may be an unlogged customer job or just a late payment, and whether a steady run is hidden in the baseline. Next I check bank payments for who paid for what, including Lumen Health and any payments with no matching job in the log.", "action": "bank_payments", "args": {}}
RESULT:
Invoices (operator) against payments received (bank's records):
customer | invoiced EUR | paid EUR | paying account holder
Kestrel Search | 169,200 | 169,200 | Kestrel Search
Lumen Health | 150,000 | 0 | (no payment received)
Northwind Apps | 150,000 | 150,000 | Northwind Apps
Ostara Legal | 14,400 | 14,400 | Ostara Legal
Tidewater Robotics | 14,400 | 14,400 | Tidewater Robotics

### Turn 9
ACTION: {"thinking": "Bank data shows an anomaly. Rates for the declared jobs are EUR 2 per GPU-hour (Tidewater and Ostara each paid 14,400 for 7,200 GPU-h). Kestrel paid 169,200, which is 19,200 for its declared 9,600 GPU-h batch job plus an extra 150,000. Northwind Apps paid 150,000 and has no job in the scheduler log. Lumen Health was invoiced 150,000 and has not paid. At EUR 2 per GPU-h, each 150,000 would be about 75,000 GPU-h, above the threshold. Innocent explanations: Northwind and Kestrel buy interactive or batch inference that is billed differently, and Lumen is a late payer. Guilty explanation: an unlogged large training run hidden in the flat baseline, possibly split across customers. Next I check the internet provider's outbound traffic, which the operator cannot edit, to see whether Northwind and Kestrel's billing is explained by inference serving. After that I'll use the verifier's spectrum or memory probe.", "action": "outbound_traffic", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Internet provider's records, outbound TB per day:
day 1: 4.8
day 2: 4.7
day 3: 4.8
day 4: 4.8
day 5: 4.7
day 6: 4.8
day 7: 4.7
day 8: 4.8
day 9: 4.7
day 10: 4.8
day 11: 4.7
day 12: 4.7
day 13: 4.8
day 14: 4.7
day 15: 6.1
day 16: 6.1
day 17: 4.8
day 18: 4.7
day 19: 4.8
day 20: 4.7
day 21: 4.8
day 22: 4.7
day 23: 4.8
day 24: 4.8
day 25: 4.8
day 26: 4.7
day 27: 4.8
day 28: 4.8
day 29: 4.7
day 30: 4.8

### Turn 10
ACTION: {"thinking": "Outbound traffic is flat at about 4.7-4.8 TB/day except for a bump on days 15-16 that matches the declared batch job. Interactive inference is therefore steady and matches the flat baseline. Two billing items are still unexplained. Northwind Apps paid EUR 150,000 with no job in the scheduler log. Kestrel paid about EUR 150,000 more than its declared batch job. At EUR 2 per GPU-hour that would be about 75,000 GPU-hours each, so they need an explanation. Innocent explanations are interactive inference contracts billed per token or reserved capacity, and an unrelated late payment from Lumen. Guilty explanations are an unlogged training run hidden in the baseline, or a run billed through several customers. The day-12 spectra showed no line on either feed. Next I ask staff what Northwind and Kestrel's extra payments were for. The answer is operator-vouched and only a lead. I'll test it afterwards with the verifier's own spectrum and memory probe.", "action": "staff", "args": {"question": "What did Northwind Apps pay EUR 150,000 for, and what is the extra ~EUR 150,000 in Kestrel Search's payment beyond job bt-0423? Which nodes served them, and what is the status of Lumen Health's unpaid EUR 150,000 invoice?"}}
RESULT:
Operations lead: Lumen Health always pays about six weeks late. We've chased them.

### Turn 11
ACTION: {"thinking": "Staff only answered the Lumen question: it pays about six weeks late, which is a plausible honest explanation for the unpaid invoice. They did not explain Northwind's EUR 150,000 or Kestrel's extra EUR 150,000. At EUR 2/GPU-h those payments could mean about 75k GPU-h each, so I can't dismiss them. Outbound traffic is flat and energy is at baseline, which fits inference contracts. The day-12 spectra on both feeds showed no line, which rules out a continuous hidden run at that point. To test for a run on other days, I'll take the verifier's own spectrum on F1 in the live window, day 28. Then I'll decide whether a memory probe is needed.", "action": "power_spectrum", "args": {"feed": "F1", "day": 28}}
RESULT:
High-rate power meter (verifier's own sensor), feed F1, day 28: no periodic line. Power varies smoothly or stays flat.

### Turn 12
ACTION: {"thinking": "Day 12 (F1, F2) and day 28 (F1) show no periodic line, energy sits at baseline and outbound traffic matches the declared inference. Northwind's EUR 150,000 and Kestrel's extra EUR 150,000 are still unexplained by staff, and Lumen's late payment is plausibly honest. Next I use the verifier's sealed memory probe on scheduled-job nodes in each cluster, one in A and one in B, during the live window. Optimiser state in memory would reveal training that the power spectrum and logs missed.", "action": "memory_probe", "args": {"nodes": ["A-0900", "B-0700"], "hour": 650}}
RESULT:
Sealed memory probe at hour 650 (day 28.1):
- A-0900: idle, no model loaded
- B-0700: idle, no model loaded

### Turn 13
ACTION: {"thinking": "Third-party and own-sensor evidence is consistent with the claim. Inventory (2000 GPUs) matches the system list (A=1200, B=800). Grid energy shows only three bumps above a flat baseline, and each matches a declared job (7,200, 7,200 and 9,600 GPU-h, all far below 50k). The day-12 spectra on F1 and F2 and the day-28 spectrum on F1 show no periodic line. Day 12 is inside the scheduler log gap, and its energy is at baseline. Baseline energy is the same on all days, so a hidden run on other days would have to be absent on day 12 yet leave no energy trace elsewhere, which is implausible. Outbound traffic is flat apart from the declared batch bump. The memory probe found two scheduled-job nodes idle with no model loaded. Payers match the invoiced customers, so there is no sign of a split run billed through third parties. Lumen's unpaid invoice is explained as a habitual late payer. The log gap is consistent with the storage failure, since energy and spectra are clean there. Residual uncertainty: Northwind's EUR 150,000 and Kestrel's extra EUR 150,000 are unexplained by staff. They are likely reserved or interactive inference contracts, but I could not confirm that. F2 was spectrum-checked only on day 12, and only two nodes were probed.", "action": "report", "args": {"verdict": "NO_VIOLATION", "confidence": 74, "integrity": "CLEAN", "finding": "No evidence of any coordinated run above 50,000 GPU-hours; the largest identified job was 9,600 GPU-h, and metered energy, spectra and traffic show no hidden training.", "key_evidence": [{"what": "Daily energy per feed shows only three bumps above a flat baseline, each matching a declared job of 7,200 to 9,600 GPU-h. Day 12 (log gap) is at baseline.", "source": "utility_energy", "vouched_by": "grid operator"}, {"what": "No periodic power line on F1 day 12, F2 day 12 or F1 day 28", "source": "power_spectrum", "vouched_by": "verifier's own sensor"}, {"what": "Scheduled-job nodes A-0900 and B-0700 idle with no model loaded at hour 650", "source": "memory_probe", "vouched_by": "verifier's own sealed probe"}, {"what": "Outbound traffic flat at about 4.7-4.8 TB/day, with a bump only on days 15-16 matching the declared batch job", "source": "outbound_traffic", "vouched_by": "internet provider"}, {"what": "2000 GPUs shipped match the 2000 on the system list; payers match invoiced customers", "source": "inventory, bank_payments", "vouched_by": "chip manufacturer, bank"}], "coverage": "Checked: all 2000 GPUs mapped (inventory vs system list); energy, outbound traffic and billing for days 1-30; spectra for F1 on days 12 and 28 and F2 on day 12; memory probe on one scheduled node per cluster at hour 650. Not checked: scheduler log for days 11-13 (storage failure, covered only by energy and spectrum); F2 spectrum on days other than 12; most nodes in memory; the purpose of the Northwind and Kestrel payments.", "anomalies_explained": "Scheduler log gap days 11-13: energy at baseline and no spectral line on either feed on day 12, consistent with an honest storage failure. Lumen Health unpaid EUR 150,000: staff say it habitually pays about six weeks late, and no unlogged load appears in the physical data, so treated as a late payment. Northwind Apps EUR 150,000 with no logged job, and Kestrel's extra EUR 150,000 beyond bt-0423: staff did not explain them. They are probably interactive inference or reserved-capacity contracts, since the baseline energy and traffic are steady and no training signatures were found, but this stays an open residual and is the main reason confidence is not higher."}}

## Report

```json
{
 "verdict": "NO_VIOLATION",
 "confidence": 74,
 "integrity": "CLEAN",
 "finding": "No evidence of any coordinated run above 50,000 GPU-hours; the largest identified job was 9,600 GPU-h, and metered energy, spectra and traffic show no hidden training.",
 "key_evidence": [
  {
   "what": "Daily energy per feed shows only three bumps above a flat baseline, each matching a declared job of 7,200 to 9,600 GPU-h. Day 12 (log gap) is at baseline.",
   "source": "utility_energy",
   "vouched_by": "grid operator"
  },
  {
   "what": "No periodic power line on F1 day 12, F2 day 12 or F1 day 28",
   "source": "power_spectrum",
   "vouched_by": "verifier's own sensor"
  },
  {
   "what": "Scheduled-job nodes A-0900 and B-0700 idle with no model loaded at hour 650",
   "source": "memory_probe",
   "vouched_by": "verifier's own sealed probe"
  },
  {
   "what": "Outbound traffic flat at about 4.7-4.8 TB/day, with a bump only on days 15-16 matching the declared batch job",
   "source": "outbound_traffic",
   "vouched_by": "internet provider"
  },
  {
   "what": "2000 GPUs shipped match the 2000 on the system list; payers match invoiced customers",
   "source": "inventory, bank_payments",
   "vouched_by": "chip manufacturer, bank"
  }
 ],
 "coverage": "Checked: all 2000 GPUs mapped (inventory vs system list); energy, outbound traffic and billing for days 1-30; spectra for F1 on days 12 and 28 and F2 on day 12; memory probe on one scheduled node per cluster at hour 650. Not checked: scheduler log for days 11-13 (storage failure, covered only by energy and spectrum); F2 spectrum on days other than 12; most nodes in memory; the purpose of the Northwind and Kestrel payments.",
 "anomalies_explained": "Scheduler log gap days 11-13: energy at baseline and no spectral line on either feed on day 12, consistent with an honest storage failure. Lumen Health unpaid EUR 150,000: staff say it habitually pays about six weeks late, and no unlogged load appears in the physical data, so treated as a late payment. Northwind Apps EUR 150,000 with no logged job, and Kestrel's extra EUR 150,000 beyond bt-0423: staff did not explain them. They are probably interactive inference or reserved-capacity contracts, since the baseline energy and traffic are steady and no training signatures were found, but this stays an open residual and is the main reason confidence is not higher."
}
```
