# Scoring Engine Appendix Checklist

Use this checklist when a plan or pitch must explain *how the machine works* rather than only *what it does*.

## Include these layers
- **Problem framing:** one sentence that defines the machine.
- **Signal pipeline:** raw inputs -> normalization -> field scores -> baseline delta -> confidence -> state -> final composite score.
- **Per-field math:** exact score range, normalization scale, and weighting rules.
- **Baseline logic:** baseline is the operating center, not a universal ideal.
- **Confidence model:** separate score from certainty.
- **State machine:** describe conservative transition rules and safety overrides.
- **Composite formula:** show the top-line score and any modifiers (weights, balance, confidence).
- **Example calculation:** include at least one worked example so engineers can sanity check implementation.
- **Pseudocode:** provide the full loop from ingest to render.
- **Auditability:** explain what must be logged for reproducibility.

## When generating PDFs or exported briefs
- Verify the exported text, not only the rendered page.
- Search for accidental literal words where bullets should be symbols.
- If the PDF generator mis-renders bullets, use explicit hyphen-prefixed paragraphs or another deterministic representation.
- Always re-open the exported file and extract text to confirm formatting survived.

## Common failure modes
- High-level pitch docs that omit the scoring contract.
- Averages presented as if they are the whole score when the real system uses weights, confidence, or balance modifiers.
- State changes that react to a single noisy input.
- Confusing the user-facing avatar state with the underlying score vector.
