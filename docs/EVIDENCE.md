# Evidence gates

A **receipt** is the smallest unit of "done": a command, its raw output, and the
tree hash it was run on. If any of the three is missing, it is not a receipt.

```
command:  pytest tests/test_parser.py -q
output:   12 passed in 0.41s
tree:     4f2a1c9
```

## The gate ladder

1. **Acceptance criteria before code.** Each is binary and checkable
   ("`-k 0` prints nothing, exit 0"), not an adjective ("handles edge cases").
2. **Golden path + failure path.** Show both runs. A feature that only proves the
   happy path is half-proven.
3. **Mutation check.** Break the implementation (invert a condition, delete a line)
   and show the test go red. A test that stays green was never testing that line.
4. **Held-out.** A fix confirmed on the original case is `confirmed on known case`,
   not "works in general". Generalization needs a new, unrelated input.
5. **Degenerate run.** Before "verified", run with zero units, empty input, and a
   warm cache. If the tool prints a plausible result, the verdict is `not proven`.
6. **Artifact, not capability.** "The code can do X" is not "the shipped data has X":
   prove `N of M` on the artifact.

## Numbers

- Every number: unit + denominator (`17 of 23 arms`, not `74%`).
- Rates only after classifying the whole population; 0% and 100% are flagged.
- The interpreter produces the number; the model never does arithmetic it can run.
- An empty sample is `exit 2`, never "0%".
- A counter is not provenance: `N > 0` says something happened, not that it is uniform.
- If an artifact has its own counting tool, use it; a custom parser only after a
  control on an input whose answer is known.

## Reporting

The report ends with the ledger:

```
| # | Claim | Evidence (command / file:line / hash) | Status |
|---|---|---|---|
| 1 | ... | ... | ✅ / ⏳ / ❌ |
```

A ✅ is allowed only when every row is confirmed or explicitly refuted. Status
words are calibrated: `Verified` / `Committed, not pushed` / `Code changed, not
runtime-tested` / `Reported, not confirmed`.
