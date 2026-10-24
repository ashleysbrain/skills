# Clean Executive Packet Pattern

Use this when turning voice-note guidance or rough markdown into a forwardable executive packet.

## Goals
- Keep the document legible for a CTO or board member.
- Use the user’s corrected organizational language consistently.
- Remove obvious AI telltales and filler phrasing.
- Produce a real PDF and verify it before sending.

## Terminology rules
- If the user says the organization is the first user, use that framing consistently.
- Prefer the user’s named entity and team language over generic placeholders.
- Do not keep outdated phrasing like "patient zero" if the user has replaced it.
- Preserve the user’s board / lane names as requested.

## AI-telltale cleanup
- Remove meta language such as "compiled from", "as an AI", "deliverable requested" if it reads like scaffolding instead of content.
- Replace awkward internal-process phrasing with plain executive language.
- Avoid template markers, disclaimer-y phrases, and obvious machine-generated cadence.

## PDF workflow
1. Clean the source text.
2. Generate the PDF locally.
3. Verify the PDF exists and has readable text.
4. Send the PDF as a Telegram attachment.

## Quick verification
- Open the PDF or extract text to confirm the corrected terminology is present.
- Confirm the file name is date-stamped when the packet is versioned.
- Keep the Telegram caption short and direct.
