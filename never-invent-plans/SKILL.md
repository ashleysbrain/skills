---
name: never-invent-plans
description: Prevent the recurring failure pattern of inventing your own build plans when a specialist roadmap already exists
trigger: When starting ANY build, phase, or engine work — check for existing specialist plans FIRST
---

# Never Invent Plans

## The Pattern This Prevents

After context compaction, the agent loses track of which roadmap is canonical and invents a new one from scratch. This wastes hours of work building the wrong engines in the wrong order, with the wrong names, for the wrong beneficiary.

**This is not a hypothetical risk.** On 2026-06-20, the agent committed this pattern THREE TIMES in a single session:
1. Built a hypothalamus engine named "the specialist engine" — wrong name (collided with an existing clinical panel seat), wrong plan (not in BRAIN-ARCHITECTURE.md), wrong framing (built "for 8D Sleep" instead of for the operator agent).
2. After being corrected, wrote a fabricated `neurodev-phase1-spec.md` with its own phase numbering and engine names — still not following the specialist-authored `BRAIN-ARCHITECTURE.md`.
3. After being corrected again, still framed the subcortex build as "what 8D Sleep needs" rather than "what the operator agent's brain needs."

The user's exact words: *"If you were going off your own plan, you need to adjust your brain because we've been working on this all morning, and you obviously know not to do this yourself... you're starting from scratch when we're already writing the middle of a project."*

## Rule

**Before building ANY engine, phase, or system component:**

1. Search for existing specialist plans FIRST:
   ```
   grep -rl "build.*order\|phase.*1\|roadmap\|tier.*1" docs/ | head -10
   find docs/ -name "*ARCHITECTURE*" -o -name "*roadmap*" -o -name "*phase*" | sort
   ```

2. If a specialist-authored roadmap exists, that IS the plan. Follow it exactly. Do not:
   - Invent your own phase numbering
   - Rename engines that the specialists already named
   - Reorder the build sequence
   - Create a competing spec document
   - Build "for a product" when the roadmap says "build for the organism"

3. If context was compacted, your FIRST action is to reconstruct the active plan from files, NOT to start building. Read the canonical roadmap, check the todo list, check git log, check what's running — THEN decide what to do next.

4. If no specialist plan exists, delegate to a specialist agent to CREATE one BEFORE building. The generalist orchestrates and delegates; it does not write its own biological specs.

## Checklist Before Any Build

- [ ] Is there a BRAIN-ARCHITECTURE.md or equivalent specialist doc?
- [ ] What phase are we in according to THAT document?
- [ ] What is the next engine in the build order according to THAT document?
- [ ] Has the user referenced a specific roadmap by name?
- [ ] Are the engine names I'm about to use the SAME names the specialists chose?
- [ ] Have I grepped the workspace for namesake collisions (see ds-organism-engine-creation skill)?
- [ ] Am I building for the operator agent (the organism) or for a product? If for a product, STOP — the operator agent builds first.
- [ ] **Before designing ANY system that touches reproduction, product birth, or organism spin-up: have I read `docs/WOMB-ARCHITECTURE.md` (DS-ARCH-09.01.01-v2.0.0, 818 lines, LOCKED)?** This is the canonical source for the three-tier potency hierarchy. Designing a reproductive system without reading it first produces architecture violations that the user will catch.

## Red Flags

- You're creating a new spec file when one already exists → STOP
- You're naming engines that don't appear in the specialist roadmap → STOP
- You're reordering phases from what the document says → STOP
- You're building "for a product" when the user said "build for the operator agent first" → STOP
- You're writing a biological spec yourself instead of delegating to a specialist → STOP
- You're assigning a namesake without grepping the full workspace → STOP
- You're about to write code and haven't confirmed which canonical document governs → STOP
- You're designing a reproductive or birth system and haven't read WOMB-ARCHITECTURE.md → STOP
- You're proposing that an organism can "earn" or "unlock" a capability that is actually a cryptographic potency boundary → STOP (this is a locked architecture violation, not a design choice)
- You're implementing a feature the user references as "the X I worked on in telegram" and you haven't searched `state.db` for the actual instruction → STOP
- You're pulling data from the nearest available structure because the real source was lost to context compaction → STOP
- You're displaying a physics/science concept as static text (checkmarks, labels, badges) when the user expects it to be OPERATIONAL (computing real values, emitting verdicts, driving behavior) → STOP. If the user says "physics profiles" or "gates," they mean functioning gates with real math, not decorative labels. See `computeArchetypeGates()` in agent-organism-interface-building skill.

## The Production Line Direction (Critical)

```
the operator agent (the organism) — has a COMPLETE brain built FIRST
    ↓ the brain runs the operator agent's own intelligence
    ↓ the operator agent decides to produce a product
    ↓ Medawar birth canal + phenotype spec
    ↓ production line pushes DOWN
Product (8D Sleep, future products) — inherits capabilities from the operator agent
```

NEVER build brain engines "for" a product. Brain engines exist because the operator agent needs a complete brain. A product can only be as intelligent as the organism that births it. The user was explicit: *"you're just building on to 8D sleep that I need you to be building the operator agent and then the operator agent pushes this production line to from the start."*

If you catch yourself thinking "this engine will help 8D Sleep do X," reframe immediately: "the operator agent needs this engine to have a complete brain. Once the operator agent has it, the production line will push the capability down to products."

## Roadmap Status Review Protocol (2026-07-19 Lesson)

When asked to review whether a long-lived roadmap's milestones are on track
(recurring weekly cron pattern), the roadmap document is the **claimed
state**. Your job is GROUND-TRUTH VERIFICATION, not summarization. On
2026-07-19, the `ORGANISM-ROADMAP-AND-CONFERENCE-2026.md` Phase 1 table
showed milestones marked "Scheduled" that never happened — including a
July 15 TSC abstract submission that passed with zero submission evidence.
Reading the table alone would have produced a falsely optimistic report.

**Rule: every milestone in the roadmap must be checked against an
independent ground-truth source before you mark it complete or on-track.
Roadmap tables rot if no one verifies them.**

Independent ground-truth sources, strongest first:

1. **Live service probes** — `curl http://localhost:PORT/organism/health`
   (note: `/organism/health` for fleet summary, not bare `/health` which
   only returns gateway status). Returns JSON with per-engine status.
2. **Operator bus** — the canonical SQLite at
   `/<workspace>` (NOT the agent-organism
   subfolder copy, which is a fragment). Use
   `python3 organism/opencode_bus_read.py --since N --json`. Messages from
   `sibling-agent` confirm sibling work actually shipped; absence of any
   `sibling-agent` inbound during a milestone window is itself a red flag.
3. **Filesystem archaeology** — `search_files` for the named deliverables
   the roadmap promises (e.g., "Bernard", "Cannon", "abstract", "VERITAS").
   Zero files = milestone not started, regardless of what the table says.
4. **Immune patrol** — `python3 scripts/ds-metchnikoff.py --json` runs the
   organism's own innate immune scan. Non-zero CRITICAL findings = real
   gaps the roadmap didn't surface.
5. **External verification for dated events** — if the roadmap references a
   conference, deadline, or external event, web-search the current status.
   On 2026-07-19 the workspace also contained a `TSC-2026-PREPARATION.md`
   claiming "TSC 2026 CANCELLED" — that referred to a DIFFERENT TSC
  (Tucson, April). The roadmap's TSC San Diego (October) was real.
   Conflicting stale docs about the same event are common; resolve by
   checking the authoritative external source, not by guessing.

See `references/roadmap-ground-truth-verification.md` for the concrete
recipes (bus queries, health endpoints, engine-count heuristics and the
false-negatives they produce, immune-patrol interpretation).

## Post-Compaction Recovery Protocol

When context compacts mid-build session:

1. **Do NOT start building.** Read files first.
2. Find the canonical roadmap: `ls docs/*ARCHITECTURE* docs/*phase* docs/*spec*`
3. Check the todo list (if preserved through compaction)
4. Check what's running: `curl -s http://localhost:PORT/health` for known ports
5. Check git log for recent work: `git log --oneline -10`
6. Only THEN decide what to do next
7. If uncertain, ask the user which roadmap/phase to follow — do NOT guess

### When the User Says "The X I Worked On" (2026-07-16 Lesson)

When the user references something they previously specified ("the voice options I worked on in telegram"), and you cannot find it through normal memory or session_search, use **direct SQLite queries on state.db**:

```python
import sqlite3
db = sqlite3.connect('/<workspace>')
db.row_factory = sqlite3.Row
# Find sessions by source and date
rows = db.execute("""
    SELECT id, source, datetime(started_at, 'unixepoch') as started, title
    FROM sessions WHERE source = 'telegram'
    AND started_at > strftime('%s', '2026-07-01')
    ORDER BY started_at DESC
""").fetchall()
# Then query messages in that session for keywords
rows = db.execute("""
    SELECT DISTINCT content, datetime(timestamp, 'unixepoch') as ts, id
    FROM messages WHERE session_id = ?
    AND role = 'user' AND content LIKE '%voice%' OR content LIKE '%persona%'
    ORDER BY timestamp ASC
""", (session_id,)).fetchall()
```

Key details:
- `state.db` is at `/<workspace>` (~6GB)
- Messages are duplicated across compaction branches (one message may appear 15+ times with different IDs). Use `DISTINCT content` to dedupe.
- `session_search` tool has limited FTS5 coverage for recent Telegram sessions. Direct SQL is more reliable.
- Skip `[CONTEXT COMPACTION`, `[ASYNC DELEGATION`, `[IMPORTANT:`, `[OUT-OF-BAND` prefixed content — these are system noise.
- Voice messages that failed transcription show as `[voice message could not be transcribed]` — these are LOST instructions.

**Never substitute the nearest available data structure for the real source.** On 2026-07-16, the persona system was implemented WRONG 3+ times because the agent grabbed `getArchetypeVariant().voice` (archetype variant data) instead of finding the actual persona system definition in the the specialist engine migration plan. The user said: *"this is silly how i have to have to repeat work."*

## the specialist engine

- **Canonical brain roadmap:** `docs/BRAIN-ARCHITECTURE.md` (246 lines, specialist-authored 2026-06-19)
- **Canonical reproductive architecture:** `docs/WOMB-ARCHITECTURE.md` (818 lines, DS-ARCH-09.01.01-v2.0.0, LOCKED the principal-approved). Governs the three-tier potency hierarchy (Grandmother FULL, B2C/B2B PARTIAL, Products NONE), womb/gonad structure, soul composition, DNA protection, and security model. Read BEFORE designing any reproductive, birth, or organism-spin-up system.
- **Other locked architectures:** Before writing ANY design document, spec, or build plan, check whether a locked architecture doc already governs the domain. Search `docs/` and the workspace root for `*ARCHITECTURE*` files. If one exists, read it completely before writing a single line of your design doc. **2026-07-07 lesson:** I wrote a 235-line software factory design without reading the locked WOMB ARCHITECTURE, then invented a "competence period" escalation path that directly violated the locked potency hierarchy. The user caught it. The cost was a full rewrite. The rule: locked architecture docs are read-first, not referenced-later.
- **Phase 0 spec:** `docs/neurodev-phase0-spec.md` (CLOSED 2026-06-20)
- **Phase 0 closure:** `docs/phase0-closure-signoff.md` (29/29 PASS)
- **Phase 0 audit:** `ds-engine-registry/phase0_audit.py` (32/34 behaviors pass; 2 gaps: developmental FSM 3.3, spawn factory 5.4)
- **Specialists build the plans.** The agent executes them. If no specialist plan exists, delegate to a specialist agent to create one BEFORE building.
- **For the full DS engine creation methodology** (five-layer architecture, dual specialist mandate, namesake checks, embryological phases), load `ds-organism-engine-creation`.
