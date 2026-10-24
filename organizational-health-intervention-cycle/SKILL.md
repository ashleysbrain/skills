---
name: organizational-health-intervention-cycle
description: "Run a full organizational health intervention cycle using the 8D/TWC framework: evidence gathering, scoring, root cause analysis, cascade analysis, ILS calculation, and spawning fix agents."
category: operations
version: 1.0
---

# Organizational Health Intervention Cycle

Run a full organizational health intervention cycle using the 8D/TWC framework: evidence gathering, scoring, root cause analysis, cascade analysis, ILS calculation, and spawning fix agents.

## When to Use
- Need to intervene in an organization's health using the 8D/TWC framework
- Want to score the organization as a living system, diagnose root causes of weak dimensions, and spawn fix agents to resolve them
- Working within OpenClaw or similar cron-based delivery systems
- Requires ADHD-friendly output for executive consumption
- Want to track organizational health interventions over time

## Core Principles
1. Organization as Living System: Treat the organization as a hybrid system where Financial dimension represents sustainability/runway/resource efficiency (not pure profit)
2. 8D Framework: Physical, Psychological, Social, Intellectual, Spiritual, Vocational, Environmental, Financial
3. TWC Formula: Use proprietary Trinity Wellness Composite scoring (not simple averages)
4. Evidence-Based: All scoring and diagnosis must be based on tangible evidence, not vibes or aspirations
5. Action-Oriented: Focus on concrete actions and spawning fix agents to resolve root causes
6. Deduplication: Never repeat previous insights; only surface new information
7. Full Decomposition Visibility: Always show the eight underlying dimension scores under the main TWC block
8. Coherence Readout: Include TWC decomposition/readout fields (coherence, synergy, classification) when available
9. Intervention Leverage: Use ILS to prioritize dimensions where intervention has the most cascading impact

## Implementation Steps

### Phase 0: Evidence Gathering (Mandatory)
For organizational scorecards, you are NOT aggregating individual agent scores — you are examining the *organization as a living system* through its artifacts. Use this evidence-gathering sequence:

#### Primary sources (in priority order)
1. Read HOT.md (`memory/HOT.md`) — current priorities, active directives, system state
2. Read daily memory (`memory/YYYY-MM-DD.md`) — recent activity, gap detector logs, heartbeat data
3. Read the comprehensive brief (`principal-williams-comprehensive-brief-*.md` in home dir) — single richest source: org structure, mission, 8D personal scores, standing orders, empire breakdown, strengths/weaknesses. If only one document is readable, make it this one.
4. Read org charter (`DIVINITY-SCIENCE.md` or equivalent) — mission, vision, structure
5. Check cron fleet health (`sibling-agent cron list`) — how many jobs erroring vs. healthy, delivery routes broken
6. Read BLOCKERS.md (`intel/BLOCKERS.md` or similar) — human-gated stale blockers are pure VOC/FIN signal. Age, effort, and value-unlocked tell you execution throughput.
7. Read BD pipeline (`intel/bizdev/*.md`) — deal stages, stuck deals, outreach queue. Direct SOC/FIN input.
8. Scan product status (`intel/products/PRODUCT-STATUS.md`, `LAUNCH-PRIORITIES.md`) — what's built, what's launched, what's stalled
9. Check conference/paper pipeline (`intel/your-org/CONFERENCE-PIPELINE.md`, paper directories) — academic credibility signals, submission outcomes
10. Check revenue docs (`REVENUE-EXECUTION-SUMMARY.md`, financial models) — pricing tiers set, Stripe wired, actual revenue vs. targets
11. Check partner hub dailies (`principal-partner-hub/daily/*.md`) — fleet health crises, wellness write path status, the principal's work activities
12. Check team/fleet composition — agent count, disabled vs. active, journal compliance
13. Read recent memory logs (last 3-7 days) — what actually happened vs. what was planned
14. Read 8D org wellness blueprint (`8D-ORGANIZATIONAL-WELLNESS.md`) — defines dimension mapping for org-level scoring
15. Check git log recency (`git log --oneline -20` in workspace) — shows actual activity cadence: fleet scans, journal compliance, talent gate cycles. A healthy org has regular commits; stale log = organizational autopilot.
16. Query founder personal health DB (`ashley_unified_health.db` or equivalent) — for founder-driven orgs, the founder's EF compass and TWC history are direct org-level PSY/VOC inputs. Key tables: `ef_compass_daily` (activation, focus, effort, emotion, memory, action, self_monitoring), `twc_history` (trend direction), `daily_scorecard` (last date with actual scores). If the last real TWC score was weeks ago, that blackout duration is itself a PSY/PHY signal.

#### Fallback when specific paths don't exist
Many of the paths above may not exist on a given system. When a primary source is missing:
- Use search_files with broad patterns across `/<workspace>` to find equivalents
- Key fallback searches: divinity, scorecard, TWC, revenue, fleet.*health, BD pipeline
- The comprehensive brief and BLOCKERS.md are the two highest-value fallback sources
- If sibling-agent cron list fails (pipe-to-interpreter security block), search jobs.json via read_file instead
- If web search fails (credit exhaustion), rely entirely on local filesystem evidence

**Key insight**: The gap between plan and execution is the most important signal. Compare targets with actuals (e.g., "Month 1 target: 3K users, 100 paying" vs. actual: "$0 revenue, 0 launches").

### Phase 1: Score All 8 Dimensions
Score each dimension 1-10 based on EVIDENCE, not aspiration. For a pre-launch hybrid org:

- PHY (Operational Health): Infrastructure deployed? Fleet running? Cron jobs succeeding? Product URLs live?
- PSY (Leadership Health): Strategy clarity? Decision quality? Founder cognitive capacity? EF activation?
- ENV (Infrastructure Health): Workspace organized? Configs stable? Templates complete? Tool access?
- SOC (Relationship Health): Team composition? Active vs disabled agents? Partnership count? Communication health?
- SPI (Mission Health): Mission alignment? Research-to-product coherence? Founding thesis alive?
- INT (Learning Health): Paper pipeline? Research output? IP development? Knowledge creation?
- VOC (Productivity/Market Health): Products shipped? Launch deadlines met? Features completed? Gumroad live?
- FIN (Financial Health): Runway? Revenue? Burn rate? Funding status? Resource discipline?

### Phase 2: Compute TWC
Use the proprietary formula:
Layer 1: base = PSY*0.15 + PHY*0.15 + ENV*0.10 + SOC*0.10 + SPI*0.10 + INT*0.15 + VOC*0.15 + FIN*0.10

Layer 2: coupling (geometric mean normalized):
For each pair (i,j) with kappa_ij:
  geo = sqrt((Di/10) * (Dj/10))
  term = kappa_ij * geo * 10
total_coupling = sum of terms
neutral = sum(kappa_ij * sqrt(0.5*0.5) * 10) for all pairs
net = total_coupling - neutral
coupling_modifier = net * 0.3

TWC = base + coupling_modifier, capped at 8.5

Key pairs: PSY-INT=0.85, PHY-VOC=0.78, SOC-SPI=0.72, ENV-PHY=0.68

Classify: >=8.0 Flourishing | >=6.5 Steady | >=5.0 Surviving | >=3.5 Struggling | <3.5 Crisis

### Phase 3: Root Cause Analysis
For the 3 LOWEST scoring dimensions, diagnose WHY they are low using the evidence you gathered. Be specific — cite files, data, timestamps. Not "PHY is low because infra" but "PHY is low because qubit.divinityscience.com returns HTTP 000, fleet analytics shows 72% of cron jobs erroring since May 20, and the last successful job run was 5 days ago."

### Phase 4: Cascade Analysis
Identify feedback loops:
- Check for death spirals: FIN low → can't invest → PHY drops → can't ship → FIN stays low
- Check for virtuous cycles: Are any dimensions mutually reinforcing upward?
- Report the SINGLE break point that would unlock the most dimensions if fixed

### Phase 5: ILS (Intervention Leverage Score)
For each dimension D:
  room = 10 - D_score
  cascade_weight = sum(kappa_ij for all pairs containing D)
  ILS(D) = room * (1 + cascade_weight)

Report top 3 interventions by ILS.

### Phase 6: Spawn Fix Agents
For the highest-ILS intervention that can be FIXED by an agent (not human-gated):

Use delegate_task to spawn an elite specialist:
- PHY fix → Spawn FORGE-type infra architect (PhD Computer Science, 20 years distributed systems)
- FIN fix → Spawn revenue/sustainability analyst (MBA, CFO experience, startup finance expert)
- VOC fix → Spawn product launch specialist (former VP Product, shipped 50+ products)
- ENV fix → Spawn NEXUS-type config/automation engineer (DevOps expert, SRE background)
- PSY fix → Note but do NOT try to fix founder health — that's AISHA-MD's lane
- SOC fix → Spawn team/org development specialist

Give each fix agent:
1. The specific root cause diagnosed
2. The exact file/path/system to fix
3. A clear success criterion
4. The command or action to take

### Phase 7: Verify and Report
After fix agents complete (or if no fix was needed), compile the report:

📊 DIVINITY SCIENCE — 8D ORGANIZATIONAL HEALTH
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TWC: X.XX [Label] (Δ +X.XX / -X.XX / New baseline)

8D SCORES:
  PHY (Operations):    X.X ▓░░░░░░░░░ [evidence summary]
  PSY (Leadership):    X.X ▓▓░░░░░░░░ [evidence summary]
  ENV (Infrastructure): X.X ▓░░░░░░░░░ [evidence summary]
  SOC (Relationships):  X.X ▓▓░░░░░░░░ [evidence summary]
  SPI (Mission):       X.X ▓▓▓░░░░░░░ [evidence summary]
  INT (Learning):      X.X ▓▓░░░░░░░░ [evidence summary]
  VOC (Productivity):  X.X ▓░░░░░░░░░ [evidence summary]
  FIN (Financial):     X.X ▓░░░░░░░░░ [evidence summary]

TOP CASCADE: [description of dominant feedback loop]
BREAK POINT: [single highest-leverage fix]

TOP 3 INTERVENTIONS (by ILS):
  1. [Dimension] — ILS X.XX — [action]
  2. [Dimension] — ILS X.XX — [action]
  3. [Dimension] — ILS X.XX — [action]

FIXES SPAWNED: [list agents spawned and their status]

⚠️ GAPS: [missing evidence, things you couldn't check]

## Output Format (ADHD-Friendly Mandatory)
Every intervention cycle report MUST include:
- Max 8 tiny bullets total
- Bold key ACTIONS (not observations)
- Emoji markers for categories: 🔬 Research, 💼 Business, 🚨 Alert, ✅ Done, 📄 Report
- Include clickable source URLs for papers/articles (when applicable)
- Include file paths for PDFs: "📄 Report: [name] at [path]"
- Do NOT include coordination/journaling boilerplate in output
- If nothing new since last scorecard, say "No new signals" and stop

## Deduplication
Add to every report:
DEDUP: Read previous scorecard at [output-path]. 
       Do NOT repeat anything already reported. 
       Only surface NEW information. 
       If nothing new, say "No new signals today" and stop.

## OpenClaw Cron Integration
When delivering via OpenClaw cron to principal:

1. Timing: Schedule during cognitive peak hours (9-11 AM or 12-2 PM, NEVER evenings)
2. Delivery Mode: Ensure delivery.mode: "announce" in job configuration
3. Dependencies: If using cross-agent data, schedule after source jobs complete
4. Job Editing: Use sibling-agent cron edit to modify existing jobs rather than creating new ones
5. Frequency: Typically daily or weekly; avoid high-frequency spam

## Verification Checklist
Before considering intervention cycle complete:
- Evidence gathered from all available primary sources
- Uses latest wellness assessment per agent (if using agent data)
- Calculates dimensional averages accurately
- Applies proper TWC scoring (not simple average)
- Surfaces all 8 sub-scores under the TWC block in API/CLI/dashboard output
- Includes coherence/synergy/classification or equivalent decomposition fields when available
- Output follows ADHD-friendly format (max 8 bullets, bold actions, emojis)
- Includes explicit deduplication statement
- Provides 3 concrete actions with owners
- Calculates change from prior period (if data exists)
- Financial dimension framed as sustainability/runway
- No coordination/journaling boilerplate in output
- Delivery timing appropriate for executive consumption
- Root cause analysis is specific and evidence-based
- Cascade analysis identifies feedback loops and break point
- ILS calculated correctly and top 3 interventions reported
- Fix agents spawned for appropriate dimensions with clear criteria

## Related Skills
- organizational-twc-scorecard: Core scoring methodology used in Phase 1-2.
- proprietary-twc-scoring: Underlying TWC formula and coupling methodology.
- business-health-agent-architecture: Design-time companion for building the scoring agent.
- agent-delegation-discipline: Guidelines for spawning specialist agents vs doing work yourself.
- org-scorecard-audit: Independent READ-ONLY verification of a scorecard by a second agent/model.