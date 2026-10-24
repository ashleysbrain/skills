# GAS Scoring-to-Coaching Integration Pattern

Session-derived pattern for wiring a behavioral physics scoring algorithm (GAS v2.0 or similar) into a coaching engine with advisory panels.

## When to use

When the user asks to "integrate the scoring algorithm into the coaching engine," "apply the calculations," "wire the scores into the advisors," or wants the advisory panels to consume real algorithmic output instead of generic advice.

## Architecture: The Full Pipeline

```
User check-in / behavioral event
        ↓
Raw data capture (timestamps, counts, ratios)
        ↓
State vector x(t) construction (normalize to [0,1])
        ↓
Scoring algorithm runs (17-step pipeline for GAS v2.0)
        ↓
Score S(t) + diagnostics (regime, curvature, barriers, breakthrough prob)
        ↓
DB storage (daily score, per-goal decomposition, regime, susceptibility)
        ↓
Coaching decision tree (rules-first, no ML)
        ↓
Advisor panel review (principal + Marketing + Product)
        ↓
Compiled brief (AM tips, PM day-in-review)
        ↓
Delivered to user (Telegram via cron cascade)
```

## Baseline Establishment

**Day 0:** First behavioral snapshot forms initial state vector x₀. Geodesic baseline d_G(x₀, x*) computed. Coupling matrix κ initialized from population-level data.

**Days 1-14 (calibration window):** Scores run but labeled "calibrating." Not shown to advisors or user as final scores. EMA smoothing (α_s = 0.2) converges within ~5 data points. Regime classification needs 7+ days. Barrier diagnostics need 3+ distinct state observations.

**By day 14:** κ personalized from user's behavioral co-occurrence data. T_c (critical temperature) estimated from observed variance. All outputs reliable enough for advisor consumption.

**Key rule:** Zero human-rating inputs. Everything comes from timestamps, counts, ratios, or derived geometry.

## Scoring Cadence

| Cadence | When | What | Who Sees |
|---------|------|------|----------|
| Daily | 11:30 PM | Full scoring pipeline | DB only |
| Weekly | Sunday 2 AM | Deep score + κ refinement + T_c update + barrier analysis | Advisors |
| Monthly | 1st of month | Parameter audit + goal target review + sensitivity sweep | Algorithm team |

## Coaching Decision Tree (Rules-First)

1. **Classify regime** (Crisis → Declining → Drifting → Stable → Thriving)
2. **Select daily focus** (rank by: breakthrough probability × coupling strength × current gap)
3. **Generate action** (barrier-breaking vs. push-through vs. micro-step vs. lock-in)
4. **Calibrate tone** (susceptibility χ determines urgency language)
5. **Format for delivery** (3-5 bullets AM, 3-4 bullets PM)

### Regime playbook

| Regime | Strategy | Tone |
|--------|----------|------|
| Thriving | Maintain + expand. Don't over-coach. | Brief. "Keep going." |
| Stable | Find unlock via curvature leverage point. | "You've plateaued. Here's the unlock." |
| Drifting | Build coherence via strongest coupled goal pair. Use transport plan. | "Focus on [pair]. Effort exists, just needs direction." |
| Declining | Arrest decline on steepest dψ/dt. Flag if susceptibility is high. | Direct. Name what's happening. |
| Crisis | One dimension only. Skip breakthrough analysis. | Supportive, not ambitious. |

## What Advisors See (interpreted, not raw math)

**Daily dashboard:**
- Overall S(t) with 7-day trend arrow
- Regime label (not raw ψ)
- Top 2 breakthrough candidates with probabilities in plain language
- Curvature leverage point ("small push on X creates cascade")
- Transport plan summary ("redirect effort from Y to Z")

**Weekly deep:**
- Per-goal progress trajectories
- Barrier analysis (which goals are stuck, how stuck)
- Susceptibility trend (intervention leverage rising or falling)
- Coupling map (which goals pull each other)

**Advisors never see:** Raw metric tensors, Ricci scalar values, Sinkhorn convergence, Christoffel symbols. Everything gets translated to plain language before reaching the advisor prompt.

## Cron Prompt Wiring

Each cron job's prompt must:
1. **Explicitly instruct the agent to read the scoring integration spec** at the canonical path
2. **Check for scoring data** in cron output directories
3. **Apply the coaching decision tree** to translate scores into advisor actions
4. **Never surface raw math** to the user

Example prompt fragment for principal AM:
```
## MANDATORY: Load GAS Scoring Data
Read the integration spec, check for today's scores in cron output.
Apply the coaching decision tree:
1. Classify regime → determines tone and strategy
2. Select daily focus from breakthrough probability × coupling × gap
3. Generate specific action (not "work on sleep" but "set a consistent bedtime tonight")
4. Calibrate tone to susceptibility
5. Format as 5-8 plain-language bullets
```

## DB Schema

```sql
-- Daily scores
CREATE TABLE daily_scores (
  date TEXT PRIMARY KEY,
  S_t REAL,              -- Overall score [0,1]
  regime TEXT,            -- Thriving/Stable/Drifting/Declining/Crisis
  psi REAL,               -- Order parameter
  dpsi_dt REAL,           -- Coherence trend
  chi REAL,               -- Susceptibility
  R_scalar REAL,          -- Ricci scalar
  e_max TEXT,             -- Max curvature direction
  phase TEXT              -- calibration/active
);

-- Per-goal scores
CREATE TABLE goal_scores (
  date TEXT,
  goal_id TEXT,           -- G1-G8
  phi REAL,               -- Geodesic progress [0,1]
  k_escape REAL,          -- Escape rate (1/day)
  P_escape_5d REAL,       -- Breakthrough probability in 5 days
  V_barrier REAL,         -- Barrier height
  PRIMARY KEY (date, goal_id)
);
```

## Edge Cases

- **User misses 7+ days:** Scores decay per ADHD model. Warm-start from last known state on return. No baseline reset. "Welcome back, your progress is still here."
- **Regime transition mid-day:** Midday cron catches it. Only fires if regime changes by more than one level.
- **All breakthrough probabilities near zero:** Pick the dimension with lowest barrier height. One thing only. "Everything is hard right now. [Dimension] has the smallest wall."
- **High ψ but low S(t):** Coherent effort but wrong direction or stale targets. Flag for weekly deep review.

## Canonical files

- Integration spec: `hydra-os/docs/your-org/coaching-engine/GAS-COACHING-INTEGRATION.md`
- GAS algorithm: `divinity-health/sleep-app/agents/GOAL-ATTAINMENT-SCORING-ALGORITHM.md`
- Behavioral physics engine: `hydra-os/docs/your-org-behavioral-physics-engine.md`
- Obsidian lab: `Divinity Science/Behavioral Physics Lab/` in vault
