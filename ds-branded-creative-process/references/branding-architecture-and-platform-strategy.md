# the specialist engine and Multi-Platform Strategy

Condensed reference from the June 2026 branding architecture session. Covers: body-part engine gap analysis, branding panel design, and platform-specific content methodology.

---

## 1. The Organism's Marketing Gap (Body-Part Analysis)

The DS creative faculty (Goethe, Wernicke, Bell, Luria) handles content CREATION. What is missing is the closed loop: CREATE → DISTRIBUTE → SENSE → ADAPT → PRUNE → REPEAT. The organism currently does only step 1.

### Five Missing Body Systems

| Missing System | Gray's Analog | Proposed Engine | Marketing Function |
|---|---|---|---|
| Sensory/Integumentary | Skin, sense organs | the specialist engine (port 8141) | Market perception, engagement analytics, sentiment analysis |
| Cardiovascular | Heart, vessels | the specialist engine (port 8140) | Multi-platform content distribution, format adaptation |
| Endocrine | Glands, hormones | the specialist engine (port 8142) | Posting cadence, timing optimization, seasonal rhythm |
| Lymphatic | Nodes, vessels | the specialist engine extension (port 8143) | Content lifecycle, A/B testing, stale content pruning |
| Enteric | Gut-brain axis | the specialist engine (port 8144) | Creative intuition, virality prediction, trend sensing |

**Build priority:** Malpighi (distribution) first, then Muller (sensory) as companion. Selye (timing) Phase 2. Metchnikoff ext. Phase 2-3. Gershon Phase 3-4.

**Key principle:** These are organism-level systems, not marketing-specific engines. They follow the production model: organism built first, pushes to products. They align with BRAIN-ARCHITECTURE.md.

**Naming collision resolution (IMPORTANT):** The original names "the specialist engine" (sensory) and "the specialist engine" (timing) collide with EXISTING engines in the fleet registry. the specialist engine is already an interoception engine; the specialist engine is already the clinical attending seat. They were renamed:
- the specialist engine → **the specialist engine** (Johannes Muller, Law of Specific Nerve Energies)
- the specialist engine → **the specialist engine** (Hans Selye, General Adaptation Syndrome)

Before naming any new engine, check `ds-engine-registry/ecs.py` for collisions. Names follow the convention: DS + [neurologist/anatomist surname relevant to the function].

### Research/Math Foundation

- **Kolmogorov complexity** — shortest expression of maximal meaning. A tweet is a compressed worldview.
- **Complex contagion (Centola 2018)** — ideas need multiple exposures to spread. Cross-platform cascade compounds.
- **Shannon entropy** — brand coherence = low entropy across touchpoints. Same signal everywhere.
- **Predictive coding (Friston 2010)** — the organism predicts what resonates, measures mismatch, updates.
- **Narrative transportation (Green & Brock 2000)** — stories change beliefs more than arguments. Why founder-as-proof works.
- **Dual process theory (Kahneman 2011)** — System 1 (TikTok/IG: visceral, 0.5s hook) vs System 2 (LinkedIn/academic: analytical).

---

## 2. Platform-Specific Methodology

### The the specialist engine (Short-Form Video, 15-60s)

```
0-0.5s: HOOK (visceral, System 1, pattern-breaking)
0.5-3s: TENSION (why this matters)
3-10s: INSIGHT (one coupling coefficient, one cascade, one leverage point)
10-30s: PROOF (dashboard, equation, before/after)
30-60s: TURN (what this changes; end with "Healthy people are kinder people")
```

### Platform Cheat Sheet

| Platform | Audience | Best Format | Cadence | Key Rule |
|---|---|---|---|---|
| TikTok | 18-34, discovery-driven | 15-30s data viz / kinetic typography | 3-5/week | Hook in 0.5s. Insights, not metrics. |
| Instagram | 25-44, visual-first | Carousels (8-10 slides), Reels | 3 carousels + 2-3 Reels/week | Design for saves, not likes. |
| Facebook | 30-55+, community | Video (1-3min), long-form text, groups | 2-3/week + daily group engagement | Spark discussion. |
| LinkedIn | Professional | Long-form posts (500-1000 words) | 2-3/week | System 2 content. Analytical authority. |
| Twitter/X | Tech/health optimizers | Threads, single-stat posts | Daily | 280 chars = compressed worldview. |
| Academic | Researchers | Papers with coupling matrix figures | Parallel track, 6-12mo | TWC formula as math contribution. |

### Cross-Platform Content Matrix

One DS insight adapts across all platforms. Example: "Your sleep and your bank account are the same problem" (Psychological-Financial coupling: 0.54).

- **Twitter:** text + data card (280 chars)
- **LinkedIn:** 500-1000 word long-form
- **TikTok:** 15s coupling matrix animation
- **Instagram:** 8-slide carousel building the coupling map
- **Facebook:** discussion-starter text post
- **Academic:** journal figure with k=0.54 (p<0.001)

### Camera-Free Visual Concepts (Creative Faculty Can Produce)

1. Kinetic typography (Python + moviepy)
2. Animated data visualizations (D3.js, matplotlib, manim)
3. Screen recordings of actual DS engine interfaces
4. System diagram animations (manim)
5. Equation reveals (manim, 3Blue1Brown style)

---

## 3. The Branding Advisory Panel

### Distinct from Marketing Panel

Marketing Panel (Dunford, Krug, Asprey, Hyman, Bloom): positioning, category creation, distribution, content strategy.
Branding Panel: visual identity, brand architecture, platform-native design, brand coherence, emotional response.

### Seats

| Seat | Persona | Lane |
|---|---|---|
| Brand Strategy | AI Marty Neumeier | Brand definition, category identity, "the zag" |
| Visual Identity | AI Natasha Jen | Anti-blanding, brand tension, visual vocabulary |
| Platform-Native Design | AI Sahil Bloom (cross-seat) | Platform adaptation, personal branding |
| Design Psychology | AI Don Norman | Three levels: visceral, behavioral, reflective |
| Design×Technology | AI John Maeda | Computational brand consistency, simplicity laws |
| Adversarial | The Branding Skeptic | "Does this actually convert?" Prevents beautiful-but-ineffective |

### Panel Cadence

- Weekly brand review: each advisor reviews creative output through their lane
- Monthly strategy session: full panel reviews brand trajectory
- Quarterly brand audit: full coherence assessment

### How Panels Relate

Neumeier (brand identity) pairs with Dunford (positioning). Jen (visual) pairs with Krug (clarity). Bloom bridges both. Norman (feeling) pairs with Hyman (authority). Maeda (design-tech) pairs with Asprey (premium frame). The creative faculty executes both panels' direction.

---

## 4. Key Branding Decisions (from Panel Session 1)

1. Instagram is the first platform to go live (most forgiving for dark aesthetic)
2. Coupling matrix / organism visualization is the canonical brand visual signature
3. Hooks = insights (not metrics). Metrics live in carousels and papers.
4. Academic publication is parallel track, does not block platform content
5. Creative faculty produces all visuals — no stock, no templates, no filters
6. The "zag": DS optimizes the CONNECTIONS between things, not individual things
7. The one-second test: if someone sees it for one second, do they know it is Divinity Science?

---

## 5. Production Workflow for Multi-Platform Content

```
BRANDING PANEL sets visual/emotional direction
    ↓
MARKETING PANEL sets distribution/messaging strategy  
    ↓
CREATIVE FACULTY executes:
    the specialist engine → palette/proportions
    the specialist engine → copy/voice/AI-tell removal
    the specialist engine → render (HTML/PDF/SVG)
    the specialist engine → quality gate
    ↓
HUMAN reviews and approves
    ↓
MANUAL distribution to platforms (until distribution engine built)
    ↓
MANUAL engagement tracking (until sensory engine built)
    ↓
WEEKLY branding panel review of output
```

Phase 1 (current): Manual closed loop. Works today.
Phase 2: Semi-automated (distribution + sensory engines)
Phase 3: Adaptive closed loop (all 5 body systems)
Phase 4: Autonomous marketing organism (full brain operational)
