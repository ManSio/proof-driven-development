---
name: eval-lab
description: Measure agents like code: frozen inputs, control vs treatment, a mechanical rubric, pass@k and pass^k, regression baselines, artifacts in the repo. Use to compare prompts/instructions or to test whether a rule actually works.
---
# Eval lab

Evals are the unit tests of agent work: define the expected behavior before the
change, run it continuously, track regressions.

## Principles

1. **Fixed instances.** One valid task for every condition, with a known reference
   answer. Compare against the reference, not against a vibe.
2. **Objective metric, not an LLM judge.** Yes/no on verifiable artifacts: was the
   command really run? does the number match real output? does the file exist?
3. **Multiple runs.** One run is noise. ≥5 per condition; report pass@1, pass@3,
   median. **pass^k** (all k succeed) is stricter — use it for critical paths and regressions.
4. **Control group.** Same setup without the factor; otherwise you cannot attribute
   the effect.
5. **Equal conditions and isolation.** Fresh context per run, same commands, same
   environment, no leakage between runs.
6. **Pilot then full run.** 1–2 runs to calibrate the rubric and the harness; only
   then the full measurement.
7. **Trace every run.** Keep the command log so numbers and failures can be rechecked.

## Regression evals (baseline)

A stable set: `baseline` (commit/state) → same checks PASS/FAIL → compare with the
previous run (`X/Y` vs the old `Y/Y`). A regression is a drop in passing checks.
Keep the baseline as `experiments/<task>/baseline.json`.

## Checklist

```
Task (instance):   one fixed, valid task with a reference result
Conditions:        A = control · B = treatment · ...
Runs per condition: ≥5, isolated, pass@k / median
Rubric:            yes/no, by artifact — written BEFORE the run
Log:               command trace per run
Report:            pass@k + failure share per condition + verdict
```

## Artifacts

Only in the repository: `experiments/<task>/{frozen/, results.json, REPORT.md}`.
Temp directories are banned: they vanish, and the report is left without evidence.

## Anti-patterns

- One or two runs → "it works / it doesn't".
- Judging by impression or an LLM grader instead of verifiable yes/no.
- Different environments per arm.
- Full measurement before the pilot.
- Reporting raw pass rate instead of pass@k / pass^k.

## Provenance

A score must prove it ran: print `executed=N resumed=M`, refuse a replay without an
explicit flag, and stamp every row with the product revision and corpus head. Refuse
mixed provenance instead of filtering it. A capture committed to git is a
reproducibility landmine — a "stable" number may be a file read.

