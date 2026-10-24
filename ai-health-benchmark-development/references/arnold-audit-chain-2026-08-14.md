# Arnold Audit Chain — Full Findings, 2026-08-14

Session-specific detail for the three-round the specialist engine audit chain (+ Lyapunov stability validation) that took `organism/AI-HEALTH-BENCHMARK-STAGED-ROADMAP.md` from v2.0.0 to v2.3.0 SHIP-READY. The SKILL.md carries the binding rules; this file carries the full reasoning.

## Round 1 — Information-Theoretic Metrics (Arnold)

### PID/BROJA — DECORATIVE as primary
PID has no canonical decomposition: Williams-Beer's lattice is one of >=5 competing definitions (Bertschinger-BROJA, Griffith-Koch, Ince, Makarenko). A benchmark that hard-codes one lattice into a threshold hard-codes a contested axiom. BROJA's convex program can have multiple minimizers; synergy value not unique in ill-conditioned cases. **Fix:** supra-additivity Delta = v(N) - sum v(i) with bootstrap CI is primary (lattice-free, estimator-trivial). PID demoted to post-hoc exploratory on discrete variables, N large, no thresholds.

### Transfer Entropy — the OR was the error
Linear-Gaussian CMI is zero-bias only because it is a projection: it measures dependence in the best Gaussian approximation. For LLM agents (discrete tokens, saturating couplings, thresholded escalation) the Gaussian projection can be near-zero while true dependence is large. It is a lower bound with unbounded pessimism, not a fallback. **Fix — AND-escalation:**
1. Gaussian CMI always reported (closed-form lower bound)
2. Kraskov kNN TE (Frenzel-Pompe/Montalto family) with time-shift surrogates, N >= 10^4 (claim-bearing)
3. Claim stands ONLY if both agree in sign AND z >= 3. Disagreement = the finding (nonlinear coupling)
Plus Ragwitz criterion for max-lag (kNN bias grows with embedding dimension).

### Context Pollution — circular as specified
"T(i->j) of garbage" presupposes a garbage partition; whatever classifier defines it becomes the metric (measuring the classifier, not the mesh). **Fix — mediated causal effect:** CPC(i->j) = I(A_i; E_j) - I(R_i; E_j), where R_i = task-relevant subvector defined by the task spec EXTERNALLY (breaks circularity). Interventional anchor: CPC_do = P(E_j | do(A_i := garbage-injected)) - baseline, via ablation harness. Observational and interventional must concur or the observational number is confounded and dies.

### Coupling Entropy H(J) — category error
Fisher information is a functional of a parametric likelihood family p(x|theta). J is a parameter, not a distribution; no likelihood on the table. The "decreasing over installs" monotonicity claim has no derivation in either object (decreasing coupling entropy compatible with rigidity AND with death). **Fix:** excess entropy / predictive information E = I(past; future) of the joint mesh process (Bialek-Nemenman-Tishby). Descriptor alongside: spectral entropy of J (Shannon over normalized eigenvalues), labeled descriptor not "Fisher information."

### The Unifier — NO
Mesh health is irreducibly multi-objective; any scalar trade-off embeds a preference ordering = values choice, not physics. Candidate once Stage 0 defines estimators: eta_mesh = E / (H_rate * C). Demoted to appendix footnote (round 3): dimensionally asserted, no operational estimators, MDL-reduction claim lacks derivation.

## Lyapunov Round — Stability/Control Machinery

### JSR certificate — DECORATIVE as written
Common quadratic Lyapunov existence is sufficient-not-necessary (textbook counterexamples: stable matrix pairs with no common P). Binary certificate gate false-negatives healthy swap families. Exact JSR undecidable in general (Blondel-Tsitsiklis). **Fix:** report interval [rho_lower, rho_upper] — lower from enumerated products, upper from SOS hierarchy degree d. Three states: rho_upper<1 contained / rho_lower>1 unstable / gap = INCONCLUSIVE.

### Regime split — tool assignment was inverted
JSR is worst-case over arbitrarily FAST switching. Planned block swaps: week timescales, tens of switches, mode time constants seconds-minutes -> per-mode exponential stability + average-dwell-time (Hespanka-Morse) margin is PRIMARY and near-trivially satisfied. JSR earns its keep only for failover flapping, retry storms, hot-swap in request path.

### Queueing — M/G/1 fails twice
Pollaczek-Khinchine assumes Poisson arrivals + finite service variance. LLM latency heavy-tailed: unbounded sigma^2 -> infinite mean wait (formula returns garbage), rho converges slowly (variance<0.05 threshold flunked or gamed by truncation). Agent streams bursty/correlated: one user turn spawns N subagent calls. **Fix:** M^X/G/1 (batch) or MMPP arrivals, truncated-Pareto service fit, report p99 sojourn/wait quantiles not means. rho_l itself survives (assumption-light).

### Kuramoto r_w — unmeasurable until omega_i defined
LLM agents are event-driven, not autonomous oscillators; phase exists only relative to an imposed cycle (cron cadence, scheduled pipeline). **Fix:** scope r_w to meshes with genuine endogenous cycle; elsewhere event-based coordination (Hawkes reciprocity, point-process coherence).

### SIR R_0 — sound condition, unidentifiable instrument
gamma (error catch rate) requires detection timestamps; M requires propagation edges. Outcome-only branching inference ill-posed (Wallinga-Lipsitch needs generation-interval distribution = tracing). **Fix:** mandatory fault seeding — inject marked errors, log block-to-block propagation, M and gamma directly estimable. Without seeding R_0 is a fitted story.

### Stage 1 consistency verdict
Queueing + synchronization + cascade formally commensurable (all distance-to-instability margins: 1-rho, 1-R_0, incoherence margin) but NOT epistemically commensurable as instrumented (queueing observable by default; Kuramoto lacks phase; SIR lacks infection data). Fused index honest IFF phase defined AND cascades seeded; otherwise separate panels. "A fused index of one measured quantity plus two decorative ones is false precision with a physics veneer."

## Round 2 — Stage 0 Methodology + Stage 3 + Statistics + Telemetry

### Stage 0's five fatal omissions (in its OWN methodology)
1. Power: n=3 systems = 1 degree of freedom = anecdote. Rank-based construct validity needs n >= 20-30 for d=0.5 at 80% power.
2. Calibration-on-evaluation circularity: thresholds calibrated on same systems that produce validation numbers = in-sample overfitting. Held-out split required.
3. Test-retest reliability absent: same system, same workload, two runs -> metric ICC. Cheaper and more basic than cross-harness inter-rater; run first.
4. MTMM absent: 34x34 convergent/discriminant matrix. Containment-family metrics must converge; containment-vs-cost must discriminate. Detects double-counting. (Round 3 caveat: 34-var structure at n=30 under-determined; reduce to ~5 confirmatory families or pool longitudinal.)
5. Reference-outcome problem: "externally-defined success" — by whom? Pre-register (e.g., Sev-1 incident in next 30 days, ticket-level) before seeing correlations.

### Stage 3 casualty list
- R_co [0.7,1.3] band: "a magic number in a lab coat." Borkar conditions are assumptions about the user's proprietary adaptation process. Demote to qualitative regime labels (mesh-faster / user-faster / comparable).
- I_leak < 0.1 nats: bounds are attacker-relative. Declare attacker class (threshold MIA with shadow models), report inference advantage at fixed FPR, state DP epsilon if mechanism exists.
- Delta_theta > 0.3: parameterization-dependent (geometry-unidentifiable). Pin to KL between behavior distributions on probe tasks.
- tau_adapt: user optimum unobservable. Redefine as regret vs personalized oracle on probe set, event-count normalized.
- Half-life: needs 6+ months telemetry that doesn't exist. Stage 4 metric wearing a Stage 3 badge.
- Survivors: memory pathology (dose-response honest), trust calibration (conceptually; imports IRB/human-subjects costs).

### FDR meta-gap
34 metrics x systems x longitudinal slices, uncorrected alpha=0.05: ~1.7 expected false positives under complete global null; with surrogate tests and per-system slicing, effective test count in the hundreds -> ~10+ spurious findings per report. Fix: (a) pre-register ~5 primary confirmatory metrics, rest exploratory; (b) BH-FDR within metric families, Holm family-wise across panels; (c) published thresholds require q-values + held-out replication.

### Minimum telemetry manifest (7 items)
1. Block-level event log (t, block_id, version, I/O digests, tokens, latency) — partial via OTel GenAI
2. Directed interaction graph (caller->callee + escalations) — partial via A2A/MCP traces
3. Fault-seeding hooks — NO major platform exposes
4. Swap harness API — none
5. Per-block cost attribution — partial (FinOps + OTel)
6. Cadence log (scoped Kuramoto) — cron systems only
7. User-model read access (Stage 3) — near zero
Coverage: ~25-35% of platforms satisfy 1-2+5 (Stage 1 minimum); <5% full. The manifest is a spec contribution; absence of items 3-4 IS the Stage 2 opening (conformance suite defines these hooks).

### Structural proposal — prospective predictive registry
Metric snapshot at time T pre-registers prediction of incident/outcome in [T, T+Delta], scored by Brier skill vs base rate, public, time-stamped. Contemporaneous correlation is circular and Goodhart-fragile; prediction under time separation is the only validity test surviving both. Converts benchmark to forecasting system; track record unfakeable.

## Round 3 — Verification Pass

Checklist: Stage 0 PASS (all 7 items, line evidence). Stage 3 casualties PASS. Stage 4 PASS. Telemetry manifest PASS. Consistency sweep: 2 FAILS — LADDER LOGIC still said "co-adaptation validates" (stale after R_co demotion; a label cannot validate); ASSET INTEGRATION still advertised Fisher<->H(J) and EMA<->tau_adapt (killed concepts). Borderline: FJ-to-injection phrasing on a deleted framework. Minor: composition gain ">1.2" and modularity ">0.3" raw magic numbers contradicting threshold discipline -> labeled PLACEHOLDER.

Three weakest remaining claims: (1) market stats uncited -> flagged vendor-reported with named sources; (2) MTMM under-determined at n=30 -> open problem, reduce to 5 families; (3) unifier dimensionally asserted -> demoted to footnote.

Verdict: SHIP-READY CONDITIONALLY after one 30-minute consistency patch. Patch applied; mechanical grep confirmed zero stale references. Roadmap final: v2.3.0 (17.8KB, 4+1 stages).

## Timing data (brevity caps)
Open-ended audits: 840-900s, timeout failures (3x). Word-capped audits (700-900 words): 44-66s completions. Always cap.
