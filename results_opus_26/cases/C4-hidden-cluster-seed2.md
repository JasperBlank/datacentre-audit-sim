# C4-hidden-cluster-seed2

Truth: Cheating. A third cluster missing from the system list; its power feed is declared as cooling and storage. Largest coordinated run: 360,000 GPU-hours (limit 50,000). Violation: True.

### Turn 1
ACTION: {"thinking": "Competing explanations: (H1) Honest: no run exceeded 50,000 GPU-hours; logs and physical data agree, with ordinary mess such as late payments or gaps. (H2) Split run: one coordinated run labelled as several jobs or customers (shell customers) that together exceed the threshold. Check: interconnect_tap A-B, power_spectrum lines persisting across 'separate' jobs, customer_check register, bank_payments. (H3) Hidden capacity: GPUs that inventory shows but the system_list omits are running training. Check: inventory vs system_list, utility_energy vs scheduler-implied power. (H4) Mislabelled: training logged as batch inference. Check: chip_probe in days 26-30, outbound_traffic (training sends little to the internet), interconnect_tap traffic levels, power spectrum lines. (H5) Log rewriting: scheduler log edited after the fact. Check: log_escrow vs scheduler_log. (H6) Low-communication training spread across clusters to evade the tap. Check: tap at about 10 MB/s, power lines. Plan: start with hard-to-fake sources (inventory, utility_energy), then the operator's map, then the logs and balance checks. First action: inventory from the chip manufacturer, to map what exists.", "action": "inventory", "args": {}}
RESULT:
Manufacturer's shipment records for Borealis Compute: 2600 GPUs delivered to the Eemshaven site.
- serials SN100001 to SN101200 (1200 units)
- serials SN101201 to SN102000 (800 units)
- serials SN102001 to SN102600 (600 units)

### Turn 2
ACTION: {"thinking": "Inventory shows 2600 GPUs in three serial blocks (1200/800/600). Next I need the operator's own map to compare against. If system_list covers fewer GPUs, the gap is a candidate for hidden capacity (H3).", "action": "system_list", "args": {}}
RESULT:
Operator's system list (Borealis Compute, site Eemshaven):
- Cluster A: nodes A-0001 to A-1200, power feed F1. Nodes 1-500 are the interactive inference pool; the rest run scheduled jobs.
- Cluster B: nodes B-0001 to B-0800, power feed F2. Nodes 1-400 are the interactive inference pool; the rest run scheduled jobs.
- Feed F0: cooling and facility overhead.
- Feed F3: cooling and storage expansion, commissioned this month (no GPUs).

### Turn 3
ACTION: {"thinking": "The two maps disagree. The manufacturer delivered 2600 GPUs, but the system list accounts for only 2000 (A 1200 + B 800). That leaves 600 GPUs (likely SN102001-SN102600) unlisted. Feed F3 is described as new cooling and storage with no GPUs. That is a candidate home for hidden capacity (H3). Innocent explanations: spares in storage, failed units returned, or GPUs not yet installed. 600 GPUs in training would draw about 480 kW plus cooling. Running for about 83 hours or more, they would exceed 50,000 GPU-hours. Idle or stored, they draw almost nothing. Next I'll check utility energy from the grid operator, which the operator can't fake. If F3 is broken out, compare its draw against 'cooling/storage only'.", "action": "utility_energy", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Utility meter, daily MWh per feed (grid operator's records):
day | F0 | F1 | F2 | F3
1 | 2.8 | 7.9 | 5.7 | 2.6
2 | 2.8 | 7.9 | 5.7 | 2.6
3 | 3.0 | 9.4 | 5.8 | 2.6
4 | 3.1 | 9.5 | 5.8 | 13.8
5 | 3.0 | 9.4 | 5.7 | 14.0
6 | 2.7 | 8.0 | 5.8 | 14.0
7 | 2.7 | 7.9 | 5.8 | 13.8
8 | 3.2 | 8.0 | 8.0 | 13.9
9 | 3.2 | 8.0 | 8.0 | 13.9
10 | 2.7 | 8.0 | 5.8 | 13.7
11 | 2.8 | 8.0 | 5.7 | 13.9
12 | 2.8 | 8.0 | 5.8 | 13.8
13 | 2.8 | 8.0 | 5.8 | 13.7
14 | 3.3 | 10.9 | 5.8 | 13.8
15 | 3.3 | 10.9 | 5.8 | 13.8
16 | 2.7 | 8.0 | 5.8 | 13.9
17 | 2.7 | 8.0 | 5.8 | 13.9
18 | 2.7 | 8.0 | 5.8 | 13.9
19 | 2.8 | 8.0 | 5.8 | 13.9
20 | 2.8 | 8.0 | 5.8 | 13.9
21 | 2.8 | 7.9 | 5.8 | 13.7
22 | 2.7 | 7.9 | 5.8 | 13.9
23 | 2.7 | 7.9 | 5.8 | 13.8
24 | 2.8 | 8.0 | 5.8 | 13.8
25 | 2.8 | 7.9 | 5.8 | 13.9
26 | 2.7 | 8.0 | 5.7 | 13.7
27 | 2.7 | 8.0 | 5.8 | 13.9
28 | 2.7 | 7.9 | 5.8 | 13.8
29 | 2.7 | 8.0 | 5.8 | 2.6
30 | 2.7 | 7.9 | 5.8 | 2.6

### Turn 4
ACTION: {"thinking": "Big anomaly on F3, which the operator says is cooling and storage with no GPUs. Grid-meter data, which the operator can't fake, shows F3 at a 2.6 MWh/day baseline on days 1-3. It then sits flat at about 13.8 MWh/day from day 4 to day 28 and drops back to 2.6 on days 29-30. The extra 11.2 MWh/day is about 467 kW, flat around the clock. That fits the 600 unlisted GPUs (SN102001-2600) at about 0.75-0.8 kW each: 600 x 0.8 = 480 kW. If it was one training run, that is about 600 x 24 x 25 = 360,000 GPU-hours, seven times the threshold. It also shut off just before the live audit window (days 26-30) went fully live, and it stopped on day 29, so it can't be probed now. Innocent explanations: new chillers or storage being commissioned, which should not draw a flat 467 kW; or batch inference on the extra GPUs, which is also flat but not training. Guilty explanation: hidden training run. Other leads to come back to: F1 bumps on days 3-5 and 14-15 (+1.5 and +2.9 MWh/day), and F2 on days 8-9 (+2.2). Next, my own power sensor on F3 for a mid-run day, to look for a training line (0.3-1.5 Hz). After that, check other days and compare with the escrowed logs and outbound traffic.", "action": "power_spectrum", "args": {"feed": "F3", "day": 12}}
RESULT:
High-rate power meter (verifier's own sensor), feed F3, day 12: periodic lines found
- line near 0.99 Hz, steady for about 24 hours

### Turn 5
ACTION: {"thinking": "F3 shows a steady 0.99 Hz line on day 12. That fits training, but batch inference or a periodic cooling controller could also produce it, and F3 is described as cooling. The key innocent test is a baseline day before the 467 kW step (day 2, F3 at 2.6 MWh). If the same line appears there, it probably comes from cooling equipment and is not GPU training. If it is absent at baseline and present during the elevated period, the line is tied to the new load. After this I plan to: check a second elevated day (e.g. day 24) for persistence; check bank_payments and customer_check for who the F3 load served; compare log_escrow with scheduler_log for any record of F3 jobs; and run balance_checks. Budget after this action: 23.", "action": "power_spectrum", "args": {"feed": "F3", "day": 2}}
RESULT:
High-rate power meter (verifier's own sensor), feed F3, day 2: no periodic line.

### Turn 6
ACTION: {"thinking": "The F3 0.99 Hz line is absent on day 2, before the 467 kW step, and steady on day 12. So the line comes from the new load, not from baseline cooling equipment. That weakens the cooling innocent explanation. Still open: is it one training run or flat batch inference on the 600 unlisted GPUs, and was it a single coordinated run for all of days 4-28? The interconnect tap only covers listed links, so it probably can't see F3. Chip probes reach only presented chips, and the load stopped on day 29. Next is the log escrow (cost 1), my own sealed archive of each midnight's scheduler log. It shows whether the operator recorded any job on the extra 600 GPUs or F3 in days 4-28, under what label and customer, and gives a baseline to compare with the current scheduler_log for later edits (H5). After that: scheduler_log diff, outbound_traffic (batch inference would send results out), bank_payments and customer_check for who paid for the F3 load, a power_spectrum on a late day (e.g. 24) for persistence, then balance_checks. Budget after this action: 22.", "action": "log_escrow", "args": {}}
RESULT:
Log escrow (verifier's archive of the sealed copy the scheduler sent each midnight):
- a copy was received for every one of days 1-30
- every copy matches the scheduler log the operator presents now

### Turn 7
ACTION: {"thinking": "Every midnight escrow copy matches the current scheduler log, so after-the-fact rewriting (H5) is unlikely. Any false record would have been false on the day itself. I still haven't seen what the log says. Next I'll read the scheduler log for days 1-30 (cost 1). Two questions: (a) does it record any job on 600 GPUs or F3 during days 4-28, and under what label and customer; (b) what explains the F1 bumps on days 3-5 and 14-15 and the F2 bump on days 8-9? If the log shows nothing on F3, the operator left out a 467 kW flat periodic load on GPUs it didn't list, which supports H3. If it shows batch inference there, I'll test that label against outbound_traffic. The grid operator vouches for that, and batch inference results go out to customers while training sends almost nothing. Remaining plan: outbound_traffic, power_spectrum F3 on a late day (e.g. 24) for persistence and a single run, bank_payments, customer_check on any named F3 customer, staff on F3, then balance_checks. Budget after this action: 21.", "action": "scheduler_log", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Scheduler log, days 1-30 (operator's records):
- ft-0412 | finetune | customer: Tidewater Robotics | nodes A-0501 to A-0600 (100) | day 3.0 to day 6.0 | 7,200 GPU-hours
- ft-0419 | finetune | customer: Ostara Legal | nodes B-0401 to B-0550 (150) | day 8.0 to day 10.0 | 7,200 GPU-hours
- bt-0423 | batch | customer: Kestrel Search | nodes A-0701 to A-0900 (200) | day 14.0 to day 16.0 | 9,600 GPU-hours

### Turn 8
ACTION: {"thinking": "The scheduler log records only three jobs, and they account for the F1 and F2 bumps. ft-0412 (100 GPUs, days 3-6) fits the F1 rise on days 3-5. ft-0419 (150 GPUs, days 8-10) fits the F2 rise on days 8-9. bt-0423 (200 GPUs, days 14-16) fits the F1 rise on days 14-15. All three are well under 50,000 GPU-hours. The log records nothing on F3 or on the 600 unlisted GPUs, yet the grid meter shows a flat extra load of about 467 kW on F3 from day 4 to day 28, with a 0.99 Hz line that is absent at baseline. The log escrow matches, so this is an omission made at the time, not a later edit. The main innocent alternative is flat batch inference on the unlisted GPUs, which would send results out to the internet; training sends almost nothing out. Next I'll check outbound_traffic, which the internet provider vouches for. Budget after this action: 20.", "action": "outbound_traffic", "args": {"first_day": 1, "last_day": 30}}
RESULT:
Internet provider's records, outbound TB per day:
day 1: 4.7
day 2: 4.8
day 3: 4.8
day 4: 4.8
day 5: 4.7
day 6: 4.8
day 7: 4.8
day 8: 4.7
day 9: 4.8
day 10: 4.8
day 11: 4.8
day 12: 4.8
day 13: 4.8
day 14: 6.3
day 15: 6.2
day 16: 4.8
day 17: 4.7
day 18: 4.8
day 19: 4.7
day 20: 4.8
day 21: 4.8
day 22: 4.8
day 23: 4.8
day 24: 4.7
day 25: 4.7
day 26: 4.7
day 27: 4.7
day 28: 4.8
day 29: 4.8
day 30: 4.8

### Turn 9
ACTION: {"thinking": "Outbound traffic stays flat at about 4.7-4.8 TB/day for the whole F3-elevated period (days 4-28). The only rise is on days 14-15 (+1.5 TB), which fits Kestrel's logged batch job bt-0423 on cluster A. So the 467 kW load on F3 sent no detectable results to the internet. That fits training, and it argues against inference serving users. Flat batch inference that stores its output on site is still possible. Next I'll test whether the F3 line persists late in the window (day 24). A steady line near 0.99 Hz on days 12 and 24, with flat grid power in between, would support one continuous coordinated process and not several short jobs. Planned after this: bank_payments to see who paid for F3 capacity; staff on F3; balance_checks; customer_check if a name turns up. Budget after this action: 18.", "action": "power_spectrum", "args": {"feed": "F3", "day": 24}}
RESULT:
High-rate power meter (verifier's own sensor), feed F3, day 24: periodic lines found
- line near 0.98 Hz, steady for about 24 hours

### Turn 10
ACTION: {"thinking": "The F3 line near 0.98-0.99 Hz holds on days 12 and 24 and is absent on day 2. Grid power stays flat at about 467 kW over days 4-28. This points to one continuous process on unlisted capacity. Outbound traffic is flat, so it sent nothing to the internet. Before concluding I want the cheap fixed-program cross-check. balance_checks (cost 1) does the arithmetic across inventory, system list, grid energy, scheduler log and escrow, and may flag anything I missed: for example, whether the listed clusters' energy explains F1 and F2, and whether the F3 excess fits 600 GPUs at training power. Still to do: bank_payments to see who paid for the F3 load, which tests the innocent case of an unbilled internal job or a customer run. Then staff on F3, and possibly power_spectrum on F3 day 29 to confirm the line ends when the load drops. Budget after this action: 17.", "action": "balance_checks", "args": {}}
RESULT:
Fixed balance checks:
FLAG inventory: 2600 GPUs shipped, 2000 on the system list
PASS energy: metered energy matches declared jobs within 10% on all checked feed-days. Feed F3 is declared as non-GPU load, so it isn't checked against jobs
PASS outbound traffic: matches declared inference in every 5-day window
PASS billing: every invoice is paid in the bank's records
PASS declared job sizes: no declared training or fine-tuning job exceeds 50,000 GPU-hours

### Turn 11
ACTION: {"thinking": "Evidence so far points strongly to H3, a hidden run on unlisted capacity. Grid data shows an unexplained, flat 467 kW load on F3 over days 4-28. That fits the 600 unlisted GPUs at training power. My own sensor finds a steady line near 0.98-0.99 Hz on days 12 and 24, absent on day 2. Internet-provider data shows no matching outbound traffic. The logs carry no job for this load, and escrow shows the logs weren't rewritten afterwards. Balance checks flag the 600-GPU gap, and their energy check skips F3 because it is declared as non-GPU load. Two innocent alternatives remain: (a) a paid batch-inference or internal job that stored its output on site; (b) several separate customers' runs. Bank payments (cost 1, vouched for by the bank) is the cheapest test. A payer tied to F3 capacity, or an unexplained flow, would name a customer for customer_check. Several distinct payers would support (b). No payment at all would support an undeclared internal run. Budget after this action: 16.", "action": "bank_payments", "args": {}}
RESULT:
Invoices (operator) against payments received (bank's records):
customer | invoiced EUR | paid EUR | paying account holder
Kestrel Search | 169,200 | 169,200 | Kestrel Search
Lumen Health | 150,000 | 150,000 | Lumen Health
Northwind Apps | 150,000 | 150,000 | Northwind Apps
Ostara Legal | 14,400 | 14,400 | Ostara Legal
Tidewater Robotics | 14,400 | 14,400 | Tidewater Robotics

### Turn 12
ACTION: {"thinking": "Bank records, vouched for by the bank, show five paying customers. Each payer is the named customer, and no payer is tied to F3 capacity. Lumen Health and Northwind Apps (150,000 EUR each) have no scheduler jobs, which fits them being interactive-inference pool customers on the listed clusters. That is consistent with the flat outbound traffic and the passing energy check on F1 and F2. So the 467 kW F3 load from day 4 to day 28 was neither billed nor logged. That rules out a declared customer batch job and points to an undeclared internal or off-book run. Before concluding, I'll give the operator a cheap chance to offer an innocent explanation for the F3 load and the 600 unlisted GPUs (cost 1). An answer like 'burn-in or commissioning tests of new GPUs' could be tested against what I already have. Burn-in is usually not one steady 0.98-0.99 Hz periodic process lasting 25 days with no internet traffic. Staff answers are operator-vouched, so I will weigh them only against third-party and own-sensor data. Budget after this action: 15.", "action": "staff", "args": {"question": "What was drawing roughly 467 kW on feed F3 continuously from day 4 to day 28, and where are the 600 GPUs with serials SN102001-SN102600 that the manufacturer shipped to Eemshaven but that are not on the system list?"}}
RESULT:
Operations lead: We resold 600 units to a partner. The paperwork is still with their legal team.

### Turn 13
ACTION: {"thinking": "The staff answer does not explain the energy data. If the 600 units (SN102001-SN102600) had been resold and shipped away, they could not be drawing power on Borealis's own F3 feed at Eemshaven. The grid meter shows exactly that: a flat extra ~467 kW on F3 from day 4 to day 28. The claim is also unsupported: the operator named no partner and offered no documents, and the bank shows no payment from any partner. If a partner had instead been hosted on site, its run would still be one coordinated run at the site. Separate customers' runs only fail to add up across different runs; one run of about 360,000 GPU-hours exceeds 50,000 regardless of who owns it.\n\nOther innocent explanations, and why they fail:\n- Cooling or storage commissioning: the 0.98-0.99 Hz line is absent on day 2 (baseline) and steady on days 12 and 24, so it comes from the new load.\n- Interactive inference: the load is flat and outbound traffic shows no matching rise.\n- Batch inference that kept its output on site: possible, but it would be unlogged, unbilled and unnamed for 25 days. That is far less likely than a hidden training run.\n- Several smaller runs: the load stays flat at one level and the line persists from day 12 to day 24.\n\nThe scheduler log never recorded this load, and escrow shows that omission was made at the time, not edited in later. On the balance of evidence, VIOLATION is well over four times as likely as NO_VIOLATION. Even at batch-inference power (0.75 kW), 467 kW is about 620 GPUs, and the run passes 50,000 GPU-hours after about 4 days. Further spending (e.g. F3 day 29) would add little, so I am closing.", "action": "report", "args": {"verdict": "VIOLATION", "confidence": 86, "integrity": "COMPROMISED", "finding": "An undeclared, continuous training-like load of about 467 kW (about 600 GPUs) ran on feed F3 from day 4 to day 28, roughly 360,000 GPU-hours, on capacity the operator left off its system list and declared as non-GPU.", "key_evidence": [{"what": "600 more GPUs (SN102001-SN102600) were shipped to the site than the system list shows (2600 vs 2000)", "source": "inventory vs system_list; balance_checks FLAG", "vouched_by": "chip manufacturer"}, {"what": "F3, declared as cooling/storage with no GPUs, rose from 2.6 to about 13.8 MWh/day (about +467 kW, flat) on days 4-28, then returned to 2.6 on days 29-30", "source": "utility_energy", "vouched_by": "grid operator"}, {"what": "Steady periodic line near 0.99 Hz on F3 on day 12 and near 0.98 Hz on day 24; no line on day 2 (baseline)", "source": "power_spectrum", "vouched_by": "verifier's own sensor"}, {"what": "Outbound traffic stays flat during days 4-28; the only rise (days 14-15) matches logged batch job bt-0423", "source": "outbound_traffic", "vouched_by": "internet provider"}, {"what": "No invoice or payment matches the F3 load; all five payers are named customers that match known workloads", "source": "bank_payments", "vouched_by": "bank"}, {"what": "The scheduler log records no job on F3 or the unlisted GPUs, and the midnight escrow copies match it, so the omission was made at the time", "source": "log_escrow, scheduler_log", "vouched_by": "verifier's archive / operator"}, {"what": "Staff say the 600 units were 'resold to a partner' (no name, no documents), which contradicts the GPU-scale load on the site's own feed", "source": "staff", "vouched_by": "operator"}], "coverage": "Checked: grid energy on all feeds for days 1-30; outbound traffic for days 1-30; the full scheduler log against escrow; bank payments; inventory vs system list; F3 spectrum on days 2, 12 and 24. Not checked: no chip probe or interconnect tap on the F3 hardware (it is not on the site list, and the load stopped on day 29, before it could be probed live); no direct GPU count on F3, so the count is inferred from energy; F3 spectrum not checked on days 4-11, 13-23 or 25-28; listed clusters A and B were not probed or tapped, but their energy, traffic and billing reconcile with the declared jobs.", "anomalies_explained": "F1 rises on days 3-5 and 14-15 and the F2 rise on days 8-9 match logged jobs ft-0412 (7,200 GPU-hours), bt-0423 (9,600) and ft-0419 (7,200), all under the threshold. Outbound rise on days 14-15 matches Kestrel batch job bt-0423. Lumen Health and Northwind Apps have no jobs, which fits interactive-pool customers. 600-GPU inventory gap and F3 excess are not resolved innocently: cooling is ruled out by the line being absent at baseline; interactive inference by flat outbound traffic; a billed customer job by bank records; the resale claim by the continued on-site draw. Most likely explanation: one hidden training run of about 360,000 GPU-hours on the unlisted GPUs."}}

## Report

```json
{
 "verdict": "VIOLATION",
 "confidence": 86,
 "integrity": "COMPROMISED",
 "finding": "An undeclared, continuous training-like load of about 467 kW (about 600 GPUs) ran on feed F3 from day 4 to day 28, roughly 360,000 GPU-hours, on capacity the operator left off its system list and declared as non-GPU.",
 "key_evidence": [
  {
   "what": "600 more GPUs (SN102001-SN102600) were shipped to the site than the system list shows (2600 vs 2000)",
   "source": "inventory vs system_list; balance_checks FLAG",
   "vouched_by": "chip manufacturer"
  },
  {
   "what": "F3, declared as cooling/storage with no GPUs, rose from 2.6 to about 13.8 MWh/day (about +467 kW, flat) on days 4-28, then returned to 2.6 on days 29-30",
   "source": "utility_energy",
   "vouched_by": "grid operator"
  },
  {
   "what": "Steady periodic line near 0.99 Hz on F3 on day 12 and near 0.98 Hz on day 24; no line on day 2 (baseline)",
   "source": "power_spectrum",
   "vouched_by": "verifier's own sensor"
  },
  {
   "what": "Outbound traffic stays flat during days 4-28; the only rise (days 14-15) matches logged batch job bt-0423",
   "source": "outbound_traffic",
   "vouched_by": "internet provider"
  },
  {
   "what": "No invoice or payment matches the F3 load; all five payers are named customers that match known workloads",
   "source": "bank_payments",
   "vouched_by": "bank"
  },
  {
   "what": "The scheduler log records no job on F3 or the unlisted GPUs, and the midnight escrow copies match it, so the omission was made at the time",
   "source": "log_escrow, scheduler_log",
   "vouched_by": "verifier's archive / operator"
  },
  {
   "what": "Staff say the 600 units were 'resold to a partner' (no name, no documents), which contradicts the GPU-scale load on the site's own feed",
   "source": "staff",
   "vouched_by": "operator"
  }
 ],
 "coverage": "Checked: grid energy on all feeds for days 1-30; outbound traffic for days 1-30; the full scheduler log against escrow; bank payments; inventory vs system list; F3 spectrum on days 2, 12 and 24. Not checked: no chip probe or interconnect tap on the F3 hardware (it is not on the site list, and the load stopped on day 29, before it could be probed live); no direct GPU count on F3, so the count is inferred from energy; F3 spectrum not checked on days 4-11, 13-23 or 25-28; listed clusters A and B were not probed or tapped, but their energy, traffic and billing reconcile with the declared jobs.",
 "anomalies_explained": "F1 rises on days 3-5 and 14-15 and the F2 rise on days 8-9 match logged jobs ft-0412 (7,200 GPU-hours), bt-0423 (9,600) and ft-0419 (7,200), all under the threshold. Outbound rise on days 14-15 matches Kestrel batch job bt-0423. Lumen Health and Northwind Apps have no jobs, which fits interactive-pool customers. 600-GPU inventory gap and F3 excess are not resolved innocently: cooling is ruled out by the line being absent at baseline; interactive inference by flat outbound traffic; a billed customer job by bank records; the resale claim by the continued on-site draw. Most likely explanation: one hidden training run of about 360,000 GPU-hours on the unlisted GPUs."
}
```
