---
name: technical-research-planning
description: Conduct structured research to evaluate technologies, platforms, and approaches for building a specific system, including surveying existing solutions, researching relevant standards and frameworks, assessing trade-offs, checking existing assets, and producing research documentation with recommendations and implementation plans.
version: 1.0.0
author: the operator agent
license: MIT
metadata:
  hermes:
    tags: [research, technical-evaluation, planning, documentation, technology-assessment]
---

# Technical Research and Planning

Use this skill when you need to evaluate options for building a technical system or platform, gather current facts from official sources, and produce research documentation that informs implementation decisions. For a concrete open-core commercialization example, see `references/open-core-commercialization.md`.

## When to use

- User needs to evaluate options for building a technical system or platform
- Research requires gathering current facts from official sources, documentation, and existing codebases
- Goal is to produce a research document that informs implementation decisions
- Task involves comparing multiple alternatives and recommending an approach
- You need to build on previous research in recurring cycles (e.g., weekly research jobs)
- You are conducting structured research for open-source platforms, showcases, or marketplaces
- You need to audit existing codebases for reusable assets before building new components
- You need to choose the best release candidate from several existing skills or artifacts and want a class-level recommendation rather than a narrow one-off pick
- User asks for a **strategic foresight brief** — mapping capability evolution timelines, identifying the next paradigm after the current state, or producing a product hypothesis for a specific buyer (SpaceX, NASA, enterprise). See `references/strategic-foresight-brief-pattern.md` for the foresight-specific workflow and `references/strategic-intelligence-brief-template.md` for the general brief format.

## Workflow

### 1. Clarify the vision and requirements
- Understand the core vision and goals of the system to be built
- Identify key user needs and use cases
- Note any constraints or non-negotiable requirements

### 2. Survey existing solutions and platforms
- Research open-source projects, commercial products, and community initiatives in the relevant space
- For each solution, note:
  - License and accessibility
  - Technology stack and architecture
  - Level of activity and community support
  - How well it matches the vision (fit assessment)
  - Potential to borrow patterns or components
  - Any red flags (e.g., licensing issues, abandonment)
- For deep literature or model-discovery work, use a sequential specialist panel rather than a single generic research pass so each stage can preserve and verify detail before synthesis

### 3. Research relevant technologies and standards
- Investigate data formats, protocols, and standards relevant to the domain
- Explore enabling technologies (e.g., specific libraries, frameworks, cloud services)
- Review privacy, security, and compliance frameworks that may apply
- Identify reference implementations or best practices

### 4. Assess agentic/AI applicability (if relevant)
- Research how AI/agentic technologies could be applied to the use case
- Look for existing patterns of usage in similar systems
- Identify gaps where new agentic approaches could provide value
- Consider portability and interoperability of agent configurations

### 5. Evaluate data portability and standards
- Research relevant data exchange standards (e.g., FHIR, HL7, specific JSON schemas)
- Investigate data ingestion paths from common sources (wearables, health platforms, etc.)
- Look for synthetic data generators or demo datasets that could be useful
- Assess export capabilities for user data portability

### 6. Examine privacy and security considerations
- Research privacy-preserving techniques applicable to the data types involved
- Look for established frameworks and tools for data sanitization, anonymization, etc.
- Consider consent management, data subject rights, and compliance requirements
- Identify reference implementations or recommended approaches

### 7. Design system architecture and information flow
- Sketch high-level architecture showing major components and data flows
- Define information architecture (how users will navigate and discover content)
- Consider submission/review/publishing workflows if it's a platform
- Sketch core data models or schemas needed
- Plan for different runtime strategies (static vs dynamic components)

### 8. Audit existing assets and codebase
- Search for relevant existing work in the codebase that could be leveraged
- Identify documents, databases, schemas, or other assets that could seed the project
- Note any existing dashboard, scoring methodology, or data recipe work
- Determine what can be reused vs what needs to be built

### 9. Draft technical specifications and implementation plan
- Define core schemas, data models, or configuration formats
- Outline MVP feature list with priorities
- Propose a phased implementation timeline (e.g., week-by-week breakdown)
- Identify what could be built first to provide immediate value
- Note open questions that require human decision-making

### 10. Produce research documentation
- Create a structured research document with:
  - Executive summary
  - Competitive landscape analysis
  - Technology stack recommendations
  - Architecture options
  - MVP feature list and timeline
  - What already exists in the codebase
  - What the team could build first
  - Open questions for human review
  - Plan for future research cycles
- Include specific, actionable recommendations
- Cite sources and note where decisions are based on evidence vs assumptions

### 11. Translate research into open-core commercialization strategy when relevant
- Explicitly separate what will be open-sourced vs what stays proprietary.
- Define the brand/entity boundary if there is a parent lab and a product subsidiary.
- Map the revenue ladder: free standard → paid hosted product → API/enterprise/consulting.
- Call out low-friction distribution channels such as Telegram, mini-apps, and PWA/web.
- If the product includes avatars, game loops, or other engagement systems, describe how they also collect structured data with consent.
- For avatar-driven health products, enforce a hard split between the **private healing avatar** (human, user-representative, internal) and the **public/social avatar** (opt-in, may be creature-like or authentic human). Treat that split as part of the architecture, not just visual design.
- When packaging methodology for release, identify which layer becomes the community standard (open source/spec) and which layer remains the premium intelligence moat (hosted prediction, orchestration, premium assets, enterprise workflows).
- Revenue strategy is part of the architecture: include the monetization ladder in the first-pass recommendation instead of treating it as a downstream marketing exercise.
- For methodology-heavy docs, spell out the native math and the display math separately; do not let a friendly 1-10 summary replace the engine contract.
- For scoring-methodology deliverables, do not collapse the product into a single score. Keep the full score-family map visible, including sub-scores, optional/contextual families, confidence, and baseline logic.
- For pitch-pack or PDF deliverables, prefer a small number of combined artifacts (for example: master brief + technical appendix) over many fragments, unless separate audiences truly need separate entry points.
- When producing one-page whiteboard or roadmap visuals, design for **print-safe light backgrounds** and **box-fit first**: keep labels short, compress the last section first if overflow appears, and verify the exported PDF is still exactly one page.
- After generating PDFs, verify the extracted text for the exact phrases that matter to the release narrative and math contract; if bullets or symbols render poorly, rewrite the source with deterministic plain-English or hyphenated lines.
- If the user explicitly requested Telegram delivery, send the verified artifact proactively once it is ready; do not wait for a second reminder.
- For first-product release docs, include open-source recommendations inside the main narrative so the launch shape and the monetization boundary are obvious together.
- For pitch packs or launch briefs, put the parent-methodology vs commercial-product split on page one and repeat it on the appendix title page; do not bury the brand boundary later in the document.
- When revising a pitch pack or roadmap visual, update the source markdown/HTML/generator first, regenerate the PDFs from source, verify extracted text for the exact phrases that matter, and then send the verified artifact(s).
- For brand architecture, keep the parent methodology brand and the commercial product brand distinct in the recommendation; the research deliverable should state which entity owns credibility, standards, UX, and revenue.
- For launch strategy, recommend a narrow wedge and one daily loop before broader expansion; avoid generic category language until the core loop proves retention.
- When a user asks to "redo" a product document and visual, update the *source markdown first*, then regenerate the HTML/PDF derivatives from that source, then verify the rendered artifact. Do not stop after improving only the visual layout.
- Add a one-line pointer to any supporting reference files under `references/` for future runs, especially session-derived commercialization briefs and methodology lessons.
- See `references/divinity-health-open-core-methodology-lesson.md` for the session-derived release rules, score-family wording, and PDF verification pattern.
- See `references/divinity-health-whiteboard-roadmap-pattern.md` for the board-friendly science-to-revenue roadmap shape used for health-tech/gamification planning.
- See `references/divinity-health-launch-roadmap-pattern.md` for the open-core launch sequencing, brand split, and monetization ladder used in this session.
- See `references/divinity-health-whiteboard-delivery-pattern.md` for the compact one-page visual and Telegram delivery checklist used in this session.
- See `references/divinity-health-weekend-execution-board.md` for the compressed Saturday-noon dual-track launch board, owner/support checklist format, and PDF verification pattern.
- See `references/divinity-health-bootstrapped-marketing-roadmap.md` for the low-energy, low-budget marketing phase and one-page visual verification pattern used in this session.
- See `references/proof-first-content-engine.md` for the proof-first content engine pattern: collect evidence first, classify by trust level, then repurpose one proof event across multiple channels.
- See `references/strategic-intelligence-brief-template.md` for the multi-question strategic brief format (dense, word-counted, table-heavy research deliverables with fallback research ladder).
- See `references/strategic-foresight-brief-pattern.md` for the foresight-specific workflow: paradigm mapping, funding-signal tracking, product hypothesis framing for a named buyer, and path-to-attention steps. Complements the intelligence brief template.
## 12. For recurring research cycles (weekly/monthly):
- When analyzing creator or founder-led marketing content, extract the underlying content system, not just the surface opinion. Look for the proof source, the trust ladder, the repurposing loop, and the distribution channels.
- Build marketing around a proof vault: screenshots, demos, user quotes, founder insights, and product outcomes should be the raw material for all claims.
- Classify content by trust level so AI is used for packaging and scale, not as the truth layer.
- Prefer one strong proof event repurposed into many assets over many weak AI-generated assets with no evidence.
- If the source material includes gamification or engagement loops, separate **healthy retention mechanics** (streaks, progress, adaptive difficulty, cohort rewards) from dark patterns and document the guardrails.
- If the domain includes identity/avatars, document personal-vs-public avatar semantics explicitly; do not collapse them into a single character model.
- Prefer a Telegram-first or similarly low-friction bootstrap surface when the goal is rapid habit formation, early distribution, or validation without app-install friction.

### 11. For recurring research cycles (weekly/monthly):
- Load and reference previous research documents at start
- Explicitly build upon prior decisions rather than restarting from scratch
- Note if new evidence suggests changes to previous decisions
- Use clear versioning and dating (e.g., "-research-YYYY-MM-DD.md")
- Reference specific sections from prior research when applicable

## Tactics that worked

### When surveying platforms
- Create comparison tables with consistent criteria (license, stack, activity, fit, action)
- Clearly mark what to adopt, what to borrow patterns from, and what to avoid
- Note any licensing traps or compatibility issues early

### When researching standards
- Focus on the practical usability of standards (are there good libraries/tools?)
- Note versions and stability (e.g., FHIR R5 vs older versions)
- Look for reference implementations or starter projects

### When checking existing assets
- Use targeted searches (find, grep) for relevant file types and keywords
- Look beyond obvious places - valuable assets might be in research/ or database/ folders
- Document exactly what exists and how it maps to needed components

### When drafting implementation plans
- Order tasks by dependency (what needs to be built first?)
- Provide concrete, achievable goals for each time period
- Include success criteria for determining when a phase is complete
- Suggest what could be built in parallel vs sequentially

### When producing documentation
- Build on previous research documents if they exist (don't restart from scratch)
- Explicitly reference prior decisions and note if new evidence suggests changes
- Use clear versioning and dating for recurring research cycles
- Separate established facts from open questions requiring human input
- For printable math-heavy deliverables, use `references/printable-math-pdf-verification.md` as the source→PDF→vision QA pattern before shipping

### When researching privacy frameworks
- Evaluate both established tools (Presidio, Anonymeter) and emerging techniques
- Consider implementation effort vs privacy guarantees
- Map privacy techniques to specific data types (text, structured data, images)
- Note false positive/negative rates and mitigation strategies

## Output template

1. **Executive Summary** - Vision, opportunity, strategic positioning, recommended path
2. **Competitive Landscape** - Survey of existing solutions with comparison tables
3. **Technology & Standards Research** - Data formats, protocols, enabling technologies
4. **Agentic/AI Applicability** - How AI agents could be used (if relevant)
5. **Data Portability Standards** - Ingestion/export options, standards compliance
6. **Privacy & Security Frameworks** - Techniques, tools, and approaches considered
7. **Showcase/System Architecture** - High-level design, information architecture, data flows
8. **Existing Assets Audit** - What already exists in codebase that can be leveraged
9. **Technical Spec & MVP Plan** - Feature list, timeline, what to build first
10. **Open Questions** - Decisions needing human input
11. **Future Research Cycles** - Planned progression for recurring research jobs
12. **Appendices** - Detailed notes on specific topics as needed

### When web search is blocked — fallback research ladder

All major search engines (Google, Bing, DuckDuckGo) CAPTCHA-block requests from server/datacenter IPs. When web search returns CAPTCHA pages or empty results, escalate through this fallback ladder:

1. **Wikipedia browser navigation** — `browser_navigate` to `https://en.wikipedia.org/wiki/<Topic>` articles. Wikipedia articles are the most reliable source for company valuations, technology definitions, and historical context. Figure AI's $39B valuation was verified live via Wikipedia in a session where all three search engines were blocked.
2. **Direct site access** — navigate directly to known URLs (crunchbase.com/organization/X, goldmansachs.com/insights, company /press pages) via browser instead of searching.
3. **arXiv direct access** — `curl https://arxiv.org/list/cs.AI/2025` works even when search engines block.
4. **Training knowledge supplementation** — when real-time data is inaccessible, clearly state the limitation and supplement with training knowledge through the most recent cutoff, then flag for human verification of time-sensitive figures.

**Never report "no data found" when the blocker was an IP-level CAPTCHA — always try the Wikipedia/direct-site ladder first.**

### When producing dense intelligence briefs

When the user asks for a "brief," "intelligence brief," or specifies a word count:
- **Word count is a hard ceiling**, not a suggestion. Track it.
- Prefer tables over paragraphs for any comparative data (funding rounds, feature comparisons, market projections).
- Every line should carry a specific name, number, or date. No filler.
- Use headers per section with `##` — scannability is the format's purpose.
- Flag sources and data freshness limitations transparently at the bottom.

### Vocabulary constraints on DS deliverables

Some DS intelligence briefs and external-facing documents require **technology-only terminology** — no biological/organism metaphors. When the user says "no biological terms," "use technology analogs only," or "distributed systems language":

| Instead of... | Use... |
|---------------|--------|
| organism | multi-engine fleet / system |
| neural / neuron | dispatch node / processing unit |
| cortex / cognitive layer | orchestration layer |
| cognitive architecture | autonomy architecture |
| sensorimotor | sensor-actuator loop |
| nervous system | distributed control system |

Many DS skills use organism metaphors internally (organism, engine, dispatch). The brief OUTPUT for external audiences must NOT carry that vocabulary. This constraint is common for investor/partner-facing documents where plain engineering language is expected.

### Pitfalls

- Don't get lost in endless research; time-box each phase and move forward
- Don't ignore licensing incompatibilities - they can be showstoppers
- Don't overlook the importance of existing assets - they can give you a major head start
- Don't make recommendations without considering implementation effort and trade-offs
- Don't forget to plan for demo data or synthetic datasets so the system works out-of-the-box
- Don't skip the privacy/security analysis even if it seems like an afterthought
- Don't produce purely narrative summaries; include concrete facts, tables, and actionable items
- In recurring research, don't overwrite previous decisions without explicit justification
- Don't open-source the crown jewels by accident: when a methodology is commercially valuable, define the boundary between the community standard and the hosted/intelligence layer before recommending release
- Don't design retention with shame, coercion, or addiction mechanics; gamification in health products must reward consistency, recovery, and agency
- Don't treat revenue strategy as an afterthought in product research; packaging and monetization are part of the architecture
- Don't stop at the big-picture story: if the methodology has a native mathematical model, spell out the worked example and make the display layer explicit so engineers can implement it correctly
+- Don't collapse a deep academic question into a generic assistant answer; if the user asked for source-backed research and model extraction, preserve the staged specialist flow and keep peer-reviewed and public sources separated

## Validation checklist

- Have you verified key facts from official sources rather than inferred them?
- Have you compared alternatives using consistent criteria?
- Have you identified what existing assets can be leveraged from the codebase?
- Have you provided specific, actionable recommendations rather than just observations?
- Have you outlined a feasible implementation plan with clear dependencies?
- Have you separated established facts from open questions requiring human input?
- Does your document build on previous research rather than restarting from scratch?
- If open-core is involved, is the free/paid boundary explicit and economically coherent?
- If the product uses gamification, are the retention loops health-safe and agency-preserving?