# Dispatching builds from referral science

Route from research findings to organism build lanes. Applies whenever a
referral was ingested for system evolution.

## Decision order
1. If findings map to new mechanisms with negative free energy (worth
   building), dispatch them NOW — same turn, before replying.
2. Ledger write path first: `gates/task_ledger.py` `submit()` with a flow tag
   from `stores/flow-registry.json` (research-driven builds = FLW-RESEARCH).
   Raw `INSERT INTO tasks` is refused by the single-write-path gate.
3. Ledger write-locked (BEGIN IMMEDIATE contention from concurrent daemons)?
   Retry once with busy_timeout; still locked → fall back to
   `operator_bus.post(from="hermes", to="glia", type="build_request", …)` with
   the full build spec — the bus post is the receipt; read back the msg id.
4. Build spec must be self-contained: file paths, table schemas, verification
   commands (py_compile + a live query), the evidence source (which digest/mapping
   doc), and the instruction to post a completion receipt from a fixseat identity.

## Ledger submit gate: canonical vocabularies, flow codes
The GENOME block validator rejects free-text in `body=` (must be a canonical
system: circulatory, sensory, metabolic, nervous, network, regulatory, …) and
`8d=` (must be a canonical dimension: accuracy, adaptability, alignment,
coherence, consensus, coordination, efficiency, latency, load_balance — NOT
'robustness', NOT 'feedback'), and `--flow` must be an exact code from
`stores/flow-registry.json` (there is no FLW-INFRA; infra-shaped builds ride
FLW-INTAKE). Write payloads from those lists FIRST — each rejection costs a
full round trip — and when rejected, fix the payload and resubmit: never
bypass or shop for a looser lane.

## Bus law gate: limit claims need raw counters
The law gate (checked inside operator_bus.post) flags Q1 FABRICATION when body
text states failure/limit counts (HTTP codes, "timed out", "exhausted",
"budget") without raw counters. Phrase as "N of N events (ids, api_call counts)"
and append "cause: unrecorded" when the underlying cause has no counter. Write
bus bodies in that shape first time — the gate blocks otherwise.

## Seat dispatch discipline
- delegate_task refuses when the Sherman route is >5 min old — re-run
  specialist_gate.py --route before dispatching.
- Split multi-defect briefs: one seat with a many-part brief times out at the
  1800s wall mid-surgery. Check the live transcript tail + py_compile touched
  files before re-dispatching — partial work usually survives; send a
  verify+complete seat over it rather than restarting from zero.
- Provider overload (429-class) kills a seat before any work: re-dispatch the
  identical brief once.
- Seats complete only on receipt evidence read back from the bus, never on
  self-report.

## Never re-trip fixed defects
Auto-restarts are launchd KeepAlive: if a service is down, wait ~10s for
auto-relaunch instead of hand-starting (hand-started instances block the
managed one). Veritas resume/state_path defects are fixed — see the
ceo-referral-intake-route skill for the list; don't workaround them again.

## Overlap note
ceo-referral-intake-route (operations) covers the same referral territory from
the delivery/gating side; this file covers the build-dispatch side. Prefer that
skill for comment/answer lanes.
