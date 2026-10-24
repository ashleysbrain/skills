# Pass 6 adversarial QA catalog — architecture + process flows (the OS)

Context: principal directive "do antoher thorough qa on architecture and process
flows mosaic methodlogy. microtasks. adversarial brains. elite layered phds."
Executed as the specialist engine (near-decomposability / doc split-brain), the specialist engine
(feedback control on the conduction spine), the specialist engine (pattern order vs
the doc's own constitution) over `your-stack/PROCESS-FLOWS.md` +
`stores/flow-registry.json`.

Read together with `pass5-defect-catalog.md` so a future adversarial pass
re-checks these classes instead of re-discovering them.

## Defects found and fixed

| # | Brain | Defect | Fix | Live proof |
|---|---|---|---|---|
| A1 | Alexander | 6 organ-flow sections (PANCREAS/SPLEEN/MARROW/LIVER/REPRODUCTIVE/IMMUNE) had NO verification stamps — violating PROCESS-FLOWS.md's own constitution "Unverified flows do not get sections" | Ran the selftests LIVE (7/7 pancreas, 8/8 spleen, 8/8 liver, 11/11 marrow, 4/4 reproductive), probed immune chain engines (Bernard :port, Semmelweis :port, Franklin :port, Mangold :port — all alive), then stamped headings with the real numbers | selftest exits 0 this pass; curl health all alive |
| A2 | Simon | "Flow 12" name collision: ESTRA (08-18) vs ACTION SELECTION (08-19) both numbered Flow 12; RUN-RECORD cited both | ACTION SELECTION -> Flow 16, TONGUES -> Flow 16a | grep: no duplicate flow-number headings remain |
| A3 | Alexander | flow-sync gate BLIND SPOT: `store_gate.py --flow-sync` only checks headings carrying FLW- codes, so uncoded flow headings were invisible — the A2 collision passed green for a day | minted FLW-ACTION + FLW-TONGUES into stores/flow-registry.json | FLOW-SYNC OK; independent census 26 doc codes / 25 registry rows, symmetric diff NONE (26th is a body doc-cite, not a heading) |

## Dissolved hypotheses (recorded honestly, NOT defects)

1. **"fanout 61 events behind"** — compared two DIFFERENT streams:
   `your-stack/telemetry/events.jsonl` (63 provider-outcome lines, Flow
   10 substrate) vs `technology-registry/events.jsonl` (2 seq-carrying
   events, Flow 4 substrate). Registry fanout position 2 = fully caught
   up. Lesson: name-collision on `events.jsonl` across subtrees; always
   resolve the exact path the code reads (`mosaic_chain_executor.py`
   REGISTRY_EVENTS) before declaring a lag.
2. **"pokes 1863 vs cycles 1265 = 32% lost"** — documented coalescing in
   the conduction daemon header (pokes arriving mid-cycle set a pending
   flag). By design, not loss.

## Architecture-QA techniques that worked (reusable)

- **Constitution check (Alexander):** a governance doc's own rules
  ("unverified flows do not get sections") are the strongest audit oracle
  you have. Scan EVERY section against the doc's stated admission rule,
  not just the sections that look wrong.
- **Heading-collision scan:** `grep -n "^##* Flow" doc | sort` by number —
  duplicate numbers mean cross-references elsewhere are ambiguous.
- **Registry-vs-doc symmetric difference:** extract codes from both, diff.
  But beware regex overreach: body doc-cites (`Doc: docs/FLW-X-DESIGN.md`)
  are not flow headings; validate matches against heading position.
- **Stamping discipline:** a stamp is EARNED in the same pass it is
  written — run the selftest / probe the ports / read the report BEFORE
  editing the heading. Never write a stamp for evidence you did not
  personally generate this session. Gate-level honest states count ("row
  held queued, no fabricated measurement" IS Flow 4a's verification).
- **Claimed-task staleness, the two-reader trap:** checking task age from
  `tasks.created_at` overstates age of CLAIMED work; the claim timestamp
  lives in `task_events` (schema: seq/task_id/ts/actor/actor_kind/event/
  detail — column is `ts`, not `timestamp`).
- **macOS harness:** `timeout` is not available in this bash; guard
  subprocess timeouts in Python (`subprocess.run(..., timeout=N)`) instead
  of shell `timeout`.

## Signals surfaced (no defect, routed)

- Registry events idle since 08-17 — G2 probe runner (sibling-agent lane,
  already in autonomy advisory; 15 entries unprobed).
- 171 open ledger tasks, oldest 42h — visible to broker salience; backlog,
  not a bug.

## Meta

- Specialist gate expiry (>5 min) blocked `patch` mid-pass; the documented
  fallback (re-route via specialist_gate.py, then edit via terminal
  Python) worked. Gate expiry is routine on long doc passes — route once,
  edit fast.
