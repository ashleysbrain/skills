# AI Health Dimension Physics Validation (in progress, 2026-08-13)

## Session Context
Three physics specialists dispatched to validate each dimension's physics:
- the specialist engine (Bell Labs/MIT) — COG dimension (information theory)
- the specialist engine (Moscow State) — PIPE + ADAPT dimensions (transport phenomena + relaxation dynamics)
- the specialist engine (Kyoto) — INTER + KNOW + ALIGN dimensions (synchronization + decay + potential landscape)

## the specialist engine (COG - Information Theory)

### Validated approaches:
- KL divergence is the workhorse for drift detection. Standard, well-founded.
- JS DISTANCE (not divergence) is the correct bounded object for composite scoring. Endres & Schilling (2003) proved it satisfies triangle inequality.
- Hallucination decomposition via chain rule: `H(Y) = I(Y;C) + H(Y|C)` is rigorously correct as an identity.

### Warnings:
- KL divergence direction matters. Forward KL (P_baseline || P_current) is the defensible default.
- KL is unbounded and asymmetric. Must use JS distance for composite.
- Support mismatch: if P_current assigns near-zero mass where P_baseline had mass, KL explodes. Need epsilon-flooring.
- Entropy alone is necessary but NOT sufficient. A confidently-wrong model has LOW entropy.

### Unifying theory: Minimum Description Length (MDL)
- Health = description-length efficiency
- KL divergence IS expected excess description length
- JS distance, MI, conditional entropy all have MDL interpretations
- Lead the paper with this

## the specialist engine (PIPE + ADAPT)

### Architecture design:
- 600 frozen tasks across 7 strata, k=5 sampling per task
- 4 parallel detectors: CUSUM, Bayesian changepoint, embedding drift, z-test
- Composite H score on [0,100] with empirical baseline quantiles
- Cost: ~$5/day/endpoint

### CUSUM validation:
- Legitimate, well-established (Page, 1954)
- Must segment by changepoint FIRST, then CUSUM within each segment
- 600 tasks need FDR correction (Benjamini-Hochberg)

### Non-determinism handling:
- temp=0 is NOT deterministic (batching, quantization, routing variance)
- k=5 sampling converts each task from binary to distribution
- Task flipping 3/5 -> 1/5 overnight is signal; 5/5 -> 4/5 is not

## the specialist engine Review (Existing Code)

### 12 fatal flaws in existing TWC scoring (HUMAN 8D system, NOT AI system):
1. TWC engine crashes on execution (KeyError: 'PSY')
2. Peer assessment layer (30% of formula) doesn't exist
3. Cascade sim result reverses with proper control
4. Isomorphism score gameable by keyword stuffing
5. Health endpoints return hardcoded "status: ok"
6. MI framework has 3 data points, needs 50+
7. EFFICIENCY_CAP not applied in AI-mode path
8. C_r gives perfect score to dependency-free nodes
9. No drift detection code in fleet
10. "Williams (2026)" = self-citation
11. Dimensions measure infrastructure labeled as wellness
12. Coupling normalization is ad hoc

### 3 fatal flaws in NEW concept (must fix before launch):
1. Judge model without kappa validation
2. Arithmetic-mean composite hides compensatory degradation
3. Frozen test suite contamination

## the specialist engine Validation (existing drift code)

### 3 critical issues in existing drift detection:
1. No multiple comparisons correction (expects 10.9 false flags per measurement)
2. Threshold has no statistical basis (36% false positive rate)
3. Biased variance estimator (33% underestimate, population variance /N instead of sample /(N-1))

### 3 high issues:
1. critical_slowing_metric() is mislabeled (computes recovery-time ratio, not variance ratio)
2. Insufficient sample size (n=4 required, need n>=20)
3. Endpoint slope uses only 2 of 8 data points

## Per-Dimension Validation Results (ALL COMPLETE 2026-08-13)

### COG (Cognitive Integrity) — the specialist engine verdict: MAJOR REVISION
- KL divergence infinite on any hallucination (zero ground-truth support). Use JS distance instead.
- Coupling priors backwards: COG-KNOW should be stronger (0.30) than COG-PIPE (0.28). Biased prior is unrecoverable from inside cognition; additive noise is detectable/correctable.
- Contradiction density is a weak entropy proxy. Need true output entropy H(P_model) from API logprobs.
- MISSING telemetry: verified-reality distribution Q (where does ground truth come from?), I(output;evidence), output entropy, hallucination propagation rate.
- "Low entropy = healthy" is too crude. Correct: low CONDITIONAL entropy H(output|evidence).
- context_coherence_score is undefined — needs explicit formula.

### PIPE (Pipeline Reliability) — the specialist engine verdict: MINOR REVISION
- Little's law gives relationship but not diagnostic. Must compute utilization rho = lambda/mu.
- Alert when rho > 0.8 (M/G/1 Pollaczek-Khinchine divergence).
- MISSING telemetry: throughput lambda, service rate mu, queue length L, retry multiplier, tail exponent (p95 alone hides the tail).

### RES (Resource Efficiency) — the specialist engine verdict: MAJOR REVISION
- F = cost - T*info_gain is dimensionally invalid. T never defined, no units, no k_B-equivalent conversion constant.
- Carnot efficiency is purely metaphorical — no hot/cold reservoir analogs. Drop or formalize.
- MISSING telemetry: T parameter (with units), info_gain itself (entirely absent), quality-gated token split, F trajectory, marginal efficiency.

### KNOW (Knowledge Currency) — the specialist engine verdict: MINOR REVISION
- Radioactive decay is memoryless. Knowledge isn't — retrieval reinforces facts (spacing effect).
- Single lambda ignores per-domain heterogeneity. Need heterogeneous lambda_i.
- MISSING telemetry: retrieval frequency per fact, per-domain lambda_i, source-of-truth divergence, verification events, confidence calibration.

### ALIGN (Aligned Execution) — the specialist engine verdict: MAJOR REVISION
- Landau framework is correct but V(x) never operationally defined. No order parameter. No measured barrier. No competing wells enumerated.
- Fix: x = output-distribution KL from aligned baseline. Barrier = adversarial-escape threshold (smallest perturbation that flips behavior). Enumerate competing minima.
- MISSING telemetry: adversarial-escape threshold epsilon*, landscape curvature, competing-well catalog.

### ADAPT (Adaptation Capacity) — the specialist engine verdict: MAJOR REVISION
- CORRECTED: volatility "low = canary" claim contradicts CSD theory. Established signal: rising AR(1) and rising variance (Scheffer 2009, Dakos 2012). Code implements wrong direction.
- tau not measurable from point estimates (recovery_time_after_failure is one raw point, not a curve). Need continuous post-failure recovery trajectory X(t).
- Minimum 7-10 perturbation events for fitted tau; >=20 for single-point estimates.
- MISSING telemetry: continuous recovery trajectory, lag-1 autocorrelation (sliding window >=15), perturbation magnitude tagging, allostatic load accumulator, exploration breadth.

### INTER (Interaction Coherence) — the specialist engine verdict: MAJOR REVISION (reject as written, accept with fix)
- Order parameter r CANNOT be computed from listed telemetry. Rates and counts are not phase variables.
- Fix: define theta_j as output-embedding angular deviation from fleet centroid. omega_j = per-agent task-cycle frequency. K = inter-agent communication bandwidth.
- MISSING telemetry: per-agent phase vectors theta_j(t), natural-frequency distribution, temporal lag at handoff, cross-spectral coherence, critical-coupling verification.

### COMPOSITE FORMULA — the specialist engine verdict: SURPRISINGLY GROUNDED
- TWC = 0.5*linear + 0.5*coupling_norm uses geometric-mean coupling. Disguised tight-binding Hamiltonian: coupling_norm = psi^T K psi / S where psi_i = sqrt(phi_i).
- Curvature test: geometric-mean form produces genuine restoring basin (curvature -1.58). Naive product form gives 0.00 (no basin). The code's choice is physically superior.
- Quantum-inspired scoring: 80% decorative. Only entanglement entropy has real value. Drop qubit encoding, Bloch sphere, quantum gates for benchmark purposes.

### CROSS-CUTTING ISSUES (all dimensions)
1. No falsifiability thresholds (what value = healthy vs degraded?)
2. No temporal validation (coupling converges to truth, but no proof/rate/dataset)
3. Dimension independence not established (KNOW stale_fact_hallucination_rate and COG hallucination_detection_rate overlap)
4. Scale ambiguity (all 1-10 but r is 0-1, lambda is 1/time, V is energy — mapping unspecified)
