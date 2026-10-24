# Actual Built Gamification System Architecture

**Purpose:** Compact context block to pass to specialist reviewers so they
review the REAL production system, not planning documents.

**Last verified:** 2026-07-07

---

## System 1: Task Engine (organism/task_engine.py)

Physics-driven 8D life-task OS. Every task carries free energy:
- `F = cost - T × info_gain`
- cost = priority_weight + age (capped 7 days)
- T = priority weight (P0=3, P1=2, P2=1)
- info_gain = 1.0 on completion, 0.0 otherwise

Physics functions:
- `free_energy(t)`: F drops sharply on completion = dopamine moment
- `dim_strain(tasks, dim)`: strain = min(mean_F/10, 1.0) + 0.15×blocked_ratio + 0.25 if critical_slow. Critical slowing = task age > 72 hours.
- `coupled(dim)`: strain propagation across linked dimensions
- `microtask(parent, count)`: adiabatic breakdown into plan/do/verify

Coupling edges: physical.sleep↔psychological, psychological↔physical,
financial↔psychological, vocational↔psychological, intellectual↔physical.sleep,
social↔psychological.

## System 2: Bragg Lattice (ds-bragg-engine)

the specialist engine (Prefrontal Cortex BA 9/46, Action Selection). Tasks form a CRYSTAL
LATTICE. Each task = lattice site with energy = difficulty − urgency + dependency_bonus.
The lattice SETTLES to minimum energy via gradient descent (50 iterations, lr 0.1).
Lowest-energy site = selected action.

TaskLattice: add_task, add_coupling (strength 0.15). Coupling lowers energy:
total -= strength × (1 − abs(urgency_a − urgency_b)).
settle(): d(energy)/d(urgency) = difficulty − 2×urgency.

## System 3: Schultz RPE (organism/schultz_rpe.py)

the specialist engine reward prediction error (DS-ECS-NPR-13.01.07-v1.0.0, :port).
δ = R_actual − R_expected. Runs THROUGH existing engines:
Bragg (completion) → Schultz (RPE) → Carlsson (reinforcement) → Dale (broadcast).

Three modes:
- standard: raw δ
- scarcity_adjusted: δ × 1.5 (compensates ~33% VTA dampening under chronic
  cortisol). Floors to 0.1 when expectation met. Negative δ stays negative.
- habit_formation: δ declines toward zero. Sunset when avg|δ| < 0.15 over 21+ reps.

Rescorla-Wagner: E_new = E_old + 0.15×δ (bounded [0,10]). Per-user per-dimension
baselines persist to <agent-home>/state/schultz_baselines.json.
`check_sunset()` called by mechanics layer BEFORE awarding XP.

## System 4: XP Economy (ACTUAL FORMULA)

```
xp_reward = base_xp × coherence_multiplier × difficulty_multiplier × confidence_multiplier × pacing_multiplier
```

Five multipliers:
1. base_xp: task's intrinsic value
2. coherence_multiplier: rewards dimensional alignment
3. difficulty_multiplier: rewards harder tasks
4. confidence_multiplier: rewards high-confidence scoring data
5. pacing_multiplier: anti-inflation mechanism

## System 5: Experience Hierarchy

Goals > Quests > XP. Three separate concepts:
- XP: single action reward (one task completion)
- Quest: multiple XP events grouped (multi-step objective)
- Goal: multiple quests grouped (life objective)

Harada Mapping: 1 goal > 8 pillars/quests > 8 actions each.
Quest Sources: habit-based, signal-based, context-picked.
Quest Types: micro, daily, weekly, seasonal, lifetime, emergent.

## System 6: 8D Scoring Engine

TWC = η × μ × C × (1 + 0.5 × S)
- η = scaling constant
- μ = mean of 8 dimension scores
- C = coherence factor = 1 − σ/μ (penalizes variance)
- S = synergy tensor (rewards positive coupling)

8 Dimensions: Quantum Cognition (Psychological), Prigogine Thermodynamics
(Physical), Shannon Information Theory (Intellectual), Kuramoto Model (Social),
Consciousness Science (Spiritual), Flow Theory (Vocational), Prospect Theory
(Financial), Attention Restoration Theory (Environmental).

Coupling matrix: 28 unique inter-dimension pairs. Sigmoid psychometric curves.
SOS (System Operating Status): overall system health.
Baseline normalization: user-specific anchors, drift handling, version updates.

## System 7: Resonance + Mastermind Engine (the specialist engine)

Resonance Core: reads 8D scores as natural frequencies. Impedance matching.
Coupled wave propagation: Physical→Emotional (0.7), Physical→Intellectual (0.5).
Phase detection (depression/hypomanic/stable/transition).

Mastermind Core: advisor panel harmony. Third Mind generation (emergent insight).
Phase alignment protocol. Modes: Active, Consultation, Review, Emergency.
Mode Router: One-Off, Goal-Oriented, Situational, Advisory Panel.

## System 8: Habit Loop Chain

The complete computational skeleton:
Bragg (select action via lattice settling) → Schultz (RPE on completion) →
Carlsson (reinforcement learning) → Dale (broadcast signal).

Every game mechanic sits ON TOP of this chain.

## Source Files (for verification)

- Task engine: `/<workspace>`
- Bragg lattice: `/<workspace>`
- Schultz RPE: `/<workspace>`
- Architecture: `/<workspace>`
- Case file: `/<workspace>`
- Integration: `/<workspace>`
- Product thesis: `/<workspace>`
