# B2B Body-System → Business-Function Mapping

When the task is "map body systems to B2B organism functions" (or "what business role does the [X] system serve"), the deliverable is a **B2B body-system mapping document** — a distinct class from design specs, synthesis docs, or deep dives. It translates each biological organ system into a concrete business function, then audits what the fleet has vs. what's missing.

## When this pattern applies

- "Map body system N to B2B function X"
- "For each body system: what existing engines serve this, what's MISSING, what document does it produce"
- Any task that assigns a fixed business meaning to a named biological system (integumentary=brand, skeletal=legal, muscular=operations, lymphatic=compliance, reproductive=IP creation)
- Extension of an existing B2B-BODY-SYSTEMS-MAPPING.md to cover more systems

## Do NOT create a parallel file — extend the canonical doc

**Critical (pitfall):** The baseline-first gate blocks `write_file` to a NEW path when a canonical artifact on the same topic already exists. If `B2B-BODY-SYSTEMS-MAPPING.md` already covers systems 1–6, do NOT create `B2B-BODY-SYSTEMS-MAPPING-7-11.md`. Instead:
1. `patch` the existing doc's title + scope note to broaden coverage (e.g., "1–6" → "1–11")
2. `patch` the existing doc's closing summary to append "Part 2" with the new systems

This mirrors the Fragmented List Reconciliation pitfall: never split a continuous enumeration across two files. The user should see ONE reconciled document covering all systems.

## Per-system triad (the fixed structure)

Each body system gets THREE subsections, always in this order:

### 1. Existing DS engines serving this
- Enumerate by `body_system` field in `ecs.py`: `grep -nB3 "body_system.*<system>" agent-organism/ecs.py | grep -E "directory|engine_name|ds-"`
- For each engine: cite port, DS-ECS code, scientist, LOC count (from ARCHITECTURE.md), and ONE line on what it = in business terms (italics)
- Include cross-system feeders (engines in OTHER body systems that feed this one) under a sub-bullet
- Mark PENDING engines explicitly (designed but not in ecs.py)

### 2. MISSING — needs to be built
- Distinguish capability gaps (no engine exists for this function at all) from wiring gaps (engine exists but no business process_flow registered)
- The fleet-wide finding: peripheral/organ engines have strong L1 physics but **zero or near-zero registered business process_flows** (per the 2026-07-07 immune audit). This applies to almost every peripheral system — call it out once per system.
- Flag registry inconsistencies (e.g., an engine classified differently in ecs.py vs verify_physics.py vs genesis_engine.py)

### 3. Business document / process this engine produces
- Name the concrete business artifact (e.g., "Legal Structure & Entity Graph", "Compliance & Immune Defense Report")
- For unwired capabilities, write "NEEDS BUILD" so the gap is visible
- Each artifact should map back to the engine's biological physics (e.g., Unna's wound-healing cascade → Reputation Wound-Repair Report with the same 4 stages)

## Cross-system interaction axes

After the per-system sections, include a coupling table:

| Axis | Systems coupled | B2B meaning |
|---|---|---|
| Skeleton ↔ Muscle | Skeletal (8) ↔ Muscular (9) | Legal structure defines the frame operations execute within |

These are the axes that make the individual systems a working organism. Cross-reference the PHYSIOLOGY-COMPLETE-BODY-SYSTEMS.md coupling pattern if it exists.

## Summary table (close every mapping doc)

| # | Body System | B2B Function | Primary Engine(s) | Status | Key Gap |
|---|---|---|---|---|---|

Status column: ✅ Strong / ⚠️ Thin / ❌ Missing, with engine count. The "Pattern:" paragraph after the table should name the 1–2 capability gaps (not just flow gaps) that are the real build priorities.

## Grounding rules

1. **Cite system NAME, not number.** `ecs.py`'s DOMAIN_MAP uses Gray's Anatomy numbering (Integumentary=1, Skeletal=2, Muscular=3, Lymphatic=7, Reproductive=11). Task numbering (7–11) can collide. Always key off the system name and note the discrepancy.
2. **Read the engine's actual source for physics claims.** `engine.py` docstring headers contain the real equations (e.g., Waddington's Landau `F(η)=a(T−Tc)η²+bη⁴`, Unna's `P=(K·D)/h`). Cite the equation, not "like diffusion."
3. **Cross-check `verify_physics.py` FLEET dict vs `ecs.py`.** Engines are sometimes classified inconsistently across the two (e.g., the specialist engine/Turing/Bragg skeletal classification differs). Flag these as "Registry ambiguity — flagged for reconciliation."
4. **Check operator ownership.** `agents.yaml` and `ONTOLOGY.md` §4-§6 map which operator (hermes/sibling-agent/sibling-agent) maintains each engine and which tissue layer wires it. Include this where relevant.
5. **No phantom engines.** Verify every cited engine exists in `ecs.py` FLEET_REGISTRY before writing (cf. organism-biological-isomorphism-verification Rule 12).

## Worked example

`~/your-workspace/organism/B2B-BODY-SYSTEMS-MAPPING.md` — 361-line mapping of all 11 Gray's Anatomy organ systems to B2B business functions. Part 1 (§§1–6) covers Nervous/Cardiovascular/Respiratory/Digestive/Urinary/Endocrine. Part 2 (§§7–11) covers Integumentary=brand, Skeletal=legal, Muscular=operations, Lymphatic=compliance, Reproductive=IP. Each system follows the existing/missing/document triad. Two headline capability gaps identified: (1) no external regulatory compliance engine, (2) no legal-entity/IP-holding structure engine.

## Dynamic complement

This pattern answers "what does each system DO in isolation." The companion pattern — `cross-system-process-flow-pattern.md` — answers "how does a business entity MOVE across systems through gates." Use both together: the static mapping establishes the per-system function vocabulary; the process-flow design shows the gates and handoffs that make the 11 systems work as ONE organism.
