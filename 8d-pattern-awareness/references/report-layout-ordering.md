# 8D report layout ordering notes

This reference captures layout-order corrections that repeatedly matter in the rendered 8D report surface.

## Ordering rules
- Put the dimension recommendations block (the quick-wins grid) before the confidence line.
- Keep Confidence after the recommendations so the specialist answers land before the meta judgment.
- Keep Watch-outs before Confidence when the report includes both.
- If the footer exists, render it as plain text only; do not wrap it in a separate header, label chip, or card.
- Do not add a generic intro blurb above the dimension recommendations; let the cards speak for themselves.

## Footer rule
- The footer should read like footer text, not a section heading.
- If the footer text already carries the branding and timestamp, do not add a second label above it.

## Source-of-truth rule
- When the user asks for section moves or order changes, update the editable source and regenerate rather than rearranging the rendered PDF by hand.
- Preserve the baseline artifact’s geometry unless the user explicitly asks for a layout change.
