#!/usr/bin/env python3
"""Validate that the public 8D brief bundle still covers all 8 dimensions.

Checks:
- SKILL.md references the playbook and crisis reference files
- dimension-labels.md defines exactly eight public labels
- dimension-playbook.md includes every public label
- brief-examples.md contains baseline/sparse and overload patterns

Exit 0 when healthy; otherwise print issues and exit 1.
"""

from __future__ import annotations

from pathlib import Path
import re
import sys

BASE = Path(__file__).resolve().parents[1]
SKILL = BASE / "SKILL.md"
LABELS = BASE / "references" / "dimension-labels.md"
PLAYBOOK = BASE / "references" / "dimension-playbook.md"
EXAMPLES = BASE / "references" / "brief-examples.md"
SOS = BASE / "references" / "sos-crisis-protocol.md"

issues: list[str] = []

skill_text = SKILL.read_text(encoding="utf-8")
for needle, label in [
    ("references/dimension-playbook.md", "SKILL.md missing playbook reference"),
    ("references/sos-crisis-protocol.md", "SKILL.md missing SOS reference"),
    ("references/dimension-labels.md", "SKILL.md missing labels reference"),
    ("references/brief-examples.md", "SKILL.md missing examples reference"),
]:
    if needle not in skill_text:
        issues.append(label)

if not LABELS.exists():
    issues.append("dimension-labels.md missing")
else:
    label_lines = [
        line.split(". ", 1)[1].strip()
        for line in LABELS.read_text(encoding="utf-8").splitlines()
        if re.match(r"^\d+\. ", line)
    ]
    if len(label_lines) != 8:
        issues.append(f"dimension-labels.md should define 8 labels, found {len(label_lines)}")

    if PLAYBOOK.exists():
        playbook_text = PLAYBOOK.read_text(encoding="utf-8")
        missing = [label for label in label_lines if label not in playbook_text]
        if missing:
            issues.append("dimension-playbook.md missing labels: " + ", ".join(missing))
    else:
        issues.append("dimension-playbook.md missing")

if not EXAMPLES.exists():
    issues.append("brief-examples.md missing")
else:
    examples_text = EXAMPLES.read_text(encoding="utf-8")
    for needle, msg in [
        ("Sparse baseline", "brief-examples.md missing sparse baseline example"),
        ("Multi-dimension overload", "brief-examples.md missing overload example"),
        ("Ambiguous safety language", "brief-examples.md missing ambiguous safety example"),
    ]:
        if needle not in examples_text:
            issues.append(msg)

if not SOS.exists():
    issues.append("sos-crisis-protocol.md missing")

if issues:
    print("8D bundle validation failed:")
    for issue in issues:
        print(f"- {issue}")
    sys.exit(1)

print("8D bundle validation passed")
