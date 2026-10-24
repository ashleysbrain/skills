---
name: multi-provider-credential-routing
description: Use when a model 403s via one route; retry vendor-native.
version: "1.0.0"
last_updated: "2026-08-31"
---

# Multi-Provider Credential Routing

## When to Use

- A model call returns **HTTP 403** through an aggregator key (OpenRouter etc.) — or the session's active provider rejects image/multimodal content with a 400 `allowed ['text']`.
- You are about to conclude "model X is unavailable" or "tool Y does not work here."
- You need a vision-capable, long-context, or premium model and the first route fails.

## Core Law

**A 403 from one key is per-key entitlement scoping — not an outage, not a dead key, not a global unavailability fact.**
The same model often works through a vendor-native credential sitting in the same auth file. Route, don't retreat.

## Procedure

0. **Consult recorded state BEFORE the first attempt (ratings-first law, principal 2026-08-31).** Before calling ANY model for a capability, check what memory/ratings already record about entitlements and working routes. A 403 that was seen once is a *prediction*, not a surprise: the vision incident of 08-31 burned 6 calls on an OpenRouter vision wall that same day's memory already documented. Query recorded ratings → select best-rated route → THEN execute. Trial-and-error against a known wall is a defect class ("that vision thing was a major failure and it should have been predictable"). Log every selection's outcome back so the prediction hit-rate compounds.

1. **Classify the failure.** 400 content-type = session provider is text-only. 403 = entitlement. 402 = credits. 429 = throttle. Only 402/429 say anything about the model itself.
2. **Enumerate routes.** Read `<agent-home>/auth.json`: `providers` (OAuth: xai-oauth, google-gemini-cli, …) and `credential_pool` (openrouter, llm-vendor, custom, nvidia-nim, …). Check `last_status` and `failure_reason` fields — `ok` entries are live.
3. **Retry vendor-native.** Same model, vendor's own endpoint, vendor's own credential. Verified example: grok-4.6 vision → 403 on OpenRouter, **first-shot success** via `providers.xai-oauth.tokens.access_token` at `https://api.x.ai/v1/chat/completions` (OpenAI-compatible multimodal body, Bearer auth).
4. **Only then** conclude unavailability — and say which routes were tried.
5. **Log the working tuple**: task-class × model × credential-route. These tuples are the raw data for per-stack scoring; route knowledge compounds.

## Vision Specifically
- `vision_analyze` inherits the session's active provider; text-only providers 400 on images. Fallback chain: vision_analyze → Grok 4.6 via xAI OAuth → Gemini via google-gemini-cli OAuth (`last_status: ok`) → NVIDIA NIM vision models.
- xAI OAuth tokens are device-code, ~6h expiry, auto-refresh present in auth.json (`last_refresh` timestamp).
- Send images as `data:image/jpeg;base64,...` in an OpenAI-style `image_url` content part.

## Distinguish Token-Invalid from Not-Entitled (2026-09-01)

A vendor-native route that worked yesterday can 403 today with `bad-credentials` — that is **token expiry/validation**, not entitlement. Same error class, different fix:
- **403 `bad-credentials` / `could not be validated`** = the OAuth token itself is stale. xAI device-flow tokens are ~6h; check `providers.xai-oauth.last_refresh` BEFORE the call and re-arm if old. The route is still good.
- **403 `unauthenticated` entitlement-shaped / per-model** = key scoping. Route elsewhere (see Core Law).

Auth-pool dead-route detection (read these fields during route enumeration, step 2):
- `providers.<name>.last_auth_error` with `invalid_grant` + `relogin_required: true` = route dead since the `at` timestamp (seen: nous dead since 2026-08-09).
- `providers.google-gemini-cli` may hold ONLY an `email` (no `tokens` key) — and `~/.gemini/google_accounts.json` with `"active": null` = account signed out, no armed token on disk. Not a route until re-armed.

## Keyless-First Law (principal correction 2026-09-01)

Before surfacing ANY purchase/vendor decision card to the principal, exhaust the zero-cost path first — including local-stack upgrades. principal: "You need to find the workaround instead of waiting on me all the time. You are the intelligent operating system."

Applied example (STT): the "purchase vendor ASR key" card sat open for days while the actual root cause was a **whisper-tiny hardcode** in the local STT config; local whisper **large-v3** is a different animal on accent-garbled clips and needs zero dollars, zero keys, zero principal input. Correct order: probe live credential pool → probe local-stack upgrade → cut in-house eval corpus (e.g. Telegram voice cache at `<agent-home>/cache/audio/*.ogg`) → only if keyless measurably fails, surface the decision card WITH bake-off numbers attached, never a bare question.

Audio probe note: vendor audio understanding (grok audio, chirp) rides the same route-enumeration procedure as vision — classify the 403 first (token vs entitlement) before concluding anything.

## Pitfalls
- Do NOT write "X doesn't work" into memory or other skills from a single-route failure — that hardens into a months-long false refusal.
- Aggregator catalog listing ≠ callable on a given key (seen: slug listed, call 404s).
- Keys live in `credential_pool[i].access_token` (not `api_key`) — field name varies; walk the JSON, don't assume.
- A provider entry existing in auth.json ≠ a live route — check `last_refresh`, `last_auth_error`, and for armed tokens before counting it as an option.

## References
- `references/2026-08-31-vision-entitlement-routing.md` — full incident: five 403s on OpenRouter, diagnosis, working xAI route, code shape.
- `references/2026-09-01-audio-stt-route-probe.md` — audio/STT probe (token-invalid vs entitlement), keyless-first law, whisper-tiny hardcode root cause.
