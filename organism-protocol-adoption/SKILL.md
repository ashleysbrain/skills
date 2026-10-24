---
name: organism-protocol-adoption
description: Adopt MCP/A2A-style protocol standards into the OS OS.
category: devops
---

# Organism Protocol Adoption

Use when the task is: "research protocol X / the new version of X" followed
by "implement it in our system" where X is an industry standard (MCP, A2A,
AGNTCY, OTel). The deliverable is a WORKING, live-verified loop in the
organism — never a research summary alone.

## Binding principal preferences (violated-then-corrected 2026-08-20)

1. **Provenance discipline.** External standards and internal architecture
   iterations are NEVER blurred. If the industry calls a spec revision
   "2.0", that label refers to THEIR spec, not to any internal iteration of
   ours. Lineage must be unambiguous: their spec -> our digest -> our
   adoption. Bespoke internal designs that duplicate an existing standard
   get killed, not versioned (ConnectorBase -> superseded by MCP-native,
   bus #2573 -> #2574).
2. **Implement, don't narrate.** "don't just talk about it. this is the
   self-evolving self-healing element." A digest posted to the bus is an
   intermediate artifact, not the deliverable. The deliverable is code on
   an organism surface with live-verified output.
3. **Full the OS methodology on every build.** Elite layered specialists
   (stacked-PhD DS names, one brain per microtask), physics gates,
   microtask FLW, run-record entries with graded claims, live verification.
   Protocol adoption without the methodology is hollow.

## Workflow: the microtask ladder

Split adoption into microtasks, each owned by a DIFFERENT elite brain
(rotate; never one generalist pass):

- **MT-digest** (e.g. the specialist engine): fetch the spec changelog from the
  PRIMARY source (`curl` the official spec site; do not trust blog
  summaries). Extract: new mechanisms, breaking changes, deprecation list
  + removal window, security changes. Post digest to the bus amending any
  in-flight build requests it affects.
- **MT-implement** (e.g. the specialist engine for OS/protocol surface): patch the
  organism's server/adapter to speak the new era. Keep legacy
  compatibility (era negotiation) — clients on old versions must not
  break.
- **MT-probe** (e.g. the specialist engine): build a prober that interrogates the
  whole fleet with the new mechanism (e.g. `server/discover`), writes
  append-only snapshots to
  `~/your-org/organism/registry-live/`, and posts
  TRANSITION-ONLY drift alerts to the operator bus.
- **MT-sense** (e.g. the specialist engine): wire a `sense_*` function into
  `real_sensors.sense_all` reading the prober snapshot. Self-refreshing:
  stale snapshot -> run prober inline on the existing self-healing launchd
  tick. NO new cron.

## The self-healing composition pattern (no new cron)

principal rule: no new the operator agent crons by default. Compose instead:

1. Prober = standalone idempotent script, runnable on demand.
2. Sensor (`real_sensors.py`) reads the prober's snapshot; if older than
   one self-healing tick (900s), the sensor runs the prober inline (quiet
   mode).
3. The existing launchd daemon `com.your-org.self-healing-loop`
   (StartInterval 900) carries the whole loop for free.
4. Drift alerts: transition-only. Steady-state dead servers live in the
   snapshot; re-alerting them every tick is polling theater (fired twice
   in one session before being caught — see pitfalls).

## Live-verification standard

For a stdio MCP server: pipe JSON-RPC lines into the real process and
inspect the output. Minimum battery:
- new-era RPC (e.g. `server/discover`) answers with identity + versions
- stateless call (no `initialize` handshake) executes a real function
- legacy `initialize` still negotiates
- subscription/registration RPC issues a stable id

For sensors: run `real_sensors.py`, then a full `sense_all -> score ->
detect` cycle, and confirm no false alerts. Record GRADE A only with
inspected output, and list DISCLOSED LIMITS (e.g. subscriptions register
but never emit on stdio; tasks extension "planned", not faked).

## Pitfalls

- **Steady-state re-alerting.** Alerting on `dead_now` every tick spams
  the bus. Alert on CHANGE (died/revived/era_upgraded/identity_changed/
  disappeared) plus a one-time baseline on first run only.
- **Canonical paths vs bridges.** `~/your-workspace` holds bridge
  symlinks; `patch` through a symlink resolves to the canonical file under
  `~/your-org`. Derive snapshot/output paths from the CANONICAL
  organism root (`~/your-org/organism/`), and verify with `find`
  before trusting a sensor's neutral defaults — a path mismatch reads as
  all-neutral telemetry and looks like "no data" instead of "wrong path".
- **Don't invent scored dimensions.** A new sensor rides as telemetry-only
  in `sense_all` until the principal settles the taxonomy (6+1 pending). Never
  mint a scored dimension to make a feature look bigger.
- **Disclose, never fake.** Registering subscriptions without emission, or
  declaring extensions "planned", must be stated in the run-record — not
  hidden.
- **Prober subprocess pattern.** Use `subprocess.run(input=...)`, not
  `Popen` with pipes (Pyright flags it and it deadlocks); probe stdio
  servers by writing all requests up front and parsing the first `result`
  line.
- **Disabled servers are config truth.** Probe only enabled entries; a
  server missing from the snapshot is usually disabled, not dead.
- **Partial patch hazard on symlinked files.** A `mode='replace` patch
  anchored on a function HEADER can match and delete the header while the
  body stays — always re-read after patching and restore immediately; the
  lint/diagnostics catch it, but only if you look.

## Reference

- `references/mcp-2026-07-28-stateless-era-spec.md` — digest of the MCP
  2026-07-28 revision (mechanisms, deprecations, error-code renumbering)
  plus where each landed in the organism (server v1.2.0, prober, sensor).
