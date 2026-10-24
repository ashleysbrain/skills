---
name: business-health-agent-architecture
description: Research-backed workflow for designing a master business-health agent that mirrors the human 8D model, scores a company as a living system, and later spawns subsidiary-specific child agents.
version: 1.0
---

# Business Health Agent Architecture

Use when building a master agent for company health, enterprise wellness, business-scoring, or organizational health modeling that must mirror the human 8D framework while remaining scientifically grounded.

## Trigger Conditions
- User wants a parent agent that scores a company first, then later spawns subsidiary-specific agents
- User wants a business-health framework that mirrors human 8D scoring with business analogues
- User wants literature-backed design for company health, organizational health, or enterprise wellness
- User wants a master profile plus blueprint for a new business-health agent
- User wants a first-company rollout and a later subsidiary spawn framework
- User wants a scientific gap audit of an existing 8D business-health model before spawning specialist panels for methodology
- User wants a business-only scorecore that can interconnect with private human and AI 8D systems through summary bridge scores
- User wants a simplified executive-friendly PDF or explainer that shows what the business score is made of without code or heavy math
- User wants a shareable methodology brief for a partner, subsidiary company, or second AI that needs to score a parent company and its subsidiaries with the same 8D backbone
- User wants to expand a business-health methodology PDF with a dimension-by-dimension evidence map, size-to-evidence matrix, or similar calibration aid
- User wants a methodology or scoring document split into a human explanation section and a separate AI operating-instructions section
- User wants a reusable blueprint that includes scheduled-task inputs, credentials/access placeholders, and operational data requirements for correct scoring
- User wants a deterministic organizational scoring engine draft with a JSON schema, validation tests, and PDF verification before delivery
- User wants a cybersecurity or cyber-risk organization-health score built from measurable evidence, not subjective vibes, using the same 8D-style calibration logic
- User wants the methodology to include a vocational intake layer that profiles the organization’s work identity, purpose, rhythms, and vocational wellness before scoring
- User wants the methodology to scale from solo operators to enterprise organizations without treating every organization like the same size
- User wants the blueprint to include an explicit agent registry, role/persona stack, adjustable credential bands, and process-familiarity requirements before calibration starts
- User wants the blueprint to include an explicit agent spawn sequence and a hard spawn-to-calibration gate
- User wants the quick operating summary or intake prompt to be updated when the spawn sequence changes so the short-form instructions stay in sync with the full blueprint
- User notices the quick summary is out of sync with the body and wants the spawn/register order fixed in the short-form instructions before delivery
- User wants the blueprint reviewed for implementability gaps, especially missing fields, ambiguous calibration selection, schema/template mismatches, or non-deterministic agent selection before delivery
- User wants the blueprint hardened so calibration-pack selection, role assignment, audit fields, and credential scales are deterministic and reproducible
- User wants a zero-ambiguity pass that converts vague fields into explicit integer scales, selection rules, and tie-breakers
- User wants the intake prompt, JSON schema, and blueprint body kept in sync so the short-form form fields exactly match the main spec
- User wants the final PDF/title/copy audited so no leftover project-specific names remain
- User wants the PDF export verified to be non-blank and to preserve visible section structure

## What This Skill Covers
- Literature-backed synthesis for organizational health and performance systems
- Mapping human 8D dimensions into company analogues
- Building a company-level master score and child-agent architecture
- Designing privacy-preserving bridge contracts to human 8D and AI 8D systems
- Keep the raw human and AI details in their own private lanes while sharing only summarized overall scores, confidence, trend, and provenance hashes
- Propagate the architecture into both the canonical repo spec and the Obsidian vault with linked MOCs and sibling notes
- Create partner-ready methodology briefs that another founder or AI can use to score a primary company and subsidiaries with the same 8D backbone
- Talent request filing for the master agent
- Create partner-ready methodology briefs that another founder or AI can use to score a primary company and subsidiaries with the same 8D backbone
- Split methodology docs into a human blueprint section and a separate AI operating-instructions section
- Draft the master profile and business-health blueprint
- Generate PDFs for both profile and blueprint


## Core Workflow

### 1. Survey the problem class
Before proposing a structure, determine:
- what company or companies are in scope
- whether the user wants a master parent agent, child agents, or both
- whether the rollout starts with one company and expands later
- what business data sources exist already

### 2. Research the literature first
Use scientific and management literature to ground the model. Prioritize sources on:
- balanced scorecards
- leading and lagging indicators
- complex adaptive systems
- psychometrics and measurement invariance
- resilience and performance management
- organizational health and workplace performance
- calibration against archival data

The goal is not citation padding. The goal is to ensure the business-health model behaves like a measurable system.

### 2b. Run a scientific gap audit
Before finalizing the architecture, explicitly ask:
- Does the 8D business map need a new core dimension, or are the missing constructs better handled as bridge layers?
- Which constructs belong to occupational/vocational science rather than the core scorecard?
- Which constructs belong to measurement governance, not the score itself?
- Which claims are legitimate, and which are too speculative for production use?

This audit should usually separate:
- core business dimensions
- human work-capacity bridge layers
- measurement integrity / governance layers

If a gap can be represented as a control or bridge, do not force it into a new dimension without evidence.

### 3. Design the 8D business analogues
Mirror the human 8D structure with company equivalents. A typical mapping is:
- PHY → operational health
- PSY → leadership and decision health
- ENV → infrastructure health
- SOC → relationship health
- SPI → mission health
- INT → learning health
- VOC → productivity and market health
- FIN → financial health

Keep the analogue set stable unless the user explicitly requests a new mapping.

### 3b. Add private bridge contracts when systems must interconnect
If the business model must connect to human 8D or AI 8D systems:
- keep raw human details in the human lane
- keep raw AI internals in the AI lane
- expose only bridge summaries to the business layer
- allow only overall score, confidence, trend, and provenance hash to cross the boundary
- treat bridge values as advisory inputs, not a replacement for business telemetry
- preserve bilateral contracts so the business layer can return only aggregate score feedback

### 4. Build the scoring logic
Recommended principles:
- use a weighted geometric mean or equivalent bottleneck-sensitive structure
- include coupling coefficients between dimensions
- separate leading indicators from lagging indicators
- include confidence or evidence-quality weights
- avoid one strong dimension masking a weak one
- preserve recency effects
- require calibration and backtesting
- make every comparison deterministic: explicit integer scales, explicit tie-breaks, explicit fallback rules
- when writing partner-facing methodology briefs, show the actual scoring flow in plain language: choose company type, choose stage, load calibration, score 8 dimensions, compute weighted TWC, add coupling, then roll up parent and subsidiary results
- when the document must be PDF-safe, use ASCII math for formulas instead of Unicode subscripts or special symbols

### 4b. Build the agent registry before calibration
If the methodology depends on human or AI scoring agents, define the agent roster before loading calibration.

Minimum order:
1. define the task family or scoring lane
2. choose the base model or operating mode
3. assign role and persona
4. set credential targets / bands
5. verify process familiarity
6. verify evidence-domain familiarity
7. record `spawned_by` and `spawned_at`
8. register the agent
9. mark calibration authorization
10. only then calibrate or score

Hard rule: a spawned agent is not calibration-ready until it is registered and authorized. A profile stub, draft roster row, or unregistered draft does not count as a real agent.

If the registry is missing or incomplete, calibration should not begin.

- Does an existing strategy agent already own this?
- Does an existing revenue, operations, finance, or health agent already cover part of it?
- Is the request truly for a new parent architecture, or just a new view layered on an existing owner?

If an existing agent can do the work, dispatch rather than spawning.

### 6. File the talent request if a genuine gap exists
When the master agent truly does not exist:
- create a talent request
- describe the company-health scope
- specify that the agent must be the parent of future subsidiary agents
- include the 8D business analogue requirement
- include scientific validation requirements
- include the first-company scope and any explicit exclusions
- if the methodology itself needs review, file a staged sequence: first occupational/vocational science, then math/physics scoring panel

Follow the OpenClaw talent gate before any spawn.

### 7. Draft the master profile
The master profile should include:
- identity and reporting chain
- gap filled
- deep role-specific credentials
- MBTI, Enneagram, Big Five
- core functions
- 8D business model mapping
- scientific validation section
- operational constraints
- subsidiary spawn mode

Keep the profile at the class level, not session-specific.

### 8. Produce a business-health blueprint
The blueprint should explain:
- why the model fits the literature
- the 8D business analogue mapping
- scoring architecture and confidence model
- data sources
- validation plan
- operating rules
- first-company rollout
- future subsidiary-agent architecture

### 9.1 Plain-Language Scoring Explainers
When the user wants a simplified PDF or handoff document for business scoring:
- state clearly that the entire scoring algorithm is based on analogues of the human 8D wellness model
- show how the AI chooses business type, company stage, and the right calibration pack before scoring each company
- explain parent company vs subsidiary separation so the AI scores each entity independently before rolling up results
- include the actual scoring algorithm in plain language, even if the document avoids heavy math
- map each human dimension to a business analogue in plain language
- explain what signals contribute to each score
- avoid code, formulas, or jargon unless explicitly requested
- if formulas are included, render them in ASCII-safe form so PDFs do not break on subscripts or Greek characters
- keep the core business score separate from personal, sexual, or unrelated domain material
- verify that the 8D backbone is visible in the final artifact, not implied only in the background

### 9.2 AI-Ready Business-Health Handoff Package
When the user wants a document another AI can directly ingest, include the operational spec, not just the narrative.

Best-practice structure:
- Part I: Human Blueprint — explain the logic, assumptions, calibration meaning, and interpretation rules
- Part II: AI Operating Instructions — provide step-by-step implementation, operating rules, output schema, and prompt block
- An operational appendix — include scheduled-task inputs, data freshness, and credential/access placeholders

Minimum contents:
- a dimension-by-dimension evidence map showing which signals support each dimension
- a size-to-evidence matrix showing how evidence requirements change from solo to enterprise organizations
- a dimension-by-dimension evidence map showing which signals support each dimension
- a size-to-evidence matrix showing how evidence requirements change from solo to enterprise organizations
- parent vs subsidiary separation rules
- business type selection rules
- stage selection rules
- weighted 8D score formula with coupling terms
- calibration-pack naming and selection rules
- an explicit pack-selection order using entity_role, business_type, stage, size_band, and risk_profile
- explicit agent spawn request fields and a spawn status field for registry rows
- deterministic agent selection rules with registry filters, minimum thresholds, tie-breaks, and selection-reason auditing
- integer credential scales for credential_level, process_familiarity, and evidence_domain_familiarity
- JSON schema for AI input/output
- calibration table template
- output schema with strengths, constraints, actions, owners, timing, and roll-up fields
- a paste-ready machine prompt block
- a pre-scoring input packet listing data sources, task cadence, access requirements, and organization-size band
- a vocational intake layer that asks what the organization is for, who it serves, what good work means, and what vocational wellness looks like
- organization-size scaling rules so the same model can handle solo, micro-team, mid-size, large, and enterprise entities
- an explicit agent registry that must exist before calibration begins
- a role/persona/credential stack for every scoring agent
- adjustable credential bands and process-familiarity thresholds by calibration pack
- role skill-match rules that determine which agent is allowed to calibrate, review, or arbitrate
- credential placeholders only; never hardcode secrets
- explicit fallback rules when no approved calibration pack exists
- explicit fallback rules when no approved calibration pack exists

Default scoring structure to include when requested:
- 8D dimensions: PHY, PSY, ENV, SOC, SPI, INT, VOC, FIN
- formula: weighted composite plus coupling terms, not a simple average
- business-type interpretation of FIN
- stage-dependent calibration differences
- a requirement to score parent and subsidiary separately before roll-up

If the user asks for a document the other AI can directly ingest, make the schema and calibration table explicit rather than implied.

### 9.3 Formatting and delivery checks
When rendering a methodology blueprint to PDF:
- genericize the title and cover so no project-specific names remain
- keep the human and AI sections visually separated
- ensure the PDF has visible body text, not a blank render
- verify the final file opens and contains non-trivial extracted text
- verify the quick operating summary is present in extracted text and that the spawn/register-first ordering matches the body
- if the companion intake prompt exists, update it in the same pass so the short-form instructions match the main blueprint
- if the regenerated PDF or extracted text still appears stale, rebuild and re-check the output before delivery
- if the brief includes a scoring appendix, make it *objective and evidence-led*: define the evidence hierarchy, scoring formula, dimension rubrics, and required inputs explicitly
- when adding a scoring appendix, prefer telemetry, logs, records, timestamps, and other operational artifacts over self-ratings or feelings
- include a clear anti-subjective rule when the model must not infer scores from vibes, mood, or other unsupported qualitative claims
- verify the appendix pages themselves render cleanly and are not clipped or collapsed during export
- if the regenerated PDF or extracted text still appears stale, rebuild and re-check the output before delivery
- if the brief includes a scoring appendix, make it *objective and evidence-led*: define the evidence hierarchy, scoring formula, dimension rubrics, and required inputs explicitly
- when adding a scoring appendix, prefer telemetry, logs, records, timestamps, and other operational artifacts over self-ratings or feelings
- include a clear anti-subjective rule when the model must not infer scores from vibes, mood, or other unsupported qualitative claims
- verify the appendix pages themselves render cleanly and are not clipped or collapsed during export

## Practical Design Rules
- Do not collapse company health into finance only
- Do not collapse company health into a dashboard of disconnected KPIs
- Do not use vague mission language without measurable indicators
- Do not compare companies until measurement stability is tested
- Do not spawn subsidiary agents until the parent architecture is defined
- Do not let the model drift away from the human 8D logic
- **For founder-driven organizations**: Organizational scorecards should NOT include direct interventions for founder Psychological (PSY) dimension — this is AISHA-MD's exclusive lane. Organizational interventions focus on VOC, PHY, FIN, etc. that unlock founder capacity.

## Overlap Notes
This skill overlaps with:
- `sibling-agent-talent-gate-protocol` for spawn decisions and talent gating
- `professional-agent-pdf-profiles` for profile PDF generation
- `qubit-gr-8d360-scoring-pipeline` for the underlying 8D scoring philosophy
- `references/health-insurance-methodology-differentiation.md` for a concise note on using methodology as a health-benefits moat

### Applied differentiation pattern for regulated health products
- Use the methodology as a *visible operating layer* that improves routing, explanation, partner matching, and reporting.
- Keep the regulated insurance core clean; do not let the methodology become hidden underwriting or an opaque denial engine.
- For market positioning, methodology should strengthen member experience and operational discipline, not just branding.
- For launch strategy, a narrow employer-first wedge (SMB / ICHRA / level-funded) is a cleaner starting point than broad consumer insurer economics.

Use this skill when the task is specifically about *business-health architecture* rather than personal health or generic agent spawning.

## Verification Steps
- Confirm the correct parent agent scope is defined
- Confirm the 8D business analogues are explicitly mapped
- Confirm literature-based rationale is included
- Confirm the talent request exists when a new agent is needed
- Confirm the profile is fully finalized before freezing the blueprint
- Confirm the blueprint reflects the correct default personality posture / mode for the master agent
- Confirm the profile and blueprint are written before PDF output
- Confirm the blueprint includes a dimension-by-dimension evidence map and a size-to-evidence matrix when the user wants a calibration-forward methodology brief
- Confirm the PDF title, cover, and visible text are generic and contain no leftover project-specific names
- Confirm the PDF opens with non-trivial visible content and is not blank or near-empty
- Confirm the PDFs were generated successfully

## Output Pattern
A complete run usually produces:
1. Literature-backed synthesis
2. Talent request
3. Master profile
4. Business-health blueprint
5. PDF exports
6. Short note about any overlapping skills that may need future consolidation

## Best-Fit Use Case
A user says, in effect:
- “Design the master business-health agent for my company.”
- “Mirror the 8D human model for enterprise scoring.”
- “Start with one company, then spawn subsidiary agents later.”
- “Research the literature first, then package it as a profile and blueprint.”

That is this skill.
