#!/usr/bin/env python3
"""
VERITAS Stage 4: Regulatory Language Compliance Scanner

Scans academic papers, abstracts, and external-facing documents for FDA SaMD
triggering language. Flags prohibited terms with context and suggests replacements.

Usage:
    python3 regulatory_language_scan.py <file_path>
    python3 regulatory_language_scan.py abstract.md
    python3 regulatory_language_scan.py paper.tex
    cat abstract.md | python3 regulatory_language_scan.py -

Exit codes:
    0 = PASS (no flags)
    1 = FLAGS FOUND (review output)
    2 = ERROR (file not found, etc.)
"""

import sys
import re

# Terms that trigger FDA SaMD classification concerns.
# Maps term -> suggested replacement.
PROHIBITED = {
    "detect": "identify",
    "diagnose": "characterize",
    "diagnosis": "assessment",
    "treat": "address",
    "treatment": "intervention",
    "medication": "supplement",
    "medication management": "supplement tracking",
    "clinical assessment": "structured evaluation",
    "clinical monitoring": "structured observation",
    "episode detection": "pattern recognition",
    "predict episodes": "identify patterns",
    "replace clinical care": "complement professional guidance",
    "medical device": "wellness tool",
    "therapeutic": "supportive",
    "cure": "support",
    "patient": "user",
    "prescribe": "recommend",
}

# Terms that are caution-level (review context before deciding)
CAUTION = {
    "predict": "identify patterns (if medical context)",
    "clinical": "wellness (if product feature context)",
    "monitor": "track (if medical context)",
    "assess": "evaluate (if medical context)",
}


def scan_text(text: str) -> list[dict]:
    """Scan text for prohibited and caution terms. Returns list of flags."""
    flags = []
    text_lower = text.lower()

    for term, replacement in PROHIBITED.items():
        pattern = r"\b" + re.escape(term) + r"\b"
        for match in re.finditer(pattern, text_lower):
            idx = match.start()
            start = max(0, idx - 40)
            end = min(len(text), idx + len(term) + 40)
            context = text[start:end].replace("\n", " ").strip()
            flags.append({
                "level": "PROHIBITED",
                "term": term,
                "replacement": replacement,
                "context": f"...{context}...",
            })

    for term, note in CAUTION.items():
        pattern = r"\b" + re.escape(term) + r"\b"
        for match in re.finditer(pattern, text_lower):
            idx = match.start()
            start = max(0, idx - 40)
            end = min(len(text), idx + len(term) + 40)
            context = text[start:end].replace("\n", " ").strip()
            flags.append({
                "level": "CAUTION",
                "term": term,
                "replacement": note,
                "context": f"...{context}...",
            })

    return flags


def main():
    if len(sys.argv) < 2:
        print("Usage: regulatory_language_scan.py <file_path>")
        print("       regulatory_language_scan.py -  (read from stdin)")
        sys.exit(2)

    path = sys.argv[1]

    if path == "-":
        text = sys.stdin.read()
    else:
        try:
            with open(path, "r") as f:
                text = f.read()
        except FileNotFoundError:
            print(f"ERROR: File not found: {path}")
            sys.exit(2)

    # Strip LaTeX commands for more accurate scanning
    clean_text = re.sub(r"\\[a-zA-Z]+(\{[^}]*\})*", " ", text)

    flags = scan_text(clean_text)

    if not flags:
        print("VERITAS STAGE 4: REGULATORY SCAN")
        print("Result: PASS - No prohibited or caution terms found")
        sys.exit(0)

    prohibited = [f for f in flags if f["level"] == "PROHIBITED"]
    caution = [f for f in flags if f["level"] == "CAUTION"]

    print("VERITAS STAGE 4: REGULATORY SCAN")
    print(f"Result: FLAGS FOUND ({len(prohibited)} prohibited, {len(caution)} caution)")
    print()

    if prohibited:
        print("=== PROHIBITED TERMS (must fix) ===")
        for f in prohibited:
            print(f'  TERM: "{f["term"]}" -> REPLACE WITH: "{f["replacement"]}"')
            print(f'  CONTEXT: {f["context"]}')
            print()

    if caution:
        print("=== CAUTION TERMS (review context) ===")
        for f in caution:
            print(f'  TERM: "{f["term"]}" -> NOTE: {f["replacement"]}')
            print(f'  CONTEXT: {f["context"]}')
            print()

    sys.exit(1)


if __name__ == "__main__":
    main()
