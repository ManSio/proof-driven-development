#!/usr/bin/env python3
"""PDD doctor: keep the protocol tree sane. Read-only, stdlib only.

Checks
  1. kernel budget     AGENTS.md <= CORE_LIMIT bytes (growth guard)
  2. skill refs        every `skill `<name>`` in AGENTS.md resolves to skills/<name>/SKILL.md
  3. section refs      every §N / §N.M in AGENTS.md is a header `## §N` (dot optional)
                       or a numbered item `M.` inside that section
  4. skill index       every skill named in the §13 table has skills/<name>/SKILL.md
  5. descriptions      every skill has a description <= 400 chars
  6. duplicates        exact sentences >= 120 chars repeated across files (WARN only)

Exit codes: 0 clean (warnings allowed) · 1 findings · 2 cannot measure.

Usage
  python scripts/doctor.py --root .
  python scripts/doctor.py --selftest
"""
import argparse
import re
import sys
import tempfile
from pathlib import Path

CORE_LIMIT = 45_000
DESC_LIMIT = 400
DUP_MIN = 120

SKILL_REF = re.compile(r"skill\s+`([^`]+)`")
SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
SECTION_REF = re.compile(r"§(\d+(?:\.\d+)?)")
SECTION_HEADER = re.compile(r"^##\s+§(\d+(?:\.\d+)?)(?:\.|\s)", re.MULTILINE)
SENTENCE = re.compile(r"[.!?]+|\n+")


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


def section_bodies(text: str) -> dict:
    matches = list(SECTION_HEADER.finditer(text))
    bodies = {}
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        bodies[match.group(1)] = text[match.end():end]
    return bodies


def resolves_section(ref: str, bodies: dict) -> bool:
    if ref in bodies:
        return True
    if "." not in ref:
        return False
    parent, item = ref.split(".", 1)
    body = bodies.get(parent)
    if body is None:
        return False
    return re.search(rf"^\s*{re.escape(item)}\.\s", body, re.MULTILINE) is not None


def check_index(core: str, root: Path) -> list:
    body = section_bodies(core).get("13", "")
    fails = []
    for row in body.splitlines():
        row = row.strip()
        if not row.startswith("|") or "---" in row or "Skill" in row:
            continue
        cells = [c.strip() for c in row.strip("|").split("|")]
        last = cells[-1] if cells else ""
        match = re.search(r"`([^`]+)`", last)
        if not match:
            fails.append(f"§13 row without a skill name: {row[:70]}")
            continue
        name = match.group(1)
        if not SAFE_ID.fullmatch(name):
            fails.append(f"§13 skill '{name}' is not a safe id")
        elif not (root / "skills" / name / "SKILL.md").is_file():
            fails.append(f"§13 references missing skill '{name}'")
    return fails


def audit(root: Path) -> tuple[list, list, int]:
    core_path = root / "AGENTS.md"
    if not core_path.is_file():
        raise CannotMeasure(f"AGENTS.md not found under {root}")
    core = core_path.read_text(encoding="utf-8-sig")
    fails, warns, checks = [], [], 0

    checks += 1
    size = core_path.stat().st_size
    if size > CORE_LIMIT:
        fails.append(f"kernel is {size} bytes (> {CORE_LIMIT}); trim before adding rules")

    refs = sorted(set(SKILL_REF.findall(core)))
    for name in refs:
        checks += 1
        if not SAFE_ID.fullmatch(name):
            fails.append(f"skill ref '{name}' is not a safe id")
        elif not (root / "skills" / name / "SKILL.md").is_file():
            fails.append(f"skill ref '{name}' has no skills/<name>/SKILL.md")

    bodies = section_bodies(core)
    section_refs = sorted(set(SECTION_REF.findall(core)))
    missing = [r for r in section_refs if not resolves_section(r, bodies)]
    checks += 1
    if missing:
        fails.append("section refs point nowhere: " + ", ".join("§" + r for r in missing))

    index_fails = check_index(core, root)
    checks += 1
    if index_fails:
        fails.extend(index_fails)

    for skill_md in sorted(root.glob("skills/*/SKILL.md")):
        checks += 1
        desc = read_front_matter(skill_md.read_text(encoding="utf-8-sig")).get("description", "")
        if not desc:
            fails.append(f"{skill_md.parent.name}: no description")
        elif len(desc) > DESC_LIMIT:
            warns.append(f"{skill_md.parent.name}: description {len(desc)} chars (> {DESC_LIMIT})")

    corpus = [core_path] + sorted(root.glob("docs/*.md")) + sorted(root.glob("skills/*/SKILL.md"))
    seen: dict[str, set] = {}
    for path in corpus:
        for sentence in SENTENCE.split(path.read_text(encoding="utf-8-sig")):
            sentence = " ".join(sentence.split())
            if len(sentence) >= DUP_MIN:
                seen.setdefault(sentence, set()).add(path.relative_to(root).as_posix())
    groups = {s: files for s, files in seen.items() if len(files) > 1}
    checks += 1
    if groups:
        sample = "; ".join(sorted({p for files in groups.values() for p in files})[:4])
        warns.append(f"{len(groups)} duplicate sentence(s) across: {sample}")

    return fails, warns, checks


def selftest() -> int:
    controls = {}

    def check(name, cond):
        controls[name] = bool(cond)
        print(f"{'PASS' if cond else 'FAIL'}  {name}")

    check("plain §1 resolves", resolves_section("1", {"1": "\n1. a\n2. b\n"}))
    check("§1.2 resolves to item 2", resolves_section("1.2", {"1": "\n1. a\n2. b\n"}))
    check("§1.3 fails (no item 3)", not resolves_section("1.3", {"1": "\n1. a\n2. b\n"}))
    check("§14 fails (no section)", not resolves_section("14", {"1": ""}))

    clean_agents = (
        "# K\n## §1 Level\nskill `good` see §1.1\n1. item\n"
        "## §13 Skills\n| Trigger | Skill |\n|---|---|\n| x | `good` |\n"
    )
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "skills" / "good").mkdir(parents=True)
        (root / "AGENTS.md").write_text(clean_agents, encoding="utf-8")
        (root / "skills" / "good" / "SKILL.md").write_text(
            "---\nname: good\ndescription: short\n---\nbody\n", encoding="utf-8")
        fails, warns, _ = audit(root)
        check("clean tree passes", not fails)

        bad_agents = (
            "# K\n## §1 Level\nsee §9.9\nskill `missing2`\n"
            "## §13 Skills\n| Trigger | Skill |\n|---|---|\n| x | `missing` |\n"
        )
        (root / "AGENTS.md").write_text(bad_agents, encoding="utf-8")
        (root / "skills" / "long-desc").mkdir()
        (root / "skills" / "long-desc" / "SKILL.md").write_text(
            "---\nname: long-desc\ndescription: " + "x" * (DESC_LIMIT + 1) + "\n---\n", encoding="utf-8")
        fails, warns, _ = audit(root)
        check("missing skill ref fails", any("missing2" in f for f in fails))
        check("missing index skill fails", any("missing" in f and "§13" in f for f in fails))
        check("bad section ref fails", any("§9.9" in f for f in fails))
        check("long description warns", any("long-desc" in w for w in warns))

    ok = all(controls.values())
    print(f"RESULT: {'PASS' if ok else 'FAIL'} ({sum(controls.values())}/{len(controls)} controls)")
    return 0 if ok else 1


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="PDD protocol doctor (read-only).")
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
