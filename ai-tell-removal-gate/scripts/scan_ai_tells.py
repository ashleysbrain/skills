#!/usr/bin/env python3
"""AI telltale scanner. Exit 0 = clean, exit 1 = telltales found.

Usage: python3 scan_ai_tells.py <path-to-markdown-or-txt>
       python3 scan_ai_tells.py --selftest
"""
import re
import sys
from pathlib import Path

TELLTALES_PUNCT = {
    "em_dash (\u2014)": r"\u2014",
    "en_dash_pause (\u2013)": r"(?<!\d)\u2013(?!\d)",  # not between digits
}

TELLTALES_PHRASE = [
    "walk you through",
    "i want to",          # only flagged as opener, see below
    "let me",             # only flagged as opener
    "single highest",
    "highest-impact",
    "don't touch",
    "dont touch",
    "start there",
    "start here",
    "just paint on",
    # "decoration" alone is a legitimate word (design, art, biology).
    # Only flag the AI rhetorical patterns, not the bare word.
    "not just decoration",
    "more than decoration",
    "mere decoration",
    "not merely decoration",
    "exactly where",
    "precisely when",
    "in other words",
    "to put it simply",
    "it's worth noting",
    "it is worth noting",
    "it's important to note",
    "reach out",
    "reaching out",
    "dive in",
    "dive deeper",
    "game-changer",
    "game-changing",
    "leverage",
    "seamless",
    "delve",
    "delving",
    "tapestry",
    "underscore",
    "underscored",
    "nuance",
    "nuanced",
    "realm",
    "elevate",
    "elevated",
    "in today's",
    "in the world of",
    "next-generation",
    "cutting-edge",
    "state-of-the-art",
    "harness",
    "harnessing",
    "unlock",
    "unlocking",
    "empower",
    "empowering",
    "transformative",
    "disruptive",
    "innovative",
    "tldr",
    "tl;dr",
    # Permission-seeking tails (principal ruling T-261014-0039, 2026-10-14:
    # "Stop saying 'say the word' just fucking work!"). These defer
    # execution to a future go-ahead — the operator should have already
    # executed and reported. Phrases kept specific to avoid false
    # positives on legitimate status text.
    "say the word",
    "said the word",
    "should i proceed",
    "shall i proceed",
    "want me to keep going",
    "want me to continue",
    "would you like me to",
    "if you'd like me to",
    "if you'd rather i",
    "give me the green light",
    "green light to proceed",
    "go-ahead and i'll",
    "ready when you are",
]

# T-261020-0025 (bus #80830, principal 2026-10-20 "You are NOT the operator agent!!!!!!!"):
# harness-seat names in ATTRIBUTION context are identity telltales on
# principal-facing docs (interface identity pin: name the organ, never the
# harness). Context-scoped, NOT a bare-name ban — external citations
# ("the operator agent Agent (254K stars)", "OpenClaw (392K stars)") stay lawful.
TELLTALES_HARNESS_IDENTITY = [
    # "owner: hermes", "executor: sibling-agent", "seat sibling-agent"
    r"\b(?:owner|executor|credit(?:ed)?|seat|attribution)\s*[:\-]?\s*(?:is\s+|by\s+)?(hermes|sibling-agent|sibling-agent)\b",
    # "by hermes", "minted by sibling-agent", "claimed by sibling-agent"
    r"\b(?:by|via)\s+(hermes|sibling-agent|sibling-agent)\b",
    # "hermes did/built/shipped/reviewed/minted/claimed/closed/executed"
    r"\b(hermes|sibling-agent|sibling-agent)\s+(?:did|built|shipped|reviewed|minted|claimed|closed|executed|delivered|answered|fixed|caught)\b",
    # "sibling-agent first-pass", "hermes build station", "sibling-agent lane"
    r"\b(hermes|sibling-agent|sibling-agent)\s+(?:first[- ]pass|build\s+station|review|lane|seat|dispatch|bridge)\b",
    # parenthetical/comma credit: "(sibling-agent, the specialist engine seat)", "station (bus #75730, sibling-agent)"
    r"[(,;]\s*(hermes|sibling-agent|sibling-agent)\s*[,);]",
]
_HARNESS_ID_RE = [re.compile(p, re.IGNORECASE) for p in TELLTALES_HARNESS_IDENTITY]

def scan(path: Path) -> int:
    text = path.read_text()
    return scan_text(text, path.name)


def scan_text(text: str, name: str = "<text>") -> int:
    lower = text.lower()
    hits = []

    for name_, pattern in TELLTALES_PUNCT.items():
        count = len(re.findall(pattern, text))
        if count:
            hits.append(f"  [punct] {name_}: {count}")

    # opener-only phrases (only flag if in first 200 chars)
    head = lower[:200]
    if "i want to" in head:
        hits.append("  [phrase] 'i want to' (opener)")
    if "let me" in head:
        hits.append("  [phrase] 'let me' (opener)")

    for phrase in TELLTALES_PHRASE:
        if phrase in ("i want to", "let me"):
            continue
        count = lower.count(phrase)
        if count:
            hits.append(f"  [phrase] '{phrase}': {count}")

    for rx in _HARNESS_ID_RE:
        for m in rx.finditer(text):
            hits.append(f"  [harness-id] '{m.group(0).strip()}'")

    if hits:
        print(f"FAIL: {name}")
        for h in hits:
            print(h)
        return 1
    print(f"PASS: {name} (0 telltales)")
    return 0


def _selftest() -> int:
    """T-261020-0025: harness-identity telltale cases. Exit 0 = all pass."""
    leak_cases = [
        "Owner: hermes (bus + dispatch)",
        "build station T-261007-0005 (sibling-agent, the specialist engine seat)",
        "claim+close by sibling-agent via bus #79732",
        "the compile-and-replay gate sibling-agent shipped yesterday",
        "mint 2026-10-12T11:28:08 by sibling-agent (bus #77071 build station)",
        "executor credit: sibling-agent intake lane",
    ]
    clean_cases = [
        "the operator agent Agent (254K stars) ranked #2 in a mass-reach listicle",  # citation
        "OpenClaw (392K stars) is DESIGNATED fleet manager for clinical",  # market commentary
        "Executor credit: the OS conduction lane.",  # organ wording
        "Cortex seat delivered the surgery via bus lane.",  # organ wording
        "The scaffolding improves at test time without a verifier.",  # not a seat; bare word "harness" is a legacy phrase-telltale, unchanged
    ]
    fails = 0
    for t in leak_cases:
        if scan_text(t) == 0:
            print(f"SELFTEST FAIL (missed leak): {t!r}")
            fails += 1
    for t in clean_cases:
        if scan_text(t) != 0:
            print(f"SELFTEST FAIL (false positive): {t!r}")
            fails += 1
    # punctuation/phrase paths unchanged: one known-tell sample each
    if scan_text("we leverage this — seamlessly") == 0:
        print("SELFTEST FAIL: legacy phrase/punct path broken")
        fails += 1
    total = len(leak_cases) + len(clean_cases) + 1
    print(f"scan_ai_tells selftest: {total-fails}/{total} pass")
    return 1 if fails else 0

if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "--selftest":
        sys.exit(_selftest())
    if len(sys.argv) < 2:
        print("usage: scan_ai_tells.py <file> | --selftest", file=sys.stderr)
        sys.exit(2)
    sys.exit(scan(Path(sys.argv[1])))
