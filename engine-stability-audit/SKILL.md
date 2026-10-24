---
name: engine-stability-audit
description: Confirm or refute engine fix claims with hard timing data.
version: 1.0.0
author: the specialist engine
license: MIT
metadata:
  hermes.tags: [organism, stability, audit, verification, performance, persistence, concurrency]
  hermes.category: software-development
  hermes.related_skills: [engine-depth-gate, systematic-debugging, code-review]
---

# Engine Stability Audit

Independently verify whether claimed engine/code fixes actually hold under stress.
Produce CONFIRMED FIXED / STILL BROKEN / PARTIAL verdicts, each backed by hard
evidence (counts, timing, R² regression fits, grep hits). Never accept a fix
claim on faith — re-test it empirically.

Companion to `engine-depth-gate` (which verifies *static* build depth: lines,
layers, physics). This skill covers *dynamic* stability: does the engine actually
persist, scale, dedup, handle concurrency, and bound its growth?

This skill covers BOTH halves of the loop:
1. **Audit** — find defects and confirm/refute fix claims with hard evidence.
2. **Fix verification** — after applying a fix, prove it holds under the same stress
   that exposed the original defect. A fix that passes the author's happy-path but
   fails the audit's stress test is not fixed.

## When to Use

- Re-auditing an engine after someone (the operator agent, sibling-agent, a subagent) claims defects were fixed
- Pre-production stability check on a stateful engine (memory, queue, cache, store)
- Verifying a migration (e.g. in-memory dict -> SQLite) didn't introduce new defects
- **Auditing an agent-built REIMPLEMENTATION/rewrite of an engine** (port,
  framework escape, cross-language rewrite) — run the Differential
  Verification Protocol FIRST (below); fidelity precedes stability
- **Verifying your own fixes** before declaring a defect closed — re-run the exact test
  that failed, plus the regression suite below
- Any "confirm or refute each fix claim with hard timing data" task

## Differential Verification (agent-built reimplementations) — fidelity before stability

When the audited change is a REIMPLEMENTATION (a rewrite of a reference
implementation — MATLAB→Python port, framework escape, cross-language
rewrite), the engine's own tests prove nothing about fidelity: the agent
that misread the reference also writes the tests. The reference
implementation is the only valid oracle.

**Protocol (Spynach pattern, T-261021-0049, the specialist engine immune GENOME):** an
agent-built reimplementation is accepted only when EVERY stage is
differentially verified against the reference — both sides executed on
identical inputs, outputs compared with the correct comparator class
(exact / tolerance / periodic for phase-wrapped / keys / statistical Welch-t
for stochastic), per-stage verify/pass counts reported, ZERO unverified
stages shipped. A skipped stage is a rejection, not a concession.

Executable harness + selftest (15/15 falsification checks incl the
261023 adversarial battery F10-F14: invalid-spec rejection, comparator-crash
containment, partial-selection law, self-reference refusal, statistical
floor): `scripts/differential_verification.py` (manifest schema, comparator
taxonomy, and acceptance law inside).

Run it BEFORE the 8 standard tests: a rewrite that is stable but not
differentially verified is STILL BROKEN — wrong physics that never crashes
is the worst failure class. Full protocol:
`references/differential-verification-protocol.md`.

## Core Principle: Empirical + Code-Inspection Cross-Check

Every claim gets TWO lines of evidence:
1. **Code inspection** — read/grep the hot path to *predict* the behavior before testing.
2. **Empirical test** — run the engine under stress and measure. The measurement must
   *confirm or refute* the prediction. If they disagree, trust neither until resolved.

A claim is CONFIRMED FIXED only when both agree. Code looks right but test fails =
something else is wrong. Test passes but code looks wrong = the test isn't stressing
the real path.

## The 8 Standard Tests

Run these against an **isolated temp DB** per test (never the production DB):

| # | Concern | Method | Verdict logic |
|---|---------|--------|---------------|
| 1 | **Persistence** | Encode N, destroy engine/kill process, read via raw `sqlite3` in a fresh process. Then encode M more, kill, read N+M. | All rows survive across process death = FIXED |
| 2 | **Full-set processing** | Encode >batch-size items, call the batch operation, count how many were processed. | All processed (not capped at batch size) = FIXED |
| 3 | **Encode scaling** | Multi-trial timing regression (see below) | Bounded per-op cost = FIXED; per-op cost grows with N = BROKEN |
| 4 | **Dedup** | Encode identical input N times, count rows | 1 row + access counter bumped = FIXED |
| 5 | **Eviction / bounds** | Encode past any declared ceiling, count rows | Ceiling enforced = FIXED; dead constant = BROKEN |
| 6 | **Concurrent writes** | N threads writing simultaneously, count survivors + errors | No lost writes / constraint errors = FIXED |
| 7 | **Corruption / WAL** | Hard-kill subprocess mid-batch, then `PRAGMA integrity_check` | integrity_check = ok = structurally safe |
| 8 | **Large content** | Encode max-expected-size payload, retrieve byte-exact | Exact round-trip = FIXED |

## Timing Regression Methodology (THE critical technique)

**Small-N timing is misleading.** A single run at N<=200 will often show "bounded"
behavior because constant-factor overhead (SQLite connection setup, Python import)
dominates at small N. This produces false CONFIRMED FIXED verdicts for O(N^2) bugs.

### Correct method

1. **Warm up** to each checkpoint with real unique inputs (not a loop of the same string —
   that exercises dedup, not the scaling path).
2. At each checkpoint (N = 50, 100, 200, 400, 800, 1200), take **5 trials** and use the
   **median** (not mean — outliers from GC/scheduler jitter are common).
3. Fit **both** linear (`t = a*N + b`) and quadratic (`t = c*N^2 + a*N + b`) models. Compute
   R^2 for each.
4. Classify:
   - Linear fit R^2 > 0.9 with positive slope -> **per-op cost is O(N)** -> aggregate work
     for N ops is **O(N^2)** -> STILL BROKEN at scale.
   - Quadratic R^2 beats linear R^2 by >0.02 with c>0 -> per-op is O(N^2) -> aggregate O(N^3) -> severely broken.
   - Flat (slope ~= 0, R^2 poor because no trend) -> CONFIRMED FIXED.

### Why median-of-5 matters

Single trials at small N bounce wildly (observed: 1.9ms -> 37ms -> 4.4ms for the *same*
operation at N=1/25/50). The median-of-5 regression smoothed this into a clean linear
fit (R^2=0.93) that correctly identified O(N) per-call growth. See
`references/hippocampus-reaudit-2026-08-12.md` for the exact data where the initial
single-trial N<=220 test gave a WRONG answer.

## Dormant-Layer Verification (when auditing newly-added layers)

When a re-audit is triggered by "new layers were added to the engines," the FIRST
question is whether those layers are actually live. A layer that is well-written
but never imported into the request path is **dormant** — it cannot cause runtime
instability no matter what its buffers do. Prove dormancy (or liveness) before
spending time stress-testing the layer's internals.

**Method:**
1. Grep the engine's `server.py` (or equivalent entry point) for imports of the new
   layer module. `from X.core.cognitive import` absent = dormant.
2. Grep ALL `.py` files in the engine dir (excluding the layer's own definition file)
   for instantiation of the layer's classes (`CognitiveLayer(`, `FindingBuffer(`, etc.).
3. If the only references are in `tests/`, the layer is dormant. A `cognitive_layer=True`
   flag in a `/health` response is **advertising metadata**, not proof of wiring.
4. For dormant layers: still note latent risks (below) but verdict is "no runtime risk."
   For live layers: run the full stress suite against the endpoints that invoke them.

**Why this matters:** A re-audit that spends 30 minutes stress-testing a layer's
buffer bounds, only to discover the layer is never called, has wasted the budget.
Dormancy check takes 2 minutes and routes effort correctly.

## Code-Inspection Checklist (run BEFORE timing)

These greps predict behavior and catch defects timing might miss at small N:

- **Hot-path scan:** Does the write/encode path call a `_load_all()` / full-table-scan
  followed by a Python-level O(N) loop? -> predicts O(N) per-op, O(N^2) aggregate.
- **Dead constants:** `rg -n 'SOME_CEILING'` — if the only hit is the definition line,
  the constant is dead code. The ceiling is NOT enforced.
- **Non-atomic ID generation:** Does `_next_id()` do `SELECT MAX(id)+1` then a separate
  `INSERT`? -> predicts a TOCTOU race under concurrency (test #6 will surface it as
  `UNIQUE constraint failed`).
- **Eviction/TTL:** grep for `evict`, `ttl`, `max_size`, `DELETE ... ORDER BY ... LIMIT`
  in the prune path. Absent = unbounded growth for any phase that isn't actively pruned.
- **Transaction discipline:** grep for `PRAGMA`, `journal_mode`, `wal`, `BEGIN`, `commit`.
  Absent = relies on SQLite defaults (rollback journal, FULL synchronous) — safe but slow.
- **Unbounded per-profile lists (cognitive/tracker layers):** grep for
  `profile["..."].append(` or `_changes.append(` backed by a plain `= []` or
  `defaultdict(list)`. These are dict-of-lists that grow without bound per entity key.
  Distinct from the bounded `deque(maxlen=N)` working-memory buffers they sit next to.
  Latent leak: harmless while the layer is dormant; must be capped (wrap in
  `deque(maxlen=N)`) BEFORE the layer is wired into any request path.

## HTTP Endpoint Stress Test (running servers)

Distinct from the in-process timing regression above. Use this when the engine is a
live FastAPI/uvicorn server on a port and you must test it over HTTP (the real request
path), not via in-process function calls.

**Method:**
1. **Confirm each engine is up** — `GET /health` on each port before testing. A down
   engine is not a stability finding; it's a setup gap.
2. **Discover the request schema** — read the Pydantic `Request` model from `server.py`
   BEFORE firing calls. A `422 Unprocessable Content` storm from a wrong field name
   wastes a stress run and looks like 100% failure. Warm up with one call per endpoint.
3. **Warmup pass (discard)** — fire one call per engine before measuring. First-call
   latency includes import/JIT overhead and is not representative.
4. **50 sequential calls per engine** with unique payloads (so dedup doesn't mask the
   write path — see dedup caveat in the in-process method above).
5. **Compute the right stability metric.** This is the non-obvious part:
   - **Coefficient of variation (CV = stdev/mean)** is a TRAP here. HTTP latency
     distributions have heavy right tails from occasional GC/scheduler spikes. A single
     20ms spike in a sea of 3ms calls inflates CV to >1.0, falsely flagging "UNSTABLE."
   - **Quartile trend (first-quartile-mean vs last-quartile-mean)** is also a trap when
     periodic spikes happen to cluster in one quartile — an apparent +164% trend that is
     really a flat 3-4ms baseline with a ~21ms spike every ~8 calls.
   - **Correct approach:** (a) **trimmed mean** (discard top/bottom 10%) for a stable
     central-tendency number, (b) **per-call drill-down** (print all 50 times) to
     visually confirm the spike pattern is periodic, not progressive, and (c) verdict
     on **flat-or-negative trend with no progressive growth**. Periodic spikes at a
     constant interval = scheduler artifact = STABLE.
6. **Report p50/p95/p99 + trimmed mean + per-call spike pattern.** Do not report only
   p50 and max — the max tells you a spike happened, not whether latency is degrading.

**Shared-singleton note:** FastAPI servers typically hold the engine as a module-level
global (`engine = FooEngine()`). This is read-mostly and safe under FastAPI's
async/await for stateless compute engines. For stateful engines (Hippocampus with
SQLite writes), the engine's own concurrency controls (WAL, BEGIN IMMEDIATE) handle
safety; you do not need to see a threading.Lock in server.py to call it stable.

**localhost IPv6 false-DOWN pitfall:** On macOS, `curl http://localhost:<port>/health`
resolves `localhost` to BOTH `::1` (IPv6) and `127.0.0.1` (IPv4). If the uvicorn
server binds `0.0.0.0` (IPv4-only), the IPv6 connection is refused first and curl
may report "Connection refused" / return empty before the IPv4 fallback succeeds —
or fail entirely depending on curl version and timing. This produces **false "DOWN"
readings** on a live engine. Always use `http://127.0.0.1:<port>` explicitly in all
health checks, stress calls, and subprocess `execute_code` scripts. This is a
false-positive trap of the same class as the CV/quartile-trend traps above.

## Regression Re-Audit Battery (round N+ quick confirmation)

When you are on audit round 2+ (or later) and the goal is **"verify no regressions
from a change"** rather than first-time deep discovery, run the compact battery below.
It covers all failure modes in ~3 minutes without the full single-defect deep-dive
overhead. If ANY cell shows degradation, escalate to the full suite for that engine.

| Step | What | Pass criterion |
|------|------|----------------|
| 1. Fleet health | `GET /health` on every port (use `127.0.0.1`) | All return `status: ok` |
| 2. Encode flatness | 50 sequential encodes on Hippocampus | median <50ms, drift <50%, no progressive growth |
| 3. ATK load | 20 rapid sequential calls on each ATK engine | 0 errors, median <100ms, no slowdown drift |
| 4. Eviction cap | Encode 100 at the cap, re-check `/v1/stats` | total_memories stays at ceiling (e.g., 1000) |
| 5. Cognitive layers | `GET /v1/cognitive` on all engines post-load | All return non-empty JSON (>500 bytes) |
| 6. RSS stability | `ps -o rss=` before and after 20 calls per engine | delta <5% (no monotonic growth) |

**Report format for regression audits:** STABLE or UNSTABLE with a compact timing
table (median/p95 per engine). Do not over-narrate — if it's clean, say so and stop.
The point of a regression audit is a fast yes/no, not a re-discovery pass.

## Persistence Test: Must Bypass the Engine

**Never** verify persistence with `engine.get_stats()` alone — it may read from an
in-memory cache even when the backing store is broken. The definitive test:

1. Encode N items in the engine.
2. **Destroy the engine object** (`del eng`) — releases any held connection.
3. Open the DB file with **raw `sqlite3`** in a **fresh process** (subprocess or new
   script). Count rows directly. This proves the bytes are on disk, not in a cache.

For the strongest test: encode in subprocess A (`os._exit(137)` to simulate SIGKILL),
then read in subprocess B. See `references/hippocampus-reaudit-2026-08-12.md` test 7.

## Concurrency Test Pattern

```python
errors = []
def writer(n):
    try:
        for i in range(K):
            eng.encode(f"thread-{n}-item-{i}")
    except Exception as e:
        errors.append(str(e))
threads = [threading.Thread(target=writer, args=(n,)) for n in range(N_THREADS)]
for t in threads: t.start()
for t in threads: t.join()
# survivors == N_THREADS * K  AND  errors == []  =>  FIXED
```

If you see `UNIQUE constraint failed: <table>.id`, the root cause is almost always a
non-atomic `SELECT MAX(id)+1` -> `INSERT` sequence (TOCTOU race). The fix is an
`AUTOINCREMENT` column, `INSERT ... ON CONFLICT DO NOTHING`, or a transaction-wrapped
id generation. Note: this is a defect *introduced by* naive SQLite migrations from
in-memory dicts — the in-memory version didn't have the race because the GIL serialized it.

### PITFALL: sequence-table seed off-by-one

A common fix is a `memory_seq` table with `BEGIN IMMEDIATE` atomicity. **The naive
seed is wrong**: `INSERT INTO seq VALUES (1)` then "read next_val, return it, bump"
returns `1` on BOTH the first and second call (first call reads the just-inserted 1;
second call reads 1, returns 1, then bumps to 2). Collision on call #2.

Correct semantics: **`next_val` stores the NEXT id to hand out.** First call returns 1
and seeds `next_val = 2`. Every subsequent call reads-and-returns, then increments.
Transcribed sequence-table fixes must be tested with ≥3 sequential encodes, not just 1,
or the collision won't surface.

## Test Harness Pattern

Each test gets an isolated temp DB so tests don't contaminate each other:

```python
import tempfile
def fresh_engine(tag):
    db = os.path.join(tempfile.mkdtemp(), f"{tag}.db")
    return HippocampusEngine(db_path=db), db
```

Run tests **in-process** via `execute_code` (not by writing a script file — workspace
write gates may block new files, and in-process runs avoid path issues). If a test needs
a true process boundary for persistence/corruption tests, spawn a **subprocess** that
imports the engine, does the work, and `os._exit()`s.

## Verdict Format

Each finding: `[TEST-ID] => CONFIRMED FIXED | STILL BROKEN | PARTIAL` followed by one
line of hard evidence (the actual count, timing, R^2, or grep result). End with a
scorecard table and a bottom line: "X of Y original defects confirmed fixed; Z still
broken; plus N new defects found."

## Pitfalls

- **Trusting small-N timing** — the #1 source of false CONFIRMED FIXED verdicts. Always
  scale to N>=800 and use median-of-5 regression. (See references for the exact case where
  N<=220 gave the wrong answer and N<=1200 corrected it.)
- **Verifying persistence through the engine's own API** — caches lie. Read the DB file
  with raw sqlite3 in a separate process.
- **Forgetting to cross-check code vs. timing** — if timing says "fixed" but the code
  still has a full-table-scan + O(N) loop, the test isn't reaching scale. Don't declare
  fixed until both agree.
- **Counting dedup access_count wrong** — first insert sets access_count=0, each
  subsequent dedup bumps it by 1. So 10 identical encodes -> access_count=9, not 10.
- **Assuming a "claimed fix" was actually applied** — read the code. The claim "processes
  all in batches" might mean the `[:10]` slice was removed (real fix) or might be
  unsupported by the code (claim without implementation).
- **Patching the file but testing the old process** — if the engine is a long-lived server
  (uvicorn/FastAPI on a fixed port), starting a background server can fail silently if the
  port is already held by the production instance. Your HTTP requests then hit the OLD
  code while you believe you're testing the patch. Always confirm the test server is the
  process on the port (`lsof -nP -iTCP:<port>`), use a DIFFERENT isolated port for
  verification, and check the server's stdout/stderr for bind errors before trusting
  responses. A 200 response from an old process is a false CONFIRMED FIXED.
- **Proving O(1) with a single checkpoint** — "encoded 1000 fast" does NOT prove O(1);
  it only proves the constant factor is small at N=1000. The rigorous proof is
  **first-half vs last-half ratio**: time the first 50 encodes (small DB) and the last 50
  (large DB). O(1) holds the ratio near 1x; O(N) per-op shows a ratio ≈ N_final/N_start
  (e.g. 17x). The 23.4s/1000-encode number in the Hippocampus audit was O(N) per-op, not
  a slow O(1).
- **Doubly dead code** — a method can be "called" by another method that is itself never
  called. `apply_ebbinghaus_decay()` was defined and looked correct, but `update()` (the
  only caller) was never invoked from `server.py` — the /consolidate endpoint bypassed it
  entirely. Always trace the FULL call chain to the entry point (server.py / main /
  route handler), not just one level up. `grep -n 'method_name' *.py` across ALL files,
  not just the defining module.

## Read-Only Fix Verification (no destructive tests)

When the engine is production-critical and you CANNOT kill it, corrupt files,
or run destructive stress tests, use **read-only fix verification** instead.
Every fix claim still gets two independent lines of evidence — just read-only ones.

### Protocol

1. **Code at exact line numbers** — Read the actual source file. Cite exact line
   numbers where each fix component sits. Confirm execution order by tracing line
   numbers (e.g., "novelty check at line 730 fires before ca3.store() at line 737").
   Never accept a description of the fix — read the code.
2. **Live read-only API calls** — `GET /health`, `GET /memories`, `GET /retrieve`
   or bridge `recall()`. Never POST/encode/delete on a production system unless
   explicitly authorized.
3. **Persist-file analysis** — Read the JSON/SQLite backing store directly with
   `json.load()` or raw `sqlite3`. Check: trace count matches /health, no duplicate
   IDs/hashes, no empty text, timestamp distribution.
4. **Dead-code grep** — `grep -n 'method_name' engine.py`. If the only hit is the
   definition line, it's dead code. For "X calls Y" claims, grep for Y's name across
   ALL files — if Y appears only in its own definition, the call path is broken.

### When to use this instead of the stress suite

- Production engine with real user data that cannot be risked
- Task explicitly says "do NOT run destructive tests"
- Quick re-verification of a previously-stress-tested fix
- Verifying fix ordering claims (e.g., "check moved before store")

### Stale-baseline pitfall

Task context or prior audit notes may state a memory count (e.g., "13 memories")
that is stale by the time you run. Always verify the claimed count against the
live system. A count change is normal growth, not corruption — check for valid
text and unique IDs before reporting it as a finding.

See `references/okeefe-readonly-fix-verification-2026-08-12.md` for the full
worked example: 7 fixes verified read-only, 4 open items confirmed still open,
including the "doubly dead code" pattern (method never called + the method that
would call it is also never called).

## Operational Resilience Audit (the supervision layer)

After verifying an engine's internal stability (does it crash under stress?),
audit whether the SUPERVISION SYSTEM can keep it alive unattended. Internal
stability + working supervision = true production readiness. Internal stability
+ broken supervision = the engine dies and nobody notices.

### The supervision audit checklist

1. **Boot coverage:** Does ANY launchd plist, systemd unit, or crontab entry
   start this engine at machine reboot? Check `launchctl list`, `ls ~/Library/LaunchAgents/`,
   `crontab -l`. If nothing starts it, that's CRITICAL.
2. **Supervisor restart window:** How long does the watchdog wait for `/health`
   after spawning a new process? If it's <10s and the engine imports numpy/scipy/
   torch, cold-boot will intermittently exceed it → false-failure restarts.
3. **Post-restart persistence verification:** After ANY restart, does the
   supervisor check that persisted state loaded? Probe `memory_count` (or
   equivalent) in `/health`. A restart that amnesia'd is worse than no restart.
4. **Escalation path:** After retries exhaust, where does the alert go? Trace
   the FULL chain: watchdog → message bus → consumer cron → delivery channel.
   If the consumer is the same process that might be down (e.g., the operator agent), the
   escalation is single-point-of-failure.
5. **Dual-supervisor race:** If two independent supervisors both restart dead
   engines, do they coordinate? If not, one can kill the other's freshly-started
   process via `_kill_port_holders()`.
6. **Unattended survival estimate:** Based on observed death rate and restart
   success rate, how long before data loss or permanent degradation?

See `references/okeefe-operational-resilience-audit-2026-08-12.md` for the
full worked example with live command outputs, self_healing.db analysis, and
a 7-day survival estimate methodology.
- `references/okeefe-readonly-fix-verification-2026-08-12.md` — the specialist engine read-only
  verification of 7 claimed O'Keefe fixes (all confirmed) + 4 open items (all confirmed
  still open). Covers the read-only verification protocol (code-at-line-numbers, live
  GET-only API calls, persist-file analysis, dead-code grep), the stale-baseline pitfall
  (task said 13 memories, live had 29), and the "doubly dead code" pattern
  (apply_ebbinghaus_decay never called + update() that would call it also never called).

## Test Depth Scoring (companion technique)

Stability auditing verifies RUNTIME behavior (persistence, scaling, concurrency).
Test depth scoring verifies whether the TEST SUITE ITSELF has enough depth to be
trusted — distinct from "tests pass." A file of 15 tests that all assert
`isinstance(x, dict)` passes but constrains nothing (THEATER). The 5-engine
final audit (ATC-01 through Hippocampus, DS J Eccles) produced a reusable scoring
methodology: reference-anchored LOC/assertion/class metrics + theater detection
(strong vs weak assertions) + live execution + multi-round upgrade tracking.

**When to use it:** production-readiness scoring of an engine's test suite,
multi-round iterative audits (NEEDS-WORK → PRODUCTION-READY), or detecting
shallow/theater test files that look tested but aren't.

See `references/test-depth-scoring-methodology.md` for the full 7-dimension rubric
(LOC, assertions, categories, theater detection, live execution, **live falsifiability
verification**, **mtime regression gate**), metric computation script, and the 5-engine
scored example across 6 audit rounds.

## References

- `references/differential-verification-protocol.md` — DIFFERENTIAL-VERIFICATION
  PROTOCOL (T-261021-0049, Spynach pattern): stage inventory, comparator-class
  taxonomy (exact/tolerance/periodic/keys/statistical-Welch-t), zero-unverified
  acceptance law, report format, falsification battery F1–F14 (incl the
  261023 adversarial station hardening: spec validation, crash containment,
  partial-selection law, self-reference refusal, statistical floor). Harness:
  `scripts/differential_verification.py --selftest`.
- `references/test-depth-scoring-methodology.md` — scoring rubric for evaluating
  whether a test suite is deep enough for production (LOC/assertions/coverage
  against a reference engine + theater detection + live execution). Includes a
  reusable Python scoring function and a worked example across 5 engines.
- `references/hippocampus-reaudit-2026-08-12.md` — full the specialist engine re-audit of the
  Hippocampus engine: 5 original defects re-tested, 3 confirmed fixed, 2 still broken,
  1 new concurrency defect found. Includes the exact timing data showing how small-N
  testing gave a false negative and the regression methodology corrected it.
- `references/hippocampus-fix-verification-2026-08-12.md` — the specialist engine's fix-and-verify
  cycle for the 3 defects the re-audit left open (O(N^2) encode, no eviction, concurrent
  write race) plus WAL enablement. Documents the sequence-table off-by-one bug in the
  naive fix, the first-half-vs-last-half O(1) proof method, and the production-port
  isolation pitfall. Use this as the template for verifying any audit-flagged defect fix.
- `references/hippocampus-third-audit-cognitive-layers-2026-08-12.md` — Third audit:
  cognitive layers added to all 5 engines. Covers dormant-layer verification (grep
  server.py for imports BEFORE stress-testing layer internals), unbounded per-profile
  list detection (`profile["scores"].append()` escaping `deque(maxlen=)`), and the
  HTTP stress-test false-UNSTABLE lesson (CV and quartile-trend both mislead on
  heavy-tailed latency; use per-call drill-down + trimmed mean).
- `references/okeefe-operational-resilience-audit-2026-08-12.md` — the specialist engine audit
  of whether the O'Keefe supervision system (auto_repair_watchdog + fleet-autonomic
  launchd) can keep the engine alive unattended. Covers: boot coverage verification,
  8s restart-window false-failure pattern, post-restart amnesia (memory_count=0 with
  populated persist file), the operator agent-dependent escalation chain with no independent
  fallback, dual-supervisor race condition, and a 7-day survival estimate methodology.
