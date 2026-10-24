# Coupling Matrix Higher-Order Tensor Extension

Worked example of extending an existing physics-based scoring system. Parallel
to `gas-v2-extension-pattern.md`. Demonstrates the rank-2 → rank-3 tensor
evolution with situational gating, free-energy gating, and adiabatic staging.

## The existing system

The 8D wellness coupling matrix is a rank-2 (pairwise) interaction tensor:

```
TWC = Σ w_i · D_i  +  Σ_{i<j} κ_ij · √((D_i/10)(D_j/10)) · 10
```

- 28 pairs = C(8,2), all-positive, symmetric, static.
- Equivalent to Ising interaction energy: `H_Ising = -Σ_ij J_ij · s_i · s_j`.
- Canonical source: `organism/canonical_coupling.py` (VERITAS-locked, evidence-graded, schema-capped at |κ| ≤ 0.5).

## The limitation the user identified

The rank-2 matrix assumes every interaction is pairwise, time-invariant, and
synergy-only. Real life has compound effects (3+ dimensions jointly impacting
each other) and situation-dependent coupling strengths. The matrix cannot
represent these.

## The extension (passes the 5-check criteria)

### Check 1 — Variable sharing: PASS
The extension uses the same 8 dimension scores D_i as inputs. The situation
vector s is an additional external-field input, not a replacement.

### Check 2 — Self-consistency: PASS
The higher-order terms are the natural Taylor expansion of the same Ising
Hamiltonian. Rank-3 triples `κ_ijk · D_i·D_j·D_k` are the 3-spin interaction
terms that the Ising model already supports theoretically.

### Check 3 — Zero human-rating preservation: PASS
All coefficients are computed from mutual information (data) or evidence-graded
priors (DB). The situation vector components are physically measurable (sleep
debt hours, binary stressor flags, etc.), not subjective ratings.

### Check 4 — Real calculations: PASS
Each term produces a number. The free-energy gate `F = cost − T·info_gain`
produces a go/skip verdict per candidate term.

### Check 5 — Layer extension, not addition: PASS
The 28-pair matrix becomes Layer 1 (ground state). Triples are Layer 2
(corrections on top). Situational gating is Layer 3 (modulation). No rip-out.

## The three-layer Hamiltonian

```
H(s) = Σ_i h_i(s)·D_i                              [rank-1, external field]
     + Σ_{i<j}   κ_ij(s)·D_i·D_j                    [rank-2, pairs — existing 28]
     + Σ_{i<j<k} κ_ijk(s)·D_i·D_j·D_k               [rank-3, triples — NEW]
```

where every coefficient is a function of the situation vector s.

### Situation vector (7 dimensions)

```
s = (sleep_debt_7d, acute_stressor, circadian_misalignment,
     social_isolation, financial_pressure, illness_load, life_transition)
```

### Situational gating

Each coupling becomes a gated function:

```
κ_ij(s) = κ_ij^base · σ(w_ij · s + b_ij)
```

At s = 0 (neutral), behavior is identical to the current matrix. The gate
learns from data which situations amplify or invert each pair. This is the
mean-field-with-external-field formulation from non-equilibrium statistical
mechanics.

## The free-energy gate (which terms to include)

For every candidate triple or situational gate:

```
F = cost − T · info_gain

  cost       = n_params · log(N_samples)         [AIC/BIC form]
  info_gain  = Δlog-likelihood on HELD-OUT data
  T          = exploration temperature (default 1.0)
```

- F > 0 → SKIP (term does not earn its parameters)
- F < 0 → ADD (term pays for itself in predictive power)

This prohibits adding all 56 possible triples. Most will correctly fail the
gate. Only biology-justified seeds with real data support survive.

## Adiabatic staging (don't skip stages)

### Stage A — Sparse triples (rank-3 only, no gating)
- Add 8–12 biology-justified triples. Allow antagonistic (negative) triples.
- Validate: held-out log-likelihood must improve vs rank-2-only.
- Risk: low. Pure addition.

### Stage B — Situational gating on existing 28 pairs
- Initialize w_ij = 0 → launch behavior identical to today.
- Learn w_ij from data via Bayesian update.
- Risk: medium. Must prove it doesn't add variance without accuracy.

### Stage C — Triples + gating (full Hamiltonian)
- Apply situational gating to the rank-3 triples.
- Target end state.

**Do NOT collapse stages.** Stage C without A and B is a 130-parameter model
with no priors — guaranteed overfit.

## Antagonistic coupling (resolves the all-positive limitation)

The canonical 28-pair prior stays all-positive (VERITAS-locked). Antagonism
enters at rank-3 and via situational gating. Example antagonistic triples:

- (VOC, PHY, SOC): overwork → physical neglect → social withdrawal
- (FIN, SPI, PSY): material accumulation without meaning → emptiness/anxiety

## User preference: lock design details, don't questionnaire

When presenting a physics-scoring design to the user, DO NOT append open-ended
questions asking them to curate parameter lists. Lock the implementation
details yourself (which triples, which situation factors, which evidence
policy) with stated rationale. The user's role is veto-only. See
`adhd-choice-discipline` skill for the full pattern.

## Implementation reality (rank-3 build, 2026-06-29)

The Stage A upgrade landed via the mastermind spec-to-surgery loop. What
actually shipped differs from the design above in three ways that future
calibration work must respect.

### What shipped

- `KAPPA_3D: dict[tuple[int,int,int], float]` with 56 entries (C(8,3)).
- Values derived deterministically from the 28 pair kappas:
  `kappa_ijk = 0.5 * (k_ij * k_ik * k_jk)^(1/3)` (geometric mean, attenuated).
  This makes triples entangled with pairs — recalibrate KAPPA and triples
  follow on next import. Values range 0.057–0.181, inside the 0.5 schema cap.
- Triple loop runs AFTER the pair loop in `compute_twc()`. Both raw integral
  and kappa_total include triples.
- `TWCResult` extended with `kappa_3d_sum` and `triple_coupling_sum`.
- Engine tag bumped from `calculator_v3` to `calculator_v4`.

### Backward-compatibility lesson (surgeon caught a spec error)

The spec proposed `synergy = coupling_sum / 84` (28 pairs + 56 triples).
This BREAKS backward compat: empty KAPPA_3D produces `pair_coupling / 84`
which differs from v3's `pair_coupling / 28`. The test
`test_compute_twc_backward_compat` failed.

**Sound fix** (landed): `synergy = pair_coupling/28 + 0.5 * (triple_coupling/56)`.
This collapses to EXACTLY v3 when KAPPA_3D is empty. Only the synergy
normalization diverged from the spec; `twc_raw` and `kappa_total` still
include triples as specified.

### Modulation verification technique

To prove triples contribute (not cosmetic), patch the module global in place:

```python
import calculator as calc
r_with = calc.compute_twc(scores)
orig = calc.KAPPA_3D
calc.KAPPA_3D = {}  # patch in place, NO reload
r_without = calc.compute_twc(scores)
calc.KAPPA_3D = orig  # restore
delta = abs(r_with.twc_final - r_without.twc_final)
```

Measured result for a mid-range input vector
(psy7/phy6.5/int7.5/soc6/spi5.5/voc6.5/fin6/env5.8):
- WITH triples: `twc_final=0.431`, synergy=0.0814, triple_coupling_sum=1.0397
- WITHOUT triples: `twc_final=0.429`, synergy=0.0721, triple_coupling_sum=0.0
- Delta: 0.002 (0.235 points on the 100-scale). Well under the 5pt adiabatic cap.

**WARNING**: do NOT use `importlib.reload()` to empty KAPPA_3D. Reload rebuilds
module globals from source, silently undoing the patch and producing a false
zero-delta result. Patch the attribute on the live module object only.

### Three post-surgery flags (domain-specific)

1. **Detached HEAD**: the hydra-os submodule commit (e81f2f57) sits on a
   detached HEAD. Must be branched before any submodule-pointer push or it
   can be garbage-collected.
2. **Missing input_adapters**: `health-private/score_from_evidence.py` imports
   from `input_adapters` which is absent from the tracker directory. This
   blocks end-to-end CLI scoring runs. Pre-existing, not caused by the upgrade.
   The calculator engine itself is fully operational standalone.
3. **Divergent vendored copy**: `your-org/the operator agent/health-private/` has a
   separate copy of score_from_evidence.py that is NOT synced with this rank-3
   patch. Sync if that copy is a live caller.

### What is still needed

- kappa_ijk values are INITIAL ESTIMATES only (geometric mean of pairs, ×0.5).
  Ready for calibration against the principal's longitudinal data once the pipeline
  is re-enabled (the daily scorecard cron was disabled ~May 29 and never
  re-enabled).
- Situational gating (Stage B) and triples + gating (Stage C) from the design
  above have NOT been built. The current implementation is Stage A only.

## Source artifacts

- Design doc: `COUPLING_V2_PHYSICS_DESIGN.md` (your-workspace)
- Canonical prior: `organism/canonical_coupling.py` (28-pair DB source)
- MI refinement layer: `twc_coupling_physics.py` (normalized mutual information)
- Audit context: `coupling-matrix-audit/REVIEW-2-STATISTICAL-CAUSAL.md` §4.4
