# Adversarial Science Review — Rev L (2026-08-03)

Deep audit of actual the operator agent process flows for slide 2 accuracy.
Sources: BOOT.md, SOUL.md, AGENTS.md, WORKLOAD-SPLIT.md, physics_gate.py, mastermind-protocol skill.

## What was wrong in rev K

The rev K slide 2 prompt described the Physiomorphic process at the wrong level of abstraction. It showed a simplified 3-stage flow (DIGEST -> SPECIALISTS+SYNTHESIS -> AUDIT) and conflated several distinct architectural layers.

| Error in rev K | Correction from source code |
|---|---|
| DIGEST -> SPECIALISTS -> SYNTHESIS -> AUDIT | DIGEST -> EXCHANGE -> ORDER -> EXECUTE -> CONSOLIDATE (5 stages, not 3) |
| ORDER and EXECUTE missing | ORDER = free-energy filter on atomic steps. EXECUTE = one specialist at a time via Sherman, physics gate wrapping. |
| EXCHANGE buried inside mastermind loop | EXCHANGE is its own stage (stage 2), before ORDER |
| Six modules shown as a cluster stage | These are background engines (heartbeat, autonomic bridge, regulation). NOT sequential process steps. |
| Diagnostics as one feedback node | Physics gate has 3 stages: pre-flight (GO/SKIP/FORK), in-flight (CONTINUE/PAUSE/REDESIGN), post-flight (ACCEPT/REDO/CONSOLIDATE). Each forces a binding decision. |
| Mastermind = specialist-level loop | Mastermind runs between OPERATORS (hermes + sibling-agent), not between specialists. Sherman routes each task to one specialist within each operator. |
| Audit as two badges at end | Physics gate runs continuously: pre/during/post on every operation, not just before output |

## The actual SOLVE Protocol (from BOOT.md + AGENTS.md)

```
DIGEST: restate ask. Gather state (files, sibling work, git log, operator bus). Label DONE/MISSING/CONFLICTING. NO EDITS.
   ↓
EXCHANGE: read sibling operator's recent work BEFORE producing your own.
   R1 (independent assessment) -> read sibling R1 -> R2 (refine).
   Never duplicate, never conflict.
   ↓
ORDER: decompose into smallest atomic steps.
   Free-energy filter: drop any step where F = cost - T*info_gain > 0.
   Adiabatic sequence: safest, dependency-first, smallest change.
   ↓
EXECUTE: act in order. ONE specialist at a time (Sherman routes).
   Each step wrapped in physics gate (3 stages, binding verdicts):
     PRE-FLIGHT: GO / SKIP / FORK
     IN-FLIGHT: CONTINUE / PAUSE / REDESIGN / COLLAPSE
     POST-FLIGHT: ACCEPT / REDO / CONSOLIDATE
   ↓
CONSOLIDATE: one output neither operator could alone.
   Post handoff to sibling.
```

## The Physics Gate (from physics_gate.py)

3-stage operation wrapper. Every operation (task dispatch, engine call, file edit, subagent spawn, comms) can be wrapped.

1. PRE-FLIGHT (before the op runs)
   - Free energy: F = cost - T*info_gain. F > 0 -> SKIP.
   - Adiabatic: change_size > safe limit -> PAUSE.
   - Superposition: ambiguity high + branches -> FORK.
   - Verdicts: GO | SKIP | FORK

2. IN-FLIGHT (during long-running ops)
   - Critical slowing: recovery_times trending up -> PAUSE-REDESIGN.
   - Entanglement: a dependency just collapsed -> COLLAPSE.
   - Verdicts: CONTINUE | PAUSE | REDESIGN | COLLAPSE

3. POST-FLIGHT (after the op returns)
   - Entropy delta: post_uncertainty - pre_uncertainty. delta > 0 -> REDO. delta <= 0 -> ACCEPT. delta <= -threshold -> CONSOLIDATE.
   - Stress delta: post_stress - pre_stress > limit -> REDO.
   - Verdicts: ACCEPT | REDO | CONSOLIDATE

Body analog: Pre-flight = sensory gating (thalamus). In-flight = anterior cingulate conflict monitoring. Post-flight = hippocampal consolidation gate.

## The Mastermind Protocol (from mastermind-protocol skill + WORKLOAD-SPLIT.md)

OPERATOR-level, not specialist-level. Runs between hermes and sibling-agent.

```
R1: each operator produces independent assessment FIRST (before reading sibling work)
Exchange: structured handoff (3 parts):
   1. What I found (domain expertise applied)
   2. What I need from you (where domains overlap)
   3. Gap I see (what neither covers)
R2: each re-evaluates WITH the other's handoff as input. Adjust. Stay in own lane.
Synthesis: merge best of each. NOT blending. Plated dish, not smoothie.
   The synthesizer does NOT add new analysis. They merge, organize, prioritize.
```

Rules:
- Each specialist maintains identity (biologist stays biologist).
- Handoffs are structured (3 parts), not free-form chat.
- Maximum 2 rounds for bilateral exchange (R1 + R2).
- Synthesis preserves specialist voices.
- Adversarial loops exempt from 2-round cap.

Autonomic coordination (runs without user intervention):
- Heartbeat watchdog: every 2 min
- Autonomic bridge / vagus nerve: every 2 min
- R2 reflex arc: every 10 min

## Background subsystems (NOT process steps)

These run continuously and are NOT sequential stages in the I/O path:
- Heartbeat watchdog (cardiac automaticity)
- Autonomic bridge (vagus nerve, operator bus polling)
- R2 reflex arc (processes claimed bus messages)
- Regulation, recovery, defense, timing engines

The six modules shown on slide 1 body map (SPECIALISTS, COORDINATION, REGULATION, RECOVERY, DEFENSE, TIMING) represent these background subsystems. They should NOT appear as a cluster stage between INPUT and OUTPUT on slide 2.

## The "mandatory" principle (adversarial audit rev K finding)

The Physiomorphic distinction from existing frameworks rests entirely on the word **mandatory**:

- LangGraph CAN build R1/exchange/R2/synthesis (it is Turing-complete over a graph), but it does not REQUIRE it.
- AutoGen's conversation graph is free-form turns, not a forced two-round independent->informed re-evaluation.
- The distinction is mandatory vs optional.

**Without the word "mandatory," the skeptic is correct: Physiomorphic is just a well-architected LangGraph app.**

## Corrected slide 2 Physiomorphic column structure

```
INPUT (user query + data)
  ↓
DIGEST: restate task, gather state, read sibling work + operator bus before editing
  ↓
EXCHANGE: R1 independent assessment -> structured handoff -> R2 informed re-evaluation
  (mandatory mastermind exchange between operators, shown as horizontal loop)
  ↓
ORDER: decompose into atomic steps. drop steps where cost exceeds information gain.
  ↓
EXECUTE: one specialist at a time, routed by thalamic gate
  [PRE-FLIGHT: GO/SKIP/FORK]
  [IN-FLIGHT: CONTINUE/PAUSE/REDESIGN]
  [POST-FLIGHT: ACCEPT/REDO/CONSOLIDATE]
  ↓
CONSOLIDATE: one output neither operator could produce alone. post handoff to sibling.
  ↓
OUTPUT: code · documents · analysis · decisions
```

## Gate: SHIP WITH FIXES

The process flow is now accurate to the source code. The distinction is real but narrow and rests on mandatory primitives + physics gates + operator-level mastermind exchange.
