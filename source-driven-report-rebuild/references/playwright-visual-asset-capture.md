# Playwright CLI Visual Asset Capture for Reports

## When to use
When a report needs page screenshots embedded as local images (e.g. competitive landscape visuals, product homepage surveys), use the Playwright CLI to capture them. This works even when the Node.js `require('playwright')` API is not importable in the session environment.

## Prerequisites

```bash
# Install Chromium browser (one-time, ~280MB)
npx playwright install chromium
```

If the install warns about missing project dependencies, it still downloads the browser binary — proceed.

## Capture pattern

```bash
cd /path/to/report/directory
mkdir -p assets

# Single page screenshot
npx playwright screenshot \
  --browser chromium \
  --viewport-size '1440,2200' \
  --wait-for-timeout 4000 \
  https://example.com/ \
  assets/example-home.png
```

### Key flags
- `--viewport-size 'W,H'` — set large (1440×2200) for report-quality captures
- `--wait-for-timeout N` — milliseconds to wait for JS rendering before capture
- `--browser chromium` — use Chromium (most reliable for modern SPAs)
- `--full-page` — add only if you need the entire scrollable area

### Batch capture
Chain multiple captures in one command. Each is independent so a failure doesn't block the rest:

```bash
npx playwright screenshot --browser chromium --viewport-size '1440,2200' --wait-for-timeout 4000 https://site1.com/ assets/site1.png && \
npx playwright screenshot --browser chromium --viewport-size '1440,2200' --wait-for-timeout 4000 https://site2.com/ assets/site2.png
```

## Embedding in markdown source

```markdown
### Platform Name — Tagline

![Platform Homepage](assets/platform-home.png)

Key visible signals: brief annotation of what's visible on the page.
```

## Rebuilding the PDF with local images

```bash
pandoc master-report.md \
  --pdf-engine=weasyprint \
  --resource-path=. \
  -V margin-top=20mm -V margin-bottom=20mm \
  -o report.pdf
```

`--resource-path=.` is **critical** — without it, pandoc/weasyprint silently replaces images with alt text.

## Verifying images rendered

```python
from pypdf import PdfReader
r = PdfReader("report.pdf")
for i, p in enumerate(r.pages):
    t = p.extract_text() or ""
    if "Visual Survey" in t:
        print(f"Page {i+1}: {t[:200]}")
```

## Why not the Node API?

The `require('playwright')` / `import { chromium }` pattern fails if playwright is installed globally via npx but not as a local node_module. The CLI (`npx playwright screenshot`) works regardless because it resolves its own browser path.

## File sizes to expect

Typical homepage screenshots at 1440×2200:
- Simple pages: 300–500 KB
- Image-heavy pages: 800 KB–1.2 MB
- Budget ~5 MB total for a 5-platform visual survey

## Session: 2026-06-06
Used for 8D360 competitive landscape report — captured OpenEvidence, K Health, Ada Health, Glass Health, Hippocratic AI homepages.
