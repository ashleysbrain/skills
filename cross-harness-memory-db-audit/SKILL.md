---
name: cross-harness-memory-db-audit
description: Use when auditing sqlite memory stores read-only.
category: devops
version: 1.0.0
author: the operator agent Agent
license: MIT
metadata:
  hermes:
    tags: [sqlite, audit, memory, wal, read-only]
    related_skills: [state-file-system-compliance]
---

# Cross-Harness Memory DB Audit

## When to Use
Any read-only audit of a sqlite store belonging to a harness or organism (sibling-agent memory dirs, sibling-agent session db, operator bus): liveness checks, table/row censuses, size attribution, or preparing a slimming PROPOSAL that must not be executed. Also the reference for WAL-safe read patterns when a live db refuses mode=ro.

Read-only audits of sqlite memory stores across harnesses (sibling-agent, sibling-agent, message-bus). Every reported number comes from a real query; anything derived or estimated is labeled as such in the report.

## Stores
- `~/.sibling-agent/memory/` — legacy layout; live sibling-agent memory is per-agent `~/.sibling-agent/agents/<name>/agent/sibling-agent-agent.sqlite` plus `~/.sibling-agent/state/sibling-agent.sqlite`. Verify with lsof before declaring any file dead.
- `~/.local/share/sibling-agent/sibling-agent.db` — live session store (WAL). NEVER mutate, move, or truncate it (SESSION DB SAFETY law in ~/.config/sibling-agent/AGENTS.md); the launchd rolling backup must stay in place.
- `~/your-workspace/message-bus.db` — live bus (WAL, near-continuous writers).

## Procedure
1. Read the clock, then inventory: `ls -la` each directory; record db, -wal, -shm, and backup-copy sizes and mtimes.
2. Liveness: `lsof -p <writer-pid>` filtered to sqlite/memory paths — a db no process holds, with an old mtime, is dead. mtime alone is the fallback when no writer is running.
3. Open read-only, by store state:
   - Live WAL dbs: a `mode=ro` URI open often fails (error 14, unable to open). Copy the db AND its -wal to scratch (`<agent-home>/cache/scratch/...`) and query the copy — the live file is never touched.
   - Abandoned files with stale/remnant -wal/-shm siblings: open with `immutable=1` URI.
4. Per db: list tables from sqlite_master (type='table'), then COUNT(*) per table. Giant tables: count via covering-index scan; multi-minute scans run in a background job writing to a file, then read the file.
5. Timestamps: confirm units before formatting. sibling-agent `time_created` is ms-epoch (divide by 1000); message-bus `timestamp` is ISO-8601 text compared lexically.
6. Report compactly: per file — size, mtime, per-table counts, live/dead verdict with the evidence (lsof or mtime).

## Slimming proposals (propose only; never execute against a live store)
- sibling-agent.db: `VACUUM INTO` a full archive first; then reviewed `DELETE FROM session WHERE id IN (...)` (FKs cascade message/part/todo/session_* children); event rows need an explicit `DELETE FROM event WHERE aggregate_id IN (...)` — the event FK cascade only covers event_sequence; finally `PRAGMA wal_checkpoint(TRUNCATE); VACUUM;`. Check `PRAGMA freelist_count` before and after: zero freelist means nothing is reclaimable until rows are deleted.
- message-bus.db: BEGIN IMMEDIATE; CREATE TABLE messages_archive_<date> AS SELECT * FROM messages WHERE status='done' AND timestamp < cutoff; DELETE with the same predicate; COMMIT; offline VACUUM. Derive the cutoff fresh from MAX(timestamp) at execution time. Never sweep `claimed` rows implicitly — stale claims deserve their own disposition pass.

## Pitfalls
- Do not put `PRAGMA busy_timeout=N` in the same sqlite3 CLI argument as a query — the pragma's return value prints alongside the result and corrupts parsed numbers.
- python sqlite3 execute() takes ONE statement; issue BEGIN IMMEDIATE separately from the INSERT.
- Writers hold locks for seconds at a time: wrap any corpus write in BEGIN IMMEDIATE + busy_timeout + a bounded retry loop, then read the row back to verify.
- On very large dbs under live I/O contention, per-table byte accounting (dbstat, SUM(LENGTH(col))) can exceed any foreground budget — background it with an output file rather than abandoning the measurement.
- Attribute size before proposing deletes: event-sourcing tables (per-edit event rows with full payloads) can dwarf the visible message tables; count rows x average payload per event type first.