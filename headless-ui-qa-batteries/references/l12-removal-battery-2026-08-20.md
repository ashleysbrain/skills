# L12 removal battery — PIN purge → federated identity (2026-08-20)

Battery: `/tmp/ws_qa_l12.cjs` — 13/13 PASS live (playwright-core + cached
chrome-headless-shell, the established rig).

## Context

principal rejected the PIN member-auth system as archaic (Law L12 "build forward,
not backward"). The battery had to prove the purge AND the forward surface in
one run. Full pivot record: `b2b-organism-spinup/references/l12-build-forward-pivot-2026-08-20.md`.

## Checks that generalize to any removal-falsification battery

1. `pinModal` absent from DOM (getElementById → null)
2. `wsPin*` functions undefined (`!window.wsPinOpen && !window.wsPinSubmit`)
3. `ws_user_id` absent from localStorage (client-trust key purged)
4. Forward surface present + visible: `wsGoogleBtn` offsetParent !== null
5. Roster real: 4 users, canonical ids exactly `P-ANGELA,P-ASHLEY,P-BRANDON,P-NANDITA`
6. Identity selector paints the roster (NOT just the hardcoded fallback)
7. Honest-pending: click → tbSub shows "OAuth credentials" message; NO navigation
8. Still on the app origin (no fake redirect)
9. Zero page errors
10. Admin view intact (heroStatus painted, dash-metric cards present)
11. composeAuthor follows roster
12. Author preserved through dependent flows (selectPipeline)
13. Fetch the local token via page.evaluate first; probe roster with explicit
    Bearer to separate "API works" from "UI wiring works"

## Bugs the battery caught (and their fixes)

- **Auth-race:** roster fetch fired pre-token; `/api/auth/users` 401'd silently
  (exempt from the wrapper's 401-retry because it matches `/api/auth/`).
  Symptom: selector painted only 'the principal Williams'. Fix IN THE PRODUCT:
  `await window._authPromise` at the top of `wsLoadRoster()`. Battery-side:
  wait ~1.5s after boot before asserting selector contents.
- **Hardcoded metric count:** the battery assumed >= 3 `.dash-metric` cards;
  the real dashboard renders 2 (it was built for 4 but only 2 elements carry
  the class on this build). Probe the REAL count before hardcoding count
  assertions — assert against observed truth, not remembered truth.

## Rig notes

- `require('/<workspace>')` +
  executablePath chrome-headless-shell mac-149 — same as pass 5.
- `pw.chromium.launch(...)` NOT `pw.launch(...)` — playwright-core exports the
  browser-type factory.
- `page.evaluate(async (arg) => {...}, tok)` for passing args into evaluates.
