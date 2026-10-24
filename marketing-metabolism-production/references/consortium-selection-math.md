# Consortium Selection Math — Agent Decision Engine

**Created:** 2026-06-29
**Updated:** 2026-06-29 (all 8 dimensions protected, deeper math complete)
**Status:** DNA-encoded selection function. Every spin-out inherits it.
**Executable:** `marketing-consortium/src/selection_engine.py`

## Core Problem

When agent consortiums face a task and look at a library of philosophies,
frameworks, and case-study patterns, HOW do they decide which to apply?
Not heuristics. Not vibes. Math.

User correction (2026-06-29): "There's got to be some sort of a math behind
their decision making... it's not just based on legistics."

## Selection Function

```
Score(P, T) = 0.30 * DNA(P) + 0.25 * EIGHT_D(P) + 0.20 * FIT(P,T)
              + 0.15 * EVIDENCE(P) + 0.10 * CONTRARIAN(P)
```

| Component | Weight | What It Measures | Range |
|-----------|--------|------------------|-------|
| DNA(P) | 0.30 | the specialist engine DNA alignment | 0 to 1 |
| EIGHT_D(P) | 0.25 | 8D HUMAN wellness alignment | -1 to +1 |
| FIT(P, T) | 0.20 | Task-audience-channel fit | 0 to 1 |
| EVIDENCE(P) | 0.15 | Strength of evidence | 0 to 1 |
| CONTRARIAN(P) | 0.10 | Differentiation / anti-generic | 0 to 1 |

## Decision Rules

```
Step 1: 8D HUMAN WELLNESS GATE (mandatory pre-screen)
  IF EIGHT_D(P) < 0 -> REJECT (harms human consumer wellness)
  IF ANY of ALL 8 dimensions < 0 -> REJECT (no hierarchy of harm)

Step 2: DNA GATE (mandatory)
  IF DNA(P) < 0.5 -> REJECT (insufficient brand alignment)

Step 3: FREE ENERGY GATE (RATIO, not difference)
  F = COST(P) / [Score(P,T) * (1 + INFO_GAIN(P))]
  F >= 1.0 -> SKIP (cost exceeds value)
  F < 1.0 -> ADMIT

Step 4: SELECT
  From admitted candidates, hold top 3 in superposition
  Collapse on quality gate measurement (Luria)
```

## 8D Human Wellness Gate — CRITICAL DEFINITION

**This measures HUMAN consumer wellness.** NOT AI wellness. NOT system health.
The question: does this marketing content harm or support the HUMAN who
consumes it across the 8 dimensions?

User correction (2026-06-29): "Is it wellness for AI or is this wellness for
humans? Because there's a very big difference."

### ALL EIGHT Dimensions Protected (corrected 2026-06-29)

ALL EIGHT dimensions are protected. No exceptions. No hierarchy of harm.
Any negative score on ANY dimension = automatic REJECT:

| Dimension | Protected Against |
|-----------|-------------------|
| Physical | Harm to human bodies (health, sleep, movement, nutrition) |
| Psychological | Harm to human minds (manipulation, anxiety, exploitation) |
| Intellectual | Harm to human intellects (misinformation, dumbing down, confusion) |
| Social | Harm to human connections (division, loneliness exploitation, outrage) |
| Spiritual | Harm to human spirits (cynical co-opting of meaning, fake guru) |
| Vocational | Harm to human work (undermining professional integrity, exploitation) |
| Financial | Harm to human finances (predatory pricing, deceptive billing) |
| Environmental | Harm to human environments (wasteful consumption, destruction) |

The mission: heal humanity across all 8 dimensions. POSITIVE language only.

### Scoring Rubric (per dimension: +1 supports, 0 neutral, -1 harms)
- Physical: promotes health/awareness (+1), promotes harmful consumption (-1)
- Psychological: empowers/reduces anxiety (+1), manipulates/exploits (-1)
- Intellectual: educates/informs (+1), misinforms/dumbs down (-1)
- Social: builds genuine community (+1), exploits loneliness/division (-1)
- Spiritual: aligns with purpose/meaning (+1), exploits vulnerability (-1)
- Vocational: helps professional growth (+1), undermines integrity (-1)
- Financial: empowers financial literacy (+1), predatory/exploitative (-1)
- Environmental: promotes sustainability (+1), promotes waste (-1)

## the specialist engine DNA Scoring (4 markers)

```
DNA(P) = (physics_informed + bio_isomorphic + anti_slop + elite_standard) / 4
```

## Evidence Hierarchy
1.0 = peer-reviewed academic (JMR, Marketing Science)
0.8 = elite institutional methodology (Wharton, Kellogg, MSI)
0.6 = multi-company case study (3+ companies)
0.4 = single company case study
0.2 = practitioner opinion
0.0 = unproven

## Immutable Elements (Cannot Mutate Without principal Approval)
- ALL 8 protected dimensions (Physical, Psych, Intel, Social, Spiritual, Vocational, Financial, Environmental)
- DNA markers (physics-informed, bio-isomorphic, anti-slop, elite)
- REJECT on 8D < 0
- REJECT on DNA < 0.5
- Healing mission (positive language only)

## What CAN Mutate (within +-0.05 per generation)
- Weights (alpha, beta, gamma, delta, epsilon)
- T_urgency default
- Evidence thresholds (can be raised stricter, not lowered)

## Deeper Math Layer (COMPLETE — 44 formulas)

The quantitative math layer is complete across 3 tracks:
- Measurement (06a): sample size, power, Thompson sampling, MMM, ROMI, CAC/LTV, attribution
- Prediction (06b): Bass diffusion, prospect theory, SIR virality, K-factor, Aral research
- Valuation/Decision (06c): Interbrand, CBBE, Binet 60:40, Van Westendorp, EV, Shannon entropy, portfolio theory, UCB1, real options

Files at: `marketing-consortium/06a/b/c-QUANTITATIVE-MATH-*.md`

## Decision Sequence (9 Phases)

The formulas do NOT run all at once. They apply at specific phases:
- Phases 0-3 (before content): selection scoring, classification, no measurement
- Phase 4 (production): creative engines, no measurement math
- Phase 5 (quality threshold): anti-slop rules, brand coherence
- Phase 6 (prediction): Bass, K-factor, prospect theory
- Phase 7 (immediate measurement): CTR, engagement, dwell
- Phase 8 (delayed measurement): A/B stats, ROMI, attribution, incrementality
- Phase 9 (learning): Bayesian update, parameter refinement

Full detail: `marketing-consortium/07-DECISION-SEQUENCE.md`
