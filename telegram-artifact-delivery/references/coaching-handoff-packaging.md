# Coaching Handoff Packaging

Use this pattern when the user wants a review artifact for later reference *and* a Telegram delivery.

## Recommended flow
1. Compile the brief into a local PDF or other clean attachment format.
2. Verify the artifact exists and is the expected type/size before sending.
3. Send the file as `MEDIA:<absolute-path>` so Telegram delivers a real attachment.
4. Keep the chat caption short and action-oriented.
5. Include the next-step coaching bullets in the message body when the user wants the recipient to act on the brief.

## Good caption pattern
- `Attached is the brief for future reference.`
- `Next steps:`
  - lock category/wedge
  - pick the smallest useful first outcome
  - define the first aha moment
  - clarify evidence bounds
  - stay at market/direction/trajectory level before feature design

## Verification habit
- Confirm the file path before delivery.
- If possible, confirm the file type after generation (e.g. PDF).
- Do not claim delivery until the send call succeeds.

## Why this matters
This keeps the artifact both reviewable and actionable: the user gets a durable file for later reference and the recipient gets a clean coaching handoff in the same turn.
