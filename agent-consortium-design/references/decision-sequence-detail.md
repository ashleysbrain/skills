# Decision Sequence Detail — 9-Phase Formula Ordering

## Core Principle

The 44 formulas do NOT all run at once. They apply at different PHASES of the
task lifecycle. The phase determines the formula. The agent never asks "which
formula should I use?" — it asks "what phase am I in?"

## The 9 Phases

### Phase 0: CLASSIFY (no math)
- What is this task? Who is it for? What format?
- Pure classification. No formulas.

### Phase 1: HARD GATES (rules only, no math)
- 8D check: does this idea harm humans in ANY dimension?
- DNA check: is this DS enough?
- If EITHER fails -> STOP. No further evaluation.
- Cost: near-zero. Prevents the most expensive failure (producing harmful content).

### Phase 2: PHILOSOPHY SELECTION (selection engine math)
- Score all candidate philosophies.
- Free energy ratio gate.
- Hold top 3 in superposition.
- Math: Score(P,T) weighted sum. F = COST/[Score*(1+INFO_GAIN)] ratio gate.

### Phase 3: AUDIENCE CALIBRATION (classification, no math)
- Schwartz awareness level (MANDATORY tag).
- Demand state mapping.
- JTBD (functional + emotional job).
- Output: content spec with all parameters.

### Phase 4: PRODUCTION (creative, no measurement math)
- Route to creative engines.
- Content gets MADE.
- No formulas — this is the creative process.

### Phase 5: QUALITY THRESHOLD (rule-based checks)
- Now content EXISTS. First measurement math begins.
- Anti-slop checklist (deterministic, instant).
- Brand coherence check.
- Awareness level match verification.
- If ANY fail -> return to Phase 4. Max 3 iterations.

### Phase 6: PREDICTIVE MODELING (before publishing)
- Estimate how content will perform.
- Bass diffusion: will this idea spread?
- K-factor: viral coefficient estimate.
- Prospect theory: loss frame vs gain frame effectiveness.
- Price elasticity: if pricing content.
- Math: Bass, K-factor, prospect theory, elasticity.

### Phase 7: IMMEDIATE MEASUREMENT (hours/days after publish)
- CTR = Clicks / Impressions
- Engagement Rate = interactions / impressions
- Dwell Time Score (attention quality)
- Math: instant engagement formulas.

### Phase 8: DELAYED MEASUREMENT (days/weeks)
- A/B test significance: p-value, power, sample size.
- Thompson sampling update: Beta posterior.
- Brand lift: (Exposed - Control) / Control.
- NPS, CSAT.
- ROMI = (Revenue * Margin - Spend) / Spend.
- Attribution: Shapley value, Markov removal effect.
- Incrementality: difference-in-differences.
- Math: statistical + causal formulas.

### Phase 9: LEARNING + STRATEGIC UPDATE
- Feed results back into the system.
- Burnet immune memory: what worked, what didn't.
- Update Thompson priors (Beta parameters).
- Update Bass parameters for future predictions.
- Update philosophy evidence scores.
- Update selection weights (+-0.05 max).
- Math: Bayesian update + parameter refinement.

## Periodic Strategic (not per-content)
- MMM (marketing mix modeling): quarterly.
- Portfolio optimization (Sharpe ratio for channels): quarterly.
- Real options (Black-Scholes for investment decisions): per major investment.
- Brand equity measurement (CBBE, Interbrand): annually.

## Physics Justification for This Order

### Free Energy Principle
Hard gates (Phase 1) cost almost nothing but prevent the most expensive failure.
Running them FIRST minimizes F = cost - T*info_gain.

### Superposition Principle
You cannot MEASURE content quality before content exists. Running Phase 8
formulas during Phase 2 is a category error.

### Adiabatic Principle
Each phase must COMPLETE before the next begins. No skipping. Jump from
philosophy to production without audience calibration = wrong content for
wrong audience = adiabatic violation (excites chaos).

### Critical Slowing Down
Phase 8 is where you detect critical slowing down. If ROMI trending down across
cycles, or variance increasing, the system is approaching a tipping point.
STOP pushing that channel and redesign.

## Decision Tree (what the agent executes)

```
RECEIVE TASK
  |
  Phase 0: Classify. Is this a valid task? -> sort by type
  Phase 1: 8D GATE. Any dimension < 0? -> REJECT
           DNA GATE. < 0.5? -> REJECT
  Phase 2: SELECTION. Score philosophies -> hold top 3
           Free energy gate -> skip any F >= 1.0
           No philosophies admitted? -> REJECT (task not viable)
  Phase 3: AUDIENCE. Tag awareness level (MANDATORY)
           Cannot determine? -> REJECT (insufficient info)
  Phase 4: PRODUCTION. Route through engines
           Engine DOWN? -> file pathology, halt or reroute
  Phase 5: QUALITY. Anti-slop fail? -> return to Phase 4
           Iteration >= 3? -> ESCALATE
  Phase 6: PREDICT (optional). K-factor < 0.5? -> flag low-virality
  Phase 7: PUBLISH. Route to distribution organs
  Phase 8: MEASURE (async). Collect data -> statistical analysis
           ROMI < 0? -> flag for strategy review
  Phase 9: LEARN (async). Update memory, priors, weights
           SYSTEM IS SMARTER FOR NEXT CYCLE
```
