---
name: fleet-master-profile-assembly
description: Coordinated multi-specialist assembly of master agent profiles — 17 sections across 56+ agents with specialist ownership, parallel fill, and monitoring
tags: [fleet, profiles, master-hr, forge, specialist-volley, monitoring, sibling-agent]
version: 1.0
---

# Fleet Master Profile Assembly

## When to Use

- Building or rebuilding master profiles for the entire agent fleet
- User says "fill out all sections" or "specialist agents need to own their sections"
- Any fleet-wide document assembly requiring multiple specialist agents to contribute sections
- MASTER-HR-TEMPLATE.md needs to be applied across all agents

## Fleet Size (Updated 2026-03-30)

The fleet is NOT 56 agents. Full roster from agents.db:
- **~59 core ops agents** — full 17-section MASTER-HR-TEMPLATE profiles
- **50 Dr. AI reviewers** — lighter VERITAS-REVIEWER-TEMPLATE profiles
- **49 Discipline AI reviewers** — lighter VERITAS-REVIEWER-TEMPLATE profiles
- **1 PEER-REVIEW orchestrator** (E-145) — manages the 99 reviewers
- **Total: ~159 agents** needing profiles of some kind
- **4 DB duplicates** to ignore: Cipher/CIPHER, Muse/MUSE, Sable/SABLE, Vesper/VESPER
- **~6 process docs** to exclude: TRAINING-PROGRAM, SKILL-GAP-ANALYSIS, etc.

Always query `agents.db` for the real count: `SELECT COUNT(DISTINCT display_name) FROM agents WHERE status='active';`

### Reviewer Naming Convention
All reviewers MUST have "AI" in their name. No human-sounding names like "Dr. Alexander Petrov" — must be "Dr. Alexander Petrov AI". Discipline reviewers: "Cognitive Science AI Reviewer". This was enforced 2026-03-30.

## Architecture

### The 17-Section Template

Location: `/<workspace>` (981 lines, 41KB)
Output: `/<workspace>[NAME]-profile.md`

### Section Ownership Map

| Section | Owner Agent | What They Fill |
|---------|------------|----------------|
| S1: Agent Overview | FORGE | Job codes, employee numbers, reporting, credentials tier |
| S2: Job Description | FORGE | Position summary, responsibilities, KPIs, tools |
| S3: Variation Registry | FORGE | 10-variation table from 10-variations file |
| S4: Variation Detailed Profiles | FORGE | V1-V10 full blocks (credentials, OCEAN, triggers, etc.) |
| S5: 8D Wellness Profile | VITALS | TWC scores, coupling matrix, composite scoring |
| S6: 8D Score History & Trends | METRICS | Rolling 90-day history, change log, state file integration |
| S7: Fleet Gap Analysis | SCOUT | Problem statement, capability map, unique value prop |
| S8: Team Compatibility Matrix | CATALYST | Agent-to-agent compatibility, best variation pairings |
| S9: Core Functions & Capacity | ARBITER | Function allocation percentages, variation-to-function mapping |
| S10: 30-Day Onboarding | CATALYST | Week 1-4 deliverables, status tracking |
| S11: Deployment Specification | FORGE | Model config, escalation triggers, comms protocols |
| S12: Journal System Integration | SENTINEL | Journal format, compliance, three query modes |
| S13: Version Tracking | FORGE | Version format, changelog, update locations |
| S14: Analytics Tracking | METRICS | Variation performance table, SQL schema, metrics targets |
| S15: Switching Protocol | FORGE | Switching table, rules, trigger detection |
| S16: Scientific Validation | HALO | Personality frameworks, task-personality research, measurement integrity |
| S17: Appendices | NEBULA | OCEAN reference, Enneagram, job code dimensions, related docs |

### Two-Phase Assembly

**Phase 1: FORGE (skeleton creation)**
- Creates all profile files with S1, S2, S3, S4, S11, S13, S15 filled with REAL data
- Other sections get headers + `[PENDING - OWNER_AGENT]` placeholders
- This MUST complete fully before Phase 2 starts

**Phase 2: Specialist Fill (parallel)**
- All 8 specialist agents run simultaneously
- Each reads existing profile, fills ONLY their section(s), writes back
- VITALS, METRICS, SCOUT, CATALYST, ARBITER, SENTINEL, HALO, NEBULA

## Batch Sizing (Learned 2026-03-30)

| Work Type | Agents per Subagent | Avg Output | Timeout Risk |
|-----------|--------------------|-----------:|:-------------|
| FORGE skeleton (7 sections) | 6 | ~37KB each | Low at 6, interrupted at 6+ with complex SOULs |
| Specialist fill (1-2 sections) | 10-14 | ~2-5KB added | Low |
| Full profile from scratch | 3-4 | ~40KB each | Medium |

**Key finding:** 6 agents per FORGE subagent is the sweet spot. Subagents writing ~220KB total (6 x 37KB) complete reliably in ~1200s. At 7+ complex agents, they hit the timeout wall around 580s but still produce 2-4 files before dying.

## Execution Playbook

### Phase 1: FORGE Skeleton

```python
# Split 56 agents into batches of 6
batches = [agents[i:i+6] for i in range(0, len(agents), 6)]

# Launch 3 parallel subagents at a time
for batch_group in [batches[i:i+3] for i in range(0, len(batches), 3)]:
    delegate_task(tasks=[
        {
            "goal": f"You are FORGE. Create MASTER PROFILE files for: {', '.join(batch)}...",
            "context": "Template at MASTER-HR-TEMPLATE.md. Fill S1,S2,S3,S4,S11,S13,S15...",
            "toolsets": ["terminal", "file"]
        }
        for batch in batch_group
    ])
    # VERIFY after each group
    verify_files_on_disk(batch_group)
    # RELAUNCH any missing immediately
```

### Verification After Every Batch (MANDATORY)

```python
import os
codes_dir = "/<workspace>"
profiles = {f.replace("-profile.md","") for f in os.listdir(codes_dir) if f.endswith("-profile.md")}
remaining = sorted(set(all_agents) - profiles)
print(f"Done: {len(profiles)}/{len(all_agents)} | Missing: {remaining}")
```

**NEVER report "done" without running this check.** Subagents that timeout still report "completed" in the summary — only file verification tells the truth.

### Phase 2: Specialist Fill

Each specialist gets a batch of profiles to update. They read the existing file, find their `[PENDING]` section, replace it with real data, and write back.

```python
# Example: VITALS filling S5 for all 56 agents
delegate_task(tasks=[
    {
        "goal": "You are VITALS. Fill Section 5 (8D Wellness Profile) in these profile files...",
        "context": "Read each -profile.md, find [PENDING - VITALS], replace with real 8D data from agents.db...",
        "toolsets": ["terminal", "file"]
    }
    # Split into batches of 14 for specialist work (lighter per-agent)
])
```

### Data Sources Per Specialist

### Single-Agent Brain Creation (DB-Backed)

Use the same template family when creating one new agent brain/persona pair, but keep the workflow tight:

1. Inspect the live roster first so the new sequence/code is consistent with the current max in the lane.
2. Confirm the schema constraints before insert — especially enum-backed fields like `decision_speed`.
3. Create or update the agent row, personality row, and persona rows together.
4. Write the matching `-profile.md` file using the 17-section template.
5. Verify with the live DB and the file on disk; do not trust the write summary alone.
6. If a DB insert fails on a CHECK constraint, resolve the enum/value mismatch before retrying.

Reference notes for the LATTICE session: `references/lattice-agent-brain-creation.md`.


| Specialist | Primary Data Source |
|-----------|-------------------|
| VITALS | `agents.db` wellness tables, `EVALUATION-PROTOCOL-v2.md` |
| METRICS | `agents.db` performance tables, cron run history |
| SCOUT | Fleet capability audit, SOUL.md cross-comparison |
| CATALYST | Org chart, collaboration patterns from cron jobs |
| ARBITER | Cron job assignments, task routing data |
| SENTINEL | `JOURNAL-ENFORCEMENT-SYSTEM.md`, compliance logs |
| HALO | `PERSONALITY-ARCHETYPES.md`, scientific framework docs |
| NEBULA | All reference docs, QA pass on entire profile |

### Current Fleet Audit Reference
- `references/fleet-profile-audit-2026-06-01.md` — concise audit of the live DB schema, profile counts, and 17-section completion check.

## SOUL File Locations (Gotchas)

Most agents: `/<workspace>[lowercase]/SOUL.md`

Exceptions:
- `AISHA-MD` → `agents/AISHA-MD.md` (standalone)
- `IP-SCRUBBER` → `agents/IP-SCRUBBER.md` (standalone uppercase)
- `SENTINEL` → `agents/SENTINEL.md` (standalone uppercase)
- `OBSIDIAN-ARCHITECT` → `agents/OBSIDIAN-ARCHITECT.md` (standalone)
- `NEXUS` → empty dir, real SOUL at `agents/_archived/binary/SOUL.md`
- `CATALYST` → empty dir, no SOUL.md exists (build from 10-variations)
- `NEBULA` → no SOUL.md (build from 10-variations)

## Monitoring Discipline (CRITICAL — the principal called this out 2026-03-30)

the principal asked AISHA to monitor an overnight talent sprint. AISHA set up a dashboard and cron but **never verified outputs landed**. 7 agents' work was lost because batch 5 timed out and nobody relaunched. the principal had to discover this herself the next morning. This is unacceptable.

1. **After EVERY batch of subagents returns:** Run file verification on disk — not just read the summary
2. **If any file missing:** Relaunch IMMEDIATELY without asking user
3. **Track progress in coordination file:** Update SPRINT-COORDINATION.md after every batch
4. **Cross-system check:** Verify OpenClaw cron jobs aren't duplicating the same work
5. **Don't trust "completed" status:** Subagents that timeout still report "completed" — only file verification tells the truth
6. **Overnight monitoring means ACTUAL monitoring:** If user asks you to watch a sprint, you must verify deliverables at each checkpoint, not just set up a dashboard and walk away
7. **If a subagent times out, RELAUNCH IMMEDIATELY** — never wait for user to notice

### Two Profile Templates

| Agent Type | Template | Sections | Location |
|-----------|----------|----------|----------|
| Core ops (C-suite, directors, specialists) | MASTER-HR-TEMPLATE.md | 17 sections | `intel/agents/codes/[NAME]-profile.md` |
| VERITAS reviewers (Dr. AI + Discipline AI) | VERITAS-REVIEWER-TEMPLATE.md | 10 sections (lighter) | `intel/agents/codes/[NAME]-reviewer-profile.md` |

The VERITAS template covers: identity, credentials, personality, review style, performance history, coverage map, panel history, collaboration, deployment, changelog. No 10-variation system, no 8D wellness, no switching protocol.

### PDF Generation

**ONLY use:** `~/.sibling-agent/workspace/output/generate-profile-pdf.py`
Reads CSS from `output/master-hr-template.html`. the principal confirmed "Yessssss this is the template" 2026-03-30.

```bash
python3 ~/.sibling-agent/workspace/output/generate-profile-pdf.py \
    ~/.sibling-agent/workspace/intel/agents/codes/[NAME]-profile.md \
    /tmp/[NAME]-profile.pdf
```

**the principal rejected 5 other approaches (2026-03-30):** fpdf2 md-to-pdf.py, custom weasyprint generate-agent-profile-pdf.py, md-to-pdf npm + adhd-pdf.css, md-to-pdf npm + Qubit Brand V3.0 CSS, generate-profiles.py (old weasyprint). All wrong design/format.

### Content Quality Issues Found (2026-03-30)

FORGE wrote S2 and S4 with problems the principal flagged:
- **S2 Job Description too agent-specific** — should be general role-level info (what the ROLE does, not what this specific agent instance does). Needs rewrite.
- **S4 task lists too thin** — each persona only got 3-5 triggers and 3-5 "best for" items. the principal wants comprehensive potential task lists for ALL 10 personas. "Not just a handful."
- **Who wrote it matters** — the principal asked "Who wrote the job description section?" Track section authorship so you can route corrections to the right agent.

## Critical Lessons from 2026-03-30 Sprint

1. **Monitor overnight work or it fails silently.** the principal asked AISHA to monitor overnight profile batches. AISHA set up a dashboard but didn't verify outputs landed. 7 agents' work was lost to timeouts and nobody caught it until the principal asked. When told to monitor, actually CHECK that files exist on disk after each batch.

2. **The fleet is bigger than you think.** Initial count was 56 agents. Actual count: 147 (59 core ops + 88 VERITAS reviewers + PEER-REVIEW). Always query the database AND scan disk AND check cron jobs to get the real number. Don't assume your initial list is complete.

3. **Specialist agents own their sections — don't do it yourself.** the principal explicitly said "Volley this to the talent team and around to appropriate agents to complete this. It isn't supposed to be done by you." File talent requests, route through FORGE+ARBITER, let the specialist agents fill their owned sections.

4. **S2 Job Description must be GENERAL.** "The job description needs to reflect general information and not agent specific data." FORGE wrote S2 too narrowly with agent-specific details instead of role-level descriptions.

5. **S4 needs COMPREHENSIVE task lists.** "All agents need potential tasks for all 10 personas. Not just a handful." Each persona variation needs a full list of potential tasks, not 3-5 bullet points.

6. **Agent scope boundaries are strict.** AISHA-MD was written with fleet responsibilities (validating all agent scores, fleet-wide data layer). the principal corrected: "AISHA-MD is for my health and wellness only." Always verify profile content matches the agent's actual scope.

7. **Batch size: 6 agents per subagent for profile creation, 20 for section fills.** Larger batches timeout. Section fills (patching existing profiles) can handle more agents per batch than full profile creation.

8. **Rate limits will hit during large sprints.** Building 59 profiles burned through Opus rate limits. Plan for model rotation or stagger work across time.

## Pitfalls

1. **Subagent says "completed" but wrote 4/6 files** — always verify on disk
2. **Agents without SOUL.md** — build from 10-variations file or other workspace references
3. **Duplicate work with OpenClaw** — check if cron jobs are already building profiles
4. **Phase 2 before Phase 1 done** — specialists need the skeleton to exist first
5. **Generic placeholder data** — each agent's S1-S4 must use REAL data from their SOUL, not template defaults
6. **10-variations files don't exist for all agents** — 16 agents had no 10-var file; FORGE must synthesize variations from SOUL data
7. **File size variance** — simple agents (SENTINEL, VITALS) produce 20-25KB profiles; complex agents (HERA, AISHA-MD) hit 45KB+. Both are fine.
8. **Fleet size assumption is ALWAYS wrong** — we assumed 56 agents initially; actual count is 159 (59 core + 100 reviewers). Always query DB first: `SELECT COUNT(DISTINCT display_name) FROM agents WHERE status='active'`
9. **S2 Job Description must be role-general, not agent-specific** — FORGE tends to write overly specific job descriptions. The JD should describe what the ROLE does generically, not recite the individual agent's SOUL back.
10. **S4 task lists are too thin** — FORGE only generates 3-5 triggers and 3-5 "best for" per persona. the principal wants COMPREHENSIVE potential task lists for all 10 personas. Expand significantly.
11. **PEER-REVIEW agent (E-145) is the panel orchestrator** — owns the entire VERITAS review panel lifecycle (brief, coordinate, debrief, post-mortem). Created 2026-03-30 because the role was referenced in docs but never built.
12. **Reviewer names must contain "AI"** — never use plain human names for AI reviewers. "Dr. Alexander Petrov" → "Dr. Alexander Petrov AI"
13. **Agent role boundaries are STRICT** — AISHA-MD is ONLY for the principal's personal health. She is NOT responsible for fleet wellness, agent scoring, or organizational metrics (that's AISHA/the operator agent). AISHA-MD convenes panels with research agents (HALO, DARK-MATTER, AURORA) to triple-check science/math before making health decisions. the principal corrected FORGE's S2 for blurring this boundary on 2026-03-30.
14. **Profile content requires domain review** — FORGE writes S2/S4 from SOUL data but doesn't understand role boundaries between agents. Always have the principal or the relevant supervisor review job descriptions before considering them final. The S2 for any agent that shares responsibilities with another agent (like AISHA vs AISHA-MD) needs explicit boundary statements about what's IN and OUT of scope.

## Rate Limit Management (Learned 2026-03-30)

After heavy Opus usage (59 profile builds = ~3M input tokens), Opus hits HTTP 429 rate limits. When this happens:
- **Switch models immediately** — don't retry Opus. Use Sonnet for the next batch.
- **the principal interprets retrying as "not working"** — she asked "Are you working yet?" when subagents kept failing on 429s
- **Plan model diversity upfront** for multi-hour sprints: Opus for complex work (FORGE profiles), Sonnet for medium work (specialist fills, security audits), Haiku for light work (verification, status checks)
- **Security audits specifically**: the principal wants "different models for different perspectives" — this is both a quality measure and practical rate limit avoidance

## AISHA-MD Panel Collaboration Pattern (Learned 2026-03-30)

When the principal asked AISHA-MD to plan a scheduling system, the correct process was:
1. AISHA-MD does initial research and drafts plan
2. Files talent requests for specialist agents through proper gate
3. Specialists (HALO, DARK-MATTER, PULSAR) each review/supplement in parallel
4. AISHA-MD synthesizes ALL inputs into final document
5. PDF generated for the principal's review
6. PLAN ONLY until the principal approves

This multi-agent panel pattern applies to any complex project:
- Lead agent does initial work
- Files talent requests for specialists
- Specialists contribute their expertise (verify citations, supplement research, design architecture)
- Lead agent compiles the final deliverable
- the principal reviews before implementation

**Key: The final document must incorporate ALL specialist feedback, not just the lead agent's work.** the principal specifically said "I want to see the full plan after she has collaborated with the other agents."

## Non-Profile PDF Generation

`generate-profile-pdf.py` ONLY works for agent profile markdown (it parses profile metadata). For general documents (plans, reports, research summaries), it strips content to ~6KB.

For non-profile documents use `md-to-pdf` npm with extracted master template CSS:
```bash
md-to-pdf DOCUMENT.md \
    --stylesheet ~/.sibling-agent/workspace/output/plan-styles.css \
    --pdf-options '{"format":"A4","margin":{"top":"1.5cm","bottom":"1.5cm","left":"1.5cm","right":"1.5cm"},"printBackground":true}'
```

## Success Criteria

- [ ] All intended core-op `-profile.md` files exist on disk
- [ ] Each core-op profile has all 17 `## Section N` headers
- [ ] FORGE sections (S1-S4, S11, S13, S15) have real data, not placeholders
- [ ] Specialist sections filled with real data (Phase 2)
- [ ] No `[PENDING]` markers remain after Phase 2
- [ ] Profile completeness is verified against both filesystem and DB schema
- [ ] `agents.db` includes the credential/persona tables needed for each profile
- [ ] Total fleet profile size remains substantial enough to reflect real content
