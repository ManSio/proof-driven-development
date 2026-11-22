# Case study: does a minimalist ruleset help — measured

A sanitized summary of a real A/B run on a small, self-contained coding task.
It is included because the methodology is part of PDD: decisions about rules
should be measured, not argued.

## Question

Does a minimalist "lazy senior dev" ruleset (a 7-rung code ladder, "one small
test", "end your reply with what you skipped") change the output when the agent
already runs under an evidence-first protocol?

## Design

- **Frozen input:** one held-out PRD (a small stdin line-frequency CLI with a
  MUST/STUB/NEVER table and 13 acceptance checks), written for the experiment.
- **Arms:** 2 control runs, 2 treatment runs; same model, same brief, isolated
  fresh contexts; treatment added the ruleset verbatim.
- **Scoring:** fully mechanical (subprocess + exact stdout/exit-code comparison,
  line counts, perf run on 2,000,000 input lines).
- **Pre-registration:** hypotheses and decision thresholds written before the runs.
- **Calibration before the measurement:** a reference implementation had to score
  13/13, and a deliberately broken variant had to redden exactly the checks it broke.

## What calibration caught (before any arm was scored)

1. Windows pipes translate `\n` to `\r\n` — exact-match comparison failed on
   correct code until the harness normalized newlines.
2. A CP1251 console crashed the scorer when printing Unicode failures —
   `reconfigure(utf-8)` fixed the harness, not the solutions.
3. Child processes decoded stdin with the locale codepage while the spec declared
   UTF-8 — running children with `-X utf8` restored the promised contract.

Lesson: a harness that cannot pass a known-good input measures itself.

## Results

| Arm | Condition | Acceptance | Lines (total/code) |
|---|---|---|---|
| c1 | control | 13/13 | 84/65 |
| c2 | control | 13/13 | 79/62 |
| t1 | ruleset | 13/13 | 56/45 |
| t2 | ruleset | 13/13 | 26/21 |

- Treatment ≈ **50% of control lines** with equal correctness; arms did not overlap.
- n=2 per arm: the direction was consistent, but an exact permutation test gives
  p≈1/6 — **not significant**. Reported as a pilot, not proof.
- The incremental gain looked stylistic (manual arg parsing vs `argparse`,
  docstrings, helper functions), not architectural: the control was already lean
  because the surrounding protocol rewarded minimal diffs.

## Red team on our own experiment

- One task, one model, two runs per arm — noise cannot be excluded.
- The task shape (stdlib solves everything) favors the ladder; results may differ
  on UI or systems work.
- The brief's "one file only" rule suppressed in-file self-tests, weakening one
  hypothesis we wanted to test.
- Isolation was instructed, not technically enforced.

## Takeaway

Measure the rules you add; keep the artifacts in the repo; report p-values and
confounds honestly. A rule that survives a pilot gets another round — not a
celebratory README.
