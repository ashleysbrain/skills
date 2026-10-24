---
name: local-activity-recovery
description: |
  Reconstruct what the user was recently doing on their Mac when standard
  queries come up empty. Covers browser tabs/history recovery (Chrome,
  Safari), recently viewed files, app state inspection, and the buffering
  gaps that make recent activity invisible to disk-based queries. Use when
  the user asks "what was I just looking at?", "find the article I had
  open", "check my history for X", or any task that needs to recover
  recent local activity that hasn't been committed to disk yet.
version: 1.0.0
platforms: [macos]
metadata:
  hermes:
    tags: [macos, browser, forensics, activity-recovery, chrome, safari]
    category: apple
    related_skills: [macos-computer-use]
---

# Local Activity Recovery

Recover what the user was recently viewing or doing on their Mac when
memory or disk caches haven't caught up. The core problem: applications
buffer state in memory and only flush to disk periodically or on clean
exit. A tab closed 2 minutes ago may not be in the on-disk history DB yet.

## Decision tree: what to try and in what order

**Step 1 — Live state via AppleScript (fastest, always available).**
Query currently open tabs and documents before touching disk:

```bash
# Safari — current tab
osascript -e 'tell application "Safari" to get {URL, name} of current tab of front window'

# Safari — ALL tabs across all windows
osascript -e 'tell application "Safari"
set output to ""
repeat with w in windows
repeat with t in tabs of w
set output to output & (URL of t) & " ||| " & (name of t) & "\n"
end repeat
end repeat
return output
end tell'

# Chrome — all tabs
osascript -e 'tell application "Google Chrome"
set output to ""
repeat with w in windows
repeat with t in tabs of w
set output to output & (URL of t) & " ||| " & (title of t) & "\n"
end repeat
end repeat
return output
end tell'

# Preview — open document
osascript -e 'tell application "Preview" to get name of front document'
```

This catches what is STILL open. It does NOT catch what the user already
closed.

**Step 2 — Disk-based history (catches closed tabs, but may be stale).**
Copy the history DB (Chrome locks the original) and query:

```bash
# Chrome — copy then query (Chrome time = microseconds since 1601-01-01)
cp ~/Library/Application\ Support/Google/Chrome/Default/History /tmp/chrome_hist.db
sqlite3 /tmp/chrome_hist.db \
  "SELECT datetime(last_visit_time/1000000-11644473600,'unixepoch','localtime') as visit, title, url FROM urls ORDER BY last_visit_time DESC LIMIT 30;"

# Safari
cp ~/Library/Safari/History.db /tmp/safari_hist.db
sqlite3 /tmp/safari_hist.db \
  "SELECT datetime(visit_time + 978307200,'unixepoch','localtime') as visit, url FROM history_items hi JOIN history_visits hv ON hi.history_item_id = hv.history_item WHERE lower(url) LIKE '%keyword%' ORDER BY visit_time DESC LIMIT 20;"
```

**CRITICAL PITFALL: Chrome's on-disk History DB is STALE while Chrome is
running.** Chrome holds recent visits in an in-memory buffer and only
flushes to the SQLite file periodically or on clean exit (Cmd+Q). If the
user closed a tab minutes ago but Chrome is still running, that visit
will NOT be in the History file on disk yet. The file's mtime will be
hours old. See `references/chrome-history-buffering.md` for the full
reproduction and recovery paths.

**Step 3 — Chrome DevTools Protocol (if remote debugging is enabled).**
If Chrome was launched with `--remote-debugging-port=9222`, query live
page state including recently closed tabs still in the session:

```bash
curl -s http://127.0.0.1:9222/json/list   # all open pages
curl -s http://127.0.0.1:9222/json/version # protocol version
```

Check if the port is listening first: `lsof -i :9222`. Most users do NOT
have this enabled by default, so this is a fallback, not a primary path.

**Step 4 — Ask the user to fully quit Chrome.**
If Steps 1-3 fail and Chrome is still running, the cleanest recovery is:
ask the user to Cmd+Q Chrome (not just close the window). On clean exit,
Chrome flushes the full in-memory history buffer to disk. Then re-run
Step 2 against a fresh copy.

**Step 5 — Content-based academic search (when the user can describe it).**
When history recovery fails because Chrome is still running and hasn't
flushed, but the user CAN describe what they were reading (topic, methods,
keywords), pivot from disk forensics to academic search. Use the OpenAlex
API (free, no key, structured JSON) to find the paper by content, then
confirm with the user. See `references/openalex-api-reference.md` for the
full query pattern, abstract reconstruction from inverted indexes, and the
iterative narrowing technique. This is often faster than waiting for Chrome
to flush or asking the user to quit Chrome.

**Step 6 — Filesystem signals.**
When browser history is a dead end, check recently modified files:

```bash
find ~/Downloads ~/Desktop ~/your-workspace -mtime -1 -iname "*keyword*"
```

Also check app-specific state: Preview's recent documents
(`defaults read com.apple.Preview NSRecentDocumentRecords`), Finder
recent files, etc.

## Profile awareness

Chrome supports multiple profiles, each with its own History DB:
- `Default/History`
- `Profile 1/History`
- `Profile 2/History`

Query ALL of them. A meditation article might be in Profile 1 while your
work tabs are in Default. Copy each to a temp file and search them all.

## Chrome epoch conversion (reference)

Chrome stores `last_visit_time` as microseconds since 1601-01-01 UTC.
To convert to Unix epoch: `unix_time = chrome_time / 1000000 - 11644473600`.
SQLite: `datetime(last_visit_time/1000000-11644473600, 'unixepoch', 'localtime')`.

Safari stores `visit_time` as seconds since 2001-01-01 (Core Data epoch).
To convert: `unix_time = visit_time + 978307200`.
SQLite: `datetime(visit_time + 978307200, 'unixepoch', 'localtime')`.

## When to stop and ask

If all recovery paths fail because Chrome is running and hasn't flushed:
do NOT keep trying variations on stale data. Tell the user plainly: the
article hasn't been written to disk yet because Chrome is still running,
and offer the Cmd+Q option. Do not fabricate or guess what the article
was.

## Pitfalls

- **Copying a locked DB**: Chrome holds an exclusive lock on its History
  file while running. `cp` still works (SQLite WAL mode allows readers),
  but the copy reflects the last flush, not the current in-memory state.
- **Forgetting profiles**: Always check all Chrome profiles, not just
  Default.
- **Safari History.db permissions**: May need TCC (Full Disk Access)
  permission. If `cp` fails silently, that is the likely cause.
- **Stale `lsof` output**: Checking for a debug port via `lsof -i :9222`
  can be slow or blocked by the approval layer. Use it as a last resort.

## References

- `references/chrome-history-buffering.md` — full reproduction of the
  stale-history-while-running problem, with the exact timestamps showing
  a 2-day gap between on-disk history and actual activity, and the three
  recovery paths ranked by reliability.
- `references/openalex-api-reference.md` — when disk history fails but the
  user can describe the content, pivot to academic paper search via the
  OpenAlex API (free, no key). Covers query syntax, abstract reconstruction
  from inverted indexes, iterative narrowing, and the proven meditation-MEG
  case from 2026-07-06.
