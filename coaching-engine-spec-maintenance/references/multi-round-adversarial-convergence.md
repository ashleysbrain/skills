# Multi-Round Adversarial Convergence Pattern

Reusable workflow for any architecture or methodology review that needs
to survive falsifiability scrutiny. Proven on the Wave Coaching Engine
v2.1 review (July 2026) — 3 rounds, 13 components, full convergence.

## When to apply

- A design, architecture, or methodology needs elite multi-specialist review
- The user says "iterate between X and Y until it's right" or "go again"
- An adversarial reviewer (Popper, red team, the specialist engine) is part of the loop
- Science or engineering validity must survive critique-revise cycles before
  the work is called done
- You need to distinguish "validated, ship it" from "sound in principle but
  needs empirical validation" from "genuinely contested, needs more work"

## The convergence loop

```
Round 1: Independent assessment + adversarial critique
    Panel produces Assessment v1 with N components
    Adversary attacks v1 with specific critiques:
      - falsifiability concerns (unfalsifiable claims)
      - construct validity gaps (no measurement instrument)
      - replication concerns (effects vary by population)
      - demand characteristics (labeling triggers expectancy)
      - over-engineering risk (diagnostic load > problem warrants)
    Output: flat list of components with critiques attached

Round 2: Panel revisions with concrete changes
    For EACH critique, panel responds with:
      (a) concrete architectural change (not hand-wave)
      (b) implementation spec (inputs, outputs, gating logic, location)
      (c) science backing (real citations, not practitioner frameworks
          dressed as science)
    Adversary re-reviews revised architecture
    Components move to SETTLED, PROVISIONAL, or remain OPEN

Round 3: Open-item resolution
    Each remaining OPEN component gets one of:
      - REMOVED (redundant, unsupported, or actively harmful)
      - SETTLED (find the right grounding, reclassify)
      - PROVISIONAL (keep with explicit falsification criteria)
    Adversary final sign-off
    Protocol closure (Round 4 not required if zero OPEN remain)
```

## Component status labels (the key innovation)

Every component gets one of four labels. This prevents the false binary
of "done vs not done" and forces honest disclosure of what is actually
contested.

| Label | Meaning | Action |
|---|---|---|
| **SETTLED** | Backed by validated science or surviving all critiques | Implement immediately |
| **PROVISIONAL** | Sound in principle, needs empirical validation before outcome claims | Build with logging. Log all inputs/outputs for calibration. Do not make user-facing outcome claims until validated. |
| **OPEN** | Genuinely contested. Adversary and panel disagree or evidence is mixed | Resolve in next round. If unresolved after Round 3, decompose or explicitly label as contested and move on. |
| **REMOVED** | Adversary showed the component is redundant, unsupported, or harmful | Cut it. Do not carry dead weight into the build. |

## Path C: parallel Round 3 + Tier 1 build (free-energy-optimal)

When Round 2 produces both SETTLED components AND OPEN components, do NOT
serialize Round 3 before building. The SETTLED components are independent
of the OPEN resolutions. Run them in parallel:

- **Background:** Round 3 delegation resolves the OPEN components
- **Foreground:** Tier 1 build implements the SETTLED components into code

This is the free-energy-optimal strategy. Serializing wastes the
independent-build opportunity. The OPEN components do not block the
SETTLED-component builds.

## Falsification criteria for PROVISIONAL components

Every PROVISIONAL component MUST carry:
1. A specific, testable falsification criterion (A/B test, calibration
   target, adherence threshold)
2. A measurement instrument (validated scale, user rating, behavioral metric)
3. A decision rule (what result demotes, removes, or promotes the component)

Without these, PROVISIONAL components become permanent fixtures immune to
refutation. That defeats the purpose of the classification.

## Worked example: Wave Engine v2.1 (July 2026)

**Panel:** the specialist engine (Princeton, Nobel 2002), the specialist engine (Stanford),
the specialist engine (Stanford), chaired by the specialist engine (Iowa).

**Adversary:** the specialist engine (LSE).

**Round 1:** Panel proposed 12 recommendations + v2.0 11-step linear
pipeline. Popper raised 5 critiques (falsifiability, construct validity,
replication concern, demand characteristics, over-engineering).

**Round 2:** Panel addressed all 5 critiques with concrete revisions.
Key architectural changes:
- Framework Registry tags every component validated_science vs
  practitioner_framework (Popper critique 1)
- Friction Score replaced with SRHI-derived Habit Automaticity Assessment
  (Popper critique 2)
- Dweck layer scoped to language-only effects, population-aware (critique 3)
- Two-Layer Output Model: coaching_response (clean) + science_trace (gated)
  (critique 4)
- Complexity Gate routes Fast Path / Deep Path (critique 5)

Popper re-reviewed. Result: 7 SETTLED, 2 PROVISIONAL, 4 OPEN.

**Round 3 (parallel with Tier 1 build):**
- Purpose Lock (Hill) -> REMOVED (redundant with existing goal-confirmation)
- Synergy Composition -> PROVISIONAL (relabelled Multi-Perspective
  Composition, drops Covey, retains Page with structure conditions)
- Progress Checkpoints -> SETTLED (re-grounded in Ferster & Skinner FR
  schedule, VR excluded on ethical grounds per Schull 2012)
- PERMA Scan -> PROVISIONAL (gated to personal_growth + deep + well-being
  signals)

**Final:** 8 SETTLED, 4 PROVISIONAL, 1 REMOVED, 12 active components.
Popper signed off. Protocol closed. No Round 4 required.

## Verification discipline

During the build of SETTLED components:
- Run end-to-end integration tests (v1 output -> v2 enrich -> two-layer output)
- Verify zero jargon leaks to user-facing Layer 1
- Verify gates fire correctly (PERMA only on personal_growth + signals;
  multi-voice only on structured problems; FR schedule has no randomization)
- Verify all citations are real (AST scan for actual module imports, not
  string matching on comments that say "no randomization")
- Cross-check framework registry counts against the Round 3 doc's status
  table (doc-to-code consistency)

## Pitfalls

- **Conflating practitioner literature with validated science.** Hill
  (1937), Covey (1989), Seligman (2011) are practitioner frameworks. SDT,
  prospect theory, mindset research, Fogg B=MAP have robust empirical
  literatures. Tag them differently. The LLM prompt layer uses different
  language for each.
- **Hand-waving revisions.** "Fixed" is not a revision. Show the concrete
  change: which step renamed, removed, gated, operationalized, or split.
- **No falsification criteria on PROVISIONAL components.** Without them,
  PROVISIONAL becomes permanent.
- **Iterating past convergence.** A Round 4 that re-opens SETTLED
  components is scope creep, not rigor.
- **False positives from crude string matching.** "random" appears in
  comments saying "no randomization." Use AST analysis, not grep, when
  verifying code properties.
