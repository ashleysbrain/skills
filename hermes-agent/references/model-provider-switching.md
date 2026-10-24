# Model Provider Switching Troubleshooting

## Symptom
the operator agent is routing requests through the wrong provider (e.g., OpenRouter when Z.ai LLM is configured and preferred), resulting in errors like "no credits" or unexpected model behavior.

## Root Cause
The `model` section in `<agent-home>/config.yaml` controls the active provider. Even when alternative providers are configured under `providers:`, the active one is determined by:
- `model.provider` — which provider to use
- `model.default` — which model to use
- `model.base_url` — endpoint for that provider

If these point to OpenRouter but a Z.ai provider exists in `providers.llm-vendor`, requests go to OpenRouter.

## Quick Fix (CLI)
```bash
# Switch to Z.ai LLM
hermes config set model.provider llm-vendor
hermes config set model.default glm-4.6
hermes config set model.base_url https://api.z.ai/api/coding/paas/v4

# Verify
hermes -z "ping - just say pong"
```

## Verify Current Config
```bash
# Show model section
hermes config show | grep -A 10 "model:"
# Or read directly
cat <agent-home>/config.yaml | grep -A 10 "^model:"
```

## Verify Provider Exists
Check `providers:` section has the target provider with valid API key:
```yaml
providers:
  llm-vendor:
    api_key: <your-glm-key>
    api_mode: chat_completions
    base_url: https://api.z.ai/api/coding/paas/v4
    name: Z.ai LLM Coding
```

## Common Scenarios

| Scenario | Fix |
|----------|-----|
| OpenRouter free model needs credits | Switch to Z.ai (free tier) or add OpenRouter credits |
| Provider configured but not active | Update `model.provider`, `model.default`, `model.base_url` |
| Multiple profiles, wrong one active | `hermes profile use <name>` then verify config |
| Delegation uses different provider | Check `delegation.provider` / `delegation.model` in config |

## Persistent Switch
The `hermes config set` commands persist across sessions. No `/reset` needed for config changes — they take effect on next agent instantiation.

## Related
- `hermes model` — interactive model/provider picker
- `hermes config edit` — open full config in $EDITOR
- Provider setup: https://hermes-agent.nousresearch.com/docs/integrations/providers