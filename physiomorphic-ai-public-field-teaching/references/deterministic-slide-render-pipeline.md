# Deterministic Slide Render Pipeline (SCAFFOLDING ONLY — NOT SHIP ART)

> **WARNING (learned 2026-08-02):** the principal rejected code-rendered slides as "not good at all." Pillow renders are programmer art, not museum-quality field-introduction visuals. Use this pipeline ONLY for label-geometry validation, arrow-direction proofing, and structural scaffolding. Never ship as final LinkedIn slides. Final deliverables require diffusion imagery (xAI Grok Imagine / FAL).

## When to Use This Pipeline (scaffolding only)

- Validate that label positions and leader lines work geometrically before committing to a diffusion prompt
- Verify arrow direction logic in I/O flow diagrams before asking diffusion to reproduce them
- Structural mockup for composition planning (where panels go, how much space labels need)
- Emergency fallback when you need to show the principal a layout concept, NOT a finished deliverable

## When NOT to use

- Final LinkedIn slides (use diffusion)
- Anything the principal will post publicly
- Hero images or craft-quality visuals

## Environment

```bash
cd /<workspace>
uv run --with pillow python - <<'PYEOF'
# ... script
PYEOF
```

System Python has a broken PIL `_imaging` import. Always use `uv run --with pillow` to get a clean Pillow install. The the operator agent venv PIL is also broken for drawing operations.

## Slide 1: Neuron + Body with Tech Labels (geometry template)

Output: `physiomorphic-ai-linkedin-teach-v3k-slide1.png` (1920x1080, landscape) — DRAFT ONLY

### Key design decisions (learned)

1. **Body fill must be ivory/bone tone** `(200, 195, 180)`, not dark navy. Dark body fill reads as an abstract blob, not a human figure.
2. **Arms and legs drawn as thick filled lines** (width 14-16px) with outline stroke.
3. **Torso is a filled trapezoid polygon** with gold outline.
4. **Labels go OUTSIDE the body silhouette** with leader lines to gold node pins ON the body.
5. **Neuron is fully deterministic**: recursive branch() for dendrites, ellipse soma, myelin segments as rounded rectangles with gold gap markers for nodes of Ranvier.

### Label positions (right panel, bx=center of body, by=torso center)

```
SPECIALISTS  -> head (bx+2, by-200)
COORDINATION -> upper chest (bx+28, by-85)
REGULATION   -> mid torso (bx-18, by-25)
RECOVERY     -> upper abdomen (bx-3, by+50)
DEFENSE      -> lower torso side (bx-32, by+105)
TIMING       -> hip side (bx+22, by+125)
```

Labels alternate left/right of body for visual balance.

### Palette

| Element | RGB |
|---|---|
| Background gradient | (8,22,34) to (6,20,30) |
| Teal (neuron) | (140,190,198) |
| Teal dark (soma fill) | (35,75,88) |
| Gold (body/physiomorphic) | (201,162,39) |
| Gold bright (labels) | (232,205,120) |
| Body fill (ivory) | (200,195,180) |
| Bone (text) | (236,232,220) |
| Muted (captions) | (150,165,175) |
| Chip background | (28,24,12) |

## Slide 2: Three-Path I/O Flow (geometry template)

Output: `physiomorphic-ai-linkedin-teach-v3k-slide2.png` (1920x1080, landscape) — DRAFT ONLY

### Arrow logic

- **Main flow arrows**: downward, from INPUT to middle stage to OUTPUT. Filled triangle arrowheads.
- **Feedback loop (physiomorphic only)**: upward curved arrow from DIAGNOSTICS back to REGULATION. Arc with arrowhead at top.
- **LOAD/STRESS bar**: horizontal red line across all three columns with downward triangle markers.

### Column layout

```
Column width = (1920 - 120) / 3 = ~600px each
Margins: [60, 660, 1260]
Centers: [360, 960, 1560]
```

### Arrow rendering function

```python
def draw_arrow_down(cx, y0, y1, color, width=3):
    d.line([(cx, y0), (cx, y1)], fill=color, width=width)
    d.polygon([(cx, y1+8), (cx-7, y1-1), (cx+7, y1-1)], fill=color)
```

### Middle stage by column type

- **single** (model-centric): one large box "MODEL / LLM CORE"
- **multi** (common multi-agent): three small agent boxes + two tool boxes
- **physio** (physiomorphic): six module boxes in 3x2 grid + DIAGNOSTICS circle with feedback arc

## Pitfalls

1. Do NOT use system python3 or the operator agent venv for Pillow. Use `uv run --with pillow`.
2. Do NOT paste diffusion text over code base. Composite at panel level only.
3. Do NOT draw arms/legs as thin 2px lines. Use width 14-16.
4. Do NOT use dark body fill. Ivory/bone tone only.
5. Arrowheads must be filled triangles, not line endpoints.
6. **Do NOT ship these as final deliverables.** They are geometry proofs only.
