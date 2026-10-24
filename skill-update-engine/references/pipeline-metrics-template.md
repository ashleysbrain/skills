# Pipeline Metrics Template

Weekly metrics are generated every Monday at 09:00 UTC.

## Template

```json
{
  "week": "YYYY-WNN",
  "period_start": "YYYY-MM-DD",
  "period_end": "YYYY-MM-DD",
  "candidates_generated": 0,
  "candidates_unique": 0,
  "candidates_auto_shipped": 0,
  "candidates_reviewed": 0,
  "patches_auto_shipped": 0,
  "patches_reviewed": 0,
  "patches_rejected": 0,
  "patches_shipped": 0,
  "human_escalations": 0,
  "pipeline_stall_days": 0,
  "portfolio_freshness_score_pct": 0.0,
  "top_patched_skills": [],
  "stale_skills": [],
  "protected_skills_patched": 0,
  "candidate_quality_breakdown": {
    "trivial": 0,
    "low": 0,
    "medium": 0,
    "high": 0
  },
  "product_strategist_notes": ""
}
```

## Health Thresholds

- **Green:** `candidates_generated ≥ 21/week`, `patches_shipped ≥ 7/week`, `human_escalations ≤ 2/week`, `pipeline_stall_days = 0`, `portfolio_freshness ≥ 80%`
- **Yellow:** `candidates_generated < 21/week` OR `pipeline_stall_days = 1` OR `portfolio_freshness 60-79%`
- **Red:** `pipeline_stall_days ≥ 2` OR `human_escalations > 5/week` OR `portfolio_freshness < 60%`
