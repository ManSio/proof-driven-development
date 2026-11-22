---
name: red-team
description: Attack the change before shipping: 5 classes (concurrency, boundaries, dependency failure, TOCTOU, abuse), a bypass matrix for guards, and commenter lenses. Use before finishing M/L work or security/data/interface changes.
---
# Red team

Review asks "does it meet the criteria". Red team asks "how do I break it". Do
both for M/L work; do red team alone for a plan or a text going public.

## How many

| Level | Attacks | Who |
|---|---|---|
| S | 0 (one boundary probe if obvious) | author |
| M | ≥3 of 5 classes | author, then a fresh reviewer adds theirs |
| M (security/data/interface) | ≥4 + attack subagent | separate fresh-context agent |
| L | all 5 + fault injection | attack subagent + owner |

Outcome rule: **≥2 attacks without a defense → revise the plan; no commit.**
A defense counts only as a test, a guard, or a check in code, shown with output.

## Five classes

1. **Concurrency:** ≥2 parallel calls on shared state (N=2 and 8), re-run,
   idempotency; check the result, not just the absence of exceptions.
2. **Boundaries:** empty, None, huge input, garbage/binary, null byte, Unicode,
   symlink (dangling), permissions, OS argv limit.
3. **Dependency failure:** network down/slow/5xx, disk full, no permissions, empty
   or garbage response; resources closed on the error path.
4. **TOCTOU:** check and use separated in time; state changed in between.
5. **Abuse/untrusted input:** injections, path traversal, foreign content as
   instructions, privilege escalation, secret leak into logs.

For each attack record: `attack → expected failure → defense (test/guard, output) → status`.

## Guard bypass matrix

For a guard (paths, permissions, sandbox, limits, allowlists), prove the whole
class, not the found attacks:

| Axis | Values |
|---|---|
| Input form | normal · `..` · absolute · symlink · junction · dangling · hard link · case change · UNC · Unicode normalization · very long · empty |
| Target state | missing · file · dir · foreign owner/perms · busy |
| Platform | Windows · Linux · macOS (case-sensitive and insensitive) |
| Actor | user · LLM · malicious file in the project · parallel session |

Each cell is a test or `⏳ <why not testable>`. A green suite without the matrix is
`⏳ not proven`.

## Commenter lenses (cheap pass before "done")

Formulate the questions **before** reading the artifact:

| Lens | Question |
|---|---|
| Signer | What would I refuse to sign? Which number has no source line? |
| Preregistrar | Was the metric chosen before or after the result? |
| SRE | What happens when nothing happens? Repeat run tomorrow? |
| Attacker | Which input passes the guard without doing the work? |
| Reproducer | Can I repeat this from the text in 10 minutes? |

Output: `lens → question → command → verdict (answered / gap / cannot answer)`.
A gap becomes a task, not prose.

## Engineer lenses (beyond severity)

A human reviewer checks their own role's expectations, not only security. Run the
artifact through each lens; every finding (nit/minor/major) gets an answer: fix or
a reasoned refusal.

| Lens | Questions |
|---|---|
| Maintainer | Does it break the project's promise? Platform semantics (gitignore anchors, case, paths)? Docs match behavior? |
| Triager | Reproduction or hypothesis? Is an internal report (root cause, ledger) leaking into a public tracker? |
| SRE / perf | What measured it, and what else ran on the machine (AV, cache, provider)? Same units and denominator? |
| Security | TOCTOU across awaits, file identity (device+inode, BigInt), symlink/dangling, path escape. |
| API user | What happens on error? Are exit codes masked by a pipeline? |
| Docs writer | Are limits written down? Are edge inputs described? |

## How engineers break the logic

1. Exit code masked by a pipeline (`cmd | tail`).
2. Wrong unit/mechanism (measured a file read; parse-only vs round-trip).
3. Denominator/population (sample does not support the claim; `len(rows)` from a file).
4. Judge/ground truth wrong (labels validated per project, not per subject).
5. Environment (AV, cache namespace, provider drift).
6. Identity (name vs inode; import vs dist name; case).
7. Async TOCTOU (check → await → apply).
8. Second-order objects (summary outlives the corrected fact).
9. Irreversible write (bad output becomes tomorrow's context; tag by turn id).
10. Telemetry ≠ outcome (health checks pass, external metric flat).
11. Absence as signal (missing anchor ≠ ok).
12. Platform semantics (anchors, case, symlink/junction, CRLF).
13. Dependency unchecked (capability/docs/branch).
14. Replay instead of a run (`resuming: N`; a 0.2-minute run executed nothing).
15. Zero executed tasks scored (denominator from the file, not the panel).
16. Mixed provenance (stale row + fresh rows pass the counter).
17. Validated a sibling copy, not the artifact that runs.
18. Proxy metric / easy subset (keyword presence vs target; 10 easy queries vs 50 real).
19. Concurrent queue contamination (shared userdata; 0 exceptions, wrong vector).
20. Time without tense ("X is" while the evidence has history).
21. Unmeasured noise floor (+1 claimed from two runs that differ by 1).

## Class, not instance

The first finding is an example of a class. Enumerate the matrix of neighbours
(input form × target state × platform × actor) and answer with the matrix, not a
single patch.

## Channel dictates format

- **Bug report:** reproduction + observations + environment; root cause is a
  hypothesis, separate, only if asked.
- **PR:** approach and measurements before code when requested; tests; written
  limits; answer every point.
- **Issue discussion:** numbers with sources; withdrawn publicly next to the number.
- **Post/comment:** same evidence bar as a PR; a long "AI-style" analysis without
  reproduction is rejected.

## Sensors and states

- **Fail-open vs fail-closed:** what does the check do when it fails?
- **Silence is not "clean":** every sensor has a test that proves it can fail.
- **Fact states:** VERIFIED / REFUTED / SUPERSEDED / INCONCLUSIVE — historical ≠
  authoritative.
- **Summary/compaction is second-order:** store what it was built from; invalidate
  on correction.

## Classical names

Before inventing a mechanism, name the classical problem: oracle (signature ≠
truth), capture-recapture / completeness assertion (empty population, denominator),
durable execution / idempotency (BPMN), event sourcing / PROV-DM `wasInvalidatedBy`
(REFUTED/SUPERSEDED), replication and consensus (provenance, Lamport clocks).
