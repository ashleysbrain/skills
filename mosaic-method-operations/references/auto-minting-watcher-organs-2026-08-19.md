# Auto-minting watcher organs: build + calibration discipline (2026-08-19)

Born from the Media Lab watcher organ (T-260819-0055/0056,
`organism/medialab_watcher.py`, commit 52eac6b) after two scorer iterations
minted 27 junk tasks into the PRODUCTION ledger. Applies to any organ that
auto-creates ledger tasks from external sources (watchers, hunters, monitors).

## Build shape (mirror gap_hunter.py)

scan -> dedupe (append-only state file, title/pushed_at keys) -> score
against OUR capability axes -> mint severity-gated ledger tasks -> silent on
success, failure-only logging. State capped (2000 keys, 500 mints) to avoid
monotonic growth. Cron tick script wraps the python; one line, silent.

## Census BEFORE design (no guessing)

Verify each source live before wiring it:
- media.mit.edu/news/ — scrapeable (52 titles + excerpts in markup); RSS does
  NOT exist (4 URL patterns 404 — verified, don't assume a feed).
- GitHub org API — `api.github.com/orgs/mitmedialab` (580 repos); the obvious
  guess `mit-media-lab` 404s. Probe org names before coding.
- JS-heavy SPA (neuro2.ai): skeleton SvelteKit HTML carries no data; data
  endpoints SPA-fallback to index.html (200 + 2488 bytes = the tell). Read
  the RENDERED DOM from a live tab instead. On 3D-force-graph pages the main
  thread is hammered: async Runtime.evaluate times out — short SYNCHRONOUS
  expressions (`document.body.innerText.slice(0,900)`) succeed.
- Login-walled export (⤓ button) = honest limit, disclosed, never guessed past.

## DRY-RUN-FIRST calibration (the hard-won law)

Anything that mints into the production ledger ships with a `--dry-run` flag
FROM BIRTH. Calibrate the scorer offline until the digest is clean, then and
only then production-run. Two junk iterations (v1 substring, v2 single-hit
exception) each minted real tasks that then had to be cleaned up.

Scorer rules that survived calibration:
- Word-boundary regex per keyword (`\b` + re.escape) — substring matching
  produced `restore`->'store health' and 'guitar launch'->'health' junk.
- Require 2+ DISTINCT keyword hits per axis; no exceptions for "important"
  axes — the exception re-admitted the junk.
- HTML-unescape scraped titles (`&#x27;` ships to the ledger otherwise).
- Watch the digest itself: junk matches visible in your own output are a
  defect to fix BEFORE the principal reads the digest.

## Lawful cleanup when calibration mints anyway

Events are append-only (Flow 3); tasks are NEVER deleted:
1. `UPDATE tasks SET state='cancelled' WHERE ...`
2. Append a `cancelled` event naming the reason (superseded-by version).
3. Count-verify to 0 — and cancel by `origin=` predicate, NOT id LIKE ranges
   (a range pattern missed 7 of 11; `origin='watch:medialab' AND state='open'`
   caught all).

## Ledger ID convention (collision-safe minting from organs)

IDs are `T-YYMMDD-NNNN` — note YY not YYYY (first watcher version minted
`T-20260819-XXXX`, off-convention). Probe the next free id with
`SELECT id FROM tasks WHERE id LIKE 'T-<stamp>-%' ORDER BY id DESC LIMIT 1`
before INSERT; on UNIQUE failure NEVER attach events to the colliding task
(events are undeletable — contamination is permanent).

## Scheduling fallback pattern

If system `crontab` install wedges (stdin mode `crontab -` and file mode both
hung on this host, verified with clean-process diagnostics), do not fight it:
register the tick in the the operator agent cron fleet instead —
`cronjob(action='create', no_agent=True, script='<tick>.sh', schedule=...)`,
script-only, silent-on-clean, `deliver='origin'`. Fire it once via
action='run' to verify the whole chain (cron -> script -> organ -> ledger)
before declaring it live.

## Sibling-repo commit note

Workspace `organism/` is a symlink to `~/your-org/organism` (own git
repo). `git add` from the workspace fails with "beyond a symbolic link" —
commit in the canonical repo, not through the bridge symlink.
