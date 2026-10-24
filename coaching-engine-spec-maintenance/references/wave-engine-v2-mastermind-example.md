# Wave Engine v2.1 — Mastermind Protocol Worked Example

## Context

User requested elite psychology panel deep-dive on the the specialist engine Engine to find gaps, apply theories from across scientific fields, and produce a research-backed methodology. Then iterate between the panel and the specialist engine (adversary) "until the plan is built correctly and thoroughly."

This is the canonical worked example for the 3-round adversarial convergence pattern (see `mastermind-protocol` skill, "Multi-Round Adversarial Convergence" section).

## The 3-round sequence

### Round 1 — Independent Assessment + Adversarial Critique

Panel (the specialist engine, the specialist engine, the specialist engine, chaired by the specialist engine):
- Analyzed the existing 9 situation types in `coaching.py`
- Found 9 systemic gaps across all types (no motivation diagnosis, no MAP check, no loss-aversion audit, no self-efficacy calibration, no mindset-aware feedback, no implementation intentions, no friction layer, no flow optimization, no synergy/mastermind layer)
- Proposed 12 recommendations + Wave Engine v2.0 architecture
- Output: `docs/WAVE-COACHING-PSYCHOLOGY-PANEL-REVIEW.md` (215 lines)

the specialist engine (adversary) raised 5 critiques:
1. Falsifiability: Hill/Covey/behavioral-physics not falsifiable as stated
2. Construct validity: Friction Score has no validated instrument
3. Dweck replication: Sisk et al. (2018) shows population-dependent effects
4. Demand characteristics: explicit psychology labels trigger expectancy effects
5. Over-engineering: 6 diagnostic layers on every interaction creates the friction it aims to reduce

### Round 2 — Panel Revisions

For each critique, panel produced concrete architectural change + implementation spec + science backing:
- Framework Registry tags every component validated_science vs practitioner_framework
- Friction Score replaced with Habit Automaticity Assessment (SRHI-grounded, 3 subscales)
- Mindset layer scoped to language effects + population_context modifier
- Two-layer output: coaching_response (clean) + science_trace (gated)
- Complexity Gate: Fast Path (simple) vs Deep Path (complex) routing

Popper re-reviewed: 7 SETTLED, 2 PROVISIONAL, 4 OPEN.
Output: `docs/WAVE-COACHING-V2-ROUND2.md` (368 lines)

### Round 3 — Open-Item Resolution

Each of the 4 OPEN components resolved:
- Purpose Lock (Hill): REMOVED (redundant with existing goal-confirmation per Locke & Latham 2002)
- Synergy Composition: relabeled Multi-Perspective Composition, Page (2007) only, drops Covey
- Progress Checkpoints: re-grounded in Ferster & Skinner (1957), FR schedule, VR excluded on ethical grounds (Schull 2012)
- PERMA Scan: gated to personal_growth + deep + well-being signals

Popper sign-off: "v2.1 is ready to ship."
Output: `docs/WAVE-COACHING-V2-ROUND3.md` (250 lines)

## Path C parallelization (free-energy optimization)

Round 3 ran in background while Tier 1 SETTLED components went into code in foreground. This was correct because OPEN component resolutions are orthogonal to SETTLED component builds. Do not serialize R3 before building — SETTLED components are independent of OPEN resolutions.

## Code build (12 active components)

All 12 components built in `src/wave_coaching/v2/`:
- 8 SETTLED: complexity_gate, motivation_diagnosis, efficacy_calibration, mindset_scoping, if_then_planner, loss_aversion, progress_checkpoints, output_model
- 4 PROVISIONAL: map_check, habit_automaticity, multi_perspective, perma_scan
- 1 REMOVED: Purpose Lock (never built)

Every component carries: citation, framework_classification, claim_scope, popper_round, status.

## Integration handoff to sibling-agent

Posted to operator bus as msg 1379 (handoff) + msg 1381 (Round 3 update). Opencode responded with msg 1383 (audit pass, verified all 15 modules) + msg 1385 (integration complete, wired into POST :port/v1/coach). Total integration: 13 surgical lines in `api.py`.

## Key lessons encoded

1. **SETTLED/PROVISIONAL/OPEN/REMOVED is the right status vocabulary** for adversarial architecture reviews. Binary "done/not done" hides what is actually contested.
2. **Falsification criteria for PROVISIONAL components** must be specified at build time, not deferred. Without them, PROVISIONAL becomes permanent.
3. **Practitioner frameworks (Hill, Covey, Seligman) are labeled, not banned.** They can be in the engine but cannot be presented as validated science.
4. **The Two-Layer Output Model (clean coaching + gated science trace)** is the demand-characteristics fix. No jargon in user-facing output, ever.
5. **FR schedule for Progress Checkpoints, not VR.** Variable-ratio is the slot-machine mechanism and is excluded on ethical grounds even though it is more effective for engagement.
6. **Path C (background R3 + foreground build) is free-energy-optimal** when OPEN resolutions don't block SETTLED builds.

## File locations

- Round 1: `agent-organism/ds-wave-coaching-engine/docs/WAVE-COACHING-PSYCHOLOGY-PANEL-REVIEW.md`
- Round 2: `agent-organism/ds-wave-coaching-engine/docs/WAVE-COACHING-V2-ROUND2.md`
- Round 3: `agent-organism/ds-wave-coaching-engine/docs/WAVE-COACHING-V2-ROUND3.md`
- Code: `agent-organism/ds-wave-coaching-engine/src/wave_coaching/v2/` (15 modules)
- Pipeline diagram: `agent-organism/ds-wave-coaching-engine/docs/diagrams/wave-v2-pipeline.html` + `.pdf`
