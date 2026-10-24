# Flow-registry audit battery — PROCESS-FLOWS.md + flow-registry.json QA

Use when running an adversarial/QA pass over the live process-flow pair
(`your-stack/PROCESS-FLOWS.md` + `stores/flow-registry.json`). Developed
in the 2026-08-20 Simon/Deming/Alexander pass that caught 3 defects the
flow-sync gate had passed green.

## The battery (in order)

1. **Constitution check.** PROCESS-FLOWS.md's own rule: "Unverified flows
   do not get sections." Scan EVERY flow section for a verification stamp
   (heading OR body). Defect class found: six organ flows (PANCREAS,
   SPLEEN, MARROW, LIVER, REPRODUCTIVE, IMMUNE) had passing selftests
   that were never folded back into stamps — verification existed,
   recording didn't.
2. **Heading-collision scan.** `grep -n "^##* Flow" PROCESS-FLOWS.md`,
   sort by number. Two sections numbered "Flow 12" (ESTRA + ACTION
   SELECTION) made every external "Flow 12" citation ambiguous. Fix:
   renumber the NEWER section (ACTION SELECTION -> 16, TONGUES -> 16a) and
   keep RUN-RECORD citations consistent.
3. **Registry-vs-doc symmetric difference.** Extract FLW-* codes from doc
   and registry; diff. `gates/store_gate.py --flow-sync` enforces this
   BUT is blind to headings that carry no FLW code (that's how the
   collision survived). Mint missing codes into the registry
   (code/name/version/lane/stages/doc keys), re-run the gate, then
   re-census independently — beware regex overreach: body doc-cites
   (`Doc: docs/FLW-X-DESIGN.md`) are not headings.
4. **Earn the stamp before writing it.** Run the module selftest
   (`python3 <module>.py --selftest` via subprocess with Python-level
   timeout — shell `timeout` does not exist on this macOS), probe engine
   health ports, read the latest autonomy report. Stamp with the ACTUAL
   numbers (e.g. "selftest 11/11"). Honest gate-level states count as
   verification: "scheduler row held queued, no fabricated measurement"
   IS Flow 4a's verification record.

## Dissolved-hypothesis discipline

Record hypotheses that failed with evidence, as DISSOLVED — not as finds,
not silently dropped:
- "fanout 61 events behind" = two different `events.jsonl` streams
  (telemetry/events.jsonl vs technology-registry/events.jsonl). Resolve
  the exact path the code reads (mosaic_chain_executor.py
  REGISTRY_EVENTS) before declaring lag.
- "pokes 1863 vs cycles 1265 = 32% loss" = documented pending-flag
  coalescing in the conduction daemon header. By design.

## Schema note

task-ledger.db `task_events` columns: seq, task_id, ts, actor, actor_kind,
event, detail (the timestamp column is `ts`, not `timestamp`). Age of
CLAIMED work = claim event ts, not tasks.created_at.
