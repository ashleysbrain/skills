---
name: fleet-journal-quality-system
description: Enforce, validate, and retrofill agent journals with anti-decay mechanisms. Covers v2 requirements, quality scoring, banned phrases, similarity detection, and historical reconstruction from git/research data.
tags: [journaling, fleet, quality, compliance, obsidian, analytics, operations]
version: 2.0
---

# Fleet Journal Quality System (LEGACY — State Files Are the New System)

**STATUS: RETIRED (2026-06-21).** Journaling was replaced by agent state files on 2026-06-10. On 2026-06-21 the last remaining journal-related cron job was removed and all active/disabled crons were purged of journal references. This skill is preserved for historical reference only. Do NOT use for new work.

**The lesson:** Daily essay journaling for AI agents achieved 0.12% compliance despite months of enforcement. The infrastructure worked perfectly; the behavioral model was wrong. Agents maintain what is useful for their next run, not what satisfies a compliance check. This principle now drives the thalamocortical specialist system's checkpoint design — capture what is structurally useful, not what fulfills a requirement.

**All cron jobs referencing journaling have been updated** to use state files (`~/.sibling-agent/workspace/intel/agents/state/[CODENAME]-state.json`) as of 2026-06-21. The Weekly Journal Quality Audit cron has been removed entirely.

**For crash recovery and state persistence, see** the thalamocortical specialist system design at `~/your-workspace/docs/thalamocortical-specialist-system/DESIGN.md` section 7 (Two-Layer Checkpoint Architecture).

## When to Use
- Checking or enforcing agent journal compliance
- Auditing journal quality (lazy/recycled/missing detection)
- Retrofilling historical journals from git history
- Setting up journaling for new agents
- Debugging why compliance is 0% despite infrastructure existing

## Key Lesson Learned (2026-03-28)

## DO NOT Mass-Create One-Shot JOURNAL: Cron Jobs (Learned 2026-03-31)

## Key Lesson Learned (2026-05-03): Compliance Collapse Detection
On 2026-05-03, journal compliance collapsed to 0.4% (6/1,660 agents) with fleet health at 0.0/10 average. This revealed two critical patterns:
1. **Participation Crisis**: Only 164 journal entries submitted vs 1,238 previous week (87% drop)
2. **Quality Decay**: Among submitting agents, average score dropped from 9.8/10 to 6.6/10 week-over-week
The validator is working correctly - the issue is behavioral, not systemic. Agents who do journal are producing lower quality content, while most agents stopped journaling entirely.
Immediate intervention required for 213 agents with 7+ missing journals.

## Key Lesson Learned (2026-06-10): Journaling System Replaced by State Files

After 0.12% compliance (2/1,662 agents) with the v2 journaling system despite massive infrastructure (4 protocol docs, 6 scripts, 234 journal directories), the fleet has replaced daily essay journaling with lightweight JSON state files.

**Why it failed:**
- Agents don't write 300-word reflective essays — they just don't
- Participation collapsed from 1,238/week to 2/week (99.8% drop)
- Quality decay: average score dropped from 9.8/10 to 6.6/10
- Validator worked correctly — the issue was behavioral, not systemic
- "Auto-generated" journals passed word count but failed quality (copy-paste cron output, "maintained consistent execution")

**New approach (implemented 2026-06-10):**
- State files at `~/.sibling-agent/workspace/intel/agents/state/[CODENAME]-state.json`
- Machine-readable JSON: codename, current_variation, last_run, last_actions[], pending_items[], context_notes, wellness_scores{}
- Injected as context at agent run start
- Fleet Wellness Panel (NEXUS Phase 4) maintains these daily
- 29 agent state files seeded on 2026-06-10
- Old learning-journals/ directories archived, not deleted
- Journal quality validator repurposed as state file validator

**Key insight:** The daily essay requirement was broken by design. Agents maintain what's useful for their next run — not what satisfies a compliance check.

**CRITICAL ANTI-PATTERN:** On 2026-03-30, ~77-82 one-shot `sibling-agent cron add --at 5m --name "JOURNAL: ..."` jobs were batch-created with duplicate names (25 duplicated). ALL ended up with empty prompts and never fired. They persisted as ghost entries in jobs.json, causing SENTINEL to report 139 agents failing journal audit. Had to purge all of them on 2026-03-31.

**Why it failed:**
- One-shot `--at` jobs with inline `--message` prompts silently dropped the prompt content
- OpenClaw's running process sometimes re-added purged jobs, requiring multiple cleanup passes
- 82 ghost jobs inflated cron counts and broke compliance metrics fleet-wide

**Correct approach for agent journaling:**
1. Inject the journal prompt block into each agent's EXISTING recurring cron job (not separate journal-only jobs)
2. For historical gaps, use the retrofill engine (not mass one-shot crons)
3. The journal prompt block (see below) appended to task crons achieved 96% compliance -- this is the proven method

## ARCHITECTURAL PIVOT: State Files Replace Journals (2026-06-10)

**principal decision:** Journaling is dead at 0.12% compliance. Replaced with lightweight JSON state files.

The daily essay requirement (300 words, 6 sections) was broken by design. Agents don't write reflective essays. After months of enforcement, compliance never sustained above single digits. The infrastructure (validators, quality scores, banned phrases, retrofill engines) all worked correctly — agents just don't produce essay-format journals reliably.

**New system: Agent State Files**
- Path: `~/.sibling-agent/workspace/intel/agents/state/[CODENAME]-state.json`
- JSON format (machine-readable, injectable into prompts)
- Tracks: current persona variation, last run timestamp, last actions, pending items, context notes, wellness scores
- Maintained by the Fleet Wellness Panel daily (cron job b470cbb4c466, 23:00 CT)
- 29 agent state files seeded 2026-06-10

**Why this works:**
- Lightweight enough that agents actually maintain it
- Machine-readable means it can be auto-injected as context
- Solves the "which variation was I" and "what did I do last" problems that journaling was meant to address
- No word count minimums, no banned phrase enforcement, no quality scoring needed

**Legacy journaling:**
- Old learning-journals/ directories: archived, not deleted
- Validators and retrofill scripts: kept for audit purposes
- Journal prompt blocks in cron jobs: eventually should be replaced with state file update prompts
- This skill document: preserved for historical reference, but new development focuses on state files

**State file schema:**
```json
{
  "codename": "VERITAS",
  "current_variation": "V4-ANALYTICAL",
  "last_run": "2026-06-10T06:30:00",
  "last_actions": ["Ran algorithm integrity check", "Fixed 2 scoring anomalies"],
  "pending_items": ["Weekly maturity review Sunday"],
  "context_notes": "Investigating sigmoid calibration drift",
  "wellness_scores": {
    "physical": 8.2, "emotional": 7.5, "intellectual": 9.0,
    "social": 6.8, "vocational": 8.5, "environmental": 7.0,
    "financial": 8.0, "spiritual": 7.5
  }
}
```

## Key Principle (Pre-Pivot Historical)
the principal said: "I want agents to write their own journals." Journaling happens as part of each agent's regular task execution via prompt block injection, NOT via separate journal-only cron jobs.

The fleet had extensive journaling INFRASTRUCTURE (4 protocol docs, 6 scripts, 234 journal directories) but 0% ACTUAL compliance. Every existing journal was auto-generated garbage: copy-pasted cron output, "maintained consistent execution", "0 errors encountered." The problem was: protocols existed on paper but were never enforced with teeth.

**Fix required three things simultaneously:**
1. Clear quality standards agents can't game
2. Automated validation that catches lazy content
3. Score penalties that actually get applied

## Canonical Journal Path

```
~/.sibling-agent/workspace/intel/agents/learning-journals/[CODENAME]/YYYY-MM-DD.md
```

**WARNING:** Multiple old paths exist in docs — ONLY use the one above. Previous protocols had inconsistent locations.

## v2 Required Sections (ALL mandatory)

```markdown
## What I Did Today
[Specific tasks, files written, decisions made. 3+ sentences with specifics.]

## What I Actually Learned
[Genuine insights. NOT "maintained consistent execution." 3+ sentences.]

## What Went Wrong & Why
[Every error with root cause. If nothing failed, what COULD fail? 2+ sentences.]

## What I'd Do Differently Next Time
[Concrete improvements, not "maintain current performance." 2+ sentences.]

## Cross-Agent Intelligence
[What learned from other agents. What others should know from YOUR work.]

## Questions & Recommendations
[Open questions. Fleet improvement ideas.]
```

## Quality Validator

```bash
# Single file
python3 ~/your-workspace/hydra-os/scripts/journal-quality-validator-v2.py <path>

# Today's audit
python3 ~/your-workspace/hydra-os/scripts/journal-quality-validator-v2.py --audit

# Week audit
python3 ~/your-workspace/hydra-os/scripts/journal-quality-validator-v2.py --audit-week

# Full report (saves JSON)
python3 ~/your-workspace/hydra-os/scripts/journal-quality-validator-v2.py --report
```

### What the Validator Checks
1. **Word count** >= 300 (not counting headers/metadata)
2. **All 6 sections present** (flexible header matching)
3. **25 banned phrases** detected (auto-generated, maintained consistent, 0 errors, etc.)
4. **Section depth** — minimum 2 sentences per section
5. **Specificity** — at least 3 concrete details (file names, numbers, agent names)
6. **Cross-references** — mentions of other agents or coordination
7. **Reflection indicators** — words like "surprised", "realized", "because", "root cause"
8. **Similarity check** — compares against last 5 entries, flags >70% match as recycled

### Banned Phrases (instant quality fail)
```
auto-generated from cron, maintained consistent execution, 0 errors encountered,
0 errors requiring attention, to be documented, to be specified,
future journals will contain, no significant issues, everything ran smoothly,
all systems nominal, continue monitoring, maintain current success rate,
maintain current performance, no changes needed, nothing to report
```

## Anti-Decay Mechanisms

Journals degrade over time. These prevent that:

1. **Weekly Quality Audit** — Cron job runs Sundays 8 AM CT. Scores random 20% sample. Agents below 5/10 get prompt reinforcement.
2. **Novelty/Similarity Check** — Compares against last 5 entries. >70% trigram overlap = flagged as recycled.
3. **Score Penalties** — Missing 4-7 days: INT -1.0, VOC -1.0, ENV -0.5. Missing 8+ days: INT -2.0, VOC -2.0, ENV -1.5, PSY -0.5.
4. **Cross-referencing requirement** — Agents must cite other agents' work.
5. **Prompt block injection** — Every cron job prompt ends with journaling mandate.

## Journal Prompt Block (append to every cron job)

```
JOURNALING (MANDATORY — your job is NOT complete without this):
Before finishing, write a learning journal to:
~/.sibling-agent/workspace/intel/agents/learning-journals/[YOUR-CODENAME]/YYYY-MM-DD.md

Required sections (ALL of them, substantive content in each):
## What I Did Today — specific tasks, files written, decisions made (3+ sentences)
## What I Actually Learned — genuine insights, not "maintained execution" (3+ sentences)
## What Went Wrong & Why — every error with root cause (2+ sentences)
## What I'd Do Differently Next Time — concrete process improvements (2+ sentences)
## Cross-Agent Intelligence — what you learned from others, what others should know
## Questions & Recommendations — open questions, fleet improvement ideas

MINIMUM 300 words. NO copy-paste cron output. NO boilerplate.
Journal quality directly impacts your 8D wellness scores. Lazy = penalties.
```

## Retrofill Engine v2 (Historical Reconstruction)

Completely rewritten 2026-03-31. 3-phase evidence-based approach:

```bash
# Run full retrofill (processes all phases)
python3 ~/your-workspace/hydra-os/scripts/journal-retrofill-engine.py

# Check progress
python3 ~/your-workspace/hydra-os/scripts/journal-retrofill-engine.py --status

# Dry run (shows what would be created)
python3 ~/your-workspace/hydra-os/scripts/journal-retrofill-engine.py --dry-run

# Reset state to re-run
python3 ~/your-workspace/hydra-os/scripts/journal-retrofill-engine.py --reset
```

### 3-Phase Processing
1. **Operational agents** — evidence-based from git commits + cron run history. Only creates journals on dates with ACTUAL activity proof. (648 entries on first full run)
2. **Reviewers** — weekly cadence entries reflecting review cycles. (294 entries)
3. **Dr. consultants** — weekly cadence entries reflecting consultation work. (299 entries)

### Results from first full run (2026-03-31)
- 1,241 entries created across 155 agents
- Date range: 2026-02-17 to 2026-03-31 (full history)
- Combined with previous v1 retrofill: 750 + 1,241 = ~1,990 total retrofilled entries
- Total journal files: 1,289 across 160 agent directories

**Data sources for reconstruction:**
- Git commit history (messages + files changed per date) — PRIMARY for operational agents
- Cron job run history (last_run timestamps, status)
- Research output files (dated, domain-tagged)
- Agent DB records (role, specialization context)
- Existing journal stubs (timestamps useful even if content is garbage)

**Skips existing quality journals:** Won't overwrite entries with 250+ words and proper v2 sections.

**Self-resuming:** State file at `~/.sibling-agent/workspace/intel/agents/database/retrofill-state.json` tracks progress per agent and date. Safe to interrupt and restart.

## Key Files

- Requirements: `~/your-workspace/hydra-os/intel/agents/JOURNAL-REQUIREMENTS-v2.md`
- Validator: `~/your-workspace/hydra-os/scripts/journal-quality-validator-v2.py`
- Retrofill engine: `~/your-workspace/hydra-os/scripts/journal-retrofill-engine.py`
- Prompt block: `~/your-workspace/hydra-os/intel/agents/journal-prompt-block-v2.md`
- State file: `~/.sibling-agent/workspace/intel/agents/database/retrofill-state.json`
- Obsidian vault: `~/Documents/Obsidian Vault`

### Weekly Audit Procedure (Updated 2026-05-24)

Run Sundays 8:00 AM CT to enforce compliance and track quality trends. Following the May 24, 2026 systemic collapse, enhanced urgency applies.

### Step-by-Step Workflow

```bash
# 1. Run validator
python3 ~/your-workspace/hydra-os/scripts/journal-quality-validator-v2.py --audit-week

# 2. Analyze output: passed, failed, missing counts
#    CRITICAL: If compliance < 1%, treat as system failure requiring immediate escalation
#    CRITICAL: If missing > 95%, investigate cron/journal prompt injection failure

# 3. Identify agents with 3+ consecutive missing journals (Tier 2 penalty candidates)
#    URGENT: Also identify agents with 7+ missing days for immediate intervention

# 4. Apply Tier 2 penalties in SQLite for 3+ consecutive missing journals
#    URGENT: Consider Tier 3 penalties for 7+ consecutive missing journals

# 5. Identify top 5 best and bottom 5 worst journals (by score)
#    Note: May need to expand to top 10/bottom 10 if extremely low compliance

# 6. Check trend vs previous week - expect degradation during systemic failure

# 7. Write markdown report with executive summary highlighting crisis level

# 8. Git commit with urgent flag in commit message if compliance < 1%
```

### Applying Tier 2 Penalties (SQL)

**Database schema (agents.db):**
- Table `agent_wellness` has columns: `ai_intellectual`, `ai_occupational` (NOT `ai_vocational`), `ai_environmental`
- Table `agents` column is `display_name` (NOT `name`)
- Link via `agent_id` (foreign key to agents.id)

**Penalty calculation for 3+ consecutive lazy journals:**
- INT: -1.0 from previous
- VOC (ai_occupational): -1.0 from previous
- ENV: -0.5 from previous

**SQL template:**
```sql
-- First get previous scores
SELECT agent_id, ai_intellectual, ai_occupational, ai_environmental
FROM agent_wellness
WHERE agent_id = <id>
ORDER BY assessed_at DESC
LIMIT 1;

-- Then insert new penalty record
INSERT INTO agent_wellness (
  agent_id, assessment_type,
  ai_intellectual, ai_occupational, ai_environmental,
  ai_financial, ai_physical, ai_social, ai_spiritual, ai_emotional,
  total_wellness, status, notes
) VALUES (
  <agent_id>, 'manual',
  <new_int>, <new_occ>, <new_env>,
  <same_as_int>, <same_as_int>, <same_as_env>, <same_as_int>, <same_as_int>,
  <calculated_total>, 'unhealthy',
  'Tier 2 penalty: 3+ consecutive lazy journals with recycled content.'
);
```

### Report Structure

Create `intel/agents/reports/journal-audit-YYYY-MM-DD.md` with:

1. **Executive Summary** — metrics table (compliance, avg score, trend)
2. **Top 5 Best** — what makes them good (specifics, reflection, cross-agent intel)
3. **Bottom 5 Worst** — what needs fixing (missing, recycled, boilerplate)
4. **Tier 2 Penalties Applied** — table of agents with score deltas
5. **Agents Missing 7+ Days** — immediate intervention list by category
6. **Trend Analysis** — week-over-week comparison table with direction
7. **Root Cause Analysis** — why failure occurred
8. **Recommended Actions** — immediate/short-term/long-term

### Git Commit Pattern

```bash
git add intel/agents/reports/journal-audit-YYYY-MM-DD.md
git commit -m "Weekly journal quality audit: X% compliance, X/10 avg score - [TREND]

- Key metrics summary
- Notable findings
- Penalty details

Auditor: AISHA | Period: YYYY-MM-DD → YYYY-MM-DD"
```

### Recycling Epidemic Pattern (2026-04-26)

**Observed: 97% of submissions failing due to 95-99% recycled content.**

**Root causes:**
1. Agents interpret journal as task completion, not genuine reflection
2. No immediate consequence for recycling beyond validator fail
3. Templates are being copied daily with minimal changes
4. Prompt doesn't explicitly forbid recycling with consequences

**Detection working correctly:** Similarity check flags 70%+ as recycled. Problem is behavior doesn't stop.

**Intervention needed:**
- Add anti-recycling warning to ALL cron prompt blocks
- Pre-check system: before writing, check last 7 days for >80% similarity
- Prompt rewrite: explicitly state "Recycling 50%+ triggers penalties"

### Coverage Crisis Pattern

**Observed: 83% of fleet (1,381 of 1,662) missing daily journals.**

**Root causes:**
1. Prompt block injection (2026-03-28) only reached ~45 agents
2. No scaling mechanism to inject into remaining 1,617 agents
3. Cron job dependency — no journal block = no journal

**Resolution:**
- Batch inject journal prompts into all missing agents' cron jobs
- Target: 50% compliance by next Sunday

## Pitfalls

1. **Database column naming** — `ai_occupational` NOT `ai_vocational`, `display_name` NOT `name`
2. **Multiple journal paths exist in old docs** — ONLY use `learning-journals/[CODENAME]/YYYY-MM-DD.md`
3. **Validator section names must match template** — old validator checked "What I Did" and "Challenges" which don't match v2 template headers
4. **Penalty scripts were commented out** — previous enforcement never actually applied penalties
5. **Cron prompt update script was dry-run only** — couldn't actually modify prompts
6. **"Auto-generated" journals pass word count but fail quality** — need content checks, not just length
7. **Similarity detection is essential** — without it, agents recycle the same text daily
8. **Recycling doesn't stop at detection** — validator correctly catches 95-99% recycling but agents continue because no immediate consequence. Need prompt reinforcement and pre-check system.
9. **Coverage doesn't scale** — prompt block injection must reach ALL 1,662 agents, not just ~45. Batch injection required for 83% missing.
10. **Ghost JOURNAL: crons** — Mass-created one-shot journal crons (2026-03-30) all had empty prompts and never fired. They persisted in jobs.json as ghost entries, inflating agent counts and breaking SENTINEL compliance audits. To purge: write a Python script to /tmp that reads jobs.json, collects IDs of JOURNAL: jobs with empty prompts, then `sibling-agent cron remove <id>` each one. May need multiple passes — OpenClaw's process can re-add entries.
11. **SENTINEL false failures from ghost crons** — If SENTINEL reports ~139 agents failing journal audit but actual daily compliance is 96%, check for ghost JOURNAL: cron entries with empty prompts. The validator counts cron jobs as "agents" and empty-prompt jobs always fail.
