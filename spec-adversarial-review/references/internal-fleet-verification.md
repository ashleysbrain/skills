# Internal-Fleet Spec Review: Port Verification + Differential Probes (2026-08-19)

From the FLW-BRAINSTORM v0.1 adversarial review (10 findings, 2 critical).
Applies whenever a spec names engines/ports of the local organism fleet
(your-stack, agent-organism, the :80xx block).

## Crack class 1 — WRONG PORT / WRONG ORGAN

v0.1 implied the Wave engine served :port. Live probe: :port is the Ramón y
Cajal nervous-system gateway (DS-ECS-APP-04.00.01), NOT Wave. The real
Kuramoto Wave engine (DS-ECS-SUB-04.03.01, order_parameter in /health) is
**:port** (ds-wave-coaching-engine). This is the port-squat pattern in the
organism-reflex-arc skill (identity-drift class 2) seen from the spec side.

Diagnostic sequence:
1. `curl :PORT/health` — read the self-reported engine/engine_code.
2. If the name doesn't match the spec's claim: `lsof -ti :PORT -sTCP:LISTEN`
   then `ps -p <pid> -o command=` and `lsof -p <pid> | grep cwd` to find the
   serving directory.
3. Correct the spec with the pinned port + engine_code + serving dir.

## Crack class 2 — CAPABILITY ASSUMED BUT UNMEASURED

v0.1 claimed "Wave engine measures resonance per framing" as if verified.
Honest check = differential probe of the claimed capability:

```
register 5 oscillators freq=1.0 (coherent swarm, population "coh")
register 5 oscillators freq=0.2..3.8 spread (incoherent swarm, population "incoh")
POST /v1/coupling/set {"K": 3.0}   -> 60x POST /v1/tick
GET /v1/sync_state  -> order_parameter r
POST /v1/coupling/set {"K": 0.01}  -> 60x tick -> re-read r
```

Result: r=0.494 (coherent) vs r=0.301 (incoherent) — the engine genuinely
differentiates, so the spec stage may cite it. Had the two reads matched, the
stage would be a propagation gap (capability named, nothing measured).

RULE: a spec citing a fleet engine's capability must either attach the probe
output or mark the capability UNVERIFIED until probed. Schema quirks found
live: /v1/coupling/set takes {"K"} not {"global_coupling"}; /v1/tick takes {}
(empty body) — always read requestBody schemas from /openapi.json before
probing.

## Related verified-fleet map (2026-08-19, for port pinning)

- :port Ramón y Cajal nervous-system gateway (organism/health aggregator)
- :port Wave / Kuramoto (oscillators, coupling, order parameter) — REAL
- :port the specialist engine "Genius" (product nucleation: layers, nucleate, engine,
  feature, sprint, gate, rollback) — the BUILD organ for unified loops
- :port self-reports DS-ECS-ORG-11.04.01; canonical dir
  your-org/the operator agent/ds-genesis-engine
- VERITAS process = 19 stages (0→7.5 incl. human checkpoints) in
  your-workspace/veritas_process.py (STAGE_ENGINES map at ~L112); specs
  should REUSE these stages, not invent parallel gates
- :port conduction daemon (poke-driven) — loop nervous system, verify with
  /health pokes/cycles counters
