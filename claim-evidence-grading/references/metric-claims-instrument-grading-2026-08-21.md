# Metric-claim grading additions — 2026-08-21 (physiomorphic I(S) audit)

Three new verification operations for this skill, proven in the pass-2 registry
audit. PENDING SKILL.md INTEGRATION: the background-curator read-before-write
gate refused the SKILL.md patch (view tool dedupes already-loaded skills, so
the same-turn load requirement was unsatisfiable). Fold these three into the
"Verification operations" numbered list (as items 8-10) on next SKILL.md edit.

## 8. Derived counts must be re-derived after the action settles
Any count you report (edges updated, files changed, refs fixed) is a CLAIM.
Re-derive it mechanically from the artifacts (diff backup vs live, count) after
the action completes. Case: pass-1 reported "141 dependency edges updated";
post-hoc AST/module diff showed 53 engines' dep-sets changed and <=131 edge
lines touched. Counts computed mid-action drift upward because repeated
tool-log lines get mentally summed as separate edits.

## 9. Metric claims = instrument claims
A claim resting on a computed score inherits the score's IMPLEMENTED
operations, never its docstring labels. Read the scorer's source before
publishing any number. Case (Bridgman seat, 2026-08-21): isomorphism C_r's
docstring promised 3 checks (resolution + same-system + cross-system
biological plausibility) but the code implemented string-resolution ONLY, and
scored zero-dependency engines 1.0 by fiat. "C_r=1.000 means wiring is
biologically plausible" was FALSE as worded; true only as "dependency
resolution rate 100%". Grade each metric axis REAL / THEORETICAL / DECORATIVE
by its code; publish under the operational name it actually measures (e.g.
"Registry Integrity Index"), never the aspirational construct name. Companion
statistical rule (Fisher seat): the same-instrument pre->post delta is the
legitimate headline; cross-cohort comparisons with different n and composition
(68 vs 98) are noise, not evidence of improvement.

## 10. Key-name vacuity
When verifying a dict-key-based claim, confirm the key you read is the key the
CONSUMER reads. Case: a dead-edge verification script read `depends_on` while
the registry and the scorer both use `dependencies` — the check returned "0
defects" against a registry actually holding 61 dead edges. A verification
against the wrong key is a verification against nothing, and it is WORSE than
no verification because it launders the claim as checked.
