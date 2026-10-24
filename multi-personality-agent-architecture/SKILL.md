---
name: multi-personality-agent-architecture
description: Design and implement multi-personality agent systems where a single agent adopts different personality profiles for different work types, with work tracked per profile variant
tags: [agent-architecture, personality-systems, work-attribution, database-design, agent-management]
version: 1.0
---

# Multi-Personality Agent Architecture

## When to Use This Skill

- Building agent systems where different tasks require different personality traits
- Need to track which agent personality completed which work
- Agent work quality varies by task type
- Want to optimize agent-task matching over time
- User corrects approach: "agents aren't versioned linearly, they have personality dimensions"
- A front-door generalist seat must stay elite, variation-locked, and connected to executive guidance instead of collapsing into a generic helper
- The user wants a system agent to consult a COO / executive layer before routing or execution on meaningful tasks

## Core Concept

**Traditional (Wrong) Model:**
```
IP-SCRUBBER v1.0 → work A → upgrade → IP-SCRUBBER v2.0 → redo work A
```

**Multi-Personality (Correct) Model:**
```
IP-SCRUBBER (constant agent identity)
  ├── ISTJ-6w5-SEC-01 personality → did security audit work
  ├── ISTJ-6w5-SEC-02 personality → did compliance work (slight trait shift)
  └── ENTJ-8w7-SEC-01 personality → did crisis response (major shift)
```

## Key Principles

1. **Agent identity is constant** - "IP-SCRUBBER" doesn't change
2. **Personality profile varies by task** - different MBTI/Enneagram for different work
3. **Work attribution includes personality** - track which profile did which task
4. **Profiles are job codes** - `[MBTI]-[Enneagram]-[Domain]-[Variant]`
5. **Profile change = restart work** - ANY change affecting output invalidates in-progress work
6. **One persona per dimension** - do not collapse multiple dimensions into one generic role when the task needs specialist reasoning
7. **Run personas consecutively when the goal is synthesis** - if the output will be merged, let one persona finish before the next starts; do not run dimensions in concert or fan out parallel reads that contaminate each other
8. **Front-door seats stay elite** - when the user defines a lead intake/orchestrator seat, do not let it degrade into a generic assistant voice; keep credentials, methodology, and variation selection live on every meaningful task
9. **Executive guidance is part of routing, not an afterthought** - when the user links a seat to COO/executive guidance, encode that as a standing dispatch rule in the brain contract, not an optional note

## Implementation Steps

### 1. Define Personality Profile System

**Profile Code Format:**
```
[MBTI]-[Enneagram]-[Domain]-[Variant]

Examples:
- ENFJ-2w3-COORD-01  (Coordinator personality)
- ISTJ-6w5-SEC-01    (Security specialist personality)
- INTJ-5w6-STRAT-01  (Strategic planner personality)
```

### 2. Database Schema

```sql
-- Core agents table (identity constant)
CREATE TABLE agents (
    agent_id INTEGER PRIMARY KEY,
    agent_name TEXT UNIQUE NOT NULL,  -- e.g., "IP-SCRUBBER"
    role TEXT,
    spawned_date DATE,
    spawned_by TEXT
);

-- Personality profiles library (reusable across agents)
CREATE TABLE personality_profiles (
    profile_id INTEGER PRIMARY KEY,
    profile_code TEXT UNIQUE NOT NULL,  -- MBTI-Enneagram-Domain-Variant
    mbti TEXT NOT NULL,
    enneagram TEXT NOT NULL,
    domain TEXT NOT NULL,
    variant_number INTEGER NOT NULL,
    traits_json TEXT,  -- detailed personality traits
    strengths TEXT,
    weaknesses TEXT,
    working_style TEXT
);

-- Agent-to-personality assignments (many-to-many)
CREATE TABLE agent_personality_assignments (
    assignment_id INTEGER PRIMARY KEY,
    agent_id INTEGER,
    personality_profile_id INTEGER,
    assigned_date DATE,
    reason_for_assignment TEXT,
    is_active BOOLEAN DEFAULT 1,
    FOREIGN KEY (agent_id) REFERENCES agents(agent_id),
    FOREIGN KEY (personality_profile_id) REFERENCES personality_profiles(profile_id)
);

-- Work attribution (CRITICAL: track which personality did which work)
CREATE TABLE agent_work (
    work_id INTEGER PRIMARY KEY,
    agent_id INTEGER,
    personality_profile_id INTEGER,  -- which personality completed this
    task_id INTEGER,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    output_path TEXT,
    success BOOLEAN,
    quality_score REAL,
    FOREIGN KEY (agent_id) REFERENCES agents(agent_id),
    FOREIGN KEY (personality_profile_id) REFERENCES personality_profiles(profile_id)
);
```

### 3. Agent Profile Document Structure

**File:** `agents/[AGENT-NAME].md`

```markdown
# AGENT-NAME

**Role:** [Primary function]
**Spawned:** [Date] by [Spawner]
- See `references/behavioral-physics-wellness-panel.md` for the panel shape and calculation stack.
- See `references/ds-scientist-naming-and-two-layer-architecture.md` for the DS + Scientist naming convention, two-layer board/agent architecture, Research Board/Execution Panel pattern, Honcho API workflow, and engine body-system metaphors (established June 2026).

---

## Multi-Personality System

[AGENT-NAME] operates with N distinct personality profiles, selected based on task requirements.

### Current Active Profile
**[PROFILE-CODE]** ([Name])
**Activated:** [Timestamp]
- See `references/behavioral-physics-wellness-panel.md` for the panel shape and calculation stack.
- See `references/ds-scientist-naming-and-two-layer-architecture.md` for the DS + Scientist naming convention, two-layer board/agent architecture, Research Board/Execution Panel pattern, Honcho API workflow, and engine body-system metaphors (established June 2026).

---

## Personality Profile Library

### 1. [PROFILE-CODE-01] ([Descriptive Name])
**MBTI:** [Type]
**Enneagram:** [Type]

**Core Traits:**
- [Trait 1]
- [Trait 2]

**Best For:**
- [Task type 1]
- [Task type 2]

**Performance Metrics:**
- See `references/behavioral-physics-wellness-panel.md` for the panel shape and calculation stack.
- See `references/ds-scientist-naming-and-two-layer-architecture.md` for the DS + Scientist naming convention, two-layer board/agent architecture, Research Board/Execution Panel pattern, Honcho API workflow, and engine body-system metaphors (established June 2026).

---

### 2. [PROFILE-CODE-02] ([Descriptive Name])
- See `references/behavioral-physics-wellness-panel.md` for the panel shape and calculation stack.
- See `references/ds-scientist-naming-and-two-layer-architecture.md` for the DS + Scientist naming convention, two-layer board/agent architecture, Research Board/Execution Panel pattern, Honcho API workflow, and engine body-system metaphors (established June 2026).

---

## Work Assignment by Personality

| Task Type | Personality Profile | Rationale |
|-----------|-------------------|-----------|
| [Task A] | [Profile-01] | [Why this personality fits] |
| [Task B] | [Profile-02] | [Why this personality fits] |
```

## Profile Selection Logic

**When assigning work:**

1. Analyze task requirements (speed vs thoroughness, creativity vs compliance, single-domain vs multi-domain synthesis)
2. **Check the roster first**: if the user has an established agent roster, pick from that roster before inventing a new persona or rolling your own defaults
3. Prefer the **most senior / elite-credentialed roster persona** that actually fits the domain and the current task
4. Match task traits to personality strengths
5. Check historical performance: which profile performed best on similar tasks?
6. If the task has distinct domains, assign one persona per domain instead of a blended persona
7. If the output will be merged, schedule the personas sequentially and pass a strict handoff contract between them
8. If the user explicitly asks for a "run them one at a time" workflow, do **not** fan out the personas in parallel even if concurrency is available
9. **LOCK profile before work starts** - no changes mid-task

### Front-door orchestrator contract

When the user defines a seat like AISHA as the **front door** for mixed personal/business intake:
- treat that seat as a real operating brain, not a lightweight receptionist layer
- keep a **locked variation** active on every meaningful task
- keep the **elite credential stack** active on every meaningful task
- keep the **philosophy / methodology stack** active on every meaningful task
- if the user links that seat to a **COO or executive layer**, encode a default guidance map directly in the artifact
- route health / medical / scoring work downward to the protected specialist subagent instead of flattening it into the front-door seat
- make the executive guidance path explicit in collaboration tables, routing rules, and every-task contracts
- document the default executive map in priority order when specified (for example: COO first, then principal/CTO/CPO/CFO/CMO as relevant)
- when patching these rules, update both the canonical profile and the variation registry so the contract exists at identity and mode levels

Recommended contract headings:
- `Every-Task Brain Contract`
- `Default executive guidance map`
- `Default philosophy stack on every task`

Use `references/aisha-front-door-executive-guidance.md` for the session-derived pattern and wording cues.

### Builder Fleet vs Patient Interface Architecture (New — June 2026)

When the user is both **building engines** AND **patient 0** for those engines, the architecture splits cleanly:

| Fleet | Profiles | Purpose | Interface |
|-------|----------|---------|-----------|
| **Builder Fleet** | One per engine (morphogen, wave, quartz, diviq, seed) | Build, test, deploy engine math to FastAPI ports | CLI, GitHub, Terminal |
| **Patient Interface** | **Single profile** (principal-interface) | Receives Telegram/voice → calls engine APIs → returns coaching | Telegram, Voice, Photos |

**Key insight:** The patient does NOT need a full mirrored agent fleet. The engine math lives in FastAPI services (ports 8000, 8089, 8090, 8091, 8093). One the operator agent profile acts as the patient's single contact point, translating messy human input → clean HTTP calls → coaching response.

This avoids the recursive loop where builder cognition starves patient data capture.

### Telegram Routing: Sensory Input → Brain First (New — June 2026)

**Physiological principle:** Sensory input enters through the **Brain/CNS (Wave)**, not the Skeleton (Morphogen).

| Wrong (Current) | Correct (Physiological) |
|-----------------|-------------------------|
| Telegram → Morphogen (Registry) | Telegram → **Wave (Brain/CNS)** |
| Registry receives messages | Brain processes, then coordinates via morphogen gradients |

**Fix:** `hermes config set telegram.default_profile "wave"` — Wave profile (Kuramoto oscillators = neural sync) is the Telegram entry point. Morphogen stays as skeletal registry (identity, contracts, gradients) — other profiles register WITH it, but sensory input enters through the brain.

### 4-Engine Fleet + Morphogen Registry Architecture (New — June 2026)

The the specialist engine VERSION.md defines a **4-engine fleet** plus Morphogen registry:

| Engine | Port | Body System | Scientist | Capability |
|--------|------|-------------|-----------|------------|
| **Wave** | 8000 | Brain/CNS | Kuramoto | Coaching, Resonance, Mastermind |
| **Quartz** | 8089 | Autonomic NS | Diviq | Lattice, Tasks, PID Control |
| **Diviq (Self-Healing)** | 8091 | Immune/Homeostatic | Sterling | Surveillance, Diagnosis, Intervention |
| **Seed** | 8090 | Endocrine/Growth | Waddington | Avrami/JMAK, Landau, SOC, CPM |
| **Morphogen** | 8093 | Skeletal/Registry | Francis Paxton | Identity, Contracts, Gradients |

**Harvey (Circulatory, port 8092) is extra** — not in the 4-engine fleet. Remove or repurpose.

**Builder profiles should match 1:1:** morphogen, wave, quartz, seed, diviq (5 profiles).

### Base / task / project mode selection

When the roster uses layered metadata instead of hard persona variants, choose the active mode before dispatch:

- **base** = stable default persona
- **task** = short-lived execution lens for a bounded job
- **project** = mission-scoped overlay tied to an ongoing initiative

Rules:
- The active mode must be explicit in the dispatch record or agent card
- Do not treat a task or project mode as a new permanent identity
- If a task is narrow and operational, prefer `task`
- If the work spans a mission or initiative, prefer `project`
- Keep the base persona stable so analytics can attribute work correctly
- For Qubit / health-engine work, resolve the active mode onto existing health/scoring agents instead of inventing new personas
- When delegating, carry the resolved `brain`, `project_mode`, and `persona_layers` through the entire path: prompt, callback/event payloads, session info, and UI cards
- Normalize `persona_layers` to a string list before persisting or rendering

Session-specific notes and examples for health-engine project modes live in `references/health-engine-project-modes.md`.

See `references/project-mode-overlays.md` for the overlay field set and display rules.
See `references/project-mode-metadata-relay.md` for end-to-end dispatch, callback, and UI propagation of brain / project_mode / persona_layers.
See `references/project-mode-metadata-relay.md` for end-to-end dispatch, callback, and UI propagation of brain / project_mode / persona_layers.
See `references/memory-layering.md` for the shared-baseline + per-engine delta memory pattern and the no-auto-include rule.

### Memory layering for related engines

When you need multiple engines or personas to share most of the same memory, treat memory as a layered artifact rather than a chain of recursive includes:
- keep one canonical shared baseline for stable facts that apply everywhere
- keep each engine’s memory file small and focused on deltas, exceptions, and lane-specific rules
- do not assume `MEMORY.md` can import or merge another `MEMORY.md` automatically unless the runtime explicitly supports that behavior
- if you want reuse, generate or render the final memory file from the shared base plus the engine-specific overlay
- use plain references for humans only; a link is not a loader instruction
- if the shared rule is critical to output correctness, repeat it in the engine file or make the merge step explicit and testable

### Roster-first persona rule

- Do **not** create a fresh persona name when the user has already defined an agent roster
- Treat the roster as the source of truth for role names, lanes, and authority
- If multiple roster personas fit, choose the one with the strongest domain credentials and the narrowest lane that still covers the task
- If the roster is missing a fit, pause and ask for the roster or use the closest approved umbrella persona rather than improvising a new identity
- When the user has declared a naming prefix for a brand family, preserve it consistently across all related agent names rather than mixing prefixed and unprefixed forms
- For Divinity Science agent families, default to the `DS` prefix on all outward-facing agent names, and keep the lead coach naming stable (e.g. `the specialist engine`) unless the user explicitly revises it
- When a user's advisory system spans distinct functions or privacy boundaries, split it into separate private repos or panels instead of one blended roster
- Create a master routing map that says which repo/panel handles which question type, and keep it alongside the repos as a durable handoff artifact
- Put repo-local coaching context inside each repo so downstream sessions can use upstream review as context without relying on chat history
- If one panel has already reviewed the work, treat that review as upstream context for the next panel rather than collapsing the voices too early
- Keep advisor outputs separate unless the user explicitly asks for synthesis across lanes
- If the user has split advisory work into separate private repos, respect that split as the primary unit of organization; do not collapse multiple rosters back into one repository just because they are conceptually related
- When several repos exist, build a master routing map that says which repo owns which question class, then keep that map updated as the source of truth for dispatch
- Treat cross-repo handoffs as a deliberate workflow: principal → Product → Marketing → Elite only when the question truly spans those lanes
- Keep repo-local context files, manifest metadata, and advisor files aligned so each private repo can stand alone without importing another repo's roster

See `references/ds-wave-repo-routing-map.md` for the session-specific the specialist engine repository split and handoff order.

### Elite-credential expectation

When a task needs deep expertise, the selected persona should read as an expert, not a generic assistant. For user-facing agent panels, spell out the full credential stack explicitly:
- exact universities attended or trained at
- professional qualifications and senior roles
- licenses / certifications / board or peer recognition where relevant
- years and type of experience
- methodological lineage or school of thought the brain is using
- if the user says "full personas" or "not half credentials," do not compress this into prestige shorthand; include the whole stack up front
- if the user asks to see the panel first, give the panel lineup first and stop before any summary, research synthesis, or recommendations

Reference: `references/cupid-ai-heal-panel.md`

### Panel-first credential contract

When the user asks for "full personas," "not half credentials," or a panel review before the work begins:
- Present the panel lineup first, and stop there until the user approves
- Include the full credential stack for each persona: exact universities / training institutions, degrees, qualifications, licenses/certifications, senior roles, and methodology lineage
- Do not compress to prestige shorthand or vague titles
- Keep the panel output separate from the research/synthesis output
- For QAI health-engine work, treat the source memo as the authoritative user brief: `references/qai-health-engine-source-brief.md`
- If the task is a health-engine build or audit, route to scoring/engineering skills after panel approval; do not let a persona panel masquerade as the engine itself

Reference: `references/cupid-ai-heal-panel.md`
Reference: `references/coach-engine-panel-spec.md`
Reference: `references/university-philosophy-stacking.md`

For any agent card, panel, or project-mode overlay, spell out:
- university / training lineage
- degree level and field
- professional qualifications and credentials
- relevant years and kind of experience
- methodology lineage (e.g. psychometrics, observability, deterministic scoring, systems engineering, security-first design)

Do not compress this into "elite training" or a generic expert label. The user wants provenance they can inspect.

### University-philosophy stacking rule

When the user is not merely asking for pedigree but for the **philosophy of the brain**, do not stop at naming schools or fields. Build a stacked provenance model:
- list each university separately
- state the discipline / concentration attached to that school
- explain the school's methodological or philosophical contribution to the brain
- explain why that philosophy belongs in this specific persona or variation
- explain which blind spot or weakness that school offsets in the rest of the stack

This means the correct unit is not:
- `PhD Computer Science`

It is:
- `Stanford Computer Science for product-systems leverage`
- `MIT systems / operations research for rigor and optimization`
- `Carnegie Mellon for HCI, decision science, or operator-aware workflow design`
- `Berkeley for information systems / open-systems realism`

Adapt the actual schools to the role, but always make the philosophy explicit.

### Critical distinction: system agent-brain stacks vs coaching-engine advisor philosophy

Do **not** collapse these into one philosophy system.

**1. System agent-brain philosophy stacks**
- Use when building or routing the actual internal agent brains that execute work in the system
- Purpose: choose the correct **personality variation** of a system-owned agent based on task class, methodology fit, reasoning style, and blind-spot coverage
- Applies to orchestrator, ops / engineering, research, health, GD, and other internal system seats
- This layer belongs in the system-wide dispatch flow for runtime routing and variation locking

**2. Coaching-engine advisor philosophy**
- Use inside the specialist engine or similar coaching engines when selecting human-like advisors, public-figure mirrors, or philosophy/framework lenses
- Purpose: choose the right **advisor lens** for the user's question, not the internal execution variation of a system agent
- Selection should follow coaching-panel rules such as lane fit, mission / philosophy alignment, public evidence, public-fit scoring, and the smallest useful advisor set
- This layer should not be mistaken for the system-agent variation architecture

**Operational rule:**
- If the work is about building or updating the multi-agent runtime itself, use **system agent-brain philosophy stacks**.
- If the work is about the specialist engine coaching, panel composition, or human-like advisors, use **coaching-engine advisor philosophy**.
- When the user says the coaching-engine philosophy is different from the agent-brain philosophy, treat that as a correction and separate the two layers explicitly in the artifact, routing logic, and terminology.

### Variation-specific credential mapping rule

Do not present the same credential blob for every variation of an agent.
For each active variation:
- state the base brain
- state the active variation
- explain how the same credential stack is being expressed differently in this variation
- narrow the credential emphasis to the mission instead of repeating the full generic biography unchanged
- if the user says the seat should have elite credentials and a philosophy stack **on every task**, encode that as an always-on contract section near the top of the profile/registry rather than burying it inside one variation

Example distinction:
- a base CTO brain may be broad platform architecture
- a task variation may re-express that stack as enforcement rails, canonical artifact protection, and anti-rework systems design

### Verified-vs-designed separation rule

When building cards from mixed evidence sources:
- explicitly separate `verified from live files` from `designed overlay` or `proposed variation`
- never imply a canonical file exists when you did not verify it on disk
- if one seat is inferred from operational artifacts rather than a dedicated SOUL/AGENT file, say so plainly

This prevents false confidence and preserves auditability.

### Panel sequencing pitfall — do not run the audit before the brains are rebuilt

If the user is frustrated with weak personas, generic credentials, or missing methodology lineage:
1. lock or identify the base variation first if needed
2. rebuild the panel cards using the full provenance architecture
3. get approval on the exact brains
4. only then run the sequential audits or reviews

Do **not** jump from a generic roster straight into the audit. That recreates the same failure mode the user is trying to eliminate.

### Panel sequencing pitfall — do not run the audit before the brains are rebuilt

If the user is frustrated with weak personas, generic credentials, or missing methodology lineage:
1. lock or identify the base variation first if needed
2. rebuild the panel cards using the full provenance architecture
3. get approval on the exact brains
4. only then run the sequential audits or reviews

Do **not** jump from a generic roster straight into the audit. That recreates the same failure mode the user is trying to eliminate.

### Pitfall: front-door brain drift into generic-assistant mode

If the user explicitly says a lead seat should still have elite credentials, philosophy, and a personality variation on **every task**, do not assume those qualities are implied by the existence of a 10-variation registry.

You must encode them in an explicit always-on contract near the top of the artifact. Otherwise future edits will preserve the registry but still let the seat behave like a generic helper in practice.

Required fix pattern:
- patch the canonical profile
- patch the variation registry
- add the executive guidance map if the user named a COO/executive layer
- add a short philosophy-stack section that applies on every task

### Coaching-engine variant: stable coach + adaptive advisors

Use this pattern when the user wants a coaching engine, not a pure panel of peers:
- keep the lead coach identity stable across time; do not silently rewrite the coach’s brain when the user’s strain changes
- let the advisor panel change only via explicit panel-delta proposals (add / remove / replace / keep)
- let the user approve, veto, or lock advisors; never auto-mutate the panel behind the user’s back
- explain why each advisor was selected, what philosophy/methodology it represents, and what blind spot it covers
- allow limited obstacle removal (calendar cleanup, drafting, organization, prep) only within autonomy bounds
- if the user becomes healthier or less strained, propose a panel review rather than automatically collapsing the support structure
- preserve historical recommendations so prior advice remains auditable
- when the user continues to unpack the situation, re-evaluate whether the current panel is still sufficient and add advisors only when a missing lens would materially change the answer
- prefer the smallest useful advisory panel, but allow any number of agents when the user’s needs justify it

See `references/ds-wave-dynamic-advisory-panels.md` for the dynamic add-advisor rules and reassessment heuristics.

### the specialist engine coach-panel selection

When the user invokes the the specialist engine coaching engine or asks for a long-term principal coach with panel advisors:
- default to a **stable principal mentor / integrator** as the lead coach
- pick the **smallest useful advisor set** rather than a broad chorus
- rank advisor fit in this order when relevant: Industry-matched principal → Marketing principal → Finance / funding principal → Talent principal → Mission / philosophy alignment principal → Growth principal
- include **Health / medical principal** only when the user’s actual question is health/medical and not general execution or strategy
- treat Marketing as a core system when the user is asking about launch, positioning, proof, content, distribution, or market selection
- when the user names a niche market, match the marketing advisor to that niche instead of using a generic growth voice. Example lanes: biohacking, quantified-self, longevity, health tech, neurodivergent productivity, or coaching/education.
- for AI-native products, include the product's simplicity promise as a first-class marketing criterion. If the user says the product should be easy enough for a non-technical family member to use, preserve that as a core positioning constraint, not a throwaway line.
- treat Talent as high priority when the user is asking about roster design, specialist selection, delegation, or org structure
- treat Mission / philosophy alignment as a standing check for firewalls, identity, and long-horizon coherence
- when the user is deciding between paths, classify the state as **deciding** and sequence advisors one at a time
- each advisor should answer in the same compact shape so synthesis is comparable
- the lead coach synthesizes the panel into one recommendation; do not present disconnected opinion dumps
- if the user keeps revealing new context, re-check whether a missing lens now matters before locking the synthesis
- do not treat the panel as static for the whole conversation; it can expand or narrow as the user’s needs evolve

### Dedicated personal the specialist engine seat rule

When the user asks to create a seat for their **personal Wave agent and engine**, do not leave the specialist engine as a vague optional future lane.

Treat it as a **real dedicated seat** when the user explicitly promotes it.

Required architecture:
- **the specialist engine agent** = the stable front-door coaching / advisory identity
- **the specialist engine engine** = the routing, panel-separation, COO-style handoff, and action-synthesis layer behind that identity
- **the specialist engine product-panel** = support lane only when the request is specifically product-facing

Ownership default for the Personal the specialist engine seat:
- personal coaching
- principal-life integration
- decision support
- advisor synthesis
- execution planning from mixed life/business context

Boundary rules:
- do **not** collapse Personal the specialist engine into the main orchestrator seat
- do **not** collapse it into AISHA-MD medical orchestration
- do **not** silently merge personal the specialist engine work into Divinity Health product work
- let it consume orchestrator outputs, but keep the seat itself distinct
- if the user explicitly says to "go ahead and do a seat," update the architecture artifact in place and promote the lane from optional to active instead of merely describing the idea

See `references/coach-engine-panel-spec.md` for the default panel shape, selection order, and advisor output contract.
See `references/ds-wave-dynamic-advisory-panels.md` for the live reassessment rules.

### Wellness-aware coaching lens

For coaching work, overlay an eight-dimension / TWC-style wellness lens before selecting advisors:
- interpret strain, recovery, bandwidth, and readiness first
- modulate tone and intensity based on current state
- use wellness state to recommend support-heavy or leaner advisors, but never as a private diagnosis
- if the user is working with human exemplars, the engine should include a public-fit / leadership-integrity score with explicit rationale, status, and evidence basis
- disqualify or watchlist public human advisors when evidence suggests harmful leadership or mass-harm risk
- update advisor status when new evidence changes the fit

### Public human-figure mirroring

When the user asks to mirror a *public human figure*:
- use public TWC scores for the mirrored figure, not private-user scoring
- keep the mirrored agent updated with the latest public news and public information about that human
- treat the mirrored agent as a public brain/skillset profile that should evolve as the public record evolves
- give the agent a unique `DS-` prefixed creative name that describes the human
- keep this workflow separate from private coaching, private health scoring, and the principal-only identity rules

See `references/coach-engine-panel-spec.md` for the session-derived workflow notes.
See `references/public-figure-mirroring.md` for the mirrored-human rules, naming pattern, and separation from private scoring.

### Consecutive specialist panels

When the user wants best-in-class reasoning across multiple dimensions, treat the personas as a *consecutive panel*, not a chorus:
- one persona works at a time
- each persona receives the same source material plus the prior handoff note
- each persona writes a short, explicit handoff for the next one
- do not run multiple dimension lenses in concert
- do not fan out dimension lenses in parallel just because concurrency exists
- the final synthesis only happens after every required persona has run
- use a simple public-facing output shape; keep private scoring or calibration inside the specialist layer

### ⚠️ Health Engine ≠ Persona Panel (critical routing disambiguation)

If the user asks for a **QAI self-healing health engine**, **behavioral/telemetry-based scoring**, **anomaly detection**, **guardrails**, **self-healing scoring**, or anything framed as *building or maintaining the engine that scores health dimensions* — that is a **scoring/engineering** task, NOT a persona panel task.

- DO NOT route to the panel pattern below.
- DO NOT design agent personas, brain architectures, or personality panels.
- DO route to scoring-pipeline skills (`proprietary-twc-scoring`, `health-scoring-daily-pipeline`, `qubit-gr-8d360-scoring-pipeline`, `aisha-md-health-orchestration`).

The panel pattern below is for when the user explicitly asks for **specialist agent panels** to *consult on* or *validate* health models — not when they want the scoring engine built or audited.

### Physics / behavior / wellness panels

When the user asks for spacetime geometry, decision theory, human behavior modeling, or eight-dimensions-of-wellness reasoning, prefer a *panel with distinct roles* rather than a blended generic expert:
- one formal math / geometry agent
- one human-behavior modeler
- one eight-dimensions-of-wellness specialist
- one decision-theory / policy agent
- one behavioral-physics translator
- one synthesis / implementation agent

Run the panel individually first, then in concert for validation. Ask each agent for the same output shape so the handoff is comparable:
- what this lens sees
- strongest recommendation
- what the next agent should carry forward
- unresolved risk / watch item
- whether human review is needed

For this class of work, the output should separate:
- state vector / latent state
- regime or mode
- trajectory forecast
- intervention ranking
- confidence / uncertainty
- explanation / reason code

See `references/consecutive-dimension-panels.md` for the general handoff contract and `references/behavioral-physics-wellness-panel.md` for the panel shape and calculation stack.

Requirements: Collaboration, empathy, partnership building
Best match: ENFJ-2w3-COORD-01 (The Facilitator)
Rationale: High EQ, persuasive, strategic communicator
```

### 5. Critical Rule: Profile Change = Work Restart

**If ANY aspect changes that affects output:**
- Credentials added/removed
- Personality traits modified
- Model assignment changed
- Tools/context altered

**Then:**
1. STOP work immediately
2. Invalidate all in-progress output
3. Log profile change with timestamp
4. Restart work from scratch with new profile

**Code this in your system:**

```python
def change_agent_profile(agent_id, new_profile_id, reason):
    """Change agent personality profile."""
    # Get current work
    in_progress = get_in_progress_work(agent_id)
    
    if in_progress:
        # Stop and invalidate
        for work in in_progress:
            work.status = "INVALIDATED"
            work.invalidation_reason = f"Profile changed: {reason}"
            work.invalidated_at = datetime.now()
            save_work(work)
        
        # Log the restart requirement
        log_message = (
            f"Agent {agent_id} profile changed. "
            f"{len(in_progress)} tasks invalidated and require restart."
        )
        logger.warning(log_message)
    
    # Assign new profile
    assign_personality(agent_id, new_profile_id, reason)
    
    return {
        "invalidated_tasks": len(in_progress),
        "restart_required": in_progress,
        "new_profile": new_profile_id
    }
```

## Variation Locking and Provenance Discipline

When a task uses a named agent plus a task-specific variation/overlay, always separate three layers explicitly:
1. **Base brain** — the canonical agent identity
2. **Verified V1-V10 substrate** — the underlying registry-backed personality variation actually being used
3. **Mission overlay** — the narrower task-mode applied for this specific job

Required output pattern before dispatch:
- base brain
- verified variation source file(s)
- exact V# chosen
- whether the variation is **verified** or **derived**
- mission overlay name
- why this substrate is the right fit for the task

Do **not** collapse a custom overlay name into the canonical V1-V10 slot.
If a task-specific overlay uses labels like "V2" or "V3", but the live registry says the best substrate is a different V#, show both layers explicitly instead of pretending they are the same thing.

Before launching multi-agent review work, create a lightweight **variation lock** artifact (or equivalent explicit record) that lists the exact V# for each agent. Each reviewing agent must log its locked variation before starting and keep that variation fixed for the full task. If the variation changes mid-task, invalidate and restart that review.

### Sequential locked-audit execution rule

When the user asks for a deep systems/process audit using named brains one at a time:
- finish **identity lock before dispatch** for every seat that will participate
- if one seat is missing a canonical variation registry, formalize or derive it transparently **before** the audit chain starts; do not launch the chain with one unresolved seat and hope to fix it later
- once the user approves the lineup or explicitly authorizes the full sequence, run the auditors consecutively without stopping for routine permission between seats
- if the user also says "don't stop in between" or otherwise removes routine approval gates, treat that as a workflow instruction for the whole chain and preserve it in the audit/orchestration skill rather than re-asking between seats
- require every auditor to read the upstream audit packet plus the prior reviewer handoff, then produce a short handoff note for the next seat
- keep each seat in-lane: architecture seat should not synthesize control-plane sequencing, measurement seat should not rewrite persona architecture, etc.
- do the global synthesis only after the final locked seat completes
- if a child run fails because of truncation/max-iterations, relaunch the same locked seat with a tighter brief instead of skipping ahead or silently changing the variation
- for audit chains about rewrite-heavy/circular work, the synthesis must collapse findings into a deduplicated implementation plan and a small number of measurable control changes rather than a pile of overlapping recommendations

If an agent lacks a canonical 10-variation file, label the chosen variation as **derived** and identify the source profile or role file it was derived from. If the missing registry blocks trustworthy dispatch, formalize the registry first rather than bluffing.

### ⚠️ Pitfall: personality data that doesn't flow (the "display-only" trap)

When adding a personality layer (MBTI, OCEAN, Enneagram, etc.) to an agent system, wiring it into a SINGLE display surface is NOT integration. The user WILL catch it. Every downstream system that reads agent state must carry the new personality fields or the personality is decorative.

**Symptom:** Personality renders in one tab/panel but the organism doesn't actually know its own MBTI when making decisions, routing tasks, greeting in chat, or birthing new organisms.

**The mandatory propagation checklist (verify ALL points, not just the first):**

1. **Data source** — the master personality object (e.g. `ARCHETYPE_PERSONALITY`) covers every ID, no gaps
2. **Read APIs** — `getArchetypesForContext()`, `getArchetypeVariant()`, and any equivalent getter must RETURN personality fields, not just id/name/drive
3. **Agent state object** — the runtime state object (e.g. `__activePersonality`) carries `mbti`, `ocean`, `combo` — this is what downstream decisions read
4. **Bridge/cache objects** — if a system caches archetypes into a derived array (e.g. `BRIDGE_ARCHETYPES`), that cache must re-map with personality fields, not just copy basic fields
5. **Selection UI** — archetype selector dropdowns show personality (e.g. `[ENFJ]` badge on each option)
6. **Chat/greeting** — the chat greeting line includes the personality type inline
7. **Birth/spawn flows** — the organism creation dropdown lists ALL archetypes (not a hardcoded 8 of 36) with personality visible
8. **Dead links** — any link to a page that doesn't exist yet (`gg-archetypes.html`) must be redirected, not left as a 404
9. **Trajectory/decision systems** — `applyArchetypeTrajectory()` receives and stores personality so routing/decision code can read it

**Self-audit pattern (run after any personality integration):**
```
For each integration point above:
  → Does it carry mbti/ocean?  (verify in browser console, not by reading code)
  → If NO → fix it before reporting done
```

The user's words: "go back through your work and ensure you completed it correctly and thoroughly. I don't think you did everything. I bet you have gaps."

They were right every time. The personality data existed but only flowed to 1 of 8+ integration points.

### MBTI + OCEAN combination pattern (the operator agent organism implementation)

When assigning combination personalities to archetype variants:

- **Same Jungian family, different MBTI per tier** — e.g. the Hero family gets ENFJ (alpha/tactical), ENTJ (beta/strategic), INFJ (gamma/transcendent). This gives genuine variety even within repeated Jungian categories.
- **MBTI chosen to match the tier's operational mode** — alpha = action-oriented types (ESTP, ENFJ), beta = strategic types (INTJ, ENTJ), gamma = transcendent types (INFJ, INFP)
- **OCEAN scores are tier-sensitive** — e.g. Curie alpha = C:98 (measurement-obsessed), Curie gamma = O:92 (pattern-seeing). The same personality family shifts trait emphasis by tier.
- **14 of 16 MBTI types should appear** across a 36-archetype system for real variety. If you only use 5-6 types, the system is too narrow.

See `references/gg-archetype-mbti-ocean-system.md` for the full 36-archetype personality mapping, the `ARCHETYPE_PERSONALITY` data structure, and the integration audit script.

## Common Pitfalls

### ❌ Don't: Treat personalities as versions

```
IP-SCRUBBER v1.0 (ISTJ) → v2.0 (ENTJ)  # WRONG
```

### ✅ Do: Treat personalities as variants

```
IP-SCRUBBER remains IP-SCRUBBER
  Uses ISTJ-6w5-SEC-01 for audit work
  Uses ENTJ-8w7-SEC-01 for crisis response
```

### ❌ Don't: Change personality mid-task

```python
agent.start_work(task_id=42, personality="ISTJ-6w5")
# ... 2 hours later ...
agent.personality = "ENTJ-8w7"  # WRONG - invalidates 2 hours of work
```

### ✅ Do: Lock profile before work starts

```python
agent.lock_profile("ISTJ-6w5-SEC-01")
agent.start_work(task_id=42)
# ... work completes ...
agent.unlock_profile()
```

### ❌ Don't: Lose attribution when personality changes

```sql
-- Bad: only tracks current personality
SELECT agent_name, current_personality FROM agents;
```

### ✅ Do: Preserve historical work-personality mapping

```sql
-- Good: can answer "which personality did this work?"
SELECT 
    a.agent_name,
    p.profile_code,
    w.task_id,
    w.completed_at
FROM agent_work w
JOIN agents a ON w.agent_id = a.agent_id
JOIN personality_profiles p ON w.personality_profile_id = p.profile_id
WHERE w.task_id = 42;
```

## Advanced: Personality Performance Analytics

**Track which personalities excel at which tasks:**

```sql
CREATE VIEW personality_task_performance AS
SELECT 
    p.profile_code,
    t.task_type,
    COUNT(*) as tasks_completed,
    AVG(w.quality_score) as avg_quality,
    AVG(w.duration_seconds) as avg_duration,
    SUM(CASE WHEN w.success THEN 1 ELSE 0 END) * 1.0 / COUNT(*) as success_rate
FROM agent_work w
JOIN personality_profiles p ON w.personality_profile_id = p.profile_id
JOIN tasks t ON w.task_id = t.task_id
GROUP BY p.profile_code, t.task_type;
```

**Use this to optimize future assignments:**

```python
def recommend_personality_for_task(task_type):
    """Recommend best personality profile for task type."""
    query = """
        SELECT profile_code, avg_quality, success_rate
        FROM personality_task_performance
        WHERE task_type = ?
        ORDER BY (avg_quality * success_rate) DESC
        LIMIT 1
    """
    return db.execute(query, (task_type,)).fetchone()
```

## Example: AISHA Multi-Personality System

**From conversation - AISHA has 4 personalities:**

```markdown
### AISHA-ENFJ-2w3-COORD-01 (The Facilitator)
- Best for: Agent spawning, team building, partnerships
- Traits: Empathetic, persuasive, collaborative

### AISHA-INTJ-5w6-STRAT-01 (The Architect)
- Best for: Strategic planning, system design
- Traits: Analytical, big-picture, future-focused

### AISHA-ISTJ-6w5-EXEC-01 (The Executor)
- Best for: Task completion, documentation, compliance
- Traits: Methodical, thorough, detail-oriented

### AISHA-ENTJ-8w7-COMM-01 (The Commander)
- Best for: Crisis response, rapid decisions, blockers
- Traits: Decisive, assertive, action-oriented
```

**Work assignment logic:**

```python
task_to_personality = {
    "agent_spawning": "ENFJ-2w3-COORD-01",
    "strategic_planning": "INTJ-5w6-STRAT-01",
    "documentation": "ISTJ-6w5-EXEC-01",
    "crisis_response": "ENTJ-8w7-COMM-01",
}

current_task = "agent_spawning"
aisha.adopt_personality(task_to_personality[current_task])
```

## Verification Checklist

Before deploying multi-personality system:

- [ ] Database tracks agent identity separately from personality
- [ ] Work attribution includes personality_profile_id
- [ ] Profile changes invalidate in-progress work
- [ ] Profiles are locked before work assignment
- [ ] Profile codes follow consistent format
- [ ] Historical work-personality mapping preserved
- [ ] Analytics can answer "which personality did this work?"
- [ ] Profile selection logic documented
- [ ] Performance metrics tracked per personality-task pairing

## Dispatch Metadata Pattern

Use a small, explicit metadata block for each persona or overlay:

```json
{
  "persona": "AISHA-MD",
  "activeMode": "project",
  "lens": "health",           // persona operating lens — NOT the QAI health engine
  "scope": "QAI health engine review",
  "activation": "user assigned a project-scoped brief",
  "exit": "project ends or scope narrows",
  "rules": ["no persona drift", "no permanent identity rewrite"]
}
```

> **Note:** `"lens": "health"` means the persona is operating in a health-focused mode. It does NOT mean the persona *is* the health engine. The QAI self-healing health engine (behavioral telemetry, scoring, anomaly detection, guardrails) is a separate system — route scoring/engineering requests to the scoring pipeline skills, not to persona dispatch.

Operational notes:
- `activeMode` should be decided before dispatch
- the same base persona can carry different mode overlays over time
- analytics should record both identity and mode for attribution
- if a mode changes output-critical behavior, treat it as a dispatch change, not a cosmetic label

## Communication Channel Architecture for Multi-Personality Agents

When deploying multi-personality agents on messaging platforms, you have two architectural options:

### Option 1: Labeled Messages in Single Channel (Recommended for MVP)

**Implementation:**
- All personality variants post in same DM/channel
- Use emoji prefixes to distinguish personalities
- Example: `🎯 [AISHA FLEET]: spawning IP-SCRUBBER...` vs `🏥 [AISHA-MD]: your PSY score is 5.0`

**Pros:**
- ✅ Zero infrastructure setup
- ✅ Works immediately (no gateway config changes)
- ✅ Mobile-friendly (all updates in one place)
- ✅ No permission/admin issues

**Cons:**
- ❌ Single scroll - no topic separation
- ❌ Relies on user visually parsing labels

**Use when:** Quick deployment, single user, agent testing, mobility is priority

### Option 2: Separate Channels/Topics per Personality

**Implementation (Telegram supergroups with topics):**

1. **Discover bot username** (agent may not know its own username):
   - Query Telegram API getMe endpoint to retrieve bot username
   - Use the `send_message(action='list')` tool to see available chats

2. **User creates supergroup:**
   - Create group in Telegram app
   - Add bot as member by searching bot username
   - Make bot admin (needed for "read messages" permission)
   - Enable Topics in group settings

3. **Configure gateway to allow group:**
   - User must manually add group chat ID to gateway configuration
   - Note: Security restrictions prevent agent from editing config files directly
   - Gateway restart typically required to pick up new allowed chats

4. **Create topics for each personality:**
   - 🎯 AISHA Fleet (agent coordination)
   - 🏥 AISHA-MD (health/personal)
   - 📊 Reports (deliverables)
   - 🔧 Alerts (system notifications)

5. **Route messages to appropriate topics:**
```python
# Each personality knows its topic ID
personality_topics = {
    "ENFJ-2w3-COORD-01": "aisha-fleet-topic-id",
    "MD-VARIANT": "aisha-md-topic-id",
}

def send_as_personality(personality_code, message):
    topic_id = personality_topics[personality_code]
    target = f"telegram:{chat_id}:{topic_id}"
    send_message(target, message)
```

**Pros:**
- ✅ Clean separation of concerns
- ✅ Can mute specific personalities
- ✅ Searchable by topic

**Cons:**
- ❌ Gateway configuration required
- ❌ Manual config editing by user
- ❌ Gateway restart needed
- ❌ Bot must be admin in group
- ❌ More complex setup

**Use when:** Production deployment, multiple users, organizational needs, topic-level permissions required

### Gateway Limitations to Know

**When working with messaging gateways:**

1. **Agent cannot directly edit config files** - Security restrictions block writes to credential/config files
2. **Cannot query platform APIs directly** - Direct API calls may be blocked by security scan
3. **Must use `send_message(action='list')`** - Only way to discover available chats from agent context
4. **Gateway cache delays** - New groups may not appear immediately; may need external restart
5. **Channel discovery is async** - Bot added to group → gateway polls updates → chat appears in list

**Workaround for config edits:**
```python
# Generate instructions for user to manually update config
chat_id = "-1001234567890"  # example chat ID
instruction = (
    f"Please add this chat ID to your gateway configuration:\n"
    f"Chat ID: {chat_id}\n"
    f"Then restart the gateway service."
)
# Agent provides instructions; user makes the edit
```

## Real Implementation: Extending an Existing Agent Database

**Critical lesson:** In practice, you are almost never building from scratch. The OpenClaw fleet already had `agents.db` with 18 tables, 126 agents, personality profiles (Big Five), credentials, wellness (8D), performance tracking, review panels, leaderboards, and auto-update triggers. The sub-persona system had to be ADDED to this existing schema.

### Actual Schema Extension (tested, production)

```sql
-- Added to existing agents.db alongside agents, personalities, agent_performance, etc.
CREATE TABLE IF NOT EXISTS agent_personas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id INTEGER NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    persona_code TEXT UNIQUE NOT NULL,       -- 'AISHA-MD', 'AISHA-CTO'
    persona_name TEXT NOT NULL,
    persona_type TEXT,                       -- 'health', 'fleet-mgmt', 'operations'
    mbti TEXT,
    enneagram TEXT,
    model_override TEXT,
    system_prompt_hash TEXT,
    temperature_override REAL,
    domain_focus TEXT,                       -- JSON array
    authorized_tools TEXT,                   -- JSON array
    status TEXT DEFAULT 'active',
    activated_at TIMESTAMP,
    last_active_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Key difference from theoretical schema
- `agent_personas` links to the EXISTING `agents` table via `agent_id` FK
- Sessions table (`agent_sessions`) has BOTH `agent_id` and `persona_id` — aggregate at agent level, drill down by persona
- Views do the rollup: `primary_agent_analytics` aggregates all personas, `persona_analytics` breaks down per-persona
- Existing tables (agent_performance, agent_wellness, agent_metrics_summary) remain untouched — new tables extend, not replace

### Seeding Real Personas

```sql
-- Register primary agent first
INSERT INTO agents (code, display_name, domain, family, role, status)
VALUES ('OPS-CHF-TAL-L7', 'AISHA', 'OPS', 'CHF', 'Chief Talent Officer', 'active');

-- Then sub-personas reference the parent
INSERT INTO agent_personas (agent_id, persona_code, persona_name, persona_type, mbti, domain_focus)
SELECT id, 'AISHA-CORE', 'AISHA Core CTO', 'fleet-management', 'ENFJ',
    '["talent","fleet","analytics"]'
FROM agents WHERE display_name = 'AISHA';

INSERT INTO agent_personas (agent_id, persona_code, persona_name, persona_type, mbti, domain_focus)
SELECT id, 'AISHA-MD', 'AISHA Medical Director', 'health', 'ISTJ',
    '["health","wellness","medical","ADHD","bipolar"]'
FROM agents WHERE display_name = 'AISHA';
```

### Runtime overlay retrofit pattern for existing fleets

Use this when the live fleet already has an `agents` table and maybe even an `agent_personas` table, but the real runtime state is incomplete, stale, or split across repos.

Required sequence:
1. inspect the live DB first: confirm whether the target seats exist, whether `agent_personas` is actually populated, and which metadata fields the runtime already supports (`brain`, `project_mode`, `persona_layers`, etc.)
2. inspect the live artifact layer separately: variation registry files, SOUL/AGENT files, routing docs, and any canonical JSON registry the seeder uses
3. if the canonical registry is stale or missing seats, do **not** trust it as the only runtime source. Add a small runtime overlay artifact that expresses the live seat contract explicitly
4. split philosophy layers explicitly when needed:
   - execution philosophy stack for system-owned runtime brains
   - advisor philosophy stack for coaching / public-facing advisor lanes
5. if a seat exists conceptually but not in the live DB, upsert the seat into `agents` and then seed its persona rows into `agent_personas`
6. if SOUL paths in the runtime repo do not resolve locally, mirror or create the needed local seat files before pointing live overlays at them
7. write the overlay and persona manifest as first-class artifacts, then run a deterministic loader script to apply them to the DB
8. verify with direct queries, not assumptions: confirm the target seats, their `project_mode`, their `persona_layers`, and persona counts per seat

Operational rule:
- treat "docs say it exists" and "DB/runtime say it exists" as different claims
- the system is only live when both the artifact layer and DB layer agree
- when the user asks about the *live fleet* size or coverage, anchor the count to the DB-backed live roster first; do not union the broader code library, alias files, or archive-only profiles into that number
- if you create DS-prefixed alias copies for outward-facing consistency, do not let those aliases inflate the roster count or appear as separate agents in manifests

Default live artifact set for this retrofit:
- one seat-overlay JSON that defines seats, philosophy stack, task-tag-to-variation routing, and canonical default variation
- one routing-contract markdown file that explains execution vs advisor split in plain language
- one persona-manifest JSON that lists the concrete persona rows to seed
- one deterministic loader script that can be rerun safely to upsert seats and personas

This pattern is especially important when the user wants the distinction between the system's internal agent-brain philosophy and the specialist engine style advisor philosophy made live immediately, without waiting for a full registry rewrite.

See `references/sibling-agent-runtime-overlay-retrofit.md` for the concrete OpenClaw implementation pattern: stale canonical registry, missing the specialist engine DB seat, empty `agent_personas`, mirrored SOUL files, runtime overlay artifacts, and DB verification queries.

### Personality-Specific Sub-Agent Pools (Engine-Level Pattern)

**User directive (2026-06-17):** "The agent should be able to spawn 4 subagents and I feel they should be specific to the personality type selected or task at hand, not general. The agent may have better support with more specialized agents per the actual task or need."

This is a critical refinement to the multi-personality pattern. Each personality variant gets its **own** 4 specialized sub-agents, scoped to that personality's strengths and the task at hand. Sub-agents are NOT shared across personalities.

**Wrong (General Sub-Agents):**
```
Engine Lead Agent
  ├── 4 general sub-agents shared by all personalities
  └── Personality switch doesn't change who gets spawned
```

**Correct (Personality-Specific Sub-Agents):**
```
Engine Lead Agent (10 personalities)
  ├── The Diagnostician → spawns: Immune Analyst, Lab Analyzer, Imaging Reader, Risk Stratifier
  ├── The Emergency Responder → spawns: Acute Coordinator, Protocol Selector, Resource Allocator, Complication Monitor
  ├── The Researcher → spawns: Literature Synthesizer, Data Validator, Statistical Reviewer, Citation Checker
  └── ... (each personality has its own 4)
```

**Design rules:**
- Each personality variant defines its own sub-agent pool (typically 4 per personality)
- Sub-agents inherit the personality's decision speed, risk tolerance, and methodology
- A 10-personality engine has up to 40 unique specialized sub-agent specs
- The lead agent selects sub-agents based on: active personality + task type
- Sub-agents should be named after the domain specialty (e.g., "Hemodynamics Analyst"), not generic roles

**Implementation:** See `references/personality-specific-subagents.md` for the dataclass pattern and indexing approach used in the DS engine fleet (29 engines, 10 personalities each, 4 sub-agents per personality = 1,160 total specs).

### Two-Layer Persona Architecture: Psyche (Decision) vs Voice (Translation)

**User-corrected architectural separation (2026-07-17, BINDING, terminology corrected same session).** A persona system has TWO distinct layers that must be architecturally separated, not merged:

| Layer | Name | Controls | Does NOT Control |
|-------|------|----------|-----------------|
| **Layer 1** | PSYCHE (Decision Engine) | WIP limits, routing bias, gate strictness, reasoning depth, risk tolerance, Sherman routing weights, task sort strategy | How output is worded |
| **Layer 2** | VOICE (Translation Membrane) | HOW decisions are communicated to the user (tone, word choice, style) | Decisions, routing, gates, WIP, priorities |

**Terminology corrections (user, 2026-07-17, BINDING):**
- The archetype is the *pattern* (Jungian template). The living expression of that pattern in the organism — the actual operating psychology — is the **psyche**. Label the layer "Psyche", not "Archetype". The archetype is the blueprint; the psyche is the running instance.
- Voice is a SMALL part of the persona. UI labels should say "Voice", not "Persona", because the panel controls the voice layer only, not the entire persona.
- The voice layer does NOT need its own body-analog process flow. The correct isomorphism is **prosody** — non-verbal modulation of speech that rides on the existing language pathway. It has no organ of its own. It is a membrane property. Do not design a voice-specific process flow.

**The critical principle (user's exact words):** "The voice doesn't make the decisions. It just speaks to the human in a way that helps them do it. We need to have this persona as a built-in layer as the organism is functioning. The archetypes drive decisions and the voice is the translation between the user and the organism."

**Wrong (merged):** Persona = one thing that both decides AND speaks. Changing the voice accidentally changes routing weights or WIP limits.

**Correct (separated):**
```
USER INPUT → ARCHETYPE makes decision → ORGANISM OPERATES →
  VOICE translates output → USER sees it
```

**Implementation pattern (the operator agent Ops Platform):**
- `window.__orgTrajectory` stores the active archetype's decision parameters (WIP, routing, gates, risk)
- `window.__activeVoiceLayer` stores the active voice's delivery parameters (name, blurb, category)
- `translateThroughVoice(rawText, context)` wraps any organism output with voice metadata
- The function returns `{raw, voice, prefixed}` — raw decision + voice instruction for LLM + prefixed display
- `classifyRoute()` reads ONLY from `__orgTrajectory` (archetype), NEVER from `__activeVoiceLayer` (voice)
- `applyArchetypeTrajectory()` modifies ONLY decision systems, never touches voice

**Pitfall — function-scoped voice data (2026-07-17):** If the voice registry (`PERSONA_REGISTRY` or `VOICE_DNA`) is defined inside a render function (e.g. `renderPsychTab()`), it is unreachable by `selectPersonaVoice()` which runs at page load. ALWAYS extract voice blurbs to a global lookup (`window.VOICE_DNA_LOOKUP`) so the voice layer can be set before the user visits the Psychiatry tab. Without this fix, `selectPersonaVoice()` stores empty blurbs and the translation layer has nothing to work with.

**Pitfall — voice data as display-only decoration:** Just like the "display-only trap" for personality data (see above), wiring a voice layer into ONE display surface is NOT integration. The voice must flow through ALL user-facing output paths: chat messages, coaching output, toasts, notifications. If only the Psychiatry tab shows the voice name but chat doesn't tag messages with it, the voice is decorative.

## Related Patterns

- **Job Classification Systems** - HR job codes (similar concept)
- **Role-Based Access Control** - but for personality traits not permissions
- **State Machines** - personality as state, tasks as transitions
- **Strategy Pattern** - personality as strategy implementation
- **Channel Multiplexing** - Multiple logical channels over single connection
- **Personality-Specific Sub-Agent Pools** - each personality variant spawns its own specialized sub-agents, not shared/general ones
- **Two-Layer Persona Architecture** - Archetype (decision engine) and Voice (translation membrane) are architecturally separated layers, not one merged persona

## References

- See `references/body-engine-architecture.md` for the 4-engine fleet + Morphogen registry mapping, builder vs patient interface split, Telegram sensory routing fix, and patient interface profile specification.
- See `references/consecutive-dimension-panels.md` for the consecutive panel pattern and handoff contract.
- See `references/project-mode-overlays.md` for temporary project-scoped overlays (Mode/Lens) on stable personas and the `base` / `task` / `project` dispatch split.
- See `references/project-mode-and-health-routing.md` for the project-mode metadata pattern, roster-first dispatch, and behavior-only health-engine rails.
- See `references/qai-health-engine-source-brief.md` for the user's original voice-memo brief: full-persona panel first, then behavior-only self-healing health-engine work.
- See `references/your-org-naming.md` for the DS prefix convention and the stable `the specialist engine` lead-coach name.
- See `references/behavioral-physics-wellness-panel.md` for the panel shape and calculation stack.
- See `references/ds-scientist-naming-and-two-layer-architecture.md` for the DS + Scientist naming convention, two-layer board/agent architecture, Research Board/Execution Panel pattern, Honcho API workflow, and engine body-system metaphors (established June 2026).

---

**Key Insight from User:**

> "It's not linear versions, it's personality dimensions. Agents aren't upgraded, they shift personalities based on task needs."

This fundamentally changes how we think about agent evolution - not progressive improvement, but contextual adaptation.
