---
name: health-scoring-improvement-cycle
description: Conduct periodic evidence-based improvement cycles for personalized health scoring systems (8D/TWC, EF COMPASS, related dimensions) to identify enhancements, analyze data pipeline issues, review scientific literature, and maintain improvement logs.
category: mlops
version: 1.1
---

# Health Scoring Improvement Cycle

Conduct periodic evidence-based improvement cycles for personalized health scoring systems (8D/TWC, EF COMPASS, related dimensions) to identify enhancements, analyze data pipeline issues, review scientific literature, and maintain improvement logs.

## When to Use
- Running scheduled health scoring improvement cycles (e.g., every 8 hours as required)
- After detecting data pipeline stagnation or scoring system issues
- When reviewing current scoring logic for potential evidence-based enhancements
- Prior to implementing changes to scoring algorithms, weighting, or interpretation
- When creating a new condition-specific support subscore, sidecar metric, or passive fusion overlay (e.g., ADHD/EF support score blended into a base TWC)
- When a subscore should *straddle multiple dimensions* rather than live inside only one dimension, and the goal is to model cascade effects, secondary impacts, and outcome spillover explicitly
- When the improvement needs to be visible end-to-end in API responses, CLI pretty-print, Telegram formatting, and dashboard outputs
- When revising a daily scoring system to be *passive-first* / manual-light so the user is not forced into frequent check-ins
- When maintaining longitudinal improvement tracking for health monitoring systems
- When designing or revising a **universal scoring framework** that must work for any person, starting with patient 0 calibration and later extending to other users with separate baselines
- When the scoring model should explicitly recognize mission-aligned positive-health work as a stronger PSY/SPI signal, while keeping that boost bounded and explicit
- When building or updating a **master activity ontology/database** that scores all common human actions (hydration, hygiene, nutrition, movement, outdoor exposure, spiritual practice, sleep support, social behavior, vocational behavior, environmental behavior, financial behavior) with evidence-weighted, personalized rules
- When the cycle needs to identify which sciences are being updated each run (for example hydration science, exercise science, sleep science, nutrition science, or mindfulness/stress science)
- When you need to model **synergistic or entourage-style effects** explicitly, with bounded interaction terms rather than hidden composite blending
- When preparing a **handoff spec for another AI** that must understand raw evidence, canonical score, confidence, display normalization, and interaction rules
- When a scoring system needs to be **cleanly refactored into a canonical spec plus supporting notes**, with deterministic math, universal JSON schema, interaction matrix, calibration rules, and invariants/tests separated into maintainable layers
- When implementing activity logging and caching systems for real-time scoring updates
- When developing validation frameworks for evidence-based health scoring
- **When incorporating insights from a biweekly horizon scan** (e.g., scientific literature review, competitive landscape analysis, framework structural assessment) to identify improvement opportunities for the scoring system

## Procedure

### 1. Review Current Scoring Logic and Data
- Check freshness of 8D/TWC data sources (transcript analyzer output, nutrition/sexual health logs)
- Review EF COMPASS scoring stagnation and evidence distribution patterns
- Examine standup drafts and transcripts for recent behavioral observations
- Verify pipeline cron jobs are functioning (post-standup cron, EF scoring cron, etc.)
- Confirm data integrity in unified health database and EF tracker databases
- Run pipeline gap detection queries to identify data coverage issues
- **Use internal state assessment queries** (see references/internal-state-assessment-queries.md) to establish baseline metrics
- **Conduct Scoring Maturity Index (SMI) assessment** to measure production readiness of the scoring system for external users:
  - Evaluate Engine Completeness (25 points): Check existence of rescore, nutrition, sexual health, and fleet TWC engines; verify interaction matrix implementation
  - Assess Test Coverage (20 points): Run rescore engine tests; verify all pass including double-count property test
  - Measure Validation Coverage (20 points): Confirm VERITAS audit panel exists, calibration file exists, universal methodology exists, PRD exists
  - Analyze Data Quality (20 points): Score days with real (non-carry-forward) scores; check nutrition, EF COMPASS, and sexual health coverage; assess activity database balance and interaction matrix completeness
  - Determine Production Readiness (15 points): Verify multi-user architecture, API/export capability, and documentation for external consumption
  - Calculate SMI = sum of domain scores (max 100); classify as Production Ready (85-100), Beta Ready (70-84), Alpha Ready (50-69), Lab Stage (30-49), or Pre-Product (<30)
  - Perform trajectory analysis by comparing with previous SMI scores from scoring-maturity-log.md
  - Identify blockers to launch and recommend highest-ROI actions
  - Log full results to scoring-maturity-log.md including date, SMI score, domain scores, and key findings
  - **Use the SMI assessor script** (`scripts/smi_assessor.py`) to automate this assessment

### 2. Conduct Horizon Scan (Biweekly)
Following the HORIZON agent mandate, perform a biweekly horizon scan to evaluate whether Divinity Science's approach is still the RIGHT approach:
- **Internal State Assessment**: Run SQL queries to get current methodology state (activity counts, dimension balance, scoring coverage, interaction matrix stats)
- **Horizon Scan — Scientific Literature**: Search for latest developments in key domains using web search or duckduckgo-search skill
- **Competitive Landscape**: Analyze competing frameworks (WHO-5, WEMWBS, Oura, Whoop, Happify, Woebot, Noom, etc.)
- **Framework Structural Analysis**: Evaluate if 8 dimensions are right, if TWC formula is optimal, if evidence grading is sufficient, if product architecture scales
- **Opportunity Identification**: Identify 3-5 specific opportunities, competitive advantages/gaps, scientific breakthroughs to integrate, product roadmap implications, and threats
- **Feed Into Governance**: Update methodology-evolution-log.md with findings
- **Deliver Findings**: Produce formatted horizon scan report

### 3. Identify 1-3 Improvement Opportunities
Look for specific, actionable improvements in these areas:
- **Evidence diversification**: Address over-reliance on single evidence types (e.g., >80% from one evidence type indicates need for diversification)
- **Temporal sensitivity**: Enhance detection of meaningful change vs. measurement noise (MDC thresholds)
- **Condition-specific metrics**: Add biomarkers relevant to the principal's diagnoses (ADHD, BP2)
- **Pipeline reliability**: Fix broken data flows (stale 8D/TWC data, missing nutrition/sexual health logs, cron job failures)
  - For synchronization scripts: Implement carry-forward mechanisms when today's data is missing
  - Add staleness tracking to highlight data freshness
  - Modify database schema to support new tracking fields as needed
  - Test fixes with historical data to ensure they don't break existing functionality
- **Clinical validity**: Align scoring with established medical/research guidelines
- **ADHD/EF specificity**: Improve discrimination between related domains (Activation vs Effort)
- **Circadian stability**: Add circadian rhythm monitoring as BP2 early warning signal

### 4. Research Evidence for Each Proposed Change
For each improvement proposal:
- Search leading universities, hospitals, research institutes, and clinical guidelines
- Prioritize systematic reviews, meta-analyses, RCTs, or consensus guidelines
- Avoid blog posts, opinion pieces, or unverified claims
- Document evidence quality (STRONG, MODERATE, WEAK)
- Note any mixed evidence or limitations in the research
- Focus on applicability to the principal's specific profile (ADHD combined, Bipolar 2, medications)

### 5. Route Changes Requiring Specialist Review
If a change affects math, weighting, labels, or psychological interpretation:
- Separate reviewers by domain: math/scoring, psychology/behavior, technology/systems
- Use the operator agent delegate_task to route to appropriate specialist agents
- Require elite-credential specialist review before recommending changes
- Keep each review focused on its specific domain
- Document reviewer feedback and required modifications

When the cycle is creating a new condition-specific support subscore, require the spec to explicitly define:
- the profile discovery step
- a strongly calibrated question bank with behavioral anchors and the intended response scale
- the canonical raw score
- the personalized/profile-weighted score
- any compensation/support-effectiveness layer
- confidence math and thresholds
- overlap tags / provenance for anti-double-counting
- baseline / smoothing / drift monitoring
- versioned output schema and invariants/tests
- explicit surfacing of new fields in API, CLI/Telegram, and dashboard layers so the support metric is visible end-to-end
- backward compatibility when the support payload is absent (base score must still render cleanly)
- a calibration plan for early users / patient 0 before broad rollout
- a split between *user-facing* question text and *internal* labels/mappings so the respondent only sees neutral questions, while domain names, calibration hints, and discriminator logic remain in the schema or branching docs
- optional follow-up discriminators written as plain questions rather than category-leading prompts
- a passive-first / manual-light daily capture design when the goal is long-term engagement rather than exhaustive self-report
- a confidence-gated micro check-in rule (ask 1–3 questions max; only when passive data is sparse, confidence is low, or the score changes sharply)
- a clear separation between passive signals, manual micro check-ins, and support-effectiveness feedback so the user is not asked to repeat the same evidence in multiple forms
- an explicit confidence rule for every TWC and standalone score: confidence is always shown, increases as more supporting data accumulates, and is treated as a first-class output rather than a hidden implementation detail
- for cascade-style support metrics, an explicit multi-dimension impact map that names the primary dimension, secondary dimensions, straddle set, outcome spillovers, and any downstream calibration weights
- an explicit interaction layer for synergy/entourage-style effects, with bounded terms, caps, and provenance so one signal cannot silently inflate multiple outputs
- a versioned schema for the support metric block itself, so API, CLI, Telegram, and dashboard consumers can render richer breakdowns without breaking when the payload is absent
- a patient 0 calibration protocol before extending the framework to additional users

### 6. Maintain Improvement Running Log
After every cycle, append to `~/your-workspace/health-private/8d-improvement-running-log.md`:
- Timestamp of the cycle
- What was reviewed (specific systems and data examined)
- What changed or was proposed (with 8D/TWC mapping when applicable)
- Why it matters (clinical or operational significance)
- Evidence quality summary
- Open questions / missing information
- Cumulative update count

### 7. Deliver Summary to the principal
Provide a concise summary with these sections:
- **## Current Update**: What was found in this specific cycle
- **## Running List Update**: Summary of all work over time with update count
- **## Proposed Scoring/Tracking Changes**: Detailed proposals with 8D mappings
- **## Evidence Summary**: Quality of evidence for each proposal
- **## Open Questions / Review Needs**: What still needs investigation
- **## Next Run Priorities**: Focus areas for the next cycle

Keep tone concise, rigorous, and implementation-oriented. Use TWC/8D logic when possible and explain any new score/sub-score ideas clearly.

### Evidence Standards
- **STRONG**: Systematic reviews, meta-analyses, RCTs, consensus guidelines from leading institutions
- **MODERATE**: Single high-quality studies, well-established theories with some empirical support
- **WEAK**: Preliminary evidence, expert opinion, or limited studies
- Always note when evidence is mixed or inconclusive
- Prefer human studies over animal studies when applicable
- For digital phenotyping and sensor-based evidence, prioritize validation studies with clinical correlates (e.g., correlation with clinical assessments, ecological momentary assessment)
When changes require specialist validation:
1. **Math/Scoring**: Route to FORGE or VERITAS agents for algorithm/validation review
2. **Psychology/Behavior**: Route to SAGE or domain psychology specialists
3. **Technology/Systems**: Route to FORGE or GRAVITY agents for pipeline/architecture review
4. **Medical/Clinical**: Route to AISHA-MD with specialist consultation (HALO, DARK-MATTER, etc.)
5. Each review must return specific, actionable feedback before proceeding
6. Document all reviewer input and how it was incorporated

## 8D/TWC Mapping Guidelines
- If a proposal maps cleanly to an existing 8D/TWC dimension, state exactly how
- If not, propose the closest mapping and explain the gap
- Consider both primary and secondary dimension effects
- Note any cross-dimension interactions or cascade risks
- Align with the principal's baseline values and known score adjustments from her health profile
- Reference existing calibration.json rules when modifying or adding metrics

## Running Log Format
Each update should include:
- ## Current Update: What was found in this specific cycle (reviewed systems, key metrics, data pipeline status)
- ## Running List Update: Summary of all work over time with update count
- ## Proposed Scoring/Tracking Changes: Detailed proposals with 8D/TWC mappings when applicable
- ## Evidence Summary: Quality of evidence for each proposal (STRONG/MODERATE/WEAK)
- ## Open Questions / Review Needs: What still needs investigation or specialist review
- ## Next Run Priorities: Focus areas for subsequent cycles

## Output Requirements
Deliver summary must show:
- TWC composite + 7-day average + trend (if data available)
- 8D dimensions: score, visual bar, baseline (with staleness warning if applicable)
- EF COMPASS: overall score, 7 domains with scores + natural capacity
- Evidence count and clinical assessment with recommendations
- Clear visualization of proposed changes' impact on scoring
- Actionable next steps with owners and timelines
- Sciences Updated This Cycle (brief bullet list of scientific domains reviewed)

## Pitfalls to Avoid
- Never assume SOUL.md data reflects current reality (verify with the principal)
- Never finalize scoring alone — requires expert panel validation
- Never use Anthropic models for database operations
- Never hand-compute scoring math — must use deterministic engines
- Never add items the principal hasn't explicitly committed to
- Never ignore evidence distribution skews (e.g., >80% single evidence type)
- Never overlook circadian rhythm importance in BP2
- Never disregard minimum detectable change thresholds for EF domains
- Never skip specialist review for changes affecting scoring interpretation
- Never allow health data to leave local-only storage (PHI protection)
- Never trust carry-forward TWC/8D rows as real scores — check source column before trend analysis