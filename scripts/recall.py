#!/usr/bin/env python3
"""Search the knowledge registries for a symptom. Read-only.

Exit codes: 0 matches found · 2 cannot measure or no matches.
"No matches" is a fact to report, never silently "clean".

Usage
  python scripts/recall.py "windows encoding"
  python scripts/recall.py "mutation" --root .
"""
import argparse
import sys
from pathlib import Path

REGISTRIES = ("PATTERNS.md", "THREADS.md", "NEGATIVE.md")


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Search knowledge registries (read-only).")
    parser.add_argument("query")
    parser.add_argument("--root", default=".", help="protocol root (default: .)")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    knowledge = root / "knowledge"
    if not knowledge.is_dir():
        print(f"CANNOT MEASURE: knowledge/ not found under {root}", file=sys.stderr)
        return 2

    terms = [t.lower() for t in args.query.split() if len(t) > 2]
    if not terms:
        print("CANNOT MEASURE: query has no meaningful terms", file=sys.stderr)
        return 2

    hits = 0
    for name in REGISTRIES:
        path = knowledge / name
        if not path.is_file():
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
            low = line.lower()
            if any(term in low for term in terms):
                hits += 1
                print(f"{name}:{number}: {line.strip()[:160]}")

    if not hits:
        print("no matches in knowledge/ - this is a fact, not 'clean'", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
