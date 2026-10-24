---
name: print-friendly-pdf-ocg
description: Add a print/screen auto-switch to any styled (dark-background, light-text) PDF using PDF Optional Content Groups (OCGs). One file shows full design on screen, auto-switches to ink-saving white-on-print with no user action. Includes the dual-PDF WeasyPrint fallback for viewers that ignore OCG PrintState, plus ink-coverage measurement for verification.
version: 1.0.0
---

# Print-Friendly PDF via OCG Layers

Make dark/colored-background PDFs print-friendly without sacrificing the
on-screen design. The user loves the styled backgrounds for screen reading
but wants ink/toner savings (~90%) when printing.

## TL;DR — it is already automatic for standard generators

Both canonical PDF generators auto-produce a `-PRINT.pdf` alongside the
screen PDF on every run, via the shared module
`~/your-workspace/ds-wave-shared/scripts/print_friendly.py`.

- **`scripts/ds-pdf.py`** — markdown → styled PDF (Fleet Atlas CSS)
- **`ds-wave-shared/scripts/generate-pdf.py`** — advisory board PDFs

You do not need to run anything manually for these — the print version
ships for free. See "Pipeline Integration" below for wiring a new generator.

The standalone OCG tool (`docs/make_print_smart.py`) is for heavy atlas
HTML sources that need the single-file auto-switch, or for retro-fitting
an existing PDF that has no HTML source.

> **WARNING:** A prior session documented build scripts (`build_master_atlas.py`,
> `build_atlas.py`, `build_tech_atlas.py`, `render_ds_pdf.py`) that were
> **never actually created on disk**. Do not look for or call these files.
> The real integration is `print_friendly.py` + the two generators above.

## When to Use

- User asks for a "print-friendly" or "printer-friendly" version of a
  styled PDF.
- User wants one PDF that auto-switches when printed (no separate file).
- User wants to reduce ink/toner consumption on a dark-background document.
- User asks to "make this not waste ink when I print it."

## The Core Problem

Styled PDFs (dark teal backgrounds, gold accents, white text) look great on
screen but are catastrophically expensive to print: 56-59% ink coverage per
page vs. 5-8% for a normal document. The naive fix (just hide backgrounds)
creates a SECOND failure: white text on white paper — invisible.

The hybrid OCG technique solves both problems in a single file.

## Two Approaches (use both)

| Approach | Output | Ink cut | Reliability |
|----------|--------|---------|-------------|
| **OCG auto-switch** (primary) | 1 file | ~91% | Adobe/Foxit/Chrome: full auto-switch. macOS Preview: ignores PrintState. |
| **Dual-PDF fallback** | 2 files | ~87% | Universal — works in every viewer. |

Always produce BOTH. The OCG file is the elegant default; the standalone
`-PRINT.pdf` is the safety net for Preview users and enterprise print queues.

## The Hybrid OCG Technique (3 layers)

A single PDF gets 3 Optional Content Groups injected into its content stream:

1. **Screen Backgrounds** — all drawing ops before the first `BT` (Begin Text)
   on each page. View=ON, Print=OFF. This captures ~91% of background fills
   (gradients, rectangles, shading) because backgrounds are drawn before text.
2. **Screen Text (light colors)** — every `BT...ET` text block whose active
   fill color is light (brightness > 0.65 on the 0-1 RGB luminance scale).
   View=ON, Print=OFF. Hides the original white/gold text that would be
   invisible without its dark background.
3. **Print Text (dark equivalents)** — dark-color duplicates of every light
   text block, inserted alongside the original. View=OFF, Print=ON. Replaces
   the hidden light text with legible dark text on the now-white background.

Result: screen mode is pixel-identical to the original; print mode drops to
~5% ink coverage with all text fully legible.

### Why the naive OCG fails (and why the hybrid is needed)

A simple "wrap backgrounds in one OCG with Print=OFF" approach achieves the
ink cut but leaves 100+ light-text spans (white `#ffffff`, gold `#ffd700`)
invisible on white paper. OCGs can show/hide content but **cannot recolor**
existing text. The hybrid solves this by duplicating each light-text block
with a darkened color in a separate print-only layer.

### Color Darkening Rules

Map light colors to dark equivalents for the print-text duplicates:

| Screen color | Print equivalent | Hex |
|---|---|---|
| White (`#ffffff`) | Dark teal | `#0a3b3b` |
| Gold (`#ffd700`) | Dark amber | `#806000` |
| Light teal-green (`#4ad6b4`) | Dark teal | `#0a3b3b` |
| Other light tints | Proportional 0.3x darkening | varies |

Brightness threshold for "light" (needs duplication): luminance > 0.65
where luminance = `0.299*R + 0.587*G + 0.114*B` on 0-1 scale.

## Architecture: Built Into the Generator, NOT Post-Processed

**The user was explicit (2026-06-20):** "this shouldn't be a cron to update
created PDFs... this needs to be built into the pdf creator from the start."

The print-friendly PDF is produced at **creation time**, inside the
generator, not as a post-hoc step, cron job, or manual second pass.

### How it works

Each generator renders its HTML to a screen PDF via WeasyPrint, then calls
`render_print_pdf()` from the shared module to render the same HTML again
with CSS-variable-overridden pure-white backgrounds:

```python
from print_friendly import render_print_pdf, print_path_for
render_print_pdf(html_string, print_path_for(output_pdf_path))
```

The `inject_print_css()` function overrides ALL design-token CSS variables
(`--cream`, `--surface`, `--card`, `--bg`, etc.) to `#ffffff` at `:root`
FIRST, then kills all backgrounds via `!important`. This double-punch is
required because generic `background: white !important` alone does not
catch `var()` references in WeasyPrint.

**Wired generators** (all produce `-PRINT.pdf` automatically):
- `scripts/ds-pdf.py` → any markdown document
- `ds-wave-shared/scripts/generate-pdf.py` → advisory board PDFs

**OCG injection** (the `make_print_smart.py` CLI) is for heavy atlas HTML
that needs the single-file auto-switch, or as a recovery tool for PDFs
that have no HTML source. It is never the default path for standard docs.

### The CSS-variable override (why naive stripping fails)

DS documents use design tokens: `--cream: #faf8f3`, `--surface: #f5f2ea`,
`--card: #eee9dc`, plus a body `linear-gradient(#f5f2ea, #faf8f3, #f5f2ea)`.
These are ~95-97% brightness — nearly invisible on screen but they cover
85%+ of every page and burn toner. A generic `* { background: white !important }`
rule does NOT catch them because WeasyPrint resolves `var()` at render time.

The fix (in `generate_print_pdf()`): override the variables at `:root` FIRST,
then kill all backgrounds. Verified: tint coverage drops from 84.8% → 0.04%.

## Verification: Measuring Ink Coverage

Never claim ink savings without measuring. The method:

```python
# 1. Render PDF pages to PNG at 72 dpi
subprocess.run(["pdftoppm", "-png", "-r", "72", pdf_path, prefix])

# 2. Count non-white pixels per page, sum
from PIL import Image; import numpy as np
arr = np.array(Image.open(png).convert("L"))
ink_pct = (arr < 245).sum() / arr.size * 100
```

For OCG verification (since you can't "print" to measure), create a
**print-simulation** variant: set `BaseState=OFF` and selectively turn ON
only the print-text OCG, then measure that rendered PDF. If screen-mode
renders ~56% ink and print-sim renders ~5%, the OCG is working.

Also verify text legibility: scan all text spans via PyMuPDF
(`page.get_text("dict")`), extract color, flag any with brightness > 180
that would be invisible on white. The hybrid should produce ZERO such spans
in print mode.

## Viewer Compatibility

| Viewer | OCG PrintState | Recommendation |
|---|---|---|
| Adobe Acrobat / Reader | Full support | OCG file works perfectly |
| Foxit Reader | Full support | OCG file works perfectly |
| Chrome / Firefox built-in PDF | Respects print intent | OCG file works |
| macOS Preview | Ignores PrintState | Use the `-PRINT.pdf` fallback |

## Tools Required

```
pip install pikepdf pymupdf weasyprint
# Also needs: pdftoppm (poppler), PIL/Pillow
```

pikepdf for OCG injection (content-stream manipulation), PyMuPDF (fitz) for
text-span analysis and ink diagnostics, WeasyPrint for HTML-regeneration
fallback, pdftoppm + PIL for ink-coverage measurement.

## Pipeline Integration (ALL future PDFs — built into generators)

Print-friendly is **built into the PDF generators**, not a post-processing step.

**Shared module: `~/your-workspace/ds-wave-shared/scripts/print_friendly.py`**

Exports:
- `inject_print_css(html)` — returns HTML with aggressive print CSS
- `render_print_pdf(html, output_path)` — renders pure-white PDF
- `generate_dual_pdf(html, screen_path, print_path)` — renders BOTH
- `print_path_for(screen_path)` — derives `-PRINT.pdf` from screen path

### Generators wired (auto-produce `-PRINT.pdf` with every run)

1. **`scripts/ds-pdf.py`** — markdown → styled PDF (Fleet Atlas CSS)
2. **`ds-wave-shared/scripts/generate-pdf.py`** — advisory board PDFs

Every `ds-pdf.py input.md output.pdf` now also produces `output-PRINT.pdf`.
No extra flags, no cron, no separate step.

### Wiring a new generator

```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ds-wave-shared', 'scripts'))
from print_friendly import render_print_pdf, print_path_for
render_print_pdf(html_string, print_path_for(output_path))
```

### For heavy atlas HTML (standalone, needs OCG)

```bash
python3 ~/your-workspace/docs/make_print_smart.py SOURCE.html \
    -o OUTPUT-SMART.pdf --also-print-pdf
```

## Step-by-Step Workflow (one-off / retro-fit only)

For a document that did NOT go through a build script (so the auto-pipeline
didn't already produce a print version), or to retro-fit an existing PDF:

1. **Locate source** — find the PDF AND its HTML source if one exists.
2. **Prefer `make_print_smart.py`** — it does screen PDF + print PDF + the
   OCG layers in one step:
   ```bash
   python3 docs/make_print_smart.py any-document.html -o OUTPUT-SMART.pdf --also-print-pdf
   ```
3. **If you only have a finished PDF (no HTML)** — use `make_print_smart.py`
   to inject OCG layers directly. The standalone `-PRINT.pdf` fallback is
   NOT possible without HTML (the var()-aware CSS override needs the source),
   so for a Preview user you must obtain the HTML.
4. **Verify pure-white yourself** — never trust the render. The helper
   auto-checks page-1 `#ffffff` ratio; for OCG files, also run
   `scripts/verify_print_smart.py` (4-check probe: structure, screen
   fidelity, ink reduction, text-preservation word-count invariant).
5. **Deliver** — `*.pdf` (screen) + `*-PRINT.pdf` (print). For macOS Preview
   users, the `-PRINT.pdf` IS the deliverable; the `-SMART.pdf`/OCG file is
   the optional companion (only auto-switches in Adobe/Foxit/Chrome).

## Validated Results (2026-06-20, independently re-verified same day)

These numbers were re-measured with `scripts/verify_print_smart.py` on
2026-06-20, not just self-reported. The table is a snapshot — if you touch
the PDF or the script, re-run the probe rather than citing these figures.

| Document | Pages | Light-text | Print ink cut (poppler) | (ghostscript) | Screen diff |
|----------|-------|-----------|------------------------|---------------|-------------|
| DS-FLEET-ATLAS | 35 | 261 | 91% | 94% | 0.0% |
| DS-Master-Atlas | 125 | 0 | 60% | 70% | 0.0% |
| DS-Complete-Neuroscience-Atlas | 80 | 0 | 61% | 72% | 0.0% |

Lower reduction on Master/Neuroscience is correct: they have less background
coverage (30% original ink vs 56%) and use dark/medium text (no light-text
wrapping needed). Remaining ink is legitimate content. All three: 0 invisible
spans, 100% text content preserved in print-sim (verified via pdftotext).

## Two-Engine Validation (always use both)

Never trust a single renderer for ink measurement — poppler and ghostscript
have different rasterization paths and can disagree. Render the
print-simulation PDF with BOTH and confirm they agree on the delta (absolute
percentages will differ; the reduction percentage should be in the same band):

```python
def measure(path, engine):
    if engine == "poppler":
        subprocess.run(["pdftoppm","-png","-r","72",path,prefix], check=True)
    else:  # ghostscript
        subprocess.run(["gs","-dQUIET","-dBATCH","-dNOPAUSE","-r72",
                        "-sDEVICE=pnggray",f"-sOutputFile={prefix}-%02d.png",path], check=True)
    # count non-white pixels across all rendered pages
```

The print-simulation is created by flipping OCG states to exactly what a
spec-compliant printer does (read Usage hints, set visibility config):

```python
pdf = pikepdf.open(smart_pdf)
d = pdf.Root.OCProperties.D
d.BaseState = pikepdf.Name.OFF
d.ON  = [oc.OCGs[2]]           # print-text visible
d.OFF = [oc.OCGs[0], oc.OCGs[1]]  # backgrounds + screen text hidden
pdf.save(print_sim_path)
```

Also cross-check text with `pdftotext` (poppler's text extractor) — PyMuPDF
may return 0 spans from OCG-wrapped pages even when text renders correctly
(it struggles with BDC/EMC markers). If `pdftotext` extracts full text,
the rendering is correct and the PyMuPDF 0 is a parser limitation, not real
text loss.

## Pitfalls

- **PHANTOM FILE REFERENCES: verify skill self-reports against the
  filesystem.** A prior session documented build scripts
  (build_master_atlas.py, build_atlas.py, render_ds_pdf.py,
  make_all_print_friendly.py) and a cron job that were never actually
  created on disk. The skill read as if the integration was complete, but
  none of the referenced files existed. Before acting on a skill claim
  that something is already wired, run search_files for the named files.
  If they do not exist, the skill is describing an aspirational state, not
  reality. This was caught and fixed 2026-06-20; the real integration is
  print_friendly.py + ds-pdf.py + generate-pdf.py.
- **Cover gradients are shading objects, not vector fills.** The "wrap
  everything before the first BT" heuristic misses PDF shading objects on
  cover pages. Check the content stream for `/Pattern cs` or shading
  operators. If found, the cover background won't be suppressed by OCG —
  the dual-PDF fallback handles it correctly.
- **Content stream encoding.** Read raw bytes and decode as `latin-1`
  (not UTF-8) — PDF content streams are byte-oriented, and UTF-8 decoding
  corrupts high-byte operators.
- **Page.Contents may be an array.** Some PDFs split content across
  multiple streams. Join them before parsing, or handle each separately.
- **macOS Preview is the #1 user complaint.** It ignores OCG PrintState
  entirely. Always ship the `-PRINT.pdf` fallback alongside the SMART file.
  Tell the user explicitly which file to use in Preview.
- **CSS VARIABLES defeat naive background stripping (the "still off-white"
  bug).** DS documents use design tokens: `--cream: #faf8f3`,
  `--surface: #f5f2ea`, `--card: #eee9dc`. These are ~95-97% brightness —
  barely visible on screen but they cover 85%+ of every page and burn toner.
  The body background is typically a `linear-gradient(#f5f2ea, #faf8f3,
  #f5f2ea)` covering the WHOLE page. A generic `* { background: white
  !important }` rule does NOT catch either of these because WeasyPrint
  resolves `var()` at render time. The fix: override the variables at
  `:root` FIRST, then kill all backgrounds AND background-image. The
  script's `generate_print_pdf()` already does this — if extending it for a
  new document, add that document's token names to the `:root` override
  block. Verified result: tint coverage drops from 84.8% → 0.04%.
  Detection: render page 1 of the output and measure the `#ffffff` pixel
  ratio — if <95% pure white, the var() override is missing. Do NOT trust
  the aggregate ink% metric alone; it can read "improved" while the page is
  still cream-tinted. See `references/tint-coverage-diagnostic.md` for the
  pixel-level tint-measurement technique that catches this reliably.
- **BT/ET nesting.** BT...ET blocks don't nest in well-formed PDFs, but
  some generators produce malformed streams. The regex-based parser assumes
  no nesting — verify on your specific PDF.
- **Don't recolor inline — duplicate.** Never modify the original text
  block's color in place. Create a dark duplicate in the print OCG and hide
  the original in the screen OCG. Both layers must be present so screen
  mode stays pixel-identical.
- **CRITICAL: The `rg` injection bug.** The fill-color `rg` operator that
  set the original light text color lives OUTSIDE the BT block — it's in
  the shared graphics state (often inside the background OCG wrapper).
  Trying to darken the duplicate by replacing an `rg` *inside* the BT
  block finds nothing and produces a **byte-identical duplicate that stays
  light** — invisible on white paper in print mode. This is a silent
  failure: the script reports "Light-text wrapped: N" (correct detection)
  but the dark duplicates never render. Fix: inject an explicit dark `rg`
  as the FIRST operator after `BT`:

  ```python
  # WRONG — finds no rg inside BT, duplicate stays light:
  dark_block = re.sub(r'[\d.]+\s+[\d.]+\s+[\d.]+\s+rg', dark_color, original, count=1)

  # CORRECT — inject dark rg right after BT:
  dark_block = re.sub(r'\bBT\b', f'BT\n{dark_color_str}', original, count=1)
  ```

  **Detection:** render a print-simulation and check the title region of a
  page with known light text. If ink is ~0% there and `pdftotext` extracts
  nothing, the dark duplicates aren't rendering — the bug is present.
  Confirm by checking the content stream for a dark `rg` right after BT
  inside the DPtxt wrapper:
  ```python
  re.search(r'/OC /DPtxt BDC\s+BT\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+rg', data)
  ```

## Batch Processing (for existing PDFs without HTML source)

If you need to retro-fit print-friendly onto existing PDFs that were
generated before the pipeline integration, run `make_print_smart.py`
on each one. There is no batch script — this is a one-time retro-fit,
not a recurring operation.

```bash
for pdf in ~/Desktop/*.pdf; do
    python3 ~/your-workspace/docs/make_print_smart.py "$pdf" \
        -o "${pdf%.pdf}-SMART.pdf" --verify
done
```

> **WARNING:** The user explicitly rejected cron-as-primary-approach
> (2026-06-20): "this shouldn't be a cron to update created PDFs... this
> needs to be built into the pdf creator from the start." The primary
> mechanism is `print_friendly.py` wired into every generator.
> Never propose a cron job as the solution to "make PDFs print-friendly."

## Scripts

- `scripts/make_print_smart.py` — Reusable CLI that takes a PDF (or HTML)
  and produces the OCG auto-switch file. Supports `--also-print-pdf` for
  the dual-PDF fallback and `--verify` to confirm OCG structure.
- `scripts/verify_print_smart.py` — Independent 4-check verification probe.
  Given `original.pdf` + `smart.pdf`, confirms OCG structure, screen
  fidelity, print ink reduction, AND text preservation (word-count
  invariant). Run this instead of trusting the "Validated Results" table
  below — that table is a claim, this script is proof. Exits 0/1.
- **`~/your-workspace/ds-wave-shared/scripts/print_friendly.py`** — Shared
  module imported by `ds-pdf.py` and `generate-pdf.py` to auto-produce
  `-PRINT.pdf`. Exports `inject_print_css()`, `render_print_pdf()`,
  `generate_dual_pdf()`, `print_path_for()`. This is the canonical
  integration point for wiring new generators.

## Related Skills

- `ds-fleet-atlas-update-via-davinci` — the specialist engine generation. References
  this skill for the print-friendly output step.
- `pdf-table-layout-verification` — Wide-table PDF layout verification.
- `ocr-and-documents` — Text extraction and page reduction (different
  concern: reducing content, not print ink).
