# PENDING (curator: add SKILL.md pointer to this file under "Review the ACTUAL BUILT SYSTEM")

# Built Experience/Activity Database — Census + Portability Map (2026-08-18)

## The actual built database (not a planning doc)

`your-org/the operator agent/health-private/ashley_unified_health.db`, table
`master_activities` — **268 rows**, hand-built by principal with per-row citations.

| Field | Census |
|---|---|
| primary_dimension | PHY 66, ENV/INT/SOC/SPI 30 ea, PSY 28, FIN/VOC 27 |
| scoring_direction | POSITIVE 210, NEGATIVE 58 (harmful-at-dose rows) |
| evidence_grade | STRONG 171, MODERATE 96, WEAK 1 |
| dose_response_shape | threshold 138, linear 87, logarithmic 39, inverted_u 4 |
| evidence_source | real citations per row (Putnam 2000, Cacioppo & Hawkley 2009, Gottman 1994, ...) |
| dose fields | dose_unit, min/optimal/ceiling_dose |

Dimension-expansion SQL lives beside it: `soc/int/env_activities.sql`.
Scoring integration: `activity_scoring.py` (reads master_activities dosing
rules → activity_scoring_cache).

## Companion documents (build order matters)

- `hydra-os/intel/qubit-health/scoring-methodology-5wh-2026-02-21.md` — the
  5W+H rubric spec (486 lines, instrument-anchored: WHO-5, FACIT-Sp, UCLA-3,
  MSPSS, CFPB, JSS, with psychometric alphas).
- `qubit-gr-roadmap-2026-03-31.md` §7 — the PLANNED universal experience
  database (PostgreSQL, community calibration). Planning doc, NOT built.

## Portability: 5WH as a dimension-agnostic classification system

The schema is dimension-agnostic — the columns do not know they describe
health activities. Port to technology classification (minted as mosaic task
T-260818-0142, 2026-08-18):

| 5WH | Health DB field | Technology registry equivalent |
|---|---|---|
| WHO | primary_dimension consumer | consuming entity/lane |
| WHAT | activity class + weights | tech class + capability axes |
| WHEN | measurement frequency | probe cadence (re-measure on version drift) |
| WHERE | context weighting | execution context (local/cloud/API) |
| WHY | motivation profile | organism lane purpose |
| HOW | data collection method | integration method (MCP, bus, API) |
| — | evidence_grade | probe-measured STRONG/MODERATE/WEAK |
| — | dose_response_curve | min/optimal/ceiling economics |
| — | NEGATIVE direction | harmful-at-dose classification (curves, not booleans) |

**Binding rule that survives the port: curves get FIT from probe_runner
measurement, never asserted.** A classification without measurement is a
claim, not a fact (same law as substrate_selector).

Market context (arXiv scan 2026-08-18: RouteLLM, FrugalGPT, CASTER, LEMON,
UniScale, stepwise routing): routing literature covers cost+capability only;
no published system does evidence-graded taxonomy, dose-response economics,
or NEGATIVE-direction classification. The WHO+WHICH dispatch join
(mosaic dispatch_gate, origin `ceo:internet-of-models`) plus this schema is
the differentiation.
