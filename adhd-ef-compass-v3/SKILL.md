---
name: adhd-ef-compass-v3
version: 1.0.0
description: ADHD EF Compass v3 with sigmoid response curves and signal fusion layer for calculator.py TWC integration
files:
  - products/principal-8d-tracker/adhd_ef_compass_v3.py
  - products/principal-8d-tracker/adhd_signal_fusion.py
  - products/principal-8d-tracker/calculator.py
  - products/principal-8d-tracker/scoring_pipeline.py
tags: [adhd, scoring, twc, sigmoid, health, proprietary]
---

# ADHD EF Compass v3 — Sigmoid Response + Signal Fusion

## Architecture

```
Passive behavioral metrics (20 signals)
       ↓
adhd_ef_compass_v3.py — sigmoid transforms per metric
       ↓
10 EF Domain scores (0.0-1.0, sigmoid-normalized)
       ↓
adhd_signal_fusion.py — sigmoid fusion for multi-domain fields
       ↓
42 calculator.py input fields across 7 dimensions
       ↓
calculator.py — TWC with coupling matrix + coherence + synergy
       ↓
TWC OUTPUT (single canonical value)
```

## Key Files

| File | Purpose |
|------|---------|
| `adhd_ef_compass_v3.py` | Compass: passive metrics → 10 domain scores via sigmoid |
| `adhd_signal_fusion.py` | Fusion: 10 domains → 42 calculator fields, sigmoid-combined |
| `calculator.py` | TWC algorithm: 8 dimensions → single TWC score |

## The 10 EF Domains (v3)

Realigned from v2:
- `initiation` — task starting, overcoming inertia
- `working_memory` — holding info, cognitive load
- `planning_organization` — structuring, systems (NEW in v3)
- `time_awareness` — time blindness, duration estimation
- `emotion_regulation` — emotional lability, RSD
- `impulse_control` — impulsive decisions, spending, switching
- `motivation_persistence` — sustaining effort, overcoming boredom
- `focus_attention` — sustained + hyperfocus (merged from v2 sustained_attention + hyperfocus)
- `self_monitoring` — metacognition, error detection (NEW in v3)
- `cognitive_flexibility` — task switching, adaptability (evolved from v2 transitions)

Removed from v2: `sleep_context_sensitivity` (not an EF domain, belongs in health pipeline)

## Why Sigmoid, Not Linear

v2 used `score_ratio_good/inverse` → piecewise linear clamps (0-10).
v3 uses `sigmoid_response(raw, k, midpoint)` → smooth psychometric curves.

Properties:
1. **Maximum sensitivity at clinical threshold** (the midpoint)
2. **Automatic ceiling/floor compression** (no arbitrary clamps)
3. **Per-domain steepness (k)** calibrated to ADHD population data
4. **Double-counting prevention** in fusion: `σ(a+b) ≠ σ(a) + σ(b)`

### Double-counting proof

`VOC.work_quality` is hit by 5 ADHD domains. When all 5 are at 0.1 (severe):
- Linear sum: 1.40/5 (catastrophic)
- Sigmoid fusion: 2.96/5 (bad but functional)
- Difference: +1.56 points of prevented inflation

## Fusion Coverage

- **PSY**: 10 fields affected (mood, volatility, anxiety, awareness, triggers, etc.)
- **VOC**: 10 fields (work_quality hit by 5 domains, achievements by 2)
- **INT**: 8 fields (focus_min, distractions, memory, problem_solving, etc.)
- **SPI**: 4 fields (purpose_clarity, inner_peace, meaning, values_alignment)
- **SOC**: 4 fields (conflicts, quality, belonging, depth)
- **FIN**: 4 fields (savings_rate, stress, goals_progress, literacy)
- **ENV**: 2 fields (organization, space)
- **PHY**: 0 direct (indirect through behavior only)

## Usage

```python
from adhd_ef_compass_v3 import derive_compass, score_passive_domains
from adhd_signal_fusion import build_all_inputs

# Step 1: Score domains from passive data
domain_scores = score_passive_domains(passive_data)

# Step 2: Fuse into calculator inputs
result = build_all_inputs(domain_scores)

# Step 3: Feed into calculator.py
from calculator import PsychologicalInput, score_psychological
psy_input = PsychologicalInput(**result["PSY"])
psy_score = score_psychological(psy_input)
```

## Medication Window Model

v3 uses dual-sigmoid pharmacokinetic curve:
- Rise sigmoid centered at 40 min (onset)
- Fall sigmoid centered at 220 min (offset)
- Peak boost: 15% at ~120 min
- Domains affected: focus_attention, impulse_control, working_memory, initiation

## Domain-Metric Sigmoid Parameters

Calibrated from Barkley EF factor analysis, Conners CPT normative data, BRIEF-A T-scores:

| Metric | k (steepness) | midpoint | Direction |
|--------|--------------|----------|-----------|
| completion_ratio | 4.0 | 0.45 | positive |
| start_delay_minutes | 0.08 | 30.0 | inverse |
| app_switching_events | 0.3 | 10.0 | inverse |
| mood_volatility | 1.0 | 2.5 | inverse |
| transition_delay_minutes | 0.08 | 25.0 | inverse |
| streak_days | 0.5 | 3.0 | positive |
| calendar_adherence | 4.0 | 0.50 | positive |

## Confidence Propagation

Per-domain confidence based on passive metric coverage:
- `sigmoid_response(coverage, k=6.0, midpoint=0.40)` — steep ramp, needs 40% metric coverage for 0.5 confidence
- Fusion layer propagates: weighted average of source domain confidences per field

## Pitfalls

1. **DO NOT** bypass the fusion layer and feed ADHD scores directly into calculator.py
2. **DO NOT** use linear weighting for multi-domain fields — that's the whole point of sigmoid fusion
3. The fusion layer outputs calculator.py-compatible dicts, NOT DimensionScore objects — you must construct the dataclasses
4. PHY dimension has NO direct ADHD mapping — use overrides or defaults only
5. v2 domains (sustained_attention, hyperfocus, transitions, sleep_context_sensitivity) no longer exist in v3
6. **DO NOT** write TWC to the database without simultaneously writing dimension scores — use `scoring_pipeline.py` for atomic computation (see `health-data-pipeline-maintenance` skill for the orphan record antipattern)
