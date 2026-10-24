---
name: ecosystem-catalog-operations
version: 1.0.0
author: hermes
license: MIT
description: Use when maintaining the ecosystem slot catalog.
metadata:
  hermes:
    tags: [ecosystem, catalog, slots, surfaces, cron, mosaic-os]
    related_skills: [benchmark-fleet-stack-selection, hermes-cron-scheduling]
---

# Ecosystem Catalog Operations

## When to Use
- Syncing, pruning, or adding slots to ecosystem-catalog.db
- Building or revising the /ecosystem or /stacks surfaces (or their JSON API)
- Wiring an external sibling system (benchmark runner, security harness) into the catalog
- Scheduling or repairing the hourly no-agent sync cron

## What This Is
The ecosystem catalog is the inventory side of stack selection: every pickable unit in the organism, kept live 24/7 and surfaced as the analytics face for the benchmark system. Companion to `benchmark-fleet-stack-selection` (measurement side).

- **Store:** `your-org/your-stack/stores/ecosystem-catalog.db` (table `slots`)
- **Tool:** `your-workspace/ecosystem_catalog.py` (sync-openrouter / add-slot / lanes / slots)
- **Surfaces:** `:port/ecosystem` (catalog) and `:port/stacks` (measured stacks per task class), served by `your-workspace/boards/task_calendar_boards.py`
- **Ring:** `your-org/your-stack/harnesses/harness-registry.json`

## Always-On Rules

1. **The unit is a SLOT, not a model.** Compound key: model + harness + thinking level + route. The same model at a different thinking level or on a different harness produces different outputs, so it is a different slot and must be listed separately. Thinking vocabulary is normalized: none|minimal|low|medium|high|xhigh|max (OpenRouter-normalized effort scale; store the capability spread, materialize per-effort rows only when measured).
2. **Whole-ecosystem scope.** When the principal asks for the ecosystem view, the deliverable is every harness lane and every slot family, not one task class. A single task-class lane (e.g. voice only) reads as missing the point entirely, even when technically correct.
3. **Measured never guesses.** Slots carry status live/measured/unprobed/dead; the selector surface ranks only from measured runs in `benchmark-fleet.db`. Unmeasured layers display UNMEASURED, never a recommendation.
4. **Freshness is structural.** Catalog re-syncs hourly (no-agent cron); surfaces re-read the store on every page load. Never bake counts or statuses into HTML.
5. **Snap-connect, never rebuild.** Sibling external systems (benchmark runner, cyber/security harness) integrate through two contracts only: (a) read slot inventory as JSON at `GET /ecosystem/api/slots`; (b) write run rows into `benchmark-fleet.db` as (task_class, layer, model, harness, metric, value, unit). A new sibling system registers as a new harness lane in harness-registry.json plus its slots; the surface picks it up on next read with zero code changes.

## Procedure

### Hourly sync (no-agent cron)
1. Script must live in `<agent-home>/scripts/` — no-agent cron resolves script filenames ONLY in that directory (a script elsewhere fails with 'Script not found' while the job shows green in the list).
2. Creating the job: `hermes cron create` with `--no-agent` requires `--script` (the script IS the job; prompt is ignored). If the CLI stalls, edit `<agent-home>/cron/jobs.json` directly: append a job dict with a fresh uuid-hex id, schedule `{"kind":"interval","minutes":60}`, `"script": "<name>.sh"`, `"deliver": "local"`, `"no_agent": true`, `"enabled": true`; verify with `hermes cron list`, then fire once with `hermes cron run <id>` and read the output file under `<agent-home>/cron/output/<id>/`.
3. Sync script pattern: run `ecosystem_catalog.py sync-openrouter`, then prune openrouter rows not seen in the last 2h (delisted upstream). Failure-only output: silent when healthy, per ops law.

### Dedup law (do this at store creation)
4. Create a unique index on `(model, harness, IFNULL(effort,''), IFNULL(route,''))` BEFORE the second sync, and make the sync an upsert (`ON CONFLICT ... DO UPDATE`). A plain `ON CONFLICT DO NOTHING` insert plus an hourly cron silently multiplies rows every hour.
5. The upsert must preserve `status='measured'` (never let a sync downgrade a measured slot back to unprobed) and refresh updated/pricing/context/modality fields.

### Adding a lane
6. Own-lane slots (zcode coding-plan LLM, local whisper/VAD, oauth image lanes) go in via `add-slot`; vendor-catalog models come from sync. Fix modality by name when the source API returns list-valued output_modality (image models otherwise land as text).

## Surface DNA (the OS identity, revised)
the OS-branded surfaces use the the OS identity from `your-org/organism/brand/mosaic-os/`; the law carrier is `validate_identity.py`.
- Palette lock: #071620 night background, #0a2e2e cards, #4ad6b4 teal accent, #d8e8e4 text, #0d8b6e deep teal.
- Gold #ffd700 is EXCLUSIVELY the live/unread-state dot; never a general accent, never headings.
- Sora for display, Manrope for body and numbers (tabular-nums, never mono), breathing glow on headline stats, gold live-dot at top.
- When the principal says 'use our DNA, the revised DNA, not the outdated DNA', this set overrides older phenotype tables; run the validator's palette check against the shipped CSS as the mechanical gate.

## Pitfalls
- Scope rejection loop: a per-task-class stack view will be rejected as 'just voice' — build the full taxonomy (ring harnesses with capability counts, slot lanes per harness, thinking levels, domain ownership) in one pass, then let task-class stacks live inside it.
- Self-duplicating cron: without the unique index + upsert, hourly sync inflates the catalog (hundreds of ghost rows within hours). Always re-run sync twice during setup and assert the count is stable.
- A green `hermes cron run` receipt says 'silent (empty output)' for healthy failure-only jobs — that IS success; a 'script failed' note means the path lookup failed, not the sync logic.
