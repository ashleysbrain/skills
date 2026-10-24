# Spec structure and human readability notes

Source: session where the user asked to reorganize `ADAPTIVE-EVIDENCE-LEDGER-PRODUCT-SPEC.md` so the document reads as one coherent human spec rather than a body plus appendices.

## Durable lessons

- When reviewer feedback says the spec feels clunky, appendix-heavy, or like a running list, reorganize the material into the main narrative instead of adding more tail sections.
- Put calculations, defaults, thresholds, and update rules in the main section that owns the concept, not in an appendix.
- If a section introduces implementation order, source sets, or confidence logic, place that guidance next to the data model or scoring model it governs.
- Appendices should be reserved for raw traces, source excerpts, or non-essential references; they should not hold core product logic.
- After structural edits, rebuild the rendered artifact so the PDF matches the markdown.
