---
name: product-phenotype-spec
description: "Write the epigenetic expression profile for any Divinity Science product. Defines how the shared DS genome differentiates into a specific product identity (voice, visual personality, emotional register, design philosophy). Same genome, different cell."
version: 1.0.0
metadata:
  hermes:
    tags: [product, phenotype, design, identity, epigenetic, genome, sleep, divinity-health]
    category: creative
---

# Product Phenotype Spec Skill

## What This Is

This skill writes the **epigenetic expression profile** for a Divinity Science product. It defines how the shared DS genome (BRAND-DNA.md) differentiates into a specific product identity.

In biology, a neuron and a liver cell share identical DNA. They differ only in **which genes are expressed**. This skill produces the document that defines which DS genome chromosomes are expressed, suppressed, and amplified when the genome differentiates into a specific product.

**Without a phenotype spec, a product inherits the physics but not the identity.** It reaches for generic defaults (dark-mode dashboards, SaaS purple, technical jargon) because nobody told it what to be.

## When This Skill MUST Load

Load this skill BEFORE writing or revising any of these:

- A product phenotype specification (sleep, focus, recovery, nutrition, fitness, etc.)
- The design identity document for any Divinity Health or future womb product
- A product "soul" or "personality" definition
- Any document that defines how a specific DS product should look, feel, sound, or behave

This skill loads AFTER `ds-genome-transcription` (you must read the genome before you can write a phenotype, because the phenotype regulates the genome).

## The Biological Model

### Waddington's Epigenetic Landscape

Conrad Waddington's landscape is already assigned to the specialist engine (reproductive engine, port 8090) for physics birth. This skill extends the same model to **identity birth**.

The ball rolls down the same landscape (genome) but canalizes into different valleys (phenotypes). Each product phenotype spec defines which valley the product rolls into.

```
DS GENOME (one landscape)
    ↓ epigenetic regulation
PRODUCT PHENOTYPE (which valley)
    ↓ compiled alongside
PHYSICS DNA (coupling matrices)
    ↓ expressed as
PRODUCT EXPERIENCE (what the user feels)
```

### The Layering Model

```
Layer 0: GENOME (BRAND-DNA.md)
         Shared by ALL products. Never changes per product.
              ↓ epigenetic regulation
Layer 1: PRODUCT PHENOTYPE (this skill produces this)
         Expression profile for ONE product.
              ↓ compiled alongside
Layer 2: PHYSICS DNA (DNA Package)
         Coupling matrices, solvers, scoring.
              ↓ expressed as
Layer 3: PRODUCT EXPERIENCE
         What the user sees, hears, feels.
```

**DNA without phenotype = engine with no body.**
**Phenotype without DNA = body with no engine.**
**Both required for a living product.**

---

## How to Write a Phenotype Spec

### Step 1: Read the Genome

Load `ds-genome-transcription` and read `/<workspace>` in full. The phenotype regulates the genome. You cannot regulate what you have not read.

### Step 2: Identify the Product

Determine:
- Product name (e.g., 8D Sleep)
- Womb (e.g., Divinity Health)
- Primary 8D dimension(s) the product addresses
- The core human experience the product serves (sleep, focus, recovery, etc.)

### Step 3: Build the Chromosome Expression Map

This is THE core mechanism. For each of the 11 DS genome chromosomes, assign an expression level:

| Expression Level | Meaning | When to Use |
|-----------------|---------|-------------|
| **AMPLIFY (core)** | This chromosome is the HEART of this product. Maximum expression. | For the dimensions the product lives in (e.g., Ch4 Philosophy for sleep = surrender) |
| **EXPRESS (tuned)** | Active but adjusted for this product's register. | For chromosomes relevant but needing domain tuning (e.g., Ch3 Voice = quieter for sleep) |
| **EXPRESS (adapted)** | Active but adapted to product brand, not DS brand. | Ch1 Identity always (product brand, not DS) |
| **MODERATE** | Present but not dominant. Available on demand. | For chromosomes that support but don't lead (e.g., Ch11 Evidence for sleep) |
| **SUPPRESS** | Active in the system but invisible to the user. | For chromosomes the user should never feel (e.g., Ch6 Engineering) |
| **SUPPRESS (background)** | Exists but never surfaced. | Ch8 Legal, Ch5 Business internals |

The expression map IS the differentiation. Two products with the same genome but different expression maps are different products.

### Step 4: Define the Emotional Register

Answer: **What should the user FEEL when they use this product?**

- The core feeling (one sentence)
- Emotional states by context (morning, evening, during use, after use)
- The anti-emotion (what the product must NEVER make the user feel)

The emotional register is NOT about features. It is about the felt experience. A sleep product feels calm. A focus product feels sharp. A recovery product feels warm.

### Step 5: Write the Design Philosophy

Write 5-7 product-specific design principles that layer ON TOP of the genome's design rules (golden ratio, Mucha/Klimt/Bauhaus/Da Vinci, no emoji, custom SVG, structural rebuild).

These principles do NOT replace genome rules. They add the product-specific dimension. The genome says "use phi." The phenotype says "phi, and the screen is a bedroom."

Each principle should connect to an amplified chromosome. If Ch4 (Philosophy) is amplified, a design principle should express that philosophy in product terms.

### Step 6: Define the Voice Register

The genome defines the organism's voice. The phenotype tunes it for this product.

- How does THIS product speak? (Same DNA, different register)
- Voice by context/time/state
- Vocabulary rules: banned words (technical terms) and preferred words (human equivalents)
- The translation rule: every technical concept has a human equivalent

### Step 7: Define the Visual Personality

The genome specifies "product-specific CSS." The phenotype defines what that means for THIS product.

**Palette:** A product-specific color system derived from (not copied from) the genome's indigo context. Define:
- Primary background (warm or cool dark?)
- Primary accent (one hero color)
- Secondary accents (muted, supportive)
- Text colors (never pure white for dark products)
- Border treatment (warm-tinted, near-invisible, or structural?)

**Typography:** How the genome's Helvetica Neue expresses in this product:
- Font weights (sleep = ultra-thin 200; focus = medium 500)
- Letter-spacing (airy vs tight)
- Line-height (generous vs compact)
- Score/number treatment (light and large vs bold)

**Motion:** How the product moves:
- Transition durations (sleep = slow 500-800ms; focus = snappy 200ms)
- Easing curves
- Ambient motion (breathing for sleep; pulse for focus)
- Banned motions (no bounce for sleep; no drift for focus)

**Imagery/Iconography:** Drawing from the genome's artist palette but tuned:
- Which motifs fit this product? (lunar for sleep, solar for focus, botanical for recovery)
- What NOT to use (dashboard icons, medical iconography, achievement markers)

### Step 8: Define the First-Sight Principle

What does the user see and feel in the first 3 seconds of opening the product?

- Describe the primary screen in words
- What is the ONE message?
- Where is the data? (behind a tap, never first)
- The test: does this screen advance or hinder the product's core feeling?

### Step 9: Define the Interaction Posture

How does the product behave?

- Gamification rules (usually: none for wellness products)
- Notification rules (when to push, when to stay silent)
- Comparison rules (usually: never compare users)
- Color rules for negative states (no red for wellness)
- Depth-on-demand rules
- Affirmation-first rules

### Step 10: Write the Anti-Pattern

Define what this product is NOT. This section prevents regression to generic defaults.

List 5-7 things the product must never be. Reference the current build's violations if applicable.

### Step 11: Implementation Translation

Map phenotype principles to concrete changes in the actual codebase:
- CSS token changes (current value → phenotype-correct value)
- Component changes (current behavior → phenotype-correct behavior)
- Rebuild priority (what to fix first for maximum impact)

### Step 12: Pre-Code Freeze Protocol (MANDATORY before any code changes)

After the phenotype spec is written but BEFORE any code is changed, create a freeze point. This is a hard rule from the user. The purpose is to ensure full revertability if the implementation goes wrong.

**What the freeze point captures:**
1. **Current state snapshot** — record every CSS token, component structure, and voice string currently in use (the "before" state)
2. **Backup the genome** — `cp docs/BRAND-DNA.md docs/BRAND-DNA.md.bak-pre-[feature]-[date]`
3. **Implementation plan** — the 4-phase rebuild roadmap (palette → primary screen → motion → voice) with specific token swaps
4. **Revert instructions** — exact commands to undo every change
5. **Decision log** — what was decided, why, and when

**Save as:** `docs/womb-architecture/04_PRE_CODE_FREEZE_[date].md` (or next available number)

**The rule:** No code changes may begin until the freeze point document exists. The user must be able to say "revert to the pre-code state" and have a clear, tested path to do so. This applies to ALL product implementations, not just 8D Sleep.

---

## The Phenotype Template

Use this structure for every phenotype spec:

```
# [Product Name] Phenotype Specification
## The Epigenetic Expression Profile for [Womb]'s [Nth] Product

1. What This Document Is
2. The Layering Model
3. Chromosome Expression Map (THE core mechanism)
4. Emotional Register
5. Design Philosophy (product-specific principles)
6. Voice Register
7. Visual Personality (palette, typography, motion, imagery)
8. The First-Sight Principle
9. Interaction Posture
10. The Anti-Pattern
11. Implementation Translation
12. The Phenotype Template (reference to this skill)
```

Save to: `docs/womb-architecture/[NN]_[PRODUCT]_PHENOTYPE_SPEC.md`

---

## Differentiation Examples

Same genome, different phenotype. The mechanism is epigenetic.

| Product | Emotional Register | Ch4 Amplification | Ch6 Suppression | Design Philosophy | Palette Base |
|---------|-------------------|--------------------|-----------------|-------------------|--------------|
| 8D Sleep | Calm, dark, surrender | Non-attachment, impermanence | Physics invisible | The screen is a bedroom | Warm midnight + moonlight amber |
| 8D Focus | Sharp, clear, energized | Dynamic non-equilibrium | Physics as confidence | The screen is a morning run | Cool dawn + signal teal |
| 8D Recovery | Warm, healing, patient | Compassion, adaptation | Physics as guidance | The screen is a healing space | Soft earth + dawn rose |
| 8D Nutrition | Clear, vibrant, alive | Interdependence | Physics as intelligence | The screen is a kitchen garden | Fresh green + harvest gold |

**The genome does not change. The expression does.**

---

## Quality Gate

Before finalizing a phenotype spec, verify:

- [ ] Genome was read first (ds-genome-transcription loaded)
- [ ] Chromosome expression map covers all 11 chromosomes
- [ ] Emotional register has a core feeling + anti-emotion
- [ ] Design philosophy has 5-7 product-specific principles
- [ ] Voice register defines banned words and preferred words
- [ ] Visual personality defines palette, typography, motion, imagery
- [ ] First-sight principle describes the 3-second experience
- [ ] Interaction posture defines behavioral rules
- [ ] Anti-pattern lists what the product is NOT
- [ ] Implementation translation maps to actual codebase changes
- [ ] No emoji, no AI tells? Run the anti-tell checklist (see Human-Touch Engineering section: border-accent, symmetry, uniform roundness, template rigidity, over-detail)
- [ ] Surgical imperfection specified via Phi Deviation Table? (every deviation from perfection must be phi-calculated, never random — see Surgical Imperfection section)
- [ ] No Anthropic models used in production (per genome Ch5.3)

Before any code changes are made from the spec, verify:

- [ ] Pre-Code Freeze document created (Step 12)
- [ ] Current state fully snapshotted (CSS tokens, components, voice strings)
- [ ] Genome backed up
- [ ] Revert instructions written and tested
- [ ] User can restore the pre-code state by following the documented commands

---

## Human-Touch Engineering

This is the hardest problem in phenotype design: making AI output that does not look AI-generated. The research is clear — see `references/human-touch-research.md` for the full findings. Key takeaways for every phenotype spec:

### Anti-Tell Checklist (embed in Visual Personality section)
Every phenotype spec must enumerate which AI tells are banned for this product and how to avoid them:

- **Border-accent pattern:** The #1 AI tell (colored accent on left border of content blocks). Ban it explicitly.
- **Dead-center symmetry:** Humans use rule-of-thirds, negative space, imbalance. Encode off-center composition.
- **Uniform roundness:** Mixed radii (4px for data, 12px for cards, 999px only for pills), never one radius for everything.
- **Template rigidity:** Vary structure. Avoid rigid "Subject/Objective/Audience/Benefits" blocks.
- **Over-detailed everything:** Enforce focal hierarchy. One hero element per screen.
- **Em-dash and AI vocabulary:** Banned in voice register (already covered).

### Surgical Imperfection — The Phi Deviation Rule (embed as a phenotype trait)

**HARD RULE: No deviation from symmetry, centering, or perfection may be random.** Every "imperfection" in DS design output must be calculated against the golden ratio. This is what separates craft from chaos.

The user was explicit: "We don't want to just make things randomly off balance. It needs to be mathematical, not just throw this weird thing over here because it's not perfect. It needs to be precise and surgical."

A human master painter's brushstroke is imperfect, but its deviation is not arbitrary — it follows an internal logic born of trained instinct. We encode that instinct mathematically.

| Imperfection Type | WRONG (Random) | RIGHT (Phi-Based, Surgical) |
|---|---|---|
| **Off-center placement** | "15% to the left" | 0.382 from edge (golden conjugate), or 0.618. Never 0.50. |
| **Focal point offset** | "Shift slightly" | On phi intersection of canvas grid (1/phi from edge) |
| **Line weight variation** | "Randomly thicker" | phi scale: 1.0px, 1.618px, 2.618px by hierarchy position |
| **Grain/texture opacity** | "5% noise" | phi^-3 = 2.36% (below conscious perception, above zero) |
| **Animation timing** | "Vary the speed" | Duration = 400ms x phi^n. Easing via cubic-bezier with phi-derived control points |
| **Spacing irregularity** | "Vary margins" | Deviations are +/- phi^-2 x base unit (+/- 0.382x), never arbitrary pixels |
| **Color temperature drift** | "Slightly warmer" | Measured in Kelvin, offset by phi^-1 of base palette range |

Every phenotype spec must include a **Phi Deviation Table** specific to that product, defining exactly which elements deviate from perfection and by what phi-derived amount.

**The difference between "handcrafted" and "sloppy" is whether the deviation is phi-justified.** Fechner proved in 1876 that the human visual cortex preferentially responds to phi-derived asymmetry. Random asymmetry feels wrong. Phi asymmetry feels human.

### Aesthetic Evaluation (for the quality gate)
The phenotype spec's quality gate should reference multiple evaluation dimensions, not a single scalar:

- **HPSv3** (SOTA, Spearman r=0.94 with human judgment) for aesthetic quality scoring
- **CREA six-principle Creativity Index** for creative evaluation (originality, expressiveness, aesthetic appeal, technical execution, unexpected associations, interpretive depth)
- **Anti-tell detector** for AI-marker screening
- **Domain-specific critic** for product-fit (sleep app should not look like a dashboard)

**CRITICAL:** Never use a single scalar aesthetic score as the sole gate. Aesthetic evaluation models carry bias (the "Algorithmic Gaze" problem — LAP disproportionately filters by gender and culture). Run a portfolio of evaluators.

---

## Pitfall: Using the Wrong Phenotype for Interactive Products (2026-07-16 — CORRECTED 5 TIMES IN ONE SESSION)

**The failure:** I repeatedly built interactive dashboards using the wrong phenotype. The user corrected me FIVE TIMES in one session. Each time I used either the Fleet Atlas (PDF) phenotype, the 8D report phenotype (from `phenotype_8d.py`), or a generic light-mode design. All wrong.

**The three phenotypes (DEFINITIVE):**

1. **Fleet Atlas** = PDF documents ONLY. Dark navy/teal + gold. WeasyPrint rendered. NEVER for interactive products.
2. **8D Report Phenotype** (`phenotype_8d.py`) = Bell-rendered PDF reports ONLY. Light paper (#ffffff), ink (#0a1e2e), teal (#4ad6b4), gold (#ffd700), tables, weight-200 headers. This is the PDF/scientific report look. NOT for dashboards. NOT for interactive products.
3. **the specialist engine Phenotype** (`phenotype_ds.py` in `ds-engine-shared/`) = ALL interactive products (dashboards, chat interfaces, command centers, organism tools). Dark night sky (#080d1a), moonlight (#e8d5a0), starlight (#c4d4e8), indigo (#6366f1), Inter font, JetBrains Mono data, rounded cards, noise texture, breathing glow. This is the dark, humanlike, organism-aware interface.

**THE RULE:** For ANY interactive HTML product (dashboard, chat, command center, tool):
- Use `phenotype_ds.py` from `ds-engine-shared/`
- Call `render_shell(title, subtitle, nav_items)` to generate the shell
- Dark background. Moonlight accents. Rounded cards. Breathing animations.
- NEVER use `phenotype_8d.py` for interactive products
- NEVER use Fleet Atlas for interactive products
- NEVER use a light background for a dashboard

**The `phenotype_ds.py` module** was created 2026-07-16 at `ds-engine-shared/phenotype_ds.py`. It provides `TOKENS`, `PHENOTYPE_CSS`, and `render_shell()`. Same pattern as `phenotype_8d.py` but for the dark product phenotype.

**Why I kept getting it wrong:** The BRAND-DNA has three contexts (PDF, Interactive Prototype, Shipped Product). I conflated "Interactive Prototype" with the Fleet Atlas because the DNA references "Fleet Atlas adapted for dark theme." But the ACTUAL dark product phenotype evolved through the gg-command-center and 8d-sleep-web builds into something completely different from Fleet Atlas. The DNA is the starting point. The phenotype modules (`phenotype_8d.py` for reports, `phenotype_ds.py` for products) are the authoritative implementations.

**The failure:** When building a DS-branded 3D task visualization, defaulted to dark mode (navy bg + neon teal accents). User correction was immediate and multi-layered:
1. "these colors and this font still look super ai generated"
2. "these colors are too dark and gloomy. I can't easily tell them apart it takes eye strain"
3. "match the 8D fonts as this font isn't our branding"

**Root cause:** Dark mode with saturated neon accents is the universal AI-generated mockup aesthetic. Every ChatGPT/Claude/DALL-E output defaults to it. On top of that, dark mode with muted colors creates eye strain because low-contrast colors on dark backgrounds are harder to distinguish.

**The rule (CORRECTED 2026-06-27):** DS has MULTIPLE phenotypes. The user explicitly said "the 8D phenotype is not white." Product UI uses the Crystal Hive phenotype (dark #080d1a + moonlight gold + whisper teal). Reports/PDFs use the Fleet Atlas phenotype (white #ffffff). The phenotype spec MUST state which one applies. See `ds-branded-creative-process` Step 3 for the full three-phenotype hierarchy.

**When starting ANY DS product design:**
1. Determine: is this a PRODUCT (interactive UI) or a REPORT (document/PDF)?
2. For products: use Crystal Hive phenotype (dark). Source: `divinity-health/task-engine-live/index.html` or `divinity-health/8d-sleep-web/`
3. For reports: use Fleet Atlas phenotype (white). Source: `docs/bell-output/ds-report-*.html`
4. NEVER use warm charcoal (#13100d) + sage + serif — this was REJECTED by the user as "too dark and gloomy, can't tell colors apart, eye strain"

See `references/canonical-8d-phenotype-tokens.md` in the `ds-genome-transcription` skill for the extracted CSS.

---

## Workflow Pitfall: Phenotype Specs Are Advisory Until Birth Canal Enforces Them

**CRITICAL architectural finding (2026-06-20):** The phenotype spec model works
on paper but is NOT enforced at the engineering level. The Medawar birth canal
(`ds-trophoblast-engine`, :port) validates:
- Capability cassette signatures (HMAC-SHA256)
- Leak scans (cassette cannot reconstruct the operator agent internals)
- Capability format (CapabilityItem: `{name, kind, version}`)

But it does NOT check for a phenotype reference. The capability cassette has no
`phenotype_ref` field. This means a product baby can be born with full physics
and zero identity enforcement. The phenotype spec is an advisory document that
the build team must manually apply — the organism does not automatically express
or suppress chromosomes based on it.

**The "regulation inversion" symptom:** When a phenotype spec exists but isn't
enforced, products default to expressing Ch6 (Engineering) at full strength
(gauges, scores, equations visible) while Ch4 (Philosophy) and Ch10 (Product &
Interaction) are barely expressed. The 8D Sleep Phenotype Spec documents this
exact problem in Section 3, line 70: "Ch6 is expressed at full strength while
Ch10 and Ch4 are barely expressed. The regulation is inverted."

**The architectural fix (not yet built):** Add a `phenotype_ref` field to the
capability cassette format, enforced at the `/transfer` step. The morphogen
engine (the specialist engine) would provide gradient signals telling the product baby
which chromosomes to amplify/suppress — the biological analog of morphogen
gradients telling a stem cell what to differentiate into.

**What this means for phenotype spec writers:** Until the birth canal is upgraded,
phenotype specs must be manually translated into code changes. The spec is the
design authority, but enforcement is human/agent-mediated, not automated. Always
include an Implementation Translation section (Step 11) with concrete CSS token
swaps, component changes, and rebuild priorities — because no system automatically
applies these changes from the spec.

## Workflow Pitfall: Document Before Code

The user's hard requirement when approaching code changes on any DS product:

1. **Documentation freeze point FIRST.** Before any code is modified, create a pre-code freeze document that captures: current CSS tokens, current component structure, current voice, and the exact changes planned. The user must be able to see what will change before it changes.
2. **Backup every file before touching it.** Every file gets a `.bak-pre-<change>-<date>` copy. The genome gets a backup before any mutation.
3. **Revert path documented.** The freeze document must include explicit revert instructions (exact `cp` commands).
4. **No code changes until the phenotype spec exists AND is reviewed.** The phenotype spec is the design authority. Code follows the spec, never the other way around.

This is not optional. The user explicitly said: "I want to be able to go back to this version if you do a poor job on the next version." Treat every code change as potentially needing full rollback.

## Workflow Pitfall: Phenotype = Craft Language, NOT Layout

**CRITICAL (2026-06-27 user correction):** The phenotype is the **craft language** (palette, motion, typography, grain, Mucha lines, progressive disclosure, breathing glow) — NOT the layout structure of the reference product. The user's exact words: "This looks like you just copy/pasted the new words into the 8d phenotype. I need you to actually build a new design but keep the same theme for the phenotype."

Each new product must have its OWN structural identity built IN the shared craft language. A task engine should NOT look like a sleep app with the words changed. It should be its own 3D/living structure that happens to breathe with the same warm-midnight atmosphere.

**Phenotype source hierarchy (binding):**
1. The live reference product URL the user provides — navigate to it, read its source, extract exact CSS variables.
2. An existing phenotype spec HTML file.
3. The brief's own aesthetic tokens — LAST RESORT ONLY.

When the user says "I want it to look like [product X]", that product IS the phenotype source for the craft language. But the LAYOUT must be original to the new product. Copy the DNA (colors, motion, type, atmosphere), then build a NEW structure speaking that language.

**PHENOTYPE = craft language (palette, motion, typography, grain, atmosphere)**
**LAYOUT = unique to each product (never copy from the reference)**

This is the same distinction as genome vs phenotype in biology: the genome (craft language) is shared; the phenotype (body structure) is unique to each organism.

---

**PITFALL:** When fighting AI-generated appearance (anti-tell work), it is tempting to "add imperfection" by randomly offsetting elements, varying spacing arbitrarily, or injecting noise at round-number opacities. The user caught this and corrected it firmly.

**The correction:** Every deviation from perfection must be phi-calculated. Off-center at 0.382, not "about 15%". Grain at 2.36% (phi^-3), not "about 5%". Line weights at 1.0/1.618/2.618px, not "varied". The difference between "handcrafted" and "sloppy" is whether the deviation is phi-justified.

**Why:** Random asymmetry feels wrong because the human visual cortex evolved to find phi-derived proportions beautiful (Fechner 1876). Imperfection placed at phi positions feels human. Imperfection placed randomly feels like an error. The user said: "it needs to be precise and surgical, what we're doing, and not just making random errors in our work."

**Embed this as a Phi Deviation Table in every phenotype spec's Visual Personality section.**

---

## Reference

- **First phenotype spec:** `docs/womb-architecture/03_8D_SLEEP_PHENOTYPE_SPEC.md` (the canonical example)
- **Genome:** `docs/BRAND-DNA.md`
- **Genome transcription skill:** `ds-genome-transcription` (load before this skill)
- **Da Vinci Creative System:** `docs/DA-VINCI-CREATIVE-SYSTEM.md` (design philosophy source)
- **Womb Architecture:** `docs/WOMB-ARCHITECTURE.md` (birth system)
- **Human-touch research:** `references/human-touch-research.md` (AI tells, HPSv3, CREA framework, taste injection techniques, HITL workflows)
- **Blank template:** `templates/phenotype-spec-template.md` (copy and fill for new products)
- **PDF generation script:** `scripts/ds-pdf.py` (markdown to DS-branded PDF via weasyprint + Fleet Atlas CSS; usage: `python3 ds-pdf.py input.md output.pdf "Title"`)
- **Creative Faculty Guide:** `docs/CREATIVE-FACULTY-GUIDE.md` (team operations guide for the design team)
- **Diagnostic reference:** `references/diagnosing-inverted-regulation.md` — how to diagnose when a product "looks too technical" (root cause: inverted epigenetic regulation, not styling)

---

*Product Phenotype Spec Skill*
*Divinity Science*
*The epigenetic regulation mechanism for product differentiation*
