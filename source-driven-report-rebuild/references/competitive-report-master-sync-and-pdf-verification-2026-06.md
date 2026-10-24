# Competitive report master-sync and PDF verification (2026-06)

Use this pattern when maintaining a large user-facing report that exists both as:
- per-section source markdown files, and
- a current concatenated master markdown that is the direct PDF input.

## What changed in this session
- Added a new AI-health competitor layer (Perplexity Health, OpenEvidence, K Health, Ada Health, Glass Health, Hippocratic AI) to the holistic section.
- Patched **both**:
  - the section source: `09-HOLISTIC-multi-dimensional-competitors.md`
  - the master artifact source: `8D360-Competitive-Landscape-Report-2026-06-06.md`
- Rebuilt the PDF with `pandoc` + `weasyprint`.
- Verified the finished PDF with `pypdf` text extraction instead of trusting build warnings alone.

## Durable lesson
When the user wants the shipped PDF updated now, and the repo currently has both section source files and a direct master markdown used for rendering, patching only one layer is insufficient.

Patch both layers unless you also regenerate the master deterministically from the section sources in the same session.

## Verification pattern
1. Rebuild the PDF.
2. Record whether the build produced a file, even if warnings appear.
3. Treat internal-anchor/CSS warnings as **diagnostic output**, not automatic failure.
4. Run a text-layer verification pass on the final PDF.
5. Search for the newly added headings/keywords.
6. Report the page numbers where the new content appears.

## Why this matters
Large report pipelines often have pre-existing warning noise. If you stop at warnings, you may falsely report failure after a successful rebuild. If you skip text-layer verification, you may falsely report success even though the new content never made it into the exported PDF.

## Example verification target set
- new section heading
- new platform names
- new watchlist heading
- any user-requested newly added competitor or framework names

## Good outcome
- section source stays aligned
- current master source stays aligned
- rebuilt PDF exists
- new content is proven present in the final artifact
- user gets exact page references, not just a claim that it worked
