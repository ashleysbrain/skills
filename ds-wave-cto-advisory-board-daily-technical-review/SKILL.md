---
name: ds-wave-cto-advisory-board-daily-technical-review
description: Conduct the the specialist engine CTO Advisory Board's daily technical review following the advisor-based format
version: 2.0.0
---
# CTO Advisory Board Daily Technical Review

A class-level skill for conducting the the specialist engine CTO Advisory Board's daily technical review following the established advisor-based format. This skill captures the process, format, and key principles for producing the technical intelligence report that informs the Product, Marketing, COO, Design, and principal advisory boards.

## When to Use This Skill

Use this skill when:
- Conducting the daily CTO Advisory Board technical review (typically as a cron job)
- You need to assess the technical architecture of Divinity Science's health platform
- You must provide lane-specific advice from five CTO-focused advisors
- You need to generate actionable technical recommendations for the engineering team
- You are preparing the pre-cascade intelligence that other boards build upon

## Skill Overview

This skill embodies the CTO Advisory Board's responsibility to:
1. Review the technical state of Divinity Science's platform (8D360 scoring, GAS v2.0, behavioral physics, self-healing, the specialist engine coaching engine)
2. Evaluate architecture through the lens of five specialized advisors
3. Identify gaps between technical capabilities and market/competitive demands
4. Generate prioritized, actionable technical recommendations
5. Produce a formatted report that feeds into the wider advisory cascade

The review follows a strict format with sections for each advisor, cross-lane synthesis, and top actions - mirroring the structure used by the Research & Analytics Advisory Board but focused on technical excellence.

## Preparation Phase

Before beginning the review, complete these prerequisite steps:

1. **Read the foundational context**:
   - `COACHING_CONTEXT.md` - Understand the full product stack and current state
   - `API-CONTRACT.md` - Review current API definitions and versioning strategy
   - `BUILD-DIRECTION-STATEMENT.md` - Understand current technical priorities and constraints
   - `CI-CD-SETUP.md` - Assess current deployment and infrastructure practices

2. **Load the advisor profiles** (read these files to embody each perspective):
   - `coaches/andrew-ng.md` - AI Architecture Advisor
   - `coaches/eric-topol.md` - Health Tech Product Advisor  
   - `coaches/nicole-forsgren.md` - Infrastructure & DevOps Advisor
   - `coaches/will-larson.md` - CTO Leadership Advisor
   - `coaches/balaji-srinivasan.md` - Blockchain & Web3 Architecture Advisor

3. **Review key technical documentation and fleet state**:
   - `ARCHITECTURE.md` - Understand the Resonance + Mastermind model and system overview
   - `INTEGRATION.md` - Study integration patterns between coaching engines and other systems
   - Relevant algorithm documents (e.g., GAS v2.0, 8D360, behavioral physics)
   - **PIML-STRATEGIC-PIVOT-BRIEF.md** (if present) - Check for Physics-Informed Machine Learning context. The PIML pivot (announced June 10, 2026) changes the AI architecture story — neural ODE prototypes with physics constraints, 4.2x extrapolation accuracy improvements, and market validation (PhysicsX $300M raise). This affects Andrew Ng's recommendations significantly.

4. **Check the engine fleet registry** (25+ engines as of June 2026):
   - `/<workspace>` — port assignments and dependencies
   - `/<workspace>` — v2.0.0 authoritative registry with ecs.py mirror
   - `/<workspace>*.md` — most recent fleet audit (check for latest date)
   - The fleet includes: Core Intelligence (Wave/Kuramoto, Morphogen/Turing, Creative Cortex), Body Systems (Harvey, Beaumont, Bright, Haldane, Burnet, Hill, Helmholtz, Unna, Sutherland, Allostasis), Infrastructure (Quartz, Self-Healing, Clinical/Osler, Scanner, Tech Currency), and Sensory I/O (Audio, Text/Vision, Speech, Interoception, Environment)

5. **Detect what changed since last review** (critical for freshness):
   ```bash
   # Check modification times on key files
   stat -f "%Sm %N" -t "%Y-%m-%d %H:%M" \
     /<workspace>*.md \
     /<workspace> \
     /<workspace>

   # Find files modified in last 2 days across the workspace
   find /<workspace> -maxdepth 2 -mtime -2 -type f -not -path "*/node_modules/*" 2>/dev/null | head -30
   ```
   Report staleness: if API-CONTRACT.md, BUILD-DIRECTION-STATEMENT.md, or CI-CD-SETUP.md haven't changed in 7+ days, flag it — stale specs are blockers.

## Conducting the Review\n\nFollow this exact format for the final report. Each section must embody the specific advisor's voice, perspective, and priorities.\n\nThe review is conducted in two phases:\n\n**Phase 1: Individual Advisor Reviews** - For each advisor, conduct their independent technical review (sections 1-7 below)\n\n**Phase 2: Board Synthesis** - After completing individual advisor reviews, synthesize the insights (sections 8-11 below)\n\n### 1. Executive Summary (3-5 sentences)
- Identify the most significant technical gap between market/competitive state and DS capabilities
- Focus on what prevents rapid iteration, user exposure, or competitive advantage
- State the #1 technical action needed today to close this gap
- Reference the current engine fleet state and any changes since last review

### 2. Current State Snapshot (NEW — critical for context)\nInclude these subsections:\n- **Engine Fleet Status**: How many engines, which are working, any new since last review. Reference the fleet audit.\n- **API Contract Status**: Current version, what's covered, what gaps remain (function-calling schemas, contract tests).\n- **Build Direction Status**: Is BUILD-DIRECTION-STATEMENT.md approved? If still DRAFT, flag days stale — this is a blocker.\n- **CI/CD Status**: Is the pipeline deployed? What SLOs are defined?\n- **What Changed Since Last Review**: Use file mtimes to identify recent modifications across the workspace. Note staleness on key spec files.\n\n### 3. Part 1: Andrew Ng — AI Architecture Advisor
Embody Ng's data-centric, pragmatic, iteration-focused perspective:

**Context**: Check for PIML-STRATEGIC-PIVOT-BRIEF.md. If present, the PIML (Physics-Informed Machine Learning) pivot changes the AI architecture significantly:
- Neural ODE prototype: dx/dt = f_physics + f_neural with learnable mean-reversion, coupling dynamics, conservation constraints
- 8 validated physics isomorphisms (homeostatic sleep pressure, Van der Pol circadian, Lotka-Volterra REM-NREM, Langevin wake-sleep, etc.)
- 4.2x extrapolation accuracy advantage over unconstrained models
- Market validation: PhysicsX raised $300M at $2.4B valuation doing PIML for industrial engineering

This means the architecture is now a **hybrid system**: physics-informed models as the scoring core, LLM as the conversational interface (not a pure LLM RAG story anymore).

**Assessment**: Evaluate the current AI architecture - separation of concerns, API design, model choice, data flow. Note where tight coupling exists or where LLM is being asked to replicate engine logic. In PIML context: Are physics-informed models hardening or over-engineering before user validation?

**Recommendations** (numbered, specific):
- Implement coaching engines as versioned microservices with clear APIs
- Add structured output validation to LLM pipeline  
- Deploy feature flag system for engine versioning
- Each recommendation must include: action, why it matters, concrete next step

**Key Metric**: The single most important thing to measure right now (e.g., percentage of LLM-generated requests successfully invoking coaching engines without validation errors)

**Risk to Watch**: The primary technical risk that could derail progress (e.g., over-engineering API layer before validating user flows)

**One-Liner Takeaway**: Single sentence distillation of Ng's core advice

**API Design Guidance (Ng)**: Lane-specific API recommendations — e.g., function-calling JSON schemas per engine, tool registry format, confidence scoring thresholds.

**One Actionable Step for Today**: A single concrete, completable-today action with exact deliverable (e.g., "Define the function-calling JSON schema for GAS v2.0 and add to API-CONTRACT.md section 13").

### 3. Part 2: Dr. Eric Topol — Health Tech Product Advisor
Embody Topol's evidence-first, patient-safety, validation-focused perspective:

**Assessment**: Evaluate risks of conflating health information with medical advice, validation gaps for scoring algorithms, regulatory boundaries.

**Recommendations** (numbered, specific):
- Dual-track launch strategy (information tool first, then coaching integration)
- Clinical safety review board with licensed clinician
- Uncertainty quantification in all coaching outputs
- Each must include actionable steps with clear rationale

**Validation Requirements**: Specific studies/tests needed before proceeding (e.g., 8D360 analytical validity study, GAS v2.0 geometric validation)

**Patient Impact Statement**: 1-2 sentences on how inaccuracies could harm users (asymmetric responsibility in health tech)

**Regulatory Considerations**: Intended use documentation, HIPAA, FDA SaMD considerations

**API Design Guidance (Topol)**: Lane-specific — e.g., citations[] array on health answers, response_class field for info/advice boundary, validation_status on scoring endpoints, feedback flag endpoint.

**One Actionable Step for Today**: Single concrete action (e.g., "Run citation accuracy audit on 50 health queries").

### 4. Part 3: Dr. Nicole Forsgren — Infrastructure & DevOps Advisor
Embody Forsgren's metrics-first, DORA-focused, reliability-oriented perspective:

**Assessment**: Current state of CI/CD, observability, security practices, deployment frequency, lead times.

**Recommendations** (prioritized, with expected impact and effort):
- Instrument system before first user deployment (metrics, logging, tracing, SLOs)
- Automate deployment pipeline completely (build, test, security scan, staged deployment)
- Implement secrets management immediately (no credentials in env/variables)
- Each recommendation follows format: [Action] — Expected impact: [metric improvement] — Effort: [S/M/L]

**Target State (Elite Benchmark)**: DORA elite performer benchmarks (deploy frequency: on demand, lead time: <1hr, change failure rate: 0-15%, MTTR: <1hr)

**Gap Analysis**: Specific, measurable gaps between current and target state based on actual system observation

**Measurement Plan**: What to instrument, how often to review, what "done" looks like

**Risk Assessment**: Quantified consequences of inaction (where possible)

**API Design Guidance (Forsgren)**: Lane-specific — e.g., standard response headers for tracing, idempotent scoring endpoints, fleet health endpoint, contract testing schemas.

**One Actionable Step for Today**: Single concrete action (e.g., "Stand up GitHub Actions CI pipeline with lint + tests + health check").

### 5. Part 4: Will Larson — CTO Leadership Advisor
Embody Larson's systems-thinking, sequencing, sustainable-pace perspective:

**Assessment**: Current prioritization, the principal-the principal feedback loop health, engineering capacity allocation.

**Recommendations** (sequenced, with clear tradeoffs):
- Sequence build: coaching engines first (focus on making 8D360, GAS v2.0, behavioral physics excellent)
- Adopt, don't build, health UI (use existing patterns, customize only where it exposes unique value)
- Embed cybersecurity as team property (PR reviews, automated scanning, coding standards - not separate team)
- Each recommendation should reflect systems-level thinking

**Tradeoffs**: Explicit articulation of what you gain, give up, and defer with each recommendation

**What to Watch**: Leading indicators that the approach is working (e.g., the principal in coaching engine code weekly, the principal-the principal alignment with psychological safety, sustainable work weeks)

**API Design Guidance (Larson)**: Lane-specific — e.g., sequence contracts in dependency order, don't spec all 25 engines simultaneously, one-page strategy document.

**One Actionable Step for Today**: Single concrete action (e.g., "Get the principal to approve or edit the Build-Direction Statement today").

### 6. Part 5: Balaji Srinivasan — Blockchain & Web3 Architecture Advisor
Embody Srinivasan's protocol-first, trust-assumption, patient-sovereignty perspective:

**Assessment**: Current consideration of blockchain/token integration, data ownership architecture, trust assumptions.

**Recommendations** (phased implementation path):
- Implement W3C Verifiable Credentials for coaching milestones (include GAS v2.0 geometric proof points)
- Design data model for patient-as-endpoint (FHIR-compatible export, portable formats)
- Defer tokenized health incentives until specific coordination problem exists (write token engineering doc first)
- Each recommendation should reference which protocol layer it addresses (settlement, data availability, identity, application)

**Implementation Path**: Clear phases with timelines (Now, 6-12 months, 12-24 months, 24+ months)

**Verdict**: Clear yes/no/defer with reasoning on blockchain readiness

**API Design Guidance (Srinivasan)**: Lane-specific — e.g., W3C VC issuance endpoint, FHIR export completeness, data deletion endpoint for consent revocation.

**One Actionable Step for Today**: Single concrete action (e.g., "Add verifiable credential issuance endpoint stub to API-CONTRACT.md").

### 7. Cross-Lane Synthesis: Where Research Converges
Identify where 2+ advisors see the same opportunity or threat - this is the highest-signal section. This is where you integrate insights across advisors to produce actionable, unified guidance.

Include these specific elements in your synthesis:

**Technical Priorities Ranked by Blocker Status**
- List and rank the most critical technical blockers preventing progress
- For each blocker: status, impact, and priority level (CRITICAL/HIGH/MEDIUM/LOW)
- Base this on actual system observation, not assumptions

**API Contract Guidance for ALL Engines**
- Synthesize API design guidance from all advisors into unified principles
- Cover all engines: 8D360, GAS v2.0, behavioral physics, self-healing, coaching
- Include versioning, error handling, logging, authentication, and metadata standards
- Provide engine-specific guidance where advisors diverge

**Build Direction Guidance**
- Affirm and emphasize key points from BUILD-DIRECTION-STATEMENT.md
- Add any additional emphases based on advisor insights
- Refine sequencing recommendations with specific timelines and milestones

**Infrastructure Recommendations**
- Organize by implementation horizon (Immediate, Foundation, Scaling)
- Prioritize based on blocker impact and implementation effort
- Include specific, actionable steps for each timeframe

**Integration Architecture for Perplexity Health UI**
- Describe layered architecture showing how components interact
- Detail data flow for key user journeys (check-in, advice request, scoring)
- Specify safety and quality mechanisms (confidence thresholding, fallback responses, audit logging)
- Define key integration points and their responsibilities

Look for convergence on:
- Technical excellence in coaching engine core before scaling
- Need for architectural separation and validation
- Importance of independent iteration capabilities
- Requirements for safe, rapid production operation
- Foundational data sovereignty patterns

### 8. ⚡ Top 5 Actions for Today
Format each as a table row:
| # | Action | Owner | Why It's Today |

Select the five highest-leverage, immediately actionable technical steps. Each should:
- Be completable same-day or within 1-2 days
- Address a verified gap or blocker
- Have a clear owner (the principal or the principal)
- State why it must happen today (staleness, blocking, safety gate)

### 9. Risk Register (NEW)
A table of top risks with severity (CRITICAL/HIGH/MEDIUM/LOW), mitigation strategy, and owner.
Include at minimum: hallucination risk, regulatory misclassification, scope creep, uninstrumented production, silent regressions, unapproved specs, premature blockchain.

### 10. Board Consensus Statement (NEW)
A closing paragraph synthesizing where all five advisors converge. The consensus should:
- Identify the shared truth across all lanes
- Distill to one or two sentences the team can act on
- Be quotable and memorable

## Report Writing and PDF Generation (CRITICAL)

### Writing the Report File

Use the `write_file` tool to write the markdown report to `/tmp/cto-review-YYYY-MM-DD.md`. The baseline-first gate does not block new file writes in `/tmp/` for report artifacts.

**IMPORTANT**: Always use today's date in the filename (YYYY-MM-DD format) to avoid overwriting previous reports.

### PDF Generation

After writing the report markdown, use the the specialist engine shared PDF generation script:

```bash
python3 /<workspace> \
  /tmp/cto-review-YYYY-MM-DD.md \
  /tmp/cto-review-YYYY-MM-DD.pdf \
  "CTO Advisory Board" \
  "AM"
```

The script accepts 4 arguments:
1. Input markdown file path
2. Output PDF file path
3. Document title (appears in header/footer)
4. Time period (AM/PM for morning/evening reports)

**Archive copies** to the panel's reports directory (optional, for record-keeping):
```bash
mkdir -p /<workspace>
cp /tmp/cto-review-YYYY-MM-DD.pdf /<workspace>
cp /tmp/cto-review-YYYY-MM-DD.md /<workspace>
```

### Final Output Format

Your final response MUST include: `MEDIA:/tmp/cto-review-YYYY-MM-DD.pdf`

This is the required delivery format for the cron job automation.

## Quality Gates

Before considering the review complete, verify:

- [ ] Each advisor section embodies their specific voice (not generic AI tone)
- [ ] All recommendations are specific, actionable, and technically grounded
- [ ] Each advisor section includes "API Design Guidance" and "One Actionable Step for Today"
- [ ] API design guidance covers ALL engines (8D360, GAS v2.0, behavioral physics, self-healing, coaching)
- [ ] "Current State Snapshot" section includes fleet status, API contract status, build direction status, and what changed since last review
- [ ] "Risk Register" table included with severity levels and mitigations
- [ ] "Board Consensus Statement" closes the report with a quotable synthesis
- [ ] Exactly one actionable technical step is highlighted as "#1 action today" in Executive Summary
- [ ] Top 5 Actions table includes owner and "why today" for each
- [ ] No AI telltales (no em-dashes, no "Furthermore/Moreover/Additionally")
- [ ] If a lane is quiet, explicitly state so (silence is signal)
- [ ] Report file written via Python terminal (not write_file, which is blocked)
- [ ] PDF generated via pandoc --pdf-engine=weasyprint and verified with `file` command
- [ ] Report archived to reports/ directory

## Common Pitfalls & How to Avoid Them

**Pitfall**: Treating coaching engines as monolithic backends instead of tool-callable services
**How to avoid**: Explicitly design each engine (8D360, GAS v2.0, etc.) as independent microservices with versioned APIs that the LLM orchestrates

**Pitfall**: Over-engineering the API layer before validating core user flows
**How to avoid**: Follow Ng's advice - "Ship v0.1 in weeks, not months." Start with simplest working version

**Pitfall**: Launching without proper observability in a health context
**How to avoid**: Instrument first - define SLOs for query latency and availability before first user deployment

**Pitfall**: Spreading engineering capacity too thin across parallel workstreams
**How to avoid**: Follow Larson's sequencing - focus exclusively on coaching engine excellence for defined period

**Pitfall**: Considering blockchain integration prematurely
**How to avoid**: Follow Balaji's path - implement verifiable credentials and data sovereignty patterns first, defer tokens

**Pitfall**: Conflating health information with medical advice in UI
**How to avoid**: Follow Topol's dual-track approach - release information tool first, validate scoring separately

**Pitfall**: Missing or corrupted coach files in the coaches directory
**How to avoid**: Check if the file is readable; if not, use the corresponding reference file from the skill's references directory (e.g., if `coaches/nicole-forsgren.md` is empty or unreadable, use `references/nicole-forsgren-advisor.md` instead).

**Pitfall**: PDF generation fails when using pandoc directly
**How to avoid**: Always use the custom `generate-pdf.py` script from `ds-wave-shared/scripts/` instead of calling pandoc directly. The script handles WeasyPrint rendering, header/footer styling, and the correct invocation pattern.

**Pitfall**: Working directory confusion — CRO and CTO advisory panel repos have similar names and structures
**How to avoid**: Always verify your working directory with `pwd` before reading files. The CTO panel is at `ds-wave-cto-advisory-panel-private`. Common confusion: starting in `ds-wave-marketing-advisory-panel-private` (marketing panel) instead. If you're in the wrong directory, use `cd` to navigate to the correct workspace.

## References\n\nThis skill references the following advisor profile files (copied to references/ for session-specific detail):\n- `references/andrew-ng-advisor.md`\n- `references/eric-topol-advisor.md` \n- `references/nicole-forsgren-advisor.md`\n- `references/will-larson-advisor.md`\n- `references/balaji-srinivasan-advisor.md`\n\nIt also references:\n- `references/architecture-overview.md` (from ARCHITECTURE.md)\n- `references/integration-patterns.md` (from INTEGRATION.md)\n- `references/june-18-2026-technical-review.md` (session-specific technical review from June 18, 2026)