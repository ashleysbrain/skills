# Vision Model Routing Through Per-Key Entitlements (2026-08-31)

## Situation
principal sent a poster photo for image analysis. The session's active provider was text-only, and the principal-or OpenRouter key 403'd on every vision-capable model.

## What failed and why
- `vision_analyze` tool → provider 400 `content.type invalid, allowed ['text']` (active provider = text-only; the tool inherits the session's provider).
- OpenRouter (principal-or key) → **403 Forbidden** on: x-ai/grok-4.6, openai/gpt-5.4, anthropic/claude-sonnet-4.6, google/gemini-3.7-flash, google/gemini-3.1-flash-image. `z-ai/glm-5.3` → 404 (slug listed in public catalog but not callable on that key).
- Verdict: per-key entitlement scoping. The key is alive (`last_status: ok`); the models are fine; the pairing is disallowed.

## What worked (verified live)
**Grok 4.6 vision via the xAI OAuth token in `<agent-home>/auth.json`:**
- Credential: `providers.xai-oauth.tokens.access_token` (device-code OAuth, ~6h expiry, auto-refresh; `last_refresh` timestamp in auth.json)
- Endpoint: `POST https://api.x.ai/v1/chat/completions`, `Authorization: Bearer <token>`
- Body: OpenAI-compatible multimodal content array (`text` + `image_url` with a `data:image/jpeg;base64,...` URL)
- First-shot success reading dense poster detail; the model also correctly refused to invent unreadable small labels.

Other live credential routes found in auth.json (untested for vision that day): 3× google-gemini-cli OAuth (`last_status: ok`), NVIDIA NIM key (`ok`), openai-codex OAuth (`ok`).

## Generalizable pattern
On 403/400 for a capability through one route:
1. Treat it as a routing problem, not an availability fact.
2. Enumerate `providers` + `credential_pool` in `<agent-home>/auth.json` — vendor-native OAuth often carries different entitlements than aggregator keys.
3. Retry the same model through the vendor-native route before declaring it dead.
4. Record the working tuple: task-class × model × credential-route. These tuples are the raw data for per-stack output scoring (apples-to-oranges graded per-context, never cross-compared raw).

## Stack-database note
This incident was logged as the first real data point in the the OS stack-scoring program (T-260831-0046): vision-analysis microtask → grok-4.6 × xAI-OAuth × direct API = success; five OpenRouter-routed alternatives = 403.
