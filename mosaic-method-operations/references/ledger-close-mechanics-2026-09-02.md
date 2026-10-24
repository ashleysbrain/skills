# Ledger Close Mechanics + Flow-Ledger Archive — 2026-09-02

Operational recipes from closing 113 isomorphism-gap tasks through the
gates (T-260901-0010) and shipping the done-archive principal order.

## Signatures (verified via inspect.signature, 2026-09-02)

```python
import sys; sys.path.insert(0, 'your-stack/gates')
import task_ledger

task_ledger.claim(c, actor='hermes', actor_kind='ai', task_id=tid)
# actor/actor_kind POSITIONAL-ORDER sensitive; wrong order raises
# "actor_kind must be 'ai' or 'human'"

task_ledger.complete(c, task_id=tid, actor='hermes', outcome='...')
# refuses rows not in state='claimed' — claim first, always

task_ledger.release(c, task_id=tid, reason='...', actor='hermes')
# reason is the 2nd POSITIONAL arg; only works on state='claimed'
```

## The gates that bite at close time

1. **PROOF GATE** (PROOF kinds): outcome needs inline evidence classes —
   exit codes, command output, or file/offset anchors. Advisory kinds
   (decision/question/gap/probe/maintenance/research) pass untouched.
2. **WIRING GATE**: if outcome text matches DELIVERY_RE
   (`daemon|cron|launchd|plist|keepalive|watchdog|listener|socket|service|
   scheduler|timer|delivers|delivery|carries|port \d+|:\d{4,5}|job #\d+`),
   the close must carry a machine-checkable locator (launchd label, :port,
   job id) which the gate PROBES LIVE — or close as `BUILT-INERT
   owner=<name>` + activation ticket `T-\d{6}-\d{4}`. Escape hatch for
   non-delivery work: reword. "carries" → "HAS" fixed 21 refused closes.
3. **FLOW liveness check** (build kinds): closing a delivery-class build
   into a flow with computed_liveness DEAD is refused — route a consumer
   first.

## Unblocking a blocked task (release() refuses blocked rows)

```python
from datetime import datetime, timezone
ts = datetime.now(timezone.utc).isoformat(timespec='seconds')
c.execute("UPDATE tasks SET state='open' WHERE id=? AND state='blocked'", (tid,))
c.execute("INSERT INTO task_events (task_id, ts, actor, actor_kind, event, detail) "
          "VALUES (?,?,?,?,?,?)",
          (tid, ts, 'hermes', 'ai', 'unblocked', '<why — cite the dependency resolved>'))
# then claim + complete normally
c.commit()
```

task_events columns (pragma_table_info): `seq` (auto), `task_id`, `ts`,
`actor`, `actor_kind`, `event`, `detail`. There is NO created_at. Direct
INSERT into task_events is legal (append-only history); direct INSERT
into tasks is trigger-blocked — submit() only.

## Title-variant matching when closing a scan's backlog

The same scanner changed title format across weeks: `GAP: isomorphism
gap [EVOLVE] (NNNN)`, `EVOLVE: isomorphism gap — <organ>...`, `BUILD:
EVOLVE: ...`, plus QA-pickup children titled `QA pickup: verify+build gap
task T-...`. A prefix LIKE silently misses variants — count stayed
"0 open" while 25 sat in the live view until the query broadened to
`title LIKE '%isomorphism gap%' AND state IN ('open','claimed','blocked')`.
ALWAYS verify from SQL after a close pass:

```sql
SELECT state, COUNT(*) FROM tasks WHERE title LIKE '%<pattern>%' GROUP BY state;
```

## Flow-ledger archive (principal order 2026-09-01: "done items should be
archived in historical records if they are truly done")

- **Truly-done audit first** (principal: "you must be sure and I don't trust you
  rn"): check every done task for post-done_at events excluding
  bookkeeping types (note/ceo_note/minted/amend/taxonomy repair/
  ts-normalize/deadline-*). 39 carried events — all bookkeeping, zero
  reopens. Real rework signals would be repair/claimed/tri-advance.
- **Implementation = VIEW discipline**: conduction_daemon.py
  `/api/flows/tasks` gained `_arch = archive=1 in query` →
  `_where = "state IN ('done','cancelled')" if _arch else
  "state IN ('open','claimed','blocked')"` prepended to the SELECT. Rows
  never move (tasks_no_delete trigger = birth certificates law).
- **Surface**: header `<span id="ft-live-count">N</span> active · done
  archived, in history · history link` → `ftShowArchive()` toggles
  FTARCHIVE, re-fetches with/without `&archive=1`, shows gold banner
  `ft-archbanner` (HISTORY — done and cancelled records, read-only ·
  back to live work). Live count span updates on every load AND toggle.
- **Verification stack** (never vision alone): API probe (live states
  exactly {open,claimed,blocked}; archive {done,cancelled}; pollution 0)
  → Playwright DOM read (FLOWTASKS[0..3] states flip open↔done) →
  screenshot → vision audit for overlap/clipping.
