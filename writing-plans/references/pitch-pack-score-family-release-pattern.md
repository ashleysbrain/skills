# Pitch-pack / score-family release pattern

Session-derived pattern for methodology-heavy, open-core launch docs.

## Packaging
- Prefer a small number of combined PDFs instead of many fragments.
- Default shape: 1) a readable master brief, 2) a technical methodology/scoring appendix.
- Put formula detail, score-family taxonomy, and worked examples in the appendix.
- Keep the front brief non-repetitive and point readers to the appendix for math.

## Math / scoring wording
- Describe the engine as **database-scored first**.
- Native score outputs are the source of truth.
- 0–100 / 1–10 is a final presentation layer only.
- Never describe the engine layer as normalized input unless that is literally true.
- Spell out: raw evidence -> native score -> baseline -> confidence -> coupling -> composite -> display.

## Score-family coverage
- Keep the full family map visible: main scores, base scores, sub-score families, and optional/contextual families.
- For the current health methodology, explicitly document:
  - ADHD family: baseline vs acceleration classification
  - Nutrition composite: 7-sub-score family with partial-day adjustment
  - Sexual health composite: relational integration, not intercourse-centric
  - Sleep family: planned next, separated from current physical/state layers

## Open-core positioning
- State the community-standard / hosted-moat boundary in the launch narrative itself.
- If methodology is commercially valuable, release the community standard openly but keep premium intelligence, orchestration, hosted workflows, or enterprise assets as the moat.
- Revenue strategy belongs in the architecture and release plan, not only in marketing.

## Verification
- After PDF generation, extract text and verify the exact teaching phrases survive rendering.
- Check for the presence of score-family headings and worked-example headings in the extracted text.
- If bullets render poorly, switch to deterministic hyphen-prefixed paragraphs for the exported document.
