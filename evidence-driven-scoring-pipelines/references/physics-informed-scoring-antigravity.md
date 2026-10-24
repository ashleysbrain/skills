# Physics-Informed Scoring: Antigravity Model Pattern

Reference pattern for building physics-informed scoring pipelines where domain disruptors are modeled as repulsive force fields opposing a natural restorative "gravity."

## When to Use This Pattern

- Building a health/wellness scoring algorithm where external factors actively oppose the desired state
- The domain has a natural "attractor state" (restorative sleep, calm, focus) that disruptors push against
- User wants real physics concepts (not just metaphors) embedded in the scoring math
- The score needs to explain *why* it's low, not just *that* it's low

## Architecture

### 1. Define the Attractor Basin (Gravity)

Identify the restorative state and quantify its "basin depth" from measurable indicators:

```
B = f(quality_metrics)
```

Example (sleep): `B = 0.4 × SE + 0.35 × FI + 0.25 × sigmoid(TST)`

### 2. Identify Antigravity Sources

Each disruptor becomes an antigravity source with:
- **Magnitude** (Ᾱ): how strongly it opposes the attractor
- **Decay function** (f(t)): how its effect changes over time
- **Data source**: where to measure it (sensor, self-report, API)

Use real pharmacokinetic/physiological half-lives for decay functions:
- Caffeine: τ = 360 min (6-hr half-life), exponential decay
- Cortisol: ~3-hr decay, exponential
- Blue light: step function + exponential decay (melatonin suppression)
- Alcohol: negative during consumption, positive rebound 4-5 hrs later (delayed antigravity)
- Acoustic noise: impulse events (Dirac delta)

### 3. Compute the Antigravity Field

```
V_antigravity(t) = Σ_k Ᾱ_k × f_k(t)
```

### 4. Derive the Antigravity Index

```
AGI = V_antigravity / B_natural × 100
```

This normalizes the disruptor field against the individual's natural resilience.

### 5. Adjust the Core Score

```
Score_adjusted = Score_raw × (1 - AGI / denominator)
```

The denominator controls how much antigravity can reduce the score. In the sleep app: `CSI_adjusted = CSI × (1 - AGI/200)`, meaning maximum 50% reduction.

### 6. Coaching Integration

The antigravity model naturally produces explainable coaching output:
- List each source with its contribution percentage
- Identify the single largest contributor
- Recommend reducing that source specifically
- Show what the score *would have been* without antigravity

### 7. Escape Velocity (Chronic Cases)

For users stuck in a poor-state attractor, compute whether gentle interventions have enough "thrust":

```
v_escape = √(2 × G_poor × M_disruption / r_recovery)
```

If AGI is chronically >40, simple tips won't work. Escalate to higher-intensity intervention (CBT-I, clinical referral, etc.).

## Scoring Pipeline Integration

This pattern fits into the evidence-driven scoring pipeline as follows:

```
Raw evidence → Evidence interpretation (extract signals from data)
            → Core Score computation (attractor basin model)
            → Antigravity field computation (disruptor sources)
            → Score adjustment (AGI modifies core score)
            → Cascade propagation (8D coupling matrix)
            → Personal baseline delta
            → Final composite score
            → Presentation + coaching language
```

The antigravity field is computed **after** the core score and **before** cascade propagation, because antigravity effects should propagate through the dimension network.

## Key Design Decisions

1. **Decay functions must use real half-lives**, not arbitrary constants. This makes the model scientifically defensible.
2. **Magnitudes should be calibrated from literature** (e.g., caffeine reduces SE by X% in controlled studies), not guessed.
3. **The coaching output is the primary user-facing artifact**, not the raw AGI number. Users don't need to know "your AGI was 41" — they need "caffeine at 4 PM was 18% of the antigravity fighting your sleep."
4. **Low-AGI users get gentle nudges. High-AGI users get structured interventions.** Don't give CBT-I homework to someone whose only issue was one late coffee.
5. **The model must work without every source.** If a user doesn't log caffeine, the model runs without it. Missing data ≠ zero antigravity from that source.

## Source

Divinity Health Sleep App (2026-06-07). First implementation of the antigravity scoring pattern in the 8D Sleep Score Algorithm v1.1.0.
