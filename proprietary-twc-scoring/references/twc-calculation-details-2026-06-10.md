# TWC Calculation Details and Validation

This document provides detailed information about the TWC (Total Wellness Composite) calculation, validation procedures, and known issues related to the proprietary TWC formula used in the 8D360 scoring system.

## TWC Formula

The proprietary TWC formula consists of three layers:

```
TWC = Σᵢ wᵢ·Dᵢ + Σᵢ≠ⱼ κᵢⱼ·Dᵢ·Dⱼ
```

Where:
- wᵢ are the dimension weights
- Dᵢ are the dimension scores (0-10 scale)
- κᵢⱼ are the coupling coefficients

### Dimension Weights (Layer 1 - 40%)
- ψ PSY (0.15) — reasoning coherence, cognitive load
- φ PHY (0.15) — infrastructure health, error rates, uptime
- ε ENV (0.10) — configuration, paths, tool access
- τ SOC (0.10) — collaboration, cross-pollination
- σ SPI (0.10) — mission alignment, DS grounding
- ι INT (0.15) — output quality, depth, accuracy
- υ VOC (0.15) — mandate completion, task throughput
- ϕ FIN (0.10) — cost efficiency, model optimization

### Key Coupling Coefficients (Layer 3 - 30%)
- PSY↔INT: 0.85 (strongest — reasoning drives quality)
- PHY↔VOC: 0.78 (infra drives output)
- SOC↔SPI: 0.72 (collaboration drives alignment)
- ENV↔PHY: 0.68 (config drives health)

### Layer 2 (30%): Peer assessment — agents score each other (weekly rotation)

## Validation Procedures

### TWC Recomputation
To validate a stored TWC value:
1. Retrieve the 8 dimension scores from daily_scorecard
2. Calculate the weighted sum: Σ(wᵢ·Dᵢ)
3. Calculate the coupling sum: Σᵢ≠ⱼ κᵢⱼ·Dᵢ·Dⱼ
4. Sum the two components: TWC = weighted sum + coupling sum
5. Apply efficiency cap: TWC = min(TWC, 8.5)
6. Compare with stored value

### Known Implementation Gap
Despite the formula documenting significant coupling coefficients, the current implementation in `twc_calculator.py` does NOT apply these coupling terms to the TWC calculation. The stored TWC value matches the computation `weighted_sum × 10 × stacked_modifier` exactly, with the coupling_sum column (6.775) never being added.

This means Layer 3 (cross-dimensional coupling) has zero effect on scores regardless of dimension values.

## Validation Steps

To validate TWC calculations in the system:

1. **Check coupling terms**: Verify that interaction_matrix values are being used in TWC calculation
2. **Recompute TWC**: Use the full formula with coupling terms
3. **Compare results**: Check if stored TWC matches recomputed value
4. **Review coupling_sum**: Verify that coupling_sum in daily_scorecard is being incorporated

## References
- Proprietary TWC Scoring skill
- Health Scoring Daily Pipeline skill: Database Integrity Verification Procedure section