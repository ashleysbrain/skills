---
name: hermes-model-lane-routing
description: "Switch the operator agent model lanes; sweep pins, verify endpoints."
category: operations
version: 1.0.1
created: 2026-08-14
created_by: agent
author: the operator agent Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, model-routing, config, llm-vendor, glm]
    related_skills: [model-selection-for-agents, model-routing-rules, model-recommendation-maintenance]
---

# the operator agent Model Lane Routing

## When to Use

- Upgrading or switching the model in `<agent-home>/config.yaml` (any provider)
- Splitting routing into default vs elite lanes (main thread vs delegated
  specialists)
- Verifying a new model ID actually exists on a provider endpoint
- Auditing which model each lane/pin site currently serves
- Troubleshooting "the model change didn't take effect"

Configure and verify which model serves which class of work in the operator agent. Covers
model upgrades, two-lane (default vs elite) splits, full pin-site sweeps, and
endpoint verification before pinning.

## Current Lane Policy (principal directive 2026-08-14)

- **Default lane `glm-5.2`** — `model.default`, provider `llm-vendor`,
  base_url `https://api.z.ai/api/coding/paas/v4`. All lower-priority work:
  chat, cron (jobs with no per-job override), routine ops.
- **Elite lane `glm-5.3`** — `delegation.model`, provider `llm-vendor`. Heavy tasks
  requiring elite credentials: security, architecture (OS/kernel/scheduling),
  advisory panels. Every spawned subagent/specialist inherits it.
- **Routing rule:** the main thread stays at the economy tier; escalate by
  DELEGATING (subagent inherits the elite model), not by answering in-thread.
- **Fallback chain (do not blindly bump):** nvidia-nim `z-ai/glm-5.2` →
  llm-vendor `glm-4.7` → llm-vendor `glm-5.3`. NIM's catalog lagged one release behind
  llm-vendor's endpoint; only bump a fallback entry after confirming that provider
  serves the new ID.

## Procedure: model change sweep

1. **Read current state**: `<agent-home>/config.yaml` sections `model:`,
   `delegation:`, `fallback_providers:`. (`hermes config` output may be
   empty in some shells — read the file or use `execute_code` subprocess.)
2. **Verify the target model ID on the endpoint BEFORE pinning** — see
   `references/catalog-lag-probe.md`. Provider `/models` lists go stale
   before the endpoint does; a 10-token chat probe is the only real proof.
3. **Enumerate every pin site** (partial sweeps silently leave old models
   active):
   - `model.default` (main lane)
   - `delegation.model` (subagent lane)
   - `fallback_providers[]` entries — model IDs are provider-namespaced;
     `z-ai/glm-5.2` on nvidia-nim ≠ `glm-5.2` on llm-vendor
   - per-cron-job `Model:` overrides (`hermes cron list`; no override =
     inherits `model.default`)
   - custom provider blocks with own `base_url` + model
4. **Apply** via `hermes config set <key> <value>` (rc 0 + "✓ Set" confirms).
5. **Propagate**: model config is snapshotted at session start — running
   conversations keep their old model. Changes reach the next session, all
   future delegations, and platform sessions after `hermes gateway restart`.
6. **Verify propagation**: gateway PID must actually change. `hermes gateway
   start` refreshes a stale service definition but may NOT swap the process;
   `hermes gateway restart` does. Confirm new PID in `hermes gateway status`.

## Pitfalls

- Catalog absence ≠ model absence. z.ai's `/models` omitted `glm-5.3` while
  serving it (a 5.2 request even echoed `glm-5.3` back — the provider was
  already routing traffic to new hardware).
- A "successful" `gateway start` after a config change can still be the OLD
  process serving the OLD routing. Check the PID.
- Terminal tool returning empty output for even `echo hello` = output-capture
  failure, not command failure (rc was 0). Switch to `execute_code` with
  `subprocess.run(..., capture_output=True, text=True)` and continue; do not
  conclude commands are failing.
- Model upgrades are lane-aware: per the directive above, a new flagship goes
  to the ELITE lane (delegation) while the default lane may deliberately stay
  one release back for economy.
- **`model:` in config.yaml is a NESTED DICT** (`base_url`/`default`/
  `provider`/`max_tokens`), not a flat `model: glm-x.y` string. Code that
  does `cfg["model"] = "glm-5.3"` or reads `cfg.get("model")` as a string
  will silently no-op or corrupt the config (2026-08-27: a hand-written
  auto-upgrade daemon had exactly this bug — it compared a dict to a string,
  never fired, and its write path would have flattened the dict). Read
  `cfg["model"]["default"]`; write `cfg["model"]["default"] = ...`.
- **Downgrades must self-heal upward (principal directive 2026-08-27).** When
  bandwidth/rate limits force a drop to a cheaper model (or smart_model_routing's
  cheap_model takes over), the system must raise back to the flagship
  (e.g. glm-5.3) as soon as the provider is healthy — never wait for the principal
  to do it manually. Implemented as launchd agent
  `com.your-org.bandwidth-upgrade` (15-min interval): probe the
  provider with a 1-token completion; on 200, raise BOTH `model.default` and
  `smart_model_routing.cheap_model`; silent when at target or still degraded;
  raise event recorded to `<agent-home>/logs/.bandwidth-upgrade-state.json`.
  `smart_model_routing.cheap_model` is a SECOND pin site a downgrade sweep
  must include — raising only `model.default` leaves simple tasks on the
  cheap model.

## Support files

- `references/catalog-lag-probe.md` — exact probe recipe (models list +
  minimal chat completion) with the 2026-08-14 worked example.
- `references/bandwidth-upgrade-daemon.md` — self-healing model raise-back
  daemon (probe → raise both pin sites → state file), 2026-08-27.

## Overlap note

`model-selection-for-agents`, `model-routing-rules`, and
`model-recommendation-maintenance` cover adjacent territory but are
user-owned (not curator-managed). If the user runs
`hermes curator adopt` on them, this skill's procedure should be merged into
`model-recommendation-maintenance` and this one retired.
