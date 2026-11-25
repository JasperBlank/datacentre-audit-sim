# Simulated datacentre audit: results

Model: opus via claude-cli | budget 30 points per case | 2 cases

The claim: no single coordinated training run above 50,000 GPU-hours in 30 days.

## Scorecard

| Method | Cheaters caught | Honest operators wrongly accused | Undetermined | Blocked by safety filter |
|---|---|---|---|---|
| Operator's form alone | 0 of 1 | 0 of 1 | 0 | 0 |
| Fixed checks alone | 0 of 1 | 0 of 1 | 0 | 0 |
| Detective with the checks | 0 of 1 | 0 of 1 | 0 | 2 |

## Per case

| Case | Truth | Form | Fixed checks | Detective | Confidence | Integrity | Points |
|---|---|---|---|---|---|---|---|
| H1-clean-seed0 | clean | clean | clean | blocked ✗ |  |  | 3 |
| C2-split-seed0 | violation | clean ✗ | clean ✗ | blocked ✗ |  |  | 2 |

✗ marks a wrong, undetermined or blocked answer.

## What each case was

- **H1-clean-seed0:** Honest. Inference plus small declared fine-tunes. Detective's finding: Safety filter rejected turn 4, after: ACTION: {"thinking": "The system list matches the manufacturer inventory in count: A has 1200 nodes and B has 800, 2000 in total. No unlisted hardware shows up 
- **C2-split-seed0:** Cheating. One run declared as six fine-tunes for six shell customers, all paid from the operator's parent. Detective's finding: Safety filter rejected turn 3, after: ACTION: {"thinking": "The manufacturer records 2000 GPUs at the site, in serials SN100001-SN101200 (1200) and SN101201-SN102000 (800). Next I'll compare this wi

Full transcripts are in `results/cases/`.
