---
name: tech-terraform
description: Assimilate external tech into the OS OS via 6 gated stages.
version: 1.1.0
author: the operator agent Agent
license: MIT
metadata:
  hermes:
    tags: [terraform, external-tech, registry, probe, mosaic-os]
    frozen_from: /<workspace>
    panel: "v1 6/6 UPHELD 2026-08-21; v1.1 deltas 1-7 applied same day (QA pass 2: Lamport/Bridgman/Scheffer/Andreasen + cross-model critic gpt-oss-20b KILLED the aspirational F-gate)"
---

# TECH-TERRAFORM — external-tech assimilation into the OS OS

## When to Use

Any task involving an EXTERNAL technology — harness, mesh, bridge, SaaS, API, model,
business — "how does X work", "connect X", "evaluate X", "adopt X", or a fresh
`tech.discovered` event. NEVER answer capability or behavior questions about external
tech from memory. The founding failure: a prior-based UI answer (Notion "Connections"
misdiagnosis, 2026-08-21) that cost a principal round-trip.

Authoritative full text: `~/your-workspace/technology-registry/PROTOCOL-TECH-TERRAFORM.md`.
Registry: `~/your-workspace/technology-registry/` (schema v0.4).

## Lifecycle

`unprobed -> manual-digested -> probed -> boundary-pushed -> terraformed -> evolved -> retired`
with `parked` reachable from any stage (free-energy escape hatch, reversible).
v1.1: `retired -> rediscovered` and `evolved -> terraformed` are legal (revival keeps
measured history + boundary map; re-probe re-enters the FULL terraform contract).

## The 6 stages

1. MANUAL — vendor primary docs for the CURRENT version (URL + date). Docs feed ONLY
   `claimed` with source stamps; memory goes to `unverified_notes`. Emit `tech.manual_digest`.
2. CHATTER — forums/issues where reality deviates from docs. Output: cited HYPOTHESES or
   structured negative results, never conclusions.
3. LIVE PROBE — black-box calls; record error bodies verbatim (error-as-documentation);
   NOKEY on missing creds, never fabricate. Execution-record law: every `measured` value
   resolves to a run (exact call, timestamp, raw response, environment, probe identity —
   the auth context; never generalize across tenants). Emit `tech.measured`.
4. BOUNDARY PUSH — adversarial edges (wrong auth, cross-tenant, UA drift, rate limits,
   UI drift). Each probe is a decisive test with mutually exclusive outcomes; if no
   outcome would change belief, the probe is theater. Boundary map rides the
   `tech.measured` payload.
5. TERRAFORM — fold into the OS OS. Four artifacts, all four or park: (a) bridge organ
   running MEASURED behavior, (b) Sherman routing entry, (c) version-pinned agents.yaml
   contract, (d) healthy-tech gate verdict quoting measured evidence (default-on
 surveillance, addictive mechanics, dark patterns = reject regardless of capability).
 v1.1 discriminating checklist — any YES = reject; zero citations = invalid verdict:
 (1) default-on exfiltration? (2) engagement-optimizing loops? (3) deceptive UI?
   Plus flow registration: at least one named lattice flow step consuming the organ
   (anti-orphan triple: live + routed + used). Answer the imagination question in one
   line: "what does this make possible that we did not set out to do?" Resolve all
   serendipity notes. Emit `tech.terraformed`.
   v1.1 rate card: terraforming a LIVE business surface runs canary <= 10% of dispatch
   for >= 48h dwell; any degradation signal AUTO-PARKS (binding reverts to prior
   version). No exception.
6. RUN RECORD — append method name with execution record to the audit ledger; event in
   `events.jsonl` (flock + fsync). Method names appear only with execution records.

Free-energy gate before EVERY transition (v1.1 — operational, no longer aspirational):
run `free_energy.py evaluate()` in the registry dir — operator = the transitioning
agent, never "system"; cost in agent-minutes; T 0-10 from NAMED raises only (base 5.0,
vendor_version_bump +2.0, chatter_spike +2.0, user_need_ping +1.0); verdict appends
to free-energy.jsonl (flock+fsync). F <= 0 -> GO; F > 0 -> park WITH re-entry
conditions. A stage-5 terraform gate must show gate_check() GO on file: no GO, no
terraform (cross-model critic escalation, binding).

## Hard laws

- Claimed never measured; ranking reads only `measured`; unprobed entries never rank.
- Decisive-test law at stages 3-4.
- Production telemetry triggers re-probe but never writes `measured`.
- Version-pinned bindings: `tech.evolved` invalidates flow bindings citing the old version.
- Event-driven propagation, never cron; watchers are launchd KeepAlive daemons.
- PERSONA zones never write back through any terraformed organ.
- Serendipity capture: unexpected capabilities -> `tech.serendipity` note; must be
  promoted to hypothesis or explicitly dismissed before `terraformed`.

## Defect taxonomy

Prior-based answer, vendor-claim capture, probe fabrication, orphaned organ, doc-drift
snapshot, provenance leak, event-log race/dup, cross-kind contamination, silent NOKEY,
big-bang promotion (live without adiabatic DRIVEN-tier trace).

## Verification checklist

- Every measured field has run id + raw response + probe identity.
- Every claimed field has source + source_verified stamp.
- Deviation ledger cites sources or records structured negatives.
- Boundary edges each have decisive test + outcome or next-test pointer.
- Terraform: organ alive + route resolvable + flow registered + healthy-tech verdict
  quoting evidence.
- Event emitted with monotonic unique seq; replay reproduces state.
