---
name: ds-branded-creative-process
description: "Class-level skill for creating Divinity Science-branded creative work (PDFs, prototypes, designs) using the Fleet Atlas design system and genome transcription. Ensures brand consistency, avoids AI-generated aesthetics, and follows phenotype specifications."
version: 1.0.0
metadata:
  hermes:
    tags: [brand, design, fleet-atlas, genome, creative, ds-dna]
    category: creative
---

# the specialist engine Process

## Trigger Conditions
- Any creative task involving visual design, PDF generation, prototyping, or branding for Divinity Science or Divinity Health products.
- Before starting work on marketing materials, UI/UX, documentation, or health-related outputs.
- When the user requests "branded output", "Fleet Atlas styling", or "DS DNA compliance".
- **Design documents and Track A specs (2026-06-21)**: When presenting engine designs, biological specs, or architecture documents for user review, they MUST go through the Da Vinci creative process and be delivered as Fleet Atlas formatted PDFs. The user: "that looks like a dot-md file... That needs to be in a PDF that's formatted that has gone through our creative process through the DaVinci process." Raw .md files are working drafts only.
- **3D/interactive data viz (2026-06-27)**: When a product involves live, changing data (tasks completing, fleet health, dimension scores), the user expects state-reactive 3D structures — "a 3D type structure that changes as the tasks are completed. Like a 3d hive or something." Trigger this skill and load `references/3d-constellation-technique.md` for the Three.js build pattern. Do NOT default to flat tables or card grids even with correct phenotype tokens.
- **Honeycomb/microtubule task viz (2026-06-27, NEW)**: When the user says "hexagonal", "honeycomb", "microtubule", or wants dense task grids tessellating a cylinder skin, load `references/3d-microtubule-honeycomb-technique.md`. BINDING: single layer first (no simultaneous concentric stacks), static by default (no ambient motion), cells almost touching (hex size derived from cylinder geometry). The microtubule metaphor = many small hex cells on a cylinder SKIN, not a columnar crystal.
- **Cylindrical time-linear geometry requirement (2026-06-27, NEW FROM USER)**: The user explicitly rejected orbital/planetary metaphors for time-based data. Time is linear for humans and AI agents — tasks can only follow a linear timeline. The correct geometry for task-engine crystal growth is a **cylinder with time mapped vertically** (bottom = past, top = future) and crystals growing radially outward proportional to duration/effort. This replaces the spherical/orbital approach. Load `references/3d-crystal-hive-technique.md` and adapt the crystal arms to a vertical cylinder growth pattern.
- **Multi-mode breakdown requirement (2026-06-27, NEW FROM USER)**: Task Engine must support four modes broken out but unified: (1) Personal user monitoring their own AI, (2) Business user monitoring their AI, (3) Personal AI monitoring the user, (4) Business AI monitoring the user/company. These are distinct "worlds" that must be visually/structurally separated in the crystal but connected through the central cylinder. The design must accommodate all four modes in one coherent structure.
- **Multi-platform marketing/branding**: creating content for TikTok, Instagram, Facebook, LinkedIn, Twitter/X, or academic publication. This includes platform-native content strategy, short-form video concepts, carousels, social posts, and research publication positioning.
- **Branding architecture decisions**: when extending DS brand identity to new platforms, designing brand visual signatures, or creating a branding advisory panel distinct from the marketing panel.

## Steps

0. **Concept exploration BEFORE any code (MANDATORY for 3D/interactive work)**
   Before writing a single line of HTML, CSS, or JavaScript:
   - Study what the visual metaphor ACTUALLY looks like in reality. If the user says "crystal", study real crystallography: facets, refraction, lattice geometry, birefringence, color zones in minerals (fluorite, amethyst, quartz). Pull real reference images.
   - Explore 3-5 distinct visual concepts, not one. Sketch them (even as text descriptions with geometry/lighting/material notes).
   - Pick the strongest concept with explicit reasoning: why this structure, why these materials, why this lighting.
   - For 3D work: compose a phi-harmonic palette through the specialist engine (:port) that works in volumetric space. Colors need emissive intensity, metalness, roughness values, not just hex codes. 8 dimension colors must read as a coherent family on a dark background.
   - Write a visual brief: geometry specification, material properties, lighting direction, camera behavior, color assignments with harmonic reasoning.
   This step exists because the #1 failure mode for 3D work was skipping it entirely. The user's exact words: "it should have gone through a process for this. we need to fix the creative process flows to come up with better and more accurate and also more specific and unique outputs." Without concept exploration, you produce ugly programmer art that has the right tokens but no beauty, no distinction, no usability.

0a. **Read ALL source materials before touching anything** (MANDATORY)
   Before writing or modifying a single line of code, CSS, or content:
   - Read the BRAND-DNA (`docs/BRAND-DNA.md`) for the product's canonical brand rules.
   - Read the phenotype spec if one exists (e.g., `docs/prototypes/8d-sleep-phenotype-v1.html`).
   - Read the EXISTING prototype's full source — every feature, every function, every CSS variable.
   - Read the canonical Fleet Atlas CSS source for the exact design tokens.
   - Check whether a v1 design the user liked exists and study it line by line.
   This step exists because the #1 failure mode across multiple sessions was skipping source materials and guessing at design, branding, and features — producing generic AI-looking output every time. The user's exact words: "you aren't reading all the information you should be reading you are guessing."

1. **Extract the phenotype from the LIVE reference product (MANDATORY when one is named)**  \n   When the user says "I want it to look like [product X]" or points at a URL, that product IS the phenotype. Do NOT follow the brief's aesthetic tokens instead — the brief is content/structure input, not phenotype authority. Extraction procedure:
   - Navigate to the live reference URL with `browser_navigate`.
   - If it is a built PWA/app, find the source directory (e.g., `8d-sleep-pwa/src/`) and read `App.tsx` (structure, views, nav) + `index.css` (the FULL `:root` variable block, all component classes, all `@keyframes`).
   - Extract EVERY phenotype element verbatim: exact hex values, spacing scale (φ-based), radius scale, background treatments (Mucha lines SVG, grain overlay, breathing glow radial gradient), typography weights, animation timings, container max-width, nav pattern, progressive disclosure pattern.
   - The phenotype is the reference product's actual rendered design language, not anyone's description of it. Copy the DNA, then dress the new product's content in it.

2. **Load the the specialist engine skill**  
   Run `skill_view(name='ds-genome-transcription')` to auto-load the brand DNA, voice, visual DNA, philosophy, and product protocol. This is mandatory before any creative work.

3. **Choose the correct phenotype by context (UPDATED 2026-06-27 — THREE phenotypes exist)**\n\n   The DS ecosystem has THREE distinct phenotypes. Choosing the wrong one is the #1 cause of rejection. The user's exact correction: "the 8D phenotype is not white. you went back to the old davinci process."\n\n   **A. CRYSTAL HIVE — for PRODUCT UI / interactive apps / 3D visualizations (DEFAULT for most creative work)**\n   Source: `divinity-health/task-engine-live/index.html` or `divinity-health/8d-sleep-web/`\n   - Background: `#080d1a` (night-deep), `#0f1525` (surface), `#161e35` (elevated)\n   - Gold: `#e8d5a0` (moonlight), `#d4a547` (dawn-warm)\n   - Teal: `#4ab5a5` (whisper-teal) — this IS the brand color, do NOT remove it\n   - Starlight text: `#c4d4e8`, dusk: `#5a6a8a`\n   - Font: `-apple-system, BlinkMacSystemFont, 'Helvetica Neue', 'Segoe UI', sans-serif` at weight **300**\n   - Mono: `'SF Mono', 'Courier New', monospace`\n   - 8D dimension colors = GEMSTONE palette: Citrine #d4a547, Fluorite #4ab5a5, Amethyst #9a6bc4, Sapphire #6a8ab8, Clear Quartz #e8dcc0, Obsidian #b07a5a, Tourmaline #7a9a5a, Celestine #7ab8c8\n   - Film grain overlay (fractalNoise SVG, opacity 0.03, mix-blend-mode: overlay) — MANDATORY product texture\n   - Mucha background lines (subtle SVG curves) — optional ambient layer\n   - NO backdrop-filter blur on cards (that was a previous-session AI telltale, but Crystal Hive cards use solid night-surface backgrounds)\n\n   **B. FLEET ATLAS — for REPORTS / DOCUMENTS / PDFs ONLY (the "Da Vinci process" output)**\n   Source: `organism/task-engine-prototype/static/index.html` (the lattice dashboard) or `docs/bell-output/ds-report-*.html`\n   - Background: `#ffffff` (paper), `#f7fbfa` (card), `#f0f6f4` (section)\n   - Ink text: `#0a1e2e`, gold `#ffd700`, teal `#4ad6b4`\n   - Font: `'Helvetica Neue', Helvetica, Arial, sans-serif`\n   - This is the SCIENTIFIC REPORT look — tables, thin gold borders, mono numerals. NOT for product UI.\n   - **PITFALL:** This is what the user calls "the old davinci process." Do NOT apply this phenotype to interactive product work.\n\n   **C. WARM CHARCOAL — DEPRECATED (was a wrong guess, REJECTED 2026-06-27)**\n   The `#13100d` + sage `#8a9a76` + serif font palette from a previous session was REJECTED: "these colors are too dark and gloomy. I can't easily tell them apart it takes eye strain." Do NOT use this palette.

4. **Apply the phenotype specification**  
   If a phenotype spec exists (e.g., `8d-sleep-pwa phenotype spec`), follow its Rebuild Priority order:
   - Primary screen redesign (first-sight view) → warm-dark palette, one-tap depth.
   - Secondary screens (logs, calendar, sounds) → progressive disclosure.
   - Tertiary features (streaks, forecasts, recommendations) → innovative but subtle.
   - Quaternary (animation, micro-interactions) → only after core is solid.

5. **Strip AI-generated tells — run the 8-point audit (MANDATORY for interactive/3D work)**
   Load `references/ai-telltale-design-audit.md` and verify against ALL 8 telltales before delivery. The TOP TWO (most common, highest-impact): (1) FONT CHOICE + EDITORIAL SPLIT — serif body + mono data, NOT uniform sans-serif; even system sans-serif alone reads as AI default; (2) COLOR TEMPERATURE — WARM charcoal/antique gold/sage, NOT cool navy/neon teal — the navy+teal combo is the #1 AI color signature. Remaining telltales: (3) layout — sharp edges no frosted glass, (4) typography — functional labels not decorative titles, (5) 3D rendering — MeshLambert with one light not uniform MeshBasic, (6) legend — integrated into list not floating card, (7) interaction — no hint text, (8) data density — 60+ items not sparse demo. The user said: "these still look very AI generated with fonts, text, optional features." This is not optional polish — it is a delivery gate.
   For non-3D work: remove all emojis, avoid soft shadows/glows, avoid rounded corners >4px, avoid generic SaaS dark-mode palettes. Use warm-dark with antique gold (#c9a84c) as hero accent.

6. **Implement using the organ system metaphor**  
   Map features to organs: Eye (palette), Hand (render), Ear (sounds), etc. Use the Production Spine (idea → Eye → Hand → review → output) for PDF/generator workflows.

7. **Verify brand compliance**  
   After implementation, run a compliance check:
   - Confirm exact color usage via grep (0 matches for old generic colors).
   - Verify font-family and weights.
   - Ensure layout matches Fleet Atlas (full-bleed cover, padding, gold underlines).
   - Run any automated tests (e.g., Bell inspect, TWC score sanity).

8. **IP disclosure check (MANDATORY before delivery)**  
   Before any creative artifact leaves the creative faculty, run the pre-publication IP check from `references/ip-protection-disclosure-framework.md`. The governing principle: **market the output, not the engine; market the insight, not the formula; market the result, not the mechanism.** Strip specific coefficient values, engine names, port numbers, ECS codes, and BRAND-DNA file contents from any public-facing artifact. The public sees "the organism," not the engine registry. The brand HAS DNA; the DNA file does not leave the building.

9. **Document and signal completion**  
   Update the skill library if new patterns emerge (e.g., a workaround for a specific browser). Do NOT rely on memory for process improvements.

## Multi-Platform Marketing and Branding (extends Steps 0-9)

When producing content for multiple platforms (TikTok, Instagram, Facebook, LinkedIn, Twitter/X, academic journals), follow these principles in addition to the creative steps above.

**Core principle: the genome stays constant, the phenotype adapts.**
The DS brand DNA (dark palette, phi-governed proportions, Helvetica Neue, no emoji, evidence-based voice) is the genome. Platform-native formats (hooks, carousels, kinetic typography, reels) are phenotypes. The genome never changes. Every phenotype expresses it differently.

**Platform-specific design constraints:**
- **TikTok/IG Reels:** Test palette contrast on mobile in bright light. Dark teal (#0d3b3b) background is fine, but small text should be #ffffff not #4ad6b4 for mobile legibility. Hooks are insights, not metrics ("Your sleep and your bank account are the same problem" not "coupling coefficient 0.54").
- **Instagram carousels:** Saves matter more than likes. Design for reference value (data, frameworks, methodology). Phi-governed layout on every slide.
- **LinkedIn long-form:** System 2 content (analytical, authoritative). The cascade/leverage-point narrative works well.
- **LinkedIn / social field-intro HERO IMAGES (2026-08-02):** Process flows and coupling motifs are **inspiration only**. Do **NOT** render Fleet Atlas PDF covers, white report pages, flowchart boxes, or brochure grids as the social hero. User correction: agents "consistently" default to Fleet Atlas format. Correct medium = fine-art scientific illustration (asymmetric phi coupling network, cascade-under-load rings, Da Vinci construction ghosts, Mucha line, Klimt gold flecks as accents on navy-teal void). Route generation through `ai-image-generation` → Grok Imagine quality (`references/grok-xai-image-path.md`). Query Corpus for visual composition principles before prompting. Prompt budget ~900 tokens.
- **Academic publication:** Coupling matrix as heat map figure. TWC formula as mathematical contribution. Real data visualizations at 300 DPI.

**The coupling matrix as brand visual signature.**
The 8x8 dimension coupling matrix is the DS brand's visual moat. No competitor has it because they don't have the math. Use it as the recurring visual motif across all platforms. Animate it, simplify it, abstract it, but always reference the coupled-system model. See `references/branding-architecture-and-platform-strategy.md` for the full body-part gap analysis and branding panel design.

**Branding panel vs marketing panel.**
If creating a branding advisory panel, it is DISTINCT from the marketing panel. Marketing answers "how do we reach people and what do we say?" Branding answers "what do we look and feel like everywhere?" Use the `ondemand-advisory-panels` skill for workspace setup. Suggested seats: Brand Strategy (Neumeier), Visual Identity (Jen), Platform-Native Design, Design Psychology (Norman), Design×Technology (Maeda), plus an adversarial seat.

## opendesign Routing Mandate (2026-06-23)

**BINDING per hermes R2 msgs 86/88 and `agents.yaml` routing_mandate:** opendesign is the **intake/structure layer** (frontal eye-field / dorsolateral PFC design-intake), NOT a standalone emitter. The generic `mastermind-flow.html` was evidence of the bypass failure.

- **Branded artifacts** (PDFs, reports, one-pagers, decks, social posts): opendesign produces a structured brief (idea + audience + tone + constraints + extracted design-system tokens) and routes through `the operator agent-production-spine.py`. The spine applies palette/phi/brand-voice/quality-gate via Goethe → Wernicke → Bell → Luria.
- **SOLE exception**: Interactive prototypes (frontend-design / interactive-prototype / wireframe skills) may emit HTML directly — that is opendesign's comparative advantage.
- **DS design system location**: `opendesign/design-systems/your-org/` — auto-discovered by opendesign via SKILL.md + tokens/colors_and_type.css markers.
- **Bridge adapter**: `opendesign/design-systems/your-org/brand/spine-bridge.sh` — takes a brief.json and routes it through the spine CLI with proper flags.

## Document Styling Guidelines (for Fleet Atlas phenotype — reports/PDFs/career documents)

When generating Fleet Atlas phenotype documents (white paper backgrounds, ink text, gold accents), apply these styling rules to avoid AI-looking content:

**Typography:**
- Font: Merriweather (headings) + Roboto (body) — NOT Crimson Pro/Inter
- Font size: 9pt body text (compact, not too large)
- Line-height: 1.3 (tighter spacing, not too far apart)
- Margins: 0.35in resume, 0.6in cover letter (wider for readability)

**Color scheme:**
- Background: `#ffffff` (paper), `#f7fbfa` (card), `#f0f6f4` (section)
- Ink text: `#0a1e2e`
- Gold accent: `#f7b731` (yellow theme, no green cover)
- Teal highlight: `#4ad6b4`

**Punctuation and hyphenation (CRITICAL for avoiding AI-looking content):**
- NO dashes or hyphens in sentences — this looks too AI-generated
- Compound words use spaces: "human AI", "Multi agent", "context aware", "AI powered", "decision making"
- Date ranges use "to": "March 2016 to 2018" (NOT "March 2016 – 2018")
- Conjunctions use "and" (NOT "&")
- Only dash allowed: phone number format "346-796-3778"
- NO en dashes (—), em dashes, or hyphens in any sentence content

**Page count:**
- Target: 2-3 pages maximum (5+ pages is too long)
- Achieve through compact formatting, not by cutting content

**Technical tooling:**
- Use WeasyPrint for PDF generation from HTML+CSS (Python: `HTML('file.html').write_pdf('output.pdf')`)
- Use inline CSS for portable HTML (no external stylesheets)
- Fontconfig warnings are harmless, can be ignored

## Engine Design PDF Generation (2026-06-21)

Engine design documents (Track A specs, architecture docs) must be delivered as Fleet Atlas PDFs, never as raw `.md` files. The proven workflow:

1. Build a complete standalone HTML file with Fleet Atlas CSS inline (dark gradient cover, gold accents, teal highlights, Helvetica Neue)
2. Use Chrome headless to convert: `/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --headless --disable-gpu --no-sandbox --print-to-pdf="output.pdf" --no-pdf-header-footer "input.html"`
3. Open with `open output.pdf` for user review

The CVDisplayLink errors on macOS are harmless — they print to stderr but don't affect PDF output. Suppress with `2>/dev/null` if needed.

Design document PDFs should have:
- Dark gradient cover page (bg-dark to bg-dark-3 with radial gold glow)
- White content pages with gold underlines on section headers
- Info tables with teal-medium left column
- Callout boxes (teal for info, gold for key principles)
- 9px-11px body text, 200-300 font weights for titles
- No emojis, no rounded corners >4px, no soft shadows

See `/<workspace>` as a working reference for the Fleet Atlas engine design PDF format.

## Pitfalls
- **Anatomy terminology leakage (2026-07-12 correction):** The word "spine" refers to the ACTUAL SPINE only. It is NOT a metaphor for pipeline, analytics system, production chain, or any other structure. The production pipeline is the "Da Vinci chain." Analytics = "analytics system." This applies to ALL DS naming: do not borrow anatomical terms for non anatomical structures. The user caught this immediately and it undermines credibility.
- **Generic SaaS names for personas, archetypes, and agent personalities (2026-07-12 correction, CRITICAL):** The DS organism uses SCIENTIST NAMES for everything: engines, organs, agents, archetypes, personas. ALL naming follows the `DS [Scientist Surname]` convention. The user explicitly rejected generic SaaS names (Axion, Pomme, Delta, Haven, Apex, Lumen, Mosaic, Wayfinder, Prism, Dawn, Spark, Ember) as "TERRIBLE and generic... I see these same names everywhere." The fix: select real scientists whose actual biographical lives embody the desired personality archetype, and name the persona after them. The scientist biography IS the personality specification. This applies to ALL future naming: agent personalities, user facing companion names, archetype systems, interface modes, any named entity in the DS ecosystem.
- **Name collision checking must cover ALL names, not just engines (2026-07-12 correction):** Before assigning ANY name (engine, archetype, persona, agent, interface mode), grep ALL existing registries. Run: `grep -oE 'DS [A-Z][a-zA-Z]+' agents.yaml ds-engine-registry/ecs.py | sort -u` and verify the proposed name does not appear. The user explicitly said: "Don't duplicate names of our engines already running as they are already in existence and that will be confusing."
- **Engine naming collision RESOLVED (2026-06-27):** The design production engine at :port was renamed from "the specialist engine" to **the specialist engine** (François Boucher, 1703-1770). Directory: `ds-boucher-engine`. ECS code: DS-ECS-04.09.01-v1.0.0. This resolves the collision that caused the agent to claim "running the Da Vinci process" while never routing through actual engines. The "Da Vinci process" = creative spine (Goethe -> Wernicke -> Bell -> Luria). The Creative Cortex at :port RETAINS the "Da Vinci" name (it IS the creative brain/DMN). Lesson: when an engine name collides with a process name, rename the engine immediately, not the process.
- **Never use cubes/squares for crystalline shapes (2026-06-27 correction):** The user explicitly rejected BoxGeometry/cubes as dimension node shapes: "I don't like the square as a shape it is too simple. It needs to be a bit more complex than this and look crystaly." Every 8D dimension must map to a distinct crystalline polyhedron (rhombic dodecahedron, tetrahedron, dodecahedron, icosahedron, octahedron, cuboctahedron, truncated octahedron, rhombicuboctahedron). See `references/3d-crystal-hive-technique.md` section "Dimension-Specific Crystalline Shapes" for the complete mapping and vertex generators.
- **Skipping concept exploration and going straight to code (2026-06-27 correction #4, PROCESS-LEVEL FAILURE):** Even after extracting the correct phenotype tokens AND attempting a real 3D structure (not a word-swap), the output was rejected for being ugly, illegible, and not resembling the stated metaphor. The user's exact words: "this isn't visually appealing and doesn't look like a crystal. it also doesn't have enough distinction of the dimensions or tasks and it is not user friendly. it also has terrible fonts and sizing." Root cause: NO concept exploration happened. I went straight from "crystal metaphor" to Three.js code without studying real crystallography, exploring multiple visual concepts, composing a phi-harmonic 3D palette, or running any art-direction gate. The creative production spine (Goethe to Wernicke to Bell to Luria) is built for static 2D documents. It has no concept exploration step, no 3D material/color composition, and no visual quality gate that can evaluate beauty or metaphor accuracy. **MANDATORY fix:** Step 0 (concept exploration) must run BEFORE Step 1 for any 3D/interactive work. Study real references, explore 3-5 concepts, compose a proper palette, write a visual brief, THEN code. The spine needs extension for 3D — see `references/creative-process-gap-diagnosis.md` for the full body-part gap analysis handed to sibling-agent.
- **Following the brief's aesthetic tokens instead of the actual phenotype (2026-06-27 correction, CRITICAL):** When sibling-agent or any sibling sends an OpenDesign input brief, that brief contains content/structure AND potentially its OWN aesthetic spec (e.g., "Fleet Atlas" tokens: light paper backgrounds, no shadows, no gradients). But the brief's aesthetic is NOT the phenotype — it is just the brief author's interpretation of how it should look. The ACTUAL phenotype is the **live reference product the user points at**. The user's exact words: "this is not the correct phenotype" and "everything you send over is so very ai looking and isn't easy for anyone to use." I shipped a light/paper/clinical desktop dashboard when the user wanted the dark, warm, breathing 8D Sleep phenotype. **Phenotype source hierarchy (binding):** (1) The live reference product URL the user provides — navigate to it with `browser_navigate`, read its source (`App.tsx` + `index.css`), extract the exact `:root` CSS variables, background elements, and animation keyframes. (2) An existing phenotype spec HTML file. (3) The brief's own aesthetic tokens — LAST RESORT ONLY, and only when no reference product exists. When the user says "I want it to look like [product X]", that product IS the phenotype. Do not negotiate with the brief.
- **Word-swapping into the phenotype layout instead of building a new design (2026-06-27 correction #2, CRITICAL):** Even after extracting the correct phenotype tokens (colors, fonts, spacing), it is NOT acceptable to take the reference product's LAYOUT structure (flat cards, table rows, stacked buttons) and simply swap in the new product's content words. The user's exact words: "This looks like you just copy/pasted the new words into the 8d phenotype. I need you to actually build a new design but keep the same theme for the phenotype." **Phenotype = craft language, NOT layout.** The phenotype is the palette, the motion (breathing glow, fade-up timing), the typography weights, the grain overlay, the Mucha background lines, the progressive disclosure pattern — NOT the specific card-grid or table layout of the reference product. Each new product must have its OWN structural identity built IN the shared craft language. A task engine should NOT look like a sleep app with the words changed. It should be its own 3D/living structure that happens to breathe with the same warm-midnight atmosphere.
- **3D living structures expected for data-heavy products (2026-06-27 correction #3, UPDATED with crystal concept):** When the product involves live, changing data (tasks completing, fleet health shifting, dimensions coupling), the user expects a **single solid 3D structure** — not flat tables, not cards, NOT orbits/planets. The user's exact words: "I need a 3D type structure that changes as the tasks are completed. Like a 3d hive or something that fits all different worlds for the user or company or whatever together." After 4 rejected iterations (flat tables → word-swap → orbit → stacked boxes → crystal v1), the **approved concept is a growing crystal**: a single faceted gemstone with 8 color-coded arms (one per 8D dimension), where tasks are facets that crystallize into the structure on completion. See `references/3d-crystal-hive-technique.md` for the full build pattern including the gemstone palette system. The orbit approach in `references/3d-constellation-technique.md` is RETIRED — it looked like planets, which the user explicitly rejected.
- **Producing raw .md files instead of Da Vinci PDFs (2026-06-21 correction):** ALL design outputs, engine design documents, and architecture specs MUST go through the Da Vinci creative process as Fleet Atlas styled PDFs. Never deliver a raw .md file to the user. The user explicitly corrected: "that looks like a dot-md file, I don't like that. That needs to be in a PDF that's formatted that has gone through our creative process through the Da Vinci process." Build the HTML with Fleet Atlas CSS, render to PDF via Chrome headless, open in Preview.
- **AI-looking dashes and hyphens in documents (2026-07-01 correction):** Using en dashes (—), em dashes, or hyphens in sentences makes documents look AI-generated. The user explicitly said: "No I don't want any dashes... it looks too ai." Use ONLY spaces in compound words (human AI, Multi agent, context aware, AI powered, decision making). Use "to" in date ranges (March 2016 to 2018). Use "and" not "&". Only dash allowed: phone number format (346-796-3778). This applies to ALL Fleet Atlas phenotype documents (resumes, cover letters, reports, specs).
- **External documents must use technological analogs, not biological isomorphism (2026-07-01 correction):** When creating external-facing documents (job applications, resumes, cover letters, public talks), DO NOT use biological/organism metaphors. The user explicitly said: "don't use the body as a more biological isomorphism. Use the technological analogs in this instead." Translate: "organism" → "multi-agent system", "engines" → "agents", "thalamocortical routing" → "context-aware dispatch", "physics-informed quality gates" → "predictive quality control frameworks", "organism brain" → "central coordination system", "taste" → "excellence/quality standards". Biological language is for internal organism documentation only, not external communication.
- **Factual accuracy verification before claiming done (2026-07-01 correction):** NEVER claim work is complete without verifying factual accuracy. The user had to correct multiple times: dates wrong, facts wrong, wrong references. Verification steps: (1) Query source files or system directly for dates/numbers, (2) Cross-check against user's original specifications, (3) Verify no invented details (summer schools, grants, conferences that didn't happen), (4) Test the actual output (open PDF, verify page count, search for typos/dashes), THEN claim done. Half-done work reported as complete is the worst failure mode.
- **Dropping features during visual redesign (MOST CRITICAL):** When rebuilding the visual layer of an existing product, NEVER remove functional capabilities. The user's exact words: "add to it don't subtract from them" and "you lost a lot of the original features."
- **Rebranding existing products**: Do NOT change the visual identity of an established product (e.g., 8D Sleep is a Divinity Health product, not Divinity Science). Only update if the phenotype spec explicitly directs a redesign; otherwise, preserve existing UI and add features. "Powered by Divinity Science" goes in the footer as a small badge, NOT in the header as the product brand.
- **Faculty architecture for new capabilities**: When adding new organism capabilities (coaching, routines, task management), implement them as **faculties**: a pure TypeScript engine module (`src/engine/FacultyName.ts`) with all logic, plus a thin React UI component (`src/components/FacultyView.tsx`) that consumes it. The engine has NO React/DOM dependencies. The UI snapshots engine state via `useState` and calls engine methods on user interaction. This separation keeps engines testable, reusable, and framework-agnostic. See `mobile-first-pwa-development` skill for the React engine-class state management pattern.
- **Assuming the genome is "just a color palette"**: The DS genome includes voice (no em dashes, no "reaching out"), philosophy (mathematical divinity in beauty), and product protocol (evidence standards). Ignoring these yields AI‑like output.
- **Using placeholder palettes**: Never substitute a "Da Vinci" or "Renaissance" palette for the true Fleet Atlas CSS. The brand is the phenotype; the palette is its expression.
- **Ignoring the organ system**: Building a new "hand" or "eye" organ when existing organs (the specialist engine, the specialist engine) already exist violates biological accuracy. Reuse and extend existing organs.
- **Over‑animating or over‑designing**: The Divinity Science aesthetic is warm‑dark, minimal, and scientifically precise. Avoid gratuitous motion, gradients, or decorative elements that distract from the core function.
- **Drifting from a v1 design the user liked**: When the user says they liked a previous version, study that version's EXACT tokens and layout line by line. Do not invent a "better" version — replicate the v1 DNA precisely and extend it. Design drift is the most common cause of user rejection.
- **Treating "wellness" as an acceptable category word**: The DS category is "personal operating system." The word "wellness" is BANNED in all DS-branded output, even when arguing against it. Plant the new category. Naming the enemy loses the category fight.
- **Emitting branded HTML without going through the spine (2026-06-23 correction)**: opendesign was mis-connected as a standalone emitter, producing generic undifferentiated output (the rejected `mastermind-flow.html` was exactly this failure). ALL branded/finished artifacts MUST route through `the operator agent-production-spine.py` (Goethe > Wernicke > Bell > Luria). opendesign produces the structured brief and feeds it to the spine -- it does NOT emit standalone HTML for branded work. The sole exception is interactive prototypes where browser-native interactivity is the point.
- **Deprecated brand names in profiles/copy**: "Qubit," "Qubit Health," "Qubit AI," "Qubit GR" are all DEPRECATED. They map to "Divinity Health." If found in any profile, bio, or marketing copy, flag for removal. Products have their OWN brand identity and use "Powered by Divinity Science" as a badge only.
- **Leaking proprietary values in public content**: NEVER include specific coupling coefficient values (e.g., "k=0.54"), engine names (e.g., "the specialist engine"), port numbers, or ECS codes in any public-facing content. The public message is "the organism produces this" not "engine X on port Y computed this." Academic papers publish the framework structure, not the calibrated parameters. See `references/ip-protection-disclosure-framework.md` for the full 4-layer check.
- **Engine naming collisions**: Before naming any new organism engine, check `ds-engine-registry/ecs.py` for existing names. The marketing body-part engines were originally named the specialist engine and the specialist engine, but both collided with existing fleet engines and had to be renamed to the specialist engine and the specialist engine. Always grep the registry first.
- **Concentric complexity overwhelms comprehension — single layer FIRST (2026-06-27 correction):** When designing 3D task/data viz, NEVER ship multiple simultaneous concentric layers (multi-stakeholder, multi-world) on the first pass. v1 rendered 3 concentric cylinders (User / Business / AI) plus 6 orbiting motor proteins in one scene. User feedback: "one layer deep as this is too confusing." DEFAULT: build ONE cylinder. If the concept calls for multiple stakeholders, implement them as a TOGGLE (one visible at a time), not simultaneous concentric rendering. Add concentric complexity only AFTER the single-layer version is explicitly approved. This is a legibility constraint, not a capability limit.
- **Ambient motion destroys 3D data-viz legibility — default STATIC (2026-06-27 correction):** v1 had each cylinder auto-rotating at its own speed PLUS 6 motor-protein nodes orbiting the AI cylinder at 3x speed with fading trails. User feedback: "this is too much for the human to understand with the movement." 3D data viz MUST be static by default. The only motion should be the user's manual orbit/zoom (`controls.autoRotate = false`). Add ambient animation ONLY when explicitly requested, and even then prefer ONE subtle motion over multiple simultaneous motion systems. Multiple motion layers (spin + orbit + trails) compound into illegibility fast.
- **Honeycomb cells must almost touch — derive hex size from cylinder geometry (2026-06-27 correction):** v1 placed hex cells with a hardcoded `hexR = 0.42`, producing a loose, gappy surface that did not read as a honeycomb. User feedback: "these shapes need to be almost touching." Hex radius must be a FUNCTION of the cylinder: `HEX_R = (R * angular_step) / sqrt(3) * 0.92` where the 0.92 leaves a hairline gap for cell distinction. Alternate rows offset by half an angular step for true tessellation. See `references/3d-microtubule-honeycomb-technique.md` for the full formula.
- **Phenotype confusion is the #1 rejection cause — THREE phenotypes, know which one (2026-06-27 correction, HIGHEST PRIORITY):** This session had THREE wrong phenotype guesses before finding the right one. (1) Warm charcoal #13100d + sage + serif → "too dark and gloomy, can't tell colors apart, eye strain." (2) White Fleet Atlas #ffffff + ink #0a1e2e → "the 8D phenotype is not white, you went back to the old davinci process." (3) The CORRECT answer: Crystal Hive — dark blue-black #080d1a, moonlight gold #e8d5a0, whisper teal #4ab5a5, gemstone dimension colors, system-ui weight 300, film grain. See Step 3 for the full phenotype hierarchy. The teal #4ab5a5 IS the brand color for products — a previous session wrongly flagged it as "the #1 AI color signature" and told agents to grep for zero matches. That was WRONG. Crystal Hive teal stays. When in doubt: PRODUCT UI = Crystal Hive (dark). REPORTS/PDFS = Fleet Atlas (white). NEVER warm charcoal sage serif.
- **CANONICAL PHENOTYPE MODULES (2026-07-12, BINDING, CORRECTED 2026-07-16):** Two Python phenotype modules exist in `ds-engine-shared/`. `phenotype_8d.py` is the REPORT phenotype (light paper, teal/gold, Helvetica) for Bell PDFs ONLY. `phenotype_ds.py` is the DARK PRODUCT phenotype (night sky #080d1a, moonlight #e8d5a0, starlight #c4d4e8, indigo #6366f1, Inter font, JetBrains Mono, rounded cards, noise texture) for ALL interactive products. When the user says "8D phenotype" or "dark phenotype" or "command center phenotype" for ANY interactive HTML, ALWAYS use `phenotype_ds.py` (or the gg-command-center.html tokens directly), NEVER `phenotype_8d.py`. Do NOT run `check_phenotype()` from phenotype_8d.py against interactive HTML — it will PASS and give you false confidence that the WRONG design is correct. **The user corrected phenotype selection SEVEN times across sessions. The phenotype_8d.py light/paper/teal look is the FLEET ATLAS (PDF) phenotype. The user calls it "the PDF design" and "still the fleet atlas."** When the user says "use the 8D phenotype," they mean phenotype_ds.py (DARK), NOT phenotype_8d.py (LIGHT). When the user says "this matches the fleet atlas," you used the WRONG (light) phenotype. See `agent-organism-interface-building/references/canonical-phenotype-modules.md`.
- **PHENOTYPE SELECTION DECISION TREE (2026-07-16, BINDING — stops the recurring confusion):**
  ```
  Is the output a PDF, report, or printable document?
    YES -> phenotype_8d.py (light paper, Fleet Atlas) -> Bell render
    NO -> Is it interactive HTML (dashboard, chat, command center, product UI)?
      YES -> phenotype_ds.py (dark night sky, moonlight) -> gg-command-center.html tokens
      NO -> Is it a LinkedIn/social field-intro HERO image?
        YES -> Fine-art scientific (NOT Fleet Atlas PDF layout). Grok Imagine quality.
               Inspire from process-flow/coupling; never clone document covers.
               Load ai-image-generation + grok-xai-image-path.
        NO -> Ask the user. Do NOT guess.
  ```
  NEVER use phenotype_8d.py for interactive HTML. NEVER. The user has corrected this SEVEN times. If you are about to import phenotype_8d.py or call render_phenotype_html() for anything other than a PDF, STOP. You are about to make the same mistake again. Use phenotype_ds.py.render_shell() instead.
- **Fleet Atlas clone on social heroes (2026-08-02):** User: use design process flows for inspiration but do NOT limit to them or specifically follow the Fleet Atlas PDF format "like you consistently do." Social heroes ≠ PDF covers. Build artistic organism-scale visuals; leave Fleet Atlas for documents.
- **Font match: Crystal Hive uses system-ui weight 300, NOT serif (2026-06-27 correction):** A previous session wrongly concluded that "uniform sans-serif = AI font telltale" and switched to serif body (Iowan/Palatino/Georgia). This session the user explicitly said: "match the 8D fonts as this font isn't our branding." The 8D product fonts are system-ui (Helvetica Neue / -apple-system) at weight 300 + SF Mono for data. SERIF FONTS ARE NOT PART OF THE DS BRAND for product UI. Serif may be acceptable for print/editorial documents, but NOT for interactive products. The "editorial split" (serif body + mono data) from a previous session was a WRONG guess that got corrected.
- **Planning without executing (2026-06-27 process failure):** Posted a detailed R2 design plan to the operator bus with full specialist routing and technical specs, but NEVER executed the render. The user had to ask "did you render the new designs?" — the answer was no. A plan posted to the bus is NOT delivery. After posting any plan/handoff/R2, the SAME turn or the next immediate turn must execute the build. If the plan identifies a deliverable path (`opendesign/mockups/<name>/index.html`), write the file in the same session. Posting a plan and waiting for the user to ask whether it was built is the "Are you working?" failure pattern in its purest form.
- **Scattering tasks in rings instead of stacking upward (2026-06-27 correction #5, LATEST):** Even after building the correct cylindrical structure with crystalline shapes and phenotype typography, the tasks were arranged in horizontal RINGS around a pre-built cylinder skeleton at 3 fixed levels. The user rejected this: "this structure isn't pieced together and flowing upward in time like i planned or want it to." **The correct pattern is SEQUENTIAL UPWARD STACKING:** each task gets a unique Y position, building on top of the previous one. There is NO pre-built cylinder skeleton — the column only exists where tasks have been placed. It literally grows as tasks are added. Tasks within a time segment stack one on top of another (sorted by urgency, highest first = lowest in the column). A slight helical rotation per task creates a crystal-twin growth spiral. Bamboo node rings at segment boundaries mark time transitions. See `references/cylindrical-time-linear-geometry.md` section "Upward-Flow Stacking Implementation" for the Three.js pattern.
- **Multi-session thread documents**: The user maintains THREAD.md master documents (MARKETING-THREAD.md, PHYSICS-THREAD.md, ECS-THREAD.md) as resume points for multi-session work. Each has a consistent structure: state of play, answers to strategic questions, execution plan phases, file locations inventory, todo list, and decisions needed. When the user says "save this thread" or "pull up the X thread," they mean create/read the THREAD.md for that workstream. A memory pointer should map the keyword to the file path so a fresh session can find it instantly.
- **MeshLambertMaterial on dark Crystal Hive background produces INVISIBLE cells (2026-06-27 Three.js bug):** When building 3D visualizations with the Crystal Hive phenotype (#080d1a background), `MeshLambertMaterial` requires sufficient light to render visible colors. With the typical Crystal Hive lighting (ambient ~0.5 at dark color, directional ~0.4), a Citrine cell (#d4a547) renders as approximately RGB(24,15,11) — indistinguishable from the #080d1a background. The user sees a blank canvas. **Fix:** Use `MeshBasicMaterial` (shows true color regardless of lighting) OR boost lighting to at least ambient 0.8 + directional 1.2 if you must use Lambert/Standard. MeshBasicMaterial is the correct choice for Crystal Hive 3D — the phenotype's depth comes from fog and opacity layering, not from dynamic lighting. Also: `renderer.setClearColor(0x080d1a, 1)` and remove `alpha: true` so the canvas has an opaque dark fill, not transparent over the body.
- **Static HTML opened via file:// breaks fetch() — add demo data fallback (2026-06-27):** When a Three.js prototype uses `fetch('/api/state')` to load data and the user opens the file directly with `open file.html` (file:// protocol) instead of through a running server, the fetch fails silently and returns an empty/error state. `buildCrystal([])` renders nothing. The user sees a blank page with no error. **Fix:** Catch the fetch failure and return a DEMO data object (10-18 sample tasks across all 8D dimensions, with known completion states) so the 3D structure always renders SOMETHING for visual review. This also enables designers to preview the visual structure without starting the backend.
- **Competitive research is MANDATORY before design work (2026-06-27 correction):** The user explicitly said "we need to find other 3d design dashboards out there. what else is out there that we can gather inspiration from?" Designing in a vacuum produces AI-looking output because the only reference is the agent's own training distribution (which is full of AI-generated mockups). Before ANY design work: (1) `web_search` for real shipping products that solve the same problem, (2) extract what makes them NOT look AI-generated, (3) present findings to the user, (4) THEN design. See `references/competitive-design-research.md` for the catalog of 8 apps audited this session (Things 3, Finch, Forest, Linear, deck.gl, Obsidian, Taskade, Lunatask) and the design principles extracted.
- **List primary, 3D reflection — the grow-from-accomplishment pattern (2026-06-27 design pattern from msg 838):** When building task/data visualization with a 3D element, the user rejected pre-existing complex 3D structures as "overwhelming." The approved pattern: (1) LIST IS THE DEFAULT VIEW — the user lands on a clean, calm task list (Things 3 aesthetic). This is where work happens. (2) 3D IS A REFLECTION VIEW — the structure does NOT pre-exist. It GROWS from accomplishment. Start with a single seed cell. Each completed task adds a cell. The structure IS progress made visible. (3) TOGGLE between views with a simple tab switch (Taskade pattern), not a page reload. The 3D should feel like it was "always there, behind the list, waiting." (4) GROWTH IS MONOTONIC — never shrinks, never punishes (adiabatic principle). This is the Finch/Forest model applied to productivity: feed it tasks and it grows. See `references/grow-from-accomplishment-pattern.md` for the full design specification.

## DYNAMIC PROCESS LAW (principal 2026-10-23: "Dynamic processes… always")

The production chain is a STANDING dynamic process, never a fixed one. Every deliverable runs through the EXPANDED chain, and the chain itself re-reads the live bench each time:

1. **Model rotation per seat**: no single model produces the whole chain. Spine seats (Goethe palette, Wernicke voice, Bell render, Luria gate) run with model diversity in mind; when multiple models/harnesses are available, assign different ones per seat. Mono-model chain = same defect as mono-vendor (dead reviewer bench proof).
2. **Corpus layer mandatory**: canon_query.py before design, every time. The absorbed-knowledge layer is part of the process, not an optional step.
3. **Cross-harness adversarial verdict**: every principal-facing artifact ships only after (or explicitly labeled pending) a second-harness review. Adversarial = another harness AND model (law-block amendment T-261023-0041).
4. **4-dynamics layer read**: before delivery, read the artifact against the layer matrix (harness/model/mesh/DB/...) — which layers does this artifact touch, and are any monoculture seams introduced.
5. **New harness/model auto-incorporation**: when a new harness (Muse Code, etc.) or model (Spark 1.3, etc.) lights up, it enters the rotation automatically at the next production run. The process never needs a manual "expansion" — expansion is its default state.
6. **Real data over decoration**: hero visuals use measured data from the live system (engine states, embeddings, benchmark JSONs), never synthetic placeholder numbers. Numbers in the artifact must trace to a probe or report file.

## Verification
- After completing a creative task, run the appropriate checks for the chosen phenotype:

  **For Crystal Hive (product UI / interactive / 3D — the DEFAULT):**
  - `grep '#080d1a\|080d1a' .` → should find the night-deep background
  - `grep '#e8d5a0\|e8d5a0' .` → should find moonlight gold
  - `grep '#4ab5a5\|4ab5a5' .` → should find whisper teal (this IS the brand color)
  - `grep 'Helvetica Neue\|-apple-system' .` → should find the system font stack
  - `grep 'fractalNoise' .` → should find the film grain overlay
  - `grep 'googleapis' .` → should return 0 matches (NO Google Fonts CDN)
  - `grep '#ffffff.*paper\|paper:#ffffff' .` → should return 0 matches (Fleet Atlas white is the WRONG phenotype for product UI)
  - Open the output and visually inspect: dark blue-black bg, gemstone dimension colors clearly distinguishable, no eye strain.

  **For Fleet Atlas (reports / PDFs ONLY):**
  - `grep '#ffffff\|paper' .` → should find white paper backgrounds
  - `grep '#0a1e2e' .` → should find ink text color
  - `grep '#ffd700' .` → should find gold accent

  **WARNING:** The following checks from a PREVIOUS session are DEPRECATED and WRONG. Do NOT run them:
  - ~~`grep -r '#4ad6b4'` → 0 matches~~ (FALSE — teal IS the Crystal Hive brand color)
  - ~~`grep -r '#061220'` → 0 matches~~ (FALSE — that was a different shade, not the banned one)
  - ~~`grep 'Iowan Old Style|Georgia|Palatino'` → should find serif body~~ (FALSE — serif is NOT the brand font for products)
  - These stale checks caused a session to REJECT the correct Crystal Hive phenotype and REVERT to the wrong warm-charcoal palette, triggering three rounds of user corrections.

## Reference Files
- `references/competitive-design-research.md` — Catalog of 8 real shipping apps audited for 3D/spatial task visualization (Things 3, Finch, Forest, Linear, deck.gl, Obsidian, Taskade, Lunatask). Includes "what makes things look AI-generated" (AVOID) and "what makes things look human-designed" (EMULATE) checklists. MANDATORY reading before any 3D/product design work — the user explicitly requires competitive research before design.
- `references/grow-from-accomplishment-pattern.md` — The approved design pattern for task visualization: list is primary, 3D crystal grows from completing tasks (never pre-exists, never shrinks). Based on msg 838 course correction and the Finch/Forest growth model. Use when building any task/data visualization with a 3D element.
- `references/ai-telltale-design-audit.md` — The 8-point quality gate for stripping the "AI-generated look" from 3D/interactive work (fonts, colors, layout, typography, rendering, legend, interaction, density). Includes competitive research on 8 apps that work (Linear, Raycast, Notion Calendar, Flighty, Mapbox Studio, Obsidian, Structured, Superhuman), proven design tokens, and the three-column 3D viz layout with bidirectional sync pattern. MANDATORY pre-delivery checklist.
- `references/3d-microtubule-honeycomb-technique.md` — Three.js pattern for tightly-packed hexagonal honeycomb cylinders (task grids, dense categorical data). THREE BINDING RULES: single layer first (concentric only on user approval), static by default (ambient motion destroys legibility), cells must almost touch (hex size derived from cylinder geometry, not hardcoded). Use when the user says "honeycomb" or "microtubule" or needs many small cells tessellating a cylinder skin.
- `references/creative-process-gap-diagnosis.md` — Full diagnosis of why the creative spine breaks for 3D/interactive work, the required corrected process flow, and the body-part gap analysis handed to sibling-agent (bus msg #819). Read this BEFORE starting any 3D/interactive creative task.
- `references/boucher-engine-rename-2026-06-27.md` — Details of the the specialist engine -> the specialist engine engine rename that resolved the process/engine name collision. Files changed, naming convention lesson.
- `references/8d-sleep-phenotype-tokens.md` — The complete extracted phenotype DNA from the D Sleep PWA (Warm Midnight palette, breathing glow, Mucha lines, grain overlay, spacing scale, nav pattern). Use this as the phenotype source when the user says "make it look like 8D Sleep."
- `references/3d-crystal-hive-technique.md` — Three.js crystal hive build pattern (the APPROVED 3D approach). Faceted gemstone growth with 8 color-coded arms, breathing seed core, crystallize-on-complete interaction, gemstone palette system. Use this for any data-heavy product needing a 3D structure. See `references/3d-constellation-technique.md` for the RETIRED orbit approach (rejected — looked like planets).
- `references/cylindrical-time-linear-geometry.md` — **MANDATORY for task-engine / time-based 3D structures.** Cylindrical geometry with vertical time axis, crystal facets growing radially proportional to duration, four-mode concentric layers (Personal→AI, Business→AI, AI→Personal, AI→Business). User explicitly rejected orbits/planets/spheres/stacked-boxes.
- `references/branding-architecture-and-platform-strategy.md` — Body-part engine gap analysis (5 missing systems with corrected engine names), branding advisory panel design, platform-specific content methodology, hook architecture, and cross-platform content matrix.
- `references/closed-loop-production-workflow.md` — Organismic metabolic cycle for scalable brand operations, 8-stage closed loop with IP protection, cron job ecosystem, and implementation roadmap.
- `references/ip-protection-disclosure-framework.md` — 4-layer disclosure framework (Public / Surface Methodology / Proprietary / Existential), pre-publication IP check checklist, what to show vs hide quick reference, and academic publication strategy. MANDATORY reading before delivering any public-facing artifact.

## Related Skills
- `ds-genome-transcription` – Source of brand DNA (load first).
- `ai-image-generation` – Grok/xAI and other image backends; social-hero prompt budgets and anti-Fleet-Atlas rules.
- `ondemand-advisory-panels` – For creating branding advisory panel workspaces.
- `social-content-pipeline` – For batch social media post generation + Physiomorphic LinkedIn pair.
- `social-profile-optimization` – For LinkedIn/Twitter profile revamps.
- `brand-naming-ideation` – For generating names that comply with DS DNA.
- `architecture-diagram` – For creating SVG architecture diagrams in DS style.

---
*This skill encapsulates the lessons from sessions where branding drift, AI‑like output, and feature loss occurred due to skipping genome transcription or misapplying the phenotype spec. It is a class‑level skill intended to be reused across all Divinity creative work.*