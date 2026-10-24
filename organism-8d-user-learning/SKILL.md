---
name: organism-8d-user-learning
description: Use when organism learns owner via real 8D/TWC layers.
version: 1.0.0
---

# Organism 8D User Learning

Class-level skill for the operator agent-family organisms that personalize to **their user**, prevent burnout, and guide recovery using **Divinity Science 8D/TWC** — without recreating scoring, panels, or engines that already exist.

## When to Use

- Organism must learn the user, personalize, adapt technical level, heal, prevent burnout
- Building or reviewing Integrations + holistic user model
- Adversarial review of user-learning / health OS features
- Wiring a self-contained organism repo to 8D360 math
- Any agent invents `burnout_risk` strings or null 8D scores without calculator output

## Non-Negotiables

1. **`calculator.py` is the only TWC math.** Vendor a copy if the product ships self-contained. Never hand-compute TWC.
2. **Build on existing work first.** Search hydra-os 8D tracker, rescore engine, wave coaching, ds-selye / ds-attwell / ds-schultz before writing new scoring or healing engines.
3. **Owner-only memory.** Baselines and history are THIS owner's. Peer private state only via fungal network consent.
4. **Organism type lock.** B2BU = professional performance 8D. B2C = full personal health adapters. Do not mix personal health apps into B2BU by default.
5. **Elite brains only.** Never generalist "user learning module" design.

## Layer Stack (mandatory)

| Layer | Name | Job |
|-------|------|-----|
| L0 | Signals | Check-in, tech feedback, work sessions, free text |
| L1 | Adapters | Map to 1–10 dim estimates + confidence; blend with baseline |
| L2 | Baseline | Owner EWMA (`owner_baseline.json`); never peer defaults |
| L3 | TWC | `DimensionScore(score=dim10/10)` → `compute_twc` |
| L4 | Healing | Lowest dims, κ coupling notes, micro-actions, growth framing |
| L5 | Operating system | WIP limits, break cadence, check-in frequency, escalations |

Tech-level learning (integrations UI) feeds the **same** user model (Intellectual comfort/pain), not a parallel brain.

## Production Scoring Path (proven)

```
check-in payload
  → dim10 estimates (psy phy int soc spi voc fin env)   # 1–10
  → DimensionScore list with score = v/10
  → compute_twc(scores)   # coupling κ + coherence + synergy
  → classify_twc(twc_final)
  → healing_plan + operating_system
  → persist user_model + twc_history
```

Matches `score_from_evidence` / baseline-bridge product behavior.

### Critical pitfall: full sub-algorithm path alone

Feeding full `PsychologicalInput` / `SocialInput` / … through `score_*` then `compute_twc` often parks **healthy** days in "Needs focus" because sub-algorithms are hard to saturate. **Do not use that as the only ship path** for lightweight check-ins. Use dim10 → DimensionScore → `compute_twc`.

## Dimension Alias

- Constitution / UI: **Emotional**
- Calculator: **Psychological**
- One dimension. Alias only. Never invent a 9th.

## Psychology / Method Panel Seats

When designing or adversarially reviewing user-learning + healing OS, use elite consecutive seats:

| Seat | Lane |
|------|------|
| the specialist engine | Bias, baseline blend, no single-day identity |
| the specialist engine | Self-efficacy; interventions <15 minutes |
| the specialist engine | Growth framing; dips as recoverable state |
| the specialist engine | Allostatic load (stress × energy × sleep) with TWC |
| the specialist engine | Energy budget; Physical-first before VOC tactics |
| the specialist engine | Falsifiability; scores must move under evidence |
| CALIBER | No hand math; engine integrity |

Prefer calling existing engines over inventing intervention text: `ds-selye`, `ds-attwell`, `ds-schultz`, `ds-wave-coaching-engine`.

## Fresh Organism Rules

- Blank phenotype until setup
- No peer private panels or embedded fleet scorecards
- Inter-organism sharing = fungal network only
- No hardcoded local workspace paths at runtime

## Cyber the operator agent Reference (2026-08-02+)

- `organism/scoring/calculator.py` — vendored TWC math
- `organism/user_learning_engine.py` — L0–L5
- `organism/config/owner_baseline.json` — owner EWMA
- APIs - POST `/api/user/health-check` must return recorded true, twc_100, classification, engine, healing_plan; GET `/api/user/summary`; UI `/you`
- Phenotype **gg_core** (full the operator agent tech organism) — not locked b2bu. Can birth b2bu. Balanced 8D (0.125). Physics-PM in constitution.
- Health-first - L5 OS is downstream of TWC/healing, not a substitute.
- UI health form fields - stress_level, energy_level, sleep_quality, mental_state; success when recorded is true.
- See `references/cyber-gg-gg-core-health-api-2026-08-02.md`

## Smoke Expectations

- Healthy check-in → roughly Stable / Flourishing band
- Crash day → lower TWC; repair-first often Psychological / Physical / Vocational under high load
- `scoring_engine` on user model must name calculator path

## OPEN (do not fake done)

- Live engine calls from L4 (Selye/Attwell/Schultz/Wave)
- Multi-day TWC history charts
- B2C nutrition/transcript adapters without peer PHI
- Optional rescore_engine vendor for evidence-rescored days

## Related Skills

- `operations/8d360-unified-scoring-pipeline` — calculator + adapters (may be user-owned; recommend `hermes curator adopt` to patch)
- `operations/rescore-engine-usage` — never hand-rescore
- `operations/mastermind-protocol` — consecutive adversarial panels
- `anti-generalist-gate` — type lock B2C/B2B/B2BU
- `operations/physics-informed-ai-health-scoring` — AI-fleet native dims; not a substitute for human-owner 8D product path

## Support Files

- `references/layered-stack-and-dim10-path.md` — layer detail + product path recipe
- `references/adversarial-panel-user-learning-2026-08-02.md` — panel verdicts SETTLED/PROVISIONAL/OPEN
