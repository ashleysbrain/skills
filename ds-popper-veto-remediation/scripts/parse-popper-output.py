#!/usr/bin/env python3
"""
Parse the specialist engine cron output to extract VETO items and remediation requirements.

Usage:
    python3 scripts/parse-popper-output.py [--latest] [--output-json]

Outputs structured JSON of VETO findings for the specialist engine remediation workflow.
"""

import json
import re
import sys
import glob
from pathlib import Path
from datetime import datetime

CRON_OUTPUT_DIR = Path.home() / ".hermes" / "cron" / "output" / "bb2fc380f91d"

def find_latest_popper_output():
    """Find the most recent the specialist engine cron output file."""
    md_files = sorted(CRON_OUTPUT_DIR.glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True)
    return md_files[0] if md_files else None

def parse_veto_report(filepath: Path) -> dict:
    """Parse a the specialist engine VETO report and extract structured findings."""
    content = filepath.read_text()
    
    result = {
        "file": filepath.name,
        "timestamp": datetime.fromtimestamp(filepath.stat().st_mtime).isoformat(),
        "document_path": None,
        "review_date": None,
        "veto_applied": False,
        "fatal_flaws": [],
        "remediation_requirements": [],
        "notes_for_oppenheimer": None,
        "action_required": [],
    }
    
    # Extract document path
    doc_match = re.search(r'Document Reviewed`:\s*(.+)', content)
    if doc_match:
        result["document_path"] = doc_match.group(1).strip()
    
    # Extract review date
    date_match = re.search(r'Review Date`:\s*(.+)', content)
    if date_match:
        result["review_date"] = date_match.group(1).strip()
    
    # Check for VETO
    if "**APPLY VETO**" in content or "**VETO APPLIED**" in content:
        result["veto_applied"] = True
    
    # Extract fatal flaws (numbered list after "FATAL METHODOLOGICAL FLAWS IDENTIFIED")
    fatal_section = re.search(r'FATAL METHODOLOGICAL FLAWS IDENTIFIED`:(.+?)(?=\n\n|\n##|\n\*\*NOTES|\n\*\*ACTION)', content, re.DOTALL)
    if fatal_section:
        flaw_text = fatal_section.group(1)
        # Find numbered items
        flaws = re.findall(r'\d+\.\s+\*\*(.+?)\*\*\s*→\s*(.+?)(?=\n\d+\.|\n\n|$)', flaw_text, re.DOTALL)
        for title, desc in flaws:
            result["fatal_flaws"].append({
                "category": title.strip(),
                "description": desc.strip()
            })
    
    # Extract action required items
    action_section = re.search(r'ACTION REQUIRED`:(.+?)(?=\n\n|\n##|\n\*\*)', content, re.DOTALL)
    if action_section:
        actions = re.findall(r'\d+\.\s+(.+?)(?=\n\d+\.|\n\n|$)', action_section.group(1), re.DOTALL)
        result["action_required"] = [a.strip() for a in actions]
    
    # Extract notes for Oppenheimer
    notes_section = re.search(r'NOTES FOR DS OPPENHEIMER`:(.+?)(?=\n\n|\n##|\n\*\*)', content, re.DOTALL)
    if notes_section:
        result["notes_for_oppenheimer"] = notes_section.group(1).strip()
    
    # Map fatal flaws to standard remediation categories
    flaw_to_category = {
        "zero empirical evidence": "zero_empirical_evidence",
        "undisclosed conflict of interest": "undisclosed_coi",
        "insufficient ethical safeguards": "insufficient_ethics",
        "insufficient ethical": "insufficient_ethics",
        "undefined operational definitions": "undefined_definitions",
        "reproducibility": "reproducibility_gaps",
    }
    
    for flaw in result["fatal_flaws"]:
        cat = flaw["category"].lower()
        matched = None
        for key, val in flaw_to_category.items():
            if key in cat:
                matched = val
                break
        if matched:
            result["remediation_requirements"].append(matched)
    
    return result

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Parse the specialist engine VETO output")
    parser.add_argument("--latest", action="store_true", help="Parse only the latest output")
    parser.add_argument("--output-json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    
    if args.latest:
        filepath = find_latest_popper_output()
        if not filepath:
            print(json.dumps({"error": "No the specialist engine output files found"}))
            sys.exit(1)
        result = parse_veto_report(filepath)
    else:
        # Parse all outputs
        md_files = sorted(CRON_OUTPUT_DIR.glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True)
        result = [parse_veto_report(f) for f in md_files]
    
    if args.output_json:
        print(json.dumps(result, indent=2))
    else:
        # Human-readable summary
        if isinstance(result, list):
            for r in result:
                print(f"\n=== {r['file']} ===")
                print(f"Document: {r['document_path']}")
                print(f"VETO: {'YES' if r['veto_applied'] else 'NO'}")
                print(f"Fatal flaws: {len(r['fatal_flaws'])}")
                for f in r['fatal_flaws']:
                    print(f"  - {f['category']}: {f['description'][:80]}...")
                print(f"Remediation needed: {', '.join(r['remediation_requirements'])}")
        else:
            r = result
            print(f"Document: {r['document_path']}")
            print(f"VETO Applied: {r['veto_applied']}")
            print(f"Fatal Flaws ({len(r['fatal_flaws'])}):")
            for f in r['fatal_flaws']:
                print(f"  - {f['category']}")
            print(f"Remediation Categories: {', '.join(r['remediation_requirements'])}")
            print(f"Actions Required: {len(r['action_required'])}")

if __name__ == "__main__":
    main()