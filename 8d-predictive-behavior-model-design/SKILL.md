---
name: 8d-predictive-behavior-model-design
version: 1.0.1
description: Research-backed design for using the 8 dimensions of wellness as a predictive behavior modeling framework in a health product — state model, calculations, data requirements, UX output, and caution areas.
trigger: When designing, building, or extending the 8D360 scoring engine beyond static total wellness scores into trajectory prediction, latent-state modeling, and personalized recommendations.
tags: [8d, wellness, predictive, behavior-modeling, state-space, latent-variable, trajectory, recommendations, product-design]
---

# 8D Predictive Behavior Model Design

## Context

The 8 dimensions of wellness (PSY/Head, PHY/Body, ENV/Space, SOC/People, SPI/Purpose, INT/Growth, VOC/Work, FIN/Money) form a measurement theory grounded in SAMHSA's framework and validated across multiple psychometric instruments (Perceived Wellness Survey, Body-Mind-Spirit Wellness Behavior Characteristic Inventory, Anschutz Wellness Measurement). The existing 8D360 system computes a coupled TWC score. This document extends it into a **predictive behavior model** — a state-space engine that goes beyond "what's your score" into "where are you heading, what will happen next, and what should you do."

## Presentation / handoff guidance
When this model is turned into a founder-facing artifact, present it as a **layered document** rather than a single dense summary:
- use a polished cover or hero section
- separate each layer into its own card or section
- spell out the equations explicitly for comprehension
- include a stack-order section and a next-steps section
- for Divinity Science outputs, prefer a premium dark-blue-and-gold visual system when the user asks for a branded PDF
- if the user wants a meeting artifact, produce the PDF first, then wait for the next instruction rather than compressing the content prematurely

See `references/your-org-behavioral-physics-presentation-notes.md` for the session-specific layout and delivery notes.

---

## 1. Recommended Wellness-State Model Design

### Architecture: Hybrid State-Space + Cross-Lagged Panel Model

The model has three layers:

```
Layer 1: OBSERVED VARIABLES (data inputs)
  └── Per-dimension telemetry from check-ins, wearables, journals, passive sensors

Layer 2: LATENT STATE VECTOR (8D state at time t)
  └── D(t) = [PSY, PHY, ENV, SOC, SPI, INT, VOC, FIN] ∈ [0, 10]^8
  └── Each dimension is a LATENT variable inferred from multiple observed indicators
  └── Confidence weighting per dimension (from existing merger architecture)

Layer 3: LATENT REGIME (hidden Markov state)
  └── S(t) ∈ {Thriving, Stable, Drifting, Declining, Crisis}
  └── Captures the overall system state that individual dimensions don't describe alone
```

### Why This Hybrid

**Pure VAR (Vector Autoregression)** captures cross-dimensional lag effects (e.g., PHY drop today → PSY drop in 3 days) but assumes stationarity and linear dynamics — wellness is nonlinear.

**Pure HMM (Hidden Markov Model)** captures regime shifts (user enters "declining" state) but loses the continuous dimension-level signal.

**The hybrid uses VAR for dimension-level trajectory and HMM for regime-level state.** This is the standard approach in modern health trajectory modeling (see: Bayesian hierarchical VAR for patient trajectories, PMC6294362; dynamic factor models for longitudinal health, arXiv 2412.08873).

### State Transition Model

```
D(t+1) = A · D(t) + B · X(t) + C · ε(t)       [VAR component — 8×8]

S(t+1) | S(t) ~ Cat(π_{S(t)})                    [HMM component — 5×5]

Where:
  A = 8×8 autoregressive + cross-lag coefficient matrix
  X(t) = exogenous inputs (interventions, life events, time-of-week)
  B = exogenous coefficient matrix
  C = noise scaling matrix (dimension-specific volatility)
  ε(t) ~ N(0, I)
  π = transition matrix for regimes, conditioned on D(t) aggregated metrics
```

### The A Matrix: Cross-Lagged Coupling

This is the **engine room**. Each cell A[i,j] answers: "How much does dimension j's score yesterday predict dimension i's score today?"

Research-backed candidate interactions (from cross-lagged panel studies in health psychology):

| From → To | Expected A[i,j] | Rationale |
|---|---|---|
| PHY → PSY | +0.15 to +0.25 | Physical activity/exercise → mood elevation (robust evidence) |
| PSY → PHY | +0.10 to +0.15 | Psychological state → health behaviors (bidirectional, weaker) |
| SOC → PSY | +0.10 to +0.20 | Social connection → emotional wellbeing (strong in loneliness lit) |
| PSY → SOC | +0.08 to +0.15 | Withdrawal in low periods → social isolation |
| FIN → PSY | +0.10 to +0.20 | Financial stress → anxiety/depression (strong in health econ) |
| FIN → SOC | +0.05 to +0.10 | Financial strain → social withdrawal |
| PHY → INT | +0.08 to +0.12 | Exercise → cognitive performance |
| PSY → VOC | +0.10 to +0.18 | Mental state → work productivity |
| SOC → SPI | +0.05 to +0.10 | Community → sense of purpose |
| ENV → PHY | +0.08 to +0.12 | Environment quality → physical health behaviors |
| SPI → PSY | +0.08 to +0.15 | Purpose/meaning → resilience under stress |

These are STARTING values — they must be calibrated per-user with at least 30 days of data (see calibration section).

### Regime Definitions (HMM States)

| Regime | Typical D(t) Pattern | Interpretation |
|---|---|---|
| **Thriving** | Most dims ≥ 7.0, coherence high | User is in a growth phase. Recommendations: stretch goals, new challenges |
| **Stable** | Most dims 5.0-7.0, low volatility | Maintenance mode. Recommendations: consistency, small improvements |
| **Drifting** | Mixed dims, slow decline in 2-3 dims over 7+ days | Early warning. Recommendations: targeted dimension support |
| **Declining** | 3+ dims dropping, PSY or PHY below 4.0 | Active concern. Recommendations: stabilizing actions, reduce cognitive load |
| **Crisis** | Multiple dims < 3.0, high volatility | Protective mode. Recommendations: safety resources, minimal demands |

### Emission Function: Regime → Observed Behavior

The regime S(t) emits observable patterns:
- Check-in completion rate (dropping = possible decline)
- Response latency (slower = possible drift/decline)
- Volunteered information richness (less detail = possible withdrawal)
- Goal engagement metrics

This allows the model to infer regime even from sparse data.

---

## 2. Candidate Calculations

### 2.1 Trajectory Prediction (7-Day Forecast)

```python
# D_forecast[t+k] = A^k · D_current + Σ(A^i · B · X_forecast)
# For k = 1..7 days ahead
# Confidence degrades: conf(t+k) = conf(t) * decay^k where decay ≈ 0.90
```

Output: For each dimension, a predicted score range for each of the next 7 days with widening confidence bands.

### 2.2 Cascade Risk Score

"How likely is a drop in dimension X to cascade to other dimensions?"

```python
cascade_risk[dim_i] = Σ_j |A[j,i]| * P(D_j declining)
# Uses column i of A matrix — how much dim_i affects ALL other dims
# Weighted by the probability each target dimension is in a declining state
```

This replaces the static coupling coefficients with dynamic, state-dependent cascade risk.

### 2.3 Intervention Leverage Score (ILS) — Enhanced

The existing ILS identifies which dimension to intervene on. The predictive version adds:

```python
ILS_predicted[dim_i] = cascade_risk[dim_i] * (baseline[dim_i] - predicted[dim_i, +7d]) * intervenability[dim_i]
```

Where `intervenability` is a per-dimension ease-of-change coefficient (PHY is easier to move quickly than FIN; PSY responds faster to intervention than ENV):

| Dimension | Intervenability (rough) | Fastest realistic change |
|---|---|---|
| PHY | 0.80 | Days (exercise, sleep) |
| PSY | 0.70 | Days-weeks (behavioral activation) |
| SOC | 0.50 | Weeks (relationship building) |
| INT | 0.60 | Days (learning engagement) |
| ENV | 0.30 | Weeks-months (environment changes) |
| SPI | 0.40 | Weeks (meaning practices) |
| VOC | 0.45 | Weeks (work changes) |
| FIN | 0.25 | Weeks-months (financial planning) |

### 2.4 Regime Transition Probability

```python
P(S(t+7d) = "Declining" | S(t) = "Stable", D_trajectory) = softmax(f(D_trend, D_volatility, cascade_risk))
```

User-facing output: "Based on your current trajectory, there's a 23% chance you'll enter a declining pattern within the next week."

### 2.5 Coherence Index (Dynamic)

The existing coherence calculation measures how balanced dimensions are. The predictive version tracks coherence over time:

```python
coherence_trend = coherence(t) - EWMA(coherence, span=14)
# Negative trend = dimensions becoming more imbalanced
# This is an early signal even when individual scores look fine
```

### 2.6 Personalized Dimension Interaction Discovery

After 60+ days of per-user data, estimate a USER-SPECIFIC A matrix using Bayesian updating:

```python
# Prior: population A matrix (from research literature + aggregate data)
# Likelihood: user's observed transitions
# Posterior: personalized A matrix with uncertainty

A_user = (precision_prior * A_pop + n_user * S_user) / (precision_prior + n_user)
```

This means the system LEARNS that for THIS user, PHY→PSY coupling is 0.30 (stronger than average) while FIN→SOC is 0.02 (nonexistent). Personalized coupling means personalized predictions and recommendations.

### 2.7 Behavioral Momentum

```python
momentum[dim_i] = (D[dim_i, t] - D[dim_i, t-7]) / 7
# Positive = improving trend
# Captures rate of change, not just level
# Used to determine recommendation urgency and framing
```

### 2.8 Volatility Index

```python
volatility[dim_i] = std(D[dim_i, t-7:t]) / mean(D[dim_i, t-7:t])
# High volatility = unstable dimension = different recommendation than stable-low
# Stable-low needs encouragement; volatile needs stabilization first
```

---

## 3. Data Needed

### 3.1 Minimum Viable Data (Day 1)

| Data Type | Source | Frequency | Notes |
|---|---|---|---|
| 8D dimension scores | Check-in responses | Daily | Already in system |
| Mood/energy marker | Check-in (1 question) | Daily | Already in system |
| Dimension confidence | Merger output | Per-score | Already in system |
| Day of week | Calendar | Automatic | Captures weekly patterns |

### 3.2 Enhanced Data (Month 1+)

| Data Type | Source | Frequency | Notes |
|---|---|---|---|
| Sleep duration/quality | Wearable (Apple Health, Oura) | Daily | Maps primarily to PHY, secondarily PSY |
| Step count / activity | Wearable | Daily | Maps to PHY |
| Social interaction count | Calendar / messaging metadata | Daily | Maps to SOC (no content, just counts) |
| Work/activity pattern | Calendar | Daily | Maps to VOC |
| Financial stress indicator | Weekly check-in | Weekly | Maps to FIN (NOT daily — anxiety trigger) |
| Environmental quality | Location / weather API | Daily | Maps to ENV |

### 3.3 Rich Data (Month 3+)

| Data Type | Source | Frequency | Notes |
|---|---|---|---|
| Journal/note sentiment | NLP on journal entries | When written | Maps to PSY, SPI |
| Goal completion rate | Product engagement | Daily | Maps to VOC, INT |
| Heart rate variability | Wearable | Continuous | Maps to PHY, PSY stress indicator |
| Nutrition quality | Photo/input | Daily | Maps to PHY (already have nutrition engine) |

### 3.4 Data for Model Calibration

- **Population priors**: Aggregate anonymized cross-lag coefficients (needs 100+ users × 60 days minimum)
- **Expert calibration**: Literature-derived A matrix values (available immediately from research)
- **Personal calibration**: User's own transition patterns (viable after 30 days, robust after 90)

---

## 4. User-Facing Output Design

### 4.1 The Wellness Dashboard (Daily)

**Top level**: Regime indicator with trajectory arrow
- "You're STABLE and HOLDING STEADY" (green, →)
- "You're STABLE but DRIFTING" (yellow, ↘)
- "You're THRIVING" (bright green, ↑)

**Dimension radar**: 8-axis chart with:
- Current score (solid line)
- 7-day predicted trajectory (dashed line, fading confidence band)
- Baseline reference (gray ring)

**Key insight (1 sentence)**:
- "Your physical wellness has been rising for 5 days — your mood usually follows within 3-4 days."
- "Social dimension dropped for the 3rd day. This sometimes cascades to purpose and mood."

### 4.2 Predictive Alerts (Proactive, Not Reactive)

| Alert Type | Trigger | Framing |
|---|---|---|
| **Early drift** | 2+ dims declining 3+ days, regime still "Stable" | "A couple areas are dipping — here's a small thing that helps." |
| **Cascade warning** | High cascade_risk dimension begins declining | "When [PHY] drops, it tends to pull [PSY] with it. A short walk today could break that pattern." |
| **Opportunity window** | Momentum positive in targetable dimension | "You're building momentum in [INT]. This is a good week to start that learning goal." |
| **Regime transition** | P(transition to worse regime) > 30% | "Things have been harder lately. Would it help to scale back to just 2 focus areas?" |
| **Positive prediction** | Forecast shows improvement based on current trajectory | "If you keep this up, your mood dimension should improve by mid-week." |

### 4.3 Recommendation Engine Output

Recommendations are generated from three sources:

**Source 1 — ILS-driven**: "Focus on [highest ILS dimension] this week — it has the most positive ripple effect."
**Source 2 — Momentum-aligned**: "You're already building momentum in [dim] — here's how to sustain it."
**Source 3 — Volatility-aware**: "[Dim] has been up and down. Before pushing for growth, let's stabilize it first."

Each recommendation includes:
- **What** (specific action)
- **Why** (which dimensions it affects, based on their personal A matrix)
- **Expected effect** (predicted score change, with confidence)
- **Effort level** (low/medium/high — respects energy constraints)

### 4.4 Weekly Summary

- Regime time distribution (days in each state)
- Top positive mover / top negative mover
- Prediction accuracy (how did last week's forecast compare to reality?)
- ILS recommendation + outcome from previous week
- 2-3 personalized insights based on discovered interaction patterns

### 4.5 Tone and Safety Rules

- **No medical claims** — "this predicts wellness patterns" not "this diagnoses conditions"
- **No shame language** — never "you failed" or "you should have"
- **Uncertainty is honest** — show confidence bands, not false precision
- **Predictions can be wrong** — always frame as "based on patterns we've seen" not "this will happen"
- **Regime labels are internal** — users see "Building", "Holding Steady", "Navigating a Tough Patch", "Taking Care of Basics", never "Crisis" or "Declining"

---

## 5. Caution Areas

### 5.1 Cold Start Problem
- With <14 days of data, trajectory prediction is unreliable
- With <30 days, cross-lag coefficients are population estimates, not personalized
- **Mitigation**: Use population priors with wide confidence intervals; explicitly show "learning your patterns" state

### 5.2 Overfitting to Noise
- Daily wellness scores are noisy — mood, context, measurement error
- A VAR model fit to 30 days of noisy daily data will overfit
- **Mitigation**: Use Bayesian shrinkage toward population priors; require 60+ days before personalizing A matrix; regularize aggressively

### 5.3 Confirmation Bias in Recommendations
- If the model always recommends what worked before, it may miss what would work better
- **Mitigation**: Explore-exploit framework — 80% evidence-based recommendations, 20% exploratory suggestions with honest framing ("we're not sure if this will help, but it's worth trying")

### 5.4 Feedback Loops
- If a prediction causes anxiety ("you're predicted to decline"), it can cause the decline
- If a user optimizes for scores rather than genuine wellness, the measurement distorts the thing being measured (Goodhart's Law)
- **Mitigation**: Never show precise numeric predictions to users; frame predictions as patterns not certainties; optimize for user actions not score maximization

### 5.5 Cultural and Individual Variability
- The 8 dimensions are Western-originated; meaning and priority varies across cultures
- A user in financial stress may experience FIN→PSY coupling of 0.40 while a financially secure user may be near 0.0
- **Mitigation**: Personal calibration is not optional — it's the product; never assume population averages apply to individuals

### 5.6 Regime Label Sensitivity
- Calling a user's state "Declining" or "Crisis" is clinically adjacent language
- **Mitigation**: Use growth-oriented labels internally and user-facing; have escalation protocols for genuinely concerning patterns; never diagnose

### 5.7 Data Sparsity and Missingness
- Users skip check-ins, especially when struggling (the exact time data is most valuable)
- Missing-not-at-random data biases the model toward healthy periods
- **Mitigation**: Passive data (wearables, behavioral signals) continues even when check-ins stop; use missingness itself as a signal (3+ skipped check-ins = possible drift indicator); NEVER guilt users about missing data

### 5.8 Temporal Granularity Mismatch
- Some dimensions change daily (PSY, PHY), others weekly/monthly (FIN, ENV, SPI)
- A daily VAR treats them equally
- **Mitigation**: Use multi-resolution modeling — daily for fast-moving dims, weekly for slow-moving; or use mixed-frequency VAR approaches

### 5.9 Ethical Use of Predictive Power
- Predicting behavior change allows manipulation as easily as support
- **Mitigation**: Recommendations should always serve user-stated goals; never use predictions to increase engagement metrics at wellness cost; transparent about what data drives what prediction

### 5.10 The Coupling Matrix Gap
- As of 2026-06-01, the existing system's coupling_sum is a constant (6.775) across all scored days — the interaction terms are NOT producing differential effects despite the proprietary formula describing κ values of 0.68-0.85
- **Mitigation**: Before adding predictive modeling, the base coupling matrix must actually vary with dimension scores. The predictive layer amplifies whatever the base layer produces. A broken base layer = broken predictions.

---

## Implementation Priority (Pragmatic Roadmap)

### Phase 1 — Data Foundation (Weeks 1-2)
- Ensure coupling matrix produces differential effects (fix the constant coupling_sum bug)
- Add 7-day and 30-day EWMA trend columns to daily_scorecard
- Add volatility and momentum calculations to operational_layer.py

### Phase 2 — Population Priors (Weeks 3-4)
- Implement A matrix with literature-derived cross-lag coefficients
- Build trajectory forecast function (7-day forward simulation)
- Build cascade risk calculator
- Validate against the principal's historical data (backtesting)

### Phase 3 — Regime Detection (Weeks 5-6)
- Implement 5-regime HMM with emission functions
- Train initial transition matrix on historical data
- Build regime-aware recommendation selector

### Phase 4 — Personalization (Month 2-3)
- Bayesian A matrix personalization (shrink population priors toward user data)
- Per-user cascade pattern discovery
- Prediction accuracy feedback loop

### Phase 5 — User-Facing Output (Month 3-4)
- Predictive dashboard components
- Proactive alert system
- Recommendation engine with ILS + momentum + volatility inputs

---

## 6. PIML Implementation — Working Prototype (v0.1.0, 2026-06-09)

A Physics-Informed Neural ODE prototype was built and validated on synthetic data. This is no longer theoretical — it runs.

### Architecture
- **Framework:** PyTorch + torchdiffeq (Neural ODE via `odeint` with RK4 solver)
- **Physics-Informed ODE:** `dx/dt = f_physics(x, t) + f_neural(x, t)` where f_physics encodes known constraints and f_neural learns residuals
- **Unconstrained ODE:** Same architecture, no physics prior (baseline for comparison)

### Known Physics Encoded in the Model
1. **Mean-reversion:** α_d × (baseline_d − x_d) — first-order relaxation toward personal baseline
2. **Cross-dimensional coupling:** κ adjacency matrix (8×8, strongest edge PSY↔PHY at 0.82) with damping factor 0.30
3. **PSY↔PHY cascade constraint:** If either drops below 40, the other gets pulled down proportional to κ=0.82
4. **Boundedness:** Physics loss penalizes predictions outside [0, 100]
5. **Conservation-like constraint:** Total system energy (sum of states) should stay bounded

### Key Results (Synthetic Data, 5 Users × 90 Days)
- **Next-day prediction:** Physics-Informed MSE 10.94 vs Unconstrained 11.64 (+6% improvement)
- **30-day extrapolation:** Physics-Informed MSE 19.2 vs Unconstrained 81.5 (**4× better**)
- **Final day prediction:** Physics-Informed 15.9 vs Unconstrained 191.8 (**12× better**)
- Physics wins on PSY, PHY, ENV, FIN (dimensions with strongest known physiological coupling)
- Baseline wins on SOC, SPI, INT, VOC (dimensions with weaker mechanistic models — the gap the advisor fills)

### Files
- `references/piml-prototype-session.md` — session-specific build details and advisor questions
- Prototype code: `/<workspace>`
- Sleep algorithm (full ODEs): `/<workspace>`

### Advisor Handoff Pattern
The user prefers building finished deliverables for advisors to review rather than asking them to start from scratch. The prototype includes:
- Working code (`train.py` runs end-to-end)
- Dark-themed PDF advisor review document with specific mathematical questions
- Quantified comparison showing why physics constraints matter (the extrapolation divergence is the killer argument)

### Build Pattern (for future PIML prototypes)
1. Subagent delegation timed out on first attempt (600s, 16 API calls for a 6-file build)
2. Building directly in the main session succeeded faster and more reliably (aligns with `subagent-anti-timeout-patterns` Pattern 18)
3. NumPy 2.x incompatible with torch compiled against NumPy 1.x — fix: `pip install numpy==1.26.4`
4. The advisor review doc should include "what's known vs. hypothesized" split — it frames the collaboration clearly

---

## Release Identity
- `8D Predictive Behavior Model Design — support — v1.1.0 — 2026-06-09`
- Public role: research-backed design reference for extending the 8D system into trajectory prediction and regime detection
- Public promise: provide the theoretical and mathematical framework for predictive wellness modeling without exposing proprietary calibration

## Key Research References

1. SAMHSA Eight Dimensions of Wellness framework (2016) — theoretical foundation
2. Cross-lagged panel models for bidirectional health dimension effects (RI-CLPM literature)
3. Bayesian hierarchical VAR for patient trajectories (PMC6294362)
4. Dynamic factor models for longitudinal health trajectories (arXiv 2412.08873)
5. PMC systematic review of wellness model structures (International Journal of Wellbeing, 2024)
6. HMM with time-varying transition matrices for disease progression (Stan/brms literature)
7. Perceived Wellness Survey — psychometric validation of multidimensional wellness measurement
8. Goodhart's Law implications for health scoring systems (measurement theory)
