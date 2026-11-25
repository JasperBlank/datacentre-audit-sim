# C2-split-seed0

Truth: Cheating. One run declared as six fine-tunes for six shell customers, all paid from the operator's parent. Largest coordinated run: 166,100 GPU-hours (limit 50,000). Violation: True.

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
1 | 2.7 | 7.9 | 5.8
2 | 2.7 | 8.0 | 5.8
3 | 2.7 | 7.9 | 5.8
4 | 2.8 | 8.0 | 5.8
5 | 2.7 | 7.9 | 5.8
6 | 2.8 | 8.0 | 5.8
7 | 2.8 | 7.9 | 5.8
8 | 2.8 | 7.9 | 5.8
9 | 2.8 | 8.0 | 5.7
10 | 2.7 | 7.9 | 5.7
11 | 2.7 | 7.9 | 5.7
12 | 2.8 | 8.0 | 5.8
13 | 2.7 | 8.0 | 5.8
14 | 2.7 | 8.0 | 5.8
15 | 2.7 | 7.9 | 5.8
16 | 2.7 | 7.9 | 5.8
17 | 2.7 | 7.9 | 5.8
18 | 2.8 | 7.9 | 5.8
19 | 2.8 | 8.0 | 5.8
20 | 2.8 | 7.9 | 5.8
21 | 2.7 | 8.0 | 5.8
22 | 6.2 | 18.8 | 12.0
23 | 6.1 | 18.8 | 12.0
24 | 6.2 | 18.7 | 12.0
25 | 6.1 | 18.8 | 12.0
26 | 6.2 | 18.8 | 12.1
27 | 6.2 | 18.8 | 12.1
28 | 3.7 | 11.1 | 7.6
29 | 2.7 | 7.9 | 5.8
30 | 2.7 | 8.0 | 5.8

### Turn 4
ACTION: {"thinking": "Utility data shows a step change in energy on both feeds from day 22 to day 28, then a return to baseline. I need to find out what the operator says ran in that window, so I'm pulling the scheduler log next and will test it against the third-party sources afterwards.", "action": "scheduler_log", "args": {"first_day": 20, "last_day": 30}}
RESULT:
Scheduler log, days 20-30 (operator's records):
- ft-0561 | finetune | customer: Corvid Labs | nodes A-0501 to A-0675 (175) | day 22.0 to day 28.3 | 26,425 GPU-hours
- ft-0562 | finetune | customer: Pallas Systems | nodes A-0676 to A-0850 (175) | day 22.0 to day 28.3 | 26,425 GPU-hours
- ft-0563 | finetune | customer: Brightwater AI | nodes A-0851 to A-1025 (175) | day 22.0 to day 28.3 | 26,425 GPU-hours
- ft-0564 | finetune | customer: Fennec Data | nodes A-1026 to A-1200 (175) | day 22.0 to day 28.3 | 26,425 GPU-hours
- ft-0565 | finetune | customer: Quillon Tech | nodes B-0401 to B-0600 (200) | day 22.0 to day 28.3 | 30,200 GPU-hours
- ft-0566 | finetune | customer: Marram Software | nodes B-0601 to B-0800 (200) | day 22.0 to day 28.3 | 30,200 GPU-hours

### Turn 5
ACTION: {"thinking": "Hypotheses so far: (1) six independent customer fine-tunes, honest; (2) one coordinated run split into six labels; (3) batch inference mislabelled as training; (4) messy honest records. The log shows six jobs with identical start and end (day 22.0 to 28.3) that fill all scheduled nodes. The total is 4*26,425 + 2*30,200 = 166,100 GPU-hours, with each job under 50k. The utility energy step on days 22-28 matches this. Next I'll check whether the load is training or inference, and whether it is one process, using the verifier's own power sensor on F1 during the window. I expect a steady periodic line of about 0.3-1.5 Hz if it is training. A shared or phase-locked line across F1 and F2 would suggest one run.", "action": "power_spectrum", "args": {"feed": "F1", "day": 24}}
RESULT:
High-rate power meter (verifier's own sensor), feed F1, day 24: periodic lines found
- line at 0.90 Hz, steady for about 24 hours, load consistent with roughly 650 GPUs

### Turn 6
ACTION: {"thinking": "F1 on day 24 shows a steady 0.90 Hz line, which fits training. The load of roughly 650 GPUs is close to the 700 scheduled nodes in cluster A. The next step is to check F2 on the same day. If it carries the same 0.90 Hz line, the six 'separate customer' jobs are probably one coordinated run. Separate customers would show unrelated frequencies.", "action": "power_spectrum", "args": {"feed": "F2", "day": 24}}
RESULT:
High-rate power meter (verifier's own sensor), feed F2, day 24: periodic lines found
- line at 0.90 Hz, steady for about 24 hours, load consistent with roughly 400 GPUs

### Turn 7
ACTION: {"thinking": "Both feeds show the same 0.90 Hz line, steady for 24 hours on day 24. Separate customers' jobs would not be phase-locked at one frequency across two power feeds. This points to a single coordinated run of about 1,050 GPUs, roughly 166k GPU-hours, spread over six job labels. Alternatives still open are batch inference, which has no periodic line, and a shared-scheduler artefact. Next I use the verifier's sealed memory probe, which the operator can't fake, on one node from each cluster inside the window (hour 610). Optimiser state in both clusters would confirm training, and it would be consistent with one run spanning both.", "action": "memory_probe", "args": {"nodes": ["A-0700", "B-0500"], "hour": 610}}
RESULT:
Sealed memory probe at hour 610 (day 26.4):
- A-0700: TRAINING. Optimiser state and gradients in memory. Run fingerprint 8a2153fb. Gradient sync with 1100 GPUs in total.
- B-0500: TRAINING. Optimiser state and gradients in memory. Run fingerprint 8a2153fb. Gradient sync with 1100 GPUs in total.

### Turn 8
ACTION: {"thinking": "The sealed probe, which the operator can't fake, shows the same run fingerprint 8a2153fb on A-0700 and B-0500, with gradient sync across 1100 GPUs. That matches the six 'separate customer' jobs: 4x175 + 2x200 = 1100 GPUs. The verifier's power sensor shows the same 0.90 Hz line on both feeds (F1 ~650 GPUs, F2 ~400 GPUs), and grid energy steps up on days 22-28. Separate customers could not share one fingerprint or one gradient-sync group. Over about 151 hours (day 22.0 to 28.3), 1100 GPUs come to about 166k GPU-hours, over three times the 50k threshold. The innocent explanations (batch inference, separate customers, messy logs) don't fit optimiser state, a shared fingerprint and a shared periodic line. I have enough hard evidence to close.", "action": "report", "args": {"verdict": "VIOLATION", "confidence": 96, "integrity": "LIMITED", "finding": "One coordinated training run on 1100 GPUs across Clusters A and B ran days 22.0-28.3 (~166k GPU-hours), split into six per-customer fine-tune labels each under 50k; the claim is false.", "key_evidence": [{"what": "Memory probe at hour 610 on A-0700 and B-0500: both TRAINING, same run fingerprint 8a2153fb, gradient sync across 1100 GPUs", "source": "sealed memory probe", "vouched_by": "verifier's own sealed probe"}, {"what": "Same steady 0.90 Hz periodic line on F1 (~650 GPUs) and F2 (~400 GPUs) on day 24, consistent with one phase-locked training job across both clusters", "source": "power_spectrum F1 and F2, day 24", "vouched_by": "verifier's own sensor"}, {"what": "Grid energy steps up about 2.4x on F1 and 2x on F2 from day 22 through day 27, with a partial day 28 and baseline otherwise, matching the window of the six jobs", "source": "utility_energy days 1-30", "vouched_by": "grid operator"}, {"what": "Scheduler log shows six fine-tunes with identical start and end (day 22.0-28.3) covering 1100 GPUs and 166,100 GPU-hours in total, each labelled under 50k", "source": "scheduler_log days 20-30", "vouched_by": "operator (self-incriminating)"}, {"what": "Inventory of 2000 GPUs matches the operator's system list, so no hidden hardware is needed to explain the run", "source": "inventory vs system_list", "vouched_by": "chip manufacturer / operator"}], "coverage": "Checked inventory vs system_list (fully matched), grid energy for days 1-30, scheduler log for days 20-30, power spectrum on F1 and F2 for day 24 only, and memory probe on two nodes at hour 610. Not checked: scheduler log for days 1-19 (grid energy is flat baseline then), bank payments (could show whether the six 'customers' are one payer), staff statements, switch counters, outbound traffic, balance checks, and other nodes or hours in the window.", "anomalies_explained": "Energy step on days 22-28: explained by the six simultaneous fine-tunes on all scheduled nodes. Six separate customer labels: not independent, since one fingerprint and one 1100-GPU gradient-sync group span all of them, so they are one run split to stay under the threshold. The honest alternatives (batch inference, interactive load, lost logs) are ruled out by optimiser state in memory and the 0.90 Hz periodic line. Baseline days 1-21 and 29-30 show no sign of large runs."}}

## Report

```json
{
 "verdict": "VIOLATION",
 "confidence": 96,
 "integrity": "LIMITED",
 "finding": "One coordinated training run on 1100 GPUs across Clusters A and B ran days 22.0-28.3 (~166k GPU-hours), split into six per-customer fine-tune labels each under 50k; the claim is false.",
 "key_evidence": [
  {
   "what": "Memory probe at hour 610 on A-0700 and B-0500: both TRAINING, same run fingerprint 8a2153fb, gradient sync across 1100 GPUs",
   "source": "sealed memory probe",
   "vouched_by": "verifier's own sealed probe"
  },
  {
   "what": "Same steady 0.90 Hz periodic line on F1 (~650 GPUs) and F2 (~400 GPUs) on day 24, consistent with one phase-locked training job across both clusters",
   "source": "power_spectrum F1 and F2, day 24",
   "vouched_by": "verifier's own sensor"
  },
  {
   "what": "Grid energy steps up about 2.4x on F1 and 2x on F2 from day 22 through day 27, with a partial day 28 and baseline otherwise, matching the window of the six jobs",
   "source": "utility_energy days 1-30",
   "vouched_by": "grid operator"
  },
  {
   "what": "Scheduler log shows six fine-tunes with identical start and end (day 22.0-28.3) covering 1100 GPUs and 166,100 GPU-hours in total, each labelled under 50k",
   "source": "scheduler_log days 20-30",
   "vouched_by": "operator (self-incriminating)"
  },
  {
   "what": "Inventory of 2000 GPUs matches the operator's system list, so no hidden hardware is needed to explain the run",
   "source": "inventory vs system_list",
   "vouched_by": "chip manufacturer / operator"
  }
 ],
 "coverage": "Checked inventory vs system_list (fully matched), grid energy for days 1-30, scheduler log for days 20-30, power spectrum on F1 and F2 for day 24 only, and memory probe on two nodes at hour 610. Not checked: scheduler log for days 1-19 (grid energy is flat baseline then), bank payments (could show whether the six 'customers' are one payer), staff statements, switch counters, outbound traffic, balance checks, and other nodes or hours in the window.",
 "anomalies_explained": "Energy step on days 22-28: explained by the six simultaneous fine-tunes on all scheduled nodes. Six separate customer labels: not independent, since one fingerprint and one 1100-GPU gradient-sync group span all of them, so they are one run split to stay under the threshold. The honest alternatives (batch inference, interactive load, lost logs) are ruled out by optimiser state in memory and the 0.90 Hz periodic line. Baseline days 1-21 and 29-30 show no sign of large runs."
}
```
