# Proof-Driven Development (PDD)

**TDD for agents: rules, gates, receipts. No magic — evidence.**

AI coding agents are fast but confidently wrong. They mark work "done" without
proof, add abstractions nobody asked for, and forget what happened last session.
PDD is a small, portable protocol that makes their claims checkable:

- a **tiny always-on kernel** of rules (never more than ~200 lines),
- **procedures loaded on demand** (skills), not pasted into every prompt,
- **gates**: "done" means a command and its raw output, not a vibe,
- **red-team passes** before anything is called finished,
- **evals as unit tests** for the agent itself (pass@k / pass^k, baselines),
- **durable state**: task files and memory that survive compaction.

## What this is not

This is **not an AGI**, not a framework, and not a promise that an agent will
write "the best code in the world". No prompt does that. What this gives you is a
loop that is measurable, honest about failure, and cheap in context — the three
things that actually separate reliable agents from demos.

## The seven principles

See [`docs/PRINCIPLES.md`](docs/PRINCIPLES.md). In one line each:

1. **Small kernel** — rules always on, procedures on demand (progressive disclosure).
2. **One home per rule** — no duplicates across kernel, skills, and docs.
3. **Evidence, not assertions** — a test that cannot fail is not a test.
4. **Red team** — attack the change before shipping it.
5. **Evals** — treat prompts and rules like code: measure, regress, baseline.
6. **Lazy first** — climb the ladder before writing anything new.
7. **Durable state** — write the plan to a file; memory outlives the session.

Plus two operating rules: **honest refusal** ("not verified: <reason>") and
**human gate** for irreversible actions (push, prod, publishing).

## Quick start

```bash
# 1. Put the kernel where your agent reads its rules
cp AGENTS.md ~/.config/opencode/AGENTS.md      # or your project root

# 2. Install the skills (on-demand procedures)
cp -r skills/* ~/.config/opencode/skills/

# 3. Check the setup
python scripts/doctor.py --root .
```

Then, on your first real task, ask the agent to run the loop: plan → test →
implement → review → verify → remember. The kernel tells it how; the skills tell
it the procedures; the gates tell it when to stop.

## Repo map

```
AGENTS.md          the kernel template (<=200 lines, <=35 KB)
docs/              principles, evidence gates, context engineering
skills/            7 on-demand procedures
scripts/           doctor.py, skill_inventory.py, recall.py (read-only, stdlib only)
knowledge/         empty registries: patterns, threads, negative results
examples/          one worked A/B case study (sanitized)
```

## Status

v0.1 — a distilled, sanitized snapshot of a protocol that has been used daily on
real projects. It is opinionated and incomplete on purpose: start small, add a
rule only when its absence caused a real mistake.

## License & attribution

MIT. Ideas are synthesized from the field and credited in
[`docs/PRINCIPLES.md`](docs/PRINCIPLES.md): TDD, SWE-bench-style evals,
[Ponytail](https://github.com/DietrichGebert/ponytail) (lazy ladder),
[Superpowers](https://github.com/obra/superpowers) (design-before-code),
[ECC](https://github.com/affaan-m/ECC) (eval harness, context compaction),
Anthropic's context-engineering guidance, and the AGENTS.md specification.
No third-party text is copied verbatim.
