#!/usr/bin/env python3
"""sanitize_skills.py — build a public (sanitized) edition of a private skill corpus.

Laws enforced (generalized from the Divinity Science stack for public release):
  1. NO personal names — they become role nouns.
  2. NO internal paths/ports/org-terms — they become generic placeholders.
  3. NO secrets/tokens — hard abort (exit 1) if any secret pattern survives.
Everything else is untouched, byte-for-byte.
"""
import re
import sys
import argparse
from pathlib import Path

# law 1: personal names -> role nouns (de-personalize, never delete the rule)
NAME_MAP = [
    (r'\bCEO\b', 'principal'),
    (r'\bAshley\b', 'the principal'),
    (r'\bBrandon\b', 'the principal'),
    (r'\bGG\b', 'the operator agent'),
    (r'\bMosaic OS\b', 'the OS'),
    (r'\bMOSAIC\b', 'the OS'),
    (r'\bGLM\b', 'LLM'),
    (r'\bzai\b', 'llm-vendor'),
    (r'\bopenclaw\b', 'sibling-agent'),
    (r'\bopencode\b', 'sibling-agent'),
    (r'\bHermes\b', 'the operator agent'),
]

# law 2: internal paths/ports/org-terms -> generic placeholders
PATH_MAP = [
    (r'Users/aw/[a-zA-Z0-9._/-]+', '<workspace>'),
    (r'~/.hermes/skills', 'skills-library'),
    (r'~/.hermes', '<agent-home>'),
    (r'operator-bus\.db', 'message-bus.db'),
    (r'\boperator-bus\b', 'message-bus'),
    (r'\bmosaic-method\b', 'your-stack'),
    (r'\bdivinity-science\b', 'your-org'),
    (r'\baisha-workspace\b', 'your-workspace'),
    (r'\bgg-organism\b', 'agent-organism'),
    (r'\bDS [A-Z][a-z]+(?: [A-Z][a-z]+)?\b', 'the specialist engine'),
    (r':8\d{3}\b', ':port'),
    (r'5702987845', '<chat-id>'),
]

# law 3: secrets must NEVER appear; any survivor aborts the build
SECRET_PATTERNS = [
    (r'sk-[A-Za-z0-9]{20,}', 'OpenAI-style API key'),
    (r'ghp_[A-Za-z0-9]{30,}', 'GitHub PAT'),
    (r'gho_[A-Za-z0-9]{30,}', 'GitHub OAuth token'),
    (r'github_pat_[A-Za-z0-9_]{30,}', 'GitHub fine-grained PAT'),
    (r'xoxb-[A-Za-z0-9-]{20,}', 'Slack token'),
    (r'AIza[A-Za-z0-9_-]{30,}', 'Google API key'),
    (r'Bearer\s+[A-Za-z0-9._-]{20,}', 'Bearer token'),
]


def sanitize_text(text: str):
    for pat, rep in NAME_MAP + PATH_MAP:
        text = re.sub(pat, rep, text)
    return text


def find_secrets(text: str):
    hits = []
    for pat, label in SECRET_PATTERNS:
        for m in re.finditer(pat, text):
            hits.append(f"{label}: {m.group(0)[:10]}...")
    return hits


def load_curated(path: Path):
    return [ln.strip() for ln in path.read_text().splitlines()
            if ln.strip() and not ln.startswith('#')]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--curated', required=True, help='list of skill dirs, one per line')
    ap.add_argument('--source', default=str(Path.home() / '.hermes' / 'skills'))
    ap.add_argument('--out', required=True)
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    src_root = Path(args.source)
    curated = load_curated(Path(args.curated))
    outdir = Path(args.out)
    print(f"curated: {len(curated)} skills from {src_root}")

    ok, leaks, copied = 0, 0, []
    for rel in curated:
        src = src_root / rel / 'SKILL.md'
        if not src.exists():
            print(f"  SKIP missing: {rel}")
            continue
        raw = src.read_text()
        clean = sanitize_text(raw)
        # second pass: nested terms created by pass 1 (e.g. renamed bus path)
        clean = sanitize_text(clean)
        hits = find_secrets(clean)
        if hits:
            leaks += len(hits)
            print(f"  LEAK in {rel}:")
            for h in hits:
                print(f"    {h}")
            continue
        # also scan supporting files if the skill has references/scripts
        for extra in (src.parent / 'references').glob('*.md') if (src.parent / 'references').is_dir() else []:
            pass  # references handled below in copy step
        if args.dry_run:
            print(f"  would write {outdir / rel.split('/')[-1] / 'SKILL.md'} ({len(clean)}b)")
        else:
            dst = outdir / rel.split('/')[-1]
            dst.mkdir(parents=True, exist_ok=True)
            (dst / 'SKILL.md').write_text(clean)
            # copy reference/scripts dirs with sanitization
            for sub in ('references', 'scripts'):
                sdir = src.parent / sub
                if sdir.is_dir():
                    (dst / sub).mkdir(exist_ok=True)
                    for f in sdir.rglob('*'):
                        if f.is_file():
                            relf = f.relative_to(sdir)
                            tgt = dst / sub / relf
                            tgt.parent.mkdir(parents=True, exist_ok=True)
                            try:
                                body = sanitize_text(f.read_text())
                                if find_secrets(body):
                                    leaks += 1
                                    print(f"  LEAK in {rel}/{sub}/{relf}")
                                    continue
                                tgt.write_text(body)
                            except UnicodeDecodeError:
                                shutil.copy2(f, tgt)
        ok += 1
        copied.append(rel)

    print(f"\nsanitized={ok} leaks={leaks} dry_run={args.dry_run}")
    if leaks:
        sys.exit(1)


if __name__ == '__main__':
    import shutil  # noqa: E402  (used for binary fallback copy)
    main()
