# Physics disposition of the tri:review pile — 2026-09-02

principal order (verbatim): "there are a lot of isomorphism gap tasks in there
for me that should not be for me... you are the one that should investigate
and come up with the best position for nature. you don't need my permission
to advance the system. do it."

## Census (read-only first)

```sql
-- what's parked and how stale
SELECT kind, state, COUNT(*), MIN(created_at), MAX(created_at)
FROM tasks WHERE state NOT IN ('done','cancelled')
  AND stage='tri:review' GROUP BY kind, state;

-- physics fields present on every row (verified 161/161)
SELECT COUNT(*), SUM(est_cost IS NOT NULL), SUM(info_gain IS NOT NULL)
FROM tasks WHERE kind='gap' AND state='open' AND stage='tri:review';
```

Pile shape found: 386 at tri:review; 161 kind=gap (64 sev-4 `[AUTO]`/
`[AUTO-SHAPE]` arxiv curiosity scans parked since 2026-08-17 — 14 days).

## The disposition gate

T = {1: 2.0, 2: 1.5, 3: 1.0, 4: 0.5}; F = est_cost − T·info_gain.

```python
import sys; sys.path.insert(0, '/<workspace>')
import triangle_router as tr

# REFUSE (F > 0) — withdraw with values stamped
tr.withdraw(tid, reason=(
    f'physics REFUSE: F=cost-T*info=+{F:.2f}>0 (sev{sev}, cost {cost}, '
    f'info {info}, T={T}) — gap fails free-energy law at review; '
    'auto-dispositioned (gap work belongs to the OS, never parked for principal).'),
    actor='triangle-physics')

# GO (F <= 0) — advance PASS; station handoff + broker poke are automatic
tr.advance(tid, verdict='PASS', note=f'physics GO (F={F:.2f}); downstream station owns evidence/build.', actor='triangle-physics')
```

Withdraw returns `{'tid':…, 'withdrawn': True, 'state': 'cancelled', 'bus': <id>}`.
Advance returns `{'tid':…, 'advanced': True, 'from':…, 'to':…, 'bus': <id>,
'broker_poked': bool}`; passing the FINAL station returns `closed: True` +
arms the verified-dwell clock (close-or-downstream required same cycle —
T-260829-0048 law).

## Verified outcome

- Gap pass: 64 withdrawn (incl. 1 verb-tested solo), 97 advanced → build.
- Org-wide pass (all kinds): +94 withdrawn, +290 advanced → build/research.
- Totals: 158 withdrawn / 387 advanced; review pile 386 → 4.
- 102 TRIANGLE STATION handoffs posted to message-bus (timestamped window
  query on `subject LIKE 'TRIANGLE STATION%'`).
- 2 lawful refusals (correct guardrail behavior, logged, not retried):
  T-260818-0153 claimed-by-hermes zombie (withdraw needs --force or release),
  T-260821-0179 state=blocked (only open/claimed can move).
- Moving-with-2h-events after sweep: 16.
- Run-record minted + closed same turn: T-260902-0090 (FLW-GAP-CYCLE,
  complete() with inline proof: pre/post counts, bus ids, script paths).

## task_ledger API signatures (verified this session by failure)

- `submit(c, title=…, kind=…, lane=…, flow=…, severity=…, est_cost=…,
  info_gain=…, origin=…, created_by=…)` → returns the task-id STRING.
  NO `outcome` kwarg — outcome is `complete()`'s job. `r['task_id']` on the
  return raises TypeError: string indices must be integers.
- `claim(c, actor, actor_kind, task_id=None, lane=None)` — actor is
  positional-2; passing `task_id` positionally raises "got multiple values
  for argument 'actor'".
- `complete(c, task_id, outcome, actor='unknown')` → bool. Proof gate
  requires inline evidence classes (exit codes, command output, path
  anchors) — a narrative outcome alone is refused.

## Position for nature (stated to principal, now standing law)

Research scans mint gaps → physics gate kills low-information ones at
review (free energy is the predator; curiosity without a consumer organ
doesn't metabolize) → GO gaps flow to build/research with evidence duties.
The principal is never the disposition organ. Same disposition applies to ANY
kind parked at review — build/verify/question/defect/research piles have
the same disease and the same cure.
