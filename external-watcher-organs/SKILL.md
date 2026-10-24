---
name: external-watcher-organs
description: "Use when wiring an external source into an organism watcher."
version: 1.0.0
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [monitoring, organism, research-intake, cron-discipline]
---

# External Watcher Organs

Build recurring intelligence intakes that fold external sources into an
organism's ledger and library — not one-off scrapes. A watcher organ is a
scan → dedupe → score → mint → absorb loop with a silent-on-success contract.

## When to Use

- "Stay up to date on X institution/lab/source and incorporate it."
- "Link this tool/dataset/graph into our systems."
- Any external surface that should generate typed tasks or library entries on a schedule.

## Procedure

### 1. Census the surface LIVE (no guessing)

Fetch and read the real page/API before proposing anything. Verify with
probes, not assumptions:
- News pages: check RSS actually exists (`/feed/`, `/rss/` often 404) before assuming feeds.
- GitHub: probe org names via API until the right one returns (e.g. `mitmedialab`, not `mit-media-lab`).
- SPA sites: data lives in JS chunks or runtime state — read rendered DOM via browser or hunt the payload; SPA fallback returns index.html (~2.5KB) for every unknown path.
- Login-walled exports: record as honest limit; never guess past a wall.

### 2. Build the organ (script shape)

Single Python file, mirroring the organism's existing tick shape:
- `_load_state()` / `_save_state()` — append-only JSON state (seen keys, mints), capped (trim oldest beyond 2000 entries).
- Source scanners return `[{title, excerpt, url, ...}]`.
- Scoring: **word-boundary regex** per capability axis (compile `\b<kw>`), require **2+ distinct keyword hits** — substring matching produces junk ("restore"→"store", "guitar launch"→health).
- Mint only capability-relevant items into the task ledger; everything else is deduped silently.

### 3. Calibrate DRY-RUN-FIRST (binding)

Never calibrate a scorer against the production ledger:
- Ship `--dry-run` mode from day one; run until the digest is clean.
- Junk/erroneous mints are cancelled (append-only events stay), never deleted.
- Ledger ID conventions differ per system — read existing rows and derive the stamp format before minting (e.g. `T-YYMMDD-NNNN`, not `T-YYYYMMDD-NNNN`).

### 4. Schedule by COMPOSING, never by minting crons

- Append the watcher call to an EXISTING organ tick script that already runs on the right cadence.
- Minting a new cron entry (the operator agent cronjob or crontab) is a last resort requiring justification. principal correction 2026-08-19: "Stop creating crons that are unnecessary — this is NOT how we should immediately default."
- the operator agent cron `script:` fields resolve under `<agent-home>/scripts/` — an organism-path script will not fire there.
- System `crontab` install (`crontab -` / `crontab file`) can hang on macOS; if it does, verify with `crontab -l` diagnostics and fall back to composition.

### 5. Make results phone-visible

Items stored only in a Mac-side DB are invisible to the principal = didn't happen:
- Extend the daily report that already reaches the user's messaging surface with a watcher section (last-24h mints, plain bullet list).
- Explain findings in plain language when reporting; no internal jargon or task IDs in user-facing summaries.

### 6. Absorb decision-grade items into the library

For items worth keeping:
- Ingest `sources` + `findings` rows; anchor to PRIMARY sources (fetch the group/paper pages, not just news excerpts), verify primary papers on arXiv before citing.
- Journalism vs primary tiers get different credibility weights (0.8 vs 1.0).
- Record expansion uses (near-term vs watch-track) in `action_text`; mint follow-on tasks for decision-grade questions.

## Pitfalls

- Zip-misalignment parsing: pairing two independent regex lists (titles[], excerpts[]) misattributes evidence when counts differ (53 vs 52). Parse BLOCK-LOCALLY — split on the module boundary and extract title+excerpt from the same block.
- HTML entities in scraped titles (`&#x27;`) — unescape before storage/dedup.
- Claiming "chain verified" from a script path that never ran — run the actual scheduler path once and read its logs before reporting.
- Watcher state file holding `DRY` placeholder mints — reset mints list before first production run; keep seen-maps (real dedupe data).

## Verification

- [ ] Census claims cite live probes (byte counts, API responses), not memory.
- [ ] `--dry-run` digest clean before any production mint.
- [ ] Production mint appears in ledger with correct ID convention; verify by SQL read-back.
- [ ] Scheduled path executed once for real; log file shows the tick ran.
- [ ] User-facing report includes new items in plain language; no mints invisible to the principal.
