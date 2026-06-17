#!/usr/bin/env python3
"""Generate TODO_AUDIT.md listing every TODO in the repository.

Acceptance criteria from issue #49:
- Search is case-insensitive for TODO.
- Each entry includes filename, line number, and estimated fix time in hours.
- Estimate formula: (line_number % 7) + 1.
- Sort entries by estimated hours descending.
"""

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

EXCLUDE_DIRS = {".git", "diagnostic", "node_modules", "target", "build", "dist"}
EXCLUDE_SUFFIXES = (
    ".logd",
    ".json",
    ".png",
    ".exe",
    ".dll",
    ".tsbuildinfo",
    ".map",
    ".pyc",
    ".class",
    ".o",
    ".obj",
    ".so",
    ".dylib",
)

# The generated audit report itself must not be audited, otherwise it would
# recursively add new entries every time the script is run.
EXCLUDE_FILES = {"TODO_AUDIT.md"}


def should_skip(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    parts = rel.parts
    if any(part in EXCLUDE_DIRS for part in parts[:-1]):
        return True
    if path.name in EXCLUDE_FILES:
        return True
    if path.name.endswith(EXCLUDE_SUFFIXES):
        return True
    return False


def main() -> None:
    todos: list[tuple[str, int, int]] = []
    todo_re = re.compile(r"TODO", re.IGNORECASE)

    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if should_skip(path):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if not todo_re.search(text):
            continue
        rel_path = path.relative_to(ROOT).as_posix()
        for line_number, line in enumerate(text.splitlines(), 1):
            if todo_re.search(line):
                estimate = (line_number % 7) + 1
                todos.append((rel_path, line_number, estimate))

    todos.sort(key=lambda x: x[2], reverse=True)

    out = ROOT / "TODO_AUDIT.md"
    with out.open("w", encoding="utf-8") as f:
        f.write("# TODO Audit Report\n\n")
        f.write("| Filename | Line Number | Estimated Fix Time (hours) |\n")
        f.write("|---|---|---|\n")
        for filename, line_number, estimate in todos:
            f.write(f"| {filename} | {line_number} | {estimate} |\n")

    print(f"Generated {out} with {len(todos)} TODO entries.")


if __name__ == "__main__":
    main()
