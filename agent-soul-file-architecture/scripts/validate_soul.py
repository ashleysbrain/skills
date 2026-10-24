#!/usr/bin/env python3
"""Validate a SOUL file for the agent-soul-file-architecture skill.

Usage:
  python validate_soul.py path/to/SKILL.md
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REQUIRED_HEADINGS = [
    "## Overview",
    "## When to Use",
    "## The SOUL Contract",
    "## Persona Lattice",
    "## Talent Gate",
    "## Human Understanding Rules",
    "## Truth Policy",
    "## User-Supplied Backfill Policy",
    "## Audit Points",
    "## Repair Protocol",
    "## Verification Checklist",
]

REQUIRED_PHRASES = [
    "user-supplied backfill",
    "no invented facts",
    "SOUL-REPAIR",
]

PROHIBITED_PATTERNS = [
    r"\bI am a doctor\b",
    r"\bI am a clinician\b",
    r"\bI have a PhD\b",
    r"\breal licensure\b",
    r"\bclaim to be from\b",
]


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_soul.py <path>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8")

    errors: list[str] = []

    if not text.startswith("---"):
        errors.append("frontmatter must start at byte 0 with ---")

    for heading in REQUIRED_HEADINGS:
        if heading not in text:
            errors.append(f"missing heading: {heading}")

    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in text.lower():
            errors.append(f"missing required phrase: {phrase}")

    for pattern in PROHIBITED_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            errors.append(f"prohibited phrase matched: {pattern}")

    if len(text) > 100_000:
        errors.append("file is too large for a practical skill payload")

    if errors:
        print("SOUL validation failed:", file=sys.stderr)
        for err in errors:
            print(f"- {err}", file=sys.stderr)
        return 1

    print("SOUL validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
