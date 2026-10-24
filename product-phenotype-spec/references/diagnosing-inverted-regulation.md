# Diagnosing Inverted Regulation

## The Problem Pattern

When a DS product "looks too technical," the root cause is almost always **inverted epigenetic regulation**: the engineering chromosome (Ch6) is expressed at full strength while the philosophy (Ch4) and product/interaction (Ch10) chromosomes are barely expressed.

This manifests as:
- Physics engine visible in the UI (gauges, scores, equations, solver names)
- Dashboard-first layout (data grid as primary view)
- Technical jargon in user-facing text
- Generic SaaS aesthetics (cold navy, electric purple, pure white)
- Achievement/gamification patterns (streaks, badges, score celebrations)
- Dense information display (radar charts, dimension breakdowns as grids)

## The Diagnostic Method

### Step 1: Read the Product's CSS

Find the product's main stylesheet. Check for the "generic SaaS signature":

| Signal | What It Means | Correct Direction |
|--------|---------------|-------------------|
| Cold navy background (`#0a0e27` or similar) | No warm-dark palette defined | Warm midnight with undertone |
| Electric/saturated accent (`#7c5cfc` purple) | No product-specific accent | One muted, warm, domain-specific accent |
| Pure white text (`#ffffff`) | No dark-adapted text color | Warm off-white (e.g. `#c4d4e8`) |
| 4+ accent colors | Competing visual voices | One accent per screen |
| `rgba(255,255,255,X)` borders | Cold SaaS border treatment | Warm-tinted, near-invisible borders |
| Font-weight 600+ on headings | Urgent/aggressive typography | Light weights (200-400), generous spacing |
| Uniform border-radius | Undifferentiated component hierarchy | Mixed radii for different element types |

### Step 2: Read the Primary Component

What does the user see first when they open the product?

- **If dashboard (gauge + radar + grid + text):** Ch6 is over-expressed. The physics is the face.
- **If single feeling/message with depth behind a tap:** Correct. The physics serves the experience.

### Step 3: Scan User-Facing Strings

Search for technical terms in user-facing text:

```
grep -ri "kuramoto\|TWC\|coupling\|oscillator\|coherence\|order parameter\|dimension score" src/
```

If any appear in user-facing strings (not in engine/internal files), Ch6 is leaking into the user experience. It must be suppressed.

### Step 4: Build the Expression Audit

Create a table showing current expression vs correct expression:

| Chromosome | Current Expression | Correct Expression | Evidence |
|------------|-------------------|--------------------|---------| 
| Ch4 Philosophy | ? (check if product reflects surrender/non-attachment/etc.) | AMPLIFY for sleep | [specific findings] |
| Ch6 Engineering | [HIGH if gauges/equations visible] | SUPPRESS for sleep | [specific findings] |
| Ch10 Product/Interaction | ? | AMPLIFY for sleep | [specific findings] |

### Step 5: Write the Correction

The phenotype spec's Chromosome Expression Map (Section 3) and Implementation Translation (Section 11) are the correction. Each inverted regulation gets a concrete CSS/component fix.

## The 8D Sleep Case Study (June 2026)

**Diagnosis:** The 8D Sleep PWA had classic inverted regulation:
- Ch6 (Engineering): expressed at FULL strength — TWC gauge as primary element, radar chart primary view, 8-dimension grid, technical terms in UI
- Ch4 (Philosophy): barely expressed — no sense of surrender, calm, or rest in the visual design
- Ch10 (Product/Interaction): barely expressed — no progressive disclosure, no calm pacing, no breathing room

**Root cause:** No phenotype spec existed. The genome specified shared DNA but not how it should express for sleep. Engineers defaulted to generic dark-mode dashboard because nobody told them what sleep should feel like.

**Correction:** The phenotype spec (03_8D_SLEEP_PHENOTYPE_SPEC.md) defines the correct expression map and concrete CSS/component fixes. The Pre-Code Freeze document (04_PRE_CODE_FREEZE_20260619.md) captures the "before" state for revertability.

**Key learning:** "Looks too technical" is never a styling problem. It is a regulation problem. Fix the expression map, not the colors. The colors are a symptom.
