# Case Study: Sherman 3D Vector Spec — 3rd Adversarial Review

**Date:** 2026-08-10
**Spec:** SHERMAN-3D-VECTOR-SPEC.md (456 lines, revised 3x)
**Prior reviews:** R1 (bus 1656) found 2 critical bugs + 8 concerns; R2 (bus 1711) found 3 production risks
**This review:** 10 NEW findings (5 CRITICAL, 4 HIGH, 1 MEDIUM)

## The Technique That Found What Others Missed

R1 and R2 reviewed the spec in isolation — checking internal consistency,
math correctness, and performance. Both missed systemic interaction defects
because they never opened the actual implementation code or the binding
ontology.

R3 loaded three sources in parallel:
1. **The spec** (SHERMAN-3D-VECTOR-SPEC.md)
2. **The binding invariants** (ONTOLOGY.md I1-I11 + CONNECTION-LIFECYCLE.md A-H)
3. **The actual implementation** (sherman_router.py 1212 lines, talent_gate.py 126 lines)

Findings lived exclusively in the gaps BETWEEN these three sources.

## Cross-Cutting Root Cause: The Propagation Gap

5 of 10 findings (F1, F3, F4, F5, F7) shared one root cause: **the lens tag
is classified inside Sherman but never propagated to downstream consumers.**

The spec assumed the lens tag would be read by:
- The tissue layer (for lens injection) → F1: it's not, and putting it in
  Sherman violates I6 (orchestrator directs but does not execute)
- The VERITAS gate (for science-lens output validation) → F3: VERITAS only
  fires pre-route on the routing decision, never post-output
- The talent gate (for lens-conditioned co-signer sets) → F4: talent_gate.py
  parses `Engine:` via regex but never reads a lens field
- Skill modules (opendesign, openresearch) → F5: they may bypass Sherman
  entirely and never classify a lens
- Chain step N+1 (for inter-step quality gating) → F7: no gate exists between
  chain steps, garbage flows through

**The fix for all 5:** make the lens tag a first-class mandatory field in
every routing result, and require every consumer in the routing circuit to
read it.

## Findings Summary Table

| # | Sev | Vector | Root pattern |
|---|-----|--------|-------------|
| F1 | CRITICAL | Ontology I6 | Orchestrator executes (shapes output), violating "directs but does not execute" |
| F2 | HIGH | Physics gate | Gate params lens-blind; fixed surprise=0.3 over-gates art, under-gates math |
| F3 | CRITICAL | VERITAS gate | Science-lens claims NOT post-output validated; VERITAS fires pre-route only |
| F4 | HIGH | Talent gate | Lens tag never reaches talent_gate.py; co-signers domain-only |
| F5 | MEDIUM | Skill modules | opendesign/openresearch may bypass Sherman; lens never classified |
| F6 | CRITICAL | Operator bias | EWMA global; the operator agent (art-dominant) contaminates sibling-agent/sibling-agent vectors |
| F7 | CRITICAL | Chain atomicity | No inter-step quality gate; garbage math flows into art step |
| F8 | HIGH | Model versioning | No HF revision pin; silent weight updates invalidate all vectors |
| F9 | HIGH | Keyword governance | LENS_KEYWORDS no owner, no collision check, no regression suite |
| F10 | CRITICAL | User override | No manual override; if added naively EWMA learns from interventions |

## Key Detection Technique: Field Consumer Tracing

For each field the spec's system produces, search the codebase:

```python
# The spec produces a lens tag. Who reads it?
# search_files pattern='lens' in sherman_router.py, talent_gate.py, etc.
# Result: lens appears in spec sections but talent_gate.py only reads "Engine:"
# → propagation gap confirmed
```

This technique generalizes: for ANY spec that introduces a new field/tag/flag,
trace it through the actual code. If zero consumers exist, the field is
classified-but-not-consumed.
