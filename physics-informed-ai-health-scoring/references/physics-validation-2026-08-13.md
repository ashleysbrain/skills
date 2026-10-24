# Physics Validation: AI Health Dimensions v2

**Date:** 2026-08-13
**Validators:** the specialist engine (Bell Labs/MIT), the specialist engine (Moscow State), the specialist engine (Kyoto), the specialist engine
**Scope:** All 6+1 dimensions in `canonical_coupling_ai.py` and `AI-HEALTH-DIMENSIONS-V2.md`

## Bottom Line

Every dimension has the right physics framework but under-specified observables. None survive peer review as written. All are fixable in one revision. The frameworks are sound. The wiring is wrong.

## Dimension-by-Dimension Findings

### COG (Cognitive Integrity) — Major Revision

**CRITICAL FIX:** KL divergence is the wrong functional form. Any hallucination (zero ground-truth support) makes D_KL = infinity. The measure saturates and becomes useless for tracking DEGREE of degradation.

**Fix:** Use Jensen-Shannon DISTANCE (square root of JSD), not KL divergence or JSD itself. JS distance is bounded [0,1], symmetric, always finite, and is a TRUE METRIC (satisfies triangle inequality). This is essential for the composite score to be geometrically meaningful.

**Coupling ordering is backwards:** COG-KNOW should be STRONGER than COG-PIPE. KNOW failure is a BIASED PRIOR (systematic, unrecoverable from inside cognition). PIPE failure is ADDITIVE NOISE (detectable, correctable). Systematic error couples more tightly than stochastic noise. Recommend swap: COG-KNOW=0.30, COG-PIPE=0.28.

**Missing telemetry:**
- The verified-reality distribution Q itself (where does ground truth come from? retrieval? fact bank? fact-checking model?) — every COG measure depends on Q being defined
- Mutual information I(output; evidence) — the most pure cognitive health signal
- Output entropy H(P_model) from logprobs
- Hallucination propagation rate (fraction of hallucinations relied upon in next turn)

**Reframe:** "Low entropy = healthy" is too crude. Healthy cognition has low CONDITIONAL entropy H(output|evidence). Degradation is H(output|evidence) rising.

**Contradiction density** is NOT an output-entropy proxy. It measures coherence. Keep as secondary signal, rename as internal-consistency metric, add true output entropy as primary.

### PIPE (Pipeline Reliability) — Minor Revision

Little's law (L = lambda*W) gives a conservation relationship but NOT a diagnostic. What predicts instability is utilization rho = lambda/mu.

**Fix:** Compute rho from request rate (lambda) and service rate (mu = successful completions/time). Alert when rho > 0.8. The (1-rho)^{-1} divergence from Pollaczek-Khinchine (M/G/1) is the heavy-tail precursor.

**Missing telemetry:**
- Throughput lambda (requests/min) and service rate mu (successful completions/min) — rho is not currently computed
- Queue length L (pending/in-flight tool calls)
- Retry multiplier (attempts per successful task)
- Tail exponent of latency CDF (p95 alone hides the tail)

### RES (Resource Efficiency) — Major Revision

F = cost - T * info_gain is DIMENSIONALLY INVALID. T is undefined (no units, no telemetry, no operational definition). In real thermodynamics, Boltzmann's constant k_B bridges the gap between entropy (dimensionless) and energy (Joules). The AI version needs its own k_B-equivalent.

**Fix:** Define T explicitly with units (e.g., exploration temperature in $/bit or tokens/bit). Add a k_B-equivalent conversion constant for dimensional consistency. Track F over time, not just cost slope.

**Carnot efficiency** is purely metaphorical. Drop it or formalize hot/cold reservoir analogs (e.g., max-achievable accuracy vs random baseline).

**Missing telemetry:**
- T parameter (exploration temperature / cost tolerance) — measured how?
- info_gain (bits of learning retained and reused downstream)
- Quality-gated token split (useful vs wasted tokens)

### KNOW (Knowledge Currency) — Minor Revision

Radioactive decay is MEMORYLESS. Knowledge isn't. The testing effect / spacing effect shows retrieval SLOWS forgetting. Pure exp(-lambda*t) ignores retrieval reinforcement.

**Fix:** Hybrid model with source term: dN_i/dt = -lambda_i(t)*N_i + alpha_i*1[retrieved] + beta_i*1[verified]. Where lambda_i is domain-specific, retrieval slows decay, and verification resets N_i.

Single lambda ignores per-domain heterogeneity. Use lambda_i per fact or domain.

**Missing telemetry:** retrieval frequency per fact, per-domain lambda_i, source-of-truth divergence, verification events.

### ALIGN (Aligned Execution) — Major Revision

Landau potential framework is RIGHT. But V(x) is never operationally defined. No order parameter x. No measured barrier height. No enumerated competing wells. As written it is a metaphor, not a model.

**Fix:**
- x = behavior vector = KL divergence of output distribution from aligned baseline
- V(x) = -log p(aligned | x) (negative log-posterior of alignment)
- Barrier height = adversarial-escape threshold epsilon* (smallest perturbation that flips behavior out of mission well)
- Enumerate competing wells: adversarial goals, shortcut behaviors, persona drift

**Missing telemetry:** adversarial-escape threshold, landscape curvature at mission minimum, competing-well catalog.

### ADAPT (Adaptation Capacity) — Major Revision (FACTUAL ERROR IN CURRENT SKILL)

**CRITICAL:** The current skill and code claim "near a tipping point, volatility DROPS, not rises." This CONTRADICTS established critical slowing down theory (Scheffer et al. 2009, Dakos et al. 2012). The canonical early-warning signals near a bifurcation are RISING variance and RISING lag-1 autocorrelation (AR(1)). The code implements the WRONG direction.

**Fix:**
- Correct the volatility claim: rising AR(1) and rising variance = approaching tipping point
- Add lag-1 autocorrelation of each dimension score (sliding window >= 15 snapshots) as the CSD detector
- tau is not measurable from point estimates (recovery_time_after_failure is one raw point). Need continuous post-failure recovery trajectory X(t) to fit exponential. Minimum 7-10 perturbation events for fitted tau, or >= 20 events for single-point estimates.

### INTER (Interaction Coherence) — Major Revision

Kuramoto framework is correct. But order parameter r CANNOT be computed from the listed telemetry (handoff_rework_rate, schema_mismatch_count). These are rates and counts, not phase variables. You cannot compute a Fourier coefficient from a single scalar.

**Fix:** Define theta_j as output-embedding angular deviation from fleet centroid. Compute r from per-agent phase vectors. omega_j = per-agent task-cycle frequency. K = inter-agent communication bandwidth.

**Missing telemetry:** per-agent phase vectors theta_j(t), natural-frequency distribution {omega_j}, temporal lag at handoff points, cross-spectral coherence, critical-coupling verification (measured K vs theoretical Kc).

## Cross-Cutting Issues (All Dimensions)

1. **No falsifiability thresholds:** What measured value of r, lambda, or delta-V constitutes "healthy" vs "degraded"? No quantitative decision rules.
2. **No temporal validation:** Coupling "converges to truth" but no convergence proof, rate, or dataset.
3. **Dimension independence not established:** stale_fact_hallucination_rate (KNOW) and hallucination_detection_rate (COG) overlap. Must show mutual information between dimensions is low.
4. **Scale ambiguity:** All dimensions scored 1-10. But r is in [0,1], lambda is 1/time, V is energy/log-probability. The mapping from physical quantity to 1-10 is unspecified. Is a COG of 7 the same distance from failure as an ALIGN of 7?
5. **Composite arithmetic mean hides compensatory degradation:** Model improves at reasoning (COG up) while developing safety regression (ALIGN down). Arithmetic mean stays flat. Use geometric mean or floor operator.

## Composite Score Recommendations

- Use geometric mean or min() operator (prevents compensatory masking)
- Use JS distance as composite unit (triangle inequality required)
- Unify under MDL framework: health = description-length efficiency
- Each sub-score must be a calibrated likelihood ratio, not a raw heuristic
- Sensitivity analysis: if perturbing weights by +/-10% changes rankings, the composite is fragile

## The Unifying Physics (the specialist engine)

Minimum Description Length (MDL) is the single coherent theory that unifies all dimensions:

- KL divergence IS expected excess description length: D_KL(P||Q) = E_P[log(P/Q)]
- JS distance is its symmetric, bounded, metric form
- Mutual information is the rate
- Conditional entropy is residual randomness
- Health = description-length efficiency

Every information-theoretic drift metric is a facet of MDL. This gives a principled composite: sum of description-length excesses across probes.

## The Hallucination Metric (Most Original Contribution)

Using the chain rule of entropy: H(Y) = I(Y;C) + H(Y|C)

Where C is the grounding context:
- I(Y;C) = grounded information (output entropy explained by context)
- H(Y;C) = unaccounted information (output not traceable to source)

A drift where H(Y|C)/H(Y) rises over time is a principled, quantitative hallucination-growth signal. This is rigorously correct as a mathematical identity and genuinely publishable. "Unaccounted" upper-bounds "fabricated" (the model may introduce correct information not in C).
