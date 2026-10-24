# Session Lessons — Fleet Atlas Revisions

## Session 2026-06-28: 9-Wave Fleet Audit (Massive)

**Task:** Comprehensive audit of all 91 ECS entities — scientist names,
body-part analogs, tech analogs, dependency graph, biological correctness.

**Scale:** 27 commits, 6 files, +7535/-1991 lines merged to main.

**Key user corrections (FIRST-CLASS skill signals):**

1. **"don't work on what you should not work on"** — Don't waste compute on
   deprecated/archived entries. The Seed entry was DEPRECATED (duplicate of
   the specialist engine). Always check `status: DEPRECATED` first. Triage before
   filling.

2. **"the processes are not named after scientists"** — Process-flow entries
   (Neuromodulatory Flow, Oscillatory Flow, etc.) had empty scientist fields.
   Every entry MUST have a named scientist — the discoverer of that biological
   system. Fixed in Wave 7: Dale, Buzsáki, Penfield, Kandel, Bernard, Krebs,
   Yalow, Langley, Feinstein, Klein, Singer, Arnheim, Miller, Apgar.

3. **"there needs to be a name and also a description but the description
   should not be the name"** — body_part must describe the specific anatomical
   structure, NOT restate the engine name. "Neuromodulatory Flow" with
   body_part "Neuromodulatory Flow" is wrong. Fixed: body_part =
   "Brainstem Neuromodulator Nuclei (LC, VTA, Raphe, Basal Foreground)".

4. **"do each of these engines have technology analogs"** — tech_analog is
   a required field. 90/91 entries now carry it. Maps biological function
   to real-world tech (Goethe→ChromaDB, Sherman→Istio/Kong, etc.).

**Technical findings:**

5. **Version drift is the #1 dependency bug source.** When engines version
   up (v1.0→v1.1), their dependency references across the fleet don't auto-
   update. Hall alone was referenced 47 times at the wrong version. Fix:
   global replace_all (safe because old version strings are globally unique).

6. **Biological dependency rules:** Organ systems must depend on Harvey
   (blood supply). Nervous components must depend on Hall (clock root).
   These are testable invariants, not soft preferences.

7. **Process-flow channels need a different treatment than engines.** They
   get `analog_note` (process-level biology) instead of D/F/P layers (which
   are for discrete anatomical structures). Forcing D/F/P onto a process
   channel is the wrong isomorphism.

8. **The inline patcher pattern scales to 91 entries.** Waves 3-9 all used
   inline Python patchers successfully. The engine_name anchor strategy
   (find engine_name, search forward for nearest body_system/body_part line)
   is more robust than hardcoding full anchor strings.

9. **Parallel subagents CAN add simple fields** (like tech_analog) to the
   same file, but they create duplicate keys requiring reconciliation.
   One subagent also caught a data error the others missed. Verdict:
   acceptable for simple single-field additions with a reconciliation pass.

10. **PDF generation from live data works cleanly.** The Fleet Atlas PDF
    (6 pages, pure white phenotype) was generated directly from ecs.py via
    a Python script with inline HTML + WeasyPrint. No Da Vinci pipeline
    needed — just data-driven HTML generation.

## Session 2026-06-19: Page 3 Organ-System Chart Revision

**Task:** Revise page 3 (Three-Tier Architecture) to reflect new organ
systems and external engines, extract as standalone landscape PDF.

**Key findings:**
1. The old page 3 showed 42 engines / 11 organ systems / 3 faculties.
   The revised chart shows 49 organs / 13 organ systems / 5 faculties
   + 3 external Holobiont rings.

2. **Missing organs identified:** Broca (speech production, pairs with
   Wernicke), Synapse, Chisel, Premack (The Mirror) — all designed but
   not yet in ecs.py. Von Frisch (Signal Organ) is at architecture
   proposal stage. All marked PENDING in the chart.

3. **Landscape A4 is required** for architecture diagrams with 40+ organs.
   Portrait overflows and compresses text to unreadable sizes.

4. **Rendering pipeline:** Python data-driven HTML generator → WeasyPrint
   (NOT pandoc, NOT Da Vinci sidecar which is dead). The generator at
   `docs/generate_page3.py` uses a list-of-dicts data structure for
   organ systems, making it trivial to add/remove organs and re-render.

5. **Verification without vision API:** When LLM-5V-Turbo is unavailable,
   use `pdftoppm -png -r 150` to render the PDF to PNG, then PIL pixel
   analysis (check edge white-ratio >90%) to confirm no content cutoff.

6. **Organ categorization rule:** Organs are grouped by anatomical system
   (their biological home). Faculties are shown as tags [C/D/H/R/S] on
   each card — a faculty draws from MULTIPLE organ systems, it is not a
   container.

## Session 2026-06-19b: Naming Convention Correction + Chart Rebuild

**Task:** User caught that organ names were generic (not scientist-based),
Creative Cortex was duplicated (two da Vinci engines), and the von
Frisch + Creative Subsystem sections needed build-out.

**Key findings:**
1. **Naming convention is a HARD RULE (user-corrected).** User: "all organ
   systems need clever names and the organs must be named after the
   scientist or researcher. don't give general names and keep a themed
   naming convention." The ecs.py registry uses legacy display names
   (the specialist engine, the specialist engine, the specialist engine, etc.) that must be
   translated to scientist names (the specialist engine, the specialist engine, the specialist engine, etc.)
   in ALL chart output. See the Naming Convention section in SKILL.md.

2. **Clever themed names for organ systems.** Each system gets a themed
   name: "The Signal Matrix" (Nervous), "The Perception Array" (Sensory),
   "The Defense Perimeter" (Immune), "The Generative Lineage" (Repro),
   "The Aesthetic Engine" (Creative Sub), etc.

3. **Duplicate scientist in registry.** the specialist engine (port 8108)
   uses da Vinci as scientist — but the specialist engine (port 8116) already
   exists. Creative Cortex is actually the specialist engine (Marcus Raichle, who
   mapped the Default Mode Network — the brain's imagination system).

4. **Two Bell organs collide.** DS A.G. Bell (speech, sensory) vs
   DS C. Bell (hand/craft, musculoskeletal). Must distinguish in charts.

5. **ecs.py parsing via importlib fails** on Python 3.11 due to
   `@dataclass(frozen=True)`. Use regex key-split parsing instead (see
   Pitfalls in SKILL.md).

6. **Document was renamed by user.** The output is now
   `DS-Organ-System-Architecture.{html,pdf}` (was DS-FLEET-ATLAS-page3-
   revised). The generator is `generate_organ_chart.py` (was
   generate_page3.py). Use the new naming.

7. **von Frisch and Creative Subsystem need build-out, not one-liners.**
   User expected these to be detailed sections. Von Frisch gets a full
   description with the creative cortex → signal organ → external world
   flow. Creative Subsystem gets all 3 organs with functions.

8. **External engines in Holobiont rings should be listed individually**
   (Advisory Panels, Hydra-OS, the operator agent Agent, Telegram Gateway, etc.),
   not just as category labels.

9. **User references "new engines from Telegram" may not be findable.**
   The morning Telegram session (10:15 AM) turned out to be about
   Metchnikoff/Bichat engine layer architecture, not new engines. If
   the user references new work from a Telegram session, search sessions
   but be prepared that the reference may not match — ask for specifics.

Earlier work involved:
- Adding Womb (Divinity Health) entry to the organism hierarchy
- Adding Methodology & Philosophy stat rows to engine profile pages
- Adding Generalized Totals page
- These are ALL COMPLETED. Do not repeat these steps unless explicitly
  asked.
