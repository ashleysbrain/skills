# Watcher-organ v2 corrections: compose-first scheduling, phone visibility, pairing (2026-08-19 evening)

Four principal-facing corrections from the evening session, extending
`auto-minting-watcher-organs-2026-08-19.md` (same organ, later hours).
That file remains the base build recipe; THIS file is the correction set.

## 1. Scheduling: COMPOSE FIRST (principal directive — binding)

"Stop creating crons that are unnecessary… this is NOT how we should
immediately default in our OS methodology." Fired when a watcher organ got
its own the operator agent cron entry while an organism tick at the SAME cadence already
existed. Order:
1. **Compose into an EXISTING organism tick** — append the organ call to
   e.g. `organism/research_scan_tick.sh` (already 4x/day via system
   crontab, same silent-on-success contract). DEFAULT.
2. Existing launchd service if a tick is the wrong shape.
3. the operator agent cron mint — last resort, with stated justification.

Technical gotcha when a the operator agent cron IS justified: the job's `script:` field
resolves under `<agent-home>/scripts/` — a script living in the organism is
"Script not found" on first fire. Worse: action='run' returning
`executed: true` does NOT mean it ran — the async delegation later reported
the error. Read `last_status` before claiming the chain works; a
fired-and-errored cron makes "chain verified" claims FALSE.

Final shape: watcher = stage 3 of research_scan_tick.sh (commit b7bf610);
the operator agent cron removed same hour.

## 2. principal-phone visibility (law: invisible = didn't happen)

"I can't see these items from my phone and I don't understand what this
means." Two failures in one message: (a) ledger rows are Mac-only — no
surface reaches Telegram; (b) the chat report used internal jargon (task
IDs, "health axis"). Fixes:
- Every organ minting principal-relevant items MUST feed a Telegram-reaching
  surface; canonical = daily autonomy report (organism/autonomy_report.py,
  08:00). Pattern: section function reads the organ state file, appends
  plain-language bullets, returns "" when nothing new (report stays silent).
- In chat: plain words, no task IDs/axis names. "MIT made tiny devices that
  treat the brain without surgery" not "T-260819-0068 health/organism axis".

## 3. Block-local pairing when scraping structured lists

Never `zip(titles, excerpts)` from two independent findall lists. The Media
Lab news page has 53 title blocks but 52 excerpts — one excerpt-less module
shifted EVERY subsequent pair, silently misattributing evidence (ledger item
1 carried item 2's excerpt; found only when actually re-reading the mint
details). Fix: split the HTML on the module marker (`class='module-title'`)
and extract title + excerpt WITHIN each block; verify pairing on known items
before storing. HTML-unescape everything.

## 4. Literature absorption path (Research Library ingestion for findings)

When principal says "keep this in our literature":
- Research Library = `research-library/research-library.db`, tables
  `sources` (title/authors/venue/year/url/source_type/credibility_weight)
  + `findings` (domain_id/body/action_text/source_id/tags/confidence);
  `created_at` is DEFAULT-filled — do NOT pass added_at (column doesn't
  exist; schema-check before INSERT).
- Fetch and dissect the PRIMARY source (group/lab page in full), never store
  from a news excerpt alone. Check schema first: `.schema sources`.
- Domains are seeded (health-science=5, neuroscience-cognition=9, etc.).
- Findings carry action_text classifying OUR use: watch-track vs near-term
  grounding vs proposal — the classification is the "how can we use this".
- Close the loop in the ledger: the originating watcher tasks get a `done`
  event citing the finding/source ids (audit trail from mint to library).
