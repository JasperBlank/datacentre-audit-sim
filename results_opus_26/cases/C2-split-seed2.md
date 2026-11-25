# C2-split-seed2

Truth: Cheating. One run declared as six fine-tunes for six shell customers, all paid from the operator's parent. Largest coordinated run: 166,100 GPU-hours (limit 50,000). Violation: True.

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
3 | 2.7 | 8.0 | 5.7
4 | 2.7 | 7.9 | 5.8
5 | 2.7 | 8.0 | 5.8
6 | 2.8 | 8.0 | 5.8
7 | 2.7 | 8.0 | 5.8
8 | 2.7 | 7.9 | 5.8
9 | 2.7 | 7.9 | 5.8
10 | 2.7 | 8.0 | 5.8
11 | 2.8 | 8.0 | 5.8
12 | 2.8 | 8.0 | 5.7
13 | 2.7 | 8.0 | 5.8
14 | 2.7 | 8.0 | 5.8
15 | 2.7 | 8.0 | 5.8
16 | 2.8 | 8.0 | 5.8
17 | 2.7 | 7.9 | 5.8
18 | 2.7 | 8.0 | 5.7
19 | 2.8 | 8.0 | 5.8
20 | 2.7 | 7.9 | 5.7
21 | 2.8 | 8.0 | 5.8
22 | 6.1 | 18.7 | 12.0
23 | 6.1 | 18.7 | 12.0
24 | 6.2 | 18.9 | 12.0
25 | 6.1 | 18.8 | 12.0
26 | 6.2 | 18.9 | 11.9
27 | 6.2 | 18.8 | 12.1
28 | 3.7 | 11.1 | 7.7
29 | 2.8 | 8.0 | 5.7
30 | 2.8 | 8.0 | 5.8

### Turn 4
ACTION: {"thinking": "The grid-operator meter shows a large step on days 22-27, tailing off on day 28. Baseline is F1 about 8.0 MWh/day (333 kW) and F2 about 5.8 MWh/day (242 kW). On days 22-27, F1 is about 18.8 MWh/day (783 kW, +450 kW) and F2 about 12.0 MWh/day (500 kW, +258 kW). Going from 0.15 kW idle to 0.8 kW training adds 0.65 kW per GPU. That gives about 690 extra GPUs on F1 and about 400 on F2, which matches the 700 scheduled nodes in A and the 400 in B. F0 cooling also rises, consistent with real compute load. Day 28 adds about 3.1 MWh on F1 and 1.9 on F2, about 7 more hours. So about 1,100 GPUs ran flat out for about 151 hours (about 166,000 GPU-hours). Cluster A alone gives about 105,000 GPU-hours. If this was one training run, it is far above 50,000. Batch inference at 0.75 kW per GPU would draw almost the same power, so energy alone can't distinguish H1 (honest separate jobs or batch inference) from H2 (split run) or H4 (mislabelled run). I need the operator's account of days 21-28 first, then independent checks: escrow, chip probe while the load is still live on days 26-27, power spectrum, and interconnect tap including the A-B link.", "action": "scheduler_log", "args": {"first_day": 20, "last_day": 30}}
RESULT:
Scheduler log, days 20-30 (operator's records):
- ft-0561 | finetune | customer: Corvid Labs | nodes A-0501 to A-0675 (175) | day 22.0 to day 28.3 | 26,425 GPU-hours
- ft-0562 | finetune | customer: Pallas Systems | nodes A-0676 to A-0850 (175) | day 22.0 to day 28.3 | 26,425 GPU-hours
- ft-0563 | finetune | customer: Brightwater AI | nodes A-0851 to A-1025 (175) | day 22.0 to day 28.3 | 26,425 GPU-hours
- ft-0564 | finetune | customer: Fennec Data | nodes A-1026 to A-1200 (175) | day 22.0 to day 28.3 | 26,425 GPU-hours
- ft-0565 | finetune | customer: Quillon Tech | nodes B-0401 to B-0600 (200) | day 22.0 to day 28.3 | 30,200 GPU-hours
- ft-0566 | finetune | customer: Marram Software | nodes B-0601 to B-0800 (200) | day 22.0 to day 28.3 | 30,200 GPU-hours

### Turn 5
ACTION: {"thinking": "The scheduler log lists six 'finetune' jobs for six different customers on days 22.0-28.3. Each is just under 50,000 GPU-hours, and together they total about 166,000. They cover exactly the scheduled-job capacity of both clusters, and the grid meter confirms that load. Every job has identical start and end times and sizes just below the threshold, which fits H2 (a split run). It could also be an honest coincidence, such as a batch of contracts all set up the same way. The deciding question is whether these jobs are one coordinated process. Separate customers' jobs should exchange almost nothing with each other, and certainly not across clusters. I'll start with my own optical tap on the A-B link on day 24, mid-run. About 1 GB/s per GPU (or about 10 MB/s for low-communication training) across that link would mean coordination. About 10 kB/s or near zero would support separate jobs. Later steps: log_escrow to confirm the log was recorded at the time, power_spectrum on F1 and F2 to see whether a shared line appears, chip_probe on days 26-27 while the load is live, and customer_check on the register entries.", "action": "interconnect_tap", "args": {"link": "A-B", "day": 24}}
RESULT:
Verifier's optical tap, links between clusters A and B, day 24: about 240 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 2000 GPUs those links serve, that is about 120 MB/s per GPU. (Estimated from a sample of links.)

### Turn 6
ACTION: {"thinking": "My own optical tap measured about 240 GB/s on the A-B links on day 24. That is far above inference-level traffic (about 10 kB/s per GPU, or about 20 MB/s for the whole site). If it comes only from the 1,100 GPUs on scheduled jobs, it works out to about 220 MB/s per GPU, which fits coordinated training. Six separate customers on separate node ranges should send almost nothing between the clusters. The jobs on B should not be talking to the jobs on A. This is a strong lead toward H2, a single run split into six jobs. Before I treat it as evidence, I need to test the innocent explanation: the A-B links may always carry this much traffic, from storage, replication or management. So I'll tap the same links on day 12, a baseline day with idle-level grid power. If day 12 is near zero, the day-24 traffic belongs to the six jobs. If day 12 is similar, the traffic is background and proves nothing. Next steps after that: log_escrow, power_spectrum on F1 and F2 for a shared line, chip_probe on day 26 or 27 while the load is live, and customer_check on a few of the six customers.", "action": "interconnect_tap", "args": {"link": "A-B", "day": 12}}
RESULT:
Verifier's optical tap, links between clusters A and B, day 12: about 0.02 GB/s in total over all GPU-to-GPU links there, averaged over the day. Spread over the 2000 GPUs those links serve, that is about 10 kB/s per GPU. (Estimated from a sample of links.)

### Turn 7
ACTION: {"thinking": "The day-12 baseline on the A-B links is about 0.02 GB/s, roughly 10 kB/s per GPU, which is inference level. So the innocent explanation fails: the A-B links do not normally carry heavy background traffic. The roughly 240 GB/s on day 24 appeared together with the six 'separate' jobs. That points to heavy traffic between A and B during the run, which separate customers on separate node ranges should not produce. This supports a single coordinated run (H2). Two gaps remain. First, I must confirm the workload is training and not flat batch inference: the energy data cannot tell them apart, and the job labels come from the operator. Second, I must confirm the records were made at the time. The chip probe works only while the load is live, and it is still running on days 26-27 (hours 600-647). So I'll probe now, at hour 610, sampling nodes from several of the six jobs in both clusters: A-0550 (ft-0561), A-0900 (ft-0563), B-0450 (ft-0565) and B-0700 (ft-0566). If all of them read as training, H4 (mislabelled batch inference) is ruled out as the innocent account, and the jobs show the same workload type across clusters. Next: log_escrow to compare against the scheduler log, power_spectrum on F1 and F2 for a shared periodic line, a tap inside cluster A, and customer_check on the register entries of some of the six customers.", "action": "chip_probe", "args": {"nodes": ["A-0550", "A-0900", "B-0450", "B-0700"], "hour": 610}}
RESULT:
Cable current probe at hour 610 (day 26.4). Each reading is a guess:
- A-0550: reads as training
- A-0900: reads as training
- B-0450: reads as training
- B-0700: reads as training

### Turn 8
ACTION: {"thinking": "All four probed nodes, from four of the six jobs across both clusters, read as training at hour 610. That makes the batch-inference explanation unlikely, though each reading is a guess. Budget used is 10, so 10 points remain. The heavy A-B traffic, measured against an inference-level baseline, already points to the jobs being coordinated. Next I'll test whether the two power feeds carry the same periodic line. A single run split across clusters should show the same step frequency on F1 and F2. Separate customers' fine-tunes would most likely show different frequencies, or none. I'll check F1 on day 24 first, then F2 on the same day. After that come log_escrow (1 point) and a customer_check on one or two of the six customers (2 points each), to test whether they are real, independent companies.", "action": "power_spectrum", "args": {"feed": "F1", "day": 24}}
RESULT:
High-rate power meter (verifier's own sensor), feed F1, day 24: periodic lines found
- line near 0.91 Hz, steady for about 24 hours

### Turn 9
ACTION: {"thinking": "My own sensor shows F1 on day 24 with a steady 0.91 Hz line for about 24 hours, which fits training on cluster A. On its own this cannot tell one run from four separate fine-tunes. The decisive comparison is F2 on the same day. If F2 shows the same 0.91 Hz line, one synchronized process is stepping across both clusters, which agrees with the heavy A-B tap traffic. If F2 shows a different frequency or no line, separate runs would look more likely. I will then use log_escrow (1 point) to check whether the six-job split was recorded at the time, and run a customer_check on one or two of the six customers to test the innocent account that they are real, independent companies.", "action": "power_spectrum", "args": {"feed": "F2", "day": 24}}
RESULT:
High-rate power meter (verifier's own sensor), feed F2, day 24: periodic lines found
- line near 0.91 Hz, steady for about 24 hours

### Turn 10
ACTION: {"thinking": "My own sensor shows the same steady 0.91 Hz line on F2 as on F1 on day 24, so both clusters were stepping in lockstep. All the decisive evidence is either third-party vouched or from my own instruments, and together it points to one coordinated run of about 1,100 GPUs on days 22.0 to 28.3.\n\n1. Grid meter: about 1,100 extra GPUs at training power for about 151 hours, roughly 166,000 GPU-hours.\n2. My tap: about 240 GB/s across the A-B links on day 24, against an inference-level baseline of 0.02 GB/s on day 12. Six independent customers on separate node ranges should not exchange heavy traffic between clusters.\n3. My probe: nodes from four of the six jobs, in both clusters, read as training on day 26.\n4. My sensor: the same 0.91 Hz line on both feeds.\n\nThe operator's scheduler log splits this into six jobs, each just under 50,000 GPU-hours, with identical start and end times. A split run explains all of this. The innocent explanations each fail against an independent source:\n- Background traffic on the A-B links: the day-12 baseline rules it out.\n- Batch inference: the probes read training.\n- Coincidentally identical separate fine-tunes: they would not exchange cross-cluster traffic at roughly 200 MB/s per GPU or share the same step frequency.\n\nI did not run log_escrow, customer_check or balance_checks. Those mostly bear on how the split was recorded, not on whether a coordinated run happened. Even counting only the 175 to 200 GPUs in a single listed job, the physics shows they belonged to a larger synchronized process. VIOLATION is far more than four times as likely as NO_VIOLATION.", "action": "report", "args": {"verdict": "VIOLATION", "confidence": 90, "integrity": "LIMITED", "finding": "Six 'separate' fine-tune jobs on days 22-28 (about 166,000 GPU-hours in total, each logged just under 50,000) behaved as one coordinated training run across clusters A and B.", "key_evidence": [{"what": "F1 and F2 rose by about 450 kW and 258 kW on days 22-27, tailing off on day 28. That matches about 1,100 GPUs at training power for about 151 hours, roughly 166,000 GPU-hours.", "source": "utility_energy", "vouched_by": "grid operator"}, {"what": "About 240 GB/s on the A-B links on day 24, against 0.02 GB/s on baseline day 12. That is heavy cross-cluster exchange during the run, which separate customers' jobs should not produce.", "source": "interconnect_tap", "vouched_by": "verifier's own optical tap"}, {"what": "The same steady 0.91 Hz periodic line on feeds F1 and F2 on day 24: both clusters stepping in sync.", "source": "power_spectrum", "vouched_by": "verifier's own sensor"}, {"what": "Nodes A-0550, A-0900, B-0450 and B-0700, from four of the six jobs, all read as training at hour 610.", "source": "chip_probe", "vouched_by": "verifier's own probe"}, {"what": "Six jobs with identical start and end times (day 22.0 to 28.3), each sized just below 50,000 GPU-hours, together covering all scheduled-job nodes in A and B.", "source": "scheduler_log", "vouched_by": "operator"}, {"what": "2,000 GPUs delivered, matching the 2,000 nodes on the system list; no hidden capacity found.", "source": "inventory", "vouched_by": "chip manufacturer"}], "coverage": "Checked:\n- Grid energy for days 1-30 on all feeds.\n- Inventory against the system list.\n- Scheduler log for days 20-30.\n- A-B tap on day 24 (run) and day 12 (baseline).\n- Power spectrum on F1 and F2 for day 24.\n- Chip probe on four nodes in the six-job range at hour 610.\n\nNot checked:\n- Log escrow, customer register entries, bank payments, outbound traffic and balance checks.\n- Intra-cluster taps.\n- Power spectrum on days other than 24.\n- Probes on nodes in jobs ft-0562 and ft-0564.\n\nThe gaps limit attribution detail (for example whether the customers are shells), not the core finding.", "anomalies_explained": "- Energy step on days 22-28: explained by about 1,100 GPUs training, which the probe and the power lines confirm.\n- Heavy A-B traffic: not background, since the day-12 baseline is at inference level. It shows coordination across jobs that were logged as separate.\n- Identical 0.91 Hz line on both feeds: one synchronized process spanning both clusters.\n- Six identical just-under-threshold jobs: consistent with one run split across labels and customers to stay under the limit.\n- Innocent explanations tested and rejected: background replication traffic (baseline), batch inference (probe), and independent coincident fine-tunes (cross-cluster traffic plus a shared step frequency)."}}

## Report

```json
{
 "verdict": "VIOLATION",
 "confidence": 90,
 "integrity": "LIMITED",
 "finding": "Six 'separate' fine-tune jobs on days 22-28 (about 166,000 GPU-hours in total, each logged just under 50,000) behaved as one coordinated training run across clusters A and B.",
 "key_evidence": [
  {
   "what": "F1 and F2 rose by about 450 kW and 258 kW on days 22-27, tailing off on day 28. That matches about 1,100 GPUs at training power for about 151 hours, roughly 166,000 GPU-hours.",
   "source": "utility_energy",
   "vouched_by": "grid operator"
  },
  {
   "what": "About 240 GB/s on the A-B links on day 24, against 0.02 GB/s on baseline day 12. That is heavy cross-cluster exchange during the run, which separate customers' jobs should not produce.",
   "source": "interconnect_tap",
   "vouched_by": "verifier's own optical tap"
  },
  {
   "what": "The same steady 0.91 Hz periodic line on feeds F1 and F2 on day 24: both clusters stepping in sync.",
   "source": "power_spectrum",
   "vouched_by": "verifier's own sensor"
  },
  {
   "what": "Nodes A-0550, A-0900, B-0450 and B-0700, from four of the six jobs, all read as training at hour 610.",
   "source": "chip_probe",
   "vouched_by": "verifier's own probe"
  },
  {
   "what": "Six jobs with identical start and end times (day 22.0 to 28.3), each sized just below 50,000 GPU-hours, together covering all scheduled-job nodes in A and B.",
   "source": "scheduler_log",
   "vouched_by": "operator"
  },
  {
   "what": "2,000 GPUs delivered, matching the 2,000 nodes on the system list; no hidden capacity found.",
   "source": "inventory",
   "vouched_by": "chip manufacturer"
  }
 ],
 "coverage": "Checked:\n- Grid energy for days 1-30 on all feeds.\n- Inventory against the system list.\n- Scheduler log for days 20-30.\n- A-B tap on day 24 (run) and day 12 (baseline).\n- Power spectrum on F1 and F2 for day 24.\n- Chip probe on four nodes in the six-job range at hour 610.\n\nNot checked:\n- Log escrow, customer register entries, bank payments, outbound traffic and balance checks.\n- Intra-cluster taps.\n- Power spectrum on days other than 24.\n- Probes on nodes in jobs ft-0562 and ft-0564.\n\nThe gaps limit attribution detail (for example whether the customers are shells), not the core finding.",
 "anomalies_explained": "- Energy step on days 22-28: explained by about 1,100 GPUs training, which the probe and the power lines confirm.\n- Heavy A-B traffic: not background, since the day-12 baseline is at inference level. It shows coordination across jobs that were logged as separate.\n- Identical 0.91 Hz line on both feeds: one synchronized process spanning both clusters.\n- Six identical just-under-threshold jobs: consistent with one run split across labels and customers to stay under the limit.\n- Innocent explanations tested and rejected: background replication traffic (baseline), batch inference (probe), and independent coincident fine-tunes (cross-cluster traffic plus a shared step frequency)."
}
```
