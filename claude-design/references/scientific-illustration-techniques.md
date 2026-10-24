# Scientific Illustration Techniques

Techniques for creating scientifically accurate visual graphics, validated through adversarial multi-agent review.

## Rendering Pipeline

### Primary: Puppeteer HTML→PNG

Use Puppeteer for ALL social media and brand graphics. Full CSS support (gradients, glows, blur, web fonts) produces professional output.

```javascript
const puppeteer = require('puppeteer');
const path = require('path');
async function screenshot(htmlFile, pngFile, width, height) {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  await page.setViewport({ width, height, deviceScaleFactor: 2 });
  await page.goto(`file://${path.resolve(htmlFile)}`, { waitUntil: 'networkidle0' });
  await page.evaluateHandle('document.fonts.ready');
  await new Promise(r => setTimeout(r, 500));
  await page.screenshot({ path: pngFile, type: 'png', clip: { x: 0, y: 0, width, height } });
  await browser.close();
}
```

Check availability: `npx --yes puppeteer --version`
Common location: `/tmp/node_modules/puppeteer` or global npm packages.

### Fallback: SVG Rendering on macOS

Use ONLY when Puppeteer is unavailable AND the graphic is purely geometric (no brand styling, no gradients, no glow):

```bash
qlmanage -t -s 2160 -o /tmp file.svg && mv /tmp/file.svg.png output.png
```

**Known limitations of SVG→PNG via qlmanage:**
- No blur, no radial gradients, no CSS filter effects
- `filter="url(#shadow)"` or any undefined filter references silently fail
- Complex gradients may render differently
- Output looks flat — rejected by users as "middle school PowerPoint" when used for brand graphics
- **Do NOT use for dark-mode brand designs** — the glow, dot grid, gradient, and typography elements that make them look professional cannot be rendered

## Concept Brief Template

Before designing ANY scientific illustration, write a concept brief that specifies:

```markdown
# Concept Brief: [Title]

## Scientific Content
- [Exact equations or formulas to visualize]
- [Directions of forces/arrows — state the physical law]
- [Number of connections in a network — exact count]
- [Axis labels, units, ranges]

## Visual Elements Per Graphic
### Post/Card 1: [Title]
- [Element]: [exact specification, e.g. "28 edges total connecting 8 nodes"]
- [Element]: [direction rule, e.g. "all force arrows point downhill (F = -∇V)"]

### Post/Card 2: [Title]
...

## Brand Style
- [Colors, dimensions, typography — link to brand style reference]

## Accuracy Constraints
- [Hard rules, e.g. "stroke width must AMPLIFY in cascade, not diminish"]
- [Values, e.g. "ball positions must be at V(x) local minima"]
```

The concept brief is the **contract** between the designer and the scientific reviewer. Every element that could be wrong must be specified.

## Adversarial Review Protocol

The adversarial reviewer must:

1. **Read the concept brief** — understand what's supposed to be correct
2. **Inspect each SVG/HTML file line by line** — check coordinates, directions, values
3. **Report by line number** — "Line 64: arrow points from (200,300) to (200,200) which is uphill, but F=-∇V means force points downhill"
4. **Classify issues**:
   - CRITICAL — scientifically wrong (wrong direction, wrong value, missing elements)
   - MODERATE — misleading or unclear (ambiguous labeling, poor scaling)
   - COSMETIC — visual polish only (alignment, spacing)
5. **Count connections/elements** — verify "28/28 edges present" not just "looks connected"

### Fix-Review Loop

After fixes, re-run the adversarial review. The loop ends when:
- Zero CRITICAL issues remain
- MODERATE issues are either fixed or explicitly accepted by the user
- The reviewer confirms "all physics/math is accurate"

## Physics Diagram Specifics

### Force Fields and Potential Energy
- Force arrows must follow F = -∇V (point from high to low potential, i.e. downhill)
- Stable equilibrium: V''(x) > 0 (bowl shape, ball at bottom)
- Unstable equilibrium: V''(x) < 0 (hill shape, ball at top)
- Energy barrier (Ea) lines must align with the saddle point / barrier peak

### Network Graphs
- Count edges explicitly and state "N/M connections shown"
- Verify no duplicate edges
- Check node positioning doesn't create visual ambiguity about which nodes connect

### Cascade/Propagation Diagrams
- Stroke widths should AMPLIFY through cascade (thicker downstream) to show energy gain
- "Settled" or "reached" nodes should have visual distinction (glow, fill change)
- Direction of propagation must match the physical process

## HTML/CSS Brand Design Pattern

For dark-mode social media graphics (proven on Divinity Science LinkedIn series):

```
Body: fixed 1080×1350px, overflow hidden, dark background (#0D0F1A)
Layers: dot-grid overlay → blur glow orbs → content (z-index stacking)
Brand header: diamond icon + "DIVINITY" white + "SCIENCE" accent color
Headline: 68px bold white, accent color on key word
Bottom accent bar: 4px gradient (transparent → accent → transparent)
Post number: large, ultra-low opacity (4%) watermark
```

Each post in a series uses its own accent color (teal → purple → gold) while keeping all other brand elements identical.

## Session Reference

Pipeline proven on 2026-06-09 for Divinity Science LinkedIn 3-part Physics Engine series:
- Initial SVG approach via qlmanage: rejected by user as crude/unprofessional
- Switched to Puppeteer HTML→PNG with full CSS brand styling: accepted
- Adversarial physics review found 3 CRITICAL + 2 MODERATE issues in first SVG pass
- All issues fixed, re-rendered via Puppeteer
- Files: `/<workspace>{1,2,3}.png`
