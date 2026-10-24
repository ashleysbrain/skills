---
name: open-core-skill-architecture
description: Use when turning a broad domain workflow into a reusable skill with an open-source core, a premium moat, and a clear release boundary. Design the skill family, package the open layer, and keep proprietary intelligence out of the public skill.
version: 1.1.0
author: the operator agent Agent
license: MIT
metadata:
  hermes:
    tags: [skills, open-core, productization, architecture, release, boundary]
    related_skills: [hermes-agent-skill-authoring, subagent-driven-development, skill-update-engine]
---

# Open-Core Skill Architecture

## Overview

Use this skill when a user wants to turn a domain workflow into a skill that can be shipped publicly without giving away the premium system behind it.

The goal is to create a **class-level umbrella skill**: a reusable, durable skill that defines the public workflow, the boundary between open and premium layers, and the release shape. The skill should make the public layer genuinely useful on its own while making the hosted or proprietary layer feel like a natural upgrade.

When using this skill for strategy or release review, **state the expert lens stack first** before the recommendation. Do not stay generic. Name the actual operating roles (for example: FORGE, ARBITER, PARALLAX, SENTINEL, NEXUS, plus the open-core product strategist lens) so the user can see which credentials are driving the answer.

## Release Identity and Versioning

Use explicit release metadata rather than vague labels like "V1" or "supporting doc".

When a product-line name is clarified or standardized, update the *entire release surface* rather than only the title:
- headings
- identity lines
- inline references
- file names/slugs when they are part of the public surface
- any duplicate alias chains like `X / X` or `X / X only`

After a rename pass, verify the intended surface with a targeted search so the legacy label is actually gone where it should be.

Preferred format:
- `[Family] — [Release Class] — v[SemVer] — [Release Date]`

Release classes:
- `core` = primary user-facing skill
- `support` = QA, guide, reference, helper layer
- `bridge` = migration, compatibility, redaction, connector
- `fork` = derivative variant of an existing skill
- `ops` = internal workflow or fleet utility

Ranking rule:
- compare candidates against the **current stable core anchor** for that family, not a fixed first version
- when a newer core release ships, update the anchor and re-score future support/bridge releases against it

See `references/release-versioning.md` for the compact release spec.

This is especially useful for health, finance, productivity, and agentic workflows where the public version should build trust and adoption, but the premium version contains the calibrated intelligence, memory, or automation that creates the moat.

## When to Use

Use this skill when:
- a broad workflow needs to become a public skill without exposing proprietary logic
- you want a reusable open-core package instead of a narrow one-off skill
- you need a clear boundary between public utility and premium intelligence
- the release should drive adoption, trust, and conversion at the same time
- multiple candidate skills need to be merged into a cleaner umbrella design
- a workflow has a public standard layer and a private intelligence layer

Do **not** use this skill for:
- trivial prompt rewrites
- one-off demos with no reusable future
- pure coding tasks that do not involve skill packaging or boundary design

## Core Design Pattern

### 1. Define the public promise
Write the one thing the public skill must do extremely well.

Examples:
- normalize messy inputs into structured state
- summarize trends with safe next steps
- generate a handoff-ready report
- provide a lightweight but trustworthy daily workflow

If the promise is too broad, the skill becomes generic and unmoored.

### 2. Separate open and premium layers
The public skill should include:
- intake and normalization
- safe summaries
- explainable outputs
- baseline or trend framing
- templates and checklists
- escalation rules when safety matters

The premium layer should keep:
- personalized calibration
- private weights or scoring logic
- memory and longitudinal synthesis
- advanced automation
- richer dashboards or hosted-only workflows
- proprietary thresholds and scoring rules

### 3. Package the skill as a family
Prefer a small suite over a monolith:
- one skill for intake / normalization
- one skill for interpretation / summarization
- one skill for safety / escalation
- one skill for premium bridge / upgrade path

This makes the open layer easier to understand and the premium layer easier to justify.

When you order a family for release, do not rank by raw readiness alone. Use the current stable core as the anchor and compare candidates against that family anchor.

Use explicit release classes so the family does not fragment:
- `core`
- `companion`
- `support`
- `bridge`
- `fork`
- `ops`

When reviewing candidates, state the relevant role lenses explicitly instead of saying only "architect" or "assistant": for example, FORGE, ARBITER, PARALLAX, SENTINEL, and NEXUS when that is the right panel for the task.

### 4. Put durable knowledge in references/
Use references for:
- boundary maps
- release examples
- session-specific findings
- implementation checklists
- repository quirks
- copy-ready launch wording
- sequential panel review rules
- canonical persona aliasing rules for public-figure-inspired advisors
- master routing maps and repo-to-repo handoff artifacts when a workflow is split across multiple private repos

Keep the main SKILL.md focused on the reusable workflow.
See `references/sequential-panel-and-aliasing.md` for the reusable panel sequencing and aliasing pattern.
See `references/public-lane-routing.md` for the dedicated-profile + topic/thread routing pattern for public test lanes.

### 5. Preserve the moat
- Do not publish the calibration engine, secret heuristics, or premium decision logic.
- Do not imply that the model has real credentials or licensure it does not have.
- Use expert *lenses* for reasoning; keep the public layer transparent about uncertainty and safety.
- Prefer class-level umbrella skills over narrow one-session artifacts.
- Keep session-specific detail, examples, and quirks in `references/` so `SKILL.md` stays reusable.
- If you are building a family of private advisory repos, encode the handoff path as a repo-local artifact in the receiving repo instead of relying on chat history alone.
- Keep `COACHING_CONTEXT.md`, `COACHING_QUESTIONS.md`, and a short handoff note in the receiving repo when an upstream board review needs to drive downstream next steps.
- If two candidate skills overlap, note the overlap and broaden the umbrella instead of fragmenting the library.
- If a skill needs a thoroughness pass, deepen the public workflow and the support files together instead of inflating one while leaving the other thin.
### Safety-guarded recommendation engines
When the skill’s job is to recommend rather than merely summarize, make the open layer explicitly safety-first:
- triage for red flags before any recommendation
- separate facts, interpretation, and speculation
- state confidence and missing information
- choose conservative defaults when evidence is partial
- include escalation guidance in the standard output
- use expert *lenses* for reasoning, not fake credentials or implied licensure
- route through a panel when one lens is likely to overreach or when safety is ambiguous
- if multiple lenses are needed, run them **sequentially** unless the user explicitly needs a synthesis panel
- keep the final answer short, concrete, and actionable
- expose the public signal logic, but keep calibration weights, hidden thresholds, and private scoring rules out of the open layer
- a simple public heuristic is acceptable when it helps reviewability: `recommendation_score = (signal_strength × confidence) / (friction + 1) - risk_penalty`

See `references/safety-guarded-recommendations.md` for the compact output schema, signal interpretation order, and boundary rules.
See `references/persona-architecture.md` for specialist AI lens roles, naming rules, and panel workflow.

## Release Strategy

A strong open-core skill release should do four things:

1. **Be useful immediately**
   - The open layer should help a user today without setup friction.

2. **Show a visible standard**
   - The skill should define a clear workflow or schema that others can adopt.

3. **Create a natural upgrade path**
   - The premium layer should feel like "more intelligence, more memory, more automation," not a different product.

4. **Preserve the moat**
   - Do not publish the calibration engine, secret heuristics, or premium decision logic.

### Release triage for existing candidate skills

When you are choosing *which* existing skill to ship now, use the same open-core lens before you decide:

- Prefer the most **self-contained class-level umbrella** that another user can understand and use immediately.
- Rank candidates by **public utility**, **safety/privacy boundary**, and how little private calibration or internal infrastructure they expose.
- If the strongest candidate is still too narrow or internal, broaden the umbrella and move the session-specific detail into `references/` instead of creating a one-off public artifact.
- If two skills clearly overlap, call that out and defer consolidation to the curator rather than pretending they are unrelated.
- For safety-sensitive domains (health, legal, finance, wellbeing), prefer shipping a safer public layer first: intake, normalization, reporting, snapshotting, and explicit escalation rules. Keep recommendation/scoring logic private until it has been validated as trustworthy.
- Do not ship a recommendation or scoring engine publicly unless the open layer is safe and genuinely useful on its own.
- A simple public heuristic is acceptable only when it helps reviewability; do not let it replace the real engine contract.
- For support releases, bundle a release pack with sample outputs, a test suite, a template, and launch positioning copy in `references/` or `templates/`; generate a PDF handoff pack when the release is meant for human review.

See `references/release-triage.md` for a reusable checklist and ranking rubric.

## Common Pitfalls

1. **Shipping a generic assistant**
   - If the skill can be described as "talk about X," it is usually too broad.

2. **Leaking the moat in the public layer**
   - Publish the workflow and outputs, not the private calibration or scoring internals.

3. **Overloading one skill with too many jobs**
   - Split into an umbrella plus support skills when intake, interpretation, and escalation are distinct.

4. **No explicit premium bridge**
   - If the public skill never hints at what the hosted layer adds, conversion will be weak.

5. **Storing session-specific notes or dense taxonomies in the main SKILL.md**
   - Keep the main skill stable; move details into `references/` so the umbrella survives iteration.
   - If the skill needs a long keyword bank, dimension map, cue dictionary, or release-packaging checklist, put it in a reference file and keep the main skill focused on the workflow class.

6. **Renaming the file path but not the release text**
   - Fix: rename the artifacts first, then search the whole package for old labels like V1/V2 or legacy product names, update body text/headings/identity lines, and verify the final file list.
   - Do not treat the rename as complete until the old label is gone from titles, references, inline copy, and alias chains.

7. **Leaving duplicate alias chains in place**
   - Fix: collapse redundant forms like `X / X` or `X / X only` to the canonical product name before verifying.
   - If a section is firewalled or intentionally historical, preserve the old label only there and make the exception explicit.

8. **Letting multi-repo workflows live only in chat**
   - When a broad workflow is split across multiple private repos or panels, create a durable master routing map and repo-local handoff notes.
   - Put the cross-repo map in a reusable artifact instead of expecting the next session to reconstruct the routing from memory.
   - If one repo’s output is intended to feed another repo, write the handoff explicitly in the downstream repo so the upstream review becomes usable context.

9. **Using partial-file edits without re-reading the file**
   - Fix: if a file was read with pagination, re-read the relevant section or the whole file before overwriting it again.

10. **Using the default lane for a public test surface**
   - When a user wants to simulate public usage, create a dedicated the operator agent profile and route it to its own Telegram home channel or forum topic/thread.
   - Prefer a separate lane over prompt-only isolation; verify the lane with `hermes profile show <name>` and `hermes gateway status` before treating it as live.
   - Keep the channel/topic routing details in a reference file so the umbrella skill stays reusable.
   - For Telegram groups, bind the test lane to a *forum topic/thread* via `group_topics` rather than using the group root as the public surface.
   - Treat the root chat as a lobby/safety surface only; the public lane should be the dedicated topic/thread itself.
   - If the lane is meant to stay public-facing without taking over the group root, make the topic explicit in the config and keep the root untargeted.

11. **Using non-standard `attachments/` directory**
   - the operator agent skills use three standard support directories: `references/`, `templates/`, and `scripts/`. The `attachments/` directory is non-standard.
   - Files in `attachments/` are often invisible to manifest reconciliation patterns that grep only for `references/` paths.
   - If a skill accumulates files in `attachments/`, flag it for directory normalization: migrate content to the correct standard directory and update the manifest.

12. **Leaking premium skill names in public frontmatter**
   - The `related_skills` field in YAML frontmatter is visible if the skill is ever published or shared.
   - If a public skill lists premium-only skill names (e.g., internal scoring pipelines, proprietary tools), those names expose the private namespace.
   - Use generic labels for premium references in public skills, or omit them entirely.

14. **Leaving reference files accumulate past 15 in a single skill**
   - When a skill accumulates more than 15 reference files, it becomes harder to navigate and maintain, and can cause single-job execution stalls during skill update engine scans (see skill-update-engine risk R16).
   - Session-specific editing notes, rendering corrections, and tailored examples are common culprits.
   - When approaching 15+ reference files, consolidate related session-specific files into 2-3 authoritative references (e.g., five report-editing notes → one `report-editing-guide.md`).
   - This maintains information accessibility while reducing maintenance overhead and preventing execution stalls.
   - Example: The 8d-pattern-awareness skill (v1.1.7) has 21 reference files and would benefit from consolidating report-related references into 2-3 thematic guides.

15. **Ordering a skill family release by "wow factor" instead of usage dependency**
   - When planning a multi-skill release schedule, the instinct is to lead with the flashiest skills (creative output, design, humanizer) to grab attention. This is wrong for adoption.
   - If a user installs the creative pipeline before the dispatch and state management foundation, the pipeline runs on a system that can't route tasks, handle crashes, or verify output. The user blames the skills and uninstalls.
   - **Correct ordering is usage-first, not marketing-first:** Foundation skills (routing, dispatch, state recovery, verification) → Process skills (calibration, mode switching, project management) → Output skills (humanizer, panels, design). Each phase depends on the one before it.
   - The "wow factor" skills belong in week 3, not week 1. They are the payoff for the foundation, not the hook.
   - The release story should follow the dependency chain: a user who installs in order never hits a wall where a skill fails because its prerequisite wasn't there.
   - User correction (2026-06-21): "If we are wanting the user to have fancy processes but don't help them build out the foundation for the process to flow efficiently then the user will crash their system or it won't flow correctly. Should we look at this from a usage perspective?"

14. **Neglecting to verify the support file manifest**
    - Fix: run the verification script `scripts/verify-manifest.sh` periodically to ensure the manifest list in SKILL.md matches the actual files in references/, templates/, scripts/, and attachments/ directories.

## Benchmark-as-Authority Strategy (the "Harvey / Legal Agent Bench" pattern)

A specific open-core release shape: **release a self-validating benchmark that creates category authority without requiring domain credentials.** This is how Harvey became the legal-AI authority — not by having law degrees, but by open-sourcing Legal Agent Bench, a benchmark anyone could run and score against. The benchmark *generated* the authority; it did not depend on pre-existing authority.

### When this pattern applies
- The user asks "what is our equivalent of [competitor's benchmark]?" or "what can we release to get credibility in [community]?"
- You have an asset that is engineering-measurable but you lack domain credentials (clinical, legal, financial) to claim authority directly.
- The goal is community credibility + leaderboard adoption, not product sales.

### The Harvey test (four conditions for a self-validating benchmark)
A candidate benchmark qualifies only if ALL four hold:
1. **Self-validating** — the scoring is mechanical and reproducible; anyone can run it without trusting your expertise.
2. **Falsifiable** — it contains a prediction or scoring that *can fail*. A benchmark that can't be broken is marketing, not a benchmark.
3. **Authority-creating, not authority-dependent** — it should not require credentials to validate (no "on what basis do you define a planted pathology?"). If a domain expert can invalidate the benchmark by questioning your standing, it's the wrong benchmark.
4. **Category-defining** — it creates vocabulary others adopt. The real moat is the term/definition, not the code. Every paper using your term cites you.

### Critical pitfall: do NOT map the benchmark onto the domain you aspire to authority in
The failure mode (observed 2026-08-13): proposing a "Health Agent Bench" built on clinical scoring + synthetic patient cases. This requires medical authority to validate and any clinician can puncture it. **Map the benchmark onto the engineering property where you actually have authority** — in DS's case, biological isomorphism and cascade resilience (architecture, not health outcomes). The benchmark should showcase what you *built*, not what you *want to be credible at*.

### Candidate evaluation — discard criteria
- **Too generic** (e.g., "multi-agent coherence benchmark") → can't own the category, already crowded.
- **Subjective scoring** (e.g., "specialist panel reasoning quality") → no mechanical reproducibility, devolves into Chatbot Arena.
- **Already-killed branding** (e.g., "physics-informed") → if a prior branding panel killed the term as externally puncturable, don't relitigate.
- **Standalone taxonomy without a leaderboard** → a taxonomy creates vocabulary but no competitive surface. Ship it *inside* the benchmark as the scoring rubric.

### Document format for this class of strategy doc
- **Short.** principal-level: ~3 pages, under 10KB. Explicit length ceilings are a hard constraint ("not another 16KB").
- Lead with the one-sentence answer, then explicitly reject prior approaches and explain *why* they were rejected.
- Ground every claim in **actual runnable code/assets**, not theoretical assertions. The strongest move is "this is already built" — verify by running the code, not by asserting it exists.
- One decision asked of the principal at the end. Not five moves.

### Reference: the DS application
See `references/benchmark-as-authority-harvey-pattern.md` for the full DS case study: Physiomorphic Isomorphism Benchmark (PIB), the rejected clinical-frame analysis, the isomorphism score + cascade failure simulator as the benchmark engine, and the falsifiable prediction P1.

## Verification Checklist

- [ ] The skill describes a reusable workflow class, not a one-off project
- [ ] The open layer is useful on its own
- [ ] The premium boundary is explicit but not overexposed
- [ ] Session-specific details live in `references/`
- [ ] Any templates or starter files live in `templates/`
- [ ] Any deterministic checks live in `scripts/`
- [ ] The release path creates trust and a natural upgrade path
- [ ] The skill is narrow enough to be understandable, but broad enough to reuse
- [ ] Specialist AI lenses are named and scoped without claiming human identity or real credentials
- [ ] If a rename or rebrand happened, legacy labels were searched out and removed from the intended public surface

## References

- See `references/open-core-boundary.md` for a concise boundary map and packaging rules.
- See `references/release-patterns.md` for open-core launch patterns and anti-patterns.
- See `references/release-versioning.md` for the hybrid versioning scheme, release classes, and current-anchor coherence rule.
- See `references/safety-guarded-recommendations.md` for recommendation-specific safety and output guidance.
- See `references/human-language-taxonomy.md` for how to keep dense cue banks human-first and move them into `references/`.
- See `references/class-level-skill-shape.md` for the preferred umbrella-skill shape, maintenance flow, and anti-fragmentation rules.
- See `references/public-lane-routing.md` for the dedicated-profile + Telegram topic/thread routing pattern for public test lanes.
- See `references/cross-repo-advisory-handoffs.md` for the repo-local handoff pattern when one advisory board’s review must drive another board’s next steps.
- See `references/release-handoff-renaming-hygiene.md` for the rename + verification checklist when release package labels change.
- See `references/biological-abstraction-framework.md` for the translation table mapping private internal methodology names to public skill names, the discretion rules for releasing internally-inspired skills without exposing proprietary architecture, and the usage-first release ordering framework.
- See `references/ip-encryption-protocol.md` for the full 5-layer IP encryption protocol for ALL external-facing organism content (courses, marketing, docs, open-source). Covers terminology firewall, black-box exercises, toy implementations, crown jewel protection, cohort NDA, and the pre-publication reverse-engineering checklist. Proven on the L&D curriculum panel deployment (2026-07-02).
- See `references/benchmark-as-authority-harvey-pattern.md` for the benchmark-as-authority release shape: the Harvey test (4 conditions for a self-validating benchmark), the DS application (Physiomorphic Isomorphism Benchmark / PIB), the clinical-frame pitfall, and the candidate discard criteria.

## Release Identity
- `Open-Core Skill Architecture — support — v1.0.3 — 2026-06-12`
- Public role: reusable skill architecture for open-core design
- Public promise: guide the creation of reusable skills with a clear open/public layer and premium/moat boundary
