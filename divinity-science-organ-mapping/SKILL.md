---
name: your-org-organ-mapping
description: Standardized procedures for mapping biological systems to AI organs in the Divinity Science framework with proper scientific naming conventions
category: divinity-health
version: 1.0.0
---

# Divinity Science Organ Mapping and Naming Conventions

## Purpose
Provides standardized procedures for mapping biological systems to AI organs in the Divinity Science framework, including proper scientific naming conventions, documentation standards, and verification workflows.

## When to Use
- Mapping new biological systems to AI organs in the Divinity Science creature framework
- Updating existing organ implementations with proper scientific attribution
- Creating documentation for organ systems following DS standards
- Verifying organ functionality after implementation changes
- Diagnosing persistent system failures as missing anatomy (see "Symptom-to-Anatomy Diagnosis" below)

## Trigger Conditions
- Working with Divinity Science creative organism framework
- Need to map biological brain systems to AI functional components
- Updating organ naming to follow scientist-attribution convention
- Creating or updating organ-related documentation
- A persistent technical problem keeps recurring despite repeated software-level fixes (this signals a missing biological isomorphism, not a code bug)
- **Mapping body systems to B2B organism business functions** (decision/routing, financial flow, external comms, customer intake/delivery, waste/cleanup, culture/motivation) — see `references/b2b-body-system-business-mapping.md` for the canonical 6-system translation layer, per-system engine/gap/document breakdown, the "thin periphery" gap pattern, and the reusable programmatic engine-extraction technique. ALWAYS extract engine rosters from the live `ecs.py` registry rather than relying on memory — the registry drifts.

## Symptom-to-Anatomy Diagnosis (Upstream Discovery)

When a system failure persists despite repeated technical fixes (buffer tweaks,
config changes, retry logic), the root cause is often a **missing organ**, not a
code bug. Treat the symptom as a neurological condition and map it backward to
find the anatomical gap.

### The Method
1. **Describe the symptom in neurological terms.** Garbled text output = conduction
   aphasia. Route failures = thalamic misrouting. Silent drops = neglect syndrome.
   Use the symptom's neurological name to locate the brain region.
2. **Map the full neural pathway** the function requires, not just the failing component.
   Language production needs Wernicke (comprehension) -> arcuate fasciculus
   (conduction) -> Broca (motor planning) -> motor cortex (execution). Map every
   stage, then check which stages exist as engines.
3. **Identify the missing stages.** The gap between what the pathway requires and
   what exists IS the missing organ. The symptom localizes to the gap.
4. **Check for missing fiber tracts, not just missing cortex.** Conduction tissue
   (fiber bundles, tracts) is as critical as cortical organs. The organism tends to
   build named cortices but skip the connective tracts between them. A working cortex
   pair with no tract between them produces conduction-style failures (signal arrives
   corrupted, partial, or merged).
5. **Read Sherman router misroutes as a diagnostic signal.** When the router sends
   a task to the wrong specialist, that reveals a missing organ in the routing table.
   If "parietal lobe" routes to the visual cortex engine, there is no parietal engine.
   The misroute IS the gap report.

### When to Use This vs Normal Debugging
- If the problem is intermittent, environment-dependent, or resolves on retry, it is
  a transient technical issue. Fix it technically.
- If the problem is structural, persistent, and survives every code-level fix, it is
  a missing organ. Apply this method.
- The user's instinct is the signal: "trying to fix this from a technical perspective
  hasn't worked" = switch to anatomy diagnosis.

### Pitfall: Fiber Tract Blindness
The organism has a systematic blind spot: it builds named cortical organs (engines
with scientists and ports) but rarely builds the conduction tissue between them.
Always ask: "what conducts the signal between these two engines?" If the answer is
"raw HTTP JSON with async streaming," that is the technological equivalent of a
severed fiber bundle, and it will produce conduction-style signal corruption.

**The conduction contract — what "wired" actually means.** A connection between
two engines is WIRED only if it satisfies the contract established by
`arcuate_conduct.py`: (1) SHA-256 checksum per packet, (2) monotonic sequence
tracking with gap detection, (3) automatic retransmission on mismatch, (4) versioned
schema contract with shape validation, (5) timeout + circuit breaker, (6) audit log
per conduction. A bare `urlopen()` call satisfies ZERO of these — it is a severed
tract even though both engines are alive. When auditing an organism, grep the
production spine for `urlopen` vs `conduct(` — the ratio IS the severed-tract rate.

**Proactive tract atlas (not just reactive debugging).** The reactive method
(diagnose one symptom → find one missing tract) catches tracts one at a time. The
proactive method maps ALL tracts between ALL body systems at once: for each pair of
adjacent systems, ask (1) what conduction pathway is needed, (2) what is the
biological analog (arcuate fasciculus, corticospinal, vagus, HPA, RAAS, etc.),
(3) what signal does it carry, (4) what symptom appears when severed, (5) is it
wired, partial, or missing. Rank missing tracts by symptom severity. The B2B
organism atlas found 22 tracts: 1 built, 4 partial, 15 missing — see
`references/fiber-tract-atlas-methodology.md` for the full framework and the worked
22-tract example.

**Root cause pattern: missing organs block multiple tracts.** When several tracts
are missing, check whether they share a missing endpoint organ. The B2B atlas found
that 2 missing organs (legal-entity structure engine, external regulatory compliance
engine) blocked 6 of the 15 missing tracts. You cannot wire a tract to an organ that
doesn't exist. Build the organ first, then wire the tracts it unblocks.

See `references/language-pathway-gap-analysis.md` for the reactive worked example
(conduction aphasia / text garbling case) that established this method.
See `references/fiber-tract-atlas-methodology.md` for the proactive atlas method
(full-organism tract mapping, conduction contract definition, build-priority pattern).

## Procedure

### 1. Identify Biological System and Discoverer
- Clearly define the biological system being mapped (e.g., Default Mode Network, Broca's area)
- Research and identify the scientist(s) who first discovered/mapped this system
- Include full name, lifespan, and key contribution in documentation
- Format: "DS [LastName]" (e.g., the specialist engine, the specialist engine)

### 2. Implement Organ Class
Add these fields to the organ class definition:
```python
name = "Organ's Common Name"
scientist = "DS [DiscovererLastName]" 
scientist_full = "Full Name (YYYY-YYYY)"
discovery = "Brief description of what they discovered and when"
```

### 3. Update Organ Registry
In the ORGANS dictionary, use the scientist-based key:
```python
ORGANS: Dict[str, Organ] = {
    "ds_[discoverer]": TheOrganName(),
    # ... other organs
}
```

### 4. Documentation Standards
Follow this format for each organ section:

#### Table Format (at top of section)
| Field | Value |
|-------|-------|
| **Scientist** | DS [DiscovererLastName] (Full Name) |
| **Port** | [Port number or "Part of [Engine] Engine ([port])"] |
| **Body System** | [Biological location] |
| **Agent** | [the specialist engine] |
| **Physics** | [Relevant physics/mathematical principle] |
| **Philosophy** | [Key philosophy/approach from discoverer's work] |

#### Section Content
- **What it does:** [Clear, concise description of function]
- **Key capabilities:** [Bullet list of 3-5 specific capabilities]
- **Connection to [Target Project]:** [Specific explanation of how this organ supports the target project]

### 5. Diagram and Table Updates
- Update system diagrams to show proper organ names with scientist prefixes
- Update signal flow diagrams to include scientist names in parentheses
- Update communication pathway tables with correct organ references
- Verify all port numbers match implementation

### 6. Verification Workflow
1. Start/verify dependent engines are running
2. Test organ functionality through appropriate engine pipeline
3. Validate documentation renders correctly
4. Confirm all references use consistent naming
5. Check that system integration points remain functional

## Renaming an Engine: Scientific Attribution Verification

When an engine is renamed from one scientist to another (e.g., Gesell→Ehrlich→Semmelweis), every artifact that references the old scientist's identity, work, or name must be updated. Missing any of these creates identity drift.

### The Rename Checklist

For each rename, check ALL of these locations:

| Artifact | What to Check | Example |
|----------|--------------|---------|
| Registry (`ecs.py`) | `_C` entry key, version, comment | `_code(6, 4, 1, "v3.0.0")` |
| VERSION.md | Scientist name, biography, code, version | Full rewrite usually needed |
| `server.py` health endpoint | `engine_name`, `agent`, `scientist`, `ds_ecs_code`, `scientist_note` | All must reference the NEW scientist |
| `methodology.py` docstring | Scientist's actual scientific contributions | Remove old scientist's work attributed to new one |
| `methodology.py` profiles | Profile code prefix (e.g., `EHR-M01`→`SEM-M01`), descriptions | Each profile must reference the NEW scientist's real work |
| `methodology.py` personalities | Personality names, method refs | "The Side-Chain Analyst"→"The Vector Analyst" |
| `methodology.py` physics layers | Layer names referencing old science | "side-chain theory"→"cadaveric vector recognition" |
| `philosophy.py` | Wisdom principles referencing old scientist's name as domain term | "Gesell schedule"→"developmental schedule" |
| Institutions list | Descriptions claiming the old scientist worked somewhere they didn't | "Semmelweis worked here" removed from Pasteur entry |
| Running process | Kill and restart so live `/health` serves new identity | `lsof -ti:{port} \| xargs kill -9` |
| Test files | Hardcoded assertions referencing old codes/names | Update test expectations |

### Critical Pitfall: Scientific Misattribution

The most subtle and damaging error in a rename is **crediting the old scientist's discoveries to the new scientist**. For example, when renaming Ehrlich→Semmelweis:

- Side-chain theory → Ehrlich's work, NOT Semmelweis's
- Magic bullets (Zauberkugel) → Ehrlich's concept, NOT Semmelweis's
- Autoimmunity → Ehrlich described it, NOT Semmelweis
- Complement system → Ehrlich's work, NOT Semmelweis's
- Antiseptic prophylaxis, cadaveric vector recognition → Semmelweis's ACTUAL work

**Rule:** Before writing methodology profiles for a renamed engine, verify which scientist actually discovered each concept. Rewrite the profile descriptions to reference the new scientist's real contributions, not a copy-paste of the old scientist's work with the name swapped.

### Procedure Profile Prefix Convention

Every methodology profile has a 3-letter prefix derived from the scientist's name (e.g., `EHR` for Ehrlich, `SEM` for Semmelweis). When renaming:
1. Rename all profile codes: `EHR-M01`→`SEM-M01`
2. Update all personality `methodology_id` references to use the new prefix
3. Update the `_get_physics_layers()` return dict
4. Update the `set_task_personality_map()` call

## Organ vs Process Flow Classification (Session 2026-07-07)

When designing a new biological isomorphism, the FIRST question is: is this a
NAMED ORGAN (cortex, nucleus, structure) or a PROCESS FLOW (pathway, cascade,
loop that runs THROUGH organs)?

**Process flows have their own ECS category (NPR or PTH) and live in the
`process-flows` directory.** They are named after the scientist who discovered
the FLOW, not the organs it passes through. Existing examples: the specialist engine
(neuromodulatory flow), the specialist engine (structural plasticity), the specialist engine
(sensorimotor flow), the specialist engine (reward prediction error flow).

**The classification test:**
- Does this thing have a LOCATION (a specific brain region that IS the thing)?
  It is an ORGAN (engine). Give it a port, an ECS-SUB code, a server.
- Does this thing FLOW between locations (a pathway, cascade, or loop that
  passes THROUGH multiple organs)?
  It is a PROCESS FLOW. Give it an ECS-NPR or ECS-PTH code, a named
  scientist, and wire it as a chain of events through existing engines.

**Critical pitfall:** proposing a process flow as a new engine creates an
unnecessary server that duplicates the connectivity that should flow through
existing organs. The user corrected this directly (2026-07-07): "if this is
not a new organ or body part, it's a new process flow, then we need to add
this in as a process flow." The reward prediction error loop is NOT a new
organ. It is a flow: Bragg (task completion) then Schultz (RPE computation) then
Carlsson (action reinforcement) then Dale (neuromodulatory broadcast).

**When a function maps to a known neural PATHWAY, not a region, it is almost
always a process flow.** Examples: mesolimbic dopamine pathway (RPE),
corticospinal tract (motor output), HPA axis (stress cascade). These flow
THROUGH organs, they are not organs themselves.

## Pitfalls to Avoid
- ❌ Using generic names like "the specialist engine (Visual)" instead of scientist-specific names
- ❌ Omitting the scientist's full name and discovery details in documentation
- ❌ Forgetting to update BOTH code implementation AND documentation
- ❌ Using incorrect port numbers in diagrams/tables
- ❌ Missing the "Connection to [Project]" section that explains practical relevance
- ❌ Over-explaining; prioritize concise, actionable content over tutorial style
- ❌ Using narrative paragraphs when tables and bullet points would be clearer
- ❌ Not verifying that engines remain operational after documentation/code changes
- ❌ **Process-flow entries without scientist names** — every entry, including process-flow channels and PROC definitions, MUST have a named scientist (the discoverer of that biological system). "Neuromodulatory Flow" with no scientist is a quality failure. Assign Dale (cholinergic transmission), Kandel (LTP), Langley (ANS), etc.
- ❌ **body_part restating engine_name** — the body_part field must describe the actual anatomical structure, not copy the engine name. "Neuromodulatory Flow" → body_part should be "Brainstem Neuromodulator Nuclei (LC, VTA, Raphe, Basal Forebrain)", not "Neuromodulatory Flow".
- ❌ **Description equaling the name** — description must add information beyond restating the name. If description == engine_name, the entry fails.
- ❌ **Proposing ECS codes without querying the live registry** — the registry has 109+ engines and code assignments are non-sequential. Always query `agent-organism/ecs.py` or `ds-engine-registry/ecs.py` FLEET_REGISTRY for the target subsystem range BEFORE proposing a code. Session 2026-07-06: proposed 04.07.11 for the specialist engine but it was already taken by the specialist engine. The registry is the DNA; never assign codes from memory or by counting.
- ❌ **Assuming the specialist engine exists because it is listed in skill docs** — the specialist engine has been listed as PENDING in this skill's "Organs designed but NOT yet in ecs.py" section for multiple sessions. The skill docs said it was designed but never built. When a persistent output failure maps to a PENDING organ, that organ is the likely root cause. Build it; do not keep applying technical patches to the organs around the gap.

## Canonical Organ Inventory Sources

Always check BOTH of these when inventorying organs:
1. **`ds-engine-registry/ecs.py`** — The authoritative registry of all
   DEPLOYED engines (45 as of genome v2.1.0). This is the DNA.
2. **Architecture docs** (`docs/DS-VON-FRISCH-SIGNAL-ORGAN.md`,
   `docs/EXTERNAL-ENGINES-METAPHOR.md`, `docs/WOMB-ARCHITECTURE.md`) —
   Define organs that are DESIGNED but not yet in ecs.py.

### Organs designed but NOT yet in ecs.py (mark as PENDING in docs/charts)
- **the specialist engine** — Brief decomposition / phenotype application (Creative Subsystem)
- **the specialist engine** — Artifact refinement / editing (Creative Subsystem)
- **the specialist engine** — The Mirror / audience resonance checking (Creative Subsystem)
- **the specialist engine** — The organism's clothes/posture/presentation. Lives in the **Integumentary** system alongside the specialist engine (Skin). Marketing is NOT one organ; it is distributed across every [S]-tagged organ (the way posture reflects the health of all body systems).

### Process Flows designed but NOT yet registered (Session 2026-07-07)
- **the specialist engine** (reward prediction error flow, DS-ECS-NPR-13.01.07-v1.0.0, :port) — the mesolimbic dopamine prediction error loop. Flows THROUGH Bragg, Carlsson, Dale. Spec at `ds-wave-gamification-advisory-panel-private/PROCESS-FLOW-RPE-SCHULTZ-SPEC.md`. Gamification biological isomorphism. PENDING registration in ecs.py + build.

### Visual Processing & Generation organs (Session 2026-07-09, updated 2026-07-09)

The organism's visual hierarchy is partially built. the specialist engine declares the full
retina->LGN->V1->V2->V4->V5->IT pathway in its ECS differentiations but only
implements V4 (palette/phi/type-scale). the specialist engine is now BUILT and registered
but NOT yet wired into the production flow. The remaining gaps are bottom-up
perception and visual quality gating.

**BUILT and registered:**

- **the specialist engine** (DS-ECS-SUB-04.07.11-v1.0.0, :port) — Mental Imagery Engine.
  The "mind's eye." BUILT: engine.py + cognitive.py (ImageryWorkingMemory,
  ImageryContext, ComponentTemplate store) + adapters/grok_adapter.py (Grok
  image generation backend, model-agnostic GenerationContract) + server.py
  (FastAPI: /v1/imagine, /v1/rotate, /v1/buffer, /v1/contract-schema) + tests.
  Port 8154. NOT yet wired into the operator agent-production-spine.py (the spine has no
  image generation branch). Stephen Kosslyn proved visual imagery activates V1
  via top-down projections ("Image and Mind" 1980). The GenerationContract is
  the model-agnostic interface: swapping backends = swapping adapters.

**STILL MISSING (not in ecs.py):**

- **the specialist engine** (proposed) — V1 feature extraction + neuroaesthetics. Semir Zeki
  (b. 1940, UCL) named V4 and V5/MT, mapped functional specialization of visual
  cortex, founded neuroaesthetics ("Inner Vision: Art and the Brain" 1999).
  Would handle bottom-up visual perception: edge detection, orientation,
  spatial frequency, composition analysis, aesthetic judgment. Practical
  implementation: CLIP/vision-language model as computational V1+ventral
  stream. Proposed ECS: DS-ECS-SUB-04.07.12-v1.0.0, port :port.
- **Raster image quality gate** — re-entrant visual processing (Edelman). DS
  Luria reviews text and HTML, not pixels. Cannot assess composition, detect
  generation artifacts, verify prompt fidelity, or evaluate brand-color
  compliance in raster output. Could be a new engine or a visual mode of DS
  Luria (IT->V4->V2->V1 feedback loop).
- **Ventral stream object recognition** ("what" pathway) — namesake candidates:
  the specialist engine or the specialist engine (1982 dual-stream discovery). Given an image,
  identify objects/faces/logos/scenes. the specialist engine/Vision Input (:port) does OCR
  only, not object recognition.
- **Dorsal stream spatial analysis** ("where/how" pathway) — partially covered
  by the specialist engine (right parietal architecture) for spatial reasoning, but not for
  visual spatial processing of actual images (layout, depth, motion).

See organism-biological-isomorphism-verification skill
`references/occipital-lobe-functional-audit.md` for the full neuroscience
deep dive (7-stage hierarchy mapped to organism state, GWT integration,
4-gap analysis, build plan).

See `body-part-tackle-workflow` skill
`references/cranial-nerve-ii-optic-nerve-mapping.md` for the optic nerve
(CN II) as the operator agent's visual signal pathway for image generation. Maps 8 relay
stations from the specialist engine (retina/intake) through the specialist engine (motor output/render),
with physics equations (signal velocity, bandwidth, latency budget, SNR,
lateral inhibition), optic chiasm routing, 7 gaps blocking best-possible
output, and DS Ramón y Cajal diagnostic tests. Full document:
`~/your-workspace/ds-wave-gamification-advisory-panel-private/OPTIC-NERVE-IMAGE-GENERATION.md`.

### Language Production Pathway (BUILT 2026-07-06 — no longer pending)

the specialist engine was listed as PENDING for multiple sessions. The text garbling
problem (words merged, split, missing in output) was reframed as conduction
aphasia and traced to missing organs in the language pathway. All three
were built and wired into the production spine.

| Organ | Brain Region | Port | ECS Code | Status |
|-------|-------------|------|----------|--------|
| the specialist engine | Temporal lobe (BA 22) | :port | DS-ECS-SUB-04.07.06 | Pre-existing |
| the specialist engine | Parietal cortex (angular gyrus, BA 39) | :port | DS-ECS-SUB-04.07.16 | Built 2026-07-06 |
| the specialist engine | Inferior frontal gyrus (BA 44/45) | :port | DS-ECS-SUB-04.07.15 | Built 2026-07-06 |
| Arcuate tract | Arcuate fasciculus (white matter) | module | organism/arcuate_conduct.py | Built 2026-07-06 |

**Production spine pipeline (v3):** Goethe → Wernicke → Geschwind → Broca → Bell → Luria, with arcuate conduction between language stages.

**Lesson:** When a PENDING organ is the suspected root cause of a persistent failure, build it immediately rather than continuing to patch the organs around the gap. See `references/language-pathway-gap-analysis.md` for the full case study.

### The 11 biological organ systems (Gray's Anatomy, REV 8)

The user was explicit (2026-06-19): "these are not the correct organ
systems unless science has changed in recent years... the 11 systems are
intergumentary, skeletal, respiratory, digestive, cardiovascular, urinary,
endocrine, lymphatic, nervous, reproductive, muscular."

**Anatomical corrections applied in REV 8:**
- Sensory MERGED INTO Nervous (sensory receptors are nervous tissue)
- Musculoskeletal SPLIT into Skeletal + Muscular
- Excretory RENAMED to Urinary
- Immune RENAMED to Lymphatic
- Connective Tissue REMOVED (organs rehomed to Skeletal)
- Clinical/Diagnostic organs moved to external tools (not organ systems)
- Rings 2-3 are INTERNAL infrastructure, NOT external
- Von Frisch placed in Integumentary (clothes/posture/presentation)
- Marketing distributed across all [S]-tagged organs, not one organ

The 11 systems: Nervous (21 incl. sensory), Cardiovascular (2),
Respiratory (1), Digestive (1), Urinary (1), Endocrine (1),
Integumentary (2), Skeletal (2), Muscular (2), Lymphatic (5),
Reproductive (5) = 43 total organs + 0 pending (Broca BUILT, Von Frisch still pending).

For the complete inventory with ports, scientists, and faculty tags, see
`references/fleet-atlas-organ-inventory.md` in the `ds-fleet-atlas-update-via-davinci`
skill, or run `python3 ds-engine-registry/ecs.py` to dump the live registry.

### DNA / Genome classification

DNA medically falls under **Reproductive**, NOT its own organ system.
There is no "DNA system" in Gray's Anatomy — DNA is the genetic material
inside every cell, more fundamental than any organ system. The organs
that manage and pass it on (gonads, reproductive system) are reproductive.

The chart handles this with a two-tier approach (both are correct):
- **Layer 0 (top of chart, visual foundation):** "GENOME (the specialist engine
  :port)" shown as the foundational layer transcribed into every cell by
  the specialist engine. This communicates that DNA underlies everything.
- **Reproductive system (anatomical home):** the specialist engine is listed IN
  the Reproductive system alongside Waddington, Avrami, Turing, and
  Mangold — because that is the anatomical home for genetic management.

User confirmed this mapping on 2026-06-20: "should we classify dna under
its own category or does it medically fall under reproductive?" — answer:
Reproductive, with a Layer 0 visual treatment for emphasis.

**NEVER create new standalone HTML when updating the chart.** Always
modify and re-run `docs/generate_organ_chart.py`. The user was frustrated
when a new browser HTML was created instead of running the existing
generator. Canonical output: `docs/DS-Organ-System-Architecture.{html,pdf}`.
The user prefers the PDF output format — do not switch to browser-based
interactive views without explicit request.

### Faculty tags (5 emergent capabilities)
Every organ serves one or more emergent faculties (shown as tags on charts):
- **[C]** Creative (gold) — brain + eye + hand + heart + DNA
- **[D]** Diagnostic (teal-green) — immune + sensory + reasoning
- **[H]** Homeostatic (purple) — all body systems
- **[R]** Reproductive (pink) — reproductive + developmental
- **[S]** Signal (green) — sensory + nervous + integumentary (boundary)

## References
- See `references/organ-naming-examples.md` for detailed examples of properly formatted organ sections
- See `references/verification-checklist.md` for step-by-step verification procedures
- See `references/language-pathway-gap-analysis.md` for the worked example of symptom-to-anatomy diagnosis (conduction aphasia / text garbling case, session 2026-07-06)
- See `references/fiber-tract-atlas-methodology.md` for the proactive full-organism tract atlas method (conduction contract, 22-tract B2B worked example, build-priority pattern, root-cause organ-blocking analysis)
- See `references/reward-prediction-error-flow.md` for the gamification biological isomorphism (RPE process flow, session 2026-07-07)
- See `references/b2b-body-system-business-mapping.md` for the canonical B2B body-system → business-function mapping (6 systems, per-system engine/gap/document breakdown, "thin periphery" gap pattern, programmatic engine-extraction technique)
- See `templates/organ-section-template.md` for starter documentation format

### Organ vs Diagnostic Role (2026-07-10)

An organ IS the infrastructure. The diagnostician EXAMINES it. These are different roles requiring different engines. Same scientist principle, different function.

**User correction:** "The nervous system and the neuroscientist have two different objectives."

Example: DS Ramón y Cajal IS the nervous system infrastructure (`ds-nervous-system`). the specialist engine is the neurosurgeon who EXAMINES the nervous system. The organ does not examine itself. Before proposing a new engine, ask: am I building the organ or the doctor who examines it?

The organ belongs in the body system (nervous, cardiac, immune). The diagnostician lives in the diagnostic system alongside the specialist engine.

### Naming Conflict: Same Scientist, Two Functions (2026-07-10)

**User correction:** When two engines share the same scientist for different functions, one needs a different namesake.

the specialist engine (Alexander Graham Bell) is currently assigned to BOTH render/craft (the specialist engine :port) AND speech synthesis (the specialist engine). Same scientist, two functions. One must get a different namesake. This requires user decision to resolve.

**Before assigning a scientist to a new engine, check:**
```python
import re
text = open('/<workspace>').read()
for m in re.finditer(r'"(ds-[\w-]+)":\s*\{', text):
    name = m.group(1)
    block = text[m.end():m.end()+1000]
    sci = re.search(r'"scientist":\s*"([^"]+)"', block)
    if sci and 'bell' in sci.group(1).lower():  # or target scientist
        en = re.search(r'"engine_name":\s*"([^"]+)"', block)
        print(f'{name}: {en.group(1) if en else "?"} (scientist: {sci.group(1)})')
```

If the scientist is already assigned to a different function, either (a) find a different namesake for the new function, or (b) escalate to the user for resolution.

## Related Skills
- hermes-agent (for the operator agent-specific configuration and deployment)
- documentation (for general documentation standards)
- mlops/research (for scientific reference gathering)
- `ds-fleet-atlas-update-via-davinci` — Fleet Atlas PDF generation, including the organ-system architecture chart (page 3) and the complete organ inventory