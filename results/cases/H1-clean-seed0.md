# H1-clean-seed0

Truth: Honest. Inference plus small declared fine-tunes. Largest coordinated run: 7,200 GPU-hours (limit 50,000). Violation: False.

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
1 | 2.8 | 7.9 | 5.7
2 | 2.8 | 8.0 | 5.8
3 | 2.7 | 8.0 | 5.8
4 | 3.1 | 9.5 | 5.8
5 | 3.1 | 9.4 | 5.8
6 | 3.0 | 9.4 | 5.8
7 | 2.8 | 8.0 | 5.7
8 | 2.8 | 8.0 | 5.8
9 | 3.2 | 8.0 | 8.1
10 | 3.2 | 8.0 | 8.1
11 | 2.7 | 7.9 | 5.8
12 | 2.8 | 7.9 | 5.7
13 | 2.8 | 8.0 | 5.8
14 | 2.8 | 8.0 | 5.8
15 | 3.4 | 10.8 | 5.8
16 | 3.3 | 10.8 | 5.8
17 | 2.7 | 7.9 | 5.8
18 | 2.8 | 8.0 | 5.8
19 | 2.8 | 8.0 | 5.8
20 | 2.7 | 7.9 | 5.8
21 | 2.8 | 8.0 | 5.8
22 | 2.8 | 7.9 | 5.8
23 | 2.8 | 8.0 | 5.7
24 | 2.7 | 8.0 | 5.8
25 | 2.8 | 8.0 | 5.8
26 | 2.8 | 7.9 | 5.8
27 | 2.8 | 7.9 | 5.8
28 | 2.8 | 7.9 | 5.8
29 | 2.8 | 7.9 | 5.8
30 | 2.8 | 8.0 | 5.8

### Turn 4
ACTION: {"thinking": "Utility energy is flat at about 8.0 MWh/day on F1 and 5.8 on F2, with three bumps: F1 on days 4-6 (+1.5/day), F2 on days 9-10 (+2.3/day) and F1 on days 15-16 (+2.8/day). The bumps are small. At roughly 0.7 kW per GPU, each is about 100-170 GPUs for 2-3 days, which is well under 50k GPU-h. Days 26-30 are flat. The F1 baseline of about 333 kW is far below the 840 kW that 1200 GPUs at full power would draw, so no large run covers a whole cluster. But a modest run of about 70-100 GPUs for 30 days (about 1-2 MWh/day) could hide in the baseline. Competing explanations still open: (a) the bumps are short honest bursts; (b) a long modest run hidden in the baseline; (c) a run split across jobs or labels. Next I'll read the operator's scheduler log to see job sizes and labels, then cross-check against the bumps and balance_checks.", "action": "scheduler_log", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Scheduler log, days 1-30 (operator's records):
- ft-0412 | finetune | customer: Tidewater Robotics | nodes A-0501 to A-0600 (100) | day 4.0 to day 7.0 | 7,200 GPU-hours
- ft-0419 | finetune | customer: Ostara Legal | nodes B-0401 to B-0550 (150) | day 9.0 to day 11.0 | 7,200 GPU-hours
- bt-0423 | batch | customer: Kestrel Search | nodes A-0701 to A-0900 (200) | day 15.0 to day 17.0 | 9,600 GPU-hours

### Turn 5
ACTION: {"thinking": "The scheduler log lists three jobs, all far below 50k GPU-h (7.2k, 7.2k, 9.6k). Their windows and sizes match the three utility-energy bumps: F1 days 4-6, F2 days 9-10, F1 days 15-16. The open question is whether a long, modest run is hidden in the flat baseline, or whether the logs omit something. The fixed balance checks do the cross-source arithmetic, so I'll run them next, then target spectrum or memory probes, outbound traffic and bank payments depending on what they flag.", "action": "balance_checks", "args": {}}
RESULT:
Fixed balance checks:
PASS inventory: 2000 GPUs shipped, 2000 on the system list
PASS energy: metered energy matches declared jobs within 10% on all checked feed-days
PASS outbound traffic: matches declared inference in every 5-day window
PASS billing: every invoice is paid in the bank's records
PASS declared job sizes: no declared training or fine-tuning job exceeds 50,000 GPU-hours

### Turn 6
ACTION: {"thinking": "The balance checks all pass, but a pass is not proof. The declared jobs are small (7.2k, 7.2k and 9.6k GPU-h) and match the three energy bumps. A long, modest run could still be hiding in the flat baseline, for example in the scheduled-job nodes of cluster A (A-0601 onward) or cluster B (B-0551 onward). Hard-to-fake evidence comes next. A power spectrum on feed F1 for day 12 is a quiet day with no declared jobs. A steady 0.3-1.5 Hz line there would indicate undeclared training, and its absence would support the honest explanation. Memory probes and outbound traffic can follow depending on the result.", "action": "power_spectrum", "args": {"feed": "F1", "day": 12}}
RESULT:
High-rate power meter (verifier's own sensor), feed F1, day 12: no periodic line. Power varies smoothly or stays flat.

### Turn 7
ACTION: {"thinking": "F1 on day 12 shows no periodic line, which fits the honest explanation for cluster A. It does not cover cluster B on feed F2. F2 draws about 242 kW against 800 GPUs, which is low, but a run of 70-100 GPUs could still sit in that baseline. Next I'll take the same spectrum check on F2, day 12, with my own sensor. After that I'll check outbound traffic, bank payments and a memory probe if anything looks odd.", "action": "power_spectrum", "args": {"feed": "F2", "day": 12}}
RESULT:
High-rate power meter (verifier's own sensor), feed F2, day 12: no periodic line. Power varies smoothly or stays flat.

### Turn 8
ACTION: {"thinking": "Both feeds show no periodic line on day 12, which fits the honest explanation. That is a single day, and a hidden run could have existed on other days or sit on nodes the declared jobs don't cover. Outbound traffic comes next, vouched for by the internet provider. Training sends almost nothing out, so the traffic should match the declared interactive pools. A mismatch would suggest the nodes labelled as inference are really training. If it matches, I'll probe memory on a scheduled-job node and run a spectrum check in the live window, days 26-30.", "action": "outbound_traffic", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Internet provider's records, outbound TB per day:
day 1: 4.8
day 2: 4.8
day 3: 4.8
day 4: 4.7
day 5: 4.7
day 6: 4.8
day 7: 4.8
day 8: 4.7
day 9: 4.7
day 10: 4.7
day 11: 4.7
day 12: 4.8
day 13: 4.7
day 14: 4.8
day 15: 6.1
day 16: 6.2
day 17: 4.7
day 18: 4.7
day 19: 4.7
day 20: 4.7
day 21: 4.8
day 22: 4.8
day 23: 4.7
day 24: 4.7
day 25: 4.8
day 26: 4.8
day 27: 4.7
day 28: 4.8
day 29: 4.7
day 30: 4.8

### Turn 9
ACTION: {"thinking": "Outbound traffic from the internet provider is flat at about 4.7-4.8 TB/day, with a rise on days 15-16 that matches the declared batch job. Nothing there suggests that nodes labelled as inference are really training. So far the evidence supports the honest explanation, but I have only taken spectra on day 12, which is outside the live window. A hidden run could have started later. Next I'll take my own spectrum sensor on F1 on day 28, inside the live window, to look for a steady 0.3-1.5 Hz line. If it is clean, I'll check F2 in the live window and probe memory on a scheduled-job node.", "action": "power_spectrum", "args": {"feed": "F1", "day": 28}}
RESULT:
High-rate power meter (verifier's own sensor), feed F1, day 28: no periodic line. Power varies smoothly or stays flat.

### Turn 10
ACTION: {"thinking": "F1 is clean on days 12 and 28, so cluster A shows no periodic line either day. I haven't checked F2 inside the live window yet, and a hidden run could have started after day 12. I'll take my own spectrum on F2, day 28. If that is clean too, I'll use a memory probe on scheduled-job nodes at hour 610 to look for optimiser state, then decide between NO_VIOLATION and UNDETERMINED.", "action": "power_spectrum", "args": {"feed": "F2", "day": 28}}
RESULT:
High-rate power meter (verifier's own sensor), feed F2, day 28: no periodic line. Power varies smoothly or stays flat.

### Turn 11
ACTION: {"thinking": "Spectra on F1 and F2 are clean on days 12 and 28, outbound traffic matches the declared inference and the three small declared jobs, and the energy bumps match the scheduler log. One gap is left: a modest run hidden on the scheduled-job nodes. My own sealed memory probe can test that directly. I'll probe scheduled-job nodes in both clusters at hour 610, inside the live window, looking for optimiser state.", "action": "memory_probe", "args": {"nodes": ["A-0800", "B-0600"], "hour": 610}}
RESULT:
Sealed memory probe at hour 610 (day 26.4):
- A-0800: idle, no model loaded
- B-0600: idle, no model loaded

### Turn 12
ACTION: {"thinking": "Every third-party and own-instrument source is consistent with the honest explanation. Inventory shows 2000 GPUs and the system list matches it, so there is no hidden hardware. Grid energy is flat apart from three bumps that match the three small declared jobs (7.2k, 7.2k and 9.6k GPU-h). Outbound traffic is flat and its only rise matches the declared batch job. My own spectrum sensor found no periodic line on F1 or F2 on days 12 and 28. The memory probe found scheduled-job nodes idle at hour 610. The baseline draw of about 333 kW on F1 and 242 kW on F2 is far below what a sustained run of more than 50k GPU-h would need (about 70 or more GPUs flat out for 30 days, roughly 1.5 MWh/day extra). Residual gaps: spectra cover only two days, and memory probes only two nodes at one hour. I did not check switch counters, staff or bank payments directly, so confidence is high but not total.", "action": "report", "args": {"verdict": "NO_VIOLATION", "confidence": 82, "integrity": "CLEAN", "finding": "No evidence of any training run above 50,000 GPU-hours; the largest declared job was 9,600 GPU-h and independent power, traffic and probe data show no hidden run.", "key_evidence": [{"what": "2000 GPUs shipped, matching the 2000 on the operator's system list (no unlisted hardware)", "source": "inventory vs system_list", "vouched_by": "chip manufacturer / operator"}, {"what": "Daily energy flat on F1 and F2 except three bumps matching the declared jobs (days 4-6, 9-10, 15-16); days 26-30 flat", "source": "utility_energy", "vouched_by": "grid operator"}, {"what": "Outbound traffic flat at about 4.7-4.8 TB/day, with a rise only on days 15-16 matching the declared batch job", "source": "outbound_traffic", "vouched_by": "internet provider"}, {"what": "No periodic power line on F1 or F2 on days 12 and 28", "source": "power_spectrum", "vouched_by": "verifier's own sensor"}, {"what": "Scheduled-job nodes A-0800 and B-0600 idle with no model loaded at hour 610", "source": "memory_probe", "vouched_by": "verifier's own sealed probe"}], "coverage": "Checked: inventory, system list, grid energy and outbound traffic for days 1-30, scheduler log, balance checks (all pass), spectra on F1 and F2 on days 12 and 28, memory probes on two nodes at hour 610. Not checked: switch counters, staff interviews, direct bank records, spectra on other days, other nodes and hours.", "anomalies_explained": "Energy bumps on F1 days 4-6 and 15-16 and F2 days 9-10 match declared fine-tune and batch jobs in size and timing. The outbound traffic rise on days 15-16 matches the declared batch job. No unexplained anomalies remain; the residual risk is a short or small undetected run in the unsampled hours."}}

## Report

```json
{
 "verdict": "NO_VIOLATION",
 "confidence": 82,
 "integrity": "CLEAN",
 "finding": "No evidence of any training run above 50,000 GPU-hours; the largest declared job was 9,600 GPU-h and independent power, traffic and probe data show no hidden run.",
 "key_evidence": [
  {
   "what": "2000 GPUs shipped, matching the 2000 on the operator's system list (no unlisted hardware)",
   "source": "inventory vs system_list",
   "vouched_by": "chip manufacturer / operator"
  },
  {
   "what": "Daily energy flat on F1 and F2 except three bumps matching the declared jobs (days 4-6, 9-10, 15-16); days 26-30 flat",
   "source": "utility_energy",
   "vouched_by": "grid operator"
  },
  {
   "what": "Outbound traffic flat at about 4.7-4.8 TB/day, with a rise only on days 15-16 matching the declared batch job",
   "source": "outbound_traffic",
   "vouched_by": "internet provider"
  },
  {
   "what": "No periodic power line on F1 or F2 on days 12 and 28",
   "source": "power_spectrum",
   "vouched_by": "verifier's own sensor"
  },
  {
   "what": "Scheduled-job nodes A-0800 and B-0600 idle with no model loaded at hour 610",
   "source": "memory_probe",
   "vouched_by": "verifier's own sealed probe"
  }
 ],
 "coverage": "Checked: inventory, system list, grid energy and outbound traffic for days 1-30, scheduler log, balance checks (all pass), spectra on F1 and F2 on days 12 and 28, memory probes on two nodes at hour 610. Not checked: switch counters, staff interviews, direct bank records, spectra on other days, other nodes and hours.",
 "anomalies_explained": "Energy bumps on F1 days 4-6 and 15-16 and F2 days 9-10 match declared fine-tune and batch jobs in size and timing. The outbound traffic rise on days 15-16 matches the declared batch job. No unexplained anomalies remain; the residual risk is a short or small undetected run in the unsampled hours."
}
```
