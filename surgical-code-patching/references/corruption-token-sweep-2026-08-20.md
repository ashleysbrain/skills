# Corruption-token sweep (2026-08-20, 6 tokens in one session)

Session: Writing Studio B2BU auth frontend. Long context tail. The known
glm-5.3/llm-vendor long-context failure mode surfaced IN patch payloads.

## Tokens seen (all caught post-apply)
- 'the principal Headers' (mangled identifier, valid string)
- display = 'restore' / display = '-none' (invalid CSS values, valid syntax)
- ═-signed (glued suffix)
- ca.innerHTML = keep-ca-placeholder; (placeholder fragment)
- document.setItem ? null : null; (no-op ternary)

## Why dangerous
1. Syntactically valid — node --check / ast.parse PASS.
2. Fuzzy matcher absorbs strays into context matches — reports success.
3. One instance: a purge patch itself contained a NEW token (fuzzy match
   silently consumed it; fix = grep + verify actual file bytes).

## Sweep protocol (after EVERY patch batch)
1. Read the returned diff hunk-by-hunk. Never skim.
2. Grep patched file for intended identifiers + garbage patterns:
   grep -n "? null : null\|'-none'\|= 'restore'\|-signed═\|placeholder" <file>
3. node --check / ast.parse for syntax.
4. Found token -> purge patch -> re-sweep.

Cost: ~2s. Shipping one: guardian restore.

## Meta-rule (from memory: strike + retrace)
When corruption tokens appear in payloads, STOP writing long prose
patches. Short fragments + grep sweeps + read-back verification. The
corruption mode targets long generated text.
