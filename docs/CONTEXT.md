# Context engineering

The context window is a budget, not a bucket. Three numbers govern PDD:

| Item | Budget | Why |
|---|---|---|
| Kernel (`AGENTS.md`) | ≤200 lines, ≤35 KB | re-read on every step |
| One skill `description` | ≤400 characters | loaded at session start, every step |
| One skill body | ≤10 KB | loaded only when the skill fires |

## Progressive disclosure

- **Always on:** rules and pointers (kernel).
- **On demand:** procedures (skills) — loaded when their `description` matches the task.
- **Never preloaded "just in case":** a catalog of hundreds of skills wastes the
  budget and buries the relevant instruction.

## Compaction at phase boundaries

Compact (or write state, then start fresh) when the phase changes — not mid-task:

| Transition | Compact? | Why |
|---|---|---|
| Research → Planning | yes | research is bulky; the plan is the distilled output |
| Planning → Implementation | yes | the plan is in a file; free context for code |
| Implementation → Testing | maybe | keep if tests reference recent code |
| Debugging → next feature | yes | traces pollute unrelated work |
| Mid-implementation | **no** | losing names, paths, partial state is costly |
| After a failed approach | yes | clear the dead end before retrying |

**What survives:** files on disk, git state, memory registries, the kernel.
**What is lost:** intermediate reasoning, file contents read earlier, verbal
preferences. Therefore: **write the plan and the state to a file before compacting.**
Do not rely on a task list surviving — it may not exist; a file always does.

## Memory that outlives a session

- `knowledge/PATTERNS.md` — error classes with a guard and a source.
- `knowledge/THREADS.md` — open threads, not incidents (max 10).
- `knowledge/NEGATIVE.md` — things that did not work, so they are not retried blindly.
- Task state file — current plan, decisions, next action, open questions.

Rule: **no registry line without a source**. An empty registry is a fact
(`exit 2`), not "nothing found".
