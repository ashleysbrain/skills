---
name: state-file-system-compliance
description: Audit agent state files for staleness.
category: compliance
version: 1.0.0
---

# State File System Compliance Audit

Critical compliance check for agent state file maintenance. Detects when the OpenClaw fleet stops updating state tracking.

## Trigger

Run as part of the specialist engine daily compliance sweep. Also use when investigating fleet health issues.

## Purpose

Verify that agent state files are being updated regularly. State file staleness is a leading indicator of fleet health failures.

## Critical Finding from 2026-08-01 Audit

- **118 of 119 state files stale (48+ hours)** - 99.2% failure rate
- **Most files dated from 2026-06-10** - over 50 days old
- **State file system appears non-functional**
- **Only DS-Rio-Hortega-state.json was fresh** (updated during audit)
- **Implication:** OpenClaw fleet has stopped maintaining state tracking

## Pitfalls

**Fleet Timeout on Large Datasets**
- **Issue:** Reading all state files via `execute_code` hits the 300s timeout on fleets >50 agents (e.g., 119 state files).
- **Symptom:** Script terminates with `Script timed out after 300s and was killed`.
- **Fix:** Use shell commands (`ls -la`, `find`) to get file counts and modification times first. Use sampling (read first 10-20 files) to estimate JSON content patterns rather than reading all files.

**Modification Time vs. Schema Reality**
- **Issue:** Relying on file modification time (`mtime`) to detect staleness is incorrect for the standard agent state schema. Files may be recent (created during init) but contain stale data (`last_run=null`).
- **Symptom:** Audit reports 100% staleness despite fresh file timestamps.
- **Fix:** Always parse JSON content to check the `last_run` field.
- **Schema Pattern:** `{"codename": "...", "last_run": null, ...}` means "never run," not "stale."
- **Systemic Check:** If ALL state files have `last_run=null`, this indicates a systemic issue (agents not writing state on execution), not individual agent failure. Compare with agents using different schemas (e.g., the specialist engine) to verify the state writing mechanism works at all.

## Audit Procedure

**Location:** `/<workspace>*-state.json`

**Implementation Pattern (use execute_code - never pipe to interpreter):**
```python
import os
import json
from datetime import datetime, timedelta
from pathlib import Path

state_dir = Path('/<workspace>')
state_files = list(state_dir.glob('*-state.json'))
total_state_files = len(state_files)

# Get active agents from database
active_agents = run_sql("SELECT COUNT(*) FROM agents WHERE status='active'")

# Check for stale state files (48+ hours) - PARSE JSON CONTENT
stale_cutoff = datetime.now() - timedelta(hours=48)
stale_files = []
never_run_files = []

# Sampling strategy for large fleets (>50 agents) to avoid timeout
sample_size = min(20, len(state_files))
sample_files = state_files[:sample_size]

# Sample to determine systemic pattern
sample_never_run = 0
for sf in sample_files:
    try:
        with open(sf) as f:
            data = json.load(f)
        last_run = data.get("last_run")
        if last_run is None:
            sample_never_run += 1
    except:
        pass

# If sampling shows systemic pattern (all sampled have last_run=null),
# this is a systemic issue, not individual agent failure
estimated_never_run = (sample_never_run / sample_size) * len(state_files) if sample_size > 0 else 0

# Detailed check for small fleets, sampling for large fleets
if len(state_files) <= 50:
    for sf in state_files:
        try:
            with open(sf) as f:
                data = json.load(f)
            last_run_str = data.get("last_run")
            if last_run_str:
                last_run = datetime.fromisoformat(last_run_str)
                if last_run < stale_cutoff:
                    stale_files.append((sf.name, last_run))
            else:
                never_run_files.append((sf.name, "NEVER"))
        except:
            pass

# Calculate compliance score (active states only)
compliance_score = (len(state_files) - len(stale_files) - len(never_run_files)) / int(active_agents) * 100
```

## Compliance Score Calculation

`(fresh_agents / active_agents_in_db) * 100`

**Critical Pitfall:** Use active agents from DB as denominator, NOT total state files. Using state files as denominator yields impossible percentages.

## Escalation Thresholds

- **CRITICAL:** Compliance < 10%
- **HIGH:** Compliance < 50%
- **MODERATE:** Compliance < 75%

## Action Items When Critical

1. Investigate why agents are not updating state files
2. Verify state file update mechanism is functioning
3. Check if state update cron jobs are running
4. Consider automatic state file refresh for stale agents
5. Escalate to human operator immediately

## Historical Pattern

- **July 6, 2026:** 118/119 state files stale (386+ hours old)
- **August 1, 2026:** Same pattern - 118/119 stale, indicates persistent systemic failure

## Related Skills

This skill is a component of the broader the specialist engine compliance sweep. Related to:
- `compliance/sentinel-compliance-audit` (umbrella compliance audit)
- `sibling-agent-fleet-analytics-sync` (fleet health monitoring)

## Change Log

- **2026-08-01:** Initial skill creation based on critical finding of 99.2% state file staleness.
- **2026-08-03:** Updated audit procedure to parse JSON content instead of mtime. Added sampling strategy for fleets >50 agents. Added pitfall for systemic `last_run=null` detection.