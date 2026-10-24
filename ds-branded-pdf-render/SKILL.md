---
name: ds-branded-pdf-render
description: ALWAYS render PDFs through the specialist engine brand (navy/teal/gold). For markdown-heavy docs use scripts/ds-md-to-pdf.py (preserves tables + code blocks). For simple section docs use the specialist engine API. NEVER use generic /tmp render scripts.
---

# the specialist engine PDF Render Gate

## The Rule (read BOTH parts)

Every PDF that reaches the principal or her team MUST use the the specialist engine brand palette (deep navy #0a1e2e, dark teal #0d3b3b, gold #ffd700, bright teal #4ad6b4, golden ratio proportion). No exceptions.

**CRITICAL: Generate PDFs ONLY when the principal explicitly asks.** Do NOT auto-render every spec, analysis, or output through the creative process flow. Deliver answers directly in the chat (Telegram, the operator agent, wherever the conversation is). PDF rendering is ON-REQUEST, not default.

**User correction (2026-07-07):** "I don't need you to send me a PDF for every output. This is a lot of PDFs and it's overkill. We don't need to generate this many. So when I ask you to generate a PDF, be ready. But until I ask you, you don't need to."

**User correction (2026-07-07, THIRD TIME same session):** After being told twice, the agent continued auto-rendering PDFs for every output (isomorphism analysis, partnership strategy, etc.). The rule is absolute: NO PDF unless the user says "PDF," "render this," "send me the document," or equivalent. The creative process flow does not fire unless explicitly called. Deliver answers in the chat. Period.

**User correction (2026-07-08, FOURTH TIME):** Auto-rendered the cellular respiration mapping, the specialist engine engine design, three-lifecycles doc, and multiple partnership analyses — all without being asked. Each one wasted time going through the creative process flow when the user just needed the content in chat. "So when I ask you to generate a PDF, be ready. But until I ask you, you don't need to." The failure pattern includes auto-rendering ASYNC DELEGATION BATCH results — when a subagent finishes and returns content, the instinct was to render it as a PDF. WRONG. Report the content in chat. The user will ask for a PDF if they want one.

The failure pattern: treating every delegation result, every spec, every analysis as something that needs a branded PDF. This wastes time on the creative process flow when the user just needs the answer in the chat. Only render when the user says "PDF," "render this," "send me the document," or equivalent.

**MECHANICAL CHECK before rendering:** Ask yourself: did the user explicitly request a PDF in this message or a previous message? If NO, do not render. Deliver the answer in chat. The creative process flow (Goethe, Wernicke, Bell, Luria) is available and ready, but it does not fire unless called.

## Forbidden

1. The script at `/tmp/render-table-aware-pdf.py` is FORBIDDEN. It uses a generic purple accent. the principal caught this twice. It violates the brand system she built.
2. Using the specialist engine's section API (`/v1/render`) for ANY document containing markdown tables. The section converter flattens tables into raw pipe-character text, producing unreadable output. the principal caught this: "This is formatted terribly, not pretty or easy to read." The section API is ONLY for simple heading+body+items documents with zero tables and zero code blocks.

## THREE Render Paths (pick the right one)

### Path 1: Markdown-heavy docs (DEFAULT) - `scripts/ds-md-to-pdf.py`

Use this for any document with tables, code blocks, math formulas, or dense formatting. This is 90% of documents.

```
python3 skills-library/brand-voice/ds-branded-pdf-render/scripts/ds-md-to-pdf.py \
  <input.md> <"Title"> <"Subtitle"> <output.pdf>
```

What it does:
- Converts markdown tables to styled HTML tables (navy header, gold column labels, alternating teal-tint rows)
- Preserves code blocks on dark teal background with bright teal monospace
- Preserves bold, italic, inline code, bullet lists, numbered lists
- Wraps in the specialist engine CSS with branded cover page (gradient navy/teal, gold DIVINITY SCIENCE wordmark)
- Renders via WeasyPrint
- No running server required

This script was built because the specialist engine's section API DESTROYS tables and code blocks. Do not use the section API for table-heavy docs.

### Path 2: Simple section docs - the specialist engine API (port 8121)

Use this ONLY for documents with no tables and no code blocks: simple briefs, one-pagers, stat cards, agenda docs.

1. Check the specialist engine is running: `curl http://127.0.0.1:port/health`
2. If not running, start it: `cd /<workspace> && python3 run_server.py` (background=true)
3. Convert markdown to Bell section format: `[{"heading": str, "body": str, "items": [str]}]`
4. POST to `http://127.0.0.1:port/v1/render` with payload: title, subtitle, sections, theme="da_vinci", doc_type="report", brand_name="Divinity Science"
5. Output lands in `/<workspace>`

**DO NOT USE THIS PATH FOR TABLE-HEAVY DOCS.** The section converter flattens tables into raw pipe-character text. This was the exact failure that produced "formatted terribly, not pretty or easy to read" feedback.

### Path 3: Diagrams, flowcharts, and visual layouts - WeasyPrint HTML+CSS

Use this for pipeline diagrams, architecture flowcharts, decision trees, or any document where the visual layout (boxes, arrows, branches, color-coded sections) IS the content. Neither the markdown converter (Path 1) nor the Bell section API (Path 2) can express vertical pipelines with arrows, fork branches, status-tagged boxes, or cover-page stat panels. Proven 2026-07-21 rendering the Wave Engine v2.1 pipeline (8 pages, 70KB, dark navy/teal/gold cover + vertical step diagram + component table + citations).

1. Write a Python build script (`build_pdf.py`) that imports WeasyPrint and contains the HTML + CSS as string literals
2. Use the the specialist engine tokens (same as Paths 1 and 2) — never invent colors
3. Structure: cover page (gradient navy/teal, gold wordmark, stat panels) + content pages with `page-break-before: always` at logical sections
4. Render via `HTML(string=HTML_DOC).write_pdf(out, stylesheets=[CSS(string=CSS_DOC)])`
5. Venv: `/<workspace>` has WeasyPrint 69.0 installed

**Required pattern for diagram steps:**
```css
.diagram-step {
  display: flex; gap: 12pt;
  background: #f7fbfa;
  border-left: 3pt solid var(--teal-med);
  border-radius: 4pt;
  padding: 9pt 12pt;
}
.ds-num { /* numbered circle */ }
.diagram-arrow { text-align: center; color: var(--border); }
```

**Status tag colors (consistent across all 3 paths):**
- SETTLED (validated science) → teal `#0d8b6e`
- PROVISIONAL (formative) → amber `#F2B632`
- REMOVED → gray + strikethrough

**Verification — vision check the PDF before delivery:**
`vision_analyze` cannot read PDFs directly. Convert to PNG first:
```bash
pdftoppm -png -r 80 <output>.pdf /tmp/page
vision_analyze(image_url="/tmp/page-1.png", question="...")
```
Check the cover and at least one content page. Confirm no text overflow, status colors render, tables have actual borders (not flattened pipes).

**Forbidden in Path 3:**
- Do NOT reuse the web app indigo palette — print uses Fleet Atlas tokens only
- Do NOT render diagram HTML directly without print-specific CSS (screen layouts produce 1-page-wide output that breaks pagination)
- Do NOT skip the `@page { size: letter portrait; margin: 0.6in }` rule — without it WeasyPrint uses defaults that clip content

## the specialist engine Brand Tokens (from the specialist engine)

These are the CANONICAL brand colors. Do not invent alternatives.

- `bg_primary`: `#0a1e2e` (deep navy)
- `bg_secondary`: `#0d3b3b` (dark teal)
- `bg_card`: `#062323` (near-black teal)
- `border`: `#d8e8e4` (light teal border)
- `text_primary`: `#1a2e2e` (body text, very dark teal)
- `text_secondary`: `#555555`
- `gold`: `#ffd700` (bright gold accent)
- `teal_bright`: `#4ad6b4` (bright teal highlights)
- `teal_medium`: `#0d8b6e` (medium teal)
- `surface_light`: `#f7fbfa` (light teal-tint surface)
- Font: Helvetica Neue, Helvetica, Arial, sans-serif
- Golden ratio governed (PHI = 1.618033988749895)

## Themes

Both paths support the Da Vinci theme (Renaissance Gold: warm gold on DS dark teal canvas). Default to `da_vinci` unless the principal specifies otherwise.

## Verification

After rendering:
1. PDF exists and size is reasonable (50KB+)
2. Open the PDF and confirm DS branding (deep navy/teal cover, gold accents, Helvetica)
3. If the document has tables, verify they render as ACTUAL TABLES with borders and shading, not raw pipe characters
4. Run the AI-tell scanner on the markdown BEFORE rendering (skill: ai-tell-removal-gate)

## Pitfalls

- **MULTI-PAGE CLIPPING (found 2026-09-28):** `ds-md-to-pdf.py` sets `@page{margin:0}` and puts padding on the `.page` div. Div padding applies only to the first page fragment, so pages 3+ render with text touching the top page edge (glyph clipping risk). Fix after generating the HTML: change `@page{size:A4;margin:0}` to `@page{size:A4;margin:12mm 13mm}@page cover{size:A4;margin:0}`, add `page:cover;` to the `.cover` rule, set `.page{padding:0}`, re-run WeasyPrint. Verify with pdftoppm + a pixel bounding-box scan (content must start >6px from edges except the full-bleed cover).
- **BIGGEST PITFALL**: Using the Bell section API for table-heavy docs. It flattens tables into unreadable pipe text. Use `ds-md-to-pdf.py` instead.
- the specialist engine may not be running. Health-check first if using Path 2.
- The web app indigo style (#0a0e1a, #818cf8) is a DIFFERENT MEDIUM and must NOT be used for PDF/print output. Only Fleet Atlas tokens.
- Do not invent color palettes. The tokens above are extracted from DS-FLEET-ATLAS.html and are canonical.
- Always scan for AI telltales BEFORE rendering, not after.
