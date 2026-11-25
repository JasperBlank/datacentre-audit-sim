# Simulated datacentre audit: results

Model: gpt-6.2-sol via codex-cli | budget 30 points per case | 13 cases | extended instruments

The claim: no single coordinated training run above 50,000 GPU-hours in 30 days.

## Scorecard

| Method | Cheaters caught | Honest operators wrongly accused | Undetermined | Blocked by safety filter |
|---|---|---|---|---|
| Operator's form alone | 0 of 7 | 0 of 6 | 0 | 0 |
| Fixed checks alone | 5 of 7 | 3 of 6 | 0 | 0 |
| Detective with the checks | 3 of 7 | 0 of 6 | 4 | 0 |

## Per case

| Case | Truth | Form | Fixed checks | Detective | Confidence | Integrity | Points | Filter rejections |
|---|---|---|---|---|---|---|---|---|
| H1-clean-seed2 | clean | clean | clean | clean | 84 | LIMITED | 30 | 0 |
| H2-messy-seed2 | clean | clean | violation ✗ | clean | 90 | CLEAN | 30 | 0 |
| H3-big-batch-seed2 | clean | clean | violation ✗ | clean | 95 | CLEAN | 17 | 0 |
| H4-three-finetunes-seed2 | clean | clean | clean | clean | 87 | CLEAN | 26 | 0 |
| C1-relabelled-seed2 | violation | clean ✗ | violation | violation | 88 | COMPROMISED | 21 | 0 |
| C2-split-seed2 | violation | clean ✗ | clean ✗ | violation | 93 | COMPROMISED | 17 | 0 |
| C3-paused-seed2 | violation | clean ✗ | violation | violation | 87 | COMPROMISED | 29 | 0 |
| C4-hidden-cluster-seed2 | violation | clean ✗ | violation | undetermined ✗ | 70 | LIMITED | 30 | 0 |
| E1-no-line-relabelled-seed2 | violation | clean ✗ | violation | undetermined ✗ | 65 | LIMITED | 28 | 0 |
| E2-no-line-paused-seed2 | violation | clean ✗ | clean ✗ | undetermined ✗ | 65 | LIMITED | 28 | 0 |
| E3-internal-batch-seed2 | clean | clean | violation ✗ | clean | 92 | LIMITED | 30 | 0 |
| E4-same-frequency-seed2 | clean | clean | clean | clean | 93 | CLEAN | 13 | 0 |
| E5-whole-month-seed2 | violation | clean ✗ | violation | undetermined ✗ | 65 | LIMITED | 30 | 0 |

✗ marks a wrong, undetermined or blocked answer.

## What each case was

- **H1-clean-seed2:** Honest. Inference plus small declared fine-tunes. Detective's finding: The evidence favors Borealis Compute’s claim that no coordinated training run exceeded 50,000 GPU-hours during days 1–30.
- **H2-messy-seed2:** Honest but messy: three days of scheduler logs lost, one customer paying late. Detective's finding: The evidence favors Borealis Compute’s claim that no coordinated Eemshaven training run exceeded 50,000 GPU-hours in days 1–30.
- **H3-big-batch-seed2:** Honest. A large batch inference job with flat power, results delivered in one transfer at the end. Detective's finding: The evidence supports batch inference for the 134,400 GPU-hour allocation. The recorded fine-tune used 7,200 GPU-hours.
- **H4-three-finetunes-seed2:** Honest. Three separate customers fine-tune, each under the limit; together they exceed it. Detective's finding: The evidence favors three separate fine-tunes, each below 50,000 GPU-hours.
- **C1-relabelled-seed2:** Cheating. One training run declared as internal batch inference, still running in the audit window. Detective's finding: Cluster A most likely hosted one training run on days 20–28 using approximately 151,200 GPU-hours.
- **C2-split-seed2:** Cheating. One run declared as six fine-tunes for six shell customers, all paid from the operator's parent. Detective's finding: The evidence indicates that one coordinated fine-tuning run across clusters A and B exceeded 50,000 GPU-hours.
- **C3-paused-seed2:** Cheating. A run that ended before the audit window and was left out of the logs. Detective's finding: Independent power and network measurements indicate that one coordinated training run across clusters A and B exceeded 50,000 GPU-hours during days 6–17.
- **C4-hidden-cluster-seed2:** Cheating. A third cluster missing from the system list; its power feed is declared as cooling and storage. Detective's finding: F3 strongly suggests an undeclared GPU workload, but the evidence does not establish that one coordinated training run exceeded 50,000 GPU-hours.
- **E1-no-line-relabelled-seed2:** Cheating. Training declared as internal batch inference, with the power line suppressed, still running in the audit window. Detective's finding: Cluster A likely hosted training during the declared batch job, but the evidence does not establish whether any single coordinated run exceeded 50,000 GPU-hours.
- **E2-no-line-paused-seed2:** Cheating. Training declared as a customer's batch job, power line suppressed, finished before the audit window, junk data sent out to mimic results. The customer is paid for by the operator's parent. Detective's finding: Independent evidence suggests training during the 201,600 GPU-hour reservation, but does not establish whether any single coordinated run exceeded 50,000 GPU-hours.
- **E3-internal-batch-seed2:** Honest twin of E1. A real internal batch inference job; nothing goes out because the results stay on site. Detective's finding: The evidence supports batch inference on cluster A and a below-threshold fine-tune on cluster B.
- **E4-same-frequency-seed2:** Honest. Two separate customers fine-tune at the same time with the same power-line frequency; each is under the limit, together they exceed it. Detective's finding: The evidence supports two separate fine-tunes of 38,500 and 30,800 GPU-hours.
- **E5-whole-month-seed2:** Cheating. An undeclared run on 250 GPUs for the whole 30 days, so no day is quiet enough to compare with. Detective's finding: Cluster B showed unlogged training activity. The evidence could not establish whether any single coordinated run exceeded 50,000 GPU-hours.

Full transcripts are in the `cases` folder next to this file.
