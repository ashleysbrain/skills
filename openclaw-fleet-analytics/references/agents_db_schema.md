# agents.db Database Schema Reference

Quick reference for column names in OpenClaw agents database (`~/.sibling-agent/workspace/intel/agents/database/agents.db`).

Generated from: `sqlite3 agents.db ".schema [table_name]"`

---

## agents Table

Primary table for agent definitions and configuration.

**Key columns:**
- `id` - INTEGER PRIMARY KEY
- `code` - Full DS-ECS code (e.g., `RES-REV-NEU-L3-C3-P01-T2-001`)
- `display_name` - Human-readable name (e.g., `SINGULARITY`, `NEBULA`)
- `role` - Role description (e.g., `Chief Executive Officer`, `Reviewer`)
- `primary_model` - **NOTE: NOT `model`** - Model identifier (e.g., `anthropic/claude-sonnet-4-6`)
- `fallback_model` - Fallback model if primary fails
- `status` - Agent status: `active`, `inactive`, `archived`, `suspended`
- `domain` - DS-ECS domain code (RES, ENG, MKT, OPS, etc.)
- `family` - DS-ECS family code (RSR, REV, ANL, WRT, etc.)
- `specialty` - Domain specialty code
- `level` - Credential tier (1-7)
- `personality_code` - Shortened MBTI code (e.g., `P1`, `P2`)

**Common pitfalls:**
- ❌ `SELECT model FROM agents` → WRONG (no `model` column)
- ✅ `SELECT primary_model FROM agents` → CORRECT
- ❌ `SELECT personality_id` → Returns numeric ID
- ✅ Join with `personalities` table for human-readable personality descriptions

---

## cron_jobs Table

Cron job definitions and execution status.

**Key columns:**
- `id` - INTEGER PRIMARY KEY
- `job_id` - Unique job identifier (UUID)
- `job_name` - Human-readable job name
- `agent_id` - FK to agents table (may be NULL)
- `persona_id` - FK to agent_personas table (may be NULL)
- `model` - Model assigned to this job
- `provider` - Model provider (e.g., `openrouter`, `anthropic`)
- `status` - Job status: `enabled`, `disabled`, `error`, `paused`
- `enabled` - Boolean flag
- `consecutive_errors` - Count of consecutive failures
- `success_rate` - Success rate percentage (0-100)
- `avg_duration_seconds` - Average job duration
- `last_run_at` - Timestamp of last run
- `last_success_at` - Timestamp of last successful run
- `last_error_at` - Timestamp of last error
- `last_error_message` - **NOTE: NOT `last_error`** - Error message text
- `next_run_at` - Timestamp of next scheduled run

**Common pitfalls:**
- ❌ `SELECT last_error FROM cron_jobs` → WRONG (no `last_error` column)
- ✅ `SELECT last_error_message FROM cron_jobs` → CORRECT
- ❌ `SELECT task_complexity FROM cron_jobs` → WRONG (no such column exists)
- ⚠️  `agent_id` and `persona_id` are often NULL (jobs not linked to specific agent)

---

## agent_personas Table

Persona/runtime overlays for agents.

**Key columns:**
- `id` - INTEGER PRIMARY KEY
- `agent_id` - FK to agents table
- `persona_name` - Human-readable persona name
- `model` - Model for this persona
- `temperature` - Temperature setting
- `system_prompt_override` - Custom system prompt
- `status` - Persona status

---

## personalities Table

MBTI personality type definitions.

**Key columns:**
- `id` - INTEGER PRIMARY KEY
- `code` - **Zero-padded code (e.g., `P01`, `P02`)** - NOT shortened
- `name` - Personality type name (e.g., `INTJ - Architect`)
- `description` - Full personality description

**Critical join note:**
- `agents.personality_code` uses shortened codes: `P1`, `P2`, `P3`
- `personalities.code` uses zero-padded codes: `P01`, `P02`, `P03`
- **Normalize before joining:** Pad with zeros to three digits after 'P'
  - SQL: `SUBSTR(agents.personality_code || '00', 1, 3)` or similar logic

---

## cron_runs Table

Individual cron job execution records (runtime history).

**Key columns:**
- `id` - INTEGER PRIMARY KEY
- `job_id` - FK to cron_jobs
- `started_at` - Start timestamp
- `completed_at` - Completion timestamp
- `status` - Run status: `success`, `error`, `timeout`
- `error_type` - Type of error (timeout, auth_failure, script_error, etc.)
- `error_message` - Error message text
- `duration_seconds` - Job duration

---

## fleet_health_snapshots Table

Daily fleet health snapshots.

**Key columns:**
- `id` - INTEGER PRIMARY KEY
- `snapshot_date` - Date of snapshot
- `active_agents` - Count of active agents
- `total_agents` - Total agent count
- `journal_compliance_pct` - Journal compliance percentage (BUG: often shows 0.0%)
- `twc_score` - Total Well-being Circles score
- `avg_quality_score` - Average quality score

**Note:** This table may be empty. Sync output prints snapshot data but doesn't always persist.

---

## error_log Table

Agent session error records.

**Key columns:**
- `id` - INTEGER PRIMARY KEY
- `agent_id` - FK to agents table
- `error_message` - Error message text
- `occurred_at` - **NOTE: NOT `timestamp`** - When error occurred
- `error_type` - Type of error

**Common pitfalls:**
- ❌ `SELECT timestamp FROM error_log` → WRONG (no `timestamp` column)
- ✅ `SELECT occurred_at FROM error_log` → CORRECT

---

## Useful Sample Queries

```sql
-- Top erroring cron jobs by consecutive errors
SELECT job_name, model, status, consecutive_errors, last_error_message
FROM cron_jobs
WHERE status = 'error'
ORDER BY consecutive_errors DESC
LIMIT 20;

-- Model distribution across active agents
SELECT primary_model, COUNT(*) as count
FROM agents
WHERE status = 'active' AND primary_model IS NOT NULL
GROUP BY primary_model
ORDER BY count DESC;

-- Agent family distribution
SELECT family, COUNT(*) as count
FROM agents
WHERE status = 'active'
GROUP BY family
ORDER BY count DESC;

-- Cron jobs with NULL agent/persona links (potential config issue)
SELECT job_name, model, status, consecutive_errors
FROM cron_jobs
WHERE agent_id IS NULL OR persona_id IS NULL
ORDER BY consecutive_errors DESC
LIMIT 20;
```

---

**Last updated:** 2026-07-23
**Database path:** `~/.sibling-agent/workspace/intel/agents/database/agents.db`