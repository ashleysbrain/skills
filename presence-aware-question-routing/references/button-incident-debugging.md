# Question-lifecycle debugging recipes (2026-08-28 session)

Concrete paths and probes for the button-incident family. Environment: the OS
organism on macOS, conductor surface :port.

## Where the pieces live
- Ruling cards render from: `GET http://localhost:port/api/immune` → `rulings_pending[]`
  each with `ceo_brief` dict (`what`, `why_you`, `if_approved`, `if_rejected`).
- Brief fallback emitter: `/<workspace>`
  (~line 750: `brief = meta.get("ceo_brief") or {}`; screen side renders fields only
  if present — `conductor_screen.py` ~line 821).
- Question retry lane: message-bus operator `question-conduction` — messages look like
  `QUESTION Q-<ts>-<rand> -> <surface>: <subject>`.
- Question record source of truth: task-ledger task (kind=decision, state=open) —
  a stale one drove BOTH the :port card AND conduction retries.

## Diagnostic sequence (in order, ~2 min)
1. `curl -s http://localhost:port/api/immune | jq '.rulings_pending[] | {title, brief: (.ceo_brief | map_values(length))}'`
   → any zero-length brief field = fallback bug class.
2. Check mint origin: ledger `SELECT origin FROM tasks WHERE id=...` — `ceo:*` origin
   means it should NOT be a ruling button (ratification-vs-decision law).
3. Check ruling events vs question age: if the user answered in chat and the question
   still retries, the writeback is missing → close the ledger record manually, link the
   ruling task, then verify pending count dropped.

## Post-fix verification (mandatory, same turn)
- Daemon patches: `launchctl kickstart -k gui/$(id -u)/<label>` then re-curl the API —
  never claim fixed from the patch alone.
- GENOME gate notes: `kind=build` requires a `metrics=` clause (self-extending analytics
  law) and `body=` must be a single token (no spaces) — the gate regex is
  `body=(\S+)\s+scientist=(.+?)\s+physics=(["'])([^"']*)\3\s+8d=(\S+)`.

## Lane-grab check (routing under pressure)
When a P0 deadline pressures you to build in the orchestrator lane: the operator law
says orchestrate-only. The F-grade lesson (2026-08-28): pressure INCREASES routing
discipline — missed deadline = escalate through the owning organ, never self-execute.
Mechanical fix now building: routing-table lookup at dispatch blocks orchestrator-lane
execution of organ-owned work.
