# Coupling Matrix V2 — Higher-Order Tensor + Situational Gating

**Created:** 2026-06-28 by hermes (physics-PM mode)
**Design doc:** `/<workspace>`
**Status:** Design locked, awaiting sibling-agent implementation handoff

## The Problem

The canonical 28-pair coupling matrix (rank-2, all-positive, static) cannot represent:
1. **Compound effects** — 3+ dimensions jointly impacting each other (rank-3+ interactions)
2. **Antagonistic coupling** — all 28 pairs are positive; real wellness dimensions can be antagonistic at extremes
3. **Situational variation** — coupling strength should change based on context (sleep debt, acute stress, illness)

The audit (REVIEW-2 §4.4) flagged "No Antagonistic Coupling." Lived experience confirms all three gaps.

## The Solution Architecture

### Hamiltonian expansion (rank-2 → rank-3 + situational gating)

```
H(s) = Σ_i h_i(s)·D_i                    [rank-1, external field — situational]
     + Σ_{i<j}   κ_ij(s)·D_i·D_j         [rank-2, pairs — current 28 matrix]
     + Σ_{i<j<k} κ_ijk(s)·D_i·D_j·D_k   [rank-3, triples — NEW]
```

Every coefficient is now a function of situation vector `s`.

### Tensor counting (why not all triples?)

| Rank | Count | Cumulative |
|------|-------|------------|
| 1 (linear) | 8 | 8 |
| 2 (pairs) | 28 | 36 |
| 3 (triples) | 56 | 92 |
| 4 (quads) | 70 | 162 |
| 5-8 | 93 | 255 |

Full 255-parameter expansion is physically forbidden: curse of dimensionality, each rank needs ~10x more data. **Physics mandate: SPARSE higher-order terms only, gated by free energy.**

### Free-energy gate (which terms to include)

```
F = cost - T·info_gain
  cost = n_params · log(N_samples)
  info_gain = Δlog-likelihood on held-out data
F > 0 → SKIP    F < 0 → ADD
```

Most of the 56 triples correctly fail this gate and stay at zero.

### Situational gating (context-dependent weights)

Situation vector `s` (7 dimensions, separate from the 8 wellness scores):
- sleep_debt_7d, acute_stressor, circadian_misalignment, social_isolation, financial_pressure, illness_load, life_transition

Each coupling becomes a gated function:
```
κ_ij(s) = κ_ij^base · σ(w_ij · s + b_ij)
```
At s=0 (neutral), behavior is identical to today. The gate learns which situations amplify or invert each pair.

## Stage 0 — BLOCKER (wire Layer 1 before V2)

**Verified 2026-06-28:** `coupling_sum=6.775` is a dead constant stored across every row regardless of actual dimension scores. The live user-health path (`score_from_evidence.py` → `calculator.compute_twc`) does NOT compute coupling from scores. A fixed `compute_twc` exists in `fleet_twc_engine.py:360` but is only used for fleet scoring.

**Fix:** Replace dead constant with `canonical_coupling.coupling_term_normalized(scores)` — the function already exists. This is the prerequisite before V2 stages begin.

## Adiabatic Staging (do NOT skip stages)

- **Stage A:** 10 sparse triples (8 synergistic, 2 antagonistic), no gating yet. Pure addition.
- **Stage B:** Situational gating on existing 28 pairs. w_ij initialized to zero → launch behavior identical to today.
- **Stage C:** Triples + gating combined. Target end state.

Each stage must beat the prior on held-out before the next begins.

## Locked Decisions (physics-PM best judgment)

- **Situation vector:** 7 dimensions (locked)
- **Triple seeds:** 10 triples including 2 antagonistic (resolves the all-positive problem)
- **Asymmetric κ:** permitted in gated form (learned, not prior)
- **Evidence grades:** A/B/C/D tiers for triples (stricter than pairs; D = data-only, must pass F < -0.5)

## Canonical Coupling Source-of-Truth

The 4 spec heuristics (0.85/0.78/0.72/0.68) are REJECTED. The DB `interaction_matrix` values (0.05-0.35 scale, 28 pairs) are CANONICAL per `organism/canonical_coupling.py` VERITAS lock. The V2 model imports the canonical 28-pair matrix as its rank-2 prior (Layer 1 ground state) — no rip-out.

## Subagent Verification Trust Model (learned 2026-06-28)

When verifying audit claims via subagent delegation:
- Subagent self-reports are NOT verified facts — re-run critical queries yourself
- For database output: the subagent transcribes accurately but may mis-interpret (e.g., flagging correct DB values as "discrepancies" because it didn't know the rejection history)
- For test execution: mechanical execution is trustworthy (the subagent's role matches its capability)
- Correct pattern: dispatch leaf subagents for mechanical work, then independently verify the interpretation layer
