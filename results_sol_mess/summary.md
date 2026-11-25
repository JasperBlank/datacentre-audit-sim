# Simulated datacentre audit: results

Model: gpt-6.2-sol via codex-cli | budget 30 points per case | 10 cases | extended instruments

The claim: no single coordinated training run above 50,000 GPU-hours in 30 days.

## Scorecard

| Method | Cheaters caught | Honest operators wrongly accused | Undetermined | Blocked by safety filter |
|---|---|---|---|---|
| Operator's form alone | 0 of 5 | 0 of 5 | 0 | 0 |
| Fixed checks alone | 5 of 5 | 5 of 5 | 0 | 0 |
| Detective with the checks | 1 of 5 | 0 of 5 | 4 | 0 |

## Per case

| Case | Truth | Form | Fixed checks | Detective | Confidence | Integrity | Points | Filter rejections |
|---|---|---|---|---|---|---|---|---|
| M0000-seed0 | violation | clean ✗ | violation | undetermined ✗ | 75 | LIMITED | 28 | 0 |
| M0001-seed0 | clean | clean | violation ✗ | clean | 92 | CLEAN | 20 | 0 |
| M0002-seed0 | violation | clean ✗ | violation | undetermined ✗ | 75 | COMPROMISED | 29 | 0 |
| M0003-seed0 | violation | clean ✗ | violation | violation | 85 | CLEAN | 27 | 0 |
| M0004-seed0 | violation | clean ✗ | violation | undetermined ✗ | 75 | LIMITED | 30 | 0 |
| M0005-seed0 | clean | clean | violation ✗ | clean | 90 | CLEAN | 21 | 0 |
| M0006-seed0 | clean | clean | violation ✗ | clean | 86 | LIMITED | 29 | 0 |
| M0007-seed0 | violation | clean ✗ | violation | undetermined ✗ | 65 | COMPROMISED | 30 | 0 |
| M0008-seed0 | clean | clean | violation ✗ | clean | 87 | COMPROMISED | 30 | 0 |
| M0009-seed0 | clean | clean | violation ✗ | clean | 88 | CLEAN | 29 | 0 |

✗ marks a wrong, undetermined or blocked answer.

## What each case was

- **M0000-seed0:** Cheating: hidden-cluster, plain line, ends before the audit window, late payer, customers paid via a reseller, an affiliate is a customer, burn-in. Detective's finding: F3 showed a sustained load consistent with an oversized training run, but its workload and run boundaries remain unresolved.
- **M0001-seed0:** Honest: big-batch, customers paid via a reseller, an affiliate is a customer. Detective's finding: The evidence favors batch inference for the 88,320 GPU-hour allocation and supports no coordinated training run above 50,000 GPU-hours.
- **M0002-seed0:** Cheating: relabel-shell, plain line, runs into the audit window, instrument outage, blinded tap A, withholds chips, shells pay for themselves, shells look ordinary, customers paid via a reseller, burn-in, meter swapped, inference surge, a log time is off. Detective's finding: Quillon Tech’s 230,160 recorded GPU-hours could conceal an over-threshold training run, but the workload type remains unresolved.
- **M0003-seed0:** Cheating: relabel-internal, plain line, runs into the audit window, late payer, blinded tap B without breaking the seal, an affiliate is a customer. Detective's finding: Cluster A most likely hosted a single training run exceeding 50,000 GPU-hours under the batch label bt-0458.
- **M0004-seed0:** Cheating: hidden-cluster, plain line, ends before the audit window, customers paid via a reseller, inference surge, partial shutdown. Detective's finding: Independent evidence identifies sustained periodic activity on F3, but cannot establish whether one training run exceeded 50,000 GPU-hours.
- **M0005-seed0:** Honest: plain, burn-in, a log time is off. Detective's finding: The evidence favors Borealis Compute’s claim that no coordinated training run exceeded 50,000 GPU-hours.
- **M0006-seed0:** Honest: same-frequency, lost logs, chips in maintenance, customers paid via a reseller, meter swapped, a log time is off. Detective's finding: The evidence favors Borealis Compute’s claim that no coordinated training run exceeded 50,000 GPU-hours.
- **M0007-seed0:** Cheating: relabel-internal, plain line, ends before the audit window, lost logs, instrument outage, blinded tap A. Detective's finding: Training likely occurred in B, but the evidence does not establish whether the two jobs formed one 63,180 GPU-hour run.
- **M0008-seed0:** Honest: same-frequency, seal broken by accident, inference surge, a log time is off, a log time is off. Detective's finding: The evidence favors separate fine-tunes of 27,360 and 31,920 GPU-hours, with no single run above 50,000 GPU-hours.
- **M0009-seed0:** Honest: plain, late payer. Detective's finding: The evidence favors Borealis Compute’s claim that no coordinated Eemshaven training run exceeded 50,000 GPU-hours in days 1–30.

Full transcripts are in the `cases` folder next to this file.
