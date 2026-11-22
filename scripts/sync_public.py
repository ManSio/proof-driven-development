#!/usr/bin/env python3
"""Publish gate for the public PDD repo. Read-only by default.

Checks
  1. whitelist  every changed/untracked path is a known public path
  2. scrub      no private paths or secrets in text files
  3. gates      doctor.py and skill_inventory.py both exit 0

Usage
  python scripts/sync_public.py --check
  python scripts/sync_public.py --commit -m "docs: ..."

It never pushes. Push only on an explicit owner command.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

ALLOW = re.compile(
    r"^("
    r"AGENTS\.md|README\.md|CHANGELOG\.md|CONTRIBUTING\.md|SECURITY\.md|SYNC\.md|"
    r"LICENSE|\.gitattributes|\.gitignore|"
    r"docs/[^/]+\.md|"
    r"skills/[a-z0-9-]+/SKILL\.md|"
    r"scripts/[a-z_]+\.py|"
    r"knowledge/[A-Z]+\.md|"
    r"examples/[^/]+/[^/]+\.md|"
    r"\.github/workflows/[^/]+\.ya?ml"
    r")$"
)
SCRUB = [
    r"C:\\Users",
    r"D:\\Project",
    r"192\.168\.",
    r"workers\.dev",
    r"sk-[A-Za-z0-9]{10,}",
    r"ghp_[A-Za-z0-9]{20,}",
    r"AKIA[0-9A-Z]{16}",
    "-----" + "BEGIN",
]
BINARY = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf"}


def run(args: list, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


def changed(root: Path) -> list:
    out = run(["git", "status", "--porcelain", "-uall"], root).stdout
    paths = []
    for line in out.splitlines():
        if not line.strip():
            continue
        path = line[3:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        paths.append(path)
    return paths


def scan(root: Path) -> list:
    hits = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if rel.startswith(".git/") or path.suffix.lower() in BINARY:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for pattern in SCRUB:
            if re.search(pattern, text):
                hits.append(f"{rel}: {pattern}")
    return hits


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="PDD publish gate (read-only by default).")
    parser.add_argument("--repo", default=".", help="public repo root (default: .)")
    parser.add_argument("--check", action="store_true", help="explicit no-op; check is the default")
    parser.add_argument("--commit", action="store_true", help="commit whitelisted changes")
    parser.add_argument("-m", "--message", default="chore: sync public", help="commit message")
    args = parser.parse_args(argv)

    root = Path(args.repo).resolve()
    ok = True

    paths = changed(root)
    bad = [p for p in paths if not ALLOW.match(p)]
    if bad:
        ok = False
        print("OFF-WHITELIST:")
        for p in bad:
            print(f"  {p}")

    hits = scan(root)
    if hits:
        ok = False
        print("SCRUB HITS:")
        for h in hits[:20]:
            print(f"  {h}")

    for script in ("scripts/doctor.py", "scripts/skill_inventory.py"):
        result = run([sys.executable, script, "--root", "."], root)
        print(f"[{script}] rc={result.returncode}")
        if result.returncode != 0:
            ok = False
            print(result.stdout[-1000:] or result.stderr[-1000:])

    if args.commit and ok:
        if not paths:
            print("nothing to commit")
            return 0
        run(["git", "add", *paths], root)
        result = run(["git", "commit", "-m", args.message], root)
        print(result.stdout.strip() or result.stderr.strip())
        return 0 if result.returncode == 0 else 1

    print("CHECK:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
