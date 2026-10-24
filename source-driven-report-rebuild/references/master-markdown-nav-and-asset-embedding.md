# Master markdown nav and asset embedding

Use this when rebuilding a large PDF/report from a concatenated master markdown file assembled from many source docs.

## Problem pattern
A report rebuild adds:
- a front summary/navigation page
- internal jump links to later sections
- a screenshot appendix with local downloaded assets

Common failure modes:
1. Internal links point at guessed slug IDs that do not exist in the final concatenated markdown.
2. Pandoc/WeasyPrint emits missing-anchor errors for the section map.
3. Local screenshots render as alt text because the PDF build cannot resolve relative assets.

## Durable fix
1. Add explicit heading IDs with Pandoc-style anchors, e.g.:
   - `# Summary and Navigation {#summary-and-navigation}`
   - `# Category 1: Physical Dimension (PHY) {#category-1-physical-dimension-phy}`
   - `## 1b. Sleep Apps — Part 2 {#1b-sleep-apps--part-2}`
2. Link to those exact anchors from the front summary page rather than guessing generated slugs.
3. Build from the document directory or pass an explicit resource path:
   - `pandoc report.md --resource-path=. --pdf-engine=weasyprint -o report.pdf`
4. Verify the rebuilt PDF, not just the markdown source:
   - confirm summary pages appear first
   - confirm screenshot appendix appears at the end
   - confirm images are embedded instead of replaced by alt text
   - confirm there are no missing-anchor errors during build

## Why this matters
Concatenated master documents often contain repeated headings (`Executive Summary`, `Comparative Matrix`, etc.), so auto-generated slugs are easy to guess wrong. Explicit anchors keep the navigation page stable even as the underlying source docs evolve.

## Minimal verification checklist
- Build completes without missing-anchor errors
- Local appendix images embed successfully
- Front section map text appears on the first pages
- Target appendix pages contain the expected screenshot captions/content
