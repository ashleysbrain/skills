# Cross-System Process Flow Design

When the task is "design N end-to-end business process flows that cross multiple body systems" or "show how the organs coordinate for [scenario]," the deliverable is a **cross-system process flow document**. This is the DYNAMIC complement to the static B2B body-system mapping (`b2b-body-system-mapping-pattern.md`): the static doc says what each system IS; the process-flow doc says how work MOVES across them.

## When this pattern applies

- "Design 5-7 end-to-end business process flows that cross multiple body systems"
- "Show how the organs coordinate for customer onboarding / IP creation / incident response"
- "How does a [thing] move from [system A] to [system B] to [system C]?"
- Any task asking for a biological pathway with named gates across systems

## Distinct from adjacent patterns

| Pattern | Question answered | Document class |
|---------|-------------------|----------------|
| B2B body-system mapping (static) | What does each system DO in isolation? | Per-system audit (existing/missing/document) |
| Cross-cutting synthesis | How does mechanism X work end-to-end across LOCKED SPECS? | Design doc stitching specs |
| **Cross-system process flow (THIS)** | **How does a business entity MOVE through the organism?** | **Pathway catalog with gates** |
| Design spec | What are we building in phase N? | Phase deliverable |

## The canonical reference table (always lead with this)

Every cross-system flow document begins with the system -> engine -> business-function table, grounded in the real fleet. The current canonical mapping (from PHYSIOLOGY-COMPLETE-BODY-SYSTEMS.md + ecs.py):

| # | Body System | the specialist engine | Port | Business Function |
|---|-------------|-----------|------|-------------------|
| 1 | Nervous (cognition) | Wave | 8010 | Strategy, perception, decision |
| 1 | Nervous (autonomic) | Quartz | 8089 | Task scheduling, timing root |
| 1 | Nervous (homeostatic) | Allostasis | 8091 | Setpoints, vital-sign integration |
| 1 | Nervous (developmental) | Morphogen | 8093 | Patterning, registry (see ambiguity pitfall) |
| 2 | Respiratory | Haldane | 8098 | Marketing, lead acquisition |
| 3 | Digestive | Beaumont | 8094 | Intake, onboarding |
| 4 | Cardiovascular | Harvey | 8092 | Billing, cash flow |
| 5 | Musculoskeletal | Hill | 8101 | Execution, delivery |
| 6 | Immune/Lymphatic | Burnet | 8100 | Compliance, QC, risk |
| 7 | Integumentary | Unna | 8097 | Branding, reputation |
| 8 | Reproductive | Reproductive (Waddington) | 8090 | IP gestation, R&D |
| 9 | Endocrine | Sutherland | 8099 | Culture, incentives, coordination |
| 10 | Excretory | Bright | 8096 | Offboarding, write-offs, filtration |
| 11 | Sensory | Helmholtz | 8102 | Environmental sensing, market research |

**Note on the 11th system:** PHYSIOLOGY-COMPLETE-BODY-SYSTEMS.md counts Sensory (Helmholtz) as the 11th canonical system. Gray's Anatomy lists 11 differently (Urinary vs Excretory naming; Sensory folded into Nervous). For business mapping, the PHYSIOLOGY 11-system list is authoritative because it maps cleanly to the engine fleet. The static B2B mapping skill uses Gray's numbering — note the discrepancy explicitly in any document that references both.

## Per-flow structure (the fixed anatomy)

Each flow in the document follows this structure:

### Header
- **Biological analog** (one line: what physiological process this mirrors)
- **Flow category** from the 8 canonical PROCESS-FLOW-CATEGORIES.md categories (neuromodulatory, autonomic, oscillatory, metabolic, homeostatic, sensorimotor, structural_plasticity, endocrine). Never invent categories.
- **Trigger** (what event starts the flow)

### Stage table
Each flow is a table with one row per stage:

| Stage | System -> Organ | Implementing Engine | Gate | Handoff Signal | Gate-Fail Route |
|-------|----------------|---------------------|------|----------------|-----------------|

- **System -> Organ**: the biological role (e.g., "Cardiovascular -> Left Ventricle")
- **Implementing Engine**: eponym + port (e.g., "Harvey (8092)")
- **Gate**: italicized named check (e.g., "*Ossification Gate*: MSA signed, terms registered")
- **Handoff Signal**: `noun.verb` format (e.g., `contract.set`, `revenue.flowing`)
- **Gate-Fail Route**: where the entity goes if the gate fails (never blank — always routes to a defined destination)

### Footer
- **Pathway summary**: the engine sequence in arrow notation (Haldane -> Beaumont -> Burnet -> ...)
- **End state**: what the entity looks like when the flow completes

## Gate conventions (enforced)

1. **Every gate is named** (italicized), binary-or-scored, and logged.
2. **A gate that fails NEVER drops the entity** — it routes to a defined destination (last column). Typical fail-routes: Excretory/Bright (release), Nervous/Wave (escalation), Endocrine/Sutherland (re-calibration).
3. **Failed gates emit `gate.fail`** events observable by Allostasis (8091) for allostatic-load accrual and Wave (8010) for pattern detection.
4. Gates map to the canonical physiology: Burnet's gates use immune metaphors (Antigen, Quarantine, Clonal-Memory), Harvey's use cardiac metaphors (Systole, Diastole), etc.

## Handoff signal convention

- Format: `[noun].[verb]` (e.g., `contract.set`, `revenue.flowing`, `immunity.acquired`).
- Signals are the CONTRACT between systems. Harvey does not care how Hill contracted, only that `work.accepted` was emitted.
- Quartz (8089) is the timing root for all signal emission.

## Recurring loops (identify these in the closing section)

Every flow document should identify which feedback loops are in play:
- **Immune learning loop** (Burnet clonal memory) — faster detection next time
- **Metabolic pacing loop** (Sutherland endocrine) — throttles via resource gates
- **Allostatic observation loop** (Allostasis/Sterling) — integrates vitals continuously
- **Perception-action loop** (Wave) — opens/closes every flow

## Isomorphism verification (run before delivery)

After drafting, verify every engine/port reference against ecs.py:
```python
import re
mentions = re.findall(r'\*\*(\w+)\*\*\s*\((\d+)\)', doc_text)
# check each against canonical registry; flag any mismatch
```
Zero mismatches required. Common phantom engines to watch for: the specialist engine, the specialist engine, the specialist engine, the specialist engine (see organism-biological-isomorphism-verification Rule 12).

## The Morphogen ambiguity (known pitfall)

Morphogen (the specialist engine, port 8093) is classified differently across architecture docs:
- `AI_Organism_Body_Architecture.md` lists it as "Skeletal / Registry"
- `PHYSIOLOGY-COMPLETE-BODY-SYSTEMS.md` lists it under "Nervous (developmental)"
- `tissue-layer-architecture-shift.md` documents it as the reproductive-subsystem patterning component
- The static B2B mapping assigns Skeletal = legal/corporate structure

**Resolution for process flows:** when a flow needs "Skeletal (legal/contracts)," the implementing engine is Morphogen per the registry, BUT verify against the live ecs.py body_system field before committing to it in a flow document. Flag the ambiguity in a footnote. Do NOT silently pick one classification.

## Worked example

`/<workspace>` (2026-08-11, 246 lines) — 7 cross-system flows:
1. Ingestion (customer onboarding): Haldane -> Beaumont -> Burnet -> Morphogen -> Hill -> Harvey -> Unna
2. Gametogenesis (IP creation): Wave -> Sutherland -> Reproductive -> Morphogen -> Unna -> Haldane -> Hill
3. Inflammatory Response (incident/breach): Burnet -> Quartz -> (Morphogen // Bright) -> Unna -> Haldane -> Sutherland -> Burnet
4. Apoptosis (churn/offboarding): Unna -> Wave -> Harvey -> Morphogen -> Bright -> Burnet -> Haldane
5. Circulation (revenue cycle): Hill -> Harvey -> Beaumont -> Harvey -> Morphogen -> Bright
6. Hematopoiesis (talent onboarding): Haldane -> Beaumont -> Burnet -> Morphogen -> Sutherland -> Hill -> Harvey -> Unna
7. Homeostatic Adaptation (strategic pivot): Helmholtz -> Allostasis -> Burnet -> Wave -> Sutherland -> Morphogen -> Hill -> (Haldane + Unna) -> Reproductive -> Bright

Each flow: biological analog, flow category from the 8 canonical, trigger, stage table with named gates, pathway summary, end state. 56 named gates total, 14 engines verified with zero port mismatches. Closing section covers gate semantics, handoff signals, recurring loops, and per-system flow participation matrix.

## Cross-link

- Static per-system mapping: `references/b2b-body-system-mapping-pattern.md` (what each system IS)
- Synthesis across locked specs: `references/cross-cutting-synthesis-pattern.md` (how a mechanism works end-to-end)
- This pattern: how a business entity MOVES across systems through gates
