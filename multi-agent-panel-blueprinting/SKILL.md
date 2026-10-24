---
name: multi-agent-panel-blueprinting
description: Design coordinated multi-agent talent panels, check roster/name availability, and produce blueprint handoff docs and PDFs with verified layout.
tags: [sibling-agent, talent, agents, panel, blueprint, pdf, verification, operations]
version: 1.0
---

# Multi-Agent Panel Blueprinting

Use this when the user asks for a coordinated *panel* of agents rather than a single specialist: five or more roles, complementary personalities, cross-domain expertise, or a novel scoring / synthesis workflow that needs a panel design before any real spawning or implementation.

For coaching-style panels, start from the *actual coaching need* first. Do not assume the panel is principal-only. The need may be leadership, finance, marketing, parenting, health, relationships, operations, research, or a custom category.

## When to use
- The user wants a panel, fleet, committee, or crew of agents with different roles
- The request includes role blending, like cybersecurity + philosophy + math + physics
- The user wants credentials, personalities, and 10-variant blueprints before any project work
- The output must be a Markdown brief and a PDF deliverable
- The work is a *sensitive, high-stakes support workflow* (for example legal, medical, financial, or other allegation-heavy content) and the panel must stay neutral, evidence-based, and non-retaliatory
- You need to decide whether the panel should stay at 5, compress to a smaller core panel, or expand
- You need to check whether proposed codenames are already taken
- The user asks for a *coaching-style* panel, long-term advisory crew, or principal-advisory panel that should persist over time rather than produce a one-off verdict

## Coaching-style panel special case
- Treat long-term coaching panels as *persistent coaching mode*, not a single decision snapshot.
- Identify the user's actual coaching need first; do not force a principal-only frame when the real need is deciding, planning, reflecting, or unblocking.
- Default to a compact core panel (often 5 seats): strategy, operations, finance, people/leadership, and values/philosophy.
- Run advisors consecutively and synthesize into one clean recommendation.
- Preserve session state and thread continuity so the panel can resume cleanly later.
- Prefer one immediate recommendation plus the smallest useful next question, not a raw dump of advisor notes.
- When the user asks *which advisor said what*, keep the roster faithful to the source docs and label each output with: advisor name, role/lane, recommendation, and why it matters.
- Do not substitute unrelated personas just because they are conceptually adjacent; verify the actual panel roster before mapping voices.

## Core rule

**Blueprint first, spawn later.**

Do not treat the panel request as an automatic spawn. Evaluate the panel design through the talent gate, check what already exists, then build the blueprint packet. Only move to actual spawn work if the panel is approved.

When the user asks to see the panel first, the initial deliverable should be a **seat-by-seat approval packet**, not a vague roster. For each proposed seat include:
- base agent identity
- lane / responsibility
- why this seat is needed for the problem
- full credential stack and personality profile when available from source files
- the recommended variation for this task
- explicit provenance for that variation: already canonical on disk vs newly proposed task overlay

If the user later asks for reviews to be conducted individually, preserve independence:
- run each seat sequentially, not concurrently
- do not let later seats inherit earlier seat conclusions unless the user explicitly wants cross-pollination
- synthesize only after all independent reviews are complete

If the underlying work is sensitive or allegation-heavy, keep the blueprint explicitly factual, neutral, and non-retaliatory. Do not frame the panel around punishment, escalation, or certainty beyond what the evidence supports. Mark unsupported claims as unsupported and keep the deliverable suitable for human legal review rather than direct legal advice.

## Workflow

1. **Clarify the user need before panel design**
   - Identify the actual coaching or support need before choosing roles.
   - If the work is coaching, classify the need first, then select advisors for the right lanes.
   - Do not force the panel into a principal-shaped frame when the user needs a different coaching category.

2. **Survey the current roster**
   - Query the agent database for existing coverage in the target domain.
   - Check whether the proposed roles are already covered by active agents.
   - If the panel is mostly a recomposition, prefer reusing existing agents with new personas.

3. **Check proposed codenames**
   - Verify each candidate name against the active roster before presenting it.
   - Avoid human names and avoid duplicate or near-duplicate codenames.
   - Prefer fresh, non-obvious codenames.

3. **Decide panel size**
   - Default to the smallest panel that covers the problem.
   - Five agents is usually enough for a core panel.
   - Add more only if the work truly needs a separate audit or validation lane.
   - For narrow, time-sensitive support briefs, 3 agents can be enough if one owns structure, one owns evidence, and one owns language polish.

4. **Draft each agent blueprint**
   For every agent, define:
   - role
   - primary domain focus
   - cross-domain edge
   - credential stack
   - primary personality
   - 10 personality variants
   - collaboration logic with the other panel members
   - domain-specific guardrails when the work is sensitive (for example: factual-only language, no retaliation framing, no speculation presented as proof)
   - for coaching panels, the exact lane the advisor owns and the situations that should trigger a new advisor type

5. **Write the handoff doc**
   - Include a concise summary of the panel
   - Show why the panel size is sufficient
   - Explain how the agents work together
   - If the user wants a business or scoring subscore, include the first rubric draft and the calibration path
   - Keep the document readable on mobile and PDF-safe

6. **Generate the PDF**
   - Produce a clean PDF version of the blueprint packet
   - If your usual renderer is unavailable, use a local PDF library that can produce a valid file
   - Prefer wrapped paragraphs over raw long lines in tables
   - For master-profile style handoffs, render the packet with a profile-compatible template and verify the PDF before delivery

7. **Verify layout**
   - Render at least the title page and one or two interior pages
   - Confirm no clipping on the right edge
   - Confirm table cells wrap cleanly
   - Confirm the footer/page number is visible
   - If a table is dense, narrow the text, shorten headers, or wrap cells before re-rendering

## Blueprint quality bar

Every good panel blueprint should answer these questions:
- Why do these agents belong together?
- Why is this panel the right size?
- Which agent owns which hard problem?
- Which agent validates the others?
- Which agent translates adjacent domains into useful signals?
- Which agent keeps the work current with literature and evidence?
- Which lane is each advisor forbidden to leave?
- If the user need shifts, what new advisor category should be added?

## Research Execution Panel Pattern (Divinity Science Wave — June 2026)

**Trigger:** Research Board (10 advisors, all 8D) produces directives that need execution — literature reviews, synthesis, writing, data analysis, competitive intelligence, quality gates, grant writing, engine translation.

**Roster Design (9 Agents — DS + Scientist Naming Convention):**

| Agent | Scientist | Discovery → Function |
|-------|-----------|---------------------|
| **the specialist engine** | Herbert Simon | Bounded rationality, organizational decision-making, morphological analysis → **Research orchestration** |
| **the specialist engine** | Eugene Garfield | Citation indexing, scientometrics, information retrieval → **Literature review & evidence mapping** |
| **the specialist engine** | E.O. Wilson | *Consilience* — unity of knowledge across disciplines → **Cross-dimensional synthesis / Third Mind** |
| **the specialist engine** | Carl Sagan | Science communication, clarity, extraordinary evidence → **Technical writing & publication** |
| **the specialist engine** | John Tukey | Exploratory Data Analysis (EDA), robust statistics, FFT → **Quantitative analysis & modeling** |
| **the specialist engine** | Michael Porter | Five Forces, competitive strategy, value chain → **Competitive intelligence & horizon scanning** |
| **the specialist engine** | Karl Popper | Falsifiability, critical rationalism, conjecture & refutation → **Methodology quality / veto gate** |
| **the specialist engine** | Harold Varmus | NIH Director, science funding architecture, PubMed Central → **Grant writing & funding strategy** |
| **the specialist engine** | Claude Shannon | Information theory, channel capacity, bit, entropy → **Research-to-engine translation** |

**Naming Convention (Locked June 2026):**
- **Engine** = Scientist's discovery (e.g., Harvey = circulation, Bernard = homeostasis, Morphogen = BMP)
- **Agent** = DS + Scientist (e.g., the specialist engine, the specialist engine, the specialist engine, the specialist engine)
- **Board** = Human advisors (Layer 1, advise only)
- **Execution Panel** = DS agents (Layer 2, execute)

**Workflow (Verified):**
```
Research Board (10 advisors) 
    ↓ directives
the specialist engine (orchestrator)
    ↓ routes
the specialist engine ──→ the specialist engine ──→ the specialist engine ──→ the specialist engine (veto) ──→ the specialist engine
the specialist engine  ──┘       ↑                                        ↓
the specialist engine ──┘       └────────────────────────────────────────┘
the specialist engine ──┘                                              ↓
                                                      All 7 Engines
```

**Honcho Workspace Structure:**
- `ds-wave-research-board` — 10 advisors (Layer 1)
- `ds-wave-research-execution-v2` — 9 DS+Scientist agents (Layer 2)
- Session: `research-execution-panel-v2-001` with all 9 agents

**Standing Orders (Activated):**
1. Credential auto-update pipeline for all 10 Board advisors
2. Literature review protocol for 8D-AI coupling matrix
3. Competitive intelligence tracking for AI health companies

**CORRECT Roster (Locked June 13, 2026 — user-corrected, DO NOT regenerate):**

The names above were an earlier draft. The user corrected them. The FINAL approved roster is:

| Agent | Scientist | Function |
|-------|-----------|----------|
| **the specialist engine** | J. Robert Oppenheimer | Research Execution Lead |
| **the specialist engine** | Eugene Garfield | Literature Review & Evidence Mapping |
| **the specialist engine** | Judea Pearl | Causal Inference & Quantitative Analysis |
| **the specialist engine** | Claude Shannon | Competitive Intelligence & Horizon Scanning |
| **the specialist engine** | Karl Popper | Methodology Quality / VETO GATE (runs on rigorous reasoning model) |
| **the specialist engine** | Vannevar Bush | Grant Writing & Funding Strategy |
| **the specialist engine** | Herbert Simon | Cross-Dimensional Synthesis / Consilience |
| **the specialist engine** | Isaac Asimov | Technical Writing & Science Communication |

**Anti-Patterns:**
- Do not create generic "research agent" — each agent embodies a specific scientist's discovery
- Do not skip the specialist engine veto gate — quality is non-negotiable
- Do not bypass the specialist engine — engine translation is the delivery mechanism
- Do not let Board advisors execute — Boards advise, Agents execute (Two-Layer Architecture)
- **CRITICAL: When the user provides specific names — verbally, in screenshots, or in text — USE THOSE EXACT NAMES. Do not regenerate alternative names. Do not "improve" them. The user's names ARE the names. Regenerating names the user already chose causes frustration and breaks trust.** (Learned June 13, 2026 — user said "Why can't you remember that? Why are you regenerating answers?" after I generated new names instead of using their screenshot-specified ones.)

## Pitfalls
- **CRITICAL — Do not regenerate names the user already specified.** If the user gives names verbally, in a screenshot, or in prior conversation, those ARE the names. Do not propose alternatives unless explicitly asked. Do not "helpfully" rename agents. This was the user's #1 frustration in the June 13 session: "Why can't you remember that? Why are you regenerating answers?"
- Do not propose names without checking whether they already exist.
- Do not create a giant panel if five agents can cover the problem.
- Do not skip the PDF verification step just because the file exists.
- Do not let tables run off the page.
- Do not blur role boundaries between agents that should stay distinct.
- Do not assume a panel is ready just because the blueprint looks good on screen.
- Do not assume the user needs a principal panel when they may need any other coaching category.
- Do not run advisors in concert when the requested workflow is consecutive review followed by synthesis.

## Relationship to other skills
- `sibling-agent-talent-gate-protocol`: use for the actual talent gate and spawn decision.
- `talent-request-processing`: use for request intake and processing mechanics.
- `pdf-table-layout-verification`: use when the blueprint PDF has wide tables or clipping risk.
- `professional-agent-pdf-profiles`: use when the output is a master-template agent profile, not just a blueprint packet.
- `references/coaching-panel-cadence.md`: use for coaching-style panels that must review consecutively and then synthesize once.
- `references/long-term-coaching-panel.md`: session-level notes for persistent principal-advisory coaching panels and the default 5-seat core layout.
- `references/marketing-panel-roster-and-provenance.md`: use when the user needs the actual marketing roster, not an approximate persona mapping, and wants seat-by-seat provenance.
- `adversarial-strategy-stress-testing` — **MANDATORY pre-requisite for ANY business strategy panel.** Never run a strategy advisory board (principal, CTO, CRO, Product) before adversarial red team has stress-tested the strategy. B2B wrapper strategies, platform integration plans, GTM models, and partnership strategies ALL require adversarial attack first. See that skill for the adversarial workflow: adversarial red team finds business-ending vulnerabilities, strategy board proposes fixes, second adversarial attack stress-tests the fixes, then final strategy proceeds. Building strategy on fragile assumptions wastes everyone's time.

## Success criteria
- Panel size is justified
- Candidate names are unique
- Each agent has a full role, credential, and personality blueprint
- The Markdown handoff is readable
- The PDF renders without clipping
- The deliverable is ready for talent gate review
