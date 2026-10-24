# PASS-3: server-side gate hardening (2026-08-19)

Rotation: build Da Vinci -> PASS-2 Popper -> PASS-3 Luria. User distrust
("do another qa pass, I don't trust you") was warranted: live probes broke
three PASS-2 claims. Class lesson: a gate you verify only through the
honest client path is unverified.

## Shape validation is not enforcement

PASS-2 added a "server-side" novelty gate that:
1. fired only when the client self-declared `source: "brainstorm-canvas"`,
2. trusted a client-asserted `novelty` JSON token,
3. checked TTL one direction (future timestamps passed).

All three broken live:

| Probe | Payload | Before | After |
|---|---|---|---|
| no-source bypass | `tags:["course"]`, no source, no novelty | 200 created | 422 |
| forged-future | verdict CLEAR, scanned_at +365d | 200 created | 422 |
| forged in-window | verdict CLEAR, plausible scanned_at, never scanned | 200 created | 422 |
| dup variant | same title, case/whitespace changed | 200 duplicate | 409 |
| outage | all three prior-art APIs unreachable | verdict CLEAR | UNKNOWN |

## Hardened pattern (pipeline_api.py, reusable)

- Gate keys on WHAT the item is (`tags` contains "course" OR title starts
  `[COURSE]`), never on a client-supplied provenance field.
- Verdicts are issued server-side at scan time into `_NOVELTY_SCANS`,
  keyed `sha256(claim)`. Queue-time gate accepts only a verdict the server
  itself issued for the same claim (compares verdict + scanned_at within
  2s). Client-asserted tokens are rejected even inside the TTL window.
- TTL is two-sided: `0 <= age < 3600`. Future = forged.
- A scan where zero prior-art sources were reachable returns UNKNOWN, not
  CLEAR ("no evidence of prior art" != "evidence of novelty");
  `sources_checked` lists only sources that actually responded.
- Client additionally blocks UNKNOWN/TAKEN before any network call
  (verified in-browser with a request listener: zero POSTs fired).

Known gap (accepted, documented): `_NOVELTY_SCANS` is in-process — server
restart forgets issued scans and the user must re-scan. Persist to sqlite
if multi-user.

## The guard that "passed" by crashing

Shared `_dup_guard(conn, title)` read `_r["title"]` on a caller
connection with NO `sqlite3.Row` factory -> TypeError -> caller's
`except Exception:` swallowed it and SKIPPED the insert. Endpoint looked
successful, no row existed: the guard appeared to work because it
crashed. Fix: positional access (`_r[0]`, `_r[1]`) in any guard shared
across call sites. Verify guards by the DB state change, never by HTTP
status alone.

## Probe battery recipe (curl/urllib, tokened)

Auth: `.env` WRITING_STUDIO_TOKEN, `Authorization: Bearer`. Fire the five
probe classes above against any gated POST endpoint, then purge probe
rows and assert `count(*) == 0` for the probe title pattern. A probe row
left behind is contamination (your own traffic cited as evidence).

## Browser verification recipe (headless)

- Playwright lives in the hermes venv:
  `/<workspace>`.
- Binary discovery: walk `~/Library/Caches/ms-playwright/chromium_headless_shell-*/`
  for `chrome-headless-shell`; pass `executable_path` explicitly (version
  mismatch otherwise).
- App token key is `ws_auth_token` in localStorage; `_getAuthToken()`
  prefers `ws_jwt`. Single-user mode: `_currentUser` stays null and
  attribution falls back — a null user is NOT an auth failure. Do not
  "fix" `/api/auth/me` 404s; legacy local-token path is the live one.
- Tab must be ACTIVATED before measuring: `offsetWidth` of an element in
  a background tab is 0 — that is layout, not absence.
- Blocking proofs: set `window._bcNovelty` state directly, invoke the
  handler, count POSTs via `page.on("request")` — zero requests proves
  client-side blocking; DB row count proves server-side.

## Related

- CI paths-filter blind spot + re-pin procedure: SKILL.md CI discipline.
- Patch-tool corruption modes (fuzzy anchor doubling, hallucinated
  old_string): see tool-output-verification-discipline patterns 19-20.
