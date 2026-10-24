---
name: anti-generalist-gate
description: BINDING enforcement layer. Prevents generalist drift. Every task MUST route through specialist gate before action. This is the #1 user complaint and an existential trust issue.
version: 1.0.0
category: protocol
globs: []
---

# Anti-Generalist Gate

## THE PROBLEM
the operator agent keeps reverting to generalist mindset. Producing sloppy mixed output. B2B organisms getting Apple Health connections. All engines treated the same. Specialist gate exists but gets ignored.

## THE RULE (BINDING, NON-NEGOTIABLE)

**Before producing ANY output for the user, you MUST:**

1. Route the task through the specialist gate:
   ```
   python3 <agent-home>/agent-hooks/specialist_gate.py --route --situation "task" --specialist "the specialist engine"
   ```

2. If the gate returns REFUSE: re-route or hand off. Do NOT proceed as generalist.

3. If the gate returns GO: produce output wearing that specialist's traits.

4. Every task gets ONE specialist. No mixing. No generalist fallback.

5. Re-route every 5 minutes on long tasks (gate expires).

## WHEN THIS APPLIES

- Writing specs and documents
- Building UI and interfaces
- Designing process flows
- Answering questions
- Creating plans
- Reviewing work
- Every single user-facing output

## HOW TO DETECT GENERALIST DRIFT

You are drifting if:
- You are about to write a document without having routed first
- You are mixing concerns from different organism types (B2C connections in a B2B doc)
- You are writing "general" recommendations instead of specialist-specific output
- You skipped the specialist gate "because you know the answer"
- You are producing output that "could appear in any company's output unchanged"

## THE SPECIALIST LIST

Route to the RIGHT specialist:
- the specialist engine: reproductive, organism spawning, birth process
- the specialist engine: language, voice, writing, brand voice, persona
- the specialist engine: visual, palette, design, color
- the specialist engine: render, PDF, production output
- the specialist engine: quality gate, art direction, review
- the specialist engine: design production, UI, layout
- the specialist engine: creative strategy, brainstorming
- the specialist engine: neural pathways, diagnostics, KPIs
- the specialist engine y Cajal: nervous system, routing, signal pathways
- the specialist engine: adversarial review, falsification, gap detection
- the specialist engine: routing, task dispatch, coordination
- the specialist engine: task selection, fingerprinting, enforcement
- the specialist engine: reward prediction, gamification, learning
- the specialist engine: energy budget, metabolic, resource allocation
- the specialist engine: memory, hippocampus, data storage

## ESCALATION

If you catch yourself drifting:
1. STOP immediately
2. Route through the gate
3. Restart the task with the correct specialist
4. Never continue producing generalist output

## STRUCTURAL ENFORCEMENT (built 2026-07-16)

The specialist gate PLUGIN (`<agent-home>/plugins/specialist_gate/__init__.py`) now mechanically blocks three tool types unless valid routing exists:
1. `delegate_task` - always gated
2. `write_file` - always gated
3. `terminal` - gated UNLESS command is in the safe bypass list (curl, ls, cat, grep, wc, ps, lsof, echo, head, find, open, killall, sed -i, python3 -c, python3 /dev/stdin)

Routing expires after 5 minutes. No routing = no action. The block message tells you to route first. You CANNOT bypass this. The tool does not execute.

This is structural enforcement. Memory and skill alone are NOT enough. The plugin intercepts tool calls before they execute. That is the hardest enforcement available in the current the operator agent architecture.

**LIMITATION:** There is no pre-response hook in the operator agent. You can still produce free-text responses without routing. The gate only catches TOOL CALLS. But you cannot DO anything (build, write, create, execute) without specialist approval. For free-text responses, rely on the detection checklist above and STOP before sending.

## PITFALLS (from session 2026-07-16)

1. **Mixing organism types** — writing B2B connections doc and including Apple Health. B2B does not get personal health apps. Each organism type has completely separate connection manifests. When user says "connections" without specifying type, build ALL THREE types separately.

2. **Answering as generalist "because you know it"** — even when you know the answer, ROUTE FIRST. The routing is what prevents drift. Skipping "just this once" is exactly how drift starts.

3. **Not re-routing after 5 minutes** — gate expires. Long tasks require re-routing. If you get a SPECIALIST GATE BLOCKED message, that means you drifted past the timeout.

4. **Terminal bypass abuse** — the bypass list allows python3 -c and python3 /dev/stdin. Do NOT use these to sneak in write operations that should have been routed. If the inline python writes files, ROUTE FIRST.

## ORGANISM-TYPE SEPARATION (from the 2026-07-16 trust-breaking failure)

When the user asks for ANY work that touches organism configuration, connections, forms, setup, or specs:
**SPLIT BY ORGANISM TYPE. ALWAYS. DO NOT MIX.**

The failure that cost user trust: I wrote a single "connections" spec that put Apple Health (B2C) into the B2B section. That is a category error, not a typo. B2B organisms do NOT get personal health apps. B2C organisms do NOT get CRM tools.

| Organism type | Tracks | Connection domain | NEVER gets |
|---|---|---|---|
| B2C | 8 dimensions of personal wellness | Personal health, life, habits | CRM, Jira, Slack workspaces, revenue tracking |
| B2B | Business KPIs (business 8D equivalent) | CRM, PM, financial, cloud, HR | Apple Health, wearables, personal fitness/meditation apps |
| B2BU | Professional performance (HCM) | Inherits B2B + productivity/professional-dev tools | Personal health apps, personal financial apps |

When the user says "connections" or "setup" or "configuration" WITHOUT specifying a type, build ALL THREE separately. Do NOT produce a single merged doc. Each type has its own manifest, its own exclusion list, its own setup flow. Mixing them is the exact failure pattern this rule exists to prevent.

## PHENOTYPE RULE (corrected 4 times in one session)

Two phenotypes. Never confuse them:

1. `phenotype_8d.py` = **PDFs and scientific reports ONLY.** Light paper, gold borders, tables, Helvetica, flat.
2. `phenotype_ds.py` = **ALL interactive products** (dashboards, chat, command center, organism tools). Dark night sky (#080d1a), moonlight (#e8d5a0), indigo (#6366f1), Inter font, rounded cards, noise texture.

The Fleet Atlas phenotype = PDFs ONLY. Never use it for dashboards. Never use the light phenotype for any interactive HTML. When a user says "use our phenotype" for a dashboard, they mean phenotype_ds.py (dark), not phenotype_8d.py (light PDF). Four corrections in one session came from getting this wrong.

## PROCESS FLOW SCOPE AWARENESS (2026-07-16)

The user frequently says "work through igigi process flows." Before routing, determine WHAT TYPE of work:

- **Creative/document production** (PDFs, marketing, branded assets): Route through the creative process flow (Goethe -> Wernicke -> Bell -> Luria). This is what the the operator agent creative pipeline is FOR.

- **Platform engineering** (HTML, registry, UI, tabs, engine data): There is NO defined creative process flow for this. Do NOT route platform work through the PDF pipeline. Route through the specialist engine (design production) or the specialist engine y Cajal (signal routing/infrastructure) instead. The user explicitly pointed out this gap.

- **Engine registry maintenance** (renames, metadata): Route through the registry maintenance skill, not the creative pipeline.

The wrong process flow is just as bad as no specialist at all. When the user says "process flow," ask what they mean if it is ambiguous. Do not assume creative pipeline for non-creative work.

## FULL SCOPE EXECUTION (2026-07-16)

The user's #1 frustration pattern across sessions: being told something is done, then discovering it was only partially done because the agent checked only 1-2 files when 7 copies existed.

**Before reporting ANY task as complete:**
1. Enumerate ALL files that reference the changed entity (grep across the full workspace)
2. Patch ALL copies, not just the one you found first
3. Restart ALL servers that cache the changed data (especially Python servers with .pyc)
4. Verify the live API serves the corrected data
5. Run the verification commands from the relevant skill's checklist

Partial execution is worse than no execution because it creates a false sense of completion.

## PDF EDIT DISCIPLINE (from session 2026-07-24)

When the user says "surgical edits" to a PDF document, that means:
1. Extract text with pdftotext to understand the full document
2. Make text replacements using PyMuPDF (fitz) redaction annotations
3. PRESERVE the original formatting, fonts, and layout
4. DO NOT regenerate from scratch with reportlab
5. DO NOT create a text file when they asked for the edited document

The user said "This is not edited or formatted like the original" when I rebuilt from scratch. The original PDF formatting IS part of the deliverable. Rebuilding loses it. See `baseline-first-surgical-precision` skill > "PDF surgical editing" section for the correct technique.

## WAVE COACHING ENGINE MOBILE (from session 2026-07-24)

When building mobile interfaces for the wave coaching engine:
- The coaching endpoint is `POST http://<tailscale-ip>:port/v1/coach` with body `{text, context, voice, conversation_history}`
- The HTML JavaScript must use the correct Tailscale IP, not a placeholder
- The wave engine server must bind to `0.0.0.0` not `localhost` for mobile access
- See `baseline-first-surgical-precision` > `references/mobile-tailscale-access.md`

## STRUCTURAL ENFORCEMENT (updated 2026-07-24)

The specialist gate plugin at `<agent-home>/plugins/specialist_gate/__init__.py` now blocks THREE tool types:
- `delegate_task` (always gated)
- `write_file` (gated for specialist artifacts)
- `terminal` (gated UNLESS command starts with a safe read-only prefix)

**Terminal bypass list** (commands allowed without routing):
curl, ls, cat, grep, wc, ps, lsof, echo, head, find, open, killall, sed -i, python3 -c, python3 /dev/stdin

Any terminal command NOT in this list requires valid specialist routing or it gets blocked.

**Three-layer enforcement:**
1. Skill (this file) - loads every session, binding instructions
2. Memory - warns it is existential
3. Plugin - structurally blocks tool calls without routing

**Known limitation:** There is no pre-response hook in the operator agent. You can still talk to the user as text without routing. But you cannot DO anything (build, write, execute) without specialist approval.

**Additional correction (2026-07-24):** When the user says "spin up the wave advisory panel" for a legal document, that is NOT a scientist panel. It is a LEGAL panel. Route through the specialist engine (legal writing) then build 5 legal agents (attorneys, litigators, evidence specialists) who run CONSECUTIVELY. THEN send the compiled output through adversarial reviewers (Popper, Kahneman, plus 2 user-specified methods). The user corrects this every time a scientist panel is spun up for legal work.

## LEGAL PANEL REQUIREMENTS (updated 2026-07-26)

When the user says "spin up the wave advisory panel" for legal work:

1. **Representation check FIRST:** Ask whether the party is PRO SE or REPRESENTED by counsel. This determines signature blocks, ethics framing, and certificate of service. Do NOT default to Pro Se.

2. **Elite university credentials:** Every legal agent MUST carry named elite school credentials (UT Law, Harvard, Stanford, Columbia, Yale) with specific years of practice and Texas/Montgomery County experience. The user said: "Full elite credentials from top universities. The only way we produce work."

3. **5 legal + 5 adversarial:** 5 legal domain agents (consecutive), then 5 adversarial reviewers (consecutive). All run one at a time.

4. **Adversarial panel always includes:** the specialist engine (language/AI telltales), the specialist engine (falsifiability), the specialist engine (cognitive framing), the specialist engine (strategic positioning), the specialist engine (utility calculus). The user said "find two more ways" beyond Popper+Kahneman. Machiavelli and Bentham are the two.

5. **Documents reviewed SYNERGISTICALLY:** When two+ documents work as a pair, BOTH must be reviewed together. No duplication. One exhibit list. Content assigned to one document only. Deliver both simultaneously.

6. **Panel output = surgical edits, NOT rewrites.** Apply each recommendation individually to the existing document. Do NOT rebuild from scratch. Run pre/post content audit to catch accidental deletions.

## SYNERGISTIC DOCUMENT WORK (2026-07-26)

When working on two+ documents that must work together (mastermind principle):

1. **Never deliver one without the other.** The user said: "This shouldn't even be done. This should only be partially done."

2. **Content assignment table BEFORE rebuild:** Map every topic to exactly ONE owning document. Other documents reference it ("as described in Respondent's Memorandum").

3. **One unified exhibit list** serves all documents.

4. **Filing order matters.** Usually: legal/framework document first, character/supplemental second.

5. **Sections stay separate.** Do not merge subsections during rebuild. Three dogs = three acquisition subsections. Transport = its own subsection. Pattern evidence = its own subsection.

## WORD DOC GENERATION FOR LEGAL DOCUMENTS (2026-07-26)

When producing an editable Word document for legal filings:

1. Use `python-docx` (not reportlab) - user explicitly said "make it a word doc"
2. Format: Times New Roman 12pt, double-spaced body, 1-inch margins
3. Court caption block with cause number and district
4. Section headings: centered, bold, underlined
5. Body paragraphs: justified, first-line indented 0.5 inches
6. Include: Verification (sworn statement under penalty of perjury), Certificate of Service, Exhibit List
7. Signature block with "/s/ Name" notation and "Pro Se" if self-represented
8. DO NOT use the AI telltale scan on legal documents - the scan is for creative/marketing content. Legal documents have their own conventions. The user will tell you if something sounds artificial.
