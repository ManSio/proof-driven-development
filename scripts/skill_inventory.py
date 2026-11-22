#!/usr/bin/env python3
"""Skill inventory: format, budget, and host-neutrality checks. Read-only.

Checks per skill
  - SKILL.md exists; id is kebab-case; `name:` in frontmatter equals the directory
  - `description:` present and <= 400 chars (loaded on every step)
  - no Claude-only tokens ($CLAUDE_*) — skills must be host-neutral
  - `$ARGUMENTS` is a WARN (host placeholder, may not be substituted)
  - no two skills with identical SKILL.md content

Exit codes: 0 clean (warnings allowed) · 1 findings · 2 cannot measure.

Usage
  python scripts/skill_inventory.py --root .
  python scripts/skill_inventory.py --selftest
"""
import argparse
import hashlib
import re
import sys
import tempfile
from pathlib import Path

ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_DESC = 400
HOST_TOKEN_RE = re.compile(r"\$CLAUDE_[A-Za-z_]+")


class CannotMeasure(Exception):
    pass


def read_front_matter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    data = {}
    for line in text[3:end].splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            data[key.strip().lower()] = value.strip().strip('"').strip("'")
    return data


def audit(root: Path) -> tuple[list, list, int]:
    skills = root / "skills"
    if not skills.is_dir():
        raise CannotMeasure(f"skills/ not found under {root}")
    entries = sorted(p for p in skills.iterdir() if p.is_dir() and not p.name.startswith("."))
    if not entries:
        raise CannotMeasure(f"no skill directories in {skills}")

    fails, warns, checks = [], [], 0
    hashes = {}
    for entry in entries:
        checks += 1
        skill_md = entry / "SKILL.md"
        if not skill_md.is_file():
            fails.append(f"{entry.name}: SKILL.md missing")
            continue
        if not ID_RE.match(entry.name):
            fails.append(f"{entry.name}: id is not kebab-case")
        text = skill_md.read_text(encoding="utf-8-sig")
        fm = read_front_matter(text)
        name = fm.get("name", "")
        if not name:
            fails.append(f"{entry.name}: no name in frontmatter")
        elif name != entry.name:
            fails.append(f"{entry.name}: name '{name}' does not equal the directory")
        desc = fm.get("description", "")
        if not desc:
            fails.append(f"{entry.name}: no description")
        elif len(desc) > MAX_DESC:
            warns.append(f"{entry.name}: description {len(desc)} chars (> {MAX_DESC}) - costs context on every step")
        host = sorted(set(HOST_TOKEN_RE.findall(text)))
        if host:
            fails.append(f"{entry.name}: Claude-only token(s) {', '.join(host)} - skills must be host-neutral")
        if "$ARGUMENTS" in text:
            warns.append(f"{entry.name}: contains $ARGUMENTS (host placeholder) - resolve or declare it")
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        if digest in hashes:
            fails.append(f"{entry.name}: identical SKILL.md to {hashes[digest]}")
        else:
            hashes[digest] = entry.name
    return fails, warns, checks


def selftest() -> int:
    controls = {}

    def check(name, cond):
        controls[name] = bool(cond)
        print(f"{'PASS' if cond else 'FAIL'}  {name}")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        base = root / "clean" / "skills" / "good-one"
        base.mkdir(parents=True)
        (base / "SKILL.md").write_text("---\nname: good-one\ndescription: d\n---\nbody\n", encoding="utf-8")
        clean = audit(root / "clean")
        check("clean tree passes", not clean[0])

        bad = root / "bad" / "skills"
        (bad / "good-one").mkdir(parents=True)
        (bad / "good-one" / "SKILL.md").write_text("---\nname: good-one\ndescription: d\n---\n", encoding="utf-8")
        (bad / "Bad_Id").mkdir()
        (bad / "Bad_Id" / "SKILL.md").write_text("---\nname: X\ndescription: y\n---\n", encoding="utf-8")
        (bad / "no-desc").mkdir()
        (bad / "no-desc" / "SKILL.md").write_text("---\nname: no-desc\n---\n", encoding="utf-8")
        (bad / "copy").mkdir()
        (bad / "copy" / "SKILL.md").write_text((bad / "good-one" / "SKILL.md").read_text(encoding="utf-8"), encoding="utf-8")
        (bad / "host-leak").mkdir()
        (bad / "host-leak" / "SKILL.md").write_text("---\nname: host-leak\ndescription: h\n---\ncd $CLAUDE_PROJECT_DIR\n", encoding="utf-8")
        fails, warns, _ = audit(root / "bad")
        check("bad id fails", any("Bad_Id" in f for f in fails))
        check("missing description fails", any("no-desc: no description" in f for f in fails))
        check("duplicate content fails", any("identical SKILL.md" in f for f in fails))
        check("host token fails", any("host-leak" in f and "Claude-only" in f for f in fails))

    ok = all(controls.values())
    print(f"RESULT: {'PASS' if ok else 'FAIL'} ({sum(controls.values())}/{len(controls)} controls)")
    return 0 if ok else 1


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Skill inventory (read-only).")
    parser.add_argument("--root", default=".", help="protocol root (default: .)")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    try:
        fails, warns, checks = audit(Path(args.root).resolve())
    except CannotMeasure as exc:
        print(f"CANNOT MEASURE: {exc}", file=sys.stderr)
        return 2
    for msg in fails:
        print(f"[FAIL] {msg}")
    for msg in warns:
        print(f"[WARN] {msg}")
    print(f"\n{checks} checks, {len(fails)} fail, {len(warns)} warn")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
