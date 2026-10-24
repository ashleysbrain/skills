---
name: living-prompt-layer
description: "Use when maintaining auto-refreshing harness prompt layer."
version: 1.0.0
author: the operator agent Agent
license: MIT
metadata:
  hermes:
    tags: [living-prompt, prompts, harness, registry, fleet, staleness]
    category: devops
---

# Living Prompt Layer

Class: keeping every operating harness's system prompt current with live fleet
state so no hand-written roster goes stale. Generator:
`/<workspace>`. Output: one
generated block injected into each harness prompt surface between strict
markers; static identity/conduct text stays hand-written above it.

## When to Use
- Adding or changing a harness prompt surface; seating a new harness
- A prompt roster is reported stale, incomplete, or missing an organ/engine
- Modifying the generator, its refresh wiring, or its selftest battery
- Seating/renaming organs or engines in ENGINE_REGISTRY.yaml (verify the
  layer renders them)

## Architecture
1. Generator reads ENGINE_REGISTRY.yaml (parses as a LIST of dicts; first
   element may be None — never assume dict-of-dicts) + law-block count, probes
   engine ports live, detects the harness census by probing prompt files.
2. Renders one layer block; writes canonical copies to
   `organism/living-prompt/LIVING-PROMPT.md` and `current-layer.md`.
3. Injects into each harness prompt surface — REPLACE, never append.
4. Refresh wiring: launchd agent every 30 min + harness boot, with a hermes
   cron tick as backup (launchctl bootstrap is blocked from inside the
   gateway; a staged installer script picks the agent up from outside).

## Laws
- REPLACE, never append: block regex spans `<!-- LIVING-LAYER v1 ... -->` to
  `<!-- /LIVING-LAYER -->`; every run strips ALL existing blocks then writes
  exactly one. Stacked blocks = defect.
- COMPLETE roster: every registered engine rendered, grouped by organ system,
  liveness probed live. No previews-as-roster, no top-N truncation, no
  survivorship bias — DOWN engines listed as DOWN (honest-state).
- Organs are first-class: an organ seated on a scientist engine must carry
  the organ name in engine_name/role registry fields, and the layer renders
  an actuation-organs section explicitly. Rendering only scientist surnames
  forgets organs by construction.
- Fail-soft: unreadable registry leaves the last good layer in place and
  alerts the bus; never blank a prompt surface on a bad read.
- Auto-adoption: a census seat with a present prompt file not in CANON
  inherits the layer automatically; orphan blocks in non-canonical prompt
  files are swept to zero, never re-injected.

## Selftest battery (run after any generator change)
Stacked blocks collapse to one; second run is byte-identical; missing prompt
file skipped; unknown seat adopted via discovery; absent seat not adopted;
orphan block swept from alt prompt file; missing alt file ignored.

## Pitfalls
- Append-vs-replace: the first generator version appended a new block per run
  (4 copies accumulated in minutes). Test idempotency by running twice and
  counting blocks before shipping any generator change.
- Registry scientist fields hold FULL names ("Alexander Luria") while prompts
  use surnames — normalize when matching; never assume one form.
- Top-N port previews silently dropped everything past N, organs included —
  render the complete grouped roster; if a preview is kept, label it a
  preview and keep the complete list beside it.
- A harness census built from prose lists under-reports; probe the filesystem
  for prompt files per harness (absent file = "not seated", report honestly).
- Fleet surfaces are judged by completeness: a roster rendering 24 of 163
  engines is "not our fleet" to the principal. Completeness is a hard
  requirement, not polish.

## Related
- ds-engine-registry-maintenance (registry schema + seating)
- organism-engine-lifecycle (seat/revive engines, stale feeds)
