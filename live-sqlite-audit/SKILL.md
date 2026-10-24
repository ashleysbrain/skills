---
name: live-sqlite-audit
description: Use when auditing a live SQLite store read-only.
version: 1.0.0
author: the operator agent Agent
license: internal
metadata:
  hermes:
    tags: [sqlite, audit, read-only, wal, devops]
    related_skills: [sensor-validation, tool-output-verification-discipline]
---

# Live SQLite Audit (read-only)

## When to Use
Any request to inspect, count, size, or propose archiving for a SQLite store that may have live writers: memory/agent databases, operator buses, session stores, cron state. Also when deciding which of several similarly-named db files is live vs dead, or when a deletion of a stale db/tmp file was explicitly authorized and needs a safety gate.

## Law
Never open a live store read-write. Every reported number comes from a real query. Mutation happens only through an explicitly sanctioned gate, and archive/delete SQL is written for review, not executed unless ordered.

## Procedure
1. **Inventory**: `ls -la` the directory (sizes, mtimes). Identify the LIVE store by holder, not by name: `lsof -p <pid> | grep -i sqlite` and `lsof +D <dir>`; fall back to mtime only when no process holds any file. A gateway can hold per-agent stores elsewhere while a legacy directory looks canonical — lsof decides which files are dead.
2. **Open read-only**: `sqlite3 "file:<path>?mode=ro"`. If it fails with error 14 ("unable to open database file") the db is WAL-mode with an ACTIVE writer — copy `db` + `db-wal` + `db-shm` to scratch and query the copy, never the live file. Copying without the -wal sidecar silently loses recent commits.
3. **WAL-orphaned legacy files** (no live writer, stale journal references) that fail mode=ro usually open with `immutable=1`.
4. **Schema before counts**: `.tables`, `SELECT sql FROM sqlite_master WHERE type='table'`, `PRAGMA table_info(<t>)` — never assume column names; grep for them. Then COUNT per table, quoting identifiers in loops.
5. **Probe timestamps raw first**: `MIN(<ts>), MAX(<ts>)` before any strftime — ms-epoch stores need `<ts>/1000`, otherwise strftime returns NULL and month grouping collapses into one empty bucket without erroring.
6. **Sizing**: `PRAGMA page_size / page_count / freelist_count` (freelist=0 means zero reclaimable bloat; only deletion + VACUUM shrinks the file). Payload per table via `SUM(LENGTH(col))` grouped by month for growth attribution. dbstat per-table attribution on multi-GB files is expensive — background it.
7. **Heavy scans** (minute-plus on GB stores; worse under competing IO such as rolling `.dump` backups): run as a background job writing to a scratch file, poll the file from the foreground, and when budget-bound kill the scan and report partials explicitly labeled measured vs derived.
8. **Archive SQL pattern** (write for review, do not run): single transaction — `CREATE TABLE arch AS SELECT * FROM src WHERE 0` (carries schema), `INSERT INTO arch SELECT * FROM src WHERE <predicate>`, verify count parity, `DELETE FROM src WHERE <same predicate>`, COMMIT, VACUUM offline after. Derive time cutoffs from the live table's MAX(ts) minus the retention window, not from wall clock; exclude non-terminal statuses (e.g. claimed) by design and say so.
9. **Deletion gate for stale files** (only when explicitly sanctioned): all four checks pass or leave in place — age over threshold (stat), size <= the successor store, lsof-verified unheld, hash distinct from sibling copies (identical hash means a duplicate, distinct hash means an independent stray).

## Pitfalls
- The sqlite3 shell prints PRAGMA return values inline (busy_timeout echoes its integer) when chained with `;` into one invocation — run pragmas and queries as separate invocations or parse around the noise instead of trusting every line as data.
- An empty table list from a loop usually means the OPEN failed, not zero tables — check stderr before concluding a store is empty.
- COUNT(*) on a huge rowid heap can take minutes; prefer the smallest covering index (child tables usually index session/parent + time).
- Big deletes need FK cascade awareness: event-log tables often reference a sequence table that cascades, while the payload table itself does not — deleting parents can orphan the bulk unless the event table is swept explicitly.
