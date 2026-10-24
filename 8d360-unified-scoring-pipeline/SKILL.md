---
name: 8d360-unified-scoring-pipeline
version: 1.0.0
description: Unified 8D360 scoring pipeline — one calculator, multiple evidence sources, confidence-aware merging, automated review.
trigger: When scoring TWC, auditing the scoring system, adding new evidence sources, or running the review cycle.
---

# 8D360 Unified Scoring Pipeline

## Architecture

```
Evidence Sources          Adapters           Merger              Calculator          Storage
─────────────         ──────────          ────────            ───────────          ───────
Check-in (1.0) ─────→ checkin_adapter ──┐
Nutrition (0.7) ────→ nutrition_adapter ─┤
Transcript (0.4) ───→ transcript_adapter─┼→ confidence merger → calculator.py → DB (atomic)
ADHD Compass (0.7) ─→ adhd_fusion ──────┘                      ↓
                                                         unified_pipeline.py
                                                              ↓
                                                    system_review.py (audit)
```

**calculator.py is the ONLY scoring math.** Everything else is an input adapter.

## Files

| File | Location | Purpose |
|---|---|---|
| `calculator.py` | `products/principal-8d-tracker/` | Coupling matrix + coherence + synergy tensor. THE math. |
| `unified_pipeline.py` | `products/principal-8d-tracker/` | Single entry point. All sources → merger → calculator → store |
| `input_adapters/__init__.py` | `products/principal-8d-tracker/input_adapters/` | Confidence wrapper, baselines, merger, credibility intervals |
| `input_adapters/transcript_adapter.py` | same | Standup text → calculator fields (0.4-0.7 confidence) |
| `input_adapters/nutrition_adapter.py` | same | Nutrition 0-100 → PhysicalInput + cascades |
| `input_adapters/checkin_adapter.py` | same | Check-in answers → calculator fields (1.0 confidence) |
| `system_review.py` | `products/principal-8d-tracker/` | 6-check automated audit + specialist agent task generation |
| `operational_layer.py` | `products/principal-8d-tracker/` | Stocks, EWMA, Cascade, PCM, CSI consuming calculator.py outputs |
| `scoring_pipeline.py` | `products/principal-8d-tracker/` | Legacy pipeline (being deprecated) |

## Phase Completion Status
- Phase 1 (Input Adapters): ✅ COMPLETE — input_adapters/ with confidence-aware merging
- Phase 2 (Bridge Scripts): ✅ COMPLETE — 5 legacy systems bridged to unified_pipeline
- Phase 3 (Operational Layer): ✅ COMPLETE — operational_layer.py consumes calculator.py outputs
- Phase 4 (ADHD EF Compass v3): ✅ COMPLETE — sigmoid curves, 10 domains
- Phase 5 (Review Cron): ✅ COMPLETE — system_review.py (6 checks), 12h cron with specialist agents

## Bridge Files (Phase 2 — redirect legacy systems)

| Bridge | Replaces | Location |
|---|---|---|
| `transcript_bridge.py` | `transcript-analyzer.py` TWC | `scripts/` |
| `scoring_engine_bridge.py` | `8d360-scoring-engine.py` TWC | `scripts/` |
| `nutrition_bridge.py` | `8d360-nutrition-engine.py` modifier | `scripts/` |
| `rescore_bridge.py` | `rescore_engine.py` TWC | `scripts/rescore-engine/` |
| `rescore_report_bridge.py` | `rescore_and_report.py` TWC | `intel/agents/` |

## Commands

```bash
# Full autonomous scoring (all sources)
cd /<workspace>
python3 unified_pipeline.py --full

# Score from transcript
python3 unified_pipeline.py --transcript /path/to/transcript.md

# Score from raw text
python3 unified_pipeline.py --text "I had a productive day"

# Score for specific date
python3 unified_pipeline.py --date 2026-05-27

# System review (5 checks)
python3 system_review.py --full

# System review with auto-fix (deletes orphans)
python3 system_review.py --full --fix

# JSON output
python3 system_review.py --full --json
```

## Confidence Levels

| Level | Value | Source |
|---|---|---|
| Direct | 1.0 | Check-in answers, sensor data |
| Strong | 0.7 | Transcript with context, ADHD Compass |
| Weak | 0.4 | Keyword presence, no context |
| Baseline | 0.2 | Personal defaults (no evidence) |
| None | 0.0 | No data at all |

## Merger Rules

- Highest confidence wins per field
- On tie, incumbent (earlier source) wins
- Coverage = fraction of fields with confidence > 0
- Credibility interval: ±uncertainty based on coverage × confidence

## Specialist Agent Types (Phase 5)

| Specialist | Audits |
|---|---|
| `math_auditor` | Calculator formulas, coupling matrix, recomputation |
| `adapter_engineer` | Input adapters validity |
| `pipeline_engineer` | End-to-end unified_pipeline |
| `data_integrity` | Orphan records, missing data, stale data |
| `integration_engineer` | Bridge scripts existence and functionality |

## Cron Jobs

| ID | Name | Schedule |
|---|---|---|
| `e1b0a2a2845b` | AISHA-MD Daily Unified Scorecard | 30 7 * * * |
| `c34176850670` | Divinity Science Daily TWC Scorecard | 0 22 * * * |
| `4f12500410e3` | 8D360 System Review Cycle | every 720m |

## Phase Status

- ✅ Phase 1: Input adapter layer (confidence-aware dataclasses + 3 adapters + merger)
- ✅ Phase 2: Bridge scripts for all 5 legacy systems
- ✅ Phase 4: ADHD EF Compass v3 (sigmoid curves, 10 domains)
- ✅ Phase 5: Review cron with specialist agent spawning
- ❌ Phase 3: Operational layer reconnection (stock-and-flow, EWMA, cascade, PCM, CSI consume calculator.py outputs)

## Pitfalls

- `scoring_pipeline.py` is the OLD pipeline. Use `unified_pipeline.py` for everything.
- Legacy scripts are NOT modified. Bridges wrap them. This is intentional — the legacy scripts may have other consumers.
- The rescore contract: positive evidence must NEVER lower the score. The bridge enforces this.
- Calculator.py uses ETA=0.85 as the theoretical maximum. TWC values above this are impossible.
- SQLAlchemy must be installed: `python3 -m pip install sqlalchemy --break-system-packages`
- **score_from_evidence.py** (in `health-private/`) writes to the PRODUCTION DB (`ashley_unified_health.db`). As of 2026-05-28 it correctly imports calculator.py for TWC computation. Before that date it used simple linear arithmetic. If you see `score_engine='fallback_linear'` in the DB, the calculator import failed — investigate.
- **Two databases exist**: `wellness.db` (unified_pipeline writes here) and `ashley_unified_health.db` (score_from_evidence.py writes here). The production dashboard reads from `ashley_unified_health.db`. Do not assume wellness.db is the source of truth.

## Production DB Writer

`~/your-workspace/health-private/score_from_evidence.py` is the CLI that cron jobs and standup processing call to write scores. It writes to `ashley_unified_health.db`. As of 2026-05-28, its `compute_twc()` function delegates to `calculator.py` for the coupling matrix + coherence + synergy computation, then applies nutrition/sexual-health modifiers on the 0-100 scaled result. New columns: `coherence`, `synergy`, `coupling_sum`, `score_engine` (auto-migrated on first write).

## Native AI Dimensions and PIML Verification

When working on 8D360AI (the AI-agent variant), the human-mapped dimensions
feel wrong because they are borrowed categories, not native failure modes.
See `references/native-ai-dimensions-and-piml-results.md` for:
- Why the current human dimensions are a poor fit for AI
- The proposed "8 Resilience Pillars" replacement (Cognitive Integrity,
  Pipeline Reliability, Resource Efficiency, Knowledge Currency, Interaction
  Coherence, Adaptation Capacity, Aligned Execution, System Volatility) with
  coupling coefficients
- Three alternative naming sets using the same telemetry
- The REAL PIML prototype numbers (4.2x extrapolation, 6% overall) versus the
  inflated "4-12x" marketing claim, with the correct honest framing
- The autonomous self-healing loop architecture (8 stages, 3 physics moats)
