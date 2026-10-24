# OpenClaw Database Schema Reference

This document provides reference information for querying the OpenClaw analytics database (`~/.sibling-agent/workspace/intel/agents/database/agents.db`).

## Key Tables

### agents
Contains information about all agents in the OpenClaw system.

**Important Columns:**
- `id` - Primary key
- `code` - Full agent code (e.g., RES-REV-NEU-L3-C3-P01-T2-001)
- `short_code` - Short reference (e.g., REV-NEU-001)
- `display_name` - Human-readable name (e.g., SINGULARITY, NEBULA)
- `domain` - High-level category (RES, ENG, MKT, OPS, FIN, LEG, CRE, PGM, EXE, BD, PER, GD, DS)
- `family` - Subcategory within domain (RSR, REV, ANL, WRT, DEV, DSN, MGR, SPC, LED, DIR, CHF, AST, DSP, QA)
- `specialty` - Further specialization (NEU, CON, PSY, 8DA, 8DH, etc.)
- `level` - Seniority level (1-7)
- `credential_tier` - Certification level (0-5)
- `personality_code` - Personality type code (P01, P02, etc.)
- `training_tier` - Training level (1-5)
- `role` - Position title (principal, Chief of Staff, etc.)
- `department` - Organizational department
- `world` - Operational world (Empire, DS, GD, Personal, etc.)
- `primary_model` - Default LLM used by agent
- `fallback_model` - Backup LLM
- `status` - Current status (active, inactive, archived, suspended)

### cron_jobs
Contains scheduled jobs and their execution history.

**Important Columns:**
- `id` - Primary key
- `job_id` - Unique identifier for the job
- `job_name` - Human-readable job name
- `agent_id` - Foreign key to agents.id (NULL if not agent-specific)
- `persona_id` - Foreign key to agent_personas.id (NULL if not persona-specific)
- `model` - LLM used for this job
- `status` - Current status (enabled, disabled, error, paused)
- `consecutive_errors` - Number of consecutive failed runs
- `success_rate` - Percentage of successful runs
- `last_run_at` - Timestamp of last execution
- `last_success_at` - Timestamp of last success
- `last_error_at` - Timestamp of last error
- `next_run_at` - Timestamp of next scheduled run

### agent_personas
Contains persona information that can be layered onto agents.

**Important Columns:**
- `id` - Primary key
- `code` - Persona code
- `display_name` - Human-readable persona name

## Common Query Patterns

### Get Active Agents with Their Models
```sql
SELECT a.display_name, a.domain, a.family, a.specialty, a.primary_model
FROM agents a
WHERE a.status = 'active'
ORDER BY a.display_name;
```

### Get Cron Jobs with Agent Information
```sql
SELECT c.job_name, a.display_name AS agent_name, c.model, c.status, c.consecutive_errors
FROM cron_jobs c
LEFT JOIN agents a ON c.agent_id = a.id
WHERE c.status != 'disabled'
ORDER BY c.consecutive_errors DESC;
```

### Get Error-Prone Cron Jobs
```sql
SELECT c.job_name, a.display_name AS agent_name, c.model, c.consecutive_errors
FROM cron_jobs c
LEFT JOIN agents a ON c.agent_id = a.id
WHERE c.status = 'error'
ORDER BY c.consecutive_errors DESC
LIMIT 20;
```

### Check for Jobs Missing Agent/Persona Associations
```sql
SELECT COUNT(*) as total_jobs,
       SUM(CASE WHEN agent_id IS NULL THEN 1 ELSE 0 END) as missing_agent,
       SUM(CASE WHEN persona_id IS NULL THEN 1 ELSE 0 END) as missing_persona
FROM cron_jobs
WHERE status != 'disabled';
```

## Important Notes

1. **Foreign Keys**: The `cron_jobs` table uses `agent_id` and `persona_id` as foreign keys to the `agents` and `agent_personas` tables respectively. These can be NULL for system-level jobs not tied to a specific agent or persona.

2. **Historical Data**: The analytics database contains historical records. For live system state, always verify with `sibling-agent cron list` before making changes (see `references/sibling-agent-cron-verification.md`).

3. **Model Information**: Agent default models are in `agents.primary_model`, but individual cron jobs may override this with their own `model` field.

4. **Status Values**: 
   - Agents: `active`, `inactive`, `archived`, `suspended`
   - Cron jobs: `enabled`, `disabled`, `error`, `paused`

5. **Performance**: For frequent queries, consider adding indexes on commonly filtered columns like `agents.status`, `cron_jobs.status`, and `cron_jobs.consecutive_errors`.

## Example: Daily Talent Review Queries

### Fleet Composition
```sql
SELECT 
    COUNT(*) as total_agents,
    SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) as active_agents
FROM agents;
```

### Model Distribution
```sql
SELECT 
    primary_model,
    COUNT(*) as count
FROM agents
WHERE status = 'active'
GROUP BY primary_model
ORDER BY count DESC;
```

### Personality Distribution
```sql
SELECT 
    personality_code,
    COUNT(*) as count
FROM agents
WHERE status = 'active' AND personality_code IS NOT NULL
GROUP BY personality_code
ORDER BY count DESC;
```