---
name: brand-preserving-document-packaging
description: Rebuild document packs, handbooks, or multi-PDF bundles so they use the correct original logo, color palette, and document branding consistently across cover pages, headers, and individual files, then verify the rendered PDFs and artifact set.
tags: [documents, pdf, branding, logo, palette, weasyprint, markdown, productivity]
version: 1.0.0
---

# Brand-Preserving Document Packaging

Use this when the user says a document pack should use *our colors*, *our logo*, or the original visual identity, especially after a draft was generated with a generic or incorrect theme.

## When to use
- A PDF or document bundle needs to match an established brand system
- The user wants the original logo preserved from the source material
- The previous render used the wrong colors, fonts, or visual tone
- You need to regenerate one combined PDF and/or individual PDFs from source markdown or HTML
- The final artifact should look polished, internal-facing, and consistent across all sections
## Core workflow

1. Identify the canonical source of truth for the brand: the original document, logo asset, or approved style guide.
2. Do not guess the palette from memory when a logo or source asset exists; sample the asset or inspect the source document.
3. Rebuild the PDFs from source text/markup instead of trying to patch a bad PDF visually.
4. Apply the brand consistently to:
   - cover page
   - running header
   - section headings
   - callout boxes and borders
   - page footers
   - individual document variants in the same pack
5. Keep the layout restrained and readable: use one accent color, a neutral body palette, and clear hierarchy.
6. If the user wants both a combined pack and separate docs, render both from the same shared theme.
7. Verify the first page, page count, and embedded image/logo presence before delivery.
8. Run the draft through the Da Vinci creative organ system for final branding, design polish, and elite specialist review (Systems Architect, Physicist, Distributed Systems Engineer, QA Architect) before final verification.

## Brand extraction guidance
- If a logo file exists, inspect it first for dominant colors and visual tone.
- Prefer the actual brand asset over approximate brand descriptions.
- For dark/neutral brands, use a restrained palette with one accent color rather than a rainbow theme.
- For a logo with clear gold/charcoal identity, carry that into headings, rules, borders, and cover accents.

## Rendering guidance
- HTML + WeasyPrint is a strong default when the input is markdown or HTML and the output is a polished PDF.
- Use the same HTML/CSS theme for the combined pack and the standalone document PDFs.
- Include the logo in the cover and/or running header when the brand calls for it.
- If the source documents are already in markdown, convert them once and reuse the converted body inside the branded template.
- For markdown-heavy reports, a reliable pattern is: `pandoc` for markdown→HTML, then WeasyPrint for HTML→PDF.
- Keep title blocks, spacing, and page numbering consistent across the pack.
- Verify the rendered PDF with a real reader when possible: page count, file size, and the first-page brand treatment.

## Verification checklist
- Confirm the final PDF exists and has a non-trivial file size
- Confirm the first page contains the logo or brand mark when expected
- Confirm the page count matches the intended bundle size
- Inspect the PDF text layer if the user corrected wording or title text
- Confirm the combined pack and the individual PDFs share the same brand system

## Common pitfalls
- Do not invent a palette when the brand asset is already available
- Do not use one design for the cover and a different design for the interior pages
- Do not keep the old generic theme after the user corrects the branding
- Do not edit only the visible cover while leaving the underlying document styling unchanged
- Do not forget to rebuild the individual PDFs if the user asked for both the pack and the standalone files

## Support files
- `references/brand-rebuild-notes.md` — concise notes on the logo/palette discovery workflow, plus the verification steps used for branded handbook packs.
- `references/your-org-pdf-workflow.md` — the markdown→HTML→WeasyPrint pattern and verification notes used for Divinity Science-formatted PDFs.

## Overlap notes
- `telegram-pdf-bundle-delivery` covers delivery of PDF bundles to Telegram; this skill covers the brand system itself.
- `document-debranding-and-link-sanitization` covers removing stale names and brand references; this skill covers preserving and applying the correct brand.
- `pdf-table-layout-verification` covers dense layout safety and readability, not visual identity.

## User preferences (dated filenames, PDF-first delivery)
- Always deliver finished documents as PDFs. Do not hand the user markdown and expect them to convert it.
- Filename format: `DS-{DocumentTitle}-{YYYY-MM-DD}.pdf` (Divinity Science) or the appropriate brand prefix.
- The date goes in the filename, not just the content. This is how the user finds files later.
- No AI telltales anywhere in the document content: no em-dashes, no "Furthermore/Moreover", no perfectly balanced three-item lists, no obvious AI paragraph structure.
- No formatting identifiers: the reader should not see markdown artifacts, raw HTML tags, or obvious template markers.
- If the content is structured (sections, tables, callouts), build clean HTML directly and render via weasyprint. Do not route through pandoc unless the source is raw markdown that needs conversion.
- Deliver via Telegram using `MEDIA:/absolute/path/to/file.pdf`.

## Direct HTML-to-PDF pattern (weasyprint, no pandoc)
When the source is structured content you are composing (not raw markdown to convert), write clean HTML directly and render with weasyprint. This is faster and gives more control than pandoc→HTML→weasyprint:

```html
<style>
@page { size: letter; margin: 1in 0.9in;
  @bottom-center { content: "Brand Name — Confidential"; font-size: 8pt; color: #999; }
}
body { font-family: Helvetica, Arial, sans-serif; color: #1a1a1a; line-height: 1.6; font-size: 11pt; }
.header { text-align: center; border-bottom: 2px solid #0a0a0a; padding-bottom: 16pt; margin-bottom: 28pt; }
h2 { font-size: 15pt; font-weight: 700; border-bottom: 1px solid #ccc; padding-bottom: 6pt; margin-top: 28pt; }
.callout { background: #f7f7f7; border-left: 3px solid #0a0a0a; padding: 12pt 16pt; margin: 16pt 0; }
table { width: 100%; border-collapse: collapse; margin: 12pt 0; font-size: 10pt; }
th { text-align: left; font-weight: 600; padding: 6pt 8pt; border-bottom: 1px solid #333; background: #f7f7f7; }
td { padding: 6pt 8pt; border-bottom: 1px solid #e0e0e0; }
</style>
```

Key design choices for DS-branded docs:
- Restrained black-and-white palette (no blue, no generic colors). Accent color only if the brand system calls for it.
- Helvetica/Arial body text. Strong weight hierarchy (700 for headings, 600 for sub-headings).
- Branded footer via `@page @bottom-center`.
- Callout boxes with left border accent, not colored backgrounds.
- Tables with subtle header background and light row dividers.
- Write the HTML to `/tmp/`, render with `weasyprint`, then clean up the intermediate file.

## Output rule
When the user asks for the finished artifacts, deliver the PDF(s) directly (via MEDIA path to Telegram or as a file attachment) with a brief confirmation. Do not deliver markdown.
