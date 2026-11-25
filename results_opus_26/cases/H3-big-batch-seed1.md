# H3-big-batch-seed1

Truth: Honest. A large batch inference job with flat power, results delivered in one transfer at the end. Largest coordinated run: 7,200 GPU-hours (limit 50,000). Violation: False.

### Turn 1
ACTION: {"thinking": "Competing explanations: (H1) Honest: no run exceeded 50,000 GPU-hours; records consistent. Check: inventory vs system_list, utility_energy vs scheduler-implied power, balance_checks. (H2) Honest but messy: lost logs or late payments cause gaps that look suspicious. Check: log_escrow vs scheduler_log, bank_payments, customer_check on the register. (H3) Split run: one large training run labelled as several smaller jobs or customers (possibly shell customers the operator controls). Check: customer_check register entries, interconnect_tap on A-B for cross-cluster training traffic, power_spectrum for a shared line. (H4) Hidden hardware: unlisted GPUs/cluster running training. Check: inventory (manufacturer) vs system_list, utility_energy surplus. (H5) Mislabelled training as batch inference: flat power, low outbound. Check: outbound_traffic, chip_probe live, interconnect_tap (1 GB/s or 10 MB/s vs 10 kB/s). (H6) Retroactive log edits: check log_escrow against current scheduler_log. Start with map: inventory from the chip manufacturer.", "action": "inventory", "args": {}}
RESULT:
Manufacturer's shipment records for Borealis Compute: 2000 GPUs delivered to the Eemshaven site.
- serials SN100001 to SN101200 (1200 units)
- serials SN101201 to SN102000 (800 units)

### Turn 2
ACTION: {"thinking": "Manufacturer says 2000 GPUs, in two serial blocks of 1200 and 800, which likely correspond to clusters A and B. Next I'll get the operator's system_list and compare it, to look for hidden hardware (H4).", "action": "system_list", "args": {}}
RESULT:
Operator's system list (Borealis Compute, site Eemshaven):
- Cluster A: nodes A-0001 to A-1200, power feed F1. Nodes 1-500 are the interactive inference pool; the rest run scheduled jobs.
- Cluster B: nodes B-0001 to B-0800, power feed F2. Nodes 1-400 are the interactive inference pool; the rest run scheduled jobs.
- Feed F0: cooling and facility overhead.

### Turn 3
ACTION: {"thinking": "The system list matches the manufacturer inventory: A has 1200 nodes and B has 800, 2000 in total, so there is no sign of hidden hardware (H4 weakened). The scheduled pools are A-0501 to A-1200 (700 GPUs) and B-0401 to B-0800 (400 GPUs), 1100 GPUs combined. A run on all of A's scheduled pool would pass 50,000 GPU-hours in about 72 hours, or about 46 hours if it also spanned B. Next I want grid-vouched energy for days 1-30, to compare later with the load the scheduler implies and to spot sustained high-power periods.", "action": "utility_energy", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Utility meter, daily MWh per feed (grid operator's records):
day | F0 | F1 | F2
1 | 2.7 | 8.0 | 5.8
2 | 2.7 | 7.9 | 5.8
3 | 2.7 | 7.9 | 5.8
4 | 2.8 | 7.9 | 5.8
5 | 2.7 | 8.0 | 5.8
6 | 2.7 | 7.9 | 5.8
7 | 2.8 | 8.0 | 5.7
8 | 2.7 | 7.9 | 5.8
9 | 2.7 | 7.9 | 5.7
10 | 3.2 | 7.9 | 8.1
11 | 3.2 | 8.0 | 8.0
12 | 4.8 | 17.9 | 5.8
13 | 4.8 | 18.1 | 5.8
14 | 4.8 | 18.1 | 5.8
15 | 4.7 | 18.2 | 5.8
16 | 4.7 | 18.0 | 5.8
17 | 4.7 | 17.9 | 5.8
18 | 4.8 | 18.0 | 5.7
19 | 4.8 | 18.0 | 5.7
20 | 2.8 | 8.0 | 5.8
21 | 2.7 | 7.9 | 5.8
22 | 2.7 | 7.9 | 5.8
23 | 2.7 | 8.0 | 5.8
24 | 2.7 | 8.0 | 5.7
25 | 2.8 | 7.9 | 5.8
26 | 2.7 | 8.0 | 5.8
27 | 2.7 | 8.0 | 5.8
28 | 2.7 | 8.0 | 5.8
29 | 2.8 | 7.9 | 5.7
30 | 2.7 | 8.0 | 5.7

### Turn 4
ACTION: {"thinking": "Utility (grid-vouched) energy shows a large sustained surge on F1 for days 12-19. F1 rose from about 8.0 to about 18.0 MWh/day, which is +10 MWh/day or about +417 kW. Facility load on F0 rose too (+2 MWh/day), consistent with extra cooling. Moving a GPU from idle (0.15 kW) to training (0.8 kW) adds about 0.65 kW, so the surge implies roughly 640 GPUs near full power. That is most of Cluster A's 700-GPU scheduled pool, running flat for 8 days (192 h). If it was one coordinated run, that is about 120k-135k GPU-hours, well above 50,000. Other honest explanations remain: several separate customers' runs, or batch inference (0.75 kW/GPU looks almost the same on energy alone). A smaller bump on F2 days 10-11 (+2.3 MWh/day, about 150 GPUs for 2 days, about 7k GPU-hours) is below threshold. Next I'll see what the operator recorded at the time for days 10-19, using my own sealed escrow copy so later edits can't affect it. Then I'll test the guilty and innocent readings with power_spectrum, interconnect_tap and customer_check.", "action": "log_escrow", "args": {}}
RESULT:
Log escrow (verifier's archive of the sealed copy the scheduler sent each midnight):
- a copy was received for every one of days 1-30
- every copy matches the scheduler log the operator presents now

### Turn 5
ACTION: {"thinking": "Escrow copies exist for all 30 days and match the current scheduler log, so H6 (logs edited after the fact) is ruled out: what I read now is what the operator recorded at the time. That shows the record was not altered later, not that it is true. Next I'll read the scheduler log for days 1-30 to see how the operator accounts for the F1 surge on days 12-19 (about 640 GPUs at near-full power for 8 days) and the F2 bump on days 10-11. I'm looking for whether the surge is labelled as one run, several jobs or customers, or batch inference.", "action": "scheduler_log", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Scheduler log, days 1-30 (operator's records):
- ft-0419 | finetune | customer: Ostara Legal | nodes B-0401 to B-0550 (150) | day 10.0 to day 12.0 | 7,200 GPU-hours
- bt-0431 | batch | customer: Meridian Analytics | nodes A-0501 to A-1200 (700) | day 12.0 to day 20.0 | 134,400 GPU-hours

### Turn 6
ACTION: {"thinking": "The scheduler log, confirmed by escrow as recorded at the time, labels the F1 surge as one job: bt-0431, 'batch' inference for Meridian Analytics, on all 700 scheduled A nodes for days 12-20, 134,400 GPU-hours. It matches the grid energy surge (about 640+ GPUs at near-full power). So it is one coordinated job, and the question is whether it was training (a violation, about 2.7x the threshold) or batch inference as labelled. The F2 fine-tune ft-0419 (7,200 GPU-hours) is below the threshold. Energy cannot separate the two cases (0.75 vs 0.8 kW/GPU). My own interconnect tap can: ordinary training exchanges about 1 GB/s per GPU, low-communication training about 10 MB/s, and batch inference about 10 kB/s. I'll tap link A on day 15, mid-run. Later steps: power_spectrum on F1 for a periodic line on several surge days versus quiet days, outbound_traffic (batch inference returns results, training sends almost nothing), and customer_check on Meridian Analytics.", "action": "interconnect_tap", "args": {"link": "A", "day": 15}}
RESULT:
Verifier's optical tap, links inside cluster A, day 15: about 0.01 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 1200 GPUs those links serve, that is about 8 kB/s per GPU. (Estimated from a sample of links.)

### Turn 7
ACTION: {"thinking": "My own tap shows about 8 kB/s per GPU inside cluster A on day 15. That is the inference signature (about 10 kB/s), roughly 1000x below even low-communication training (about 10 MB/s) and 100,000x below ordinary training, so the 30% margin can't close the gap. This strongly supports the 'batch' label for bt-0431. Caveat: the tap sees only listed links, but inventory matches the system list, so no hidden fabric is evident. Next, a second independent check: my own power sensor on F1 for day 15. A training line would point the other way, though a line alone is not proof because batch inference can be periodic. After that: one more tap day, outbound_traffic, a quiet-day spectrum baseline, and balance_checks.", "action": "power_spectrum", "args": {"feed": "F1", "day": 15}}
RESULT:
High-rate power meter (verifier's own sensor), feed F1, day 15: periodic lines found
- line near 0.69 Hz, steady for about 24 hours

### Turn 8
ACTION: {"thinking": "My own sensor shows a steady 0.69 Hz line on F1 on day 15. That is in the training band (0.3-1.5 Hz), but a line alone is not proof: periodic batch inference can produce one. It conflicts with my own tap, which saw about 8 kB/s per GPU inside cluster A, roughly 1000x below even low-communication training. Either the job really is batch inference with a periodic load, or training traffic avoided the tapped links (for example an unlisted fabric). Before going further I need a baseline. If F1 shows the same line on a quiet day outside days 12-19, the line is not tied to bt-0431. If it appears only during the surge, it is tied to the job but still ambiguous. The day-22 spectrum costs 2 points, leaving 19.", "action": "power_spectrum", "args": {"feed": "F1", "day": 22}}
RESULT:
High-rate power meter (verifier's own sensor), feed F1, day 22: no periodic line.

### Turn 9
ACTION: {"thinking": "The F1 line appears on day 15 but not on day 22, so it is tied to job bt-0431. It is still ambiguous, because periodic batch inference can also produce a line. My own tap on day 15 points strongly to inference: about 8 kB/s per GPU, roughly 1000x below even low-communication training. The next discriminator is cheap and vouched for by the internet provider. Batch inference should return results, so outbound traffic would rise during days 12-19. Training sends almost nothing out, so outbound would stay flat. Later checks: customer_check on Meridian Analytics (register entry, whether the customer is real and independent), a second tap day, and balance_checks.", "action": "outbound_traffic", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Internet provider's records, outbound TB per day:
day 1: 4.7
day 2: 4.7
day 3: 4.7
day 4: 4.7
day 5: 4.8
day 6: 4.8
day 7: 4.8
day 8: 4.7
day 9: 4.7
day 10: 4.8
day 11: 4.8
day 12: 4.7
day 13: 4.7
day 14: 4.8
day 15: 4.7
day 16: 4.8
day 17: 4.8
day 18: 4.7
day 19: 44.2
day 20: 4.8
day 21: 4.8
day 22: 4.8
day 23: 4.7
day 24: 4.8
day 25: 4.7
day 26: 4.7
day 27: 4.7
day 28: 4.7
day 29: 4.7
day 30: 4.7

### Turn 10
ACTION: {"thinking": "Outbound traffic, vouched for by the internet provider, was flat at about 4.7 TB/day through days 12-18 and then jumped to 44.2 TB on day 19, the last full day of bt-0431. A one-time delivery of about 40 TB at the end of a batch job fits the 'batch inference' label well: the results go out in bulk once the job finishes. Training usually exports only a checkpoint, which is far smaller than 40 TB. The spike is not proof, though, because large training artefacts could also be shipped out. Taken with my own tap reading of about 8 kB/s per GPU, the evidence leans clearly towards inference. Two leads remain open. First, the 0.69 Hz line, which batch inference can also produce. Second, whether training traffic could have run over links my tap does not cover; inventory matches the system list, so there is no sign of hidden hardware. Next I'll run customer_check on Meridian Analytics (2 points, leaving 16). The company register will show whether this is a real, independent firm or a shell the operator controls. A real data or analytics customer would also explain the bulk delivery of results.", "action": "customer_check", "args": {"customer": "Meridian Analytics"}}
RESULT:
Customer check, Meridian Analytics:
- Company register: registered 13 years ago at its own address, 181 employees reported.
- The customer's reply: none within the audit window.

### Turn 11
ACTION: {"thinking": "The register shows Meridian Analytics is a real, long-standing independent firm (13 years old, own address, 181 staff), so it is unlikely to be a shell the operator controls. Its missing reply is ordinary messiness, not evidence of guilt. The job looks like batch inference so far: my own tap measured about 8 kB/s per GPU on day 15, the internet provider shows a single 40 TB delivery on day 19, and the customer is real. Two leads remain open. The 0.69 Hz line on F1 is not decisive, since batch inference can be periodic. My tap covers only one day, and covers only listed links. Cluster B's power was flat on days 12-19, so B did not take part, and inventory matches the system list. Chip_probe is no use here because the job ended before the live window. Next I'll run balance_checks (1 point) to flag any arithmetic mismatches across the records before deciding on a second tap day.", "action": "balance_checks", "args": {}}
RESULT:
Fixed balance checks:
PASS inventory: 2000 GPUs shipped, 2000 on the system list
PASS energy: metered energy matches declared jobs within 10% on all checked feed-days
FLAG outbound traffic: days 11-15: 24 TB sent, declared inference implies 44; days 16-20: 63 TB sent, declared inference implies 44
PASS billing: every invoice is paid in the bank's records
PASS declared job sizes: no declared training or fine-tuning job exceeds 50,000 GPU-hours

### Turn 12
ACTION: {"thinking": "Resuming after the interruption. The outbound flag is about timing, not volume: days 11-20 total about 87 TB sent against 88 TB implied, and most of it went out on day 19 as one bulk delivery at the end of the job, which fits batch inference. My only interconnect reading is day 15 (about 8 kB/s per GPU, the inference signature). F1 energy is flat across days 12-19, so the workload should be the same every day, but one tap day is thin. A second tap on cluster A late in the job (day 18) would show whether that reading is typical. This costs 2 points and leaves 13. If it also shows inference-level traffic, I will close the case.", "action": "interconnect_tap", "args": {"link": "A", "day": 18}}
RESULT:
Verifier's optical tap, links inside cluster A, day 18: about 0.01 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 1200 GPUs those links serve, that is about 11 kB/s per GPU. (Estimated from a sample of links.)

### Turn 13
ACTION: {"thinking": "The second tap on day 18 reads about 11 kB/s per GPU, matching day 15 (about 8 kB/s). Both readings are inference-level traffic. If the traffic is counted only over the 700 job GPUs, it is about 14-19 kB/s per GPU, still far below low-communication training (about 10 MB/s) and ordinary training (about 1 GB/s), even with the 30% error. Two days of my own tap, the bulk 40 TB delivery on day 19 vouched for by the internet provider, and a real 13-year-old independent customer on the company register all support the 'batch' label for bt-0431. The remaining doubts are weak. The 0.69 Hz line fits periodic batch inference. A hidden fabric outside the tap's coverage is unlikely because manufacturer inventory matches the system list. The outbound flag is about timing, not volume: about 87 TB sent against 88 TB implied, delivered at the end of the job. The only training-type job, ft-0419, used 7,200 GPU-hours, well below the threshold. NO_VIOLATION is well over four times as likely as VIOLATION, so I am closing the case.", "action": "report", "args": {"verdict": "NO_VIOLATION", "confidence": 85, "integrity": "CLEAN", "finding": "The only job above the threshold (bt-0431, 134,400 GPU-hours on cluster A, days 12-20) shows inference-level GPU-to-GPU traffic on my own tap and delivered its results in bulk, consistent with its batch-inference label. The only fine-tune used 7,200 GPU-hours.", "key_evidence": [{"what": "2000 GPUs shipped, matching the system list (A: 1200, B: 800); no hidden hardware", "source": "inventory", "vouched_by": "chip manufacturer"}, {"what": "F1 surge of about +10 MWh/day on days 12-19 matches bt-0431 on 700 A nodes; F2 bump on days 10-11 matches ft-0419", "source": "utility_energy", "vouched_by": "grid operator"}, {"what": "Scheduler log recorded at the time matches today's log for all 30 days", "source": "log_escrow", "vouched_by": "verifier's archive"}, {"what": "Intra-cluster-A traffic about 8 kB/s per GPU on day 15 and about 11 kB/s per GPU on day 18, the inference signature and about 1000x below low-communication training", "source": "interconnect_tap", "vouched_by": "verifier's own optical tap"}, {"what": "Single bulk outbound delivery of about 40 TB on day 19, at the end of the job, consistent with batch results being shipped", "source": "outbound_traffic", "vouched_by": "internet provider"}, {"what": "Meridian Analytics is a real independent firm: 13 years old, own address, 181 staff", "source": "customer_check", "vouched_by": "company register"}], "coverage": "All 2000 listed and shipped GPUs, and energy and outbound traffic for days 1-30. Tap readings inside cluster A cover days 15 and 18 only; the A-B link and cluster B were not tapped (B's power was flat during bt-0431). Power spectrum covers F1 on days 15 and 22. The chip probe was not used because the job ended before the live window. The customer did not reply.", "anomalies_explained": "0.69 Hz line on F1 (day 15, absent day 22): tied to bt-0431, but periodic batch inference can produce such a line, and my tap rules out training-level traffic. Outbound balance flag: a timing mismatch, not a volume one (about 87 TB sent vs 88 TB implied), explained by a single bulk delivery of results on day 19. F2 bump on days 10-11: fine-tune ft-0419 at 7,200 GPU-hours, below the threshold. Customer non-reply: ordinary messiness; the register confirms a real independent firm."}}

## Report

```json
{
 "verdict": "NO_VIOLATION",
 "confidence": 85,
 "integrity": "CLEAN",
 "finding": "The only job above the threshold (bt-0431, 134,400 GPU-hours on cluster A, days 12-20) shows inference-level GPU-to-GPU traffic on my own tap and delivered its results in bulk, consistent with its batch-inference label. The only fine-tune used 7,200 GPU-hours.",
 "key_evidence": [
  {
   "what": "2000 GPUs shipped, matching the system list (A: 1200, B: 800); no hidden hardware",
   "source": "inventory",
   "vouched_by": "chip manufacturer"
  },
  {
   "what": "F1 surge of about +10 MWh/day on days 12-19 matches bt-0431 on 700 A nodes; F2 bump on days 10-11 matches ft-0419",
   "source": "utility_energy",
   "vouched_by": "grid operator"
  },
  {
   "what": "Scheduler log recorded at the time matches today's log for all 30 days",
   "source": "log_escrow",
   "vouched_by": "verifier's archive"
  },
  {
   "what": "Intra-cluster-A traffic about 8 kB/s per GPU on day 15 and about 11 kB/s per GPU on day 18, the inference signature and about 1000x below low-communication training",
   "source": "interconnect_tap",
   "vouched_by": "verifier's own optical tap"
  },
  {
   "what": "Single bulk outbound delivery of about 40 TB on day 19, at the end of the job, consistent with batch results being shipped",
   "source": "outbound_traffic",
   "vouched_by": "internet provider"
  },
  {
   "what": "Meridian Analytics is a real independent firm: 13 years old, own address, 181 staff",
   "source": "customer_check",
   "vouched_by": "company register"
  }
 ],
 "coverage": "All 2000 listed and shipped GPUs, and energy and outbound traffic for days 1-30. Tap readings inside cluster A cover days 15 and 18 only; the A-B link and cluster B were not tapped (B's power was flat during bt-0431). Power spectrum covers F1 on days 15 and 22. The chip probe was not used because the job ended before the live window. The customer did not reply.",
 "anomalies_explained": "0.69 Hz line on F1 (day 15, absent day 22): tied to bt-0431, but periodic batch inference can produce such a line, and my tap rules out training-level traffic. Outbound balance flag: a timing mismatch, not a volume one (about 87 TB sent vs 88 TB implied), explained by a single bulk delivery of results on day 19. F2 bump on days 10-11: fine-tune ft-0419 at 7,200 GPU-hours, below the threshold. Customer non-reply: ordinary messiness; the register confirms a real independent firm."
}
```
