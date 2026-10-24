---
name: ocr-and-documents
description: "Extract text from PDFs/scans (pymupdf, marker-pdf). Compact/reduce page count via CSS-based reflow (markdown source) or N-up imposition (arbitrary PDF)."
version: 2.4.0
author: the operator agent Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [PDF, Documents, Research, Arxiv, Text-Extraction, OCR, Imposition, Compaction, PyMuPDF]
    related_skills: [powerpoint]
---

# PDF & Document Extraction

For DOCX: use `python-docx` (parses actual document structure, far better than OCR).
For PPTX: see the `powerpoint` skill (uses `python-pptx` with full slide/notes support).
This skill covers **PDFs and scanned documents**.

## Step 1: Remote URL Available?

If the document has a URL, **always try `web_extract` first**:

```
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])
web_extract(urls=["https://example.com/report.pdf"])
```

This handles PDF-to-markdown conversion via Firecrawl with no local dependencies.

Only use local extraction when: the file is local, web_extract fails, or you need batch processing.

## Step 2: Choose Local Extractor

| Feature | pymupdf (~25MB) | marker-pdf (~3-5GB) |
|---------|-----------------|---------------------|
| **Text-based PDF** | ✅ | ✅ |
| **Scanned PDF (OCR)** | ❌ | ✅ (90+ languages) |
| **Tables** | ✅ (basic) | ✅ (high accuracy) |
| **Equations / LaTeX** | ❌ | ✅ |
| **Code blocks** | ❌ | ✅ |
| **Forms** | ❌ | ✅ |
| **Headers/footers removal** | ❌ | ✅ |
| **Reading order detection** | ❌ | ✅ |
| **Images extraction** | ✅ (embedded) | ✅ (with context) |
| **Images → text (OCR)** | ❌ | ✅ |
| **EPUB** | ✅ | ✅ |
| **Markdown output** | ✅ (via pymupdf4llm) | ✅ (native, higher quality) |
| **Install size** | ~25MB | ~3-5GB (PyTorch + models) |
| **Speed** | Instant | ~1-14s/page (CPU), ~0.2s/page (GPU) |

**Decision**: Use pymupdf unless you need OCR, equations, forms, or complex layout analysis.

If the user needs marker capabilities but the system lacks ~5GB free disk:
> "This document needs OCR/advanced extraction (marker-pdf), which requires ~5GB for PyTorch and models. Your system has [X]GB free. Options: free up space, provide a URL so I can use web_extract, or I can try pymupdf which works for text-based PDFs but not scanned documents or equations."

---

## pymupdf (lightweight)

```bash
pip install pymupdf pymupdf4llm
```

**Via helper script**:
```bash
python scripts/extract_pymupdf.py document.pdf              # Plain text
python scripts/extract_pymupdf.py document.pdf --markdown    # Markdown
python scripts/extract_pymupdf.py document.pdf --tables      # Tables
python scripts/extract_pymupdf.py document.pdf --images out/ # Extract images
python scripts/extract_pymupdf.py document.pdf --metadata    # Title, author, pages
python scripts/extract_pymupdf.py document.pdf --pages 0-4   # Specific pages
```

**Inline**:
```bash
python3 -c "
import pymupdf
doc = pymupdf.open('document.pdf')
for page in doc:
    print(page.get_text())
"
```

---

## marker-pdf (high-quality OCR)

```bash
# Check disk space first
python scripts/extract_marker.py --check

pip install marker-pdf
```

**Via helper script**:
```bash
python scripts/extract_marker.py document.pdf                # Markdown
python scripts/extract_marker.py document.pdf --json         # JSON with metadata
python scripts/extract_marker.py document.pdf --output_dir out/  # Save images
python scripts/extract_marker.py scanned.pdf                 # Scanned PDF (OCR)
python scripts/extract_marker.py document.pdf --use_llm      # LLM-boosted accuracy
```

**CLI** (installed with marker-pdf):
```bash
marker_single document.pdf --output_dir ./output
marker /path/to/folder --workers 4    # Batch
```

---

## Arxiv Papers

```
# Abstract only (fast)
web_extract(urls=["https://arxiv.org/abs/2402.03300"])

# Full paper
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])

# Search
web_search(query="arxiv GRPO reinforcement learning 2026")
```

## Split, Merge & Search

pymupdf handles these natively — use `execute_code` or inline Python:

```python
# Split: extract pages 1-5 to a new PDF
import pymupdf
doc = pymupdf.open("report.pdf")
new = pymupdf.open()
for i in range(5):
    new.insert_pdf(doc, from_page=i, to_page=i)
new.save("pages_1-5.pdf")
```

```python
# Merge multiple PDFs
import pymupdf
result = pymupdf.open()
for path in ["a.pdf", "b.pdf", "c.pdf"]:
    result.insert_pdf(pymupdf.open(path))
result.save("merged.pdf")
```

```python
# Search for text across all pages
import pymupdf
doc = pymupdf.open("report.pdf")
for i, page in enumerate(doc):
    results = page.search_for("revenue")
    if results:
        print(f"Page {i+1}: {len(results)} match(es)")
        print(page.get_text("text"))
```

No extra dependencies needed — pymupdf covers split, merge, search, and text extraction in one package.

---

## Compact / Reduce Page Count

When the user wants to reduce the page count of an existing PDF without deleting any content — typically by tightening margins and/or using smaller fonts — choose the approach based on whether the **markdown source** is available.

### Method A: CSS-based compaction (markdown source available) ★ PREFERRED

When the source markdown is available (or can be extracted cleanly), rebuild the PDF with compact CSS via `pandoc → weasyprint`. This produces **readable, properly reflowed output** at 7–8pt body fonts instead of the 4–5pt fonts you get from N-up imposition. Typical reduction: 60–65% fewer pages.

**Pipeline:**
```bash
cd /path/to/report/directory  # MUST be in the assets directory
pandoc source.md -f markdown+pipe_tables -t html5 \
  --standalone --embed-resources \
  --metadata "title=Report Title" \
  > /tmp/compact.html
# Inject compact CSS (see template below) into <head>
weasyprint /tmp/compact.html output-compact.pdf
```

**Compact CSS template** (proven for 210→78 page reduction):
```css
@page { size: letter; margin: 0.4in 0.5in 0.4in 0.5in; }
body { font-family: 'Hiragino Sans','Helvetica Neue',Arial,sans-serif;
       font-size: 7.5pt; line-height: 1.25; color: #1a1a1a; }
h1 { font-size: 13pt; margin-top: 12pt; margin-bottom: 4pt; font-weight: 700;
     color: #0d1b2a; border-bottom: 1.5pt solid #0d1b2a; padding-bottom: 3pt; }
h2 { font-size: 10pt; margin-top: 10pt; margin-bottom: 3pt; font-weight: 700;
     color: #1b263b; }
h3 { font-size: 8.5pt; margin-top: 8pt; margin-bottom: 2pt; font-weight: 700;
     color: #415a77; }
p { margin-top: 2pt; margin-bottom: 2pt; }
ul, ol { margin-top: 2pt; margin-bottom: 2pt; padding-left: 14pt; }
li { margin-bottom: 1pt; }
blockquote { margin: 4pt 0; padding: 3pt 8pt; border-left: 2pt solid #415a77;
             background: #f8f9fa; font-size: 7pt; }
table { border-collapse: collapse; width: 100%; margin: 3pt 0; font-size: 7pt; }
th { background: #0d1b2a; color: white; padding: 2pt 4pt; font-weight: 700;
     text-align: left; }
td { padding: 2pt 4pt; border-bottom: 0.5pt solid #ddd; vertical-align: top; }
img { max-width: 100%; max-height: 120pt; margin: 3pt 0; }
hr { border: none; border-top: 0.5pt solid #ccc; margin: 6pt 0; }
```

**Single-page target variant:** When the document must fit on exactly one page (product theses, one-pagers, executive summaries), write custom HTML directly instead of going through pandoc. This gives full control over spacing. Pipeline:

```bash
# 1. Write content as MD (source of truth)
# 2. Create custom styled HTML (not pandoc output) with tight parameters
# 3. Convert
weasyprint document.html document.pdf
# 4. Verify page count
python3 -c "import fitz; doc=fitz.open('document.pdf'); print(f'Pages: {len(doc)}')"
# 5. If >1 page: tighten CSS (reduce font-size, margins, line-height) and/or condense content
# 6. Re-run and re-verify
```

Proven single-page CSS parameters (letter size, ~4,500 chars content):
```css
@page { size: letter; margin: 0.45in 0.55in; }
body { font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif;
       font-size: 7.8pt; line-height: 1.32; color: #1a1a1a; }
h1 { font-size: 14pt; margin: 0 0 0.05em 0; font-weight: 700; }
h2 { font-size: 9pt; margin: 0.6em 0 0.15em 0; text-transform: uppercase;
     letter-spacing: 0.5pt; }
p { margin: 0.25em 0; }
blockquote { margin: 0.25em 0; padding: 0.3em 0.7em; border-left: 2.5pt solid #333;
             background: #f7f7f7; font-size: 7.5pt; }
```

**Key parameters to tune:**
- `@page margin`: 0.4–0.5in is the sweet spot (down from default ~1in)
- `body font-size`: 7–8pt is readable; below 7pt strains eyes
- `table font-size`: 7pt minimum for tables
- `img max-height`: 100–140pt keeps images from dominating pages
- `line-height`: 1.2–1.25 keeps density without cramping
- For single-page: 0.45in margins + 7.8pt body + 1.32 line-height fits ~4,500 chars on letter

**Critical:** Run `pandoc` and `weasyprint` from the directory containing `assets/` so local images resolve correctly. Use `--resource-path=.` if needed.

**Verify:** After generation, check page count with PyMuPDF and spot-check font sizes on a middle page.

### Method B: N-up imposition (arbitrary PDF, no source)

When only the PDF is available (no markdown source), use N-up imposition via PyMuPDF `show_pdf_page()`. This preserves all visual content exactly — images, formatting, layout — just at smaller scale.

### Step 1: Analyze the source PDF

```python
import fitz
doc = fitz.open("source.pdf")
print(f"Pages: {doc.page_count}, Size: {doc[0].rect}")

# Check font sizes and image presence
for i in [0, doc.page_count // 2, doc.page_count - 1]:
    page = doc[i]
    sizes = set()
    for b in page.get_text("dict")["blocks"]:
        if b["type"] == 0:
            for line in b["lines"]:
                for span in line["spans"]:
                    sizes.add(round(span["size"], 1))
    has_images = bool(page.get_images())
    print(f"Page {i}: fonts={sorted(sizes)}, images={has_images}")

# Count pages with images
img_pages = sum(1 for i in range(doc.page_count) if doc[i].get_images())
print(f"Pages with images: {img_pages}/{doc.page_count}")
doc.close()
```

### Step 2: Choose the approach

- **Mostly text, no images**: Extract text and re-render at smaller font with tighter margins (true reflow). Works well for pure-text documents.
- **Has images or complex layout**: Use **N-up imposition** via `show_pdf_page()`. This preserves all visual content exactly — images, formatting, layout — just at smaller scale.

### Step 3: N-up imposition pattern (2-up)

Place two source pages side-by-side on a larger output page:

```python
import fitz
doc = fitz.open("source.pdf")
new_doc = fitz.open()

src_w, src_h = doc[0].rect.width, doc[0].rect.height
# Output page: A3 landscape for landscape source, or adjust accordingly
out_w, out_h = 1190.55, 841.89  # A3 landscape

col_w = out_w / 2
scale = min(col_w / src_w, out_h / src_h)
margin = 12

for i in range(0, doc.page_count, 2):
    new_page = new_doc.new_page(width=out_w, height=out_h)
    scaled_w = src_w * scale
    scaled_h = src_h * scale
    y_off = (out_h - scaled_h) / 2

    # Left page
    rect_left = fitz.Rect(margin, y_off, margin + scaled_w, y_off + scaled_h)
    new_page.show_pdf_page(rect_left, doc, i)

    # Right page (if exists)
    if i + 1 < doc.page_count:
        x_start = out_w / 2 + margin / 2
        rect_right = fitz.Rect(x_start, y_off, x_start + scaled_w, y_off + scaled_h)
        new_page.show_pdf_page(rect_right, doc, i + 1)

new_doc.save("output.pdf", garbage=4, deflate=True)
new_doc.close()
doc.close()
```

### Method B: Font size and readability guide

| N-up | Output size | Scale | 7pt body → | Readability |
|------|-------------|-------|------------|-------------|
| 2-up | A3 landscape | 0.71 | 5.0pt | Screen OK at zoom; tight for print |
| 2-up | B2 landscape | 0.84 | 5.9pt | Good for screen and large-format print |
| 2-up | Same size | 0.50 | 3.5pt | ❌ Unreadable |

- **5pt minimum** for laser printing, **7pt** for comfortable screen reading
- Always calculate and report the effective font size range
- If the source already uses small fonts (≤7pt), a 2-up A3 may be borderline — warn the user

### Step 4: Verify

```python
# Check effective font sizes on output
out = fitz.open("output.pdf")
page = out[5]  # sample a middle page
for b in page.get_text("dict")["blocks"]:
    if b["type"] == 0:
        for line in b["lines"]:
            for span in line["spans"]:
                print(f"  {span['size']:.1f}pt: {span['text'][:40]}")
out.close()
```

### Method B Pitfalls
- Do NOT attempt text reflow when pages contain images — the images and layout will be lost
- `show_pdf_page()` is the correct PyMuPDF method for imposition; do not use `insert_pdf()` (it doesn't scale)
- On macOS, use `mdls -name kMDItemNumberOfPages file.pdf` to quickly get page counts without Python
- If Python heredocs in `terminal()` fail with "Could not determine home directory", prefix with `HOME=/<home>` or `cd /tmp`

### Single-page target (custom HTML, bypass pandoc)

When the document must fit on exactly one page (product theses, one-pagers, executive summaries), write custom HTML directly instead of going through pandoc. This gives full control over spacing.

**Pipeline:**
```bash
# 1. Write content as MD (source of truth)
# 2. Create custom styled HTML with tight parameters (not pandoc output)
# 3. Convert
weasyprint document.html document.pdf
# 4. Verify page count with PyMuPDF
python3 -c "import fitz; doc=fitz.open('document.pdf'); print(f'Pages: {len(doc)}')"
# 5. If >1 page: tighten CSS (reduce font-size, margins, line-height) and/or condense prose
# 6. Re-run and re-verify
```

**Proven single-page CSS** (letter size, ~4,500 chars content):
```css
@page { size: letter; margin: 0.45in 0.55in; }
body { font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif;
       font-size: 7.8pt; line-height: 1.32; color: #1a1a1a; }
h1 { font-size: 14pt; margin: 0 0 0.05em 0; font-weight: 700; }
h2 { font-size: 9pt; margin: 0.6em 0 0.15em 0; text-transform: uppercase;
     letter-spacing: 0.5pt; }
p { margin: 0.25em 0; }
blockquote { margin: 0.25em 0; padding: 0.3em 0.7em; border-left: 2.5pt solid #333;
             background: #f7f7f7; font-size: 7.5pt; }
```

### Method A Pitfalls
- **Must run from assets directory**: pandoc resolves `![](assets/img.png)` relative to cwd. Running from the wrong directory silently drops all images to alt text.
- **CSS specificity**: if the HTML has inline styles or the pandoc template injects its own font sizes, the compact CSS may be overridden. Use `!important` on body/h1/h2/h3 font-size if needed.
- **File size bloat**: compact PDFs with full-resolution images will be larger than N-up (30MB vs 1.2MB for a 210-page report). This is the trade-off for readable fonts.
- **Table overflow**: very wide tables may clip at 7pt + tight margins. Increase `@page` margin or add `overflow-wrap: break-word; word-break: break-word;` to `td`.

---

## Notes

- `web_extract` is always first choice for URLs
- pymupdf is the safe default — instant, no models, works everywhere
- marker-pdf is for OCR, scanned docs, equations, complex layouts — install only when needed
- Both helper scripts accept `--help` for full usage
- marker-pdf downloads ~2.5GB of models to `~/.cache/huggingface/` on first use
- For Word docs: `pip install python-docx` (better than OCR — parses actual structure)
- For PowerPoint: see the `powerpoint` skill (uses python-pptx)
- Handbook/document rebuild workflow details: `references/handbook-revision-pipeline.md`
- Compact CSS pipeline (markdown→PDF page reduction): `references/compact-pdf-from-markdown-pipeline.md`
