# Process Document Output Pattern

## When to use
Use this pattern when the user asks to turn a workflow discussion into a deliverable document.

## Output sequence
Produce the document in this order:
1. **Process flow** — describe the system as instructions to the AI or operator.
2. **SOP version** — reorganize the same content into formal procedure sections.
3. **Command-to-AI version** — rewrite the SOP as direct action instructions.

## Core rule
- Preserve the substantive content.
- Reorganize and clarify it, but do not silently delete important steps, human touchpoints, exception handling, release metadata, or source detail.
- If the source is a PDF or symbol-heavy export, convert it losslessly to Markdown: normalize encoding and punctuation, but keep the full structure and meaning intact.

## Formatting guidance
- Prefer numbered sections and explicit gates.
- Keep human review points visible.
- Keep near-miss / revise logic visible.
- If the user asks for a file, make it attachment-ready in markdown.

## Pitfall
Do not summarize the conversation back to the user when the request is for an operational document. Deliver the process itself in a usable form.