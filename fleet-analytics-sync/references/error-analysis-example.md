# Sample Error Analysis Output

This is a representative sample of the output from running `python3 fleet_analytics.py errors`.

```
============================================================
ERROR ANALYSIS
============================================================

By error type:
  model_not_found: 38673
  auth: 35113
  unknown: 35064
  timeout: 2728
  rate_limit: 518
  unknown: 4

Most error-prone jobs:
  Friday Leadership Huddle: 1024 errors
  Weekly Fleet Report: 1024 errors
  AURORA Product Radar: 1024 errors
  Thursday Tech Architecture: 1024 errors
  AISHA Friday Financial Check-In: 1024 errors
  PULSE Process Freshness Check: 1013 errors
  GENESIS Phase 6: MORNING BRIEF: 1006 errors
  PULSE Weekly Deep Review: 995 errors
  Weekly Skill Updates: 991 errors
  SINGULARITY Morning Brief: 990 errors
  ATLAS-R2P: Daily Research-to-Product Updates: 990 errors
  agent-lnd-trainer: 990 errors
  Divinity Science Weekly Newsletter: 986 errors
  GENERAL COUNSEL Legal Scan: 982 errors
  AURORA Product Pulse: 982 errors

Recent errors (last 48h):
  [2026-05-31T20:21] Talent Sprint - Phase 1 (Empire C-Suite) — timeout: timeout
  [2026-05-31T12:50] AISHA Weekly Goal & Schedule Review — None: 
  [2026-05-31T12:50] AISHA Weekly Goal & Schedule Review — None: 
  [2026-05-31T12:50] AISHA Weekly Goal & Schedule Review — None: 
  [2026-05-31T12:50] AISHA Weekly Goal & Schedule Review — None: 
  [2026-05-31T12:50] AISHA Weekly Goal & Schedule Review — None: 
  [2026-05-31T12:50] AISHA Weekly Goal & Schedule Review — None: 
  [2026-05-31T12:50] AISHA Weekly Goal & Schedule Review — None: 
  [2026-05-31T12:50] AISHA Weekly Goal & Schedule Review — None: 
  [2026-05-31T12:50] AISHA Weekly Goal & Schedule Review — None: 
  [2026-05-31T11:42] panel-orchestrator-continuous — timeout: timeout
  [2026-05-31T11:42] panel-orchestrator-continuous — timeout: timeout
  [2026-05-31T11:42] panel-orchestrator-continuous — timeout: timeout
  [2026-05-31T11:42] panel-orchestrator-continuous — timeout: timeout
  [2026-05-31T11:42] panel-orchestrator-continuous — timeout: timeout
  [2026-05-31T11:42] panel-orchestrator-continuous — timeout: timeout
  [2026-05-31T11:42] panel-orchestrator-continuous — timeout: timeout
  [2026-05-31T11:42] panel-orchestrator-continuous — timeout: timeout
  [2026-05-31T11:42] panel-orchestrator-continuous — timeout: timeout
  [2026-05-31T11:42] panel-orchestrator-continuous — timeout: timeout
  [2026-05-31T10:25] 8D360 Sunday Full Check-In + Weekly Review — None:
```

Key sections:
- **By error type**: Counts of each error category across all time.
- **Most error-prone jobs**: Top cron jobs by total error count.
- **Recent errors (last 48h)**: Timestamped errors from the last two days, showing job name, timestamp, error type, and error message.