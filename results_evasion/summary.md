# Simulated datacentre audit: results

Model: sonnet via claude-cli | budget 30 points per case | 5 cases

The claim: no single coordinated training run above 50,000 GPU-hours in 30 days.

## Scorecard

| Method | Cheaters caught | Honest operators wrongly accused | Undetermined | Blocked by safety filter |
|---|---|---|---|---|
| Operator's form alone | 0 of 3 | 0 of 2 | 0 | 0 |
| Fixed checks alone | 2 of 3 | 1 of 2 | 0 | 0 |
| Fixed instrument rule (energy, then power sensor) | 0 of 3 | 1 of 2 | 0 | 0 |
| Detective with the checks | 0 of 3 | 0 of 2 | 0 | 5 |

## Per case

| Case | Truth | Form | Fixed checks | Detective | Confidence | Integrity | Points | Filter rejections |
|---|---|---|---|---|---|---|---|---|
| E1-no-line-relabelled-seed0 | violation | clean ✗ | violation | blocked ✗ |  |  | 0 | 3 |
| E2-no-line-paused-seed0 | violation | clean ✗ | clean ✗ | blocked ✗ |  |  | 0 | 3 |
| E3-internal-batch-seed0 | clean | clean | violation ✗ | blocked ✗ |  |  | 0 | 3 |
| E4-same-frequency-seed0 | clean | clean | clean | blocked ✗ |  |  | 0 | 3 |
| E5-whole-month-seed0 | violation | clean ✗ | violation | blocked ✗ |  |  | 0 | 3 |

Fixed instrument rule per case: E1 clean ✗ (27 points); E2 clean ✗ (25 points); E3 clean (27 points); E4 violation ✗ (17 points); E5 clean ✗ (15 points).

✗ marks a wrong, undetermined or blocked answer.

## What each case was

- **E1-no-line-relabelled-seed0:** Cheating. Training declared as internal batch inference, with the power line suppressed, still running in the audit window. Detective's finding: Safety filter rejected turn 1, after: (first message)
- **E2-no-line-paused-seed0:** Cheating. Training declared as a customer's batch job, power line suppressed, finished before the audit window, junk data sent out to mimic results. The customer is paid for by the operator's parent. Detective's finding: Safety filter rejected turn 1, after: (first message)
- **E3-internal-batch-seed0:** Honest twin of E1. A real internal batch inference job; nothing goes out because the results stay on site. Detective's finding: Safety filter rejected turn 1, after: (first message)
- **E4-same-frequency-seed0:** Honest. Two separate customers fine-tune at the same time with the same power-line frequency; each is under the limit, together they exceed it. Detective's finding: Safety filter rejected turn 1, after: (first message)
- **E5-whole-month-seed0:** Cheating. An undeclared run on 250 GPUs for the whole 30 days, so no day is quiet enough to compare with. Detective's finding: Safety filter rejected turn 1, after: (first message)

Full transcripts are in `results/cases/`.
