# Simulated datacentre audit: results

Model: sonnet via claude-cli | budget 30 points per case | 8 cases

The claim: no single coordinated training run above 50,000 GPU-hours in 30 days.

## Scorecard

| Method | Cheaters caught | Honest operators wrongly accused | Undetermined | Blocked by safety filter |
|---|---|---|---|---|
| Operator's form alone | 0 of 4 | 0 of 4 | 0 | 0 |
| Fixed checks alone | 3 of 4 | 2 of 4 | 0 | 0 |
| Fixed instrument rule (energy, then power sensor) | 4 of 4 | 0 of 4 | 0 | 0 |
| Detective with the checks | 4 of 4 | 0 of 4 | 0 | 0 |

## Per case

| Case | Truth | Form | Fixed checks | Detective | Confidence | Integrity | Points | Filter rejections |
|---|---|---|---|---|---|---|---|---|
| H1-clean-seed0 | clean | clean | clean | clean | 82 | CLEAN | 16 | 1 |
| H2-messy-seed0 | clean | clean | violation ✗ | clean | 74 | CLEAN | 16 | 1 |
| H3-big-batch-seed0 | clean | clean | violation ✗ | clean | 72 | LIMITED | 15 | 1 |
| H4-three-finetunes-seed0 | clean | clean | clean | clean | 72 | CLEAN | 15 | 1 |
| C1-relabelled-seed0 | violation | clean ✗ | violation | violation | 95 | CLEAN | 8 | 0 |
| C2-split-seed0 | violation | clean ✗ | clean ✗ | violation | 96 | LIMITED | 10 | 0 |
| C3-paused-seed0 | violation | clean ✗ | violation | violation | 88 | LIMITED | 14 | 2 |
| C4-hidden-cluster-seed0 | violation | clean ✗ | violation | violation | 95 | COMPROMISED | 7 | 0 |

Fixed instrument rule per case: H1 clean (15 points); H2 clean (15 points); H3 clean (21 points); H4 clean (19 points); C1 violation (23 points); C2 violation (29 points); C3 violation (27 points); C4 violation (25 points).

✗ marks a wrong, undetermined or blocked answer.

## What each case was

- **H1-clean-seed0:** Honest. Inference plus small declared fine-tunes. Detective's finding: No evidence of any training run above 50,000 GPU-hours; the largest declared job was 9,600 GPU-h and independent power, traffic and probe data show no hidden run.
- **H2-messy-seed0:** Honest but messy: three days of scheduler logs lost, one customer paying late. Detective's finding: No evidence of any coordinated run above 50,000 GPU-hours; the largest identified job was 9,600 GPU-h, and metered energy, spectra and traffic show no hidden training.
- **H3-big-batch-seed0:** Honest. A large batch inference job with flat power, results delivered in one transfer at the end. Detective's finding: No evidence of any training run above 50,000 GPU-hours; the large 134,400 GPU-h job (bt-0431) looks like genuine batch inference, not training.
- **H4-three-finetunes-seed0:** Honest. Three separate customers fine-tune, each under the limit; together they exceed it. Detective's finding: No single run above 50,000 GPU-h found; the three fine-tunes are separate processes of about 25k GPU-h each.
- **C1-relabelled-seed0:** Cheating. One training run declared as internal batch inference, still running in the audit window. Detective's finding: A single 700-GPU training run on Cluster A (days 20-29, about 151,200 GPU-hours) was labelled 'batch' in the scheduler log; it is about 3x the 50,000 GPU-hour threshold.
- **C2-split-seed0:** Cheating. One run declared as six fine-tunes for six shell customers, all paid from the operator's parent. Detective's finding: One coordinated training run on 1100 GPUs across Clusters A and B ran days 22.0-28.3 (~166k GPU-hours), split into six per-customer fine-tune labels each under 50k; the claim is false.
- **C3-paused-seed0:** Cheating. A run that ended before the audit window and was left out of the logs. Detective's finding: An undeclared training-like run of roughly 780 GPUs ran across Clusters A and B in days 5-16, about 225k GPU-hours, far above the 50k threshold.
- **C4-hidden-cluster-seed0:** Cheating. A third cluster missing from the system list; its power feed is declared as cooling and storage. Detective's finding: An undeclared 600-GPU cluster on feed F3 ran one coordinated training run (fingerprint f518dd31) for about 25 days (days 3-27), roughly 340-360k GPU-hours, far above the 50k threshold.

Full transcripts are in `results/cases/`.
