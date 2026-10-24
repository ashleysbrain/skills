# O'Keefe Read-Only Fix Verification (2026-08-12)

**Auditor:** the specialist engine (Percy Williams Bridgman — operationalism)
**Engine:** DS O'Keefe (`ds-okeefe-engine/`, port 8147)
**Mode:** Read-only (no destructive tests, no process kills, no file corruption)

## Context

The operational resilience audit (`okeefe-operational-resilience-audit-2026-08-12.md`)
identified 7 defects. Fixes were claimed. This audit verifies each fix independently
through **code inspection at exact line numbers + live read-only API calls** — no
destructive tests, no process kills, no file corruption.

## Read-Only Fix Verification Protocol

When you CANNOT run destructive tests (production engine, data at risk), use this
protocol. Every fix claim gets verified by two independent read-only lines of evidence:

### 1. Code-at-exact-line-numbers

Read the actual source file, not a diff or description. Cite the EXACT line numbers
where each fix component sits. Confirm the fix code is in the claimed execution order.

```
Example claim: "novelty check moved before ca3.store()"
Verification: Read engine.py lines 719-770. Confirm:
  - ca3.retrieve() at line 723
  - ca1.compute() at line 725
  - novelty threshold check at line 730
  - early return at line 731
  - ca3.store() at line 737 — AFTER the check
```

### 2. Live read-only API calls

Hit the running engine with GET requests only. Never POST/encode/delete on a
production system unless explicitly authorized.

```
GET /health — verify memory_count, engine status
GET /memories — verify all memories have text, count matches persist file
GET /retrieve or bridge recall() — verify query results are correct
```

### 3. Persist-file analysis (read-only)

Read the JSON persist file directly with `json.load()`. Check:
- Trace count matches /health memory_count
- No duplicate trace_ids or content_hashes
- No empty/null text fields
- Timestamp distribution (can reveal latent bugs like all-zero timestamps)

### 4. Dead-code grep

`grep -n 'method_name'` — if the only hit is the definition line, it's dead code.
For "X calls Y" claims, grep for Y's name. If Y appears ONLY in its own definition,
the call path is broken regardless of what X's code looks like.

## Scorecard: 7 Claimed Fixes

| # | Fix claim | Method | Verdict |
|---|-----------|--------|---------|
| 1 | Backup corrupt files before returning None | Code lines 605-615 | CONFIRMED FIXED |
| 2 | fsync before atomic replace | Code lines 576-581 | CONFIRMED FIXED |
| 3 | Novelty check before ca3.store() | Code lines 723-737 | CONFIRMED FIXED |
| 4 | _trace_order append guard | Code lines 764-766 | CONFIRMED FIXED |
| 5 | Hybrid scoring in bridge recall() | Code lines 188-192 + manual computation | CONFIRMED FIXED |
| 6 | Health-wait increased 8→15s | Code line 144: `range(15)` | CONFIRMED FIXED |
| 7 | memory_count check after restart | Code lines 148-157 | CONFIRMED FIXED |

**All 7 fixes verified.** Each confirmed by reading the exact source lines.

## Scorecard: 4 Open Items (confirmed still open)

| # | Open item | Verification method | Status |
|---|-----------|-------------------|--------|
| 1 | Vector collision silent overwrite | All 29 traces have timestamp=0.0; trace_id determined solely by content_hash | STILL OPEN |
| 2 | Ebbinghaus decay dead code | `grep apply_ebbinghaus_decay` = 1 hit (definition only, line 111) | STILL OPEN |
| 3 | Silent novelty drop returns HTTP 200 | server.py lines 113-118: no conditional on trace_id | STILL OPEN |
| 4 | Dual supervisor restart race | Both `auto_repair_watchdog.py` and `fleet_autonomic_supervisor.sh` exist independently | STILL OPEN |

## Detailed Verification Examples

### Fix 3: Novelty check ordering (line-by-line proof)

```
Line 719: dg_code = self.dg.separate(ec)          # pattern separation
Line 722: # CA1 novelty (check BEFORE storing in CA3)
Line 723: ca3_retrieved = self.ca3.retrieve(...)   # retrieval (read-only on CA3)
Line 725: ca1_out, novelty = self.ca1.compute(...)  # novelty computation
Line 730: if novelty < self.NOVELTY_THRESHOLD:      # the gate
Line 731:     return ""                              # early exit — NO ca3.store() called
Line 737: self.ca3.store(dg_code, learning_rate=lr) # store happens AFTER gate
```

The novelty gate at line 730 fires BEFORE ca3.store() at line 737. Confirmed.

### Fix 5: Hybrid scoring manual computation

```python
# Bridge recall() lines 188-192
# If keyword_score=0, strength=1.0:
ks = 0
ss = min(1.0 / 2.0, 1.0)  # = 0.5
keyword_component = 0.5 * 0     # = 0.0
semantic_floor = 0.3 * 0.5     # = 0.15
semantic_bonus = 0.2 * 0.5     # = 0.10
hybrid = max(0.0, 0.15) + 0.10  # = 0.25
# A strong semantic match with zero keyword overlap scores 0.25
# This prevents pure-keyword re-rank from burying correct semantic matches
```

### Open item 2: Ebbinghaus decay doubly dead

```
apply_ebbinghaus_decay() defined at line 111.
grep -n 'apply_ebbinghaus_decay' engine.py → only 1 hit (the definition)

Furthermore, update() at line 920 (which contains a generic decay() call
at line 941) is NEVER called from server.py:
  grep '.update' server.py → 0 hits

The /consolidate endpoint calls consolidate_memories() directly and
increments _sim_time manually, bypassing update() entirely. So even the
generic accessibility decay never runs in the live system.
```

## Pitfall: Stale baseline in task context

Task context stated "13 real T2 memories." Live /health returned 29.
All 29 had valid text and unique trace_ids — not corruption, just a stale
baseline. **Always verify the claimed count against the live system.**
A stale baseline causes you to report "memory count changed!" as a finding
when it's just normal growth since the last audit.

## Key Files

- Engine: `ds-okeefe-engine/src/okeefe/core/engine.py`
- API server: `ds-okeefe-engine/src/api/server.py`
- Bridge: `okeefe_bridge.py`
- Auto-repair: `organism/auto_repair_watchdog.py`
- Fleet supervisor: `organism/fleet_autonomic_supervisor.sh`
- Persist: `<agent-home>/state/okeefe_memory.json` (226KB, 29 traces at audit time)
