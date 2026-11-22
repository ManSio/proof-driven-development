# Contributing

Thanks for helping. This repo values **evidence over volume**.

## House rules

1. **One home per rule.** A rule lives in the kernel *or* a skill *or* a doc,
   never in two places. If you need it always-on, put it in `AGENTS.md`; if it
   is a procedure, put it in a skill.
2. **Every rule is checkable.** If a rule cannot be verified by a command or a
   file check, it is advice, not a rule — say so.
3. **Descriptions are a budget.** A skill's `description` is loaded on every
   step; keep it under 400 characters and make it say *when* to load the skill.
4. **No copied text.** Synthesize ideas in your own words and credit sources.
5. **Commit messages** follow Conventional Commits (`type(scope): desc`).
   Atomic commits; never `git add -A`.

## Adding a skill

Copy `skills/evidence-gates/SKILL.md` as a starting point:

```markdown
---
name: <kebab-case, must equal the directory name>
description: <what it does + WHEN to load it, <=400 chars>
---
# <Title>
Read when: <one condition>.
## <procedure>
```

Checklist before a PR:

```bash
python scripts/doctor.py --root .
python scripts/skill_inventory.py --root .
```

Both must exit 0 (warnings are fine). Include in the PR: what you changed, the
commands you ran, and what you did **not** verify.

## What we won't merge

- rules that weaken verification ("skip tests to go faster") or add special-casing,
- skills that execute network calls or install dependencies,
- personal paths, internal host names, or real secrets — even in examples,
- marketing claims ("writes the best code in the world") — be precise instead.
