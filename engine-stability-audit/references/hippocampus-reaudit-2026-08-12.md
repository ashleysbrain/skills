# Hippocampus Re-Audit — 2026-08-12

**Auditor:** the specialist engine (stability scientist)
**Engine:** the specialist engine (`ds-hippocampus-engine/`, port 8205)
**Code path:** `src/hippocampus/core/engine.py`

## Context

Previously audited 5 critical defects in Hippocampus. the operator agent claimed all 5 fixed.
This is the re-test. **3 confirmed fixed, 2 still broken, 1 new defect found.**

## Scorecard

| # | Original defect | Claimed fix | Verdict |
|---|-----------------|-------------|---------|
| 1 | Fake persistence (in-memory dict) | SQLite backend | CONFIRMED FIXED |
| 2 | Consolidation capped at 10 | processes all in batches | CONFIRMED FIXED |
| 3 | O(N^2) encode | unknown | STILL BROKEN |
| 4 | No dedup | content_hash before INSERT | CONFIRMED FIXED |
| 5 | Unbounded growth | unknown | STILL BROKEN |
| 6 | — (concurrent writes) | — | NEW DEFECT (BROKEN) |
| 7 | — (corruption / WAL) | — | PARTIAL |
| 8 | — (long content 50KB) | — | CONFIRMED FIXED |

## Test 1 — Persistence: CONFIRMED FIXED

- Encoded 20 memories, destroyed engine, raw `sqlite3` read = 20/20.
  IDs `mem_000001`..`mem_000020` all present.
- Then 100 more across a second engine lifecycle, raw read = 120/120, all `short_term`.
- The fake in-memory dict is gone. Real SQLite at `data/memories.db`.

## Test 2 — Consolidation coverage: CONFIRMED FIXED

- 30 short_term memories (access_count bumped to 5 so one replay crosses threshold).
- `consolidate()` promoted **all 30** to long_term (old bug capped at 10).
- Code confirmed: the `[:10]` slice was removed. It batches `MAX_REPLAY_PER_CYCLE=10`
  but processes every row.

## Test 3 — Encode scaling: STILL BROKEN (the key methodology lesson)

### What went wrong on the first pass

Initial single-trial timing at N<=220:

```
  mem #  1: 1.89ms
  mem # 25: 37.54ms
  mem # 50: 4.40ms
  mem #100: 21.49ms
  mem #150: 8.31ms
  mem #200: 22.13ms
  mem #220: 8.93ms
```

This bounced wildly and **falsely classified the scaling as "bounded/linear"** (ratio
t(#200)/t(#1) = 11.7x, under the 50x threshold). Wrong verdict. The bounce is
SQLite/Python constant-factor overhead dominating at small N.

### What the rigorous run showed

5-trial **median** at checkpoints N=50..1200:

```
     N |  median |   min |    max | vs N=50
    50 |  6.79ms | 6.47ms| 24.35ms|   1.0x
   100 |  7.65ms | 5.15ms| 24.98ms|   1.1x
   200 | 12.11ms | 6.11ms| 23.00ms|   1.8x
   400 | 11.11ms | 9.82ms| 30.31ms|   1.6x
   800 | 44.98ms |24.73ms| 48.54ms|   6.6x
  1200 | 52.49ms |45.59ms| 56.71ms|   7.7x
```

Regression fits:
- Linear:    `t = 4.36e-05*N + 2.54e-3`,  **R^2 = 0.9302**
- Quadratic: `t = 5.03e-10*N^2 + 4.30e-05*N + 2.63e-3`, R^2 = 0.9303

The quadratic term is negligible (R^2 barely improves). The linear fit is excellent.
Per-encode cost is **O(N)**, so encoding N memories is **O(N^2) aggregate**.

At N=1000, encoding 1001 memories took **23.4 seconds** (~23ms each).

### Root cause (code)

`engine.py` lines 257-261: every `encode()` calls `_load_all()` (full table scan) then
runs a Python-level O(N) similarity loop over every stored memory to build associations.
No index on content for the similarity scan; the `content_hash` index only serves dedup.

### Lesson (durable)

Small-N timing (<=220) gave a false CONFIRMED FIXED. Scaling to N>=800 with median-of-5
trials and an R^2 fit corrected it. This is the canonical example of why the timing
regression methodology in the parent SKILL.md mandates large N + median-of-trials.

## Test 4 — Dedup: CONFIRMED FIXED

- Identical string encoded 10x -> **1 memory** in DB.
- `content_hash` index + SELECT-before-INSERT works correctly.
- `access_count` = 9 (correct: first insert = 0, 9 dedup increments).
- Minor note: the returned object on a dedup hit reflects the *pre-increment* state
  (it returns `Memory.from_row(existing)` before the UPDATE commits), so callers see
  access_count one behind. Not a data-integrity bug, but worth knowing.

## Test 5 — Eviction ceiling: STILL BROKEN

- `COMPONENT_COUNT_CEILING = 1000` defined at line 36.
- `rg -n 'COMPONENT_COUNT_CEILING'` returns exactly ONE hit: the definition. **Dead code.**
- Encoded 1001 unique memories; all 1001 survived (ceiling would cap at 1000).
- No eviction/TTL/max-size logic anywhere. `consolidate()` only prunes short_term with
  `replay_count > 3 AND consolidation_score < 0.2`; long_term memories are NEVER evicted.

## Test 6 — Concurrent writes: NEW DEFECT (STILL BROKEN)

- 5 threads x 20 encodes = 100 expected. **Only 20 survived.**
- 4 threads threw `UNIQUE constraint failed: memories.id`.
- Root cause: `_next_id()` does non-atomic `SELECT MAX(id)+1` then a separate `INSERT`.
  Classic TOCTOU race — threads grab the same ID before any commit lands.
- No transaction wrapping, no UPSERT, no retry.
- This defect was **introduced by** the SQLite migration. The old in-memory dict didn't
  have the race because the GIL serialized access. The fix needs `AUTOINCREMENT` or
  `INSERT ... ON CONFLICT` or transaction-wrapped ID generation.

## Test 7 — Corruption / WAL: PARTIAL

- `journal_mode = delete` (rollback journal), `synchronous = 2` (FULL).
- No `PRAGMA`/WAL configured in engine code (grep confirmed).
- Hard-kill test: subprocess `os._exit(137)` mid-batch of 50 -> `integrity_check = 'ok'`,
  all committed rows survived (10 pre-crash + the in-flight batch up to the kill point).
- Structurally safe because each `encode()` commits in its own transaction. A hard kill
  only loses the in-flight row, never corrupts the file.
- BUT: no WAL means readers block writers under load, and N separate commits = N fsyncs
  (slow). Not corruption-prone, but not optimized for write-heavy memory workloads.

## Test 8 — Long content 50KB: CONFIRMED FIXED

- 50000-char string encoded, stored **byte-exact** (len=50000, match=True).
- encode 3.39ms. SQLite TEXT column handles large content fine.
- `retrieve("X")` returned 0 hits — correct behavior, since `"X"*50000` tokenizes as one
  giant token that won't match a single-char query. Not a storage bug.

## Reproduction

All tests ran in-process via `execute_code` against isolated `tempfile.mkdtemp()` DBs.
No test script file was written to disk (workspace write-gate blocked new files); the
harness lived entirely in the execute_code cells. Persistence/corruption tests used
`subprocess` + `os._exit(137)` for the process boundary.
