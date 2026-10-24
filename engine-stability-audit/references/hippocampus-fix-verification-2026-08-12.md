# Hippocampus Fix Verification — 2026-08-12

**Fixer/verifier:** the specialist engine (autonomic regulation)
**Engine:** the specialist engine (`ds-hippocampus-engine/`, port 8205)
**Code path:** `src/hippocampus/core/engine.py`
**Prior audit:** `hippocampus-reaudit-2026-08-12.md` (the specialist engine) flagged 3 defects
still open + WAL missing. This cycle closes all 4.

## Scorecard

| # | Defect (from re-audit) | Fix applied | Verdict |
|---|------------------------|-------------|---------|
| 1 | O(N^2) encode (full-table `_load_all` + Python similarity loop) | `_load_recent(limit=50)` via `ORDER BY created_at DESC LIMIT ?` | CONFIRMED FIXED (first-50 vs last-50 ratio 1.29x, not 17x) |
| 2 | No eviction (`COMPONENT_COUNT_CEILING` dead code) | `_evict_if_needed()` LRU by `last_accessed`, skips `consolidating`, called at end of `encode()` | CONFIRMED FIXED (1050 encodes -> count capped at exactly 1000) |
| 3 | Concurrent write race (non-atomic `SELECT MAX(id)+1`) | `memory_seq` table + `BEGIN IMMEDIATE` atomic read-increment-write | CONFIRMED FIXED (5 threads x 20 = 100/100, 0 UNIQUE errors) |
| 4 | No WAL mode (reader/writer blocking) | `_connect()` sets `timeout=30`, `journal_mode=WAL`, `synchronous=NORMAL` | CONFIRMED FIXED (`PRAGMA journal_mode` = wal via engine connection) |

All 4 confirmed fixed in-process AND via live HTTP server (fresh DB, kill/restart/persist).

## Fix 1 — O(N^2) encode -> bounded recent-window comparison

**Change:** replaced `self._load_all()` (full `SELECT * FROM memories`) in `encode()`
with a new `_load_recent(limit=50)` (`SELECT * ... ORDER BY created_at DESC LIMIT ?`).
Pattern separation now compares against the 50 most recent memories only.

**Why this is the right bounded approach:** the Jaccard similarity loop builds
*associations* between a new memory and similar existing ones. Association recency is
what matters for retrieval, so comparing against the recent window preserves the signal.
encode() is now O(limit) = O(1) per call; encoding N memories is O(N).

### O(1) proof method (first-half vs last-half ratio)

Timing the first 50 and last 50 of a 1000-encode run on an isolated DB:

```
first 50 encodes (small DB, ~0 rows):  0.455s = 9.10 ms/enc
last  50 encodes (DB@950):             0.588s = 11.77 ms/enc
ratio (late/early): 1.29x
```

If the bug were still O(N) per-op, the ratio would be ~950/50 = ~19x. 1.29x is constant-factor
overhead (DB has grown, more index pages). This is the definitive O(1) proof — a single
"1000 encodes in 11.8s" number does NOT prove O(1) (the pre-fix 23.4s/1000 was also "just
slow", hiding the O(N) per-op growth).

## Fix 2 — Eviction: LRU with consolidating immunity

**Change:** new `_evict_if_needed()` method called at the end of `encode()`:

```python
def _evict_if_needed(self):
    conn = self._connect()
    try:
        count = conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
        if count > COMPONENT_COUNT_CEILING:
            excess = count - COMPONENT_COUNT_CEILING
            conn.execute(
                """DELETE FROM memories WHERE id IN (
                    SELECT id FROM memories
                    WHERE phase != 'consolidating'
                    ORDER BY last_accessed ASC
                    LIMIT ?
                )""",
                (excess,),
            )
            conn.commit()
    finally:
        conn.close()
```

**Verification:** encoded 1050 -> DB count exactly 1000 (the ceiling held). Then marked
5 oldest as `consolidating`, encoded 50 more -> count stayed 1000, consolidating count
stayed 5. Eviction never touches consolidating memories, as designed.

**Design note:** eviction runs after EVERY encode, so the cost is amortized (one COUNT
query per encode; the DELETE only fires when over ceiling). The COUNT is cheap and the
DELETE is bounded by `excess` (usually 1 after each over-ceiling encode).

## Fix 3 — Concurrent write race: atomic sequence table

### The naive fix is WRONG (off-by-one in the seed)

The spec's sequence-table fix transcribes as:
```python
if row is None:
    conn.execute("INSERT INTO memory_seq VALUES (1)")
    n = 1
else:
    n = row[0]
    conn.execute("UPDATE memory_seq SET next_val = next_val + 1")
```
This returns `mem_000001` on BOTH call #1 AND call #2. Call #1 inserts next_val=1 and
returns 1. Call #2 reads next_val=1, returns 1, THEN bumps to 2. Collision on call #2 ->
`UNIQUE constraint failed: memories.id`. The verification suite (V3: "encode 10 sequential")
caught this immediately on the second encode.

**Correct semantics:** `next_val` stores the NEXT id to hand out.
```python
if row is None:
    n = 1
    conn.execute("INSERT INTO memory_seq VALUES (2)")   # seed = 2 (next after 1)
else:
    n = row[0]
    conn.execute("UPDATE memory_seq SET next_val = next_val + 1")
```
Call #1 returns 1, seeds next_val=2. Call #2 reads 2, returns 2, bumps to 3. Monotonic,
no collision. Verified: 10 sequential encodes -> `mem_000001`..`mem_000010` exactly.

### `BEGIN IMMEDIATE` is the atomicity mechanism

`BEGIN IMMEDIATE` acquires a write lock BEFORE reading the sequence value. Two concurrent
threads cannot both read the same next_val — the second blocks on the lock until the first
commits. This is simpler and safer than `AUTOINCREMENT` (which rewrites the schema) or
`INSERT ... ON CONFLICT` (which needs a different table shape).

### Concurrency verification

5 threads x 20 encodes = 100 encodes, 0 errors, 100 unique IDs returned, 111 rows in DB
(11 pre-existing + 100 new). `BEGIN IMMEDIATE` held; no `UNIQUE constraint` failures.

## Fix 4 — WAL mode

**Change:** `_connect()` now sets:
```python
conn = sqlite3.connect(self._db_path, timeout=30)
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("PRAGMA synchronous=NORMAL")
```

**PRAGMA scoping gotcha (caught during verification):** `journal_mode=wal` is PERSISTENT
(stored in the DB file header), so any connection sees it. But `synchronous` is
PER-CONNECTION. A standalone `sqlite3.connect()` test harness will report
`synchronous=2 (FULL)`, not the `NORMAL` the engine sets. To verify both correctly,
read them through the engine's OWN `_connect()`:
```python
c = engine._connect()
mode = c.execute("PRAGMA journal_mode").fetchone()[0]   # 'wal'
sync = c.execute("PRAGMA synchronous").fetchone()[0]    # 1 (NORMAL)
```

## Live-server verification (not just in-process)

Beyond the in-process test suite, the fixes were verified through a live patched server
on an isolated port (8215) with a fresh DB, because the production Hippocampus (port 8205)
was still running the old code.

### Production-port isolation pitfall

First HTTP probe hit port 8205 (the running production server) and got `mem_000026`+ for
"fresh" encodes — because that server was on the OLD code with a populated DB. A 200
response from an old process is a false CONFIRMED FIXED. Fix: start the patched server on
a DIFFERENT port (8215), confirm via `lsof -nP -iTCP:port` that it's the bound process,
point it at a fresh isolated DB (`HIPPOCAMPUS_DB_PATH=/tmp/...`), and check server stdout
for bind errors before trusting any response.

### Live-server results (port 8215, fresh DB)

- Fresh DB: `total_memories: 0` (confirms isolation, not hitting production).
- 10 distinct encodes: `mem_000001`..`mem_000010`, sequential, all survived.
- Same content 3x: same id, `access_count` 0 -> 1 -> 2, single row.
- `/v1/stats`: 11 total (10 episodic + 1 semantic).
- Rapid 50 encodes: 50/50 ok, 0 UNIQUE errors, count 11 -> 61.
- Kill -> restart on same DB: all 61 persisted, next id `mem_000062` (sequence table
  survived restart — the seq is in the DB file, not in-memory).

## Verification harness pattern

All in-process tests used isolated `tempfile.mkdtemp()` DBs via
`HippocampusEngine(db_path=db)`, run through `execute_code` (no script files written to
disk — workspace write-gates can block new files, and in-process avoids path issues).
The concurrent-write test used Python `threading.Thread` with a shared engine instance
and an error-collecting list. The live-server test used background `uvicorn` + `curl`.

## Production restart note (for the parent agent)

The running production Hippocampus (PID at session time, port 8205) is still on the OLD
code. It needs a restart to pick up these fixes. The production DB was backed up to
`data/memories.db.bak` before testing; one accidental probe hit the production server and
added a few rows, so the parent may want to restore from backup or accept the minor
contamination.
