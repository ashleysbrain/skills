# mint() is ID-allocation ONLY — the row INSERT carries 3 hidden constraints (2026-08-21)

`gates/task_ledger.py` `mint(c)` atomically advances the day counter and
returns the next `T-yymmdd-seq4` id. **It does NOT insert a task row.**
Calling `mint()` and committing leaves a gap id with no task; a follow-up
`UPDATE tasks ... WHERE id=?` then reports `None` (updates 0 rows) or,
with INSERT, walks into three constraints in sequence:

1. `NOT NULL constraint failed: tasks.created_at` — `created_at` has no
   default; supply `datetime.now(timezone.utc).isoformat()` explicitly.
2. `CHECK constraint failed: severity BETWEEN 1 AND 4` — severity is an
   INTEGER 1-4, not a 'P2'-style string (that's the technology-registry
   convention, not the ledger's).
3. There is **no `priority` column** — priority-like routing lives in
   `severity` (int) + `lane`. `requested_by` also does not exist; use
   `created_by` + `origin`.

Working minimal insert (verified live, T-260821-0190):

```python
import datetime, task_ledger as tl
c = tl.connect()
tid = tl.mint(c)
c.execute("""INSERT INTO tasks
  (id, title, kind, lane, severity, origin, state, detail, created_by, workstream, created_at)
  VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
  (tid, title, 'build', 'build', 3, 'ceo-ask', 'open', detail,
   'hermes', 'technology-registry',
   datetime.datetime.now(datetime.timezone.utc).isoformat()))
c.commit()
```

Also: `submit()` in this checkout takes ONLY `(c)` — the rich-keyword
`submit(c, title=..., kind=..., ...)` form referenced elsewhere is a
different revision; check `inspect.signature` before calling, don't trust
either signature from memory.

Sibling skills: `references/ledger-minting-pitfalls-2026-08-20.md` (collisions,
append-only events, state enum, cross-DB schema drift, zero-padding).
