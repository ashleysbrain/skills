# Cron Fleet Health Scoring Reference

This document explains the health scoring algorithm used in cron fleet audits and provides guidance on interpreting scores.

## Health Scoring Algorithm

The fleet health score is calculated using a weighted deduplication model:

```
Health Score = 100 - (error_count × 10) - (overlap_count × 5) - (paused_count × 2) - (stale_count × 1)
```

Where:
- `error_count`: Number of jobs with last_status != 'ok'
- `overlap_count`: (Sum of job counts in all overlap groups) - (Number of overlap groups)
- `paused_count`: Number of jobs with state = 'paused'
- `stale_count`: Number of one-shot jobs (repeat='0/1') that have already run

The result is clamped to the range 0-100.

## Weighting Rationale

Different types of issues are assigned different weights based on their impact on fleet health and operational risk:

### Errors (Weight: 10)
- **High impact**: Erroring jobs indicate immediate problems that prevent the job from functioning correctly
- **Operational risk**: Errors may lead to missed critical tasks, data inconsistencies, or system failures
- **Urgent attention**: Requires immediate investigation and resolution

### Schedule Overlaps (Weight: 5 per extra job)
- **Medium impact**: Overlapping jobs contend for the same system resources (CPU, memory, API quotas, etc.)
- **Resource contention**: Can lead to performance degradation, timeouts, or failed executions
- **Planning issue**: Reflects suboptimal scheduling that could be improved with better coordination

### Paused Jobs (Weight: 2 each)
- **Low-Medium impact**: Paused jobs are intentionally stopped but may represent forgotten or neglected tasks
- **Opportunity cost**: Represent potential work that's not being done
- **Configuration drift**: May indicate outdated processes or changing requirements

### Stale One-Shot Jobs (Weight: 1 each)
- **Low impact**: Completed one-shot jobs that retain their definitions
- **Clutter**: Contributes to visual noise in job listings
- **Minimal risk**: Generally harmless but represents incomplete cleanup

## Score Interpretation

### 90-100: Excellent 🟢
- Fleet is in very good health
- Minimal issues requiring attention
- Regular maintenance is keeping things well-tuned
- Continue current practices with minor refinements

### 70-89: Good 🟡
- Fleet is generally healthy with some areas for improvement
- May have a few erroring jobs or scheduling inefficiencies
- Regular audit cadence is appropriate
- Focus on resolving the highest-weight issues first

### 50-69: Fair 🟠
- Fleet has notable issues that should be addressed
- Multiple erroring jobs or significant scheduling problems
- Consider increasing audit frequency temporarily
- Prioritize error resolution and schedule optimization

### 0-49: Poor 🔴
- Fleet requires immediate attention
- Multiple critical errors or systemic issues
- Consider emergency intervention to stabilize the fleet
- Review fundamental processes and configurations

## Trend Analysis
Health scores are most valuable when tracked over time. Consider:
- Recording scores in a time series to detect trends
- Setting target score ranges for different fleets based on their criticality
- Establishing alerts when scores drop below certain thresholds
- correlating score changes with specific events or changes

## Limitations
- The algorithm is a simplified model and may not capture all nuances of fleet health
- Weight values are based on operational experience and may need adjustment for specific contexts
- Does not account for job criticality (some jobs may be more important than others)
- Does not consider historical performance or trends in individual job reliability

## Customization
Organizations may want to adjust the weighting based on their specific priorities:
- Increase error weight if reliability is paramount
- Increase overlap weight if resource contention is a major concern
- Decrease paused job weight if intentional pausing is common and expected
- Add additional factors such as job duration trends or success rates over time

## Related Metrics
Consider supplementing health score with:
- Mean time between failures (MTBF) for critical jobs
- Average job execution time trends
- Success rate over sliding windows
- Resource utilization during job execution windows
- Alert fatigue metrics (frequency of notifications from cron jobs)