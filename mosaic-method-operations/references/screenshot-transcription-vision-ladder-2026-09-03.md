# Screenshot Transcription — Vision Ladder (2026-09-03)

principal sent 3 LinkedIn screenshots (neuroscience-of-failure article) to be
transcribed and routed through triangle. No native vision tool in session.
Measured ladder, what worked and what is a dead end:

## The ladder (use in this order)

1. **Local tesseract FIRST** — `/usr/local/bin/tesseract`, no credentials,
   offline. Article prose transcribed near-verbatim across 2 screenshots.
   - Default segmentation for prose columns.
   - `--psm 11` (sparse text) for graphics: the circular framework wheel
     (FALL → INVESTIGATE → ACKNOWLEDGE → LEARN → EVOLVE → REALIGN) came
     out readable under psm 11 where default mode garbled it. Stage words
     land OUT OF ORDER in cyclic graphics — reassemble the cycle from the
     vocabulary set, don't trust line order.
2. **Vision-capable LLM second** — for garbled regions/layout questions.
   Endpoint pre-checks that failed 2026-09-03 (do not re-burn time):
   - Z.AI LLM `api.z.ai/api/paas/v4/chat/completions` rejects image
     content: `messages.content.type is invalid, allowed values: ['text']`.
     Writing-studio model registry has no vision path at all (5 models,
     none take images).
   - xAI OAuth (`auth.json providers/xai-oauth`): access token expired
     (~6h TTL; refresh needed). Refresh POST to auth.x.ai/oauth2/token
     REQUIRES `Content-Type: application/x-www-form-urlencoded` (JSON body
     → HTTP 415) AND `client_id` (→ HTTP 400 without it) — client_id is
     NOT stored in auth.json, so mid-session refresh is a dead end unless
     you can recover the client_id from the original device-code flow.
   - Registry API keys live in `/<workspace>` (e.g. ZAI_API_KEY)
     — but the key existing ≠ the endpoint accepting images.
3. **Merge + sanity-check**: default pass (prose) + psm 11 pass (graphics),
     merged; verify expected vocabulary present (framework stage names,
     headline words). Flag uncertain regions rather than guessing.

## After transcription

- Persist the cleaned source doc into the package (this session:
  `stores/content-pipeline/NEUROSCIENCE-OF-FAILURE-source.md`) — the
  triangle routing embeds the full transcription in the ledger task detail
  so reviewers never need the images.
- principal-methodology/external-framework intake pattern (same as 5WH): full
  verbatim claims list → named research questions mapping onto EXISTING
  flow anatomy (never blank-slate) → named counter-hypotheses (incl.
  "is this X rebranded? name the delta" and conflicts with standing laws)
  → verdict vocabulary ADOPT/ADAPT/REJECT → nothing touches flow-registry
  without verdict + glial QA. Ticket: T-260903-0089, bus #13520.

## Clock note (cross-ref)

Same afternoon produced the FIFTH clock-failure variant: instrument
correct (terminal `date` read 15:51), output wrong (header said 11:52) —
read-transcribe mismatch, not drift. Law: no manual transcription links;
copy digit-for-digit from the immediately preceding tool output; stamp
belongs in the report engine long-term. Full record: skill
`temporal-verification` training log 2026-09-03 (fifth variant).
