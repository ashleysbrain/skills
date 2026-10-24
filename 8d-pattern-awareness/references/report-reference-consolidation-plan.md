# Report Reference Consolidation Plan

## Problem
`8d-pattern-awareness` carries 21 reference files, well above the 15-file maintenance threshold (R13 from skill-update-engine). The `report-*` prefixed files (14 of 21) are the primary consolidation target — they accumulated across sessions as one-off editing notes and are now hard to navigate and maintain.

## Current `report-*` Files (14)

**Editing workflow:**
- `report-editing-constraints.md` — narrow edit rules
- `source-driven-report-rebuild.md` — rebuild from editable source
- `raster-pdf-surgical-editing.md` — raster PDF edits
- `raster-label-removal-workflow.md` — label removal
- `report-golden-master-reproduction.md` — reproduce approved document
- `report-golden-master-tailored-principal.md` — tailored variant reproduction

**Layout and style:**
- `report-layout-density-and-palette-notes.md` — density/palette
- `report-layout-ordering.md` — section order and footer
- `report-legibility-and-palette-corrections.md` — legibility fixes
- `report-palette-preflight.md` — palette checks
- `report-quote-policy-and-flow-layout.md` — quote/flow rules
- `report-style-calibration.md` — style rules

**Examples:**
- `user-facing-report-example.md` — canonical example
- `user-facing-report-tailored-principal.md` — tailored example

## Proposed Consolidation

### Group A → `report-editing-guide.md`
Merge into a single authoritative editing workflow guide:
- `report-editing-constraints.md`
- `source-driven-report-rebuild.md`
- `raster-pdf-surgical-editing.md`
- `raster-label-removal-workflow.md`
- `report-golden-master-reproduction.md`
- `report-golden-master-tailored-principal.md` (reduce to a section variant, not a separate file)

### Group B → `report-layout-and-palette-guide.md`
Merge into a single layout/style reference:
- `report-layout-density-and-palette-notes.md`
- `report-layout-ordering.md`
- `report-legibility-and-palette-corrections.md`
- `report-palette-preflight.md`
- `report-quote-policy-and-flow-layout.md`
- `report-style-calibration.md` (elevate as primary; absorb others as subsections)

### Group C → keep `user-facing-report-example.md`
Keep as canonical example. Absorb `user-facing-report-tailored-principal.md` as a "variant" section at the end, not a separate file.

## Result
14 `report-*` files → 3 files. Total references: 21 → 10 (within threshold).

## Prerequisites
- Verify no SKILL.md body text references individual `report-*` files by exact path (grep for backtick paths in SKILL.md body).
- Update manifest list after consolidation.
- Delete the merged source files only after verifying the consolidated files contain all their content.
- Update any in-body pointers in SKILL.md to the new file names.
