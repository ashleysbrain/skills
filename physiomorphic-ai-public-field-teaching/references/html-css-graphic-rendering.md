# HTML/CSS Graphic Rendering Pipeline (learned 2026-08-03)

## When to use this instead of Pillow

Pillow cannot produce museum-quality typography. Its rendering ceiling (crude anti-aliasing, no font hinting, pixel artifacts) gets WORSE with iteration, not better. When a graphic needs:

- Real serif fonts (Cormorant Garamond, Georgia at display sizes)
- Glow filters on SVG elements
- CSS gradients, vignettes, grain overlays
- Golden ratio layout precision
- Readable text on dark backgrounds

...use HTML/CSS + browser screenshot instead of Pillow.

## The pipeline

1. Write a standalone HTML file with inline CSS (no external stylesheets except Google Fonts via `@import`)
2. Set canvas to exact target size: `width: 1920px; height: 1080px; overflow: hidden`
3. Serve locally: `python3 -m http.server 8753` from the assets directory
4. Navigate with `browser_navigate` to `http://localhost:port/filename.html`
5. Screenshot with `browser_vision` (provides a screenshot path you can deliver)
6. The screenshot is the deliverable PNG

## Key advantages over Pillow

- Real font rendering with anti-aliasing and hinting
- SVG `<filter>` for glow effects (feGaussianBlur, feMerge)
- CSS `radial-gradient` for smooth glows
- CSS `linear-gradient` for text-zone curtains
- `@import url('https://fonts.googleapis.com/...')` for Cormorant Garamond, Inter, etc.
- SVG `<circle>` for constellation nodes with filter glow
- Exact pixel positioning via CSS `position: absolute`

## Golden ratio composition (binding for DS announcement posters)

```css
/* Text zone: golden section minor (38.2%) */
.text-zone { width: 38.2%; }

/* Visual zone: golden section major (61.8%) */
/* Constellation fills this zone */

/* Vertical anchors */
.phi-minor { top: 38.2%; }  /* "ANNOUNCING" label position */
.phi-major { top: 61.8%; }  /* tagline / eye rest point */
```

Phi = 1.618033988749895. Text zone width = 1/phi^2 = 0.382 = 733px on 1920 canvas. Visual zone = 1/phi = 0.618 = 1187px.

## Constellation body silhouette pattern

Build the constellation as an SVG with:
- Body-zoned node distribution (head cluster, shoulder spread, chest density, abdomen, pelvis, legs)
- Nodes as `<circle>` elements with varying radius (2.5-6px) and opacity
- Filaments as `<line>` elements with low opacity (0.25) connecting nearby nodes
- SVG `<filter id="softGlow">` with `feGaussianBlur stdDeviation="2"` for node glow
- Radial gradient glow behind the constellation from the golden focal point

## Known working HTML template

See `assets/tsc-announcement-v6.html` in `your-org-marketing/02-social-posts/` for the full working example:
- Cormorant Garamond serif typography
- Inter sans-serif for metadata
- SVG constellation with body silhouette
- Golden ratio text zone
- Film grain via SVG turbulence pattern
- CSS radial vignette
- Gold hairline border

## HTML/CSS iteration WORKS (unlike Pillow)

Unlike Pillow where each iteration gets worse, HTML/CSS iteration genuinely improves the output. Each pass adds real value: v6 (straight filaments + sparse nodes) → v7 (3-tier node system + right-side text fills) → v8 (98-node dense body silhouette + curved Bezier filaments + golden spiral overlay + layered atmosphere). Keep iterating on HTML/CSS when the user says "do another pass." The rendering ceiling is much higher and each complexity layer (gradients, filters, density) actually renders.

## Dense constellation generation technique (v8)

For a museum-quality body silhouette constellation, generate nodes and filaments programmatically in Python, then inject the SVG fragments into the HTML template:

1. Define body zones as (center_x, center_y, spread_x, spread_y, count, radius_multiplier) tuples covering head, neck, shoulders, chest, torso, abdomen, pelvis, legs, arms
2. For each zone, scatter nodes using `random.gauss(0, spread * 0.4)` for organic distribution
3. For filaments: compute pairwise distances, create short-range curved Bezier paths (`Q` control point with perpendicular offset) for dist < 55, and long-range dashed paths for 55 < dist < 120 at 30% probability
4. Three glow filter tiers: `stdDeviation="6"` for large nodes (r>=4), `"3"` for medium (r>=3), `"1.8"` for small
5. Add a faint golden logarithmic spiral path behind the constellation for phi-based construction geometry
6. Layer multiple radial gradients in the atmosphere for depth (warm gold center-right, cool blue bottom-left)

See the generation script pattern in `assets/tsc-announcement-v7.html` (v8 content) which produces 98 nodes, 83 short filaments, 115 long filaments from programmatic generation.

## When to still use Pillow

Pillow remains correct for:
- Pure typography quote cards (no visual elements, no constellation)
- Label-geometry proofs for anatomy diagrams (deterministic leader placement)
- Structural validation of I/O flow diagrams (arrow direction, column alignment)

The rule: if the graphic has ANY visual element beyond flat text, use HTML/CSS or diffusion. Not Pillow.
