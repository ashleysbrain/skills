---
name: AETHER principal Alert System
description: Autonomous system health monitoring and principal escalation protocol for distributed AI agent fleets
tags: [monitoring, cron, operations, health-check, autonomous]
version: 1.0.0
---

# AETHER principal Alert System

**Use when:** Running scheduled health checks for AI agent fleets, cron jobs, and infrastructure that should only escalate to principal when critical thresholds are breached.

**Pattern:** Silent monitoring (return `[SILENT]` when healthy) with structured escalation only for genuine emergencies.

---

## Critical Thresholds

Only escalate when ANY of these are true:

1. **Cron job failures:** ≥3 consecutive errors on enabled jobs
2. **Agent wellness degradation:** Any agent with composite_score < 0.4
3. **Infrastructure failures:** Gateway down, critical process failures
4. **Cost overruns:** >$500/hour spend detected
5. **Critical path blockers:** >1 hour delay on time-sensitive work
6. **Explicit urgent flags:** Reports tagged "FOR ASHLEY" + "URGENT" (not just "FOR ASHLEY")

---

## Health Data Sources

### 1. Cron Job Health
```bash
# Location varies by system
~/.sibling-agent/cron/jobs.json          # OpenClaw jobs (6000+ lines)
~/your-workspace/hydra-os/intel/devops/cron-health.json  # Health summary
```

**Key fields:**
- `enabled: true` — only check active jobs
- `state.consecutiveErrors` — critical at ≥3
- `state.lastStatus` — "ok" vs "error"

**Parsing gotcha:** Large jobs.json files may have encoding issues. Use fallback regex:
```bash
grep -o '"consecutiveErrors": [0-9]*' jobs.json | grep -v '"consecutiveErrors": 0'
```

### 2. Agent Fleet Health
```bash
~/your-workspace/hydra-os/intel/agents/fleet-health/YYYY-MM-DD-HH.json
```

**Key fields:**
- `fleet_summary.flagged_below_7` — count of degraded agents
- `agents[].enabled` — ignore disabled agents
- `agents[].composite_health` — critical below 0.4, warning below 7.0

**Important:** Disabled agents often show low health (expected). Only flag enabled agents.

### 3. Overnight Operation Logs
```bash
~/your-workspace/hydra-os/intel/agents/OVERNIGHT-CHANGELOG-YYYY-MM-DD.md
```

**Scan for:**
- Error patterns at end of file
- "CRITICAL" + agent name (not just docs/examples)
- Consecutive error mentions with specific agent names

### 4. Infrastructure Status
```bash
ps aux | grep -iE "python.*gateway|hermes.*gateway"
```

Gateway should be running. High CPU (200-400%) is normal for multi-threaded message processing.

---

## Escalation Format

### When Healthy
```
[SILENT]
```

Optional: Add brief internal note after `[SILENT]` (saved locally, not delivered):
```
[SILENT] All systems nominal. Fleet health 8.4/10, 0 critical cron errors, overnight sprint completed successfully.
```

### When Critical Issue Found
```
---
🚨 principal ALERT - IMMEDIATE ATTENTION REQUIRED

**ISSUE:** [One-sentence summary]

**IMPACT:** [What this affects / Why it matters]

**WHAT AETHER IS DOING:** [Actions taken so far]

**REQUIRES YOUR DECISION:**
[Specific question/choice if true, otherwise "None - monitoring and handling autonomously"]

**TIMELINE:** [How urgent - minutes/hours]

---
```

---

## Implementation Pattern

```python
# 1. Check cron jobs
grep -o '"consecutiveErrors": [0-9]*' ~/.sibling-agent/cron/jobs.json | \
  grep -v '"consecutiveErrors": 0' | \
  grep -E '"consecutiveErrors": [3-9]|[0-9]{2}'

# If found: CRITICAL - cron job failures

# 2. Check agent wellness (most recent fleet-health JSON)
cd ~/your-workspace/hydra-os/intel/agents/fleet-health
ls -t *.json | head -1  # Get latest
# Read and check: agents[] where enabled=true and composite_health < 0.4

# If found: CRITICAL - agent wellness degradation

# 3. Check overnight logs (today's OVERNIGHT-CHANGELOG)
tail -100 intel/agents/OVERNIGHT-CHANGELOG-$(date +%Y-%m-%d).md | \
  grep -iE "(error|failed|critical)" | grep -v "consecutiveErrors: 0"

# Review context - are these handled or ongoing?

# 4. Check infrastructure
ps aux | grep gateway
# Should see running process

# 5. Consolidate assessment
# If ALL checks pass → return "[SILENT]"
# If ANY threshold breached → structured alert
```

---

## Pitfalls

### Don't Flag These as Critical

- **Disabled agents with low health** — they're paused, not degraded
- **"FOR ASHLEY" tags in research drafts** — normal workflow artifacts (only escalate if also "URGENT")
- **1-2 consecutive errors on cron jobs** — normal transient failures (wait for 3+)
- **Old health snapshots** — check timestamps, use most recent data
- **Documentation mentions of "CRITICAL"** — distinguish code/docs from actual alerts

### JSON Parsing Failures

Large jobs.json files (6000+ lines) may have:
- Invalid Unicode surrogate pairs
- Control characters in embedded strings

**Fallback strategy:**
1. Try standard JSON parse
2. Try `json_parse()` helper (handles control chars)
3. Fall back to regex extraction: `"consecutiveErrors":\s*(\d+)`

### Silent vs Verbose Reporting

This pattern is for **scheduled autonomous monitoring** (every 10 minutes). User only sees output when something is wrong.

For one-time health checks or debugging, provide full status even when healthy.

---

## Example Successful Run

```
[SILENT] 2026-03-25 11:58 AM scan: Fleet health 8.4/10, 0 critical cron errors (15 jobs with 1 error, 3 with 2 errors - below threshold), overnight GENESIS sprint completed 141 agent optimizations, gateway running 17h uptime. Next scan in 10 min.
```

## Example Critical Alert

```
---
🚨 principal ALERT - IMMEDIATE ATTENTION REQUIRED

**ISSUE:** 5 critical cron jobs failing (HORIZON, DREAM-CYCLE, ATLAS, ORACLE, VITALS)

**IMPACT:** Research pipeline halted - no morning scans running, fleet health observer offline

**WHAT AETHER IS DOING:** Analyzing error logs, checking for API quota exhaustion, verifying credentials

**REQUIRES YOUR DECISION:**
Should I attempt automated recovery (restart jobs with exponential backoff) or wait for manual investigation?

**TIMELINE:** Research scans missed for 6+ hours - need decision within 30 minutes to preserve daily scan schedule

---
```

---

## Integration with AETHER Role

AETHER (principal monitoring agent) runs this every 10 minutes via cron. The `[SILENT]` pattern prevents notification spam while maintaining audit trail.

**Cron setup:**
```yaml
schedule: "*/10 * * * *"  # Every 10 minutes
deliver: telegram  # principal's primary channel
prompt: |
  [SYSTEM: If you have nothing new or noteworthy to report, respond with exactly "[SILENT]" ...]
  
  🚨 AETHER → principal URGENT ALERT
  
  Scan all systems for critical issues:
  1. OpenClaw job failures (>3 errors = critical)
  ...
```

The system instruction at the top enables silent operation while the rest defines what to check.
