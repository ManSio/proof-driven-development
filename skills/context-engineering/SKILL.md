---
name: context-engineering
description: Keep context lean: budgets, progressive disclosure, compaction at phase boundaries, durable state in files. Use in long sessions, near context limits, on phase switches, or when compaction is due.
---
# Context engineering

The window is a budget, not a bucket.

## Budgets

| Item | Budget | Why |
|---|---|---|
| Kernel | ≤200 lines, ≤35 KB | re-read every step |
| Skill description | ≤400 characters | loaded at session start |
| Skill body | ≤10 KB | loaded on demand |

## Progressive disclosure

- Always on: rules and pointers.
- On demand: procedures (skills), matched by description.
- Never preload "just in case": a large catalog buries the relevant instruction.

## Compaction at phase boundaries

| Transition | Compact? | Why |
|---|---|---|
| Research → Planning | yes | research is bulky; the plan is the distilled output |
| Planning → Implementation | yes | the plan is in a file; free context for code |
| Implementation → Testing | maybe | keep if tests reference recent code |
| Debugging → next feature | yes | traces pollute unrelated work |
| Mid-implementation | **no** | losing names, paths, partial state is costly |
| After a failed approach | yes | clear the dead end before retrying |

## What survives

Files on disk, git state, memory registries, the kernel.
Lost: intermediate reasoning, earlier file contents, verbal preferences.

**Therefore: write the plan and the task state to a file before compacting.** Do
not rely on a task list surviving — it may not exist; a file always does. After
compaction, resume from state → diary → next action.

## Memory across sessions

- `knowledge/PATTERNS.md` — error classes with a guard and a source.
- `knowledge/THREADS.md` — open threads (max 10).
- `knowledge/NEGATIVE.md` — approaches that failed, so they are not retried blindly.
- Task state file — plan, decisions, next action, open questions.

No registry line without a source. An empty registry is `exit 2`, not "nothing found".
