# Helper-Scope and Catch-Block Misdiagnosis Patterns (2026-08-20)

Two linked failure patterns found while adding a new view to the the OS
conductor screen (`conductor_screen.py`, served at localhost:port). Both
are generic to any single-file HTML app with multiple async render
functions sharing one fetch.

## Pattern 1 — Helper-Scope ReferenceError masquerading as network failure

**What happened:** A new async render function (`loadImmune`) reused a
helper (`kv()`) that LOOKED page-level but was actually
`const kv = (k,v,cls) => ...` defined INSIDE two other functions
(`loadHealth` at line 342, `loadAnalytics` at line 506), never at top
level. Calling it from the new function threw `ReferenceError`. The
surrounding `try/catch` ran and its catch block wrote
`"immune endpoint unreachable"` into the first render target — a FALSE
network error for a scope bug.

**Symptom signature:** SOME blocks fed by the same fetch render real
data (`i-open`, `i-rulings` had live rows) while ONE block shows an
error state (`i-angles` said "unreachable", `i-adapt` was empty).
If the fetch had actually failed, ALL blocks would be empty. Partial
render success = the fetch worked; the throw is inside render code.

**10-second confirmation:** `curl` the same endpoint. It returned
HTTP 200 in 8-25ms on every try while the page claimed unreachable.
Endpoint fine → the bug is in the render path.

**Fix 1 — per-block isolation + honest catch.** Never let one catch
speak for the whole handler. Report `e.message`, not a guessed cause:

```javascript
} catch(e) {
  $('i-angles').innerHTML = '<div class="empty">render error: ' +
    (e && e.message ? e.message : 'unknown') + '</div>';
}
```

With this, the page would have shown `render error: kv is not defined`
on the FIRST try instead of sending the debugger to the network layer.

**Fix 2 — hoist shared helpers.** Helpers used by multiple render
functions (`kv`, `esc`, `ago`) get ONE top-level declaration:

```javascript
// BAD: helper defined inside each consumer (N copies, 0 shared)
async function loadHealth()   { const kv = ...; }
async function loadAnalytics(){ const kv = ...; }
async function loadImmune()   { kv(...)   // ReferenceError
}

// GOOD: one top-level function declaration
function kv(k, v, cls) { return '<div class="kv">...'; }
```

**Detection grep:** `grep -n 'const kv\|function kv' file` — hits
inside multiple function bodies means every external caller is a
latent ReferenceError. Same check for any small render helper.

**Key insight:** catch-block error messages are GUESSES, not
diagnostics. "endpoint unreachable" written by a catch block proves
only that SOMETHING threw — the writer of the message assumed the
fetch was the throw site. Treat the assumption as a hypothesis, not
a finding.

## Pattern 2 — curl-works-but-page-fails is NEVER a network problem

Corollary worth internalizing as a triage rule:

| Observation | Actual bug location |
|---|---|
| curl 200 + page block empty, console clean | render code threw inside try/catch (this pattern) |
| curl 200 + page block empty, console shows fetch error | CORS / mixed content / wrong origin |
| curl fails too | server actually down — fix the server |

The first row is the most misdiagnosed because the catch block's
guessed message ("unreachable") pre-loads the wrong hypothesis.
Always run the curl check before trusting any catch-block message
that names a cause.

## Verification habit that caught it

After the fix, re-run the full-page dump and assert EACH block's
rendered content contains expected tokens (not just that the page
returns 200):

```
i-angles   -> '<span class="ftype">TECHNICAL</span>...'   (4 angle rows)
i-open     -> '137 open items'
i-rulings  -> 'T-260817-0006'                             (real IDs)
i-adapt    -> 'context vector'
```

One block at a time — page-level PASS masks per-block render throws
(same class as the multi-stage pipeline lesson: a pipeline is the
data flow, not the modules).
