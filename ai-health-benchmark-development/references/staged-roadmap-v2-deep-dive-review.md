# Staged Roadmap v2.0.0 — Deep-Dive Review Findings (2026-08-14)

Three reviewers (Popper adversarial, Kuramoto physics, Osler gap analysis) audited roadmap v1.0. All findings consolidated into `organism/AI-HEALTH-BENCHMARK-STAGED-ROADMAP.md` v2.0.0 (4 stages, 34 metrics). This file preserves the full reasoning.

## Popper — Adversarial Verdict

**Core finding: 2 of 17 thresholds theoretically derivable; donation strategy gave away the moat; n=1 validation via the OS.**

1. **Magic numbers.** lambda_2 > 0.1 is topology-dependent (Fiedler values scale with N and edge weights). r > 0.8 assumes synchronization is desirable — for specialist agents high r may be groupthink. S > 0.2 and C_emergence > 1.2 have no derivation or empirical base rate, and "whole > sum" is confounded by task selection. L_inject < 200ms measures the orchestrator shim, not the swap (inference floor ignored). tau_adapt < 7d conflates wall-clock with interaction frequency — must be event-count normalized. Derivable: eta < 1 (FJ stability condition — later replaced by SIR R_0 < 1 per Kuramoto) and lambda_max < 0 (later replaced by JSR < 1).

2. **AAIF lock-in.** A donated conformance suite is a public good, forkable; LF has 400M+ monthly SDK downloads of gravity. Real lock-in: (a) proprietary held-out swap-delta task sets, (b) longitudinal telemetry corpora (accumulated, not forkable), (c) the scoreboard/scoring substrate.

3. **the OS independence.** Stage 1/2 are protocol-level and survive the OS — that IS their credibility. But single-reference-implementation = n = 1 = unfalsifiable. Stage 3 as the OS-only reads as marketing. Fix: 3+ external systems in Stage 1 publication; Stage 3 as open portability spec.

4. **Cross-topology normalization.** The deepest technical hole: star-of-5 and ring-of-8 have different Fiedler values at identical "health." Fix: every topology-dependent metric reported as effect size vs degree-matched random-ensemble null, never raw.

## Kuramoto — Five Formula Corrections

1. **Weighted Kuramoto.** Textbook r e^{i psi} = (1/N) sum e^{i theta_i} assumes all-to-all unweighted coupling. Correct: r_w e^{i psi} = (1/sum K_i) sum K_i e^{i(theta_i - psi)}, K_i = weighted degree, computed on natural-frame drift residuals; or locked-cluster fraction rho = |{i: theta_dot_i ~ psi_dot}| / N. Report r_w + frequency dispersion of locked set. Signed/inhibitory interactions: Daido order parameters r_n (n=1,2,4) or pairwise C_ij = <cos(theta_i - theta_j)>.

2. **Transfer entropy.** Naive kNN TE gives spurious nonzero values on independent series at N < 10^3. Correct: Kraskov-style kNN with bias correction, N >= 10^4 for 3-variable lagged conditioning; Gaussian/linear CMI (closed form, zero sample bias) below that. Null: surrogate data (time-shuffled or twin), >= 1000 realizations, report z-score |z| > 3. Permutation on finite samples conflates bias with dependence.

3. **Cascade model.** Friedkin-Johnsen is belief convergence — contractive by construction, cannot express 17x error amplification. Correct: branching-process/SIR on weighted graph. R_0 = lambda_max(M)/gamma < 1 where M = next-generation matrix. Watts threshold model if severity thresholds matter. FJ deleted from cascade metric, retained as consensus-coordination metric.

4. **Emergence.** Shapley sums exactly to the whole (budget decomposition) — synergy invisible. Correct: PID/BROJA (Williams-Beer) — S = I(X1,X2 -> Y) - [unique1 + unique2 + redundant] > 0 for information emergence; v(N) - sum v(i) with bootstrap CI for task performance. Shapley is correct for attribution shares (a different Stage-1 root-cause metric).

5. **Switched-system stability.** Single Lyapunov exponent undefined for x(t+1) = A_{sigma(t)} x(t) with sigma in {A_base, A_swap}. Individual matrices can each be stable while the switched system diverges. Correct: joint spectral radius rho_hat = lim_{k} max ||A_{s1}...A_{sk}||^{1/k} < 1. Compute via max-norm/sum-of-squares bounds (Parrilo-Jadbabaie); common quadratic Lyapunov certificate V with A_i^T P A_i < rho^2 P. Average-dwell-time LMI fallback for rare swaps.

## Osler — Eight Missing Categories

Pathologist's one-liner: "an excellent cardiac and musculoskeletal workup on a patient who also needs an infectious-disease panel (security), a metabolic panel (economics), a functional-status assessment (human-in-loop), and — before any of it is believed — calibration of the lab equipment itself (Stage 0 validity)."

| Priority | Category | Stage | Key metrics |
|---|---|---|---|
| BLOCKER | Security/immunology | 2 (+1 in 1) | Injection propagation constant (adversarially-seeded SIR), trust-boundary permeability, malicious-block detection, privilege-escalation radius |
| BLOCKER | Economic metabolism | 1 | Cost-per-task vs best single model, block cost attribution, budget-flow conservation, marginal-block value |
| BLOCKER | Human-in-the-loop | 1-2 | Escalation precision/recall, ISBAR-style handoff quality, trust calibration, cognitive load (NASA-TLX) |
| HIGH | Failure recovery | 1 | Mesh MTTR, checkpoint/restart, degradation dose-response curve, blast-radius containment |
| HIGH | Longitudinal | 3 | Version-drift velocity d(metric)/dt, reconfiguration effect size, memory growth pathology, mesh health half-life |
| HIGH | Context hygiene | 1-3 | Context pollution coefficient, shared-memory integrity, grounding freshness at point of use, provenance-loss rate |
| MED | Governance/audit | 2 | Provenance chain completeness, accountability attribution vs seeded faults, tamper-evidence, consent propagation |
| META | Benchmark validity | 0 | Construct validity, inter-rater reliability, sensitivity/specificity, Goodhart resistance |

Note: FJ-to-injection connection — influence physics IS prompt-injection physics; the cascade machinery is 80% of the security metric already.

## Consolidation Outcome

Roadmap v1.0 (3 stages / 19 metrics) -> v2.0.0 (4 stages / 34 metrics). Stage 0 added. Every threshold now either theoretically derived, null-normalized, or Stage 0 pilot-calibrated. Donation strategy narrowed to spec-only. the OS decoupled.
