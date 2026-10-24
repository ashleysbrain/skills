# Fresh-organism layered 8D learning (Cyber the operator agent pattern)

When a shipped the operator agent must **learn its owner** and drive healing/high-performance without burnout:

## Never rebuild the math

Canonical calculator: `hydra-os/products/principal-8d-tracker/calculator.py`  
Ship as: `organism/scoring/calculator.py`  
Call: `compute_twc(list[DimensionScore])` → `twc_final`, `coherence`, `synergy`, `classification`

Rescore engines, nutrition/sexual-health modifiers, ADHD fusion stay in the full 8D360 product path — do not half-port them into a B2BU clone unless type is B2C and adapters are present.

## Check-in path that works

```
payload (stress/energy/sleep/mental/work/focus/…)
  → L1: map to dims_10 (psy..env), blend with owner baseline (α~0.15)
  → DimensionScore(name, symbol, score=dim10/10)
  → compute_twc
  → L4 healing_plan + L5 operating_system
  → persist user_model.json + twc_history.jsonl
```

Full sub-algorithms (`score_psychological(PsychologicalInput(...))`) require correct field scales (ints 1–5, etc.). Wrong scales → TWC ~0–0.1 even on "good" days. Prefer dim10 path for lightweight check-ins.

## Layers

| Layer | Job |
|-------|-----|
| L0 | Raw signals (check-in, tech feedback, work session) |
| L1 | Adapters + confidence |
| L2 | Owner-only baseline (`owner_baseline.json`) — never peer |
| L3 | calculator TWC |
| L4 | Repair-first dims, coupling notes (κ), micro-actions |
| L5 | Work blocks, breaks, check-in cadence from TWC risk |

## API surface

- `POST /api/user/health-check` → full score bundle (`engine` must mention calculator)
- `GET /api/user/summary`, `/recommendations`, `/model`, `/operating-system`
- UI: `/you`

## Type lock

| Type | Learning domain |
|------|-----------------|
| B2C | Personal wellness 8D (wearables, nutrition adapters ok) |
| B2B | Company KPIs |
| B2BU | Professional performance + sustainable load (Cyber the operator agent default) |

Emotional (constitution) ↔ Psychological (calculator).

## Adversarial seats for this class of work

Popper (math only), CALIBER (no hand rescore), Kahneman, Bandura, Dweck, Selye, Attwell — consecutive panel, not generalist rewrite.
