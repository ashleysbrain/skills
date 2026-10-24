---
name: organ-body-coverage-and-dark-seats
description: Use when auditing body coverage or before any organ build.
version: 1.0.0
author: curator
license: MIT
metadata:
  hermes.tags: [organism, registry, census, dark-seats, isomorphism]
  hermes.category: devops
---

# Organ Body Coverage and Dark Seats

## When to Use

- Asked "what layers/body systems are we missing?" — run a coverage census.
- About to build ANY organ, layer, engine, or capability — run the
  historical-record check first.
- A subagent or report claims something is "missing" — classify it before
  accepting the claim.

Governs two coupled task classes: (1) whole-body coverage audits, and (2) the
pre-build gate for ANY organ, layer, engine, or capability claim ("we need
X" → check whether X is already seated-dark).

## Procedure A: registry liveness census

1. Parse `organism/ENGINE_REGISTRY.yaml`. The top level may be a LIST of seat
dicts (directory, engine_name, port, serving, scientist, body_system,
ds_ecs_code) — write the loader to handle list OR dict; `.get('engines')`
raises AttributeError on the list shape.
2. **Liveness ground-truth BEFORE classification** — probe every declared
port (socket connect, then `/health`) rather than classifying from the
`serving` field. The field rots WHOLESALE: a census once reported ~6 lit of
163 seats while live probes found ~69 of 137 declared ports listening. When
the field and the probes disagree at scale, resync the registry field to the
measured truth (backup the YAML first) — a census that leaves the registry
lying reproduces the error in every downstream reader.
3. Classify each seat: port answering = LIT, port dead = DARK, `serving` used
only as a prior. Report per body-system: seat count AND lit count (coverage
ratio), plus canonical systems with zero seats. Both numbers per system —
the ratio is the finding (163 seats, 20 systems, nervous 90-seat monoculture
while entire systems serve nothing).
4. Port-truth on ANY seat being wired or lit: a declared port may be LISTENING
but owned by a different engine. Probe `/health` and read the `engine` field
in the payload — trust the payload over both the registry and the port
table.

## Procedure B: dark-seat verdicts

For each dark seat (or the subset in scope), open its directory and classify
with evidence, never from name alone:
- KEEP (light it): real code + real owner-flow; cite the main module path.
- MERGE (fold into sibling): duplicates a sibling seat's function; name both.
- RETIRE (husk): stub/empty/misleading; cite size or missing src evidence.

## Procedure C: missing-layer classification

Every "missing" capability gets exactly one label before anything is built:
- SEATED-DARK: a registry seat already owns it (name the seat).
- TISSUE-ELSEWHERE: the function lives inside another organ or script (name it).
- TRULY-MISSING: no owner anywhere, after the checks below.

## The historical-record check (before ANY organ/capability build)

Run BEFORE writing code or minting a build, in this order:
1. Registry dark-seat grep: search seat names + scientist + role fields for the
capability's methodology keyword (tipping points, statistical control,
forecasting, queue ordering...). Most "missing" capabilities are seated-dark.
2. Prior mapping canon: prior body-systems mapping docs, organ-mapping and
body-mapping skills, architecture-doc indexes.
3. Law corpus: law-block headers for the domain (isomorphism-first class laws).
4. Skills named for the workflow class (engine creation, organ seating).

A layer that prior canon already mapped is a DUPLICATION, not a gap. When a
dark seat owns the methodology, the new build must CONSUME that seat's
engine/methodology, not re-implement the math — new code does sensing,
scoring, and bound actions only; the seated scientist keeps the physics.

## Procedure D: whole-layer verification (architecture review)

When asked to verify the layers themselves — built correctly, missing
anything — subtractive discipline governs:
1. Take the layer set from the canon terminology spec's layer tree, never
   from memory — probe every written branch; a tree written from recall
   duplicates or drops branches.
2. Probe each layer live: sockets + `/health` for engines, pool config for
   models, process census for harnesses, status counts for the bus, node
   list for mesh, file census for stores. Report measured state only.
3. Apply the four dynamics per layer as defect detectors: mastermind — one
   vendor / one machine / one live reviewer at a layer is a monoculture
   defect; synergy — a producer with no consumer (engine lit, no caller)
   is a wiring debt, name both ends; symbiosis — missing receipts or
   redundancy between layers; entourage — no standby or peripheral ring.
4. Default answer to "are we missing anything" is structural completeness
   with unwired adjacencies: add or restructure ONLY when a canon branch has
   no live tissue anywhere. Wiring precedes lighting — lighting more engines
   into an unwired body makes a brighter dark room.
5. Route each defect to the layer's owning seat. The verifier measures and
   reports; it never hand-patches another layer's defect mid-pass.
6. Reconcile count drift between sources (registry vs probes, yaml vs
   live): when two live probes disagree by one, disclose the drift — a
   seat flapping between probes is a finding, not noise to average away.

## Pitfalls

- Declaring a layer "missing" from first principles without the registry grep
  — the body births organs faster than it lights them; the default state of a
  missing-looking capability is seated-dark, not absent.
- Re-implementing a seated scientist's methodology because the seat is dark
  — dark means unlit, not unowned; read the seat's engine code first.
- Trusting `serving` or the port table over the /health payload — both drift,
  and `serving` drifts wholesale (13x observed): classify from port probes,
  then resync the registry so the rot does not compound.
- Census numbers without per-system ratios — a total ("163 seats") hides the
  monoculture; the ratio per system is the decision-driving output.
- Verdicts from directory names alone — always open the seat's code.
