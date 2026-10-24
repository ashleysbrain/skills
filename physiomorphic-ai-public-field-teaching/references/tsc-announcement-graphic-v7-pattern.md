# TSC Announcement Graphic v7 Pattern (2026-08-03)

## Ship artifact
`assets/tsc-announcement-v7.html` — HTML/CSS poster rendered via `python3 -m http.server 8753 --bind 127.0.0.1` + browser preview.

## Approved content (tested through 5 rejections)

### Left text zone (golden section minor, 38.2% width)
- Label: `ANNOUNCING` (gold, Inter, 0.5em tracking)
- Title: `Physiomorphic AI` (Cormorant Garamond 88px, white + gold italic "AI")
- Tagline: `The neuron was the beginning. The organism is the next scale.` (italic, gold accent on second line)
- Divider: thin gold gradient line
- Label: `Now Live` (NOT "First Implementation" — the principal rejected both "First Living Organism" and "First Implementation")
- Name: `the operator agent` (Cormorant Garamond, large)
- Meta: `100+ specialized engines, each mapped to a biological system. An operating system engineered to function like a body, not just a brain.`
- Author: `the principal Williams` (gold)
- Title: `Divinity Science · the operator agent`

### Top right (context badge)
- Label: `PRESENTING AT TSC 2026` (gold, uppercase, tracked)
- Sub: `The Science of Consciousness · San Diego` (italic Cormorant)

### Bottom right (disclaimer)
- `Multi-Agent Architecture · Biologically Structured — Not a Consciousness Claim`

### Visual zone (golden section major, 61.8% width)
- Dense body-shaped constellation mesh: 98 nodes, curved Bezier filaments (83 short-range + 115 long-range dashed), three-tier node glow system
- Golden spiral overlay (faint, logarithmic)
- Layered atmospheric gradient (warm gold center-right, cool blue bottom-left)
- Film grain, vignette, gold border with accent corners

## Corrections that led to this version

| Rejection | the principal feedback | Fix applied |
|---|---|---|
| "too much open navy space" | Phi-based composition required | Golden ratio layout (38.2/61.8 split) |
| "doesn't follow davinci golden ratio" | Dead space reads unfinished | Dense constellation filling the visual zone |
| "First Living Organism" | "the operator agent isn't a living organism... not scientific" | Removed "living" |
| "First Organism Built on This Paradigm" | "it is technology not a real organism" | Changed to "Now Live" |
| "100+ agents" | "ensure these agents are labeled as engines... they are systems" | Changed to "100+ specialized engines" |
| "can't tell what the operator agent is" | Meta text disconnected from name | Connected narrative: label -> name -> full explanation |
| "remove poster #775 and sole author" | Conference logistics don't belong on graphic | Removed poster number + sole author; kept conference name |

## Rendering pipeline
1. Serve HTML via `python3 -m http.server 8753 --bind 127.0.0.1` in assets dir
2. `browser_navigate` to `http://127.0.0.1:port/tsc-announcement-v7.html`
3. `open_preview` for live preview
4. `browser_vision` for QA (if llm-vendor vision API available)
5. Export PNG via browser screenshot when ready for LinkedIn

## Why HTML/CSS over Pillow
Pillow produces programmer art: crude anti-aliasing, no real font hinting, pixel-level artifacts. HTML/CSS gives real web fonts (Cormorant Garamond + Inter from Google Fonts), real SVG glow filters, real CSS golden-ratio layout. Multiple Pillow iterations on complex compositions get progressively WORSE. See `references/html-css-graphic-rendering.md`.
