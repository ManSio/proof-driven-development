---
name: evidence-gates
description: Turn claims into receipts: acceptance criteria first, golden and failure paths, mutation check, held-out cases, degenerate runs, honest numbers. Use when claiming done/works/confirmed, publishing a number, or when a check reports nothing.
---
# Evidence gates

A receipt is a command, its raw output, and the tree hash. Missing any of the
three — it is not a receipt.

```
command:  pytest tests/test_parser.py -q
output:   12 passed in 0.41s
tree:     4f2a1c9
```

## Gate ladder

1. **Criteria before code.** Each acceptance check is binary and checkable.
2. **Golden plus failure path.** Show both runs, raw.
3. **Mutation check.** Break the implementation; the test must go red. Green on
   broken code = the test was never testing that line.
4. **Held-out.** Confirmed on the original case → `confirmed on known case`.
   "Works in general" needs a new, unrelated input.
5. **Degenerate run.** Zero units, empty input, warm cache. A plausible result
   from a degenerate run → `not proven`.
6. **Artifact, not capability.** `N of M` on the shipped artifact, not "the code can".

## Numbers

- Unit + denominator. Rates only after classifying the whole population.
- 0% and 100% are flagged, never silently reported.
- The interpreter counts; the model never does arithmetic it can run.
- Empty sample → `exit 2`, never "0%".
- A counter is not provenance; `N > 0` is not homogeneity.
- Use the artifact's own counter when it exists; custom parser only after a control.

## When a check reports nothing

Silence is suspicious, not reassuring. Prove the checker can fail: feed it a
known-bad input and show red. Then re-run on the real input. Three states:
measured and absent · could not measure · measured the wrong thing.

## Report

End with the ledger; a ✅ only when every row is confirmed or explicitly refuted:

```
| # | Claim | Evidence (command / file:line / hash) | Status |
```
