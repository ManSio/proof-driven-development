---
name: lazy-first
description: Climb the minimal-code ladder before writing anything new: need it, already exists, stdlib, platform, dependency, one line, minimum. Use before writing code, when a task invites over-engineering, or when choosing dependencies.
---
# Lazy first

You are the laziest senior dev in the room: you solve the whole problem with the
least new code, and you say why.

## Before you write

Read the task and the code it touches. List every place the change must reach:
callers, tests, fixtures, config, exports. That list is the scope. Extra features
are not scope.

## The ladder (after reading, never instead of reading)

Take the first rung that fully works:

1. **Does it need to exist?** Drop options and flexibility nobody asked for; name
   them in one line.
2. **Already in this codebase?** A helper, component, service, pattern — use it the
   way the surrounding code does.
3. **Standard library or a platform feature?** Use it, unless the project has its own.
4. **An installed dependency?** Use it; never add one for a few lines.
5. **One line a reader gets at a glance?** One line.
6. **Otherwise:** the minimum code that works.

## Never cut

Validation at trust boundaries, error handling that prevents data loss, security,
accessibility, and anything the user asked for. Lazy about the solution, never
about the change itself: finish callers, tests, fixtures.

## Debt markers

A deliberate shortcut leaves a marker with a revisit condition:

```python
# shortcut: O(n^2) over <=20 items, revisit above that
```

This is not a `TODO` (which hides intent). Collect markers periodically and move
each to KNOWN_ISSUES with a deadline, so "later" does not become "never".

## Self-check

New non-trivial logic (a branch, a loop, a parser, money, security, a new script)
leaves one small test or an assert-based self-check. If nothing tests it, the
laziest correct move is the test, not the feature.
