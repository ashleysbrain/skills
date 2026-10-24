# Write-path census: PASS-4 → PASS-5 falsification chain (2026-08-19)

Research Studio (pipeline_api :port + writing-studio.html build queue). Three
consecutive adversarial rotations (Popper → Luria → Tanenbaum → Popper) each
falsified the previous pass's "done". Session record for the rules now in SKILL.md.

## Defect chain (each found by live probe, not code-read)

| Pass | Defect | Probe | Fix |
|------|--------|-------|-----|
| P4 | Stored XSS via `/api/research/build` `kind` field → title → Build-view `innerHTML` (raw) | `kind:"<img src=x onerror=alert(1)>"` → 200 stored raw, echoed by GET | `_sanitize_text` at BOTH INSERT paths (title/desc/tags-kind); renderer `_esc()` on title/status/desc/assignee |
| P4 | NFD confusable dup evasion (NFC "café" vs NFD e+U+0301 both → 200) | two POSTs differing only in normalization | shared `_norm_title_key()`: `" ".join(unicodedata.normalize("NFC", s).casefold().split())` on BOTH guards |
| P4 | Novelty gate bypass: `kind:"course"` on `/api/research/build` created course items with zero verdict | POST kind=course no token → 200 | gate cloned to the second endpoint, keyed on kind, server-issued verdict required (422 without) |
| P5 | **UPDATE-path XSS re-open**: PASS-4 sanitized INSERTs only; `PUT /api/build-queue/{id}` wrote title/desc/assignee/notes raw | PUT raw XSS title → 200 stored raw | `_sanitize_text` on the four text fields in the update loop |
| P5 | Probe-hygiene leak: PASS-4's regression re-run recreated 2 rows after the "0 leftovers" claim | count query found 2 | purge + count query after EVERY run |

## Battery shape that caught these (reusable)

`/tmp` python probe script against the live server, token from `<agent-home>/.env`:
1. Auth: no-token POST to every write endpoint → expect 401 each
2. XSS storage: payload in every free-text client field (incl. `kind`) → create, then inspect DB row AND full GET body (don't truncate the read at 300 chars — a truncation bug once masked a True)
3. Dup evasion: NFC then NFD variant of same title → second must 409
4. Gate bypass: replay the gated item KIND on every OTHER endpoint that can create it → expect same rejection
5. UPDATE re-open: PUT the payload onto an existing row → stored must be escaped
6. Render: headless chromium (node playwright-core + chrome-headless-shell), verify painted geometry (offsetWidth>0), payload row renders as TEXT (no `img` element, no fire flag), pageerror list empty

## Auto-restore guardian rule

The workspace runs `ws-guardian.sh` (300s cadence) restoring
`writing-studio/writing-studio-backups/ws-good-*.html` (newest) on JS failure.
After any verified edit to the served HTML: (a) grep the NEWEST backup for the
fix marker — refresh it if stale, (b) delete same-pattern corpses elsewhere
(a root-level `ws-good-1110.html` without the fix was a restore-confusion hazard).

## Server-side gate pattern (survived all passes)

Verdicts issued server-side in a dict keyed by `sha256(claim_text)`; the queue
endpoint re-derives the key from the request's claim text and matches verdict +
scanned_at (±2s) + 1h two-sided freshness window. Client-asserted tokens are
never trusted. Known carried gap: dict is process-local (restart forgets
verdicts → user re-scans); acceptable single-user, persist to SQLite next.

## the OS ledger discipline for QA passes

Typed task in `stores/task-ledger.db` (NOT `ledger/state.db` dispatch table —
PASS-4 initially logged to the wrong one): mint → claim → done events with
run-record citations, then `python3 gates/rubric_judge.py --score <id>`
(expect ≥0.9). `task_events.actor_kind` is NOT NULL ('ai'|'human'); naive SQL
INSERTs fail loudly. Ledger DB is gitignored runtime state — don't force-add.
