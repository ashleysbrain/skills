# Cyber the operator agent gg_core + health API shape (2026-08-02)

## Phenotype
- Cyber the operator agent product type: **gg_core** (full the operator agent), not locked b2bu
- Can birth b2bu; balanced 8D weights 0.125; physics-PM constitution
- Health-first: L5 OS downstream of TWC

## POST /api/user/health-check
Request JSON:
```json
{
  "stress_level": "low|medium|high",
  "energy_level": "low|medium|high",
  "sleep_quality": "poor|fair|good",
  "mental_state": "calm|focused|anxious|overwhelmed"
}
```

Response must include:
- `recorded: true`
- `twc_100`, `classification`
- `engine` → `scoring/calculator.py` (or equivalent calculator path)
- `healing_plan`, `coherence`, dimensions

UI `/you` success path checks `result.recorded`.

## Path
dim10 → DimensionScore(score=v/10) → compute_twc — not full sub-algorithm-only path for lightweight check-ins.
