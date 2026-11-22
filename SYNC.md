# Sync model

Two trees, one source:

- **this repo (PDD)** — public, sanitized, generic: rules, skills, scripts, templates.
- **your local agent config** (`~/.config/opencode`) — the full private instance: personal paths, project registries, diaries, secrets.

Direction: **local is the source; PDD is the projection.** Improve rules locally,
then port only the generic part here.

## Publishing a change

1. Copy the generic change into the matching file here. Never copy private paths,
   hostnames, keys, diaries, or registry content.
2. Run both gates; they must exit 0:
   ```bash
   python scripts/doctor.py --root .
   python scripts/skill_inventory.py --root .
   ```
3. Scan for private data — the result must be empty:
   ```bash
   grep -RInE 'C:\\Users|D:\\Project|192\.168\.' .
   ```
4. Commit with Conventional Commits. Push only on an explicit owner command.

## Pulling a change (rare)

The public repo is usually behind the local instance. When it is ahead, apply the
change by hand to the local config (the local file is richer), then re-run the
local doctor. Do not copy this repo wholesale over a live config.

## Versioning

Kernel and skills are small; dates in file headers plus `CHANGELOG.md` are enough.
Record the PDD commit you synced in your local `knowledge/THREADS.md`.
