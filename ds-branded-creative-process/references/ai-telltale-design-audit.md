# AI-Telltale Design Audit + Competitive Reference

Reusable quality gate for stripping the "AI-generated look" from 3D data
visualizations and interactive prototypes. Developed from the microtubule
task-viz master plan review (2026-06-27) where the user said: "hermes needs
to do another DETAILED REVIEW of the designs — these still look very AI
generated with fonts, text, optional features, etc."

Use this as a pre-delivery checklist for ANY interactive/3D creative output.
Score 8/8 = ship-ready. Anything below = iterate.

## The 8-Point Audit

### 1. FONT CHOICE + EDITORIAL SPLIT — the #1 telltale
- **Telltale:** Inter (Google Fonts CDN) is the universal AI-slop font. But
  even the SYSTEM sans-serif stack alone reads as AI default — uniform sans-serif
  everywhere is the AI-generated signature. JetBrains Mono paired with Inter
  reads as "AI coder made this."
- **Fix (two-part):**
  1. **NO Google Fonts CDN.** Use macOS-native stacks.
  2. **Editorial font split — this is what kills the AI look.** Use SERIF for
     body text and dimension labels (Iowan Old Style / Palatino / Georgia — all
     macOS-native). Use MONOSPACE for data, counts, status bars, and UI labels
     (SF Mono / ui-monospace / Menlo). Make dimension labels ITALIC serif. This
     serif/mono split is a deliberate editorial decision AI almost never makes.
     Verified 2026-06-27: the user said "these colors and this font still look
     super ai generated" about a system-sans-serif design. After switching to
     serif body + mono data, the look changed to "warm, paper-based tool."

### 2. COLOR TEMPERATURE + TREATMENT
- **Telltale:** Cool navy background (#061220, blue undertones) + neon teal
  (#4ad6b4) + saturated gold. This specific combination is the universal AI
  mockup palette. Every ChatGPT/Claude design output defaults to exactly this.
  The user said: "these colors still look super ai generated."
- **Fix (color temperature shift — verified 2026-06-27):** Shift WARM across
  the board. Background: warm charcoal (#13100d, NOT cool navy). Gold: antique
  (#c9a84c, NOT bright #e8d5a0). AI accent: muted sage (#8a9a76, NOT neon teal
  #4ad6b4). 8D dimensions: earth tones (olive #6b7a52, dust rose #8a6d6b, slate
  #7a8a9a, ochre #a68b4a, rust #b56a3e) — NOT saturated jewel tones. Zero blue
  undertones anywhere. This reads as intentional, not algorithmic.
- **Treatment fix:** Flatten everything. No gradients on panels. No radial glow
  animations. If light variation is needed, use OPACITY steps (0.0 to 1.0),
  never additive bloom.

### 3. LAYOUT PATTERNS
- **Telltale:** Frosted-glass cards (`backdrop-filter: blur`), rounded corners
  (`border-radius: 4px+`), segmented pill toggles. This is the default Figma
  AI export template.
- **Fix:** Sharp edges (`border-radius: 0` or `2px` max). Solid backgrounds
  (not frosted glass). Use 1px hairline borders, not card elevation. Think
  Bloomberg Terminal, Linear.app, Raycast — flat, dense, typographic.

### 4. TYPOGRAPHY HIERARCHY
- **Telltale:** Decorative titles ("Task Microtubule" at 22px weight 200).
  Descriptive subtitles that read like AI wrote them for the AI to understand
  ("8D hexagonal honeycomb cylinder · single layer").
- **Fix:** Kill decorative titles. Replace with functional nav breadcrumbs or
  a minimal status bar (mode tag, task count, completion count). The 3D
  structure speaks for itself. If a title is needed, make it a 10px uppercase
  letter-spaced label, not a 22px styled display.

### 5. 3D RENDERING ITSELF
- **Telltale:** ExtrudeGeometry with uniform MeshBasicMaterial and wireframe
  edges — looks like a Three.js tutorial. All cells identical material.
- **Fix:** Use MeshLambertMaterial (or MeshStandardMaterial with low
  roughness variation) for subtle material depth. Add ONE directional light
  + ambient fill (not multiple point lights). Let the lighting create
  natural variation across faceted surfaces. Consider a subtle film grain
  post-pass for organic texture.

### 6. LEGEND DESIGN
- **Telltale:** Floating legend card in the corner with colored chips and
  backdrop-filter blur. Classic D3.js demo pattern.
- **Fix:** Integrate the legend INTO the UI chrome. In a three-column layout,
  the task list IS the legend — each row shows its dimension color inline.
  The 3D view should not need a separate legend floating on the canvas.

### 7. INTERACTION LANGUAGE
- **Telltale:** Floating hint text ("drag = orbit · scroll = zoom"). No real
  product does this — it screams "interactive demo."
- **Fix:** Remove hint text. If interaction is non-obvious, use a one-time
  3-second first-load animation that demonstrates the primary gesture, then
  never shows again. Or rely on discoverability — modern users expect
  drag-to-orbit.

### 8. DATA DENSITY
- **Telltale:** Sparse. 16-56 cells on a cylinder looks empty. A real task
  view for a productive person has 50-200 items visible. Sparsity screams
  "mockup, not product."
- **Fix:** Increase density. Personal mode = 60-80 visible cells. Business
  mode = 120-160. Pack tighter. The honeycomb should feel like a LIVING
  structure, not a sparse demo.

## Proven Design Tokens — CONTEXT-DEPENDENT (CORRECTED 2026-06-27)

**CRITICAL:** The original "warm shift" advice in this section (warm charcoal #13100d, sage #8a9a76, serif fonts) was REJECTED by the user: "too dark and gloomy, eye strain" and "match the 8D fonts." The ACTUAL brand phenotype is Crystal Hive (dark blue-black + teal + system-ui). See parent skill Step 3. The warm charcoal tokens below are DEPRECATED.

### Product UI (Crystal Hive — DEFAULT):
- BG: #080d1a, #0f1525, #161e35 (dark blue-black)
- Gold: #e8d5a0 (moonlight), Teal: #4ab5a5 (whisper-teal)
- Font: system-ui weight 300 + SF Mono
- 8D: gemstone palette (Citrine, Fluorite, Amethyst, etc.)
- Film grain overlay required

### Reports/PDFs (Fleet Atlas):
- BG: #ffffff, Ink: #0a1e2e, Gold: #ffd700, Teal: #4ad6b4
- Font: Helvetica Neue + SF Mono

### DEPRECATED (do not use):
- #13100d warm charcoal, #8a9a76 sage, Iowan/Palatino/Georgia serif

## Original Notes (partially superseded by correction above)

UPDATED 2026-06-27 after user rejected the navy/teal palette: "these colors
and this font still look super ai generated." The warm shift is what made it
pass. The OLD tokens below are marked DEPRECATED.

```
Fonts:   SERIF body: 'Iowan Old Style','Palatino','Georgia',serif
         MONO data: ui-monospace,'SF Mono',Menlo,monospace
         Dimension labels: italic serif
         (NOT uniform sans-serif — that is the AI telltale)

BG:      #13100d (canvas, WARM charcoal), #1c1814 (panels), #221e18 (cards)
         (NOT #061220/#0a1e2e cool navy — that is the AI telltale)

Gold:    #c9a84c (antique), #dab863 (bright), #7a6938 (dim)
         (NOT #e8d5a0 bright AI gold)

AI accent: #8a9a76 (muted sage), #5a6850 (dim)
           (NOT #4ad6b4 neon teal — that is the AI telltale)

8D dims:  Physical #6b7a52 (olive), Psych #8a6d6b (dust rose),
          Intel #8a9a76 (sage), Social #7a8a9a (slate),
          Voc #c9a84c (gold), Fin #a68b4a (ochre),
          Env #8a9a6b (moss), Spi #b56a3e (rust)
          (NOT saturated jewel tones — earth tones only)

Text:    #c9c3b5 (body, warm), #e0d9c8 (bright), #6b6557 (dim)
         (NOT #c4d8e8 cool blue-white)

Borders: 1px solid rgba(201,168,76,0.07) — hairline warm
Radius:  0 (sharp edges everywhere)
Shadows: NONE — depth from material + lighting only
Light:   1 DirectionalLight (#dab863, 0.55) + AmbientLight (#4a3f34, 0.45)
Material: MeshLambertMaterial (not MeshBasicMaterial — allows light variation)
```

## Competitive Reference — Apps That Don't Look AI-Generated

Researched during the master plan review. What each does right and what to
steal:

### LINEAR.APP
Extreme density, keyboard-first, flat with zero decoration. Status columns
with colored bars. The "My Issues" view is a flat list with inline status,
priority, project — zero chrome.
- **Steal:** Task list sidebar pattern. Inline status chips. Click list item
  opens detail panel (not floating card).
- **Anti-pattern:** Do NOT copy their purple color scheme. Use Fleet Atlas
  gold/teal instead.

### RAYCAST
Command palette over everything. Minimal chrome. Dense, monospace,
functional.
- **Steal:** The right-side task list should feel like a Raycast window —
  dense, monospace, functional. Not a frosted-glass card.

### NOTION CALENDAR
Time grid + list hybrid. Tasks have inline connections (database relation
to project, person). Visual weight is in the CONTENT, not the chrome.
- **Steal:** Dual-panel layout. Calendar connections per task (the Universal
  Hub integration).

### FLIGHTY (flight tracker)
NOT a task app, but the BEST example of dense real-time data viz that looks
human-designed. Timeline + aircraft dots. Zero decoration. Color encodes
status. Everything is functional.
- **Steal:** The visualization IS the data. No legend needed because the
  visual encoding IS the legend.

### MAPBOX STUDIO
3D map rendering with data layers. Three-column layout: left = layers,
center = map canvas, right = properties. Dense, professional, zero
decoration.
- **Steal:** The three-column layout for the task engine: LEFT = filters /
  dimensions, CENTER = 3D microtubule, RIGHT = task list. Proven pro-tool
  layout.

### OBSIDIAN GRAPH VIEW
Force-directed graph of notes. Click node = highlight in graph + open note.
Interaction is bidirectional (graph <-> list).
- **Steal:** Bidirectional sync. Click hex cell = highlight in list. Click
  list row = highlight + camera-orbit in 3D. This is the exact pattern.

### STRUCTURED (time blocking)
Visual timeline with blocks. Drag to resize. Blocks are FLAT rectangles —
size and position encode duration and order.
- **Steal:** Shape encodes meaning (tall block = long task). In our case:
  hex extrusion depth = completion, hex size = time allotted.

### SUPERHUMAN
Split-pane email. Keyboard shortcuts everywhere. Design is BORING in the
best way — it disappears. You see the data, not the UI.
- **Steal:** The disappearing UI philosophy. The 3D view should feel like
  looking at a real object through glass, not like a "designed UI."

## Design Pattern Synthesis

What makes a 3D viz NOT look AI-generated (updated 2026-06-27):
- **WARM color temperature, not cool navy** — the #1 trigger. Shift everything warm.
- **Serif body + mono data editorial split**, not uniform sans-serif
- System fonts (macOS-native), not Google Fonts CDN
- Zero gradients, zero glow, zero frosted glass
- Sharp edges (0-2px radius), not rounded
- Dense text, not spacious "designed" layouts
- Functional labels, not decorative titles
- Material variation (MeshLambert with light), not uniform flat
- One directional light source (warm), not ambient point-light fill
- Post-processing grain or natural material texture, not noise-free
- Earth-tone dimension colors (olive/sage/rust/ochre), not saturated jewel tones

## Three-Column 3D Viz Layout (the proven pattern)

```
┌─────────┬──────────────────────┬──────────┐
│  LEFT   │      CENTER          │  RIGHT   │
│ 180px   │      flex            │  300px   │
│         │                      │          │
│ Dim     │   3D Canvas          │ Task     │
│ filters │   (OrbitControls)    │ List     │
│         │                      │ (sorted  │
│ Mode    │   Status bar (top)   │  by AI   │
│ selector│   Detail strip (btm) │  priority│
└─────────┴──────────────────────┴──────────┘
```

- LEFT: dimension toggles (click to isolate), mode selector
- CENTER: 3D canvas, functional status bar (mode, count, complete count,
  AI suggestion count), detail strip on selection
- RIGHT: ordered task list, sorted by AI priority then 8D balance

**Bidirectional sync (Obsidian pattern):**
- Click 3D cell -> list scrolls to row, highlights, detail strip appears
- Click list row -> 3D cell edges brighten, camera can smooth-orbit
- Hover either -> corresponding element highlights subtly
- State is shared — single data model drives both views

## Verification

Run these checks after building:
```javascript
// In the HTML file, grep for telltales:
'@import'              // Google Fonts CDN — must be ABSENT
'googleapis'           // Google Fonts — must be ABSENT
'backdrop-filter'      // frosted glass — must be ABSENT
'border-radius:4'      // rounded — must be ABSENT
'autoRotate = true'    // ambient spin — must be ABSENT (unless requested)
'MeshStandardMaterial' // OK only if roughness variation is intentional
```

A quick Python verification (from this session):
```python
checks = {
  'NO Google Fonts CDN': '@import' not in body and 'googleapis' not in body,
  'System font stack': 'system-ui' in body and '-apple-system' in body,
  'No backdrop-filter': 'backdrop-filter' not in body,
  'No border-radius > 2': 'border-radius:4' not in body,
  'No auto-rotate': 'autoRotate = false' in body or 'autoRotate: false' in body,
}
```
