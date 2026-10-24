# Battery addenda — Pass 5, B2BU persona matrix (2026-08-20)

Battery: /tmp/ws_qa_pass5_b2bu.cjs — 16/16 live. Writing Studio B2BU auth
(roster PIN + X-WS-User visibility scoping).

## Execution-context trap (hit 3x in one battery)
Host-scope helpers (sleep, check) do NOT exist inside page.evaluate —
browser context. `await sleep(600)` inside evaluate throws ReferenceError
and kills the whole evaluate. Inline delay inside evaluate:
  await new Promise(r => setTimeout(r, 600));
or wait host-side between evaluate calls.

## Auth-header verification: use the server echo, not a fetch spy
Wrapping window.fetch to sniff headers fails silently when the app serves
calls from the adiabatic cache — no network, no observation, spy returns
null while the feature works. Probe with GET /api/auth/me (echoes the user
resolved from request headers). Cache-satisfied list loads prove nothing.

## Browser binary rots
Hardcoded chrome-headless-shell path (mac-131) failed; cache had rotated to
mac-149.0.7827.22. Resolve at battery time:
  ls ~/.cache/puppeteer/chrome-headless-shell/

## Privilege edge worth re-testing on any identity feature
Persisted display-name -> auto-attached member header WITHOUT PIN was a
real hole (crash/logout edge escalates to member view). Rule: member
identity headers exist only after PIN success; roster hydration must
attach admin ids freely but never member ids.

## Auth'd fetches must use the wrapped fetch
_originalFetch bypasses the wrapper that attaches Authorization (Bearer) —
bare calls 401 against the token gate and the roster dies silently (null,
no console error). Use the wrapped fetch for all /api/auth/* UI calls.
