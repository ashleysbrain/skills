# TWC Computation Architecture — Code Path Analysis
**Date**: 2026-06-08  
**Source**: AUDIT-ALGO independent audit session

## Code Path Map

The TWC value that lands in `ashley_unified_health.db → daily_scorecard.twc_score` can come from multiple sources, each with a different computation path:

### Path 1: Transcript/Standup Parse (most entries)
```
Transcript text → 8d360-scoring-engine.py (legacy, 2214 lines)
  → twc_geometric() [weighted geometric mean]
  → deficit_penalty() [BETA_DEFICIT = 0.15 × spread/100]
  → momentum() [MOMENTUM_COEFFICIENT = 0.05]
  → PCM, CSI overlays
  → raw_twc = geo * dp * (1 + 0.05 * mom) * pcm * csi
  → DB write via scoring pipeline
```

### Path 2: Unified Pipeline (newer, via bridge)
```
Input data → unified_pipeline.py → unified_score()
  → calculator.py → compute_twc()
    → WEIGHTS = [1/8] * 8 (equal weights, NOT proprietary 0.08–0.18)
    → twc_raw = Σ(w_i * d_i) + Σ(κ_ij * d_i * d_j)  [coupling IS computed here]
    → twc_norm = twc_raw / (1 + kappa_total)
    → coherence = 1 - σ_D / μ_D
    → synergy = coupling_sum / 28
    → twc_final = ETA * μ_D * coherence * (1 + 0.5 * S)  [ETA = 0.85 cap]
  → ADHD fusion overlay
  → Credibility intervals
  → scoring_engine_bridge.py adapts output for legacy compatibility
  → DB write
```

### Path 3: Rescore Engine
```
rescore-input JSON → rescore_engine.py
  → Preserves preliminary base dimensions
  → Lifts dimensions per evidence rules
  → Recomputes TWC using internal formula
  → DB write (if Step 6.5 verified)
```

### Path 4: Cron/Carryforward
```
Carryforward cron → copies previous day's values
  → No recomputation
  → May overwrite valid rescores (collision pattern)
```

## Three Kappa Value Sets

| Source | Range | Example Values |
|--------|-------|----------------|
| Proprietary spec (SKILL.md) | 0.68–0.85 | PSY↔INT: 0.85, PHY↔VOC: 0.78 |
| calculator.py KAPPA dict | 0.10–0.45 | Ψ-So: 0.40, In-Vo: 0.45, Ψ-P: 0.325 |
| DB interaction_matrix | 0.05–0.35 | PHY-PSY: 0.35, ENV-PSY: 0.30 |

None match. The DB values produce coupling_sum = 6.775 (constant across ALL dates) which is dead code — stored but never added to TWC.

## Independent Recomputation Results (2026-06-08)

Using documented formula: weighted geometric mean × 10 × sqrt(nut_mod × sex_mod)

| Date | Stored TWC | Independent TWC | Delta |
|------|-----------|-----------------|-------|
| 2026-05-28 | 55.58 | 55.73 | +0.15 |
| 2026-05-27 | 60.22 | 60.36 | +0.14 |
| 2026-05-29 | 28.36 | 29.00 | +0.64 |
| 2026-04-07 | 71.88 | 71.52 | -0.36 |

Deltas are small but non-zero. The actual pipeline includes deficit penalty and possibly momentum/PCM/CSI overlays not captured in the simplified documented formula.

## Key Files

- `~/your-workspace/hydra-os/products/principal-8d-tracker/calculator.py` — compute_twc() with coupling + coherence
- `~/your-workspace/hydra-os/products/principal-8d-tracker/unified_pipeline.py` — unified_score() orchestrator
- `~/your-workspace/hydra-os/scripts/scoring_engine_bridge.py` — legacy adapter
- `~/your-workspace/hydra-os/scripts/8d360-scoring-engine.py` — legacy engine (2214 lines)
- `~/your-workspace/hydra-os/scripts/rescore-engine/rescore_engine.py` — rescore specialist

## Recommendations

1. **Before product launch**: Reconcile all three κ value sets to one authoritative source
2. **For audits**: State which code path produced the "recomputed" value; never claim "independent verification" when re-running the same pipeline
3. **Architecture cleanup**: The bridge pattern (Path 2) adds complexity without clear benefit while the legacy engine (Path 1) still writes most entries
