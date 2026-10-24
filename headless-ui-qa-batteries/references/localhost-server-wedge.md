# Localhost server wedges during UI batteries — recognition + recovery

Born 2026-08-19, Writing Studio pipeline-api (:port, FastAPI under launchd).

## The false-failure pattern

Mid-battery, every request starts returning `000` (curl timeout / Playwright net error)
while the process still shows LISTEN and the log is clean. The battery then reports a
cascade of failures that look like YOUR changes broke the app. They didn't.

## Signature table (diagnose before blaming your code)

| Symptom | Verdict | Action |
|---|---|---|
| 000s within ~20s of a restart | Cold import warmup, NOT a wedge | Wait, re-probe at t+20s |
| Process alive, 0% CPU, 000s at 5+ min uptime | True wedge (threadpool exhaustion) | kill -9 + kickstart ritual |
| `[Errno 48] address already in use` in log | Stale PID holding the port | `lsof -ti :PORT \| xargs kill -9`, then kickstart |
| Health OK but one endpoint times out | Single stuck external call | Check for blocking urllib in that endpoint |

## Recovery ritual (macOS launchd)

```
lsof -ti :port | xargs kill -9
launchctl kickstart -k gui/$(id -u)/com.your-org.pipeline-api
# wait ~20s (cold import), then health-check
```

## Root cause class: sync endpoints + blocking external HTTP

FastAPI runs sync `def` endpoints on a bounded threadpool (default 40). Each endpoint
that does blocking urllib/requests to external APIs (OpenAlex, Crossref — timeout=20s)
pins a thread for up to that timeout. Bursty fan-out (a UI page firing hub search +
rabbit-hole + library load simultaneously, all hitting a rate-limited upstream)
exhausts the pool; every subsequent request — including health checks — queues forever.
Process sits at 0% CPU because all threads are blocked on sockets.

Preceding signal (critical slowing down): response-time variance trends up first
(6s → 15s → 20s timeouts) before the full wedge. If a battery's timings degrade across
runs, stop and check threadpool saturation, don't keep firing.

Fix direction (hypothesis, verify before claiming): async endpoints + httpx with 8s
budgets, or urllib timeouts dropped to 8s, or admission control (serialize external
fan-outs from the UI). Never present the fix as done until re-run under the same burst
load that triggered the wedge.

## Battery hardening

- Health-check before AND after each battery; a post-run 000 means the battery's
  results are suspect, re-run after recovery.
- Stagger concurrent page actions that fan out to external sources; a battery itself
  can wedge the server it's testing (that's a finding, not a battery bug — record it).
- Record per-step timings in battery output; trend them across runs.
