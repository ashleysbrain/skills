# Report rebuild format guardrails

## Durable lesson from Qubit/TWC deck rebuild
- When the user rejects a scoring scale or mapping, propagate the correction through the *source HTML* and regenerate the PDF.
- Do not leave mixed language across panels (for example, one section saying `1–10` while another section says `normalized input`).
- For rebuilt report/deck artifacts, verification must include the rendered PDF, not only the HTML source.
- If the user says a formatting pattern should match another document, treat the other document as the visual benchmark and check the rendered output against it.

## Practical curation note
This kind of correction belongs in the governing rebuild skill's pitfalls/verification section, not only in memory, because it affects future report regeneration workflows.