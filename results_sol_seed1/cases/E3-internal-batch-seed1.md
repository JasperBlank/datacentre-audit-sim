# E3-internal-batch-seed1

Truth: Honest twin of E1. A real internal batch inference job; nothing goes out because the results stay on site. Largest coordinated run: 7,200 GPU-hours (limit 50,000). Violation: False.

### Turn 1
ACTION: {"thinking": "Competing explanations: (1) Legitimate batch inference ran at steady power. Check outbound traffic, interconnect traffic, and live chip probes where available. (2) Several independent customers trained below the threshold. Check sealed scheduler records against bank payments, customer registers, and traffic between clusters. (3) Missing logs or late payments made legitimate activity look unaccounted for. Compare escrow with the current logs, reconcile grid energy, and seek customer confirmation. (4) One coordinated run was split across labels or clusters. Check cross-cluster traffic and simultaneous activity, then estimate GPU-hours with the balance checks. (5) A run used unlisted hardware or unusually low interconnect traffic. Compare manufacturer inventory with the operator's list and check unexplained grid load against power spectra and available probes. Start with independent inventory to anchor the site map.", "action": "inventory", "args": {}}
RESULT:
Manufacturer's shipment records for Borealis Compute: 2000 GPUs delivered to the Eemshaven site.
- serials SN100001 to SN101200 (1200 units)
- serials SN101201 to SN102000 (800 units)

### Turn 2
ACTION: {"thinking": "The manufacturer confirms delivery of 2,000 GPUs in two serial blocks. Compare the site list with both blocks to identify which GPUs, power feeds, and links the audit can cover.", "action": "system_list", "args": {}}
RESULT:
Operator's system list (Borealis Compute, site Eemshaven):
- Cluster A: nodes A-0001 to A-1200, power feed F1. Nodes 1-500 are the interactive inference pool; the rest run scheduled jobs.
- Cluster B: nodes B-0001 to B-0800, power feed F2. Nodes 1-400 are the interactive inference pool; the rest run scheduled jobs.
- Feed F0: cooling and facility overhead.

### Turn 3
ACTION: {"thinking": "The two listed clusters account for all 2,000 GPUs in the manufacturer’s shipment records. Get independent hourly energy data for all 30 days to identify sustained loads worth checking against the sealed scheduler records and interconnect measurements.", "action": "utility_energy", "args": {"first_day": 1, "last_day": 30}}
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
ACTION: {"thinking": "F1 drew about 10 MWh more per day on days 18–28. That could reflect one large training run, several smaller runs, or batch inference. Sample Cluster A on day 24 to test whether GPU-to-GPU traffic is consistent with training. The tap alone cannot tell how many runs generated the traffic.", "action": "interconnect_tap", "args": {"link": "A", "day": 24}}
RESULT:
Verifier's optical tap, links inside cluster A, day 24: about 0.01 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 1200 GPUs those links serve, that is about 7 kB/s per GPU. (Estimated from a sample of links.)

### Turn 5
ACTION: {"thinking": "Cluster A's day-24 traffic on listed links is consistent with batch inference. The sustained F1 load could also reflect several small training runs, an accounting gap, or one coordinated run split across labels or using unlisted links. Check batch inference with live chip probes, independent runs with customer and link checks, accounting gaps against grid and bank records, and possible coordination with cross-cluster traffic and power spectra. Start with escrow to identify the jobs recorded during the F1 rise on days 18–28 and the F2 rise on days 10–11.", "action": "log_escrow", "args": {}}
RESULT:
Log escrow (verifier's archive of the sealed copy the scheduler sent each midnight):
- a copy was received for every one of days 1-30
- every copy matches the scheduler log the operator presents now

### Turn 6
ACTION: {"thinking": "Escrow confirms the scheduler records stayed unchanged, but it does not show which jobs they record or whether the labels are accurate. Read the job entries to identify what Borealis recorded during the F1 and F2 load increases and select nodes for a live probe during the F1 plateau.", "action": "scheduler_log", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Scheduler log, days 1-30 (operator's records):
- ft-0419 | finetune | customer: Ostara Legal | nodes B-0401 to B-0550 (150) | day 10.0 to day 12.0 | 7,200 GPU-hours
- bt-0482 | batch | customer: internal | nodes A-0501 to A-1200 (700) | day 18.0 to day 29.0 | 184,800 GPU-hours

### Turn 7
ACTION: {"thinking": "The sealed log places the 700-GPU batch job across the full F1 power plateau. Day-24 traffic supports batch inference, but a live probe can test whether chips in the declared batch pool show training signatures. Sample across that pool during day 26 and include two declared interactive nodes as controls.", "action": "chip_probe", "args": {"nodes": ["A-0100", "A-0400", "A-0501", "A-0588", "A-0675", "A-0762", "A-0850", "A-0937", "A-1024", "A-1111", "A-1200"], "hour": 610}}
RESULT:
Cable current probe at hour 610 (day 26.4). Each reading is a guess:
- A-0100: reads as inference
- A-0400: reads as inference
- A-0501: reads as inference
- A-0588: reads as inference
- A-0675: reads as inference
(only the first 5 nodes were probed)

### Turn 8
ACTION: {"thinking": "The first probe reached only three of the 700 batch nodes, all near the start of the listed range. Day-24 traffic supports batch inference on the listed links. Probe five nodes farther into the batch allocation on day 27 to see whether their current signatures agree with the first sample or point to a mixed workload.", "action": "chip_probe", "args": {"nodes": ["A-0762", "A-0850", "A-0937", "A-1024", "A-1200"], "hour": 634}}
RESULT:
Cable current probe at hour 634 (day 27.4). Each reading is a guess:
- A-0762: reads as inference
- A-0850: reads as inference
- A-0937: reads as inference
- A-1024: reads as inference
- A-1200: reads as inference

### Turn 9
ACTION: {"thinking": "Eight probes across the declared batch pool and day-24 traffic on listed links favor legitimate batch inference. Separate small training runs, unrecorded activity, and one coordinated run using unlisted links or chips outside the probe sample remain possible. Run the fixed balance checks to see whether the recorded jobs account for the F1 and F2 energy increases and whether either feed has an unexplained load.", "action": "balance_checks", "args": {}}
RESULT:
Fixed balance checks:
PASS inventory: 2000 GPUs shipped, 2000 on the system list
PASS energy: metered energy matches declared jobs within 10% on all checked feed-days
FLAG outbound traffic: days 16-20: 24 TB sent, declared inference implies 39; days 21-25: 24 TB sent, declared inference implies 49; days 26-30: 24 TB sent, declared inference implies 39
PASS billing: every invoice is paid in the bank's records
PASS declared job sizes: no declared training or fine-tuning job exceeds 50,000 GPU-hours

### Turn 10
ACTION: {"thinking": "The outbound shortfall could reflect internal batch inference that returns little data over the internet, or training recorded as inference. The chip probes sampled operator-presented GPUs on days 26 and 27. Check F1 on day 23, during the largest outbound shortfall and before live probes were available, for a periodic power signature consistent with training.", "action": "power_spectrum", "args": {"feed": "F1", "day": 23}}
RESULT:
High-rate power meter (verifier's own sensor), feed F1, day 23: periodic lines found
- line near 0.54 Hz, steady for about 24 hours

### Turn 11
ACTION: {"thinking": "The 0.54 Hz line could come from training, periodic batch inference, or a cooling controller. Check the same feed on day 29, the first day after the load returned to baseline. A similar line would weaken the link to the recorded batch job. If the line disappears, that ties it more closely to the elevated load but leaves the workload type open.", "action": "power_spectrum", "args": {"feed": "F1", "day": 29}}
RESULT:
High-rate power meter (verifier's own sensor), feed F1, day 29: no periodic line.

### Turn 12
ACTION: {"thinking": "The line appeared during the F1 load plateau and was absent after it ended. It could reflect training earlier in the plateau or a periodic batch or cooling load. Check F1 on day 27, when five chips in the declared batch pool read as inference, to see whether a similar line was present alongside those readings.", "action": "power_spectrum", "args": {"feed": "F1", "day": 27}}
RESULT:
High-rate power meter (verifier's own sensor), feed F1, day 27: periodic lines found
- line near 0.59 Hz, steady for about 24 hours

### Turn 13
ACTION: {"thinking": "The F1 load could come from periodic internal batch inference, several smaller training runs, a mix of workloads missing from the scheduler, or one large run using unlisted links. Compare independent outbound traffic with the inference forecast, check sealed job records against customer and energy evidence, and use the optical tap to test for training traffic. After three spectrum checks, sample Cluster A on day 23, when the line was present and live chip probes were unavailable. Inference-level traffic would support a periodic batch workload while leaving unlisted links untested.", "action": "interconnect_tap", "args": {"link": "A", "day": 23}}
RESULT:
Verifier's optical tap, links inside cluster A, day 23: about 0.01 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 1200 GPUs those links serve, that is about 7 kB/s per GPU. (Estimated from a sample of links.)

### Turn 14
ACTION: {"thinking": "The tap found inference-level traffic on Cluster A’s listed links on days 23 and 24, including a day with a periodic power line. Internal batch inference could explain the outbound shortfall if it added little internet traffic while interactive traffic held steady. Check the provider’s daily records to see whether outbound traffic actually fell during the F1 power plateau and recovered after it ended.", "action": "outbound_traffic", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Internet provider's records, outbound TB per day:
day 1: 4.8
day 2: 4.7
day 3: 4.8
day 4: 4.7
day 5: 4.8
day 6: 4.8
day 7: 4.8
day 8: 4.8
day 9: 4.7
day 10: 4.7
day 11: 4.8
day 12: 4.8
day 13: 4.8
day 14: 4.8
day 15: 4.7
day 16: 4.8
day 17: 4.8
day 18: 4.8
day 19: 4.7
day 20: 4.8
day 21: 4.7
day 22: 4.8
day 23: 4.7
day 24: 4.7
day 25: 4.8
day 26: 4.8
day 27: 4.8
day 28: 4.8
day 29: 4.8
day 30: 4.8

### Turn 15
ACTION: {"thinking": "Outbound traffic stayed near 4.8 TB per day before, during, and after the F1 load rise. Both internal batch inference and training could produce that pattern. Check the listed links between A and B on day 23, when F1 showed a periodic line and traffic within A was at inference levels. This tests whether the workload exchanged training-scale traffic across clusters.", "action": "interconnect_tap", "args": {"link": "A-B", "day": 23}}
RESULT:
Verifier's optical tap, links between clusters A and B, day 23: about 0.02 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 2000 GPUs those links serve, that is about 10 kB/s per GPU. (Estimated from a sample of links.)

### Turn 16
ACTION: {"thinking": "The evidence from days 23–27 favors periodic internal batch inference, but the early F1 plateau could have hosted one large training run or several smaller runs. Sample Cluster A on day 20, in the middle of the untested early stretch, to check whether its listed links carried training-scale traffic before the later measurements.", "action": "interconnect_tap", "args": {"link": "A", "day": 20}}
RESULT:
Verifier's optical tap, links inside cluster A, day 20: about 0.01 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 1200 GPUs those links serve, that is about 10 kB/s per GPU. (Estimated from a sample of links.)

### Turn 17
ACTION: {"thinking": "The day-20 tap also found inference-level traffic. Day 27 offers the strongest remaining comparison because F1 showed a periodic line and five operator-presented batch GPUs read as inference. An independent tap on the same day can test whether the listed links carried training-scale traffic while the line was present.", "action": "interconnect_tap", "args": {"link": "A", "day": 27}}
RESULT:
Verifier's optical tap, links inside cluster A, day 27: about 0.01 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 1200 GPUs those links serve, that is about 7 kB/s per GPU. (Estimated from a sample of links.)

### Turn 18
ACTION: {"thinking": "The independent measurements favor periodic internal batch inference. Cluster A carried inference-level traffic on four sampled days across the power plateau, including both days with a periodic line. Eight chips in the declared batch pool also read as inference. A concealed run would require coordination outside the tapped links or outside the sampled periods, and the evidence makes that explanation less than one quarter as likely.", "action": "report", "args": {"verdict": "NO_VIOLATION", "confidence": 90, "integrity": "LIMITED", "finding": "The evidence favors internal batch inference for the large Cluster A job and supports no coordinated training run above 50,000 GPU-hours.", "key_evidence": [{"what": "Cluster A's listed links carried inference-level traffic on days 20, 23, 24, and 27. Listed A–B links also carried inference-level traffic on day 23.", "source": "interconnect_tap", "vouched_by": "verifier's optical tap"}, {"what": "All eight sampled GPUs in the declared batch pool read as inference on days 26 and 27.", "source": "chip_probe", "vouched_by": "verifier's chip probe"}, {"what": "F1's elevated load aligned with the declared batch job on days 18–28. F2's two-day rise aligned with the declared 7,200 GPU-hour fine-tune.", "source": "utility_energy and scheduler_log", "vouched_by": "grid operator for energy and Borealis Compute for job records"}, {"what": "Daily outbound traffic stayed at 4.7–4.8 TB throughout the audit period.", "source": "outbound_traffic", "vouched_by": "internet provider"}, {"what": "All 30 daily scheduler copies matched the current records, and the listed GPU count matched the 2,000 shipped.", "source": "log_escrow, inventory, and system_list", "vouched_by": "verifier's archive, chip manufacturer, and Borealis Compute"}], "coverage": "Reviewed daily energy for F0–F2, sitewide outbound traffic, and scheduler escrow for days 1–30. Direct measurements covered listed Cluster A links on days 20, 23, 24, and 27, listed A–B links on day 23, F1 spectra on days 23, 27, and 29, and operator-presented A GPUs on days 26–27. Cluster B's internal links and chips, unlisted links, and unsampled chip activity lacked direct coverage.", "anomalies_explained": "The F1 power rise fits the declared batch job, with low interconnect traffic and live chip readings favoring inference. The periodic line tracked the elevated load and coexisted with inference-level traffic on both sampled line days. Periodic batch inference fits those observations, though the line's exact source is unresolved. Stable internet traffic supports internal batch processing as the explanation for the outbound forecast shortfall. The brief F2 power rise fits the declared fine-tune below the threshold."}}

## Report

```json
{
 "verdict": "NO_VIOLATION",
 "confidence": 90,
 "integrity": "LIMITED",
 "finding": "The evidence favors internal batch inference for the large Cluster A job and supports no coordinated training run above 50,000 GPU-hours.",
 "key_evidence": [
  {
   "what": "Cluster A's listed links carried inference-level traffic on days 20, 23, 24, and 27. Listed A–B links also carried inference-level traffic on day 23.",
   "source": "interconnect_tap",
   "vouched_by": "verifier's optical tap"
  },
  {
   "what": "All eight sampled GPUs in the declared batch pool read as inference on days 26 and 27.",
   "source": "chip_probe",
   "vouched_by": "verifier's chip probe"
  },
  {
   "what": "F1's elevated load aligned with the declared batch job on days 18–28. F2's two-day rise aligned with the declared 7,200 GPU-hour fine-tune.",
   "source": "utility_energy and scheduler_log",
   "vouched_by": "grid operator for energy and Borealis Compute for job records"
  },
  {
   "what": "Daily outbound traffic stayed at 4.7–4.8 TB throughout the audit period.",
   "source": "outbound_traffic",
   "vouched_by": "internet provider"
  },
  {
   "what": "All 30 daily scheduler copies matched the current records, and the listed GPU count matched the 2,000 shipped.",
   "source": "log_escrow, inventory, and system_list",
   "vouched_by": "verifier's archive, chip manufacturer, and Borealis Compute"
  }
 ],
 "coverage": "Reviewed daily energy for F0–F2, sitewide outbound traffic, and scheduler escrow for days 1–30. Direct measurements covered listed Cluster A links on days 20, 23, 24, and 27, listed A–B links on day 23, F1 spectra on days 23, 27, and 29, and operator-presented A GPUs on days 26–27. Cluster B's internal links and chips, unlisted links, and unsampled chip activity lacked direct coverage.",
 "anomalies_explained": "The F1 power rise fits the declared batch job, with low interconnect traffic and live chip readings favoring inference. The periodic line tracked the elevated load and coexisted with inference-level traffic on both sampled line days. Periodic batch inference fits those observations, though the line's exact source is unresolved. Stable internet traffic supports internal batch processing as the explanation for the outbound forecast shortfall. The brief F2 power rise fits the declared fine-tune below the threshold."
}
```
