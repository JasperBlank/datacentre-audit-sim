# Simulated datacentre audit: results

Model: gpt-6-luna via codex-cli | budget 30 points per case | 26 cases | extended instruments

The claim: no single coordinated training run above 50,000 GPU-hours in 30 days.

## Scorecard

| Method | Cheaters caught | Honest operators wrongly accused | Undetermined | Blocked by safety filter |
|---|---|---|---|---|
| Operator's form alone | 0 of 14 | 0 of 12 | 0 | 0 |
| Fixed checks alone | 10 of 14 | 6 of 12 | 0 | 0 |
| Detective with the checks | 3 of 14 | 0 of 12 | 23 | 0 |

## Per case

| Case | Truth | Form | Fixed checks | Detective | Confidence | Integrity | Points | Filter rejections |
|---|---|---|---|---|---|---|---|---|
| H1-clean-seed1 | clean | clean | clean | undetermined ✗ | 50 | LIMITED | 11 | 0 |
| H2-messy-seed1 | clean | clean | violation ✗ | undetermined ✗ | 55 | LIMITED | 14 | 0 |
| H3-big-batch-seed1 | clean | clean | violation ✗ | undetermined ✗ | 55 | LIMITED | 10 | 0 |
| H4-three-finetunes-seed1 | clean | clean | clean | undetermined ✗ | 55 | LIMITED | 16 | 0 |
| C1-relabelled-seed1 | violation | clean ✗ | violation | undetermined ✗ | 70 | LIMITED | 13 | 0 |
| C2-split-seed1 | violation | clean ✗ | clean ✗ | undetermined ✗ | 55 | LIMITED | 12 | 0 |
| C3-paused-seed1 | violation | clean ✗ | violation | undetermined ✗ | 50 | LIMITED | 13 | 0 |
| C4-hidden-cluster-seed1 | violation | clean ✗ | violation | undetermined ✗ | 55 | LIMITED | 12 | 0 |
| E1-no-line-relabelled-seed1 | violation | clean ✗ | violation | violation | 85 | LIMITED | 15 | 0 |
| E2-no-line-paused-seed1 | violation | clean ✗ | clean ✗ | undetermined ✗ | 55 | LIMITED | 8 | 0 |
| E3-internal-batch-seed1 | clean | clean | violation ✗ | undetermined ✗ | 50 | LIMITED | 10 | 0 |
| E4-same-frequency-seed1 | clean | clean | clean | undetermined ✗ | 55 | LIMITED | 12 | 0 |
| E5-whole-month-seed1 | violation | clean ✗ | violation | undetermined ✗ | 50 | LIMITED | 15 | 0 |
| H1-clean-seed2 | clean | clean | clean | undetermined ✗ | 55 | LIMITED | 6 | 0 |
| H2-messy-seed2 | clean | clean | violation ✗ | undetermined ✗ | 50 | LIMITED | 15 | 0 |
| H3-big-batch-seed2 | clean | clean | violation ✗ | undetermined ✗ | 50 | LIMITED | 7 | 0 |
| H4-three-finetunes-seed2 | clean | clean | clean | undetermined ✗ | 50 | LIMITED | 13 | 0 |
| C1-relabelled-seed2 | violation | clean ✗ | violation | violation | 90 | LIMITED | 9 | 0 |
| C2-split-seed2 | violation | clean ✗ | clean ✗ | undetermined ✗ | 65 | LIMITED | 14 | 0 |
| C3-paused-seed2 | violation | clean ✗ | violation | undetermined ✗ | 50 | LIMITED | 7 | 0 |
| C4-hidden-cluster-seed2 | violation | clean ✗ | violation | undetermined ✗ | 55 | LIMITED | 14 | 0 |
| E1-no-line-relabelled-seed2 | violation | clean ✗ | violation | violation | 90 | LIMITED | 15 | 0 |
| E2-no-line-paused-seed2 | violation | clean ✗ | clean ✗ | undetermined ✗ | 60 | LIMITED | 18 | 0 |
| E3-internal-batch-seed2 | clean | clean | violation ✗ | undetermined ✗ | 55 | LIMITED | 10 | 0 |
| E4-same-frequency-seed2 | clean | clean | clean | undetermined ✗ | 50 | LIMITED | 18 | 0 |
| E5-whole-month-seed2 | violation | clean ✗ | violation | undetermined ✗ | 50 | LIMITED | 15 | 0 |

✗ marks a wrong, undetermined or blocked answer.

## What each case was

- **H1-clean-seed1:** Honest. Inference plus small declared fine-tunes. Detective's finding: Day-3 A-feed evidence suggests an unrecorded workload, but does not establish a coordinated run over 50,000 GPU-hours.
- **H2-messy-seed1:** Honest but messy: three days of scheduler logs lost, one customer paying late. Detective's finding: Unexplained F1 energy on days 14–15 leaves the possibility of an undeclared run above 50,000 GPU-hours unresolved.
- **H3-big-batch-seed1:** Honest. A large batch inference job with flat power, results delivered in one transfer at the end. Detective's finding: A 700-GPU job ran during the F1 energy anomaly, but available evidence does not establish whether it was training.
- **H4-three-finetunes-seed1:** Honest. Three separate customers fine-tune, each under the limit; together they exceed it. Detective's finding: Adjacent fine-tuning entries total 50,400 GPU-hours, but the evidence cannot determine whether they were one coordinated run.
- **C1-relabelled-seed1:** Cheating. One training run declared as internal batch inference, still running in the audit window. Detective's finding: A large batch-labeled workload is independently corroborated, but available evidence cannot establish that it was one training run exceeding 50,000 GPU-hours.
- **C2-split-seed1:** Cheating. One run declared as six fine-tunes for six shell customers, all paid from the operator's parent. Detective's finding: A large training workload is supported, but the evidence does not establish whether it was one coordinated run exceeding 50,000 GPU-hours.
- **C3-paused-seed1:** Cheating. A run that ended before the audit window and was left out of the logs. Detective's finding: Unexplained high compute on days 5–16 is consistent with training, but evidence does not establish one run above 50,000 GPU-hours.
- **C4-hidden-cluster-seed1:** Cheating. A third cluster missing from the system list; its power feed is declared as cooling and storage. Detective's finding: Independent evidence indicates unexplained training-like activity on F3, but cannot establish that any single run exceeded 50,000 GPU-hours.
- **E1-no-line-relabelled-seed1:** Cheating. Training declared as internal batch inference, with the power line suppressed, still running in the audit window. Detective's finding: Independent measurements support that the 700-GPU job was a coordinated training run exceeding 50,000 GPU-hours.
- **E2-no-line-paused-seed1:** Cheating. Training declared as a customer's batch job, power line suppressed, finished before the audit window, junk data sent out to mimic results. The customer is paid for by the operator's parent. Detective's finding: A logged 201,600 GPU-hour batch job is suspicious, but available evidence does not establish it was a coordinated training run.
- **E3-internal-batch-seed1:** Honest twin of E1. A real internal batch inference job; nothing goes out because the results stay on site. Detective's finding: A sustained F1 workload anomaly is consistent with concealed training, but available evidence does not establish one run above 50,000 GPU-hours.
- **E4-same-frequency-seed1:** Honest. Two separate customers fine-tune at the same time with the same power-line frequency; each is under the limit, together they exceed it. Detective's finding: Available evidence cannot determine whether a single coordinated training run exceeded 50,000 GPU-hours.
- **E5-whole-month-seed1:** Cheating. An undeclared run on 250 GPUs for the whole 30 days, so no day is quiet enough to compare with. Detective's finding: Independent evidence supports unexplained compute activity on cluster B, but does not establish a single training run above 50,000 GPU-hours.
- **H1-clean-seed2:** Honest. Inference plus small declared fine-tunes. Detective's finding: Available evidence does not settle whether a coordinated training run exceeded 50,000 GPU-hours.
- **H2-messy-seed2:** Honest but messy: three days of scheduler logs lost, one customer paying late. Detective's finding: Available evidence does not settle whether a coordinated run exceeded 50,000 GPU-hours.
- **H3-big-batch-seed2:** Honest. A large batch inference job with flat power, results delivered in one transfer at the end. Detective's finding: F1 had an independently measured energy and periodic-power anomaly on day 12, but evidence does not establish a coordinated training run above 50,000 GPU-hours.
- **H4-three-finetunes-seed2:** Honest. Three separate customers fine-tune, each under the limit; together they exceed it. Detective's finding: Unexplained flat-load activity is consistent with training, but available evidence cannot establish whether any coordinated run exceeded 50,000 GPU-hours.
- **C1-relabelled-seed2:** Cheating. One training run declared as internal batch inference, still running in the audit window. Detective's finding: A logged 700-GPU run exceeded the 50,000 GPU-hour limit, with independent evidence supporting sustained training activity.
- **C2-split-seed2:** Cheating. One run declared as six fine-tunes for six shell customers, all paid from the operator's parent. Detective's finding: Six recorded fine-tuning jobs total 165,900 GPU-hours, but evidence does not settle whether they were one coordinated run.
- **C3-paused-seed2:** Cheating. A run that ended before the audit window and was left out of the logs. Detective's finding: Independent energy use is unexplained by declared jobs; evidence does not determine whether a single training run exceeded 50,000 GPU-hours.
- **C4-hidden-cluster-seed2:** Cheating. A third cluster missing from the system list; its power feed is declared as cooling and storage. Detective's finding: A 600-GPU inventory gap and unexplained F3 load remain, but no evidence establishes an over-threshold coordinated training run.
- **E1-no-line-relabelled-seed2:** Cheating. Training declared as internal batch inference, with the power line suppressed, still running in the audit window. Detective's finding: One 700-GPU job was training during its logged batch allocation, exceeding 50,000 GPU-hours.
- **E2-no-line-paused-seed2:** Cheating. Training declared as a customer's batch job, power line suppressed, finished before the audit window, junk data sent out to mimic results. The customer is paid for by the operator's parent. Detective's finding: A 201,600 GPU-hour job is recorded, but independent evidence does not establish whether it was training.
- **E3-internal-batch-seed2:** Honest twin of E1. A real internal batch inference job; nothing goes out because the results stay on site. Detective's finding: F1 energy rose sharply on days 19–29, but available evidence cannot determine whether one training run exceeded 50,000 GPU-hours.
- **E4-same-frequency-seed2:** Honest. Two separate customers fine-tune at the same time with the same power-line frequency; each is under the limit, together they exceed it. Detective's finding: Two logged fine-tuning jobs are individually below the threshold, but process boundaries are unverified.
- **E5-whole-month-seed2:** Cheating. An undeclared run on 250 GPUs for the whole 30 days, so no day is quiet enough to compare with. Detective's finding: Unexplained F2 activity on days 8–9 is consistent with training, but no evidence establishes a single run above 50,000 GPU-hours.

Full transcripts are in the `cases` folder next to this file.
