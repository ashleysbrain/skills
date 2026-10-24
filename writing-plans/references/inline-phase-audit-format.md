# Inline Phase Audit Format

Use this pattern when a roadmap, product plan, or launch document needs to show what is already done *next to the relevant phase*, not in a separate summary block.

## When to use
- The user wants a completion audit tied to roadmap phases, milestones, or deliverables.
- The document may be printed in black and white, so color-only status is not reliable.
- The user wants evidence of progress without losing the original roadmap structure.

## Format
For each phase, add a short audit block directly under the phase heading:

```markdown
### Phase N — [Name]
**Goal:** [one sentence]

### Coverage audit
- **[DONE]** [item that already exists, with concrete artifact or reason]
- **[PARTIAL]** [item that is defined but not yet production-ready]
- **[TODO]** [item that still needs new work]

Deliverables:
- [original deliverable list remains below]
```

## Rules
- Keep the audit short: 3-5 bullets per phase.
- Put the status label at the start of the bullet.
- Tie each bullet to a concrete artifact, section, or implementation state.
- If the user prints in grayscale, the audit must still make sense without color.
- Do not replace the phase plan with a separate global snapshot unless the user explicitly asks for both.
- If a phase has nothing done yet, say so plainly instead of inflating partial progress.

## Good labels
- **[DONE]** already present in source docs, visuals, or code
- **[PARTIAL]** conceptually defined, but not implemented or packaged
- **[TODO]** missing or not yet started

## Bad patterns
- A top-of-document status snapshot that does not attach to any phase
- Color-only meaning with no text labels
- Percentages that are not backed by specific evidence
- Vague phrases like "mostly complete" without saying what exists

## Verification
- Check that each phase still reads naturally on its own.
- Check that the status label is visible in grayscale.
- If exporting to PDF, verify the extracted text still contains the labels and phase headings.
