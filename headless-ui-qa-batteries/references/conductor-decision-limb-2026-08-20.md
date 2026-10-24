# Conductor Human-Decision Limb — principal ruling lane + drill family (2026-08-20)

Session: principal could not act on pending decisions ("I can't find anything to
click"). Built the human efferent limb on the organism conductor (:port,
`conduction_daemon.py` + `conductor_screen.py`), then upgraded task drill
to the studio/calendar interaction family. All bugs below were caught by
live browser verification, not code reading.

## The efferent-limb contract (reusable for ANY operator surface)

`POST /api/decide {task, ruling: APPROVE|REJECT|DEFER, note}` →
- Validates kind=decision AND state in (open, claimed); 409 otherwise.
- Writes the ledger with `actor='ceo'`, `actor_kind='human'` — one writer,
  the ledger. APPROVE → `done` (follow-on work minted by the loop on next
  scan), REJECT → `cancelled`, DEFER → stays `open` + a `deferred` event
  (no silent parking).
- **Test with a THROWAWAY decision task only** (mint sev=4 test task,
  exercise all three rulings, leave it cancelled). Never test on a real
  pending ruling.
- Buttons live BOTH in the queue row AND inside the drill drawer;
  ruling from the drawer re-opens the same task with fresh state.

## Laziness audit — the user's core requirement

principal directive: "human actions must NOT be the system getting lazy...
actual blockers, things that cannot be thought around." Every pending
`kind=decision` gets a think-around-ability audit before surfacing:

- **KEEP** if the only blocker is a standing principal rule the agent cannot
  waive: purchase power (buying hardware/services), naming law (no
  product-surface rename without sign-off), blueprint-first law (no seat
  minting without approval).
- **DOWNGRADE + EXECUTE** if the agent could resolve it with its own
  authority — that is delegated work masquerading as a decision.
- **SPLIT** when part is thinkable: execute the thinkable part, surface
  only the true blocker.
All 3 pending decisions survived the audit (each blocked by a standing
rule, not laziness) — but the audit must run every time the queue is
curated; unaudited queues rot into lazy escalations.

## Drill family standard (studio/calendar parity — principal directive)

"as dynamic as the research studio and the mosaic calendar... they go
together": a decision surface must join the existing interaction family,
not invent its own pattern. Standard: click-through drawer drill;
lifecycle timeline with human-vs-AI actor highlighting (human events get
the gold treatment); linked document rendered INLINE from the task's
detail JSON `{"doc": "....md"}` (6KB preview + truncation note), not just
a title; same-day sibling-task family with click-through; 30s deep-cycle
live refresh; ruling controls inside the drill.

## Bugs caught by live verification (each invisible to code reading)

1. **Entry-point regression (the big one).** Adding Approve/Reject/Defer
   buttons replaced the row's `onclick="drill(...)"` with
   `cursor:default`. Every existence check passed (functions defined,
   drawer markup present, buttons rendered in --dump-dom) but the user
   path was DEAD: clicking a row did nothing. Fixed by moving drill onto
   the task-id/title spans (dotted underline = "open detail" affordance),
   buttons stay separate so a click cannot accidentally rule.
2. **Silent handler death = empty reply, not a 500.** An unhandled
   exception inside a `BaseHTTPRequestHandler` method kills the
   connection with zero bytes (curl rc 52) while sibling GET endpoints
   keep working. Cause here: writing `state='rejected'` — not in the
   schema CHECK enum `('open','claimed','done','blocked','cancelled')`.
   Fix: wrap the whole POST branch in try/except → `_json(500)` +
   traceback to daemon stderr; find stderr via
   `launchctl print gui/$(id -u)/<label> | grep stderr`.
   Read schema CHECK constraints before writing enum values.
3. **Dead POST connections pin the ledger.** Client-timeout mid-handler
   left an open sqlite write txn; the next write hung (WAL +
   busy_timeout=0). Fix: `timeout=10` on connect, `PRAGMA
   busy_timeout=10000`, a `BEGIN IMMEDIATE`/`COMMIT` probe that returns
   503 "ledger busy" instead of hanging, and close in the finally path.
4. **Return-by-value footgun in raw CDP:** `Runtime.evaluate` of an async
   IIFE without `awaitPromise=True` returns `{}`. Either pass
   awaitPromise or click in one evaluate and poll state in a second.
   `JSON.stringify(...)` inside the expression moves objects across.

## Raw-CDP click-path recipe (when the Playwright client cannot run)

Works with the ms-playwright chrome-headless-shell binary directly:

```python
# 1. launch (background): <shell> --headless --disable-gpu \
#      --remote-debugging-port=9333 --no-first-run about:blank
# 2. target: curl -s http://localhost:9333/json/list -> webSocketDebuggerUrl
# 3. drive:
import json, asyncio, websockets
async def main():
    async with websockets.connect(WS, max_size=10**7) as ws:
        mid = 0
        async def cmd(method, **params):
            nonlocal mid; mid += 1
            await ws.send(json.dumps({"id": mid, "method": method, "params": params}))
            while True:
                m = json.loads(await ws.recv())
                if m.get("id") == mid: return m
        await cmd("Page.enable")
        await cmd("Page.navigate", url="http://localhost:port/")
        await asyncio.sleep(5)                     # let deep cycle render
        r = await cmd("Runtime.evaluate", returnByValue=True,
            expression="document.querySelectorAll('#i-rulings .fsubj')[1].click(); 'clicked'")
        await asyncio.sleep(2)
        r = await cmd("Runtime.evaluate", returnByValue=True, expression="""
          JSON.stringify({drawerOpen: document.querySelector('#drawer').className.includes('open'),
                          title: (document.querySelector('#drawer-body h3')||{textContent:''}).textContent.slice(0,55),
                          buttons: document.querySelectorAll('#drawer-body .rb').length})""")
        print(r["result"]["result"]["value"])
asyncio.run(main())
```

Probe discipline: check `typeof drill/openDrawer/$` first; if
`.click()` "succeeds" but nothing changes, suspect the element has no
handler (bug #1) rather than the click.

## Surfaces-family note

Two "conductor" surfaces exist: organism conduction screen :port
(immune/decision/rank) and the OS Conductor calendar :port. The decision
queue should eventually join the calendar timeline (decision deadlines on
the mesh) — flagged to the curator as the next family-join build.
