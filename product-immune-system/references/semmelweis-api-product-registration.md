# Semmelweis API — Product Registration Reference

the specialist engine engine (port 8131, DS-ECS-07.04.01-v3.0.0).

## Full Endpoint Surface

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Engine health + `products_tracked` count |
| POST | `/v1/register` | Register a product for immune surveillance |
| POST | `/v1/milestone` | Record a developmental milestone (+2 health) |
| POST | `/v1/feedback` | Record user feedback (adjusts health ±5, triggers alert if <50) |
| GET | `/v1/check-readiness/{product_id}` | Maturation gate — ready for next version? |
| GET | `/v1/health-report/{product_id}` | Full immune chart (milestones by category, health, alerts) |
| GET | `/v1/products` | List all tracked products |
| GET | `/v1/layers` | Immune layer architecture (threat recognition, protocol enforcement, memory) |
| GET | `/v1/vitals` | Engine vital signs |
| GET | `/v1/methodology/*` | Methodology engine (institutions, methodologies, personalities, sub-agents) |
| GET | `/v1/philosophy/*` | Philosophy engine (wisdom principles, sources) |

## Register Request Shape

```json
{"product_id": "8d-sleep", "name": "8D Sleep", "version": "1.0.0"}
```

Response: `status: ok`, `initial_status: "newborn"`, `initial_health_score: 100.0`

## Milestone Request Shape

```json
{
  "product_id": "8d-sleep",
  "milestone_name": "ci_pipeline_active",
  "category": "innate_immunity",
  "evidence": "GitHub Actions CI: build+test on every push/PR. 3 green runs (IDs ...)."
}
```

Each milestone: +2 health, advances status newborn → developing.

## Feedback Request Shape

```json
{"product_id": "8d-sleep", "feedback_text": "Works great for tracking sleep", "sentiment": 0.8}
```

Sentiment range: -1.0 to +1.0. Health delta = sentiment * 5.0.
If health drops below 50 with negative sentiment, immune alert fires
(the specialist engine / the specialist engine alerted).

## Worked Example: 8D Sleep Registration (2026-06-20)

First product enrolled in immune surveillance. Registration + 7 birth-canal
milestones recorded in one pass:

```
REGISTER 8d-sleep -> newborn, health=100
  ci_pipeline_active              (innate_immunity)          health=100, milestones=1
  build_passes_clean              (innate_immunity)          health=100, milestones=2
  test_suite_present              (immune_memory)            health=100, milestones=3
  readme_documented               (post_birth_documentation) health=100, milestones=4
  cruft_removed                   (hygiene_protocol)         health=100, milestones=5
  birth_canal_quality_gate_passed (passive_immunity)         health=100, milestones=6
  branch_protection_soft_gate     (barrier_defense)          health=100, milestones=7

CHECK-READINESS:
  milestones_sufficient: true
  health_adequate: true
  feedback_sufficient: false    <- needs real user feedback
  ready_for_next_version: false  <- correct: immune system requires real-world exposure
```

Evidence for each milestone was verified against live GitHub state (CI run IDs,
commit SHAs, package.json scripts) before recording — never fabricate evidence.

## Dependencies

Semmelweis depends on: Quartz (timing), Waddington (reproductive), Franklin
(genome), Farr (immune defense), Clinical (diagnostic). When a product
degrades, Semmelweis signals Farr/Burnet for adaptive response.
