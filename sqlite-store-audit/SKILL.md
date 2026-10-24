---
name: sqlite-store-audit
description: 'Use when auditing live SQLite stores read-only.'
version: 1.0.0
category: devops
author: the operator agent Agent (the operator agent, the OS)
license: MIT
metadata:
  hermes:
    tags: [sqlite, audit, database, wal, retention, read-only]
    related_skills: [state-file-system-compliance, sibling-agent-fleet-analytics-database-resilience]
---

# SQLite Live-Store Audit (read-only)

## When to Use

Use when auditing any live SQLite store — agent memory DBs, session DBs, operator bus, state DBs: live-vs-dead file identification, schema/row counts safe under WAL and concurrent writers, retention analysis, and propose-not-execute slimming plans. Complements `state-file-system-compliance` (which audits JSON state-file staleness, a different data type).

## Hard rules (every audit)
- READ-ONLY on live stores. Open live databases only via `?mode=ro` (or `immutable=1` for orphaned files). Never write, VACUUM, or DELETE against a live file unless the user explicitly ordered execution in this session's task.
- Deletion of duplicate/backup/tmp DB files: ONLY files the user explicitly named, and only after the deletion gate below passes. Otherwise leave in place and report.
- Every number in the report comes from a real query; label derived/estimated figures as derived, with the derivation shown.
- All arithmetic (size sums, percentages, GiB conversions, retention cutoffs) goes through python — never mental math.
- Before proposing ANY mutation of a store owned by another harness, read that harness's AGENTS.md / boot law for binding safety rules and cite them in the plan.

## Procedure

1. **Clock + inventory.** `date -u`; `ls -la` the store dir INCLUDING `-wal`/`-shm` sidecars; record bytes and mtimes.
2. **Find the LIVE file.** `pgrep -fl <daemon>` for the owner, then `lsof -p <pid> | grep -i sqlite`. Fallback signal: mtimes of `-wal`/`-shm` (WAL mode can leave the main file's mtime stale — judge liveness by the sidecars, not the main file alone). A file no process holds, with a cold wal, is a dead copy. Zero-row-looking stores may just be an abandoned layout: verify where live data actually lives (lsof) before declaring data loss.
3. **Pick the read pattern — first one that works:**
   a. `sqlite3 "file:$DB?mode=ro" ...` — normal case.
   b. `mode=ro` fails with `unable to open database file (14)` on a WAL db under write contention → `cp` the db AND its `-wal` to scratch, open the COPY without mode=ro (wal replays on first open), analyze the copy. State in the report that counts are as-of copy time.
   c. Orphaned/renamed file (no live wal pairing) still failing mode=ro → `file:$DB?immutable=1`.
4. **Schema.** `.tables`; `SELECT sql FROM sqlite_master` for tables AND indexes — the index list reveals covering-index paths for cheap counts.
5. **Row counts.** Per-table `COUNT(*)`. For multi-GB tables under concurrent IO, run the counts as a background job appending to a scratch file and poll the file — do not block the audit, and never conclude a query is impossible from one timeout (a rolling backup or `.dump` sharing the disk can make scans minutes-slow).
6. **Time bucketing.** Detect the timestamp unit FIRST (`SELECT MIN(time_col), MAX(time_col)` raw): 13 digits = ms-epoch (divide by 1000 in strftime), 10 digits = s-epoch, ISO-8601 string = compare lexically (no datetime cast needed). strftime on ms-epoch without `/1000` silently returns empty month buckets. Then `GROUP BY` month with COUNT + `SUM(LENGTH(payload))/1048576.0`.
7. **Size accounting.** `PRAGMA page_size * page_count` = file bytes; `PRAGMA freelist_count` = pages reclaimable by VACUUM alone. freelist = 0 means bloat is NOT the problem — slimming requires reviewed row deletion first; VACUUM with no deletion reclaims nothing.
8. **Retention analysis (on the copy).** Cutoff = newest timestamp minus retention window, computed in python. COUNT + payload-MB of rows matching the predicate (e.g. `status='done' AND timestamp < cutoff`); report share of live table and what stays.
9. **Deliverable.** Compact markdown, one section per store: live/dead verdict WITH evidence (the lsof row or wal mtime), per-table counts, month buckets, the proposed-but-not-run SQL verbatim, and caveats (e.g. stale `claimed` rows that would match the predicate after a status flip).

## Deletion gate (duplicate/backup/tmp db files)

Delete a user-named file only when ALL hold: (a) `lsof +D <dir>` (or lsof -p on known pids) shows no process holding it; (b) age from mtime exceeds the user's threshold (default 48h); (c) its size is <= the canonical/successor file; (d) sha256 recorded against siblings so the deletion is auditable. Print the gate values in the report, then delete, then re-list the directory.

## Slimming plan shape (proposal only unless execution is explicitly ordered)

1. `VACUUM INTO '<archive>-$(date +%F).db'` — online, WAL-safe full snapshot before anything is removed.
2. Reviewed id list: SELECT the ids matching the retention predicate; human-review any live-critical subset before inclusion.
3. `DELETE ... WHERE id IN (reviewed list)` — but check FK cascade topology in sqlite_master first: children declared `ON DELETE CASCADE` go automatically; sibling tables keyed by the same aggregate (e.g. an event store keyed by aggregate_id, not by the parent FK) need their own explicit DELETE.
4. `PRAGMA wal_checkpoint(TRUNCATE); VACUUM;` then verify the page_count/freelist_count delta and report actual bytes reclaimed.

## Pitfalls

- The sqlite3 CLI echoes PRAGMA return values to stdout — run `PRAGMA busy_timeout` in its own invocation or the echoed number pollutes captured results.
- Never open a live WAL db read-write just to read it; the scratch-copy pattern (3b) exists so the live file is never touched.
- A busy store can refuse reads transiently (lock contention while a writer commits) — retry once after a short wait before switching to the copy pattern.
- WAL read-mode split (live 2026-10-23, task-ledger.db + message-bus.db): CLI `file:...?mode=ro` fails with disk I/O error 14; python `sqlite3.connect('file:...?mode=ro', uri=True, timeout=10)` handles WAL correctly (queue_event_probe.py pattern). CLI `?immutable=1` opens fine but IGNORES the WAL — a write made seconds ago (fresh --complete) will not appear; never conclude 'write failed' from an immutable read. Fresh-write verification: cp db + -wal + -shm to scratch, open the copy plainly (0-byte wal after checkpoint is normal).

## Support files

- `references/store-recipes.md` — measured per-store notes (sibling-agent memory layout, sibling-agent session db, operator bus) with schemas, timestamp units, and archive-SQL templates. Re-verify schema before relying on store-specific facts.
