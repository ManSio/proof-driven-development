# Principles

PDD synthesizes the parts of the field that survive contact with real work.
Each principle below names its source and its trade-off — a principle without a
cost is marketing.

## 1. Small kernel, procedures on demand
**Source:** Anthropic's context-engineering guidance ("smallest set of high-signal
tokens"), the AGENTS.md spec (Red Hat / GitHub: <150–200 lines), ECC's progressive
disclosure.
**Rule:** the always-on file contains rules and pointers, never procedures. Every
step the model re-reads it; every unnecessary line dilutes the lines that matter.
**Cost:** the model must *decide* to load a skill. Mitigation: a Bootstrap line in
§2 and imperative descriptions ("Use when…").

## 2. One home per rule
**Source:** AGENTS.md ecosystem advice ("the duplication trap").
**Rule:** a rule lives in the kernel OR a skill OR a doc. Duplicates drift and give
the model contradictory signals.
**Cost:** some repetition feels "thorough"; it is a bug. `doctor.py` warns on
duplicate sentences.

## 3. Evidence, not assertions
**Source:** TDD practice, Superpowers' `verification-before-completion`, SWE-bench
(reproducible instances and pass rates), our own field lesson: a green suite on
broken code proves nothing.
**Rule:** "done" = a command and its raw output; a test is valid only if it reddens
when the code is broken; a claim not backed by a run is labeled `not verified`.
**Cost:** slower. That is the point.

## 4. Red team before "done"
**Source:** our own practice; security-review guidance (bypass matrix); the
"commenter" idea (readers find what audits miss, because they ask about what is absent).
**Rule:** M/L work gets ≥3 attacks from 5 classes (concurrency, boundaries,
dependency failure, TOCTOU, abuse) before it is called finished; guards are proven
by a matrix, not by a list of found holes.
**Cost:** extra passes; value shows up in the bugs that never ship.

## 5. Evals as unit tests for the agent
**Source:** ECC's eval-harness (capability vs regression evals, pass@k/pass^k),
SWE-bench methodology, our A/B case study (see `examples/`).
**Rule:** compare control vs treatment on frozen inputs; score mechanically, not by
a "judge"; ≥5 runs per arm for claims; artifacts in the repo; baseline each run.
**Cost:** experiments are expensive; run them for decisions that matter.

## 6. Lazy first
**Source:** Ponytail (MIT) — "the best code is the code you never wrote".
**Rule:** climb the ladder (need it at all → already in the codebase → stdlib →
platform → dependency → one line → minimum) *after* reading the code, never instead
of it. Never cut validation, security, accessibility.
**Cost:** the solver must resist building "for later".

## 7. Durable state
**Source:** 12-Factor Agents (own your context; stateless reducer; unify state),
Anthropic's memory/compaction guidance, ECC's strategic-compact.
**Rule:** write the plan to a file; compact at phase boundaries, not mid-task;
registries (patterns/threads/negative results) carry lessons across sessions.
**Cost:** a small bookkeeping habit; it pays back the first time a session dies.

## Operating rules

**Honest refusal.** "Cannot verify" is a first-class result: `not verified: <reason>`
plus the next check. It is never replaced by a plausible guess.
**Human gate.** Irreversible actions (push, prod, publishing) require an explicit
command. Autonomy is earned per action class, not assumed.

## What we deliberately reject

- **Giant catalogs** (hundreds of skills installed at once): every description is
  paid on every step; most add noise, not capability.
- **Hard hooks by default**: a broken hook can take down every session. PDD starts
  soft (instructions) and lets you add enforcement once it has tests.
- **"Best code in the world" promises**: unfalsifiable. This repo promises
  checkable claims and a loop you can measure.
