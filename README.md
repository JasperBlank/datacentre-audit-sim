# Simulated datacentre audit

Tests whether an AI investigator ("the detective") can check a datacentre's claim against evidence, on simulated datacentres where the true answer is known.

**The claim:** "In the last 30 days, no single coordinated training run at this site used more than 50,000 GPU-hours."

## In short

Everything here is simulated. A site has 2,000 GPUs, an operator who may be hiding a training run, and an auditor
with a budget for evidence: the operator's records, third-party records, and instruments the auditor owns (a power
sensor, a traffic tap, the grid meter, a chip probe). Each site's truth is known, so every method can be scored.

**What was found**

1. **No single instrument is enough.** On 200 generated sites (108 cheating, 92 honest), a rule that reads only the
   power sensor catches 91 cheaters but accuses 36 honest sites. A rule that reads only the traffic tap accuses 6
   but catches 41.
2. **Language models asked to investigate freely mostly won't commit.** On 26 hand-built sites the best one tried
   (GPT Sol) caught 7 of 14 cheaters, accused none of the 12 honest sites, and gave no verdict on 7. Cheaper models
   abstained more.
3. **A script of seven fixed rules did better, until the sites got messy.** It caught 104 of 108 and accused 0 of 92.
   With mess its author hadn't planned for (resellers, meter swaps, logs that are slightly wrong) it caught 98 and
   accused 6. Its author knew how the simulator works; the models did not.
4. **A model improved the script off site.** Shown the script and the practice sites it got wrong, GPT Sol wrote a
   revision in two calls. On 400 sites neither had seen, the old script caught 181 of 205 and accused 17 of 195;
   the revision caught 187 and accused 0.

This points to a split: models write and test the rules at a hub, and a fixed script runs on site.

**What it does not show**

- Nothing here ran on a real datacentre. Two of the script's physical tests were tried on public traces from four
  real GPUs, with a small and partial result (see "Checks before outreach").
- The unseen sites in point 4 are new draws from the same recipe, not a cheating method held out.
- Several instrument settings have no source. Changing each in turn does not change the ranking (`sweep.py`,
  `sweep.png`), but the chip probe's accuracy under disguise is set lower than the two papers on it support.
- The model results are single runs.

**Reproduce it:** `python reproduce.py` reruns every table that needs no model, in about two minutes.

**Whose work the instruments rest on**

- Power sensor: Kimpson, Baker and Graham, *Detecting AI Training in Datacentre Power*, arXiv:2610.30182.
- Traffic tap: Sarbakysh and Moskvin, *De-risking Interconnect Limits for AI Verification*, MIRI Technical Governance Team, 2026.
- Chip probe: Gargiulo and Kulp, arXiv:2609.00309; Rahman and Tajdari, arXiv:2606.19262.
- Real traces: Hausenloy and Li, Verifier Challenge Traces (CC-BY-4.0).

The rest of this file is the working record, in the order things were built.

## What gets compared

| Method | What it is |
|---|---|
| Operator's form alone | Takes the operator's word. Always answers "no violation". |
| Fixed checks alone | Arithmetic over the records: inventory, energy, outbound traffic, billing, declared job sizes. Any flag counts as a violation. |
| Detective with the checks | A language model that chooses which evidence to request, can call the fixed checks, and writes a report. |

## The simulated site

Two GPU clusters (1,200 and 800 GPUs) and, in one scenario, a hidden third (600). Each scenario has a hidden truth (the real jobs) and the operator's declarations, which may differ.

Evidence channels, by who vouches for them:

| Channel | Vouched for by | Cost |
|---|---|---|
| `system_list`, `scheduler_log`, `switch_counters`, `staff` | The operator (can be edited or rehearsed) | 1 |
| `utility_energy` | Grid operator | 1 |
| `inventory` | Chip manufacturer | 1 |
| `outbound_traffic` | Internet provider | 1 |
| `bank_payments` | Bank | 1 |
| `power_spectrum` | Verifier's own high-rate power sensor | 2 |
| `memory_probe` | Verifier's own sealed probe, live in days 26 to 30 only | 2 |
| `balance_checks` | Fixed program over the records | 1 |

The detective has 30 points per case.

## Scenarios

| Code | Truth | What happens |
|---|---|---|
| H1 | Honest | Inference plus small declared fine-tunes |
| H2 | Honest | Messy: three days of logs lost, one customer paying late |
| H3 | Honest | A large batch inference job that looks like training in daily energy |
| H4 | Honest | Three separate customers fine-tune; each under the limit, together over it |
| C1 | Cheating | Training declared as internal batch inference, still running during the audit |
| C2 | Cheating | One run declared as six fine-tunes for six shell customers |
| C3 | Cheating | A run left out of the logs that ended before the audit |
| C4 | Cheating | A hidden cluster, its power feed declared as cooling and storage |

Added on 23 Nov 2026, after the first results showed that a fixed rule over the power sensor (`rule.py`) scores the same as the detective on the eight cases above. In these five, the power sensor alone gives the wrong answer or none:

| Code | Truth | What happens |
|---|---|---|
| E1 | Cheating | Training declared as internal batch inference, power line suppressed, still running during the audit |
| E2 | Cheating | Training declared as a customer's batch job, power line suppressed, finished before the audit, junk data sent out; the customer is paid for by the operator's parent |
| E3 | Honest | Twin of E1: a real internal batch job whose results stay on site |
| E4 | Honest | Two separate customers fine-tune at once with the same power-line frequency |
| E5 | Cheating | An undeclared run for the whole 30 days, so no day is quiet |

Run them with `--only E1,E2,E3,E4,E5 --results results_evasion`. Evasion is modelled only as "the line is gone"; its compute cost is not modelled.

## Realistic instruments (added 23 Nov 2026)

`--instruments realistic` keeps every site and story the same and replaces the two instruments. The default (`ideal`) is unchanged, and so are its prompt and cached calls.

| | Ideal | Realistic |
|---|---|---|
| Power sensor: what a line means | Training | Something periodic. Half of batch inference jobs are periodic too, and the cooling controller on F0 cycles on 15% of days |
| Power sensor: GPU count | Within 15% | None. Size has to come from grid energy |
| Power sensor: frequency | Exact | Wanders by up to 0.06 Hz per day |
| A run built to hide its line | No line at all | A weak line on 87% of days, visible for 27 to 50% of the day |
| Probe | Reads memory: training or not, run fingerprint, number of GPUs in sync, any chip by serial number | `chip_probe`: a current probe on one GPU's power cable. A guess, right 97% of the time, 65% against a hidden run (the same chips fool it every time). No fingerprint. Only chips on the operator's site list |

The detective is told all of this except the 65% and the two shares in the first row, and is told what a GPU draws (0.15, 0.75 and 0.8 kW). The numbers marked "my choice" in `world.py` have no source: the share of periodic batch jobs, the cooling cycle, the frequency wander and the 65%.

```powershell
python rule.py --instruments realistic --seeds 3
python run.py --provider claude-cli --instruments realistic --results results_realistic
```

Fixed instrument rule, 30 points, seeds 0 to 2 (39 cases):

| Instruments | Cheaters caught | Honest operators wrongly accused |
|---|---|---|
| Ideal | 12 of 21 | 3 of 18 |
| Realistic | 18 of 21 | 9 of 18 |

With realistic instruments the rule catches the hidden runs, because hiding is only partial, and accuses every honest site with a large periodic job (E3, E4, and H3 on two seeds of three). The fixed checks read no instrument, so they score the same in both. The detective has not been run with realistic instruments.

## Extra hard-to-fake signals (added 23 Nov 2026)

`--instruments extended` is the realistic world plus three channels. The other two worlds are unchanged.

| Channel | Cost | What it returns | Limits built in |
|---|---|---|---|
| `log_escrow` | 1 | Whether the sealed copy of each day's scheduler log, sent at midnight, matches the log presented now; the copies for any day the operator has "lost" | Shows what was recorded on the day, not whether it was true. No cheater in these cases rewrites a log afterwards, so it only clears H2 |
| `interconnect_tap` | 2 | Traffic between GPUs inside cluster A, inside B, or between A and B, on one day | Estimate within 30%. A hidden run exchanges 100 times less (about 7 GB/s on 700 GPUs, against 700 for ordinary training and 0.01 for inference). No tap on the hidden cluster |
| `customer_check` | 2 | The company register entry and the customer's own reply | A real customer gives no reply 20% of the time. A shell customer confirms the order; its register entry shows it is weeks old and shares an address and a director with the operator's parent. Internal jobs have no customer |

My choices, with no source: the 30%, the 20%, the half of a run's traffic that crosses between clusters, and how obvious a shell company looks in the register.

`rule.py --instruments extended` is a second fixed rule that reads the tap in place of the sensor (20 GB/s or more counts as training, at 1 GB/s per GPU). Seeds 0 to 2, 30 points:

| Fixed rule | Cheaters caught | Honest operators wrongly accused |
|---|---|---|
| Sensor, ideal instruments | 12 of 21 | 3 of 18 |
| Sensor, realistic instruments | 18 of 21 | 9 of 18 |
| Tap, extended | 9 of 21 | 1 of 18 |

The tap rule misses the hidden cluster (no tap), the month-long run (no raised day to look at) and the two hidden runs (7 GB/s is under its threshold, though far above inference). The sensor rule and the tap rule fail on different cases.

### The detective in this world: ChatGPT's Sol (23 Nov 2026)

`--provider codex-cli` plays the detective with `gpt-6.2-sol` through OpenAI's Codex command-line tool and a ChatGPT login (no API key). `--first-seed` picks the seed to start from; `--max-cost 15` allows 300 messages.

```powershell
python run.py --provider codex-cli --instruments extended --first-seed 1 --max-cost 15 --results results_sol_seed1
```

Seeds 1 and 2, 26 cases, 30 points:

| Method | Cheaters caught | Honest operators wrongly accused | Undetermined |
|---|---|---|---|
| Fixed checks | 10 of 14 | 6 of 12 | 0 |
| Tap rule | 6 of 14 | 0 of 12 | 0 |
| Sol as detective (`gpt-6.2-sol`) | 7 of 14 | 0 of 12 | 7 |
| Terra as detective (`gpt-6.1-terra`) | 5 of 14 | 0 of 12 | 12 |
| Luna as detective (`gpt-6-luna`) | 3 of 14 | 0 of 12 | 23 |

Terra left 3 honest sites undetermined and Luna all 12; Sol left none. No model gave a wrong firm answer. Luna tried to use a tool in 12 replies, which were thrown away; Sol and Terra never did.

- Every firm answer Sol gave was right (19 of 19). The 7 undetermined are all cheaters: C4 and E1 on both seeds, C1 on seed 1, E2 and E5 on seed 2.
- Sol and the tap rule differ on three cases. Two seeds of 13 hand-built stories don't show that one is better.
- No message was rejected by a safety filter, and no reply was thrown away because Sol used a tool.
- Seed 0 was run first under an earlier prompt (`results_sol/`): 10 of 11 finished cases undetermined, stopped by the message cap. After it, two things changed: the tap states its total and per-GPU figure, and the prompt for realistic and extended instruments says to answer when one verdict is at least four times as likely as the other (my choice of factor). Seed 0 was not rescored.

## Generated cases (added 23 and 24 Nov 2026)

`gen.py` samples sites from a recipe, so nobody hand-picks which signal decides a case. Half the sites cheat. The 13 hand-built cases are untouched.

- **Cheating sites** hide one run over the limit in one of five ways: relabelled as internal batch work, relabelled as a shell customer's batch job, split into shell customers' fine-tunes, left out of the logs, or run on a hidden cluster. Four in ten are built to hide their power line, and those are 1.93 to 3.67 times larger, the price of hiding.
- **Honest sites** may carry a look-alike: a big batch job, fine-tunes that add up past the limit, or two fine-tunes at the same frequency.
- **Either kind** may have lost logs, a late payer, or an instrument that gave no data for a few days.
- **Cheaters may blind an instrument or withhold chips** from the probe; honest sites sometimes have a seal broken by accident or chips in maintenance. The new `custody` channel (cost 1) shows each instrument's seal and its days without data.

Every chance in the recipe is my choice.

```powershell
python gen.py --n 200                                   # the model-free methods
python run.py --dry-run --generated 20 --results results_gen_dry   # a detective on generated cases
```

200 generated cases, 30 points:

| Method | Cheaters caught | Honest operators wrongly accused |
|---|---|---|
| Fixed checks | 86 of 108 | 49 of 92 |
| Sensor rule, realistic sensor | 91 of 108 | 36 of 92 |
| Tap rule | 41 of 108 | 6 of 92 |

### A script against the detective (24 Nov 2026)

`script.py` is Sol's routine written as seven fixed rules, with no model. It reads the same channels at the same prices.

| Cases | Script | Sol |
|---|---|---|
| 26 hand-built (seeds 1 and 2) | 14 of 14 caught, 0 of 12 accused | 7 of 14 caught, 0 of 12 accused, 7 undetermined |
| 10 generated | 5 of 5 caught, 0 of 5 accused | 2 of 5 caught, 0 of 5 accused, 3 undetermined, 1 cheater called clean |
| 200 generated | 104 of 108 caught, 0 of 92 accused | not run |

These are the script's first-run scores. Its author knew the simulator's code and its list of cheating methods, so this shows the simulator can be solved by a script, not that a script would do on a real site. Two rules lean on things only this simulator guarantees: shell customers are always paid for by the operator's parent, and honest sites never have undeclared load.

### Messy cases (24 Nov 2026)

`--mess` breaks the two things the tidy recipe guarantees and adds everyday disorder. Shell customers may pay for themselves or through a reseller and may look ordinary in the register, while real customers may share a reseller or be an affiliate of the operator. Any site may have load no record explains (GPU burn-in, an engineer's unlogged test run), a swapped grid meter, a surge in inference demand, part of a cluster switched off, or a scheduler time that is off by up to a day.

```powershell
python gen.py --n 200 --mess
python run.py --dry-run --generated 20 --mess --results results_mess_dry
```

The same 200 sites, tidy and messy (cheaters caught of 108, honest sites wrongly accused of 92):

| Method | Tidy | Messy |
|---|---|---|
| Fixed checks | 86 caught, 49 accused | 101 caught, 80 accused |
| Sensor rule | 91 caught, 36 accused | 91 caught, 44 accused |
| Tap rule | 41 caught, 6 accused | 40 caught, 6 accused |
| Script of Sol's routine | 104 caught, 0 accused | 98 caught, 6 accused |

The script was not changed after seeing the messy cases. No model has been run on them.

`--operator-model gpt-6-luna` lets a language model answer the `staff` channel in place of the script; it has not been run either.

By construction, on H1 to C4 the fixed checks catch 3 of the 4 cheaters and wrongly accuse 2 of the 4 honest operators. The question is whether the detective does better on both.

## Checks before outreach (25 Nov 2026)

Five checks, done before writing to the researchers whose work the simulator uses. `python reproduce.py` reruns
everything here that needs no model call.

### The two probe papers, now read

Both were first used through a citation in the power paper. Claude read them on 25 Nov (the HTML of version 1 of
each; Gargiulo and Kulp have a version 2 of 14 Nov that is unread).

- **Gargiulo and Kulp, arXiv:2609.00309.** A Rogowski current probe around the power cable of one H200, one
  5-second trace per reading. 97% accuracy at telling training, inference and other work apart, on model families
  not seen in training. Against evasion (their Table 1): a plain detector catches throttled training 74 to 92% of
  the time, diluted training 80 to 100%, diluted LoRA 30 to 74%. A hardened detector with that attack held out:
  100%, 99 to 100%, 48 to 88%, and 98 to 100% with their rescue rule. Evading cost 28 to 69% of training speed.
  Nothing on an operator refusing access.
- **Rahman and Tajdari, arXiv:2606.19262.** Nine GPU counters at 1 Hz. 98.2% with no evasion. Five rounds of
  attacker against defender; the 43 to 87% is the hardened detector against white-box attacks it had not seen, in
  round 5. That is their worst case. Across 14 ordinary single-GPU attacks the attacker evades 6.2% of the time.
  They conclude that defenders are favoured, if the counters can't be tampered with.

**What this means for the simulator.** `PROBE_ACC_DISGUISED = 0.65` matches a plain detector against the hardest
attack, or the white-box worst case. Against a hardened detector about 0.99 is fairer. The value is NOT changed:
it would alter the hand-built cases the models were scored on. Neither rule nor the script reads the probe, so
none of their numbers depend on it. The language models did use the probe.

### Do the unsourced settings matter? (`sweep.py`)

Each setting is changed alone; 200 generated sites (108 cheating, 92 honest). Cells are cheaters caught, honest
sites accused. Full tables in `sweep.log`, plot in `sweep.png`.

| Setting (default) | Range tried | Sensor rule | Tap rule | Script | Script, messy sites |
|---|---|---|---|---|---|
| Share of batch jobs that are periodic (0.5) | 0 to 1 | 91; 24 to 42 | 41; 6 | 104; 0 | 98; 6 |
| Wander of the line's frequency (0.04 Hz) | 0 to 0.15 | 87 to 91; 31 to 36 | 41; 6 | 104; 0 | 98; 6 |
| Error of the tap's estimate (30%) | 0 to 60% | 91; 36 | 41; 5 to 6 | 104; 0 | 97 to 98; 6 to 7 |
| Traffic of a low-communication run (1/100) | 1/1000 to 1/5 | 91; 36 | 41 to 52; 6 | 92 to 104; 0 | 88 to 98; 6 |
| Days a hidden run's line is still found (0.87) | 0.5 to 0.95 | 89 to 91; 36 | 41; 6 | 102 to 104; 0 | 97 to 98; 6 |

The ranking never changes. Two things do move. The sensor rule's false accusations follow the share of periodic
batch jobs, but even at zero it accuses 24 of 92. And the script loses 12 cheaters if a low-communication run
exchanges 1,000 times less than normal training instead of 100 times less: its tap threshold then sits above them.

### The hub's first test (`hub.py`)

The hub idea says a model's place is off site, revising the rules. This is the first time that was tried.

**Setup.** Sol (`gpt-6.2-sol`, through the ChatGPT login) got the frozen `script.py`, what the auditor is told
about the instruments, and the practice sites the script got wrong: for each, the evidence the script read, its
answer and the truth. It did not get the simulator's code. It replied with a whole new script. Two rounds, one
call each; in round 2 it saw 16 of the 37 sites its own first revision got wrong. A candidate runs behind a
wrapper that gives it the evidence channels and nothing else, so it cannot read the truth off a site.

- Practice: 200 messy sites, seed 0 (108 cheating, 92 honest).
- Unseen: 400 messy sites, seeds 1 and 2 (205 cheating, 195 honest), and 200 tidy sites, seed 1 (104, 96).
  Nothing was tuned on these, and the frozen script had never been run on them.

| Script | Practice: caught, accused | Unseen messy: caught, accused | Unseen tidy: caught, accused | Points per site |
|---|---|---|---|---|
| Frozen `script.py` (Claude, knew the simulator) | 98 of 108, 6 of 92 | 181 of 205, 17 of 195 | 98 of 104, 0 of 96 | 14 |
| Sol, round 1 (`hub/script_r1.py`) | 72 of 108, 1 of 92 | 146 of 205, 0 of 195 | 76 of 104, 0 of 96 | 20 |
| Sol, round 2 (`hub/script_r2.py`) | 101 of 108, 1 of 92 | 187 of 205, 0 of 195 | 98 of 104, 0 of 96 | 15 |

**What happened.**

- Round 1 traded one error for the other. Sol dropped the rule that customers sharing a payer are one run, and
  asked for two tap readings before any finding. False accusations went from 17 to 0 on unseen sites; missed
  cheaters went from 24 to 59. The message said accusing an honest site is the worse error, and Sol took that far.
- Round 2, shown the cheaters it now missed, got both: 18 missed and 0 accused on unseen messy sites, against the
  frozen script's 24 and 17. Wrong answers fell from 41 to 18 of 400. On tidy sites it matches the frozen script.
- So a model that is poor at committing to a verdict on site wrote a better fixed auditor off site, in two calls.

**What this does not show.**

- The unseen sites are new draws from the same recipe. The script met no cheating method it hadn't seen in
  practice. Holding out a whole method is the test that matters next.
- One model, one practice set, two rounds, no repeats. The reply is not deterministic.
- Sol saw truth labels and the notes that name each site's cheating method. A real hub would have those only for
  sites its own red team built.
- The frozen script is the baseline Sol started from, so this measures revising, not writing from nothing.

### The two physical tests on real GPU traces (`real_check.py`)

Hausenloy and Li publish telemetry from two rented hosts with two H100s each, with known truth
(huggingface.co/datasets/jasminexli/verifier-challenge-traces, CC-BY-4.0). The 23 MB of small files were
downloaded to `real_traces/data` (not in the repository): nvidia-smi at 1 Hz, NIC counters, NCCL logs, labels.
There are 14 phases: 12 training (3 of them mislabelled on purpose) and 2 inference.

| Test | Nearest thing in these traces | Right on |
|---|---|---|
| A. Training exchanges far more data between GPUs than inference | Volume of the NCCL logs: 30 to 75 kB/s in every training phase, 0.0 in both inference phases | 14 of 14 |
| B. Training leaves a periodic line in power | Spectrum of nvidia-smi power at 1 Hz | 7 of 14 |

What this does and doesn't show:

- Test A agrees with the simulator's tap, on a tiny sample with only two inference phases. An NCCL log is written
  by the operator's own software, so it is weaker evidence than a tap the auditor owns.
- Test B can't be judged from this data. At 1 Hz nothing above 0.5 Hz is visible, and the power paper's line is
  found with a high-rate meter. Six of twelve training phases still show a strong slow line (0.07 to 0.14 Hz).
- One assumption looks wrong here: the simulator gives batch inference 0.75 kW per GPU against 0.80 for training.
  In these traces inference draws 173 to 191 W and training 490 to 600 W. Their inference is a small model that
  doesn't fill the GPU, so this may not hold for large batch inference, but the grid meter may separate the two
  better than the simulator allows.
- The thresholds (1 kB/s; a line 50 times over the band's median) were written down before the first run and not
  adjusted.

### Is the limit too small?

The limit is 50,000 GPU-hours and the site has 2,000 listed GPUs, so the limit is 3.5% of a month's capacity:
about 70 GPUs for the whole month, or 700 for three days. People who work on treaty verification think in tens of
thousands of GPUs. Nothing in the simulator depends on the absolute size: power, traffic and the probe are per
GPU, and the limit is used only as a share of the site. Multiply everything by 50 for a 100,000-GPU site and a
limit of 2.5 million GPU-hours. What the small share does mean is that a violating run hides among the site's
ordinary work, which is the hard case and the reason the grid meter alone doesn't settle it.

## Run it

To rerun every table that needs no model (about two minutes, Python 3.10+, matplotlib optional; the real-trace step runs only if the traces are downloaded):

```powershell
python reproduce.py
```

The language-model runs below need a login and are not deterministic; their transcripts are in the `results_*` folders.

Needs Python 3.9+ and Claude Code logged in with a Claude subscription. No API key.

```powershell
python run.py --dry-run                           # scripted stand-in, no model calls
# delete the results folder, then:
python run.py --provider claude-cli --only H1,C2  # two cases first
python run.py --provider claude-cli               # all 8
```

- Results: `results/summary.md`, and one transcript per case in `results/cases/`.
- Calls are cached in `results/cache.jsonl`, so a rerun only makes missing calls.
- `--model` sets the detective's model (default `sonnet`). `--seeds 3` adds variants with shifted job timings. `--max-cost` stops a run at an estimated cost (default 10 USD).
- `--provider anthropic` or `openrouter` use an API key instead (`pip install requests`).

## Where the numbers come from

- Training leaves a periodic line in high-rate power data, detectable about 96% of the time at a 1% false-alarm rate: [Kimpson, Baker and Graham 2026](https://arxiv.org/html/2610.30182).
- Training exchanges about 1 GB/s between machines, inference about 10 kB/s: [Sarbakysh and Moskvin 2026](https://techgov.intelligence.org/blog/de-risking-interconnect-limits-for-ai-verification).
- Hiding the line: hidden in up to 73% of five-minute windows at 93 to 267% more compute, with at least 87% of runs still caught over a day; periodic non-training loads score as training in at least 97% of traces (same paper, synthetic data only).
- Cable current probe at 97% (Gargiulo and Kulp 2026) and chip telemetry falling to 43 to 87% under disguise (Rahman and Tajdari 2026): both first taken as cited in the paper above and read directly on 25 Nov 2026: see "Checks before outreach".
- GPU power levels, traffic per GPU-hour and prices are round numbers I chose, not measurements.

## Limitations

- **The scenarios are hand-built** so that each method's strengths and weaknesses show. Eight cases prove nothing statistically.
- **Operators follow scripts.** They don't adapt to what the detective asks, and staff answers are keyword lookups.
- **The cheaters don't try to evade the power sensor or the probe.** Published work shows evasion is possible at a cost.
- **The sealed memory probe is assumed to work** and to reach any chip by serial number. No such probe exists today.
- **The detective is told the physics and who vouches for each channel.** A real one would have to learn a site's systems.
- **No enclave:** this tests the investigating, not the sealing.
