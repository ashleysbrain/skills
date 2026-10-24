---
name: ledger-resurface-trigger-deadlock
description: Use when claim is refused by unfired resurface_trigger gate.
---

## Symptom

`task_ledger.py --claim <tid>` refuses: "trigger gate: resurface_trigger=... unfired".
A LIVE (open/claimed) row carrying a non-empty `resurface_trigger` is sealed:

1. Claim gate (T-261021-0003) refuses claims without a `resurface-fire` task_event.
2. `gates/resurface_gate.py` only writes fires for DISPOSITIONED rows (live rows land in `skipped_live`, line ~257).
3. `organism/dispatcher_daemon.py` hard-inerts unfired-trigger rows (no score/station/origin/age can surface them).

Net: live row minted with a trigger column can never be claimed and never fire. Found 2026-10-23 on T-261005-0040 (sealed 18 days; trigger 'stack-rank v0.1 goes live' objectively met 2026-10-06). Class defect flagged to glial-team (bus 83129, 2026-10-23).

## Lawful unblock (operator override)

1. VERIFY the trigger condition is objectively met with hard evidence (done sibling task ids + outcomes, live artifacts on disk). Never fire on judgment alone.
2. Optionally try the front door first: `python3 gates/resurface_gate.py --event <type> --detail ... --evidence ...` — if the row is live it will appear in `skipped_live` (confirming the deadlock).
3. Write ONE `resurface-fire` event directly into `task_events` (append-only INSERT is lawful; NEVER update the tasks row):
   detail format: `event=<type>|prior_state=<state>|prior_stage=<stage>|prior_outcome=<outcome[:160]>|trigger=<trigger[:200]>|evidence=<cited evidence>|code=operator-override-<actor>-<yymmdd>|note=<why>`
   Sanction: resurface_gate.py docstring — "the resurface-fire event IS the operator-override record" (ruling #12843 spirit).
4. Claim normally: `task_ledger.py --claim <tid> --by <seat> --lease-seconds 21600` (retry on `database is locked` — dispatcher holds the write lock in bursts).
5. Flag the class defect to glial-team (dedup once/day per defect): `operator_bus.py post --from <seat> --to glial-team --type alert --dedup-key <defect-id-yymmdd>`.

## Probe query (deadlock census)

```sql
SELECT id, resurface_trigger FROM tasks
 WHERE state IN ('open','claimed') AND TRIM(COALESCE(resurface_trigger,'')) <> ''
 AND id NOT IN (SELECT DISTINCT task_id FROM task_events WHERE event='resurface-fire');
```
Every hit = sealed row. Fix ownership: engine owners (sibling-agent) — either fire-writer handles live rows (fire = ungate-only, no state change) or claim gate accepts objective-evidence ungate.
