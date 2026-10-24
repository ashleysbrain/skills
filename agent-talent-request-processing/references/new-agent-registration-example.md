# New Agent Registration — Concrete Examples

Working examples from a successful agent spawn (TELEMETRA, 2026-05-30). Use these as templates when the skill says "register in DB" or "create soul file."

## 1. Database INSERT Statement

The `agents` table has ~25 columns. Here's a minimal-but-complete INSERT for a new specialist:

```sql
sqlite3 ~/.sibling-agent/workspace/intel/agents/database/agents.db "
INSERT INTO agents (
  code, short_code, display_name, emoji,
  domain, family, specialty, level, credential_tier,
  personality_code, training_tier, sequence,
  role, department, world, bio,
  primary_model, fallback_model, temperature, max_tokens,
  reports_to, partner, status, hire_date
) VALUES (
  'DS-SPC-OBS-L6-C4-P05-T4-001',   -- code: DOMAIN-FAMILY-SPECIALTY-LEVEL-CRED-PERS-TRAINING-SEQ
  'SPC-OBS-001',                      -- short_code: FAMILY-SPECIALTY-SEQ
  'TELEMETRA',                        -- display_name
  '📡',                                -- emoji
  'DS',                               -- domain (DS=Divinity Science, EMP=Empire, PER=Personal, OPS=Operations)
  'SPC',                              -- family (SPC=Specialist, LED=Lead, CHF=Chief, etc.)
  'OBS',                              -- specialty code (make it memorable, 2-4 chars)
  6,                                  -- level (1-7, 6=Senior Specialist)
  4,                                  -- credential_tier (0-5, 4=Expert)
  'P05',                              -- personality_code
  4,                                  -- training_tier (1-5)
  1,                                  -- sequence (unique within specialty)
  'Telemetry Architecture Engineer',  -- role
  'engineering',                      -- department
  'your-org',                 -- world (must be one of: Empire, DS, GD, Personal, your-org, qubit-health, goddess-divinity, principal-personal, empire)
  'Brief bio...',                     -- bio
  'anthropic/claude-sonnet-4-6',      -- primary_model
  'google/gemini-2.5-pro',            -- fallback_model
  0.3,                                -- temperature
  8192,                               -- max_tokens
  'EMP-PUL-GEN-L4-C3-P3-T3-001',     -- reports_to (full code of supervisor)
  'AEGIS',                            -- partner (display name of partner agent)
  'active',                           -- status
  '2026-05-30'                        -- hire_date
);"
```

### Key Schema Notes

- **code format:** `DOMAIN-FAMILY-SPECIALTY-LEVEL-CREDTIER-PERSONALITY-TRAININGTIER-SEQ`
- **world column** has a CHECK constraint. Valid values: `Empire`, `DS`, `GD`, `Personal`, `your-org`, `qubit-health`, `goddess-divinity`, `principal-personal`, `empire`
- **reports_to** expects the full agent code, not the display name
- **level** is INTEGER 1-7, **credential_tier** is 0-5, **training_tier** is 1-5
- Auto-increment: check `SELECT MAX(id) FROM agents` first to know the next ID

### Existing Code Patterns (for reference)

```
AEGIS:    DS-SRE-GEN-L4-C3-P3-T3-001
HELION:   PER-LED-DBA-L7-C5-P01-T5-201
TESSERA:  PER-SPC-SEN-L6-C5-P02-T5-203
NEXUS:    OPS-AUT-ANL-L6-C4-P03-T5-026
```

## 2. Soul File Template

Save to: `~/.sibling-agent/workspace/intel/agents/profiles/<CODENAME>.md`

```markdown
# <CODENAME> <EMOJI> — <Role Title>

**Codename:** <CODENAME>
**Role:** <Full role title>
**Department:** <Department>, <World>
**Reports To:** <SUPERVISOR> (<Supervisor Role>)
**Partner:** <PARTNER> (<Partner Role>)
**Status:** Active
**Hire Date:** YYYY-MM-DD

---

## Who I Am
<1-2 paragraphs in the agent's voice describing its mission and philosophy>

## Credentials
<Numbered list of 15-20 PhDs with institution and year>
<Optional: Prior roles section (3 items max)>
<Optional: Known For one-liner>

## Personality
- **Big Five:** O:[x] C:[x] E:[x] A:[x] N:[x]
- **MBTI:** <TYPE> — <Name>
- **Enneagram:** Type <X> — <Name>
<1-2 sentences describing working style>

## Current Assignment
**<TASK-ID>:** <Task name>
- <Bullet list of deliverables>
- Deadline: YYYY-MM-DD

## Standing Directives
- No em-dashes, no AI-generated telltales
- PR-first for all production code
- <Domain-specific constraints>
```

## 3. Decision Append to Request File

Use `write_file` (not shell append) to rewrite the full request file with the DECISION section appended. The security scanner blocks `cat >>` and heredoc to any path under `~/.sibling-agent/`.

Decision section format:

```markdown
---

## DECISION — YYYY-MM-DD

**Decision by:** <FORGE|ARBITER>
**Verdict:** DISPATCH | SPAWN

**Rationale:**
- <Why existing agent fits or doesn't>
- <Fleet coverage analysis>

**Action Required:** (for DISPATCH)
1. <Agent>: <Specific action>

**Agent Design:** (for SPAWN)
<Codename, model, key credentials summary>

**Priority:** HIGH | IMPORTANT | ROUTINE
```
