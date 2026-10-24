# Store recipes — measured facts per audited store

Store-specific facts below were measured from live queries; schemas drift with
versions, so re-verify with `.tables` + sqlite_master before relying on them.

## ~/.sibling-agent/memory/ (legacy memory layout)

- Legacy per-agent memory DBs (`atlas.sqlite`, `quill.sqlite`, `spark.sqlite`,
  `main.sqlite.*` copies). Schema: `chunks`, `files`, `meta`, `embedding_cache`,
  plus `chunks_fts*` FTS5 shell. Nearly all are empty (0 chunks / 0 files).
- When the sibling-agent gateway holds NONE of these via lsof, the whole directory
  is an abandoned layout. LIVE memory sits elsewhere:
  `~/.sibling-agent/agents/<agent>/agent/sibling-agent-agent.sqlite` (per-agent) and
  `~/.sibling-agent/state/sibling-agent.sqlite` (shared state). Verify with
  `lsof -p <gateway-pid> | grep sqlite`.
- Renamed leftovers (`*.migrated`, `*.backup-*`) may fail `mode=ro` because
  their WAL sidecars are gone/stale — open with `immutable=1`.

## ~/.local/share/sibling-agent/sibling-agent.db (sibling-agent session store)

- Dominant tables: `message`, `part`, `session` (+ `session_message`,
  `session_input`, `session_context_epoch`, `session_share`, `todo`) and an
  event-sourcing pair `event` + `event_sequence`.
- ALL `time_created`/`time_updated` columns are ms-epoch integers — divide by
  1000 in strftime or month buckets come back empty.
- `event` has NO time column: id, aggregate_id, seq, type, data. Bucketing by
  time requires a join through the owning aggregate, or bucket by type.
- Cascade topology: deleting `session` rows cascades to message/part/todo/
  session_* children, but `event` rows are keyed by aggregate_id with the FK on
  `event_sequence` — plan an explicit `DELETE FROM event WHERE aggregate_id IN
  (...)` alongside session deletion.
- BINDING: `~/.config/sibling-agent/AGENTS.md` SESSION DB SAFETY forbids
  mv/rm/truncate/overwrite of the live db; snapshot (cp or .backup) before any
  restart suggestion; the launchd rolling backup must stay enabled.
- A huge file with freelist_count = 0 is live rows, not bloat: size was driven
  by event.data + message/part payloads. VACUUM alone reclaims nothing.

## /<workspace> (operator bus)

- `messages` table: TEXT ISO-8601 UTC timestamps (`2026-10-17T18:21:32Z`) —
  lexical comparisons with a cutoff string are correct as-is.
- Status values seen: done, claimed, closed, pending, queued, open, cancelled,
  unread. Archive predicate: `status='done' AND timestamp < cutoff`.
- Archive convention: `messages_archive_YYMMDDHHMM` tables created via
  `CREATE TABLE ... AS SELECT` + DELETE in one `BEGIN IMMEDIATE` transaction,
  then VACUUM. Archive tables are plain copies (no autoincrement) — keep an id
  index if you plan to query them by id.
- Under live traffic the db can refuse `mode=ro` (writer committing) — use the
  scratch-copy pattern (cp db + -wal, open the copy) and timestamp the counts.
- Before a big archive move, run a staleness pass on `claimed` rows: old
  zombies would match the predicate after flipping to done and change the
  count materially.

## Archive-move SQL template (operator bus)

```sql
BEGIN IMMEDIATE;
CREATE TABLE IF NOT EXISTS messages_archive_<YYMMDDHHMM> AS
  SELECT * FROM messages WHERE status='done' AND timestamp < '<cutoff>';
DELETE FROM messages WHERE status='done' AND timestamp < '<cutoff>';
COMMIT;
VACUUM;
```

Cutoff = python-computed `max(timestamp) - retention window`, not a rounded
clock reading, so the boundary matches the data's own newest row.
