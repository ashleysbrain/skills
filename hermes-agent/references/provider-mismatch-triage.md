# Provider mismatch triage

Use when a the operator agent/Honcho service fails with a missing-key validation error even though the machine has *some* LLM credential configured.

## What this usually means
A service is resolving a model config whose **transport** and **credential source** do not match the available secrets.

Common pattern:
- config says `transport=openai`
- environment only exposes an OpenRouter key or another OpenAI-compatible proxy key
- the runtime asks the OpenAI client for `OPENAI_API_KEY` and crashes with a validation error

## Triage sequence
1. Check the exact runtime error in the worker or API logs.
2. Inspect the resolved model config, not just the raw env file.
3. Verify whether the process is reading:
   - `LLM_OPENAI_API_KEY`
   - per-feature overrides like `*_MODEL_CONFIG__OVERRIDES__API_KEY_ENV`
   - a proxy `base_url`
4. If the service is meant to use a proxy such as OpenRouter, make the provider/transport and secret source consistent.
5. Restart the relevant services and re-check health/logs.

## Session example
- Deriver crashed with: `Missing API key for openai model config`
- The machine had an OpenRouter credential available, but Honcho was still resolving an OpenAI transport without the matching key.
- Fix: wire the service config to the existing credential source, then restart API + worker and verify `GET /health`.

## Useful verification
- `hermes config`
- service logs under `<agent-home>/logs/`
- health endpoint for the local API
- a fresh worker poll cycle after restart