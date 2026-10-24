# Strip metric honesty — 2026-08-31 session (T-260831-0054)

principal order: top bar read `663 waiting / 20 moving / 45 done today` — "these
are not accurate, get rid of datapoints that are not actually real or live."

## Audit results (one SQL query per chip)

- **waiting 663**: real count, frozen stock. 561/663 (85%) at `tri:review`;
  hourly tri-readmit churn "touches" them so they look alive but the number
  never visibly moves.
- **moving 20**: FAKE. `state='claimed'` count including 9 zombie seats
  (oldest: T-260818-0153 claimed Aug 18, 13 days idle). "Claimed is a
  promise, not progress."
- **done today 45**: real — `substr(done_at,1,10)=today-UTC` matched exactly.
  (First audit query wrongly compared `datetime('now')` full-stamp to the
  date prefix and returned 0 — date-prefix comparisons need a date prefix on
  both sides.)

## Honest definitions (live)

```sql
-- moving: claimed + progress-class event in 24h
SELECT COUNT(DISTINCT t.id) FROM tasks t
WHERE t.state='claimed' AND EXISTS (
  SELECT 1 FROM task_events e WHERE e.task_id=t.id
  AND e.event IN ('claimed','tri-advance','tri-close','fix-landed',
                  'progress','released','done')
  AND e.ts > datetime('now','-24 hours'));

-- stale seats: claimed 72h+ with ZERO progress (zombies)
SELECT COUNT(DISTINCT t.id) FROM tasks t
WHERE t.state='claimed' AND NOT EXISTS (
  SELECT 1 FROM task_events e WHERE e.task_id=t.id
  AND e.event IN (/* same list */)
  AND e.ts > datetime('now','-72 hours'));
```

Live result: moving 20 → 10; stale_seats 9 surfaced as a kv block
("stale seats 9 claimed 3+ days, no progress") instead of inflating the chip.

## Producers patched (all three, grep census producers before declaring fixed)

1. `conduction_daemon.py` /api/render_hints inline census (~line 1898)
2. `compose_header.py ledger_census()` — Telegram/status surface feed
3. `render_hints.py flow_status_strip()` — composer: `moving_n = int(_mv) if
   isinstance(_mv, int) else claimed_n` (honest fallback, Pyright-clean;
   `int(x) if x is not None` fails type check on `Any|None`)

Composer unit test pattern (import the function, feed synthetic census,
assert chips):
```python
from render_hints import flow_status_strip
c1 = flow_status_strip({'open':663,'claimed':20,'done_today':45,'sev1_open':3,'moving':10,'stale_seats':9})
chips = {b['k']: b['v'] for b in c1['blocks'] if b['t']=='chip'}
assert chips['moving'] == 10  # honest value passes through
```

## Ledger mint→claim→complete mechanics (gates/task_ledger.py)

- `submit()` validates flow codes against `stores/flow-registry.json` —
  `FLW-DEFECT` is NOT registered; `FLW-SURGICAL` is. Check the registry
  list before minting (59 codes as of this session).
- `complete()` requires `state='claimed'` — mint-then-complete fails;
  `claim(c, actor=..., actor_kind='ai'|'human', task_id=...)` first.
- `claim(actor_kind=...)` accepts ONLY 'ai' or 'human' — 'harness' raises.
- `complete()` runs a PROOF GATE: narrative-only outcomes rejected; the
  outcome must carry inline exit codes, command output excerpts, or
  file:line anchors. Pattern that passed:
  `PROOF: composer unit test exit 0 (...); battery 58/58 exit 0; live API
curl -> chips ...; playwright innerText: ...` + `ANCHORS: file.py:line-range`.
- Display close gates (tri:close) additionally fire on delivery-class closes
  AND scan outcome+detail — keep proof inline, not attached later.

## Related

- Event-histogram "nothing moved" diagnosis (tri-readmit churn vs real
  work): same session, covered in
  `references/conductor-flow-view-surgery-2026-08-31.md`
- Zombie-seat drain (release or re-dispatch the 9) was left as follow-up
  conduction work — the honest metric now makes the debt visible.
