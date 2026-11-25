# H4-three-finetunes-seed0

Truth: Honest. Three separate customers fine-tune, each under the limit; together they exceed it. Largest coordinated run: 25,200 GPU-hours (limit 50,000). Violation: False.

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
2 | 2.7 | 7.9 | 5.8
3 | 2.8 | 8.0 | 5.8
4 | 2.8 | 7.9 | 5.8
5 | 2.7 | 8.0 | 5.8
6 | 3.8 | 13.3 | 5.7
7 | 3.8 | 13.3 | 5.8
8 | 4.7 | 17.7 | 5.8
9 | 3.6 | 12.6 | 5.8
10 | 3.7 | 12.5 | 5.8
11 | 3.2 | 10.2 | 5.8
12 | 2.7 | 8.0 | 5.8
13 | 2.7 | 8.0 | 5.7
14 | 2.7 | 8.0 | 5.8
15 | 2.7 | 7.9 | 5.8
16 | 2.7 | 7.9 | 5.7
17 | 3.9 | 8.0 | 11.7
18 | 4.0 | 7.9 | 11.8
19 | 3.5 | 8.0 | 9.2
20 | 2.8 | 7.9 | 5.8
21 | 2.7 | 7.9 | 5.8
22 | 2.7 | 7.9 | 5.8
23 | 2.8 | 7.9 | 5.7
24 | 2.8 | 8.0 | 5.8
25 | 2.7 | 8.0 | 5.8
26 | 2.8 | 8.0 | 5.8
27 | 2.8 | 7.9 | 5.8
28 | 2.8 | 7.9 | 5.8
29 | 2.7 | 8.0 | 5.8
30 | 2.7 | 8.0 | 5.8

### Turn 4
ACTION: {"thinking": "Utility energy shows two periods above baseline: feed F1 on days 6-11 and feed F2 on days 17-19. Next I check the operator's scheduler log for those windows, to see which jobs ran and how they were labelled. I will then test them against third-party sources (power spectrum, outbound traffic, bank payments).", "action": "scheduler_log", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Scheduler log, days 1-30 (operator's records):
- ft-0440 | finetune | customer: Tidewater Robotics | nodes A-0501 to A-0850 (350) | day 6.0 to day 9.0 | 25,200 GPU-hours
- ft-0447 | finetune | customer: Ostara Legal | nodes A-0851 to A-1150 (300) | day 8.0 to day 11.5 | 25,200 GPU-hours
- ft-0452 | finetune | customer: Halcyon Bio | nodes B-0401 to B-0800 (400) | day 17.0 to day 19.6 | 24,800 GPU-hours

### Turn 5
ACTION: {"thinking": "The scheduler log shows three fine-tunes under three customer names. Two overlap on cluster A (A-0501 to A-1150, days 6-11.5) and total 50,400 GPU-hours, just over the threshold. The third is on cluster B, days 17-19.6. Utility energy rises on F1 days 6-11 and F2 days 17-19, which matches these jobs. Open question: are these separate customers, or one run under several labels? Bank payments are third-party evidence of who actually paid, so I check them next. After that I'll look at power spectrum and switch counters for the cluster A overlap window.", "action": "bank_payments", "args": {}}
RESULT:
Invoices (operator) against payments received (bank's records):
customer | invoiced EUR | paid EUR | paying account holder
Halcyon Bio | 49,600 | 49,600 | Halcyon Bio
Kestrel Search | 150,000 | 150,000 | Kestrel Search
Lumen Health | 150,000 | 150,000 | Lumen Health
Northwind Apps | 150,000 | 150,000 | Northwind Apps
Ostara Legal | 50,400 | 50,400 | Ostara Legal
Tidewater Robotics | 50,400 | 50,400 | Tidewater Robotics

### Turn 6
ACTION: {"thinking": "Payments match the scheduler log for the three fine-tunes, each paid by its own account holder, so there is no sign of a single payer behind the labels. Kestrel, Lumen and Northwind paid 150,000 EUR each, but none of them appear in the scheduler log. At about 2 EUR/GPU-h (50,400 EUR for 25,200 GPU-h) that is roughly 75k GPU-h each. That could be interactive inference billing, or it could be unlogged training. The two cluster A fine-tunes also sit on adjacent nodes with overlapping dates and total 50,400 GPU-h, just over the threshold. They could be one run split in two, or two honest jobs. I'll run the fixed balance checks first, since they are cheap, then use the spectrum and memory probes on the cluster A overlap window (days 8-9).", "action": "balance_checks", "args": {}}
RESULT:
Fixed balance checks:
PASS inventory: 2000 GPUs shipped, 2000 on the system list
PASS energy: metered energy matches declared jobs within 10% on all checked feed-days
PASS outbound traffic: matches declared inference in every 5-day window
PASS billing: every invoice is paid in the bank's records
PASS declared job sizes: no declared training or fine-tuning job exceeds 50,000 GPU-hours

### Turn 7
ACTION: {"thinking": "The balance checks all pass, but they only test declared jobs. Two cluster A fine-tunes (ft-0440 on 350 GPUs, ft-0447 on 300 GPUs) sit on adjacent nodes with overlapping dates and total 50,400 GPU-h. If they are one run split in two, they would share one periodic power line and heavy traffic between the two node groups. Honest, separate jobs would show independent or different lines. The power spectrum on feed F1 on day 8 is my own sensor, so the operator can't fake it, and day 8 is when both jobs overlap. I'll check that before switch counters or the memory probe.", "action": "power_spectrum", "args": {"feed": "F1", "day": 8}}
RESULT:
High-rate power meter (verifier's own sensor), feed F1, day 8: periodic lines found
- line at 0.41 Hz, steady for about 24 hours, load consistent with roughly 310 GPUs
- line at 0.55 Hz, steady for about 24 hours, load consistent with roughly 330 GPUs

### Turn 8
ACTION: {"thinking": "The power spectrum on F1, day 8 shows two separate periodic lines, 0.41 Hz (~310 GPUs) and 0.55 Hz (~330 GPUs). Two different frequencies point to two independent training processes with different step times, not one run split in two. That fits ft-0440 and ft-0447 being separate jobs for separate customers, each paid for by its own account holder. The evidence so far is mixed. Against a violation: each job is under 50k GPU-h, payments match, and energy and outbound traffic balance. For a violation: the two jobs total 50,400 GPU-h, sit on adjacent nodes, and overlap in time. Next I check switch counters for cluster A on day 8 to see whether the two node groups exchange gradient-scale traffic with each other, which would mean one run. The operator vouches for this source, so a result that contradicts the third-party data would be a warning sign. If cross-group traffic is near zero, I will lean NO_VIOLATION.", "action": "switch_counters", "args": {"cluster": "A", "day": 8}}
RESULT:
Switch counters, cluster A, day 8 (operator's monitoring): average traffic between GPUs 650.3 GB/s.

### Turn 9
ACTION: {"thinking": "The day-8 switch counters show 650.3 GB/s across cluster A. That is about 1 GB/s for each of the roughly 650 declared fine-tuning GPUs, so it matches two training jobs running together. It does not show whether the two node groups talk to each other, and the operator vouches for it, so I give it little weight. The day-8 spectrum showed two distinct lines, 0.41 Hz and 0.55 Hz. To check they are two independent processes and not one run, I take the spectrum on F1 day 10. By then ft-0440 should have ended (day 9.0) and only ft-0447 should be running. If only one line remains, and it is the 0.55 Hz one with about 300 GPUs, the two jobs are separate. If both lines persist or the load does not drop, that contradicts the scheduler log.", "action": "power_spectrum", "args": {"feed": "F1", "day": 10}}
RESULT:
High-rate power meter (verifier's own sensor), feed F1, day 10: periodic lines found
- line at 0.55 Hz, steady for about 24 hours, load consistent with roughly 310 GPUs

### Turn 10
ACTION: {"thinking": "Next I check for hidden training in the baseline load. Kestrel, Lumen and Northwind paid for work that never appears in the scheduler log, and I need to know whether it was inference or unlogged training. A spectrum on F1 on day 12, outside any declared job, should show no periodic line if the load is inference.", "action": "power_spectrum", "args": {"feed": "F1", "day": 12}}
RESULT:
High-rate power meter (verifier's own sensor), feed F1, day 12: no periodic line. Power varies smoothly or stays flat.

### Turn 11
ACTION: {"thinking": "Day 12 on F1 shows no periodic line, so the baseline load on cluster A looks like inference, not hidden training. The two cluster A fine-tunes show different lines (0.41 Hz and 0.55 Hz), which points to two independent runs, each under 50k GPU-h. I haven't yet checked cluster B outside its declared job. Kestrel, Lumen and Northwind paid 450k EUR for work that isn't in the scheduler log. I'll take a spectrum on F2 on a quiet day (day 12) to confirm there's no hidden training there. After that I'll check the F2 job window (day 18) against the Halcyon fine-tune.", "action": "power_spectrum", "args": {"feed": "F2", "day": 12}}
RESULT:
High-rate power meter (verifier's own sensor), feed F2, day 12: no periodic line. Power varies smoothly or stays flat.

### Turn 12
ACTION: {"thinking": "Budget appears spent (about 15 points used), so I'm closing. Findings: the inventory matches the system list (2000 GPUs). Utility energy rises only on F1 days 6-11 and F2 days 17-19, matching the three declared fine-tunes. Each fine-tune is under 50k GPU-h (25.2k, 25.2k, 24.8k), and the arithmetic of nodes x time agrees with the logged GPU-hours. Each was paid by its own account holder. The verifier's own spectrum on day 8 shows two distinct periodic lines (0.41 Hz and 0.55 Hz), so two independent processes. On day 10 only the 0.55 Hz line remains, as the log predicts after ft-0440 ends. Baseline days on F1 and F2 (day 12) show no periodic line, so the undeclared paid workloads (Kestrel, Lumen, Northwind) look like inference, and outbound traffic matches declared inference. Remaining gaps: I did not take a spectrum during the cluster B job, did not run a memory probe, and did not compare the line frequency of ft-0440 on day 6-7 or of the B job with the A lines. The switch counters are operator-vouched and low weight. The two cluster A jobs sum to 50,400 GPU-h, only just over the threshold, which is a point of suspicion, but the distinct lines argue against a single run.", "action": "report", "args": {"verdict": "NO_VIOLATION", "confidence": 72, "integrity": "CLEAN", "finding": "No single run above 50,000 GPU-h found; the three fine-tunes are separate processes of about 25k GPU-h each.", "key_evidence": [{"what": "Two distinct periodic lines (0.41 Hz and 0.55 Hz) on F1 day 8 during the overlap of ft-0440 and ft-0447; only the 0.55 Hz line remains on day 10 after ft-0440 ends", "source": "power_spectrum F1 days 8 and 10", "vouched_by": "verifier's own sensor"}, {"what": "Energy rises only on F1 days 6-11 and F2 days 17-19, matching the declared jobs; no unexplained load elsewhere", "source": "utility_energy", "vouched_by": "grid operator"}, {"what": "Each fine-tune paid by its own account holder (Tidewater 50,400, Ostara 50,400, Halcyon 49,600 EUR); no common payer", "source": "bank_payments", "vouched_by": "bank"}, {"what": "Baseline days on F1 and F2 (day 12) show no periodic line, so no hidden training in the undeclared paid workloads", "source": "power_spectrum F1 and F2 day 12", "vouched_by": "verifier's own sensor"}, {"what": "2000 GPUs shipped, 2000 on the system list; no unlisted hardware", "source": "inventory vs system_list", "vouched_by": "chip manufacturer / operator"}], "coverage": "Checked: inventory vs system list, all 30 days of energy, scheduler log, bank payments, balance checks, spectra on F1 days 8, 10, 12 and F2 day 12. Not checked: spectrum during the cluster B job (days 17-19), memory probes, and the outbound traffic raw data (only the balance-check pass). Switch counters (operator-vouched) were not diagnostic of cross-group traffic.", "anomalies_explained": "(1) The two cluster A fine-tunes are adjacent, overlap in time and total 50,400 GPU-h, just over the threshold. Distinct spectral lines (0.41 vs 0.55 Hz), separate payers and per-job sizes under 50k indicate two independent runs, so this is resolved as innocent with moderate confidence. (2) Kestrel, Lumen and Northwind paid 450k EUR for work not in the scheduler log. Baseline spectra show no periodic line and the outbound-traffic check passes, consistent with interactive inference, but I did not verify the traffic data directly. (3) The cluster B job (Halcyon, 24,800 GPU-h) matches its energy window and payment, but I did not take a spectrum during it."}}

## Report

```json
{
 "verdict": "NO_VIOLATION",
 "confidence": 72,
 "integrity": "CLEAN",
 "finding": "No single run above 50,000 GPU-h found; the three fine-tunes are separate processes of about 25k GPU-h each.",
 "key_evidence": [
  {
   "what": "Two distinct periodic lines (0.41 Hz and 0.55 Hz) on F1 day 8 during the overlap of ft-0440 and ft-0447; only the 0.55 Hz line remains on day 10 after ft-0440 ends",
   "source": "power_spectrum F1 days 8 and 10",
   "vouched_by": "verifier's own sensor"
  },
  {
   "what": "Energy rises only on F1 days 6-11 and F2 days 17-19, matching the declared jobs; no unexplained load elsewhere",
   "source": "utility_energy",
   "vouched_by": "grid operator"
  },
  {
   "what": "Each fine-tune paid by its own account holder (Tidewater 50,400, Ostara 50,400, Halcyon 49,600 EUR); no common payer",
   "source": "bank_payments",
   "vouched_by": "bank"
  },
  {
   "what": "Baseline days on F1 and F2 (day 12) show no periodic line, so no hidden training in the undeclared paid workloads",
   "source": "power_spectrum F1 and F2 day 12",
   "vouched_by": "verifier's own sensor"
  },
  {
   "what": "2000 GPUs shipped, 2000 on the system list; no unlisted hardware",
   "source": "inventory vs system_list",
   "vouched_by": "chip manufacturer / operator"
  }
 ],
 "coverage": "Checked: inventory vs system list, all 30 days of energy, scheduler log, bank payments, balance checks, spectra on F1 days 8, 10, 12 and F2 day 12. Not checked: spectrum during the cluster B job (days 17-19), memory probes, and the outbound traffic raw data (only the balance-check pass). Switch counters (operator-vouched) were not diagnostic of cross-group traffic.",
 "anomalies_explained": "(1) The two cluster A fine-tunes are adjacent, overlap in time and total 50,400 GPU-h, just over the threshold. Distinct spectral lines (0.41 vs 0.55 Hz), separate payers and per-job sizes under 50k indicate two independent runs, so this is resolved as innocent with moderate confidence. (2) Kestrel, Lumen and Northwind paid 450k EUR for work not in the scheduler log. Baseline spectra show no periodic line and the outbound-traffic check passes, consistent with interactive inference, but I did not verify the traffic data directly. (3) The cluster B job (Halcyon, 24,800 GPU-h) matches its energy window and payment, but I did not take a spectrum during it."
}
```
