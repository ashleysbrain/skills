# HTML/CSS-to-PNG Social Graphic Production Pipeline

Render announcement graphics locally using HTML/CSS + Chrome headless.
This is the minimum quality bar for DS social graphics. Pillow (Python
code art) was rejected 6+ times as "programmer art."

## When to use

Any social media graphic that needs:
- Real typography (Cormorant Garamond, Inter, Georgia)
- Golden ratio / Da Vinci composition
- Gradients, glows, vignettes, film grain
- Production-quality output for LinkedIn upload

## Stack

- **HTML/CSS** with Google Fonts via `@import`
- **SVG** for any vector elements (glows, nodes, filaments)
- **Python http.server** as local dev server
- **Chrome headless** for screenshot rendering to PNG

## Production workflow

### 1. Write HTML file

Standard DS announcement graphic structure:

```
body: 1200x1200 (square) or 1920x1080 (landscape)
atmosphere: layered radial + linear gradients
focal-glow: radial gradient behind text
text-zone: flex column, centered vertically
grain: SVG noise overlay (opacity 0.03)
vignette: radial gradient darkening edges
border: thin gold hairline
corner accents: L-shaped gold marks
```

Font imports:
```css
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400&family=Inter:wght@200;300;400;500;600&display=swap');
```

### 2. Serve locally

```python
# terminal(background=True)
cd /path/to/assets && python3 -m http.server 8753 --bind 127.0.0.1
```

Verify: `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:port/filename.html`
Should return 200.

### 3. Render to PNG via Chrome headless

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless \
  --screenshot=/path/to/output.png \
  --window-size=1200,1200 \
  --force-device-scale-factor=2 \
  --hide-scrollbars \
  "http://127.0.0.1:port/filename.html"
```

The `--force-device-scale-factor=2` produces 2x retina-quality output.

### 4. Copy to Downloads for easy access

```python
import shutil
shutil.copy(source_path, '/<workspace>')
```

Deliver via `MEDIA:/<workspace>`.

## Design corrections (learned 2026-08-03)

### REJECTED approaches
- **Pillow / Python code art** — rejected 6+ times. Cannot match museum quality.
- **Quote cards that just display locked text** — "this is silly." Graphics must COMMUNICATE something beyond the post text.
- **Body constellation meshes / AI-generated silhouettes** — "I don't like this weird body like thing the ai tried to generate." User rejected constellation body shapes, node networks, and filament meshes as the visual element.
- **Dead space** — large empty areas of navy with nothing in them must be cropped out. Crop tight.
- **Wide landscape with left text + right illustration** — after the constellation was removed, the split layout left dead space. Switched to square crop with text centered over the glow.

### APPROVED approach
- **Clean typography on dark gradient** — announcement text is the hero, not illustrations
- **Gold radial glow behind text** — adds depth without complexity
- **Tight square crop** — no dead space, text fills the frame
- **Golden ratio composition** — text anchored at phi vertical points
- **Gold hairline border + corner accents** — frames the composition

### Crop discipline
When the visual element (constellation, illustration, mesh) is removed or
rejected, CROP the canvas to eliminate dead space. Do not leave large
empty areas. The text and glow should fill the frame.

Square (1200x1200) works well for LinkedIn announcement cards. Landscape
(1920x1080) only when there is actual visual content on the right side.

## User feedback signal patterns (learned 2026-08-03)

- **"do another pass"** does NOT mean tweak parameters. It means the
  design concept itself is wrong. Rethink the approach, not the knobs.
- **"this is worse"** means the last change regressed. Stop iterating
  blindly. Identify what specifically regressed before the next pass.
- **"too much open navy space"** = dead space must be eliminated. Crop
  tight. Fill the frame with content or reduce canvas size.
- **"doesn't follow davinci golden ratio"** = layout must use phi
  divisions for element placement. Not just "centered."
- When the user says the visual element (constellation, body shape, AI
  art) is bad, do NOT try to fix it. Remove it entirely and let
  typography carry the composition.
- Pillow renders at minimum 5x before user says "try building it in
  HTML." Skip Pillow entirely for social graphics. Go straight to HTML.

### User rejected centered text as too rigid

"too much centered" = the composition must hold the golden ratio
off-balance. Text should be left-anchored (or right-anchored) with
the glow weighted opposite. Not perfectly centered. Not perfectly
symmetric. The eye should travel.

### Final approved dimensions

After 8+ iterations, the approved graphic for the TSC announcement:
- Canvas: 880x720 (tight 1.22:1 aspect, minimal dead space)
- Text zone: 680px wide, left-aligned, vertical-center
- Glow: 520px, positioned at 48% left / 40% top (behind text)
- Atmosphere: single radial + linear gradient
- No constellation, no illustration, no AI art
- Typography carries the full composition

- `CVDisplayLinkCreateWithCGDisplay failed` warning is harmless on macOS
- File protocol (`file:///`) is blocked by the operator agent browser tooling. Use http.server.
- `--bind 127.0.0.1` is required; `0.0.0.0` may not resolve
- If server dies, restart with `pkill -f "http.server 8753"` then re-launch
