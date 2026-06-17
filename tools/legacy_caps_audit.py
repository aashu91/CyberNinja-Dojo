#!/usr/bin/env python3
"""Audit script to verify LEGACY comment compliance.

This script checks that every file containing 'legacy' (case-insensitive)
also contains 'LEGACY' in all caps somewhere in a comment, as per the
project's legacy code documentation requirements.

Usage:
    python3 tools/legacy_caps_audit.py
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple

# Directories to skip during audit
SKIP_DIRS = {
    '.git', 'node_modules', 'target', 'build', 'dist', '__pycache__',
    '.venv', 'venv', 'diagnostic', '.github'
}

# File extensions to check
CHECK_EXTENSIONS = {
    '.py', '.rs', '.ts', '.tsx', '.js', '.jsx', '.go', '.c', '.cpp', '.h',
    '.hpp', '.java', '.rb', '.lua', '.hs', '.md', '.txt', '.yaml', '.yml',
    '.json', '.toml', '.sh', '.bash'
}

# Pattern to detect 'legacy' (case-insensitive)
LEGACY_PATTERN = re.compile(r'legacy', re.IGNORECASE)

# Pattern to detect 'LEGACY' in all caps
LEGACY_CAPS_PATTERN = re.compile(r'LEGACY')


def should_skip(path: Path) -> bool:
    """Check if path should be skipped."""
    for part in path.parts:
        if part in SKIP_DIRS:
            return True
    return False


def check_file(filepath: Path) -> Tuple[bool, bool, bool]:
    """
    Check a file for legacy compliance.

    Returns:
        (has_legacy, has_legacy_caps, is_violation)
    """
    try:
        content = filepath.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return False, False, False

    has_legacy = bool(LEGACY_PATTERN.search(content))
    has_legacy_caps = bool(LEGACY_CAPS_PATTERN.search(content))

    # Violation: has 'legacy' but not 'LEGACY'
    is_violation = has_legacy and not has_legacy_caps

    return has_legacy, has_legacy_caps, is_violation


def find_files(root: Path) -> List[Path]:
    """Find all files to check in the repository."""
    files = []
    for path in root.rglob('*'):
        if path.is_file() and not should_skip(path):
            if path.suffix in CHECK_EXTENSIONS or path.name in {
                'Makefile', 'Dockerfile', 'LICENSE', 'README'
            }:
                files.append(path)
    return sorted(files)


def main() -> int:
    """Run the LEGACY caps audit."""
    repo_root = Path(__file__).parent.parent

    print("=" * 60)
    print("LEGACY Comment Compliance Audit")
    print("=" * 60)
    print()

    files = find_files(repo_root)
    print(f"Scanning {len(files)} files...")
    print()

    violations = []
    files_with_legacy = 0
    files_compliant = 0

    for filepath in files:
        has_legacy, has_legacy_caps, is_violation = check_file(filepath)

        if has_legacy:
            files_with_legacy += 1
            if is_violation:
                rel_path = filepath.relative_to(repo_root)
                violations.append(str(rel_path))
            else:
                files_compliant += 1

    # Report results
    print(f"Files containing 'legacy': {files_with_legacy}")
    print(f"Files compliant (have 'LEGACY'): {files_compliant}")
    print(f"Violations: {len(violations)}")
    print()

    if violations:
        print("VIOLATIONS - Files with 'legacy' but missing 'LEGACY':")
        print("-" * 60)
        for v in violations:
            print(f"  - {v}")
        print()
        print("To fix: Add a comment containing 'LEGACY' to each file above.")
        print()
        return 1
    else:
        print("All files are compliant!")
        return 0


if __name__ == '__main__':
    sys.exit(main())
