# Changelog

All notable changes to this project are documented here. Format: Keep a
Changelog; versioning: Semantic Versioning.

## [0.1.0] - 2026-11-23

Initial distilled release.

- Kernel template `AGENTS.md` (<=200 lines, <=35 KB) with task levels S/M/L,
  evidence gates, red team, DoD, number honesty, security, git, memory.
- Seven skills: `evidence-gates`, `red-team`, `eval-lab`, `research-first`,
  `lazy-first`, `brainstorm-first`, `context-engineering`.
- Portable, stdlib-only scripts: `doctor.py`, `skill_inventory.py`, `recall.py`.
- Empty knowledge registries (patterns, threads, negative results).
- One sanitized A/B case study in `examples/`.

## [0.2.0] - 2026-11-23

- `red-team`: professional lenses beyond severity, 21 engineer-break classes,
  class-not-instance, channel-fit, sensors and fact states, classical-name lens.
- `eval-lab`: provenance — a score must prove it ran; replay is opt-in; mixed
  revisions are refused.
- `SYNC.md`: local → public projection model.
- `scripts/sync_public.py`: publish gate (whitelist + scrub + both protocol gates).
- GitHub Actions: `doctor` and `skill_inventory` (with selftests) on Python 3.10
  and 3.12 for every push and pull request.

