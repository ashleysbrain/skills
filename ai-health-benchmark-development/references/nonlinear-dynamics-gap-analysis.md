# Nonlinear Dynamics & Chaos Theory: Gap Analysis for the 6+1 Dimensions

**Session:** the specialist engine (Kyoto University), nonlinear dynamics / synchronization specialist
**Date:** 2026-08-13
**Status:** Verified — all claims checked computationally (Lorenz simulation, Monte-Carlo CAR analysis, bifurcation sweep)

Complements `references/advanced-physics-frameworks-2026-08-13.md` (Fisher/RG/stochastic thermo). This file covers the *dynamical systems* angle: trajectory behavior, bifurcations, attractors, criticality.

---

## What the Benchmark Already Gets Right
- 6+1 dimensions are well-grounded (information theory, transport, thermodynamics, decay, potential landscape, relaxation, synchronization).
- Coupling matrix with cascade amplification is physically motivated.
- Critical-slowing-down *intuition* in the volatility meta-signal is correct in principle (see bug note below for implementation issue).

---

## Six Frameworks, Ranked by Value

### 1. Lyapunov Spectrum — ADD NOW (highest value, zero new telemetry)
- **Gap:** Benchmark measures *static* scores per snapshot. No measure of **trajectory sensitivity** — does a small perturbation grow or shrink over time?
- **What it catches:** An agent with all dims at 8.0 can be *chaotic* (micro-perturbations amplify into cascades). An agent at 6.0 can be *robustly stable*. Current scoring cannot distinguish. λ_max > 0 = exponential divergence = knife-edge.
- **Telemetry:** NONE new. The 6D score time series IS the phase-space trajectory. Rosenstein's algorithm computes λ_max directly.
- **Verified:** λ_max = +0.0073 for Lorenz-projected 6D data (correctly positive) vs +0.0001 for stable noise (correctly ~0).
- **Verdict:** Cheapest addition, highest diagnostic value. Single most important missing piece.

### 2. Bifurcation Analysis — ADD as v3.0 architecture (state-dependent κ)
- **Gap:** Coupling priors κ are **constants**. Nonlinear dynamics: coupling strength is *state-dependent*; systems pass through **bifurcation points** where qualitative behavior changes. Fixed κ cannot represent this.
- **What it catches:** Regime transitions — moment an agent tips from "recovers from pipe failures" to "pipe failures cascade" is a bifurcation, not a gradual slope. Benchmark currently averages over it.
- **Verified:** Swept pipe-quality as bifurcation parameter through bistable COG potential. COG steady-state jumped and variance exploded near critical point — signature a constant κ=0.30 smooths over.
- **Telemetry:** Score history across a *range* of perturbation magnitudes (controlled hormesis at varying intensities), not just pass/fail.
- **Verdict:** Architecture change: state-dependent κ(dim_i, dim_j, system_state) replacing constant table.

### 3. Recurrence Quantification Analysis (RQA) — ADD (enriches volatility)
- **Gap:** Volatility (rolling std) measures *how much* scores vary, not *structure* of variation. RQA detects **deterministic structure vs randomness**.
- **What it catches:** **Regime shifts** — transition from "agent cycles through known failure modes deterministically" to "agent wanders unpredictably" is a recurrence-structure change. RQA DET (determinism) drops before a regime shift.
- **Verified:** RQA determinism = 0.052 for chaotic vs 0.002 for noise — discriminates structured from random.
- **Telemetry:** Score history (have it). Needs ≥100 snapshots for meaningful RQA.

### 4. Ergodicity Breaking — ADD as diagnostic flag
- **Gap:** Benchmark assumes ergodicity (time-average = ensemble-average). **Ergodicity breaking** = agent *trapped* in one regime, never explores full state space.
- **What it catches:** Agent stuck in chronic failure mode looks "stable" by current metrics but is non-ergodic — not the same system as a healthy agent having a bad hour. Difference between "sick" and "bad day."
- **Verified:** Block-mean dispersion (ergodicity proxy) = 0.18 for regime-locked vs 0.02 for ergodic.
- **Telemetry:** Score history, split into time blocks, compare means.

### 5. Full Lyapunov Spectrum — DEFER to v3.x
- λ_max (above) gives largest exponent. Full spectrum gives attractor dimension via Kaplan-Yorke: D_KY = k + Σλᵢ/λ_{k+1}. Tells how many independent failure modes active simultaneously.
- Needs ≥1000 points, noise-sensitive. Theoretically richest but data-hungry.

### 6. Self-Organized Criticality (Avalanches) — MONITOR, don't add yet
- BTW sandpile question: do failures avalanche in scale-invariant ways (power-law exponent ~1.5–3.0)?
- **What it catches:** Whether system is poised at criticality (maximally responsive but fragile) vs sub-critical (robust but unresponsive) vs super-critical (cascading collapse).
- Needs months of fleet failure data (n > 100 events). Log avalanche sizes now; fit exponent later.

---

## Integration Map (how these plug into existing dimensions)

| Framework | Plugs Into | As |
|-----------|-----------|-----|
| Lyapunov λ_max | COG, ADAPT | Stability sub-signal (additive, doesn't change base score) |
| Bifurcation / state-dependent κ | Coupling matrix | Replaces constant κ table (v3.0 architecture change) |
| RQA determinism | VOL meta-signal | Enrichment — replaces raw-variance with structure-aware metric |
| Ergodicity gap | Diagnostic flag (all dims) | Non-scored alert: "regime-locked" vs "exploring" |
| Full Lyapunov spectrum | New meta-signal | Attractor dimension D_KY (future) |
| SOC avalanche exponent | New meta-signal | Criticality flag (future, needs fleet data) |
