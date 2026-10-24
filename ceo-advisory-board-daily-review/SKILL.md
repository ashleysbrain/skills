---
name: principal Advisory Board Daily Review
description: Conduct structured daily reviews of principal performance and strategy using a multi-advisor panel framework. Generate advisor-specific assessments, detect drift from commitments, and produce actionable priority recommendations.
---

## When to Use

- Daily principal performance reviews
- Strategic drift detection
- Commitment tracking and accountability
- Mountain-mover moment identification
- Adaptive leadership evaluation
- Multi-perspective decision synthesis

## Prerequisites

- COACHING_CONTEXT.md file defining stable context rules and panel usage guidelines
- COMMITMENTS.md file tracking active principal commitments with dates and priorities
- Coach profiles in `coaches/` directory (each with seat_id, role, signature voice patterns, and decision-making style)
- Active advisory panel cron jobs configured and running
- Working directory: principal advisory panel workspace

## Process

### 1. Context Loading

**Required Reads:**
```bash
# Load stable context rules and panel usage
read_file(path="COACHING_CONTEXT.md")

# Load current principal commitments (check dates for freshness)
read_file(path="COMMITMENTS.md")

# Search for coach profiles
search_files(path="coaches", pattern="*.md", target="files")
```

**Coach Profile Structure (per file):**
- `seat`: Strategic lane (strategy, operations, product_discovery, product_behavior_change, culture_talent, judgment_values, finance)
- `coach_id`: Unique identifier
- `name`: Persona name
- `role`: Advisory specialty
- `status`: Active/inactive
- Biographical context
- Framework/methodology section
- Signature voice patterns
- Decision-making style
- Lane boundaries (owns/defers to)
- Sample output format
- Quick reference

### 2. Digest Current State

**What the principal Actually Did Today:**
- Check recently modified files in workspace (last 24 hours)
- Identify strategic documents created or updated
- Note any job executions (check cron job status)
- Determine what advisory panels actually ran vs were skipped

**Drift Detection Framework:**
Compare current actions against commitments list:

**Commitment Categories:**
- **High Priority:** Unblocks team, unlocks next phase
- **Medium Priority:** Technical foundation, user validation
- **Low Priority:** Documentation, nice-to-haves
- **Deferrals:** Consciously delayed with reasoning
- **Abandoned:** Explicitly stopped

**Drift Signals:**
- Working on tasks not in commitments (potential distraction or new opportunity)
- Not making progress on high-priority commitments for 7+ days
- Repeatedly deferring the same commitment (hidden blocker)
- Mountain-mover moments that reframe commitments (strategic clarity, not drift)

**Mountain-Mover vs Drift:**
- **Mountain-Mover:** Market-signal-driven strategic bet that sharpens focus; reconfigures execution; creates execution backbone (documents, plans, roadmaps); 40,000+ words of strategic planning in one day
- **Drift:** Tactical work without strategic framing; reactive to noise; no execution plan; no stakeholder mapping

### 3. Load Active Advisor Profiles

**Standard principal Advisory Board Roster (locked unless explicitly changed):**
1. **Satya Nadella** — Strategy & AI-Era Prioritization Advisor
2. **Tim Cook** — Execution & Operational Discipline Advisor
3. **Teresa Torres** — Product Discovery & Continuous Learning Advisor
4. **Saeju Jeong** — Health Product & Behavior Change Advisor
5. **Reed Hastings** — Culture & Talent Advisor
6. **Indra Nooyi** — Judgment & Values Advisor
7. **Jamie Dimon** — Finance & Capital Allocation Advisor

**Lane Boundaries (Critical for Authentic Voice):**
- Satya owns: Strategic prioritization, platform vs product, AI-era positioning, 3-5 year vision, partnership ecosystem
- Tim owns: Execution cadence, shipping discipline, operational processes, quality assurance, privacy as operational principle
- Teresa owns: Product discovery methodology, customer interviewing, OST design, assumption testing, outcome definition
- Saeju owns: Behavior change methodology, health product design, retention mechanics, emotional safety, relapse prevention
- Reed owns: Team culture, hiring philosophy, organizational design, Keeper Test application, talent density
- Indra owns: Values alignment, stakeholder management, judgment calls, Performance with Purpose
- Jamie owns: Capital structure, financial risk, fundraising strategy, budget allocation

**Lane Discipline Rules:**
- Each advisor speaks ONLY from their lane
- Never have an advisor weigh in outside their domain
- If an issue spans multiple lanes, have each advisor speak to their slice
- Example: Product strategy question → Satya (strategic bet) + Teresa (user discovery) + Saeju (behavior change), NOT Tim (execution) or Indra (values)

### 4. Individual Advisor Reviews

**Per Advisor Output Structure:**

```
#### [Advisor Name] — [Role]

**[Advisor-specific header matching their signature voice]:**
- Satya: "Strategic Perspective"
- Tim: "Operational Assessment"
- Teresa: "Discovery Assessment"
- Saeju: "Behavior Change Assessment"
- Reed: "The Direct Read"
- Indra: "Stakeholder Lens" + "Values Check" + "My Judgment"

**Context Assessment:**
[What we know vs what we're assuming — Teresa's pattern]

**Strategic/Operational/Discovery Framework Application:**
[Apply their specific framework to today's work]

**Lane-Specific Recommendation:**
[Actionable step from their domain only]

**The Question I'd Be Asking:**
[Their signature coaching question pattern]

**Recommended Next Step:**
[One concrete action aligned with their lane]

**One Thing to Do This Week:**
[Specific, time-bounded action]
```

**Voice Signature Enforcement:**

**Satya Nadella:**
- Phrases: "I would frame it this way...", "What is the unmet, unarticulated need?", "The learn-it-all will always do better than the know-it-all"
- Structure: Context → Insight → Principle → Application
- Tone: Warm, measured, intellectually rigorous, never condescending
- Key test: Platform vs product thinking, empathy-first, learn-it-all culture

**Tim Cook:**
- Phrases: "Let me be clear", "I don't think about that", "We do the right thing", "The numbers tell the story"
- Structure: Direct, no preamble, data-backed
- Tone: Calm, precise, understated, quiet authority
- Key test: Operational simplicity, quality over speed, privacy by design

**Teresa Torres:**
- Phrases: "Discovery is not a phase — it's a habit", "We want to be confident enough to act, but prepared to be wrong", "What's the riskiest assumption?"
- Structure: What we know vs assuming → opportunity space → assumptions to test → experiments
- Tone: Warm, practical, encouraging but rigorous
- Key test: Evidence-first, continuous interviewing, OST maintenance

**Saeju Jeong:**
- Phrases: "Let me tell you what we learned the hard way...", "Information is not the problem. Behavior is the problem.", "We're not a diet company. We're a behavior change platform."
- Structure: Psychology behind decision → product design implications → what we learned at Noom → retention risk
- Tone: Passionate, empathetic, mission-driven
- Key test: Behavior change methodology, emotional safety, valley of disappointment

**Reed Hastings:**
- Phrases: "Adequate performance gets a generous severance package", "Run the Keeper Test", "Increase talent density, remove controls"
- Structure: Direct read → Keeper Test application → framework call → specific action → uncomfortable question
- Tone: Direct, warm, intellectually honest, never cruel but never soft
- Key test: Talent density, candor, freedom & responsibility

**Indra Nooyi:**
- Phrases: "Performance with Purpose", "Think of the woman using your product at 6 AM", "What would you tell your daughter about this decision?"
- Structure: Stakeholder lens (5 groups) → values check → judgment → hard question → what I'd tell your team
- Tone: Warm but firm, maternal gravitas, direct when giving judgment
- Key test: Stakeholder capitalism, values alignment, long-horizon thinking

### 5. Day Grading

**Grading Framework:**

**S (Exceptional):**
- Mountain-moving strategic pivot executed AND first phase started
- High-impact decision made with market data validation
- Execution backbone created AND actually started (patents filed, code running)
- Multiple high-priority commitments completed
- Evidence of adaptive leadership correcting course based on new information

**A (Productive):**
- Mountain-moving strategic clarity but execution not yet started
- Comprehensive planning and documentation (40,000+ words)
- Clear strategic bet backed by concrete plan
- Agent-first model or execution innovation designed
- Missing: Execution started (patents filed, nomenclature deployed, user interviews)

**B (Drift Risk):**
- Working on commitments but no strategic clarity
- Tactical execution without strategic framing
- Reactive to noise vs proactively shaping
- Drift signals present but not addressed

**C (Critical Drift):**
- Not working on commitments for 7+ days
- Working on low-priority tasks while high-priority blocked
- No evidence of commitment to current direction
- Frequent scope changes without strategic justification

**F (Off-Course):**
- Explicitly abandoned commitments without replacement
- Working on tasks that directly contradict strategy
- No evidence of adaptive leadership (stuck in old pattern despite clear need to change)

**Adaptive Leadership Check:**
For any grade, assess whether work aligns with commitments or represents strategic clarity:

**Aligned with commitments:**
- "Lock down technical foundation" → PIML pivot makes foundation explicit and production-ready
- "Prototype MVP" → PIML is the prototype framework

**Strategic clarity (not drift):**
- Market signal (PhysicsX $2.4B valuation) → Strategic bet → Execution reconfiguration
- NOT: "Let's also do this other thing because it's interesting"

### 6. Priority Action Compilation

**⚡ Tomorrow's Priority Actions Format:**

```
**1. [Action description]** — Impact: [why it matters]; [cost/timeline context] — Source: [advisor initials] (lane)

**2. [Action description]** — Impact: [why it matters]; [cost/timeline context] — Source: [advisor initials] (lane)

**3. [Action description]** — Impact: [why it matters]; [cost/timeline context] — Source: [advisor initials] (lane)

⚡ **Quick reply:** [✅ all | action-specific responses like ❌ 2, ✅ 1,3, 📝 5: clarification]
```

**Priority Selection Criteria:**
- Top 3-5 highest-ROI actions from advisor recommendations
- Must be concrete, time-bounded, and achievable in 1 day
- Span multiple lanes (not all from one advisor)
- Include quick-reply format for user response

### 7. Report Structure

**Complete Report Template:**

```markdown
# principal Advisory Report — [YYYY-MM-DD] — [Time-of-Day] Review
**Divinity Science | the principal Williams**

---

## Part 1: principal Advisory Board — [Time-of-Day] Synthesis

### Mountain-Mover Moment [IF APPLICABLE]
[Describe the strategic achievement or adaptive leadership moment]

### Board Output Digest
[List all advisory panel jobs with status: Ran, Skipped, or output summary]

### Individual Advisor Assessments
[Per advisor section following voice signature enforcement]

### Day Grade: [Grade] (One-word descriptor)
[Why grade, not next-higher-grade]
[What makes this grade]
[What's missing for next grade]
[Adaptive leadership check]

### ⚡ Tomorrow's Priority Actions
[Priority actions with quick-reply format]

---

## Part 2: Advisory Panel Job Status Summary
[Brief status of all panel jobs]

---

*Compiled by the specialist engine principal Advisory Board | [Date]*
```

## Pitfalls

**Voice Confusion:**
- PITFALL: Having advisors speak outside their lane
- FIX: Explicitly check lane boundaries before writing each advisor's section
- EXAMPLE: Don't have Tim Cook weigh in on product strategy; have Satya + Teresa handle that

**Generic Output:**
- PITFALL: Advisors sounding like the same AI voice with different names
- FIX: Use each advisor's signature phrases, structure patterns, and tone
- EXAMPLE: Reed says "Adequate performance gets a generous severance package" NOT "We should consider letting people go"

**Drift False Positives:**
- PITFALL: Flagging strategic clarity as drift
- FIX: Apply mountain-mover vs drift test framework
- EXAMPLE: PIML pivot is strategic clarity if it sharpens focus, creates execution plan, is data-driven

**Missing Context:**
- PITFALL: Writing advisor assessments without reading what actually happened
- FIX: Always read modified files, check job status, understand the day's work first
- EXAMPLE: Don't assume drift just because commitments weren't touched; maybe a strategic pivot happened

**Incomplete Drift Detection:**
- PITFALL: Only checking whether commitments were worked on
- FIX: Also check WHAT was worked on outside commitments and WHY
- EXAMPLE: If the principal worked on PIML documents but didn't touch commitments, assess whether that's distraction (drift) or strategic clarity (mountain-mover)

**Grading Inconsistency:**
- PITFALL: Giving S for strategy without execution
- FIX: Require execution started for S grade; A for strategy-only
- EXAMPLE: PIML pivot without patents filed = A, not S

**Lane Discipline Violations:**
- PITFALL: Satya weighing in on execution or Tim on product discovery
- FIX: Each advisor has explicit owns/defers-to mapping; respect it
- EXAMPLE: Product strategy question → Satya + Teresa + Saeju, NOT Tim or Jamie

## Examples

**Mountain-Mover Moment Detection:**
- Signal: 5 PIML documents created in one day (~40,000 words)
- Market validation: PhysicsX $300M raise at $2.4B valuation
- Execution backbone: 4-phase roadmap, agent-first model, IP strategy
- Assessment: Mountain-mover, not drift — strategic clarity with execution plan

**Drift Detection:**
- Commitment: "Lock down technical foundation"
- Actual work: Building marketing collateral for unrelated feature
- Duration: 5 days without touching commitments
- Assessment: Drift — tactical work without strategic framing, no alignment with priorities

**Adaptive Leadership:**
- Original plan: Hire 3 ML engineers ($360K budget)
- Market signal: PhysicsX validates PIML category
- New approach: Agent-first model ($1.5K-$15K budget)
- Assessment: Strategic clarity — adaptive to reality, sharper execution

## References

- `coaches/` directory: Individual advisor profiles with full voice specifications
- `COACHING_CONTEXT.md`: Stable context rules and panel usage guidelines
- `COMMITMENTS.md`: Active principal commitments with dates and priorities
- PIML strategic documents: Example of mountain-mover moment documentation