# Algorithm step-containment map (session-specific)

Use this note when a user asks how each step in a combined technical report *contains* specific algorithms and *why*.

## Trigger
- The user asks: "how each step contains certain algorithms and why"
- The doc needs to explain the relationship between steps, families, and layers rather than only listing formulas
- The audience is technical and expects architecture / dependency rationale

## Required structure
For each step, include:
- **Step name**
- **Algorithms/families inside the step**
- **Why each algorithm belongs there**
- **What the step consumes**
- **What the step outputs**
- **How it connects to the previous and next steps**
- **Status tag per family/card** when live/dev/spec/research matters

## Practical rule
Do not leave containment implicit in prose. If a step uses a family because it normalizes, gates, or transforms the output of another family, say that directly in a short mapping block or callout.

## Good phrasing pattern
- "Step 2 contains Families A and B because A establishes the baseline and B applies the predictive transform after normalization."
- "This step is present to convert raw evidence into a form that later scoring layers can consume."

## Delivery pattern
- Prefer a compact table-like bullet list or card grid in the HTML source.
- Re-check the rendered PDF/HTML so the mapping is visible after conversion.
- If the user asks for one combined document, keep the mapping inside the combined source instead of scattering it across two separate files.
