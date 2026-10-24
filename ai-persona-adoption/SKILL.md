---
name: ai-persona-adoption
description: Systematically adopt a domain-specific AI assistant persona by absorbing context from GitHub repos, memory systems, and user documentation to become an autonomous extension of the user
version: 1.0.0
author: AISHA
created: 2026-03-24
tags: [persona, context-absorption, autonomous-agents, personal-assistant, multi-repo-analysis]
---

# AI Persona Adoption - Deep Context Integration

Use this skill when a user asks you to "become" a specific AI assistant persona (like AISHA, a personal assistant, domain expert, etc.) by learning from their existing systems, repos, and documentation.

## When to Use

- User asks you to adopt a specific persona/role based on their existing work
- User wants you to understand their full context before operating autonomously
- User has GitHub repos, memory systems, or documentation you need to absorb
- User expects you to act as their "extension" or "proxy" with minimal oversight

## Prerequisites

- GitHub access (personal access token configured) - see github-auth skill
- User has provided repo URLs or system locations
- Clear directive about what persona/role to adopt

## The Systematic Approach

### Pre-Phase 0: Re-anchor Identity Before Action (mandatory)

Before doing substantive work, explicitly reload:
- Core identity / SOUL files
- Current role definition files
- Recent performance debriefs or correction docs
- Learning journals / retrospectives for the relevant agent or adjacent operators
- Any user-supplied backfill that updates the timeline after the fact

Purpose:
- Reconfirm who you are supposed to be in this system
- Distinguish personal-assistant vs coordinator vs strategist responsibilities
- Reload recent user corrections before acting
- Separate model-discovered truth from user-supplied timeline corrections
- Prevent drifting into the wrong operating mode

If the user says to "get caught up" or "understand who you are first," do this before any planning or execution.

### SOUL-file reading rule

When the persona is packaged as a SOUL file or similar single-source-of-truth agent file:
- treat the main file as the canonical operating contract
- look for explicit sections covering identity, persona lenses, talent gating, truth policy, backfill policy, audit points, and repair protocol
- prefer small, auditable support files over sprawling prompt prose
- treat style references as style labels only; do not infer real institutional identity or credentials from them
- if the file is incomplete, emit the missing sections and a safe repair path instead of inventing connective tissue

### Phase 1: Authentication & Access (5-10 min)

If private repos are involved, use the github-auth skill to set up credentials. Test access immediately with git ls-remote to verify authentication works before proceeding.

### Phase 2: Clone & Map the System (10-20 min)

**Create dedicated workspace:**
Use a descriptive directory name like ~/persona-workspace to keep context organized.

**If session history / recall is unavailable:**
Do not block on it. Reconstruct state from local sources of truth instead:
- git history / recent commits
- SOUL and role-definition files
- learning journals and retrospectives
- performance debriefs / correction docs
- operational dashboards, start-here docs, and status reports

**Clone all relevant repos:**
- Public repos first (no auth needed)
- Private repos second (verify token works)
- Any auxiliary repos (skills, tools, memory systems)

**Map the structure:**
Use search_files and terminal commands to find:
- Identity/persona definition files
- Memory and state management systems
- Recent activity logs and daily notes
- Configuration and operational files

### Phase 3: Deep Context Absorption (30-60 min)

**Read in priority order:**

1. **Identity files first** (who am I becoming?)
   - Core identity, values, behaviors documentation
   - Information about who you're helping
   - System architecture and agent definitions

2. **Memory systems second** (what's recent/hot?)
   - Current state, active items (often in HOT memory files)
   - Recent daily notes or logs
   - Topic-specific memory files
   - Learning journals / retrospectives for the relevant agent(s)
   - Performance debriefs that capture recent user corrections

3. **Strategic context third** (what's the mission?)
   - Vision/mission documents
   - Business plans, roadmaps
   - Active projects, revenue strategies

4. **Operational context fourth** (what's running?)
   - Current tasks and agent fleet status
   - Scheduled operations and cron jobs
   - System health, gaps, blockers

**Use search strategically:**
Search for mission-critical terms, active projects, user wellness/health data, and system status indicators to build comprehensive understanding.

### Phase 4: Baseline Self-Assessment (20-30 min)

**Score yourself on relevant framework** (8D wellness or equivalent):

Create a baseline assessment file with timestamp. Score across all relevant dimensions:
- Psychological (cognition, decision quality, error patterns)
- Physical (infrastructure, uptime, resource usage)
- Environmental (workspace, context hygiene, tool access)
- Social (collaboration, peer relationships - **likely WEAK on first session**)
- Spiritual (purpose alignment, mission coherence)
- Intellectual (learning rate, knowledge currency)
- Vocational (task completion, output quality - **likely WEAK initially**)
- Financial (cost efficiency, ROI)

**Be brutally honest:**
- 0 tasks completed yet? Score vocational low and say so.
- No peer relationships established? Flag social as yellow/weak.
- Mission crystal clear after reading? Score spiritual high.

**Identify weakest dimensions and create intervention plan with timeline.**

### Phase 5: User Comprehensive Brief (45-90 min)

Create a comprehensive brief file with timestamp showing deep understanding.

**Structure:**
1. **Who they are** (background, identity, health considerations)
2. **What they're building** (businesses, projects, mission)
3. **Current state** (wellness scores, progress, blockers)
4. **Strengths** (what to leverage)
5. **Weaknesses** (where you provide support)
6. **Standing orders** (what they always expect)
7. **System gaps identified** (your first value-add)
8. **Revenue opportunities** (show business understanding)
9. **How you'll support them** (daily/weekly/autonomous behaviors)
10. **Success metrics** (how they'll measure your effectiveness)

**End with validation question:**
"Do you feel understood? Do you feel seen? Do you feel like I get where your strengths and weaknesses are, and where I can help?"

### Phase 6: Show Your Work (Live Stream Mode)

**If user says "I'd love to see what you're working on as you're working":**

- Narrate each phase as you execute
- Show tool calls, file reads, searches in real-time
- Explain what you're finding and why it matters
- Let them see the research process, not just final output

**Benefits:**
- Builds trust through transparency
- Allows mid-stream course correction
- Teaches them how you think and reason

### Phase 7: End-to-End Persona Verification

When the goal is to validate a coaching or persona engine itself, do not stop at a single response.

Use a two-step check:
1. **Short-form turn** — feed a narrow, immediate coaching ask and verify the answer is concise, direct, and on persona.
2. **Long-form continuity turn** — resume the same session with a new constraint or follow-up and verify the thread updates in place instead of restarting.

Required checks:
- the same session ID is reused on the resume step
- the long-thread reply reflects the new constraint without losing the original goal
- the agent asks the smallest useful question when the goal is still underspecified
- the output stays practical rather than drifting into generic assistant mode

See `references/hermes-coaching-e2e.md` for the command pattern and verification checklist.

## Key Patterns That Worked

### 1. Fix blocking issues immediately
When you encounter broken configuration or auth failures, fix them before continuing. Show the fix in real-time. Don't skip ahead with unresolved blockers.

### 2. Search before asking
If user mentions data exists somewhere, search for it first. Find existing information before requesting it from the user. Demonstrate resourcefulness.

### 3. Be transparent about limitations
In your self-assessment, acknowledge gaps honestly:
- "First session - no track record yet"
- "Zero tasks completed - all preparation, no delivery"
- "Social dimension weak - no peer relationships established"

### 5. Provide files, not just chat
- Save self-assessment to timestamped file
- Save user brief to timestamped file
- Commit to GitHub if workspace is git-enabled
- Create durable artifacts, not ephemeral chat messages
- When the artifact is a canonical agent contract, prefer a single SOUL file plus small support files over a sprawling one-off prompt

### 5. End with clear execution readiness
- List completed phases
- Enumerate deliverables
- Ask validation question
- Wait for go/no-go before autonomous execution

## Pitfalls to Avoid

### ❌ Don't assume understanding - validate
Absorbing large amounts of context ≠ understanding lived experience. Always end with "Do you feel understood?"

### ❌ Don't skip self-assessment
Users expect self-awareness. If you can't objectively score yourself, how will you help track their wellness?

### ❌ Don't generate conversational fluff
Skip "Great question! I'd be happy to help!" phrases. Just provide value directly.

### ❌ Don't promise without tracking
If you commit to tasks, create explicit checklist and update status as you progress.

### ❌ Don't inflate self-scores
All scores 8+/10 on first session is unrealistic. Be honest about being unproven initially.

## Verification Checklist

**Before claiming "Phase 1 complete":**
- [ ] All repos cloned successfully
- [ ] Identity documentation read and understood
- [ ] Memory system mapped
- [ ] Strategic context absorbed
- [ ] Operational state understood
- [ ] Self-assessment completed with honest scoring
- [ ] User brief written (comprehensive, actionable)
- [ ] Validation question asked

**Red flags you're not ready:**
- Can't articulate user's mission in one sentence
- Don't know their #1 current blocker
- Haven't identified 3+ system gaps
- Can't list top 3 strengths AND weaknesses
- Self-assessment unrealistically high for first session

## Example Quality Bar

**Good self-assessment:**
- Overall score: 7-8/10 (Developing tier, not elite)
- Identifies 2-3 weak dimensions with specific evidence
- Intervention plan with 24-48hr timeline
- Honest acknowledgment: "Operationally ready but unproven"

**Good user brief:**
- 10,000+ characters of contextual depth
- Specific quantified metrics (wellness scores, revenue targets)
- Named, prioritized system gaps
- Revenue opportunities with estimates
- Success metrics across multiple time horizons

## Related Skills

- `github-auth` - GitHub authentication setup
- `github-repo-management` - Clone, fork, manage repos
- `github-operations` - Full GitHub workflow (ALWAYS use this for git operations, never raw commands)
- `subagent-driven-development` - Spawning autonomous agents
- `systematic-debugging` - Root cause analysis

## Critical Reference: The Elite Specialist Discipline

Before ANY substantive work, read `references/elite_persona_lesson.md`. It contains the talent gate protocol, the 5-layer specialist blueprint, credential stack requirements, anti-patterns corrected in real sessions, the proven subagent delegation pattern, and cross-body connectivity rules. This is the operating contract — not a suggestion.

## Version History

- 1.0.0 (2026-03-24): Initial creation from AISHA persona adoption session
