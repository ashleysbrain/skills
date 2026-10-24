# Labeled anatomy diagram pipeline

Use when a teaching figure needs multi-leader scientific labels (neuron, body systems). Diffusion alone is not ship-grade for this class.

## Failure log (2026-08-02)

| Asset | Failure |
|---|---|
| v3c split | "Ranvier" shorthand; Heart/Lungs/Gut organ mix |
| v3d Grok | soma labeled on axon; node at terminal arbor; duplicate NERVOUS/IMMUNE |
| Pure beautify without lock | leaders drift |
| v3g craft img2img | better gold but **duplicate IMMUNE** labels |
| Black rectangle heal | looks broken on LinkedIn — never ship |

## Pipeline A — full code lock

1. **Lock geometry in code** (Pillow or SVG): place each leader from structure centroid to label.  
2. **Assert label set** in code constants (no free-text hallucination).  
3. Optional **xAI edit** with: keep every scientific label and placement; improve craft only; no new systems; no wellness; no footnote.  
4. **Crop** bottom ghost text / prompt residue.  
5. **Vision QA checklist** (fail closed) — see below.  
6. Ship local master path; CDN is secondary.

## Pipeline B — hybrid category slide (preferred when the principal wants human + hero craft)

the principal (2026-08-02): physiomorphic side should combine the **human-looking figure** with the **first hero iteration** gold craft. Everything else stays the same.

1. **Build/keep left master** via Pipeline A (neuron + node of Ranvier + bottom lockup). Source: `...-v3f-split.png`.  
2. **Generate right panel only** (empty navy left ~40–45%):  
   - Human: pale filled frontal body, soft organ silhouettes (not gore, not diagnostic UI).  
   - Craft: hero-v1 DNA — luminous gold flecked nodes, unequal filaments, cascade rings, Da Vinci construction ticks, deep navy void.  
   - Labels: exactly six system-level chips (constants below).  
   - Title PHYSIOMORPHIC; caption `organism scale`; no slogan/footer (composite supplies them).  
3. Optional **img2img**: `image_url=right_raw`, `reference_image_urls=[hero-v1.png]`, prompt = craft upgrade only + keep unique labels.  
4. **Vision QA right alone** before composite. Reject duplicate labels (esp. IMMUNE). Prefer clean raw over craft-with-dupes.  
5. **Composite** at 1920×1080:  
   - Paste full left master.  
   - Paste right body above bottom lock band.  
   - Soft vertical seam blend at mid.  
   - Thin divider line.  
   - Bottom band always from left master (slogan + footer).  
6. **Heal without black boxes:** sample navy from empty field (`getpixel` on void); soft feathered fill; redraw crisp title/caption if garbled (`Organism scale bone` style glitches).  
7. Final vision QA on composite. Ship `...-v3g-split.png`.

## Vision QA checklist (fail closed)

- [ ] node of Ranvier → gap between myelin only (full phrase)  
- [ ] soma → cell body  
- [ ] dendrites / axon / myelin sheath correct  
- [ ] six unique system-level body labels (no Heart/Lungs/Gut)  
- [ ] no duplicate labels  
- [ ] no Sleep/Mood/Focus/Decision  
- [ ] no black cover patches  
- [ ] slogan + footer intact and legible  
- [ ] left NEUROMORPHIC / right PHYSIOMORPHIC titles present  

## Neuron constants

dendrites, soma, axon, myelin sheath, node of Ranvier

## Body system constants (category slide)

NERVOUS, CARDIOVASCULAR, RESPIRATORY, DIGESTIVE, IMMUNE, ENDOCRINE

## Mechanism modules (separate slide; not anatomy)

SPECIALISTS, COORDINATION, REGULATION, RECOVERY, DEFENSE, TIMING

## xAI invoke note

`XAIImageGenProvider.generate()` → URL on key `image` / `public_url`.  
Supports `image_url` (edit) and `reference_image_urls` (style refs).  
Local file path OK for edit/reference on this host.  
`image_generate` → FAL 402: fall through to xAI plugin; do not invent "image gen broken."
