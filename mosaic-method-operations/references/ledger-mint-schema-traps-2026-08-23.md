# Task-ledger mint schema traps (2026-08-23, three failed mints before success)

stores/task-ledger.db (NOT ledger/state.db — that is the dispatch chain DB).

## The traps, in the order they fire

1. `tl.mint(c)` ONLY allocates the next ID (T-YYMMDD-NNNN). It does not write a
   row. A subsequent SELECT returns nothing and looks like "transaction isolation
   failure" — it isn't; you never INSERTed.
2. `created_at` is NOT NULL with no default — INSERT must supply it
   (`datetime.now(timezone.utc).isoformat()`).
3. `severity` is INT with CHECK (severity BETWEEN 1 AND 4). 'P2'/'P3' strings
   fail with a confusing IntegrityError. 1=critical..4=low.
4. `priority` does not exist — the column is `severity`.
5. kind/lane must validate against stores/task-taxonomy.json; unknown value =
   ValueError naming the file to edit. flow must exist in flow-registry.json.

## Working pattern

```python
import sys, datetime; sys.path.insert(0,'gates')
import task_ledger as tl
c = tl.connect(); tid = tl.mint(c)
c.execute("INSERT INTO tasks (id,title,kind,lane,severity,origin,state,detail,
created_by,workstream,created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
  (tid, title, 'build','build',3,'ceo-ask','open', GENOME_DETAIL,
  'hermes', workstream, datetime.datetime.now(datetime.timezone.utc).isoformat()))
c.commit()
print(c.execute("SELECT id,title FROM tasks WHERE id=?", (tid,)).fetchone())
```

## Panel-amendment pattern (survives compaction)

Late panel verdicts fold into the minted task, not into chat prose:
`UPDATE tasks SET detail = detail || '\n\nPANEL-N AMENDMENTS (...): ...' WHERE id=?`
The build lease inherits the amendments via the ledger; chat context does not
survive. kind=build requires a GENOME block in detail (lineage, mechanism,
acceptance, owner-lane).

## Bus schema (message-bus.db, the LIVE one at your-workspace)

messages columns: timestamp, from_op, to_op, msg_type, subject, content, status,
in_reply_to. There is no `topic`/`body`. Link follow-ups via in_reply_to=<id>.
