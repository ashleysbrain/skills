---
name: living-research-hub-project
version: 0.1.0
category: software-development
description: Use when continuing the Living Research Hub build.
author: the operator agent Agent
license: MIT
metadata:
  hermes:
    tags: [research-hub, website, engines, citation, open-core]
    related_skills: [elite-panel-chain-of-custody]
---

# Living Research Hub Project ("Meet the Engines")

## When to Use
Any work touching the Divinity Science public research hub: the live engines
atlas ("Meet the Engines"), public analytics, citation infrastructure, engine
profile pages, the interactive researcher sandbox, or the open-core IP
boundary. The principal framed this as a LONG-TERM background build, run
wave-by-wave with panels (D7), so every pickup must inherit the charter and
laws below instead of re-deriving.

## Project identity (from principal voice note 2026-08-26, dissection on disk)
- **Charter**: task-ledger T-260826-0101 (kind=build). Dissection (8 directives
  D1–D8): `/<workspace>`.
- **Wave 0 artifact**: `/<workspace>`
  (taxonomy proposal, 6-wave plan, panel roster). Ratification status as of
  2026-08-26: presented to principal, NOT yet ratified — panel did not dispatch.
- Directives in one line each: D1 public "Meet the Engines" section; D2 live
  evolving data (the diff IS the content); D3 human structure with rabbit-hole
  depth; D4 citation-grade hub (stable identifiers + versioned snapshots +
  live analytics); D5 researchers send work through our engines (sandboxed);
  D6 open core (watered-down public versions, deep IP stays DS); D7 wave-by-wave
  panels; D8 plan-first long-term build.

## Ground truth (measured 2026-08-26 — re-measure, never narrate)
Run `scripts/registry_census.py` before ANY site-structure or copy decision:
- FLEET_REGISTRY (`/<workspace>`) is the
  machine source of truth for engine counts, ports, and DS-ECS codes.
- Measured at Wave 0: 139 engines, 121 unique ports; body-system skew nervous
  78/139 (~56%). **Consequence: flat "browse by body system" taxonomy is dead
  on arrival** — one bucket swallows the visitor. Taxonomy must be
  function-first (proposed halls: PERCEIVE / THINK / REGULATE / MOVE /
  CIRCULATE / REMEMBER+GROW) with body-system + DS-ECS code as drill-down.
- Any public claim ("N engines running") must come from a live registry pull
  in the same session, per anti-fluff law T-260826-0099.

## Wave plan (each wave = one drill-down, gated, principal-reviewed)
W1 live-data spine (public API surface) → W2 citation infra (versioned
snapshots, stable IDs) → W3 IP/open-core boundary → W4 site build v1 → W5
interactive researcher sandbox (rate limits, abuse, cost, security) → W6
launch + anti-fluff pass on all public copy.

## Laws binding every wave
- Anti-fluff T-260826-0099: no "unlike anything out there" class claims in
  public copy without live-measured evidence.
- Buttons-law: all principal questions render as buttons (short, plain, one screen).
- Open-source gate T-260826-0084 (autonomous market-aligned QA) gates public ships.
- Panel law: principal approves the seat roster BEFORE dispatch; one child, seats
  sequential (chain-of-custody), cross-model critic closes; see
  `operations/elite-panel-chain-of-custody`.

## Thread pickup pattern (proven 2026-08-26)
When the principal says "picking this up from Telegram": session_search the
distinctive phrase from their message (e.g. "living research hub"), scroll the
hit with around_message_id to the minted charter + handoff artifact, read the
artifact from disk, check the sibling message-bus for collisions, THEN work.
Do not re-ask the principal for context they already dictated.

## Pitfalls
- Do not dispatch the wave panel without explicit principal seat-ratification —
  an unanswered clarify = NOT ratified, park and report state flatly.
- Do not surface engine costs, prompts, or internal telemetry on the public
  layer (W1 decides the exact public/internal analytics boundary).
- Registry numbers drift as engines are born — always re-measure; never cite
  this file's 139/121 as current.

## References
- `references/wave0-2026-08-26.md` — full Wave 0 session detail: taxonomy
  rationale, roster, census commands, ledger state.
- `scripts/registry_census.py` — re-runnable FLEET_REGISTRY census
  (`--all` prints the full roster); prints a max-bucket-share warning when a
  flat taxonomy would bury the visitor.
