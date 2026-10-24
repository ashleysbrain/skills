# Event-Loop Freeze Diagnosis — Writing Studio API (2026-08-19)

Worked example behind the "Event-Loop Freeze Diagnosis" subsection in the
SKILL.md. Operator: hermes. Task: T-260819-0041 (process deep-QA on the
Writing Studio session popout + brainstorm loop). Physics lens: critical
slowing down — response times trending 6s → 15s → 20s → infinity before
each tip, the variance itself the signal of a near-bifurcation regime.

## Symptom class

FastAPI/uvicorn server (`pipeline_api.py` on `:port`) wedged three times
in one session under research-search load:
- Process alive (`ps`: running, low CPU)
- Zero HTTP responses (curl times out)
- Only `kill -9 <PID>` + `launchctl kickstart -k` recovers
- Recurrence within minutes of restart under concurrent search traffic

## Wrong first hypothesis (threadpool exhaustion)

Initial theory: `sync def` endpoints doing blocking `urlopen` exhaust
FastAPI's default threadpool (min(32, cpu+4)). Converting the search
endpoint to `async` + `run_in_executor` should fix it.

Result: did fix one endpoint, but the wedge RECURRED. Hypothesis was
incomplete — the threadpool was a contributing factor, not the root.

## The tool that cracked it: macOS `sample`

While wedged (process alive, 0% CPU, no responses), ran:

```bash
sample <PID> 2 -file /tmp/api_sample.txt
```

`sample` outputs the **full call stack of every thread** including
C-level frames. `py-spy` and `faulthandler` do not show these.

### Reading the stack

Walked the main thread's stack under:
```
run_forever → task_step → _PyEval_EvalFrameDefault → ...
  → time_sleep → nanosleep
```

The deepest frame was `time_sleep` — a **blocking sleep executing ON
the uvloop event-loop thread**. This parks the entire server for the
sleep's duration. 0% CPU because the thread is literally napping in
`nanosleep`.

If the deepest frame had been `kevent` or `__psynch_cvwait` on worker
threads, the loop would be genuinely idle and the problem would be
elsewhere.

## Pinpointing the culprit (the `time.sleep` instrument)

`grep -n "time.sleep" pipeline_api.py` found only ONE hit — a
`sync-all-citations` endpoint. Fixed it (`time.sleep` → `asyncio.sleep`).
Wedge RECURRED.

Root cause: the sleeper was in an **imported module** that `grep` against
the API file alone missed. Instrument:

```python
# At module level in pipeline_api.py
import time as _diag_time, threading as _diag_threading, asyncio, traceback
_diag_orig_sleep = _diag_time.sleep
def _diag_sleep(sec):
    try:
        if threading.current_thread() is threading.main_thread():
            with open('/tmp/loop_sleep.log', 'a') as _f:
                _f.write(traceback.format_exc()[:1200] + '\n---\n')
    except Exception:
        pass
    return _diag_orig_sleep(sec)
_diag_time.sleep = _diag_sleep
```

Restart, trigger the wedge, read `/tmp/loop_sleep.log`:

```
File ".../research_bridge_engine.py", line 70, in _fetch
    with urllib.request.urlopen(req, timeout=timeout) as resp:
...
File ".../urllib/request.py", line 634, in http_response
    response = self.parent.error(
```

**Caught red-handed**: `research_bridge_engine._fetch` does `_t.sleep(2 ** attempt * 2)` in its 429-retry loop (2s, 4s backoff). Called from `async def` endpoints `/api/research/bridges` and `/api/research/trending-bridges` directly on the loop thread.

## The four culprit endpoints

| Endpoint | Defect | Fix |
|---|---|---|
| `GET /api/research/unified` | `def` (sync) holding threadpool for full OpenAlex+HN+news chain (5 urllibs, 15s each) | `async def` + `run_in_executor` |
| `POST /api/sessions/{sid}/rabbit-hole` | `def` (sync), 2 urllibs × 20s timeout on loop | `async def` + executor, timeouts 20→8s |
| `GET /api/research/bridges` + `/trending-bridges` | `async def` calling `research_bridge_engine._fetch` whose 429 backoff = `time.sleep(2s/4s)` on loop | wrapped in `run_in_executor` |
| `POST /api/publications/sync-all-citations` | `async def` calling `_time.sleep(1.2)` per row in loop | `asyncio.sleep(1.2)` |

## Fix pattern (each endpoint)

```python
# BEFORE (sync, blocks threadpool for full external chain)
@app.get("/api/search")
def search(q: str):
    result = blocking_external_search(q)
    return result

# AFTER (async + executor, loop stays responsive)
@app.get("/api/search")
async def search(q: str):
    import asyncio
    _loop = asyncio.get_event_loop()
    result = await _loop.run_in_executor(
        None, lambda: blocking_external_search(q))
    return result
```

```python
# BEFORE (bare sleep on loop)
import time as _time
_time.sleep(1.2)

# AFTER (yields control)
await asyncio.sleep(1.2)

# FOR imported library sleepers (don't patch the library):
await _loop.run_in_executor(None, lambda: library_call_that_sleeps())
```

## Verification (prove the class is dead)

### Concurrency stress (Python `threading`)

```python
import threading, urllib.request, json, time
def hit(url, out, key):
    try:
        req = urllib.request.Request(url, headers=H)
        t0 = time.time()
        with urllib.request.urlopen(req, timeout=30) as r:
            out[key] = (r.status, round(time.time()-t0, 1))
    except Exception as e:
        out[key] = ('ERR', str(e)[:40])

out = {}
threads = []
# 6 hub searches + 1 rabbit hole + 3 health polls = 10 concurrent
for q in ["active inference", "interoception", ...]:
    threads.append(threading.Thread(target=hit, args=(url, out, key)))
for t in threads: t.start()
for t in threads: t.join()
```

**Result:** all 200, wall 2.2s, health at 0.1s mid-storm.

### Re-profile under load

```bash
sample <PID> 2 -file /tmp/api_sample2.txt
grep time_sleep /tmp/api_sample2.txt
# → absent (no loop-thread sleepers)
```

### Instrument left in place

Left the `time.sleep` instrument active for the full session. No new
entries in `/tmp/loop_sleep.log` — confirms no remaining callers in
imported modules.

## Commit

`2ef7352` — `fix(P1): kill event-loop freezes — async executor wraps for
all blocking external calls (T-260819-0041)`

## Lessons

1. **`sample` > `py-spy` for uvloop freezes** — `sample` shows C-level
   frames (`time_sleep`, `nanosleep`) that `py-spy` and `faulthandler`
   don't, because uvloop's C extension isn't visible to Python-only
   profilers.
2. **The wrong hypothesis is not wasted** — the threadpool theory led
   to converting `sync def` → `async` + executor, which was a real fix
   for one endpoint. But it wasn't the ROOT. The `sample` profile was
   needed to find the loop-thread sleepers.
3. **Instrument `time.sleep` at module level** — a 10-line monkey-patch
   that logs the caller's traceback when on the main thread catches
   library-internal sleepers that `grep` against the API file alone
   misses. Leave it in place for the full session.
4. **The variance was the signal** — response times trending 6 → 15 → 20s
   before each wedge was critical slowing down in the flesh, not noise.
   Treat trending variance as a tipping-point warning, not a cosmetic
   metric.
