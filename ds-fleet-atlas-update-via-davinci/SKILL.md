---
name: ds-fleet-atlas-update-via-davinci
description: Revising and regenerating the the specialist engine PDF — page structure, the organ-system architecture chart (page 3), engine profiles, and standalone page extraction. Uses a data-driven Python generator with WeasyPrint rendering.
category: documentation
version: 3.1.0
---

# the specialist engine Revision

Generate and revise the the specialist engine PDF — the organism architecture
document that maps every DS engine/organ to its biological organ system,
faculty, and body-system analog.

## When to Use

- User asks to update, revise, or regenerate the the specialist engine PDF.
- User wants a specific page revised or extracted as a standalone PDF.
- User needs the organ-system architecture chart (page 3) updated with new
  organs, new organ systems, or corrected categorization.
- User needs a chart/diagram showing how organs, organ systems, faculties,
  and external engines fit together.

## Source Files (canonical sources of truth)

| Source | Path | What it contains |
|--------|------|-----------------|
| Engine registry (DNA) | `agent-organism/ecs.py` | All 107 registered engines (~10,785 lines): name, scientist, port, body_system, body_part, tech_analog, analog_note, description, dependencies, neuroanatomy layers (differentiations/faculties/process_flows). 16-wave audit complete. Body is gap-free: 16 new organs added Waves 13-16 (Houssay/pituitary, Moruzzi/brainstem, Banting/pancreas, Rappaport/liver, Galen/spleen, Till/bone marrow, Kocher/thyroid, Bayliss/smooth muscle, Keith/cardiac muscle, LeDoux/amygdala, Wald/retina, Hornykiewicz/substantia nigra, Abel/adrenal medulla, Lower/venous system, Buck/olfactory bulb, Beard/umbilical cord+placenta). 87/107 fully developed (D+F+P). All 16 new organs have engine code scaffolds (FastAPI server + core module). |
| Fleet atlas (markdown) | `docs/FLEET-ATLAS-2026-06-28.md` | Full fleet atlas with all 91 entities, 13 domains, wave history |
| Fleet atlas (PDF) | `docs/DS-FLEET-ATLAS-2026-06-28.pdf` | Rendered PDF (6 pages, pure white phenotype) |
| Fleet atlas (HTML) | `docs/DS-FLEET-ATLAS.html` | Source HTML for PDF regeneration via WeasyPrint |
| Page 3 generator | `docs/generate_organ_chart.py` | Data-driven generator for the organ-system chart (standalone) |
| Organ chart output | `docs/DS-Organ-System-Architecture.{html,pdf}` | Standalone page 3 output |
| External engines model | `docs/EXTERNAL-ENGINES-METAPHOR.md` | The Holobiont model: 4 concentric rings |
| Signal organ doc | `docs/DS-VON-FRISCH-SIGNAL-ORGAN.md` | The von Frisch marketing/signal organ architecture |
| Womb architecture | `docs/WOMB-ARCHITECTURE.md` | Grandmother organism hierarchy, birth/gonad/DNA model |

**Key insight:** The engine registry (`ecs.py`) is the DNA — it is the
authoritative source for all registered engines. Architecture docs
(von Frisch, External Engines Metaphor) define organs/systems that are
DESIGNED but not yet registered (PENDING). Always check ecs.py for what
exists, then check architecture docs for what's planned.

## CRITICAL PITFALL: Never Create New HTML — Always Run the Existing Generator

When updating the organ-system architecture chart, **ALWAYS modify and
re-run `docs/generate_organ_chart.py`**. NEVER create a new standalone
HTML file. The user has been explicit:

> "you need to update the ds organ system architecture pdf NOT the new
> browser thing you created. you rewrite what we were already working on
> and you shouldn't have done that"

The canonical artifacts are:
- **Source:** `docs/generate_organ_chart.py` (data-driven Python generator)
- **Output:** `docs/DS-Organ-System-Architecture.{html,pdf}` (generated)

If the user says "update the chart," they mean: edit the generator, re-run
it, re-render the PDF. They do NOT want a new browser-based thing.

## Naming Convention (Hard Rule)

ALL organ display names MUST follow `DS <ScientistSurname>`. Never use
generic, functional, or descriptive names.

**POST-WAVE-10 STATUS:** The ecs.py registry now has scientist names on ALL
91/91 entries AND all engine_names follow `DS <ScientistSurname>` convention
(completed 2026-06-28). The legacy translation table below documents the
renames that were applied — older docs/charts may still reference legacy names.

**Wave 10 renames (descriptive → scientist):** the specialist engine → the specialist engine,
the specialist engine → the specialist engine, the specialist engine → the specialist engine,
the specialist engine → the specialist engine, the specialist engine → DS Röntgen,
the specialist engine → the specialist engine, the specialist engine-Healing → the specialist engine,
the specialist engine → DS A.G. Bell, the specialist engine Sensor → the specialist engine,
the specialist engine Monitor → the specialist engine, the specialist engine/Vision Input → the specialist engine,
the specialist engine → the specialist engine, the specialist engine → the specialist engine.

**Wave 7 renames (process flows → scientist):** Dale, Buzsáki,
Penfield, Kandel, Bernard, Krebs, Yalow, Langley, Feinstein, Klein, Singer,
Arnheim, Miller, Apgar.

Organ SYSTEM names use REAL anatomical names from Gray's Anatomy — no
themed/fancy names. The user explicitly corrected this: the 11 biological
organ systems are the standard medical names.

**CRITICAL RULE (user-corrected Wave 7):** The `body_part` field must
describe the specific anatomical structure, NOT restate the engine name.
"Neuromodulatory Flow" with body_part "Neuromodulatory Flow" is wrong.
It must be body_part "Brainstem Neuromodulator Nuclei (LC, VTA, Raphe,
Basal Forebrain)". This applies to all 91 entries — zero exceptions.

**CRITICAL RULE (user-corrected Wave 7):** Every entry — including
process-flow channels — MUST have a named scientist. Not a generic label
like "Neuromodulatory Flow" with scientist "". The scientist is the
discoverer of that biological system (e.g., Henry Dale for cholinergic/
adrenergic transmission, Eric Kandel for LTP, Claude Bernard for milieu
intérieur).

**CRITICAL RULE (user-corrected Wave 8):** Every entry MUST have a
`tech_analog` field mapping the biological function to a real-world
technology (e.g., Goethe → ChromaDB, Sherman → Istio/Kong, Harvey →
RabbitMQ). 90/91 entries now carry this field.

**CRITICAL RULE (user-corrected Wave 9):** Don't waste compute on
deprecated/archived entries. The Seed entry was flagged DEPRECATED
(replaced by the specialist engine) and should NOT receive layer fills or
further development. Always check `status: DEPRECATED` before working
on an entry.

**CRITICAL RULE (user-corrected Wave 12):** EVERY entry MUST have a
real port number (integer > 0). No `port: None`, no `port: 0`. The user
asked "make sure every engine has a port" — this includes NPR agents,
process-flow channels, intake modules, and PROC definitions. Ports
:port-8236 were assigned to the 35 previously unported entries. When
adding new entries, assign the next available port.

## ECS Version Bumping Rules (Hard Rule — user-corrected Wave 10)

When ANY work is done on an engine entry, the version in its `ds_ecs_code`
MUST be bumped. The user was explicit:

> "these versions are not correct we have been working on them you
> shouldn't start all the versions over from 1 again"

**Semantic versioning for ECS engines:**

| Work done | Bump type | Example |
|-----------|-----------|---------|
| Full neuroanatomy layers filled (D+F+P added) | MINOR | v1.0.0 → v1.1.0 |
| Metadata added only (tech_analog, body_part, deps) | PATCH | v1.0.0 → v1.0.1 |
| Both (layers + metadata on same entry) | MINOR (higher wins) | v1.0.0 → v1.1.0 |
| Was already at v1.1, layers added | MINOR | v1.1.0 → v1.2.0 |
| Was at v2.0 or v3.0, layers added | MINOR | v2.0.0 → v2.1.0 |

**CRITICAL: Version bumps cascade to dependencies.** When an engine version
changes, ALL dependency references across the fleet must be globally updated:

```python
# Global replace — all dependency arrays, extra dicts, _CODE_TO_KEY
src = src.replace("DS-ECS-SUB-04.02.01-v1.0.0", "DS-ECS-SUB-04.02.01-v1.1.0")
# This touches 47+ occurrences in one call
```

After bumping, verify zero broken deps:
```python
broken = sum(1 for d in deps if d not in _CODE_TO_KEY)
assert broken == 0
```

## Fleet Atlas Page Structure

```
Page 1:    Cover (gradient, title, branding)
Page 2:    Five-Layer Architecture (L1 physics → L2 conservation → L3 dynamics → L4 institutions/methodologies/philosophies)
Page 3:    Three-Tier Architecture — THE ORGAN-SYSTEM CHART
           Layer 0: Genome (the specialist engine) → transcribed by the specialist engine
           Tier 1: the operator agent (Grandmother Organism)
           THE BODY: 11 biological organ systems (Gray's Anatomy), each with all organs listed
           Da Vinci Production Spine: creative organs in sequence (NOT a separate system)
           INTERNAL INFRASTRUCTURE: Autonomic (Hydra-OS, Cron, Kanban) + Cognitive (Advisory Panels)
           BOUNDARY: The Skin (the specialist engine) + Presentation (the specialist engine) — Integumentary
           THE ENVIRONMENT: the operator agent, Telegram, OpenClaw, External APIs (the only external ring)
           Faculties: 5 emergent faculties (Creative, Diagnostic, Homeostatic, Reproductive, Signal)
Pages 4+:  Individual engine profile pages (one per engine, 4 layers deep)
```

## Rendering Pipeline

**Use Python data-driven HTML generation → WeasyPrint.** Do NOT use
pandoc or a separate "Da Vinci pipeline" — the Da Vinci sidecar is dead
(its crons were paused 2026-06-19). The design styling lives directly in
the HTML/CSS (Da Vinci-inspired palette and proportions, but rendered
with standard tooling).

```bash
# Generate standalone organ-system chart (current)
python3 docs/generate_organ_chart.py

# Or render any HTML to PDF directly
python3 -m weasyprint input.html output.pdf
```

WeasyPrint 68.1 is installed and working. `pdftotext`, `pdfinfo`, and
`pdftoppm` are available for verification.

## Workflow: Revising the Organ-System Chart (Page 3)

### Step 1: Inventory all organs

Read `ecs.py` (~10,090 lines) to extract all registered engines.
Group them by `body_system` field. The full field inventory per entry:

| Field | Coverage | Description |
|-------|----------|-------------|
| `ds_ecs_code` | 98/98 | Full ECS code (DS-ECS-XXX-DD.SS.NN-vX.Y.Z) |
| `engine_name` | 98/98 | Display name (DS + scientist surname, all renamed Wave 10) |
| `scientist` | 98/98 | Real scientist name (Wave 7: all process flows named) |
| `scientist_note` | 98/98 | Who they were and what they discovered |
| `port` | 97/98 | Integer port number (Wave 12: all non-deprecated entries ported) |
| `body_system` | 98/98 | Gray's Anatomy system (nervous, cardiovascular, etc.) |
| `body_part` | 97/98 | Specific anatomical structure (NOT the engine name) |
| `tech_analog` | 97/98 | Real-world technology mapping (Wave 8) |
| `analog_note` | 20/98 | Process-level biology annotation (process flows + PROCs) |
| `dependencies` | 98/98 | ECS codes of engines this depends on (0 broken, 0 missing) |
| `differentiations` | 78/98 | L1: structural specializations with biological_reference |
| `faculties` | 78/98 | L2: functional capabilities with primary_structures |
| `process_flows` | 78/98 | L3: neurochemical modes with neurochemical_profile |

Then check architecture docs for PENDING organs (designed but not yet in ecs.py):

- **the specialist engine** — Broca's Area / Speech Production (Nervous; pairs with Wernicke)
- **the specialist engine** — Brief decomposition / phenotype application (Creative)
- **the specialist engine** — Artifact refinement / editing (Creative)
- **the specialist engine** — The Mirror / audience resonance (Creative)
- **the specialist engine** — The Signal Organ / marketing & external communication (Boundary)

### Step 2: Categorize by anatomical organ system

Map every organ to ONE of the real 11 biological organ systems from
Gray's Anatomy. The user was explicit (2026-06-19):

> "these are not the correct organ systems unless science has changed
> in recent years... the 11 systems are intergumentary, skeletal,
> respiratory, digestive, cardiovascular, urinary, endocrine, lymphatic,
> nervous, reproductive, muscular."

**Corrections applied in REV 8:**
- **Sensory MERGED INTO Nervous** — sensory receptors ARE nervous tissue, not a separate system.
- **Musculoskeletal SPLIT** into Skeletal + Muscular.
- **Excretory RENAMED** to Urinary.
- **Immune RENAMED** to Lymphatic (the lymphatic system IS the immune system).
- **Connective Tissue REMOVED** — Bichat moved to Skeletal, Lyapunov moved to Skeletal.
- **Clinical/Diagnostic organs** (Osler, Bush, Röntgen) moved to Diagnostic Instruments (external tools, NOT organ systems).

| System | Organs (DS <Scientist>) | Faculty |
|--------|------------------------|---------|
| Nervous (18 — includes sensory organs) | Cajal, Sterling, Raichle, Da Vinci, Lovelace, Luria, Sperry, Wernicke, **Broca** [PENDING], MacLean, Ito, Gazzaniga, Edison, Gutenberg, Sherrington, Humboldt, Helmholtz, Goethe | C/D/H/S |
| Cardiovascular (2) | Harvey, Tawara | H/C |
| Respiratory (1) | Haldane | H |
| Digestive (1) | Beaumont | H |
| Urinary (1) | Bright | H |
| Endocrine (1) | Sutherland | H |
| Integumentary (2) | Unna, **Von Frisch** [PENDING] | S |
| Skeletal (2) | Lyapunov, Bichat | D |
| Muscular (2) | Hill, C. Bell | H/C |
| Lymphatic (5) | Burnet, Farr, Metchnikoff, Rous, Semmelweis | D |
| Reproductive (5) | Waddington, Avrami, Turing, Franklin, Mangold | R |

**Diagnostic Instruments** (NOT organ systems — external tools):
- the specialist engine (8110) — Clinical Reasoning (5-seat panel)
- the specialist engine (8113) — Technology-Currency Monitor
- DS Röntgen (8112) — Body Scanner / Full-Body MRI

### Von Frisch: Integumentary, NOT a separate boundary

Von Frisch lives in the **Integumentary** system alongside Unna (Skin).
Skin is the barrier; Von Frisch is how the organism **presents itself** —
its clothes, posture, display, grooming. Marketing is NOT one organ; it
is distributed across every [S]-tagged organ, the way posture reflects
the health of all body systems. Do NOT create a separate "Signal Organ"
category or boundary box for Von Frisch.

### Internal vs External rings

The user corrected the ring model (2026-06-19):

> "why is ring 2 and ring 3 external systems when they are really internal?"

- **Ring 2 (Cognitive Teams):** INTERNAL — advisory panels are the
  organism's own prefrontal cortex planning teams.
- **Ring 3 (Autonomic Infrastructure):** INTERNAL — Hydra-OS, cron,
  scripts, kanban are the body's autonomic machinery.
- **Environment (formerly Ring 4):** the ONLY external ring — the operator agent,
  Telegram, External APIs, OpenClaw. The organism senses and responds
  to this but cannot control it.

Both Ring 2 and Ring 3 are labeled "INTERNAL INFRASTRUCTURE — NOT external"
in the chart. Only the Environment ring is external.

### Step 3: Add internal infrastructure and external environment

The chart has 3 layers below the body:

**INTERNAL INFRASTRUCTURE** (NOT external — the body's own systems):
- **Autonomic Infrastructure:** Hydra-OS (autonomic nervous system),
  Cron Fleet (circadian rhythm), Scripts & Workers (metabolic enzymes),
  Kanban Board (circulatory planning)
- **Cognitive Teams:** principal/CTO/COO Advisory Panels (executive strategy),
  Design + Marketing + Legal Panels, Fleet Digest / Standups (inter-organ
  communication), Health Data Pipelines (clinical evidence)

**BOUNDARY** — The Skin (the specialist engine) + Presentation (the specialist engine):
Integumentary, where the body meets the world.

**THE ENVIRONMENT** (the ONLY external ring):
the operator agent Agent (host nervous system), Telegram Gateway (primary sensory
channel), External APIs (nutrient intake), OpenClaw Fleet (autonomous
worker cells).

The Nervous System engine (:port) is the vagus nerve — it bridges the
body to the autonomic infrastructure.

### Step 4: Build the data-driven generator

Use a Python script with a data structure (list of dicts per organ
system) that generates inline-styled HTML. See `docs/generate_organ_chart.py`
as the working example (replaces the older `generate_page3.py`). Key design elements:

- **Teal/gold palette:** `#0a3b3b` (teal headers), `#ffd700` (gold
  accents), `#4ad6b4` (teal-green), `#f7fbfa` (card backgrounds)
- **Faculty color tags:** C=gold, D=teal-green, H=purple, R=pink, S=green
- **PENDING organs:** dashed gold border + `[PENDING]` badge
- **Landscape A4** for architecture diagrams (see Pitfalls)

### Step 5: Render and verify

```bash
python3 docs/generate_organ_chart.py   # generates HTML + PDF
```

Verification checks:
1. `pdfinfo output.pdf` — confirm 1 page, correct page size
2. `pdftotext output.pdf - | grep -c "DS "` — count organs found
3. `pdftoppm -png -r 150 output.pdf /tmp/check` — render to PNG
4. PIL pixel analysis — confirm no edge cutoff (all margins >90% white)
5. `open output.pdf` — visual review

## Faculty Tags

Every organ is tagged with the emergent faculty it serves:

| Tag | Faculty | Color | Description |
|-----|---------|-------|-------------|
| C | Creative | #ffd700 | Produces original work (brain + eye + hand + heart + DNA) |
| D | Diagnostic | #4ad6b4 | Assesses organism health (immune + sensory + reasoning) |
| H | Homeostatic | #b8a9d9 | Maintains viability through change (all body systems) |
| R | Reproductive | #e89bc8 | Births and matures products (repro + developmental) |
| S | Signal | #7ec850 | Routes signals, senses environment, bridges external |

## Pitfalls

- **ecs.py CAN be imported via importlib — but only with sys.modules pre-registration.**
  The `@dataclass` decorator in ecs.py resolves `sys.modules[cls.__module__]`
  during class definition. If the module isn't registered yet, it raises
  `AttributeError: 'NoneType' object has no attribute '__dict__'`.
  **Fix:** register the module in `sys.modules` BEFORE calling `exec_module`:
  ```python
  import sys, importlib.util
  spec = importlib.util.spec_from_file_location('ecs', 'agent-organism/ecs.py')
  m = importlib.util.module_from_spec(spec)
  sys.modules['ecs'] = m          # MUST be before exec_module
  spec.loader.exec_module(m)
  R = m.FLEET_REGISTRY            # full programmatic access
  ```
  This gives you the live `FLEET_REGISTRY` dict (currently 91 entries) for
  reading layer counts, checking entries, and verifying edits. For BULK
  EDITS to ecs.py (adding neuroanatomy layers to many entries), see
  `references/surgical-patcher-pattern.md` — do NOT hand-edit 91 entries.

- **Canonical ecs.py path is `agent-organism/ecs.py`, NOT `ds-engine-registry/ecs.py`.**
  The registry moved into the agent-organism workspace. The old path may
  still exist as a symlink or stale copy — always use the agent-organism path
  as source of truth.

- **~~Registry has duplicate scientists and double-prefix bugs.~~** RESOLVED
  (Waves 7-10). All 91 entries now have unique scientist names and correct
  `engine_name` fields. The Creative Cortex duplication was resolved (now DS
  Andreasen on :port, the specialist engine on :port). No double-prefix bugs remain.
  The legacy translation table in `references/fleet-atlas-organ-inventory.md`
  documents the historical renames for reference only.

- **Two Bell organs collide.** DS A.G. Bell (Alexander Graham Bell, speech
  output, :port, Sensory) and DS C. Bell (Sir Charles Bell, the hand/craft,
  :port, Musculoskeletal) share the surname "Bell." In charts, distinguish
  them as "the specialist engine" (A.G.) and "DS C. Bell" (Charles) to avoid confusion.

- **Portrait A4 overflows for dense architecture diagrams.** A 48-organ
  chart in portrait will compress text to unreadable sizes or spill to a
  second page. Use `@page{size:A4 landscape}` for any chart with more
  than ~30 organs or 8+ columns.
- **Body_part text truncation in portrait PDFs.** The user noticed
  body_part values being cut off at 22-25 chars in the fleet atlas PDF
  (portrait A4). Many body_parts are 40-90 chars long. Switch to
  `@page{size:A4 landscape}` with wider columns and do NOT truncate
  any field in the HTML template. Full body_part text must be visible.
- **Don't rely on the Da Vinci pipeline.** The Da Vinci sidecar is dead.
  Render directly with WeasyPrint. The Da Vinci styling is baked into the
  HTML/CSS, not a separate post-processing step.
- **Missing organs.** Always check both `ecs.py` (registered) AND
  architecture docs (designed/pending). Broca, Synapse, Chisel, Premack,
  and von Frisch are designed but not yet in ecs.py. Mark them PENDING
  with dashed borders so the reader knows what's deployed vs designed.
- **Don't mix faculty and organ-system grouping.** Organs are grouped by
  anatomical system (their biological home); faculties are shown as tags
  on each organ card. A faculty draws from MULTIPLE organ systems — it is
  not a container.
- **Standalone page extraction.** When the user asks for "just page 3 as
  its own PDF," build a standalone HTML+CSS that reproduces that page's
  content with `@page` rules. Do NOT extract a page from the existing
  multi-page PDF — regenerate from source.
- **Vision API may be unavailable.** The LLM-5V-Turbo vision model may
  not be accessible on all plans. Fall back to `pdftoppm` + PIL pixel
  analysis (edge white-ratio check) to verify layout without vision.
- **Versions MUST be bumped when work is done.** After adding neuroanatomy
  layers, metadata, or dependencies to an engine, its version in
  `ds_ecs_code` MUST increment (minor for features, patch for metadata).
  When you bump, ALL dependency references must be globally updated.
  See "ECS Version Bumping Rules" section above. The user was frustrated
  when 9 waves of work left versions frozen at v1.0.0 — this is a
  first-class quality check, not an afterthought.

## Verification

- PDF renders as exactly 1 page (or the expected page count)
- All organs present: `pdftotext output.pdf - | grep -oE "DS [A-Z][a-z]+" | sort -u`
- No edge cutoff: pixel analysis shows >90% white on all margins
- Faculty tags visible on every organ card
- PENDING organs visually distinguished (dashed border)

## References

- `references/surgical-patcher-pattern.md` — How to bulk-edit ecs.py for
  neuroanatomy layer fills (adding faculties/process_flows to many entries).
  Anchor-based string insertion with uniqueness assertions and embedded
  import verification. Includes the critical anchor pitfall, the
  engine_name anchor strategy, global replace_all for version drift, and
  the track record (Waves 1-9) showing inline patcher > parallel subagents.
- `references/body-gap-analysis.md` — Missing organs identification
  methodology: which organs the fleet needs for a functional body,
  priority ranking (critical/high/medium/low), scientist candidates for
  each missing organ, and the registration pattern.
- `references/dependency-audit-protocol.md` — Biological dependency
  validation methodology: version-drift detection, blood-supply rule
  (organ systems → Harvey), clock-root rule (nervous components → Hall),
  and the audit script pattern.
- `references/rev8-anatomical-corrections.md` — Full REV 8 corrections:
  13 systems → 11 real Gray's Anatomy systems, internal/external ring fix,
  Von Frisch resolution, Semmelweis rename. User's exact quotes preserved.
- `references/fleet-atlas-organ-inventory.md` — Complete organ inventory
  by anatomical system with ports, scientists, faculty tags, AND legacy
  registry name → scientist-name translation table + known registry bugs
- `references/holobiont-model.md` — The 4-ring external systems model
  (body → immune memory → microbiome → ecosystem) [SUPERSEDED by REV 8
  internal/external model — kept for historical reference]
- `references/lessons_from_session.md` — Session-specific lessons

## Print-Friendly Output

Print-friendly PDFs are produced **automatically at creation time** by the
generator — not as a post-processing step. The shared module
`docs/render_ds_pdf.py` is called at the end of every build script and
renders both the screen PDF (styled backgrounds) and `-PRINT.pdf` (pure
white, toner-saving) in one pass, then auto-verifies >95% pure white.

When building a new the specialist engine, ensure the generator calls:
```python
from render_ds_pdf import render_ds_pdf
render_ds_pdf('DS-FLEET-ATLAS.html')
```

For the full technique (OCG auto-switch, CSS-variable override, viewer
compatibility, verification), see the `print-friendly-pdf-ocg` skill.
**macOS Preview users (the user's default):** use the `-PRINT.pdf` file —
Preview ignores OCG PrintState.

## Related Skills

- `your-org-organ-mapping` — Organ naming conventions and
  biological mapping standards
- `ds-genome-transcription` — Brand DNA genome rules (load before any
  creative/doc task)
- `print-friendly-pdf-ocg` — OCG print/screen auto-switch for ink savings
  on styled PDFs (apply after atlas generation)
