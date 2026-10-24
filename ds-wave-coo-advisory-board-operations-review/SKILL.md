---
name: ds-wave-coo-advisory-board-operations-review
description: Conduct a daily operations review for the the specialist engine COO Advisory Board, including individual advisor reviews, board synthesis, and PDF report generation.
category: operations
---

# the specialist engine COO Advisory Board Operations Review

This skill provides a structured process for conducting the daily operations review for the the specialist engine COO Advisory Board at Divinity Science.

## When to Use

Use this skill when:
- Conducting the daily the specialist engine COO Advisory Board operations review
- You need to synthesize input from multiple advisors/frameworks
- You need to generate a formal PDF report of the review
- You are acting as the COO Advisory Board for Divinity Science

## Prerequisites

- Access to the the specialist engine COO advisory panel private repository
- Coach files for each advisor in the `coaches/` directory
- COACHING_CONTEXT.md file in the work directory
- Access to the PDF generation script at `/<workspace>`

## Process

### Phase 1: Preparation

1. **Read Coaching Context**
   - Read `COACHING_CONTEXT.md` in your workdir
   - This contains stable, repo-local coaching context for the the specialist engine COO advisory board

2. **Read Advisor Files**
   - Read all `.md` files in the `coaches/` directory
   - Each file contains the full profile and lane for one advisor
   - Active advisors (as of this session):
     - Gwynne Shotwell — Coordination Lead
     - Tim Cook — Operations Systems
     - Ruth Porat — Resource Discipline
     - Sheryl Sandberg — Communication Glue
     - Angela Ahrendts — Launch Operations

3. **Read the Previous Day's Review for Continuity**
   - Check `/tmp/coo-review-[previous-date].md` for yesterday's review
   - Note which action items were recommended and whether they've been actioned
   - Flag anything that was P0 yesterday and is STILL pending today. A stale blocker across multiple days is itself the top finding.
   - This is how you track follow-through. Without it, every review starts from zero and loses the operational thread.

4. **Cross-Repo Intelligence Gathering (CRITICAL)**
   - The COO repo alone is NOT sufficient context. You must pull live state from multiple repos to ground recommendations in reality.
   - See `references/cross-repo-intelligence-map.md` for the full source map and verification commands.
   - Key sources to check every run:
     - **principal advisory panel** (`ds-wave-ceo-advisory-panel-private/principal-DAILY-ACTIONS.md`): current priority stack, decisions needed from the principal, commitment completion status
     - **CTO advisory panel** (`ds-wave-cto-advisory-panel-private/reports/`): build blockers, API status, infrastructure readiness
     - **Fleet journals** (`hydra-os/intel/agents/journals/FORGE/` and `/ARBITER/`): agent counts, cron error counts, fleet health
     - **Marketing content** (`hydra-os/intel/marketing/`): what launch content has been drafted (check if it's premature given product readiness)
     - **Product project docs** (`docs/`): product specs like 8D-SLEEP-PROJECT.md
     - **Coaching engine** (`ds-wave-coaching-engine/`): check `git log --oneline -5` for what actually shipped recently
   - Use `find ... -newer /tmp/coo-review-[previous-date].md` across the workspace to discover what changed since last run.

5. **Discrepancy Detection**
   - Cross-check any "facts" that appear across multiple reports. When numbers disagree across sources, that disagreement is itself an actionable finding.
   - Example: engine count appeared as 25 (CTO report), 28 (principal task table), 36 (filesystem). That gap went straight into the review as a P1 priority.
   - Run `ls -d /<workspace>*-engine 2>/dev/null | wc -l` to get ground-truth engine count.
   - Compare principal commitments log ("completed") vs principal task table ("pending") for the same item. Source-of-truth ambiguity is a finding.

### Phase 2: Individual Advisor Reviews

For each advisor, write their independent review using their specific framework. Each review should include:

- **Cross-board coordination status**: How well boards are coordinating and handing off work
- **Lane-specific assessment**: Assessment based on the advisor's specific area of expertise
- **Top operational recommendation**: The single most important operational action they recommend
- **Specific, actionable next step**: A concrete, executable step to implement their recommendation

Each advisor has a distinct voice and framework:

#### Gwynne Shotwell (Coordination Lead)
- Focus: Cross-board coordination, dependency management, follow-through
- Framework: Schedule-Driven Accountability Model
- Key questions: What's the path to yes? What's the one thing that has to happen today?
- Output format: Operational State, Cross-Board Coordination, The One Thing, Blocker Report, Coordination Recommendations

#### Tim Cook (Operations Systems)
- Focus: Process design, efficiency, simplification
- Framework: Operational Opacity as Competitive Advantage Model
- Key questions: What do the numbers say? How can we remove a step?
- Output format: Process Health, Efficiency Metrics, The Process Fix, Simplification Opportunity, Operational Directive

#### Ruth Porat (Resource Discipline)
- Focus: Resource allocation, ROI, resource audit
- Framework: Ruthless Prioritization Through Capital Discipline Model
- Key questions: Show me the return. What would you cut to fund this?
- Output format: Resource Audit, Efficiency Score, The Tradeoff, Kill / Pivot / Invest, Budget Directive

#### Sheryl Sandberg (Communication Glue)
- Focus: Communication architecture, feedback loops, team dynamics
- Framework: Radical Communication Clarity at Scale Model
- Key questions: What's the most important thing? Feedback is a gift.
- Output format: Communication Health Check, Cross-Board Signals, The Conversation That Needs to Happen, Feedback Summary, Communication Architecture Update

#### Angela Ahrendts (Launch Operations)
- Focus: Launch planning, brand experience, first impression, emotional resonance
- Framework: Emotional Launch Architecture Model
- Key questions: What should someone feel in the first 5 seconds? Human connection first.
- Output format: Launch Feeling Check, Brand Consistency Audit, The First Impression, Launch Readiness, Creative Direction

### Phase 3: Board Synthesis

After collecting all individual advisor reviews, synthesize them into a board-level view:

- **Operational Priorities Ranked by Urgency**: List the top priorities with owners and deadlines
- **Cross-Board Handoffs Needed**: Identify specific handoffs between boards that need to happen today
- **Blockers**: What's stuck and who needs to unblock it
- **Resource Allocation Recommendations**: Where to invest, divest, or reallocate resources
- **Communication Gaps**: Identify any boards not communicating effectively with each other

### Phase 4: PDF Output Generation

1. **Determine the correct report file path**:
   - Check if there is an existing canonical artifact for this type of report (e.g., `/tmp/coo-review-*.md`)
   - If an existing canonical file exists from a previous session, patch that file in place rather than creating a new variant
   - If no canonical file exists, create a new file with today's date: `/tmp/coo-review-[YYYY-MM-DD].md`
   - Follow the baseline-first principle: preserve existing structure and make surgical changes only

2. Write the full report to the determined file path

3. Run the PDF generation script:
   ```
   python3 /<workspace> [REPORT_FILE_PATH] [REPORT_FILE_PATH].pdf "COO Advisory Board" "AM"
   ```
   Where [REPORT_FILE_PATH] is the path determined in step 1

4. Your final response MUST include: `MEDIA:[REPORT_FILE_PATH].pdf`

## Output Format

The final report should follow this exact format:

```
---
## COO Advisory Board — Operations Review
📅 Date

**Operational State**: [On Track / Needs Attention / Blocked]

👥 **Advisor Notes:**
- 🚀 Gwynne Shotwell: [2-3 sentence summary]
- 🍎 Tim Cook: [2-3 sentence summary]
- 💰 Ruth Porat: [2-3 sentence summary]
- 💬 Sheryl Sandberg: [2-3 sentence summary]
- ✨ Angela Ahrendts: [2-3 sentence summary]

🎯 **Today's Operational Priorities:**
1. [PRIORITY] — owner — deadline
2. [NEXT] — owner — deadline

⚠️ **Cross-Board Handoffs Needed:**
[Any handoffs between Marketing, Product, CTO, principal that need to happen]

🔄 **Communication Gaps:**
[Any boards not communicating with each other]

## ⚡ ACTION ITEMS
**1. [ACTION]** — Impact: [why] — Source: [advisor]
→ Reply: ✅ 1 | ❌ 1 | 📝 1: your note

---
⚡ Quick reply: ✅ all, ✅ 1,3, ❌ 2, 📝 3: your idea
```

## Tone Rules

- Operational, direct, no fluff
- No AI telltales (no em-dashes, no "Furthermore/Moreover")
- Conversational, human
- Each advisor speaks in their own voice
- Celebrate what's working. Fix what isn't.
- ADHD-aware: small steps, clear owners, no vague recommendations

## Pitfalls to Avoid\n\n- Forgetting to check for new operational documents from previous session\n- Not verifying that action items from previous review were completed\n- Missing coach files or using outdated advisor information\n- Incorrect date formatting in the report filename (must be YYYY-MM-DD)\n- PDF generation failures due to wrong script path or missing dependencies\n- Losing the distinct voice of each advisor in their individual reviews\n- Being too vague in recommendations (violates ADHD-aware principle)\n- Using AI telltales like em-dashes or overly formal language\n- Making the report too long or fluffy (violates operational directness principle)\n- Not providing specific, actionable next steps for each advisor\n- **Producing a generic review that doesn't reference live operational state.** Without cross-repo intelligence gathering, every review reads the same: "boards need better coordination, reports aren't being acted on." That is true but useless. The value comes from citing SPECIFIC findings: "the Build-Direction Statement is unapproved for 9 days," "the SINGULARITY cron job has 88 errors," "engine count disagrees across 3 sources." Those specific findings only surface when you pull from principal, CTO, fleet, and marketing repos every run.
- **Creating new report files daily instead of patching the canonical existing artifact** (follow baseline-first principle: preserve existing structure and make surgical changes only)

## Verification

After completing the review, verify:
- All coach files were read and their frameworks applied correctly
- The report follows the exact output format specified
- The PDF was generated successfully at the expected location
- MEDIA: path is included in the final response
- Each advisor's section reflects their distinct voice and framework
- Action items are specific, owned, and have clear deadlines
- Cross-board handoffs and communication gaps are clearly identified

## References

- See `references/cross-repo-intelligence-map.md` for the full source map of live operational state across all the specialist engine repos, plus verification commands for grounding reviews in reality
- See `references/advisor-frameworks.md` for detailed summaries of each advisor's decision-making framework
- See `templates/report-template.md` for a template of the expected report format
- See `scripts/verify-review.sh` for a script to verify the completeness of a review

## Author

the specialist engine COO Advisory Board