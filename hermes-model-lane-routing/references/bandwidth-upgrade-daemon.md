# Bandwidth upgrade daemon — auto raise-back to flagship (2026-08-27)

principal directive (overnight priority): when models get downgraded due to
bandwidth/rate limits, the system must upgrade back to the flagship
(glm-5.3) as soon as the provider refreshes — the principal must never have to
do it manually.

## What exists (verified live 2026-08-27)

- Daemon: `/<workspace>`
- launchd agent: `com.your-org.bandwidth-upgrade` (StartInterval
  900s, RunAtLoad), log at `<agent-home>/logs/bandwidth-upgrade.log`, raise
  events at `<agent-home>/logs/.bandwidth-upgrade-state.json`.
- Behavior: probe llm-vendor with a 1-token glm-5.3 completion → on HTTP 200,
  raise BOTH `model.default` AND `smart_model_routing.cheap_model` →
  silent when already at target or provider still degraded (healthy =
  zero output, per the failure-only-alert law).

## Existing infra it composes with (do not duplicate)

- `model-failover.py` (<agent-home>) — handles DOWNWARD failover (429/503/529
  → instantly switch provider/model, never retry the same provider). It has
  NO raise-back path; this daemon is the missing upward half.
- `model-health-watchdog.py` (<agent-home>) — log-based detector that ALERTS
  on provider failure signatures (empty response, 402, 429 storms,
  connection errors). Detects state CHANGE only. It alerts; it does not heal.
- `provider_autoheal.py` (your-org/organism) — remaps CRON jobs
  whose provider vanished from config to the fallback primary.

## Bugs hit while building (the training record)

1. **Config-shape bug:** `model:` is a nested dict. First daemon draft read
   `cfg.get("model")` as a string and would have written a flat string over
   the dict — silently no-op'd, and the write path was config corruption.
   Fixed: read/write `cfg["model"]["default"]`.
2. **Second pin site:** after a rate-limit episode, `model.default` can
   already read glm-5.3 while `smart_model_routing.cheap_model` still reads
   glm-4.7 (routing "simple" tasks down indefinitely). Raising only the
   default leaves the system half-downgraded. Always sweep BOTH sites.
3. **API key resolution:** launchd context has no `ZAI_API_KEY` env; the
   daemon falls back to importing hermes_agent config resolution. If the
   probe can't get a key it stays silent (treated as "can't verify health"),
   never alerts-spams.
4. **No pkill on raise:** the gateway reloads model routing per request;
   killing the gateway on every raise is unnecessary violence. (Contrast:
   conduction_daemon on :port DOES need kill+KeepAlive-respawn to serve
   patched HTML.)

## Probe recipe

Minimal chat completion against
`https://api.z.ai/api/coding/paas/v4/chat/completions`:
`{"model":"glm-5.3","messages":[{"role":"user","content":"ping"}],"max_tokens":1,"stream":false}`
HTTP 200 = healthy; 429/5xx = still degraded (stay silent, retry next
tick). See `references/catalog-lag-probe.md` for why a live completion
probe beats the `/models` catalog.
