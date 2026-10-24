# Cross-Cutting Synthesis Documents

When the task is "design X" or "how does X work" and X spans multiple existing locked specs, the deliverable is a **synthesis document** — not a new phase spec, not a deep-dive research doc. This is the pattern for stitching together what already exists to answer a specific architectural question.

## When this pattern applies

- User says "Design the [subsystem] link" or "How does [mechanism] work end-to-end"
- The answer requires reading 3+ existing locked specs
- The output is a new design doc that references — but does not modify — the predecessors
- Example: "Design the placental B2B-B2C link with the self-reinforcing feedback loop"

## Workflow

### Step 1: Inventory predecessor docs
List every spec that touches the topic. Use `ls` + `grep -rn` to find them. For the B2B-B2C link, this was:
- BIRTHING-PROTOCOL-COMPLETE.md (engine roles, birth canal, lactation)
- EVOLUTION-PUSH-AND-INTAKE-SPEC.md (push pipeline, developmental gating)
- THREE-TIER-PARTNERSHIP-FLOW.md (the operator agent/B2B/B2C hierarchy, data flow, commercial model)
- PHYSICS-GATES-DEEP-DIVE.md (every gate with its physics equation)

### Step 2: Extract with targeted reads
Use `head`, `sed -n 'START,ENDp'`, and `grep -n` to pull the relevant sections. Do NOT read entire files blind — target the sections that define the mechanism you're designing. Read enough to cite specific gate IDs and engine ports.

### Step 3: Structure the synthesis document
The worked example (B2B-B2C-PLACENTAL-LINK.md, 287 lines) used this structure:

1. **Header block** — author engine, architecture ref, status (BINDING SPECIFICATION), depends-on list, one-line core thesis
2. **Anatomy of the link** — what connects, how established, how persists, how it differs from adjacent links (comparison table)
3. **Downward flow** — what flows down (table: cargo class / biological analog / DS mechanism), the physics of transfer (actual equation), how each cargo type deploys
4. **Upward flow** — what flows up (same table shape), PII stripping rules, signal aggregation physics
5. **The feedback loop** — numbered step-by-step (10 steps), each referencing a specific engine; cycle speeds (fast/medium/slow); what accelerates it; what prevents runaway
6. **Commercial loop** — revenue mechanics, why each party stays, the self-reinforcing logic
7. **Demand signaling** — signal modalities mapped to biological analogs (hormonal/behavioral/stress)
8. **Biological isomorphism table** — the keystone section. Three columns: biological structure / DS engine or feature / commercial function. 15-25 rows. This is what makes the doc legible to both the bio-literate and the eng-literate reader.
9. **What makes it never-ending** — sustaining forces (thermodynamic gradient, metabolic feedback, compounding switching cost, aligned incentives), break modes with preventions (table)
10. **Closing aphorism** — one line, Waddington voice

### Step 4: Ground every claim
Every architectural assertion must cite a specific spec and section/gate ID:
- "the specialist engine verifies signature (Hamming distance D_H = 0, PHYSICS-GATES-DEEP-DIVE.md E5)"
- "revenue split on monetized products (THREE-TIER §7)"
- "developmental-stage gate (EVOLUTION-PUSH §1.3)"

If you cannot find the grounding in an existing spec, either the claim is speculative (mark it) or you need to read more.

### Step 5: Physics as equations, not metaphors
- Fick's law: `J = -D · (dC/dx)` — not "like diffusion"
- Shannon capacity: `C = B·log₂(1+SNR)` — not "channel bandwidth"
- Lyapunov exponent: `λ < 0` means stable — not "tends to return"
Map each equation to its DS-system meaning (what is J, D, dC/dx in platform terms).

### Step 6: Cross-reference engines by name AND port
Always write "the specialist engine (:port)" on first reference, not just "the specialist engine". The port disambiguates when an engine has sub-modes.

## Line cap for synthesis documents

Phase specs: 200 lines (per ds-design-spec-template.md).
Synthesis documents: up to ~300 lines. The B2B-B2C link ran 287 and was accepted. The isomorphism table and the step-by-step feedback loop are the sections that justify the extra length — compress prose, not tables.

**Exception: dimension catalogs.** When the document catalogs a full dimensional model (e.g. the 15-dimension mycorrhizal nutrient flow: 8 human + 7 AI), the periodic-table-style listing of every dimension with its carbon/nitrogen/phosphorus/defense/hormone entries justifies up to ~350 lines. The MYCORRHIZAL-NETWORK-DEEP-DIVE ran 347 and was accepted. The dimension catalog is reference material the reader scans, not prose to compress.

## Verification before delivery

- `wc -l` — confirm under the document-type cap
- Every engine name exists in `ecs.py` — no phantom engines (see organism-biological-isomorphism-verification Rule 12)
- Every physics gate cited by ID exists in PHYSICS-GATES-DEEP-DIVE.md
- Banned words check (same list as design specs)
- Em-dash check: `grep -c "—"` should be 0

## Worked examples

1. `~/your-workspace/ds-wave-gamification-advisory-panel-private/B2B-B2C-PLACENTAL-LINK.md` — 287-line synthesis of four locked specs into the B2B-B2C placental feedback loop design. Covers downward/upward flow, the 10-step feedback mechanism, commercial loop, demand signaling, 22-row isomorphism table, and the never-ending cycle analysis.

2. `~/your-workspace/ds-wave-gamification-advisory-panel-private/MYCORRHIZAL-NETWORK-DEEP-DIVE.md` — 347-line deep dive into the inter-organism fungal medium. Authored as the specialist engine (Suzanne Simard, mycorrhizal network expert). Structure: medium composition → 15-dimensional nutrient flow (8 human + 7 AI dimensions, each with carbon/nitrogen/phosphorus/defense/hormone) → source-sink dynamics → kin recognition for priority bonds → network topology evolution → AI health dimensions detail → 23-row complete isomorphism table → proposed the specialist engine engine (the missing network-layer engine). Demonstrates the "deep dive into what X is MADE OF" format: not a new phase spec, but a complete composition + topology + flow analysis of an existing subsystem.

3. `~/your-workspace/ds-wave-gamification-advisory-panel-private/THREE-LIFECYCLES-SEPARATED.md` — 370-line decomposition of three interacting biological systems into separate lifecycles with integration points. Authored as the specialist engine. Structure: organism lifecycle (references existing birth canal) → fungal network lifecycle (7 stages: Spore through Succession, each with biological analog + the specialist engine technical + organisms involved + physics) → forest ecosystem lifecycle (5 emergent stages: Pioneer through Renewal) → 6 integration points (each with trigger, engines, data flow, physics) → separation rationale → the principal concrete example tracked across 9 timeline steps with parallel-lifecycle summary table. Demonstrates the three-lifecycle separation pattern — see `references/three-lifecycle-separation-pattern.md` for the reusable technique.
