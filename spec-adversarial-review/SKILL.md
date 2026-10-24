---
name: spec-adversarial-review
description: Use when reviewing specs adversarially pre-implementation.
version: 1.0.0
metadata:
  hermes.tags: [spec, review, adversarial, ontology, architecture, propagation-gap]
  hermes.category: software-development
---

# Spec Adversarial Review

## When This Skill MUST Load

Load this skill when:
- User asks for an adversarial review, final review, or "another pass" on a spec/design document
- User says "find what nobody has found yet" or "what did previous reviews miss"
- A spec has survived N review rounds and needs fresh attack vectors
- User wants to verify spec compliance with ONTOLOGY.md or other binding invariants
- Pre-implementation gate: "this is the final review before we build"

## What This Is (and Is NOT)

**IS:** Pre-implementation design review. The spec is a document (markdown). The
question is: will this design work when it meets the actual codebase and binding
architectural constraints?

**IS NOT:**
- Code review (use `code-review` skill — that's PR-level: SQL injection, DRY, security)
- Deployment readiness (use `adversarial-elite-panel-review` — that's git remotes, CSS, fresh clone)
- Research integrity audit (use `ds-popper-audit` — that's citations, tier thresholds, FDA language)
- Biological naming verification (use `organism-biological-isomorphism-verification`)

## The Method: Four-Source Cross-Reference

The core technique that finds what single-source reviews miss: **read the spec,
the binding invariants, the actual implementation code, AND (when relevant) probe
the live external system simultaneously.** Each source reveals what the others
conceal.

### Step 1 — Load All Three Sources in Parallel (plus the live external system)

```
read_file(spec)           # the document under review
read_file(ONTOLOGY.md)    # binding invariants (I1-I11, composition rules)
read_file(implementation) # the actual code the spec will touch
curl/live-probe(external) # IF the spec depends on an external API/service
```

Never review a spec in isolation. The spec describes intent; the code reveals
reality. The invariants define what's allowed. Findings live in the gaps between
the sources. **If the spec integrates with an external API, probe it live.** Specs
frequently carry the phrase "verified against the live API" when only the happy
path was tested — boundaries, failure modes, and pagination are the cracks.

### Step 2 — Assign Attack Vectors (Not Checklists)

When the user provides specific attack vectors (e.g., "check ontology compliance,
physics gate interaction, talent gate interaction"), attack each one. When the
user doesn't, generate your own from the intersection of:
- Every binding invariant (I1-I11 in ONTOLOGY.md)
- Every gate/lifecycle type (A-H in CONNECTION-LIFECYCLE.md)
- Every component the spec touches but doesn't mention

### Step 3 — Trace Data Flow to Find Propagation Gaps

**This is the highest-yield technique.** For every field/tag/flag the spec
classifies or computes, trace it through the actual implementation:

```
Spec says: "classify lens → inject into specialist prompt"
Code reality: does ANY downstream consumer actually READ the lens tag?
```

If the spec produces a value but no code path consumes it, that's a propagation
gap. This is the single most common class of spec defect.

**Detection pattern:**
1. List every output field the spec's system produces
2. For each field, search the actual codebase for where it's consumed
3. If zero consumers exist → propagation gap finding

### Step 4 — Check Invariant Compliance Per-Finding

For each architectural invariant the spec might violate:
- Does the spec assign a responsibility to a component that the invariant says
  it must NOT have? (e.g., orchestrator "directs but does not execute" — if the
  spec has the orchestrator shaping output, that's execution, not direction)
- Does the spec create a relationship the invariant forbids? (containment vs
  reference, ownership vs maintenance)
- Does the spec assume a lifecycle type that doesn't match the component's
  actual type? (e.g., treating a CONDITIONAL gate as if it were PERMANENT)

### Step 5 — Identify Cross-Cutting Root Causes

After finding individual defects, look for a single root cause that explains
multiple findings. State it explicitly. This is more valuable than the individual
findings because it tells the spec author where to focus the fix.

Example from the Sherman 3D Vector review: 5 of 10 findings shared one root cause
—"the lens is classified but not propagated to downstream consumers." Fixing the
propagation architecture resolves all 5 simultaneously.

### Step 6 — Write Findings with Concrete Fixes

Each finding must include:
- **Severity** (CRITICAL / HIGH / MEDIUM) with justification
- **Concrete failure scenario** (step-by-step: what happens in production)
- **Code evidence** (cite actual line numbers from the implementation)
- **Proposed fix** (with code/pseudocode, not just "should be fixed")
- **Cross-references** to the invariant or lifecycle rule violated

Do NOT report a problem without a fix. Do NOT propose a fix without grounding it
in the actual code.

### Step 7 — Verify Quantitative Claims Against the Live System

Specs make quantitative claims ("2 API calls", "10-second budget", "per-page=200
covers 95% of users", "embeds in 150ms"). These are almost never tested at their
boundaries. Attack each:

1. **Find the boundary and test one past it.** Spec says "per-page=200" →
   request `per-page=201` and confirm the error. Spec says "10-second budget" →
   count the actual calls for the worst-case input (a 2000-paper author needs
   `ceil(2000/200)=10` paginated calls) and multiply by the code's own sleep/throttle
   constant. If the product exceeds the claim, the claim is a lie.

2. **Demand a source for any "% of users" / "% coverage" number.** If the spec
   asserts "covers 95% of researchers" with no citation, treat it as fabricated.
   The real distribution (PIs with 2000+ papers over a 30-year career) often
   invalidates the assumption.

3. **Check the dedup-key/data-shape fit.** If the spec's design dedups on
   `sha1(title|year|author)` but the actual input is a bare list of IDs (no title,
   no year, no author), the dedup is uncomputable from the available data. Curl
   the API, inspect the JSON keys actually returned, and confirm the design's
   fields can be populated. A dedup key requiring absent fields is a silent
   duplicate-generator.

4. **Verify DB constraints, not just column existence.** `.schema <table>` shows
   columns; `.indices <table>` shows what's enforced. A non-unique index is a
   performance hint, not a constraint — two concurrent writers CAN insert the same
   key. If the spec assumes a UNIQUE constraint that only exists as an INDEX,
   multi-writer scenarios produce duplicates.

### Step 8 — Cross-Check Designs From the Same Project Against Each Other

When reviewing multiple specs from one project/session, read them against each
other. The single highest-yield contradiction: **incompatible technical choices
across stages.** Stage 0 specifies SPECTER 2 embeddings (768-dim, local GPU);
Stage 1 specifies OpenAI text-embedding-3-small (1536-dim, API). Vectors from
different models cannot be cosine-compared — the feature that spans both stages
(here: similarity search) silently produces no results. Always confirm that
cross-stage assumptions are consistent, not just internally coherent.

## Finding Severity Calibration

- **CRITICAL:** The spec violates a BINDING invariant, or the defect produces
  silent data corruption / safety risk in production. Blocks implementation.
- **HIGH:** The defect causes degraded behavior in a common scenario. Should
  fix before the spec's final phase.
- **MEDIUM:** Coverage gap or edge case. Can ship with documentation.

## What NOT to Do

- **Do NOT repeat previous review findings.** Read the spec's "Quality Gate
  Responses" / revision history section first. List what was already found.
  Attack only NEW vectors.
- **Do NOT review the spec in isolation.** A spec that looks internally
  consistent can still violate binding invariants or assume code that doesn't
  exist.
- **Do NOT file findings without code evidence.** "The spec doesn't mention X"
  is weak. "The spec says X, but sherman_router.py line 549 shows Y" is strong.
- **Do NOT propose fixes that violate other invariants.** Check that your fix
  doesn't create a new I-violation.

## Common Propagation Gap Patterns

These recur across specs. Check for each:

1. **Classified-but-not-consumed:** A field is computed (lens tag, confidence
   score, operator identity) but no downstream component reads it. The field
   exists in the output but changes nothing.

2. **Gate fires at wrong phase:** A validation gate fires pre-execution (on the
   routing decision) but the spec assumes it validates post-execution output.
   The gate's lifecycle type (CONDITIONAL) is correct but its trigger point is
   wrong.

3. **Cross-harness contamination:** A shared learning signal (EWMA, feedback
   loop) is global when the organism has multiple harnesses with different task
   distributions. One harness's traffic dominates and corrupts routing for others.

4. **Chain step atomicity gap:** A multi-step pipeline (lens chain, tissue
   handoff) has no quality gate BETWEEN steps. Garbage from step N flows into
   step N+1. Crash failure is caught (retry); quality failure is not.

5. **Version pin absence:** An external model/library is referenced by name but
   not by immutable version (commit SHA). Silent upstream updates invalidate
   stored artifacts (embeddings, cached results).

6. **Governance vacuum:** A configuration dict/constant (keyword lists, threshold
   tables) has no owner, no change-control, no regression test. A single bad
   addition silently breaks routing for an entire category.

7. **Intervention bias in learning loops:** A learning system (EWMA, classifier
   feedback) trains on both implicit signals (user didn't re-route) AND explicit
   interventions (manual overrides). Training on interventions conflates two
   different learning signals and poisons the model.

## References

- `references/sherman-3d-vector-review-3.md` — Full case study: 3rd adversarial
  review of the Sherman 3D Vector spec. 10 findings (5 CRITICAL), demonstrating
  the three-source cross-reference method, propagation gap detection, and
  cross-cutting root cause identification.
- `references/constellation-otlet-review.md` — Case study: adversarial review of
  Constellation/Otlet Stage 0 & Stage 1 API-integration specs. 9 findings (3
  CRITICAL) demonstrating Steps 7–8: quantitative-claim verification against the
  live OpenAlex API, dedup-key/data-shape fit checks, DB-constraint inspection,
  and cross-design contradiction detection.

## Related Skills

- `code-review` — for PR-level code changes (after implementation, not before)
- `adversarial-elite-panel-review` — for deployment readiness (git, CSS, fresh clone)
- `ds-popper-audit` — for research/scoring integrity (citations, tiers, FDA language)
- `organism-biological-isomorphism-verification` — for biological naming accuracy
