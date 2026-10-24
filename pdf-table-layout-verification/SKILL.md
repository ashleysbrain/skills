---
name: pdf-table-layout-verification
description: Build or repair PDF reports with wide tables, dense appendix sections, or markdown-generated content, then verify margin safety and readability using render-based inspection.
tags: [pdf, reportlab, tables, layout, verification, productivity]
version: 1.0.0
---

# PDF Table Layout Verification

Use this skill when a generated PDF has tables, dense appendices, schemas, markdown-heavy methodology content, or section-numbering/hierarchy issues that may overflow the page, clip at the right edge, render raw markdown markers, or become unreadable after compression.

## When to use
- A PDF report contains wide tables, dense appendix sections, schemas, or markdown-generated content that may overflow the page, clip at the right edge, render raw markdown markers, or become unreadable after compression
- The user reports clipping, margin overflow, text cut off at the right edge, cramped page layouts, awkward heading hierarchy, or numbering inconsistencies
- You need to rebuild a PDF and visually verify the output before delivery
- The source is Markdown, Python-generated report content, a custom document builder, or a multi-artifact document packet with a companion template file
- You need to confirm that both the table pages and the final appendix/template pages remain margin-safe and readable
- You are doing a cleanup pass that shortens headings, renumbers subsections, removes stray source artifacts, or forces a prompt/template section onto its own page before regenerating the PDF

## Core workflow
1. Inspect the source document and identify the widest tables.
2. Determine the PDF generation stack in use.
3. If using ReportLab, convert table cells to wrapped text objects instead of raw strings.
4. Compute column widths from the available page width.
5. Reduce table font size and paddings only as needed to preserve readability.
6. Rebuild the PDF.
7. Verify the rebuilt PDF with both text extraction and rendered-page inspection.
8. Deliver only after confirming no clipping, overflow, or footer loss.

## ReportLab repair pattern
Use this pattern when wide tables are produced with ReportLab:
- Wrap each cell in a `Paragraph` so text can wrap naturally
- Set explicit `colWidths` from the usable page width
- Use `VALIGN = TOP` so wrapped text stays readable
- Reduce paddings slightly instead of shrinking text aggressively
- Use `repeatRows=1` for long tables
- Prefer proportional widths for 4- and 5-column tables
- If needed, split very dense tables across multiple pages rather than forcing a single oversized row
- For markdown-heavy code blocks or fillable prompt templates, wrap long lines before inserting them into `Preformatted`/code sections so the last page does not clip at the right edge
- If code-heavy pages clip at the right edge, reduce the code font slightly and re-check the widest schema/template pages, not just the cover
- If a regenerated PDF still shows clipping in a schema block, shorten the source line or break the line before rebuilding

## Verification steps
Use at least one text-level and one visual check:
- Extract page text with `pymupdf` and confirm the expected table content is present
- Render the target pages to PNG and inspect them visually
- **Programmatic pixel audit (recommended for margin/overflow issues):** Use `scripts/pdf-pixel-audit.py` to objectively measure content extent, margin evenness, and page fill percentage per page. This catches overflow artifacts (pages with <15% content between two full pages = overflow from previous page) and asymmetric margins that vision models may miss or hallucinate. Usage: `python3 scripts/pdf-pixel-audit.py output.pdf 3` (single page) or `python3 scripts/pdf-pixel-audit.py output.pdf 2-4` (range).
- Check that table borders stay inside the page boundary
- Confirm the rightmost column is fully visible
- Confirm the footer or page number is still visible
- Inspect the widest table pages and the final appendix/template pages; do not verify only the cover page.
- For long rosters or agent catalogs, inspect both an early dense page and a late dense page. A layout can pass on the index page and still drift or clip later.
- For agent/profile cards, verify the card body, badges, and personality chips separately. Small chips can overflow even when the outer card fits.
- Confirm section numbering and heading hierarchy are consistent across page breaks (for example, 7.1 vs 7.7 vs 9.2).
- If the document contains markdown headings or mixed markdown/plain-text sections, verify that headings render as styled text rather than literal `###`/`####` markers.
- If the document has a companion prompt/template file, verify that separately as its own artifact rather than assuming the PDF covers it.
- If a user will print the PDF, default to a light background, dark text, and margins that survive physical printing.
- For diagram/whiteboard PDFs, verify that the *text sits fully inside each box* by checking the rendered result and, when possible, bounding boxes or text positions against the box geometry.
- If a regenerated PDF still shows clipping or cramped text, reduce line length, split the label into multiple lines, or shrink the font slightly before rebuilding.
- If a header, badge, or status chip is hard to read, treat contrast as a layout defect and re-render before delivery.
- Check header titles and small badges separately; large section headers can pass while the compact layer/model/family labels are still illegible.
- For combined technical report decks, verify both the narrative hierarchy and the final artifact path, not only table fit.
- For dense card lists or stacked examples, inspect rendered text blocks/coordinates on the target pages: a section can look fine in HTML while the PDF still splits into an unintended right-side column.
- When a heading is visually present but text search misses it, inspect the page blocks/coordinates before assuming the source edit failed; line breaks and badge layout can fragment the text layer.
- If the source intentionally keeps a family or section out of numeric order, preserve that order in layout but add a visible note explaining why.

See `references/pdf-self-audit-checklist.md`, `references/whiteboard-box-layout-audit.md`, and `references/agent-roster-layout-audit.md` for the compact pre-send checklist, the box-fit audit pattern, and the roster-specific verification notes.
## Self-audit before delivery
- Do not send a PDF until you have audited the final rendered artifact yourself
- Audit the exact file that will be delivered, not an earlier draft
- Check every page that contains dense content, not just the first page
- If the user mentioned print use, re-check contrast, margins, and background color specifically before delivery
- If any page looks crowded or borderline, revise and re-render before sending

See `references/pdf-self-audit-checklist.md` for the compact pre-send checklist.

## Practical repair heuristics
- If a column contains long prose, widen that column or shorten the label text
- If the table still feels crowded, shorten the header labels first
- Keep table fonts small but legible; do not over-shrink below readability
- Prefer wrapping over truncation
- Prefer fewer columns per table if the layout is too dense for a portrait page
- For mixed report sections, shorten long instruction lines or split them into separate lines before rebuilding the PDF

## Environment notes
- If `reportlab` is missing, install it with `uv pip install reportlab`
- If `pymupdf` is missing, install it with `uv pip install pymupdf`
- Use rendered-page image inspection when browser/PDF preview is available
- For premium compact reports, verify that the grouped blocks feel intentional: consistent card widths, strong hierarchy, and small but not cramped inter-card spacing
- If the user wants the page "blocked together," check that the content is visually stacked into modules rather than spread into a floating single-column essay layout
- **WeasyPrint without LaTeX (macOS):** macOS does not ship with pdflatex/xelatex. WeasyPrint (`pip install weasyprint markdown`) produces clean PDFs from markdown without any LaTeX dependency. Both packages are already in the the operator agent venv. Inline usage pattern for quick generation:
  ```python
  # Run via terminal: python3 -c "..."
  import markdown
  from weasyprint import HTML
  md = open('source.md').read()
  html = markdown.markdown(md, extensions=['extra','codehilite','tables'])
  # Wrap in styled HTML template, then:
  HTML(string=html_template).write_pdf('output.pdf')
  ```
  This is the fastest path from markdown to a professional PDF on macOS when ReportLab table-level control is not needed.

- **Chrome headless HTML→PDF (best for rich CSS layouts):** When the document uses CSS grid, flexbox, gradients, `@page` rules for cover pages, or complex multi-column layouts, WeasyPrint may render incorrectly (it lags Chromium on modern CSS). Chrome headless produces pixel-perfect output from a styled HTML file:
  ```bash
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
      --headless --disable-gpu --no-sandbox \
      --print-to-pdf=output.pdf \
      --print-to-pdf-no-header \
      "file:///absolute/path/to/source.html"
  ```
  Chrome handles `@page { size: A4; page-break-after: always }` for page breaks, `linear-gradient` for backgrounds, and CSS grid for card layouts. The errors about `CVDisplayLink` and `keychain` are harmless — ignore them.
  **When to use Chrome vs WeasyPrint:**
  - Chrome: cover pages with gradients, CSS grid card layouts, complex flexbox, `@page` pseudo-classes
  - WeasyPrint: simple markdown→PDF, when Chrome is not available, when you need programmatic control from Python
  - ReportLab: when you need precise table column width control, dynamic row generation from data
  **Post-generation QA:** Use `pymupdf` to extract page text and check for content issues (e.g., duplicate prefixes, missing data), then render pages to PNG for visual inspection. Fix issues in the HTML source and re-convert — do not try to patch the PDF directly for layout problems.

## Pitfalls
- Do not trust file size alone as proof of a good layout
- Do not assume a table fits just because the PDF renders
- Do not verify only the cover page; inspect the pages containing the widest tables
- Do not sacrifice readability just to keep everything on one page
- Do not skip the footer check on multi-page documents
- **WeasyPrint renders CSS Grid and Flexbox unreliably.** `display:grid` and `display:flex` with `align-items:center` can cause content to shrink-to-fit, shift sideways, or overflow past the page padding in WeasyPrint (confirmed v68.1). For multi-column layouts in WeasyPrint, use HTML `<table>` with explicit `width:N%` on each `<td>` — tables are the most bulletproof layout for PDF rendering. If you must use grid/flex, switch to Chrome headless instead.
- **"Page N formatting is broken" is often caused by page N-1 overflowing.** When a user reports ugly formatting on a specific page, the root cause is frequently the PREVIOUS page's content being too tall and bleeding onto the reported page as a partial strip. Always check the previous page's content height before debugging the reported page's CSS. Render ALL pages and scan their fill percentages — a page with <10% content sitting between two full pages is an overflow artifact, not a real page.
- **Do not rely on vision model subagents for layout analysis.** When the primary model lacks vision (or vision is unavailable), delegated subagents may hallucinate image content rather than admitting they cannot see it. Use programmatic pixel analysis (PIL + numpy) instead — it gives objective, reproducible measurements of margins, content extent, and overflow. See `scripts/pdf-pixel-audit.py`.

## Overlap notes
- `telegram-pdf-bundle-delivery` overlaps on PDF generation and Telegram delivery, but it focuses on WeasyPrint bundling, not table overflow repair
- `nano-pdf` overlaps on PDF editing, but it is for text edits rather than layout reconstruction
- `ocr-and-documents` overlaps on PDF inspection/extraction, but it does not cover table reflow and visual repair

## Output rule
When the repair is complete, return the final PDF path and, if relevant, the `MEDIA:` path for Telegram delivery.
