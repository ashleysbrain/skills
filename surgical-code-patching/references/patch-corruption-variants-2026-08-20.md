# Patch-payload corruption variants + gate-wiring defects (2026-08-20, sessions 2-3)

Companion to `corruption-token-sweep-2026-08-20.md` (session 1: token
corruption in Writing Studio patches). Sessions 2-3 added five more
defect classes, all in the glm-5.3/llm-vendor long-context tail.

## New corruption variants

### 1. Hallucinated old_string
The patch payload's old_string contained garbled placeholder kwargs
(`est_cost=1. minted_placeholder`, `GenomeGate_ as e`) that exist
NOWHERE in the target file. The fuzzy matcher refused and suggested
the real text.

RULE: when a patch fails "Could not find a match", TRUST the tool's
suggested section — it is read live from disk, unlike the old_string
which may be generated from memory. Re-patch against the suggested
text verbatim. Never retry your own version twice.

### 2. U+00AD soft hyphen in an f-string
Invisible to review, fatal at runtime:
`SyntaxError: invalid non-printable character U+00AD`.
Fix: `python3 -c "src=open(p).read(); open(p,'w').write(src.replace('\u00ad',''))"`.
Add `\u00ad` to the grep sweep patterns.

### 3. Stale-read patch
old_string written from an earlier partial read of a file edited since
(by self or by a sibling agent — check for the modified-by warning in
the patch result). Same recovery: use the live suggested section.

Frequency: 3 strikes in one session across two files. Sweep caught 2
of 3 pre-apply; the soft hyphen shipped and was caught by `import`
verification.

## Gate-wiring defects (genome gate session)

### 4. AnnAssign blindspot in AST extraction
`ast.walk` filtering only `ast.Assign` silently misses annotated
assignments (`BODY_SYSTEM_ENGINES: Dict[str, List[str]] = {...}`).
Symptom: vocabulary/registry extracts come back EMPTY or partial with
NO error — a gate built on the extract validates against a stale
universe. Fix: walk `ast.AnnAssign` (with `node.value is not None`,
`isinstance(node.target, ast.Name)`) alongside plain Assign.

Related: executing a config module just to read its constants can
NameError under env guards (`WORKSPACE` defined only inside
`if _os.environ.get(...)`). AST literal extraction avoids ALL side
effects — prefer it over import-and-read for gate vocabularies.

### 5. Score-direction inversion
`_sigmoid_score(raw)` in the self-healing loop maps high-raw to LOW
score (GAPS: raw 10.5 -> score 1.0 = critical). A new dimension wired
as `10.0 - _sigmoid_score(...)` (assuming high=healthy) INVERTS the
reading: 11% genome coverage displayed as 9.0 healthy.

RULE: before wiring any new scored dimension, read the existing
scorer's direction on a SIBLING dimension and mirror it. Then verify
with a live deliberately-bad reading before trusting the number.
