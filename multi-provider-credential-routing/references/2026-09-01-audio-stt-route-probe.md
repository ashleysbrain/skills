# Audio/STT Route Probe + Keyless-First Correction (2026-09-01)

## Trigger
principal: voice lane "degraded" for days with a vendor-purchase decision card (T-260828-0190) parked in the ledger. principal correction: "find the workaround instead of waiting on me."

## Probe sequence (all executed live against the newest cached voice clip)

1. **grok-4.6 audio via `providers.xai-oauth.tokens.access_token`** → HTTP 403 `bad-credentials: The OAuth2 access token could not be validated.` — token expiry, NOT entitlement (same route carried vision successfully the prior day). Fix path: re-arm device-flow token. Route remains viable.
2. **google-gemini-cli** → provider entry holds only `email`; `~/.gemini/google_accounts.json` shows `"active": null` (signed out). No armed token on disk. Not a route until re-armed.
3. **nous** → `last_auth_error: invalid_grant / relogin_required` dead since 2026-08-09.
4. **OpenRouter audio models** → same per-model entitlement wall as the 08-31 vision 403s.

## The actual root cause (not a missing purchase)
Local STT was hardcoded to **whisper-tiny** — the known root cause of twang/accent garbling. Local whisper **large-v3** was never tried. Zero dollars, zero keys.

## Correct escalation order (now law)
1. Probe live credential pool (classify each failure: token-invalid vs not-entitled vs signed-out)
2. Probe local-stack upgrade (model size/config hardcodes are the usual culprit)
3. Cut in-house eval corpus — Telegram voice cache lives at `<agent-home>/cache/audio/*.ogg` (base64 for API probes; `input_audio` content part with `format: ogg` for OpenAI-compatible audio endpoints)
4. Only if keyless measurably fails: decision card to principal WITH bake-off numbers, never a bare question

## Scoring-database tuples logged this session
- grok-4.6 vision × xAI-OAuth × api.x.ai = SUCCESS (08-31)
- grok-4.6 audio × xAI-OAuth(stale token) = 403 token-invalid (09-01)
- All OpenRouter multimodal × openrouter pool key = 403 entitlement (both days)
