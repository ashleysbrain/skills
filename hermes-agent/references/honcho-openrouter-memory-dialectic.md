# Honcho memory + OpenRouter triage

Use when Honcho memory, embeddings, or the deriver/API stack reports an OpenAI-style missing-key error even though the machine already has an OpenRouter credential.

## Core rule
Do not trust the raw `.env` alone. Inspect the *resolved* model config that the running service actually loaded.

## Common failure shape
- Embeddings or memory calls try to reach `api.openai.com`
- The machine has `OPENROUTER_API_KEY`, but the service is still resolving an OpenAI transport without the matching key or proxy base URL
- A worker crashes with a validation error such as `Missing API key for openai model config`

## Fix pattern
1. Point the feature at the OpenRouter proxy explicitly.
2. Make the API-key source line up with that proxy.
3. Restart the affected services so the new env/config is actually loaded.
4. Verify both an embedding call and a chat call after restart.

## Practical config notes
- For embeddings, set the model config override to use the OpenRouter base URL instead of the default OpenAI endpoint.
- For chat/dialectic paths, confirm the resolved config is reading the intended API-key env var, not just that the secret exists somewhere in the shell environment.
- If a worker still fails after the env edit, re-check the service's resolved config and the per-feature overrides before changing the model itself.

## Verification checklist
- health endpoint returns OK
- one embedding request succeeds
- one chat request succeeds through the same provider path
- deriver/API logs no longer mention missing OpenAI credentials