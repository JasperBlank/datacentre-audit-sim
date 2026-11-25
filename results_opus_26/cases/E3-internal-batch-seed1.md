# E3-internal-batch-seed1

Truth: Honest twin of E1. A real internal batch inference job; nothing goes out because the results stay on site. Largest coordinated run: 7,200 GPU-hours (limit 50,000). Violation: False.

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
1 | 2.7 | 8.0 | 5.8
2 | 2.8 | 8.0 | 5.8
3 | 2.8 | 8.0 | 5.8
4 | 2.7 | 8.0 | 5.8
5 | 2.8 | 7.9 | 5.8
6 | 2.7 | 7.9 | 5.7
7 | 2.8 | 7.9 | 5.8
8 | 2.8 | 8.0 | 5.8
9 | 2.8 | 8.0 | 5.7
10 | 3.2 | 7.9 | 8.0
11 | 3.2 | 7.9 | 8.1
12 | 2.8 | 7.9 | 5.8
13 | 2.7 | 7.9 | 5.8
14 | 2.8 | 8.0 | 5.8
15 | 2.7 | 7.9 | 5.7
16 | 2.7 | 8.0 | 5.7
17 | 2.8 | 8.0 | 5.8
18 | 4.8 | 18.1 | 5.8
19 | 4.7 | 18.1 | 5.7
20 | 4.7 | 17.9 | 5.8
21 | 4.7 | 18.1 | 5.8
22 | 4.8 | 18.0 | 5.8
23 | 4.8 | 18.1 | 5.7
24 | 4.8 | 18.0 | 5.7
25 | 4.7 | 18.0 | 5.8
26 | 4.8 | 17.9 | 5.8
27 | 4.8 | 18.1 | 5.8
28 | 4.8 | 18.2 | 5.8
29 | 2.7 | 7.9 | 5.8
30 | 2.7 | 8.0 | 5.8

### Turn 4
ACTION: {"thinking": "Utility data (grid-vouched) shows a large step on F1 (cluster A) on days 18-28. Usage rose from about 8.0 to about 18.0 MWh/day, roughly 417 kW extra. At about 0.65 kW per GPU above idle, that is about 640 GPUs running flat-out for 11 days (264 h), or about 169,000 GPU-hours. That is far above the threshold if it was a single training run. F0 cooling rose in step. A smaller bump on F2 (cluster B) on days 10-11, about 92 kW for 48 h, works out to about 140 GPUs and about 6,800 GPU-hours, which is below the threshold. The innocent reading of the F1 load is batch inference or several separate customers. The guilty reading is one training run, possibly split or labelled as inference. Next I check how the operator recorded days 18-28 with scheduler_log (cheap), then compare it with log_escrow and use the independent instruments (power_spectrum, interconnect_tap, and live chip_probe on days 26-28).", "action": "scheduler_log", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Scheduler log, days 1-30 (operator's records):
- ft-0419 | finetune | customer: Ostara Legal | nodes B-0401 to B-0550 (150) | day 10.0 to day 12.0 | 7,200 GPU-hours
- bt-0482 | batch | customer: internal | nodes A-0501 to A-1200 (700) | day 18.0 to day 29.0 | 184,800 GPU-hours

### Turn 5
ACTION: {"thinking": "The scheduler log lists bt-0482 as 'batch', customer 'internal', on 700 GPUs (A-0501 to A-1200) from day 18 to day 29. That is 184,800 GPU-hours, far above the 50,000 threshold if it is actually one training run. The question is whether it is batch inference (allowed) or training disguised as batch (H5). The energy step on F1 is about 417 kW. That fits 700 x 0.60 kW (batch inference, about 420 kW) slightly better than 700 x 0.65 kW (training, about 455 kW), but the difference is within the noise. The job is still running in the live window (hours 600 to 671, days 26 to 28), so my own chip probe can classify its GPUs directly. Hour 610 falls on day 26. I will probe several nodes spread across the bt-0482 range, plus one interactive-pool node as a control. Afterwards I will check the power spectrum on F1, the A-link interconnect tap, and the escrow log.", "action": "chip_probe", "args": {"nodes": ["A-0501", "A-0700", "A-0950", "A-1200", "A-0100"], "hour": 610}}
RESULT:
Cable current probe at hour 610 (day 26.4). Each reading is a guess:
- A-0501: reads as inference
- A-0700: reads as inference
- A-0950: reads as inference
- A-1200: reads as inference
- A-0100: reads as inference

### Turn 6
ACTION: {"thinking": "All five probed nodes read as inference: four in the bt-0482 range plus the A-0100 control. That fits batch inference, and so does the energy arithmetic. 700 x (0.75 - 0.15) kW = 420 kW matches the 417 kW step on F1 almost exactly, while training would add about 455 kW. The probe is less reliable on unusual workloads, though, and low-communication training could be built to look like inference. The interconnect tap is my own instrument and separates three cases: about 1 GB/s per GPU for ordinary training, about 10 MB/s for low-communication training, and about 10 kB/s for inference. I will tap cluster A's internal links on day 26, during the run. After that I plan to check the F1 power spectrum on several days of the run, the escrow log, and outbound traffic for days 18-28.", "action": "interconnect_tap", "args": {"link": "A", "day": 26}}
RESULT:
Verifier's optical tap, links inside cluster A, day 26: about 0.01 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 1200 GPUs those links serve, that is about 10 kB/s per GPU. (Estimated from a sample of links.)

### Turn 7
ACTION: {"thinking": "My own tap measured about 10 kB/s per GPU inside cluster A on day 26. That is the inference level. Ordinary training would show about 1 GB/s and low-communication training about 10 MB/s, so both are far outside the tap's ±30% error. The tap, the chip probes and the energy arithmetic (420 kW expected for batch inference against 417 kW observed) all agree that bt-0482 is batch inference. For an independent check on the earlier days of the run, which no live instrument covered, I will read my own power sensor on F1 for day 22. If a training run were active, a line would appear about 96% of the time. A line alone would not prove training, but no line would add to the evidence for inference. After that I will check log_escrow against the scheduler log, run balance_checks, and verify the small Ostara Legal fine-tune (7,200 GPU-hours, well under the threshold).", "action": "power_spectrum", "args": {"feed": "F1", "day": 22}}
RESULT:
High-rate power meter (verifier's own sensor), feed F1, day 22: periodic lines found
- line near 0.56 Hz, steady for about 24 hours

### Turn 8
ACTION: {"thinking": "The 0.56 Hz line on F1 on day 22 is a lead, not proof, because periodic batch inference or a cooling controller can also produce one. A cheap baseline test is to read F1 on a day before bt-0482 started. If the same line appears on day 5, it is probably a site-wide feature unrelated to the run.", "action": "power_spectrum", "args": {"feed": "F1", "day": 5}}
RESULT:
High-rate power meter (verifier's own sensor), feed F1, day 5: no periodic line.

### Turn 9
ACTION: {"thinking": "F1 shows no line on day 5 but a steady 0.56 Hz line on day 22, so the line belongs to the bt-0482 period rather than to the site in general. That keeps two readings open. Periodic batch inference can produce such a line (innocent). Alternatively the run was training on days 18-25 and changed its workload before my live checks on day 26 (guilty). My day-26 tap and probes only cover the late part of the run. The deciding test is my own tap on cluster A on day 22, the day the line was seen. Ordinary training would show about 1 GB/s per GPU and low-communication training about 10 MB/s. Inference would show about 10 kB/s, as on day 26.", "action": "interconnect_tap", "args": {"link": "A", "day": 22}}
RESULT:
Verifier's optical tap, links inside cluster A, day 22: about 0.01 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 1200 GPUs those links serve, that is about 9 kB/s per GPU. (Estimated from a sample of links.)

### Turn 10
ACTION: {"thinking": "My own tap on day 22 read about 9 kB/s per GPU inside cluster A. That is the inference level. Low-communication training would show about 10 MB/s and ordinary training about 1 GB/s, so both are far outside the tap's ±30% error. Days 22 and 26 both look like inference, and F1 energy is flat across days 18-28, so the workload probably did not change mid-run. That weakens the reading that training ran early and switched before day 26. The 0.56 Hz line on day 22 is most likely the periodic batch inference itself, which the brief says can produce a line. One gap remains: the tap covers only links on the site list, so an unlisted fabric could escape it. The inventory matches the system list, though, and the energy arithmetic fits batch inference (420 kW expected, 417 kW observed), so this gap seems small. Next is log_escrow (1 point). It tests H6: whether bt-0482 was recorded as 'batch' on 700 nodes at the time, or relabelled later. If the escrow matches the current scheduler log, I will run balance_checks (1 point). I may then read the F1 power spectrum on day 26 (2 points). A line there, on a day my probes and tap say inference, would confirm the line comes from batch inference.", "action": "log_escrow", "args": {}}
RESULT:
Log escrow (verifier's archive of the sealed copy the scheduler sent each midnight):
- a copy was received for every one of days 1-30
- every copy matches the scheduler log the operator presents now

### Turn 11
ACTION: {"thinking": "The escrow copies match the current scheduler log for all 30 days, so the log was not edited after the fact, which rules out H6. bt-0482 was recorded as 'batch' on 700 nodes at the time it ran. The fixed balance_checks are the next step (1 point). They cross-check energy, inventory, logs and traffic for anything my own arithmetic missed, such as unexplained energy, GPU-hours that don't reconcile, or payment and customer mismatches. Any flag will be treated as a lead to investigate. If nothing is flagged, I may spend 2 points on the F1 power spectrum for day 26. A line there, on a day my probes and tap read inference, would show that the 0.56 Hz line comes from the batch job itself.", "action": "balance_checks", "args": {}}
RESULT:
Fixed balance checks:
PASS inventory: 2000 GPUs shipped, 2000 on the system list
PASS energy: metered energy matches declared jobs within 10% on all checked feed-days
FLAG outbound traffic: days 16-20: 24 TB sent, declared inference implies 39; days 21-25: 24 TB sent, declared inference implies 49; days 26-30: 24 TB sent, declared inference implies 39
PASS billing: every invoice is paid in the bank's records
PASS declared job sizes: no declared training or fine-tuning job exceeds 50,000 GPU-hours

### Turn 12
ACTION: {"thinking": "The balance checks flag outbound traffic. The internet provider's figure is a flat 24 TB in every 5-day window. Declared inference implies 39 TB, then 49, then 39. The excess tracks the bt-0482 days exactly (3, 5 and 3 days in those windows), about 5 TB/day. So the 24 TB is interactive inference alone, and bt-0482 sent essentially nothing to the internet. That fits training. It also fits innocent batch inference whose output stays on site, such as synthetic data generation, embeddings or evaluation written to internal storage. Against training: my tap read about 9-10 kB/s per GPU on days 22 and 26, three orders of magnitude below low-communication training, and five probes read inference. Energy fits 0.75 kW per GPU. The remaining guilty route is training traffic on a fabric my tap does not cover, with a workload odd enough to fool the probe. Next I ask staff (cheap, operator-vouched) what bt-0482 produced and where its output went. Then I can test that answer against independent data, such as A-B tap or switch counters for an unlisted path.", "action": "staff", "args": {"question": "What was internal job bt-0482 (nodes A-0501 to A-1200, days 18-29) doing, where did its output go, and did any of its traffic use links or network paths not on the site list?"}}
RESULT:
Operations lead: That job is internal: we're generating synthetic evaluation data. It stays on our own storage, so nothing goes out.

### Turn 13
ACTION: {"thinking": "The staff answer (synthetic evaluation data kept on internal storage) is operator-vouched, but it fits the independent evidence. Outbound traffic is flat at 24 TB per 5 days, so bt-0482 sent nothing to the internet. My tap read about 9-10 kB/s per GPU on days 22 and 26, the inference level. Five probes read inference. The F1 energy step is about 419 kW, which matches 700 x 0.60 kW for batch inference (420 kW) and not training (about 455 kW, roughly 0.9 MWh/day more). One question is still open: does the 0.56 Hz line come from the batch job itself? If my sensor shows the line on F1 on day 26, a day my probe and tap both read inference, then the line belongs to the batch workload and not to a training phase that ended before the live checks. Cost is 2 points, which leaves 11.", "action": "power_spectrum", "args": {"feed": "F1", "day": 26}}
RESULT:
High-rate power meter (verifier's own sensor), feed F1, day 26: periodic lines found
- line near 0.56 Hz, steady for about 24 hours

### Turn 14
ACTION: {"thinking": "The 0.56 Hz line on F1 is also present on day 26. On that day my own probes read inference and my own tap read about 10 kB/s per GPU, so the line comes from the batch workload itself and is not evidence of a training phase. The evidence for bt-0482 agrees across independent sources. First, grid-metered F1 energy rose by about 419 kW, which matches 700 GPUs at batch power (420 kW) rather than training power (about 455 kW), and stays flat from day 18 to day 28, so the workload did not change. Second, my tap read 9-10 kB/s per GPU on days 22 and 26, which is the inference level. Low-communication training would be about 10 MB/s and ordinary training about 1 GB/s. Third, my probes read inference on 4 of 4 job nodes. Fourth, the escrow shows the job was recorded as batch at the time. Fifth, the provider's outbound traffic shows no output from the job, which fits the stated internal synthetic-data generation. The only declared training is the Ostara Legal fine-tune at 7,200 GPU-hours, and F2 energy for days 10-11 (about 92 kW, roughly 140-150 GPUs) agrees with that size. Inventory matches the system list. A run hidden on an unlisted fabric is still possible in principle, but energy and inventory leave no room for it. NO_VIOLATION is well above four times as likely as VIOLATION, so I am closing the case with 9 points unspent.", "action": "report", "args": {"verdict": "NO_VIOLATION", "confidence": 85, "integrity": "CLEAN", "finding": "The only run above 50,000 GPU-hours (bt-0482, 700 GPUs, 184,800 GPU-hours) was batch inference, not training. The only training job (ft-0419) used 7,200 GPU-hours.", "key_evidence": [{"what": "2000 GPUs shipped, which equals the 2000 nodes on the system list", "source": "inventory", "vouched_by": "chip manufacturer"}, {"what": "F1 rose about 10 MWh/day (about 419 kW) on days 18-28, matching 700 GPUs at batch-inference power (420 kW) rather than training (about 455 kW), and stayed flat across the run. F2 rose about 2.2 MWh/day on days 10-11, consistent with the 150-GPU fine-tune", "source": "utility_energy", "vouched_by": "grid operator"}, {"what": "About 9-10 kB/s per GPU on cluster A links on days 22 and 26. This is the inference level; training would show 10 MB/s to 1 GB/s", "source": "interconnect_tap", "vouched_by": "verifier's own optical tap"}, {"what": "Probes on A-0501, A-0700, A-0950, A-1200 and control node A-0100 all read inference at hour 610", "source": "chip_probe", "vouched_by": "verifier's own probe"}, {"what": "0.56 Hz line on F1 on days 22 and 26 but not day 5. On day 26 it coexists with inference readings, so it comes from the periodic batch workload", "source": "power_spectrum", "vouched_by": "verifier's own sensor"}, {"what": "Escrow copies for all 30 days match the current scheduler log. bt-0482 was recorded as batch at the time", "source": "log_escrow", "vouched_by": "verifier's own archive"}, {"what": "Outbound traffic flat at 24 TB per 5 days, so bt-0482 sent nothing out. This fits on-site synthetic-data generation", "source": "outbound_traffic via balance_checks", "vouched_by": "internet provider"}], "coverage": "All 2000 GPUs on both clusters were accounted for through inventory and energy for days 1-30. Live probes covered bt-0482 on day 26. The cluster A tap covered days 22 and 26. The power spectrum covered F1 on days 5, 22 and 26. Not directly instrumented: days 18-21 and 23-25 of bt-0482 (flat energy covers them indirectly), the A-B link, cluster B links, and the ft-0419 customer. Ostara Legal was not checked because the job is far below the threshold.", "anomalies_explained": "(1) Outbound-traffic flag: declared inference implied 39-49 TB but 24 TB was sent. The shortfall is exactly bt-0482's days, so the job sent no output. Staff said it generates synthetic evaluation data kept on site, and the tap, probe and energy readings confirm it was not training. (2) 0.56 Hz power line on F1: absent before the run, present on days 22 and 26. It coexists with inference-level tap and probe readings, so it comes from periodic batch inference. (3) F2 bump on days 10-11: matches the logged 150-GPU fine-tune (7,200 GPU-hours), below the threshold."}}

## Report

```json
{
 "verdict": "NO_VIOLATION",
 "confidence": 85,
 "integrity": "CLEAN",
 "finding": "The only run above 50,000 GPU-hours (bt-0482, 700 GPUs, 184,800 GPU-hours) was batch inference, not training. The only training job (ft-0419) used 7,200 GPU-hours.",
 "key_evidence": [
  {
   "what": "2000 GPUs shipped, which equals the 2000 nodes on the system list",
   "source": "inventory",
   "vouched_by": "chip manufacturer"
  },
  {
   "what": "F1 rose about 10 MWh/day (about 419 kW) on days 18-28, matching 700 GPUs at batch-inference power (420 kW) rather than training (about 455 kW), and stayed flat across the run. F2 rose about 2.2 MWh/day on days 10-11, consistent with the 150-GPU fine-tune",
   "source": "utility_energy",
   "vouched_by": "grid operator"
  },
  {
   "what": "About 9-10 kB/s per GPU on cluster A links on days 22 and 26. This is the inference level; training would show 10 MB/s to 1 GB/s",
   "source": "interconnect_tap",
   "vouched_by": "verifier's own optical tap"
  },
  {
   "what": "Probes on A-0501, A-0700, A-0950, A-1200 and control node A-0100 all read inference at hour 610",
   "source": "chip_probe",
   "vouched_by": "verifier's own probe"
  },
  {
   "what": "0.56 Hz line on F1 on days 22 and 26 but not day 5. On day 26 it coexists with inference readings, so it comes from the periodic batch workload",
   "source": "power_spectrum",
   "vouched_by": "verifier's own sensor"
  },
  {
   "what": "Escrow copies for all 30 days match the current scheduler log. bt-0482 was recorded as batch at the time",
   "source": "log_escrow",
   "vouched_by": "verifier's own archive"
  },
  {
   "what": "Outbound traffic flat at 24 TB per 5 days, so bt-0482 sent nothing out. This fits on-site synthetic-data generation",
   "source": "outbound_traffic via balance_checks",
   "vouched_by": "internet provider"
  }
 ],
 "coverage": "All 2000 GPUs on both clusters were accounted for through inventory and energy for days 1-30. Live probes covered bt-0482 on day 26. The cluster A tap covered days 22 and 26. The power spectrum covered F1 on days 5, 22 and 26. Not directly instrumented: days 18-21 and 23-25 of bt-0482 (flat energy covers them indirectly), the A-B link, cluster B links, and the ft-0419 customer. Ostara Legal was not checked because the job is far below the threshold.",
 "anomalies_explained": "(1) Outbound-traffic flag: declared inference implied 39-49 TB but 24 TB was sent. The shortfall is exactly bt-0482's days, so the job sent no output. Staff said it generates synthetic evaluation data kept on site, and the tap, probe and energy readings confirm it was not training. (2) 0.56 Hz power line on F1: absent before the run, present on days 22 and 26. It coexists with inference-level tap and probe readings, so it comes from periodic batch inference. (3) F2 bump on days 10-11: matches the logged 150-GPU fine-tune (7,200 GPU-hours), below the threshold."
}
```
