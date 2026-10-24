# O'Keefe Engine Bugs Found by Elite Panel Audits (2026-08-12)

Two rounds of 3-specialist panels (Popper/Bichat/Cannon, then
Bridgman/Sherrington/Turing) found and verified these bugs.
All P0/P1 items are FIXED. Open items are logged for sibling-agent.

## FIXED: Stale Process (P0)

**Symptom:** O'Keefe v1.0.0 running while v1.1.0 code on disk. v1.0.0
has no text field — all memories are vector husks.
**Diagnostic:** `status:"online"` = v1.0.0 (bad). `status:"ok"` = v1.1.0 (good).
**Fix:** Kill stale PID, restart with uvicorn.

## FIXED: Persistence Disconnected (P0)

**Symptom:** server.py created engine with `HippocampusEngine()` — no
persist_path. Startup script exported OKEEFE_PERSIST_PATH but server
never read it.
**Fix:** `_persist_path = os.environ.get("OKEEFE_PERSIST_PATH"); _engine = HippocampusEngine(persist_path=_persist_path)`.

## FIXED: Bridge Field Mismatch (P0)

**Symptom:** Bridge sent `location` (v1.0 field) but v1.1 expects
`location_vector`. Sent `max_results` but v1.1 expects `n_results`.
Pydantic silently dropped unknown fields.
**Fix:** Updated bridge to use correct field names.

## FIXED: Silent Amnesia on Corruption (P0)

**Symptom:** load_snapshot() catches all exceptions and returns None.
Engine boots with 0 traces, reports healthy. Next _persist() overwrites
the corrupt file with empty state — permanent data loss.
**Fix:** load_snapshot now backs up the corrupt file to
`{path}.corrupt_{timestamp}` before returning None.

## FIXED: Recall Formula Degenerate Regime (P0)

**Symptom:** v2 formula `max(0.5*kw, 0.3*floor) + 0.2*bonus` collapsed
to pure strength ranking when keyword overlap was low. Same 5
high-strength memories dominated every query. 4/5 queries returned
wrong results.
**Fix:** v3 formula `0.8 * keyword_overlap + 0.2 * normalized_strength`.
Keyword-dominant. Zero-keyword memory can never beat keyword memory.

## FIXED: Ghost CA3 Attractors (P1)

**Symptom:** ca3.store() was called BEFORE novelty check. When a trace
was dropped for low novelty, its CA3 attractor remained permanently,
contaminating retrieval. 30 ghost attractors from 9 dropped encodes.
**Fix:** Moved novelty check BEFORE ca3.store(). Rejected memories
never enter the CA3 network.

## FIXED: _trace_order.pop() Wrong Element (P1)

**Symptom:** Novelty drop did `_trace_order.pop()` which removes the
LAST element, not the dropped trace. Could orphan a different trace.
**Fix:** Novelty check moved before trace creation entirely. No pop needed.
Also added `if trace_id not in self._trace_order` guard for duplicates.

## FIXED: Silent Novelty Drop (P1)

**Symptom:** When novelty < 0.3, encode_experience returns "" (empty
trace_id). server.py returned this as `status:"encoded"` with HTTP 200.
Caller had no way to know the memory was rejected.
**Fix:** server.py now returns `status:"dropped"` with a message when
trace_id is empty.

## FIXED: No Boot-Time T2 Recall (P0)

**Symptom:** O'Keefe was write-only. the operator agent stored T2 memories but
never queried them at runtime. Both boot hooks printed static text
but never called recall. Zero of 32 cron jobs recalled from O'Keefe.
**Fix:** procedural-memory-boot.py now calls `_recall_t2_snapshot()`
which queries O'Keefe for 10 key project memories at every session start.

## FIXED: Health-Wait Too Short (P1)

**Symptom:** Auto-repair watchdog waited 8 seconds for engine health.
uvicorn cold-boot with numpy/scipy regularly exceeds this. 25% restart
failure rate.
**Fix:** Increased to 15 seconds. Added memory_count verification post-restart.

## FIXED: fsync Missing (P2)

**Symptom:** save_snapshot used temp-file + os.replace but no fsync.
On power loss, rename may not be durable.
**Fix:** Added `f.flush()` + `os.fsync(f.fileno())` before os.replace().

## OPEN: Vector Collision Silent Overwrite (MEDIUM)

**Root cause:** trace_id = `mem_{sim_time:.3f}_{content_hash}`. All
memories have timestamp=0.0 (sim_time never advances during /encode).
Identical content vectors produce identical trace_ids. Second store
silently overwrites the first.
**Owner:** sibling-agent — needs UUID + content_hash in trace_id.

## OPEN: Ebbinghaus Decay Dead Code (MEDIUM)

**Root cause:** `apply_ebbinghaus_decay()` defined at engine.py:111 but
never called. The `update()` method that calls generic decay at line 920
is also never called from server.py — /consolidate bypasses it entirely.
**Owner:** sibling-agent — wire decay into consolidation cycle.

## OPEN: Dual Supervisor Race (MEDIUM)

**Root cause:** Both auto_repair_watchdog (cron, 2 min) and
fleet-autonomic (launchd, 30s) independently restart dead engines.
No coordination. If both fire, they can fight over the port.
**Owner:** sibling-agent — needs coordination protocol or lock file.

## OPEN: Escalation Chain the operator agent-Dependent (LOW)

**Root cause:** After 3 restart failures, watchdog posts to
message-bus.db targeting the operator agent. If the operator agent is down, alert never
delivered. 30,292 historical escalations found silently consumed.
**Owner:** sibling-agent — needs launchd-level notification fallback.
