# Layered stack and dim10 product path

## Why layers

A flat `user_model.json` with null 8D scores and string burnout labels cannot heal anyone. Learning must change **measurable** TWC and **actionable** OS rules.

## L0–L5 in one pass

1. Collect check-in / tech feedback / work signal (L0)
2. Map to 1–10 dims with confidence + baseline blend (L1–L2)
3. `DimensionScore(score=v/10)` × 8 → `compute_twc` (L3)
4. Sort dims ascending; emit micro-actions + coupling notes (L4)
5. Set WIP/breaks/check-in cadence from TWC risk band (L5)
6. Persist model + append `twc_history.jsonl`

## Dim10 mapping sketch (B2BU)

| Signal | Primary dims |
|--------|----------------|
| stress_level | psy ↑ when low stress |
| energy_level + sleep_quality | phy |
| focus + work_load | int, voc |
| collaboration | soc |
| purpose | spi, voc |
| money_stress | fin |
| tools_env | env |

Blend: `0.7 * observation + 0.3 * owner_baseline` (Kahneman guard).

## Code sketch

```python
from calculator import DimensionScore, compute_twc, DIMENSION_NAMES, DIMENSION_SYMBOLS

def dim10_to_scores(d):
    order = ["psy","phy","int","soc","spi","voc","fin","env"]
    names = DIMENSION_NAMES  # Psychological first
    return [
        DimensionScore(name=names[i], symbol=DIMENSION_SYMBOLS[i],
                       score=max(0, min(1, d[k]/10)),
                       sub_scores={"dim10": d[k]})
        for i, k in enumerate(order)
    ]

result = compute_twc(dim10_to_scores(dims10))
# result.twc_final, result.classification, result.coherence, result.synergy
```

## Emotional ↔ Psychological

Store constitution keys as `emotional` if needed; always score as calculator Psychological index 0.

## What not to do

- Invent a second TWC formula in the organism
- Ship only adaptive tech quiz without feeding holistic model
- Use peer organism fleet scorecards as EMBEDDED_AGENTS_DATA
- Depend on `/<workspace>` at runtime after vendor