# Chrome History Buffering — The Stale DB Problem

## The problem (observed 2026-07-06)

User closed a meditation article in Chrome minutes ago and asked what it
was. Chrome was still running (PID 474). Standard recovery path:

1. Copied `~/Library/Application Support/Google/Chrome/Default/History` to `/tmp/`
2. Queried with SQLite for meditation/mindfulness keywords
3. Zero results

**Root cause**: Chrome's on-disk `History` SQLite file had an mtime of
`2026-07-04 07:44` — two days stale. All browsing since then (including
the meditation article) was held in Chrome's in-memory buffer and had
never been flushed to disk because Chrome never cleanly exited.

## Evidence from the session

```
$ ls -la ~/Library/Application\ Support/Google/Chrome/Default/History
-rw-------@ 1 aw  staff  8159232 Jul  4 07:44  ← mtime is 2 days old

$ sqlite3 /tmp/chrome_hist.db "SELECT max(last_visit_time) FROM urls;"
→ returns timestamps from July 4, not July 6
```

Meanwhile `osascript` showed Chrome still running with active tabs, and
Profile 1's history (also copied while Chrome was running) showed Netflix
activity from July 6 — so flushing is per-profile and irregular.

## Recovery paths, ranked by reliability

### Path 1 — AppleScript live tab query (best for currently-open tabs)
```bash
osascript -e 'tell application "Google Chrome"
set output to ""
repeat with w in windows
repeat with t in tabs of w
set output to output & (URL of t) & " ||| " & (title of t) & "\n"
end repeat
end repeat
return output
end tell'
```
**Limitation**: only catches tabs still open. Already-closed tabs are
gone from this source.

### Path 2 — Ask user to Cmd+Q Chrome, then re-query (best for closed tabs)
On clean exit, Chrome flushes the full in-memory history to the SQLite
file. After Cmd+Q, re-copy and re-query:
```bash
cp ~/Library/Application\ Support/Google/Chrome/Default/History /tmp/chrome_fresh.db
sqlite3 /tmp/chrome_fresh.db "SELECT ... FROM urls ORDER BY last_visit_time DESC LIMIT 30;"
```
This is the most reliable path for recovering recently-closed tabs when
Chrome is still running.

### Path 3 — Chrome DevTools Protocol (if enabled)
```bash
curl -s http://127.0.0.1:9222/json/list | python3 -m json.tool
```
Only works if Chrome was launched with `--remote-debugging-port=9222`.
Check with `lsof -i :9222 | grep LISTEN`. In this session, the curl to
:9222 was blocked by the approval layer (timed out without user
consent), so this path was not viable.

### Path 4 — Fresh copy while running (catches partial state)
Sometimes a profile's History file IS more recent than others. In this
session, Profile 1's copy showed same-day Netflix activity even while
Chrome was running, because that profile had been flushed more recently.
Always copy and query ALL profiles, not just Default.

## What NOT to do

- Do not loop on variations of the stale query hoping for different
  results. The data is not on disk; repeating the query wastes time.
- Do not fabricate the content of the closed article. Tell the user
  plainly that Chrome hasn't flushed and offer the Cmd+Q path.
- Do not run `strings` on the raw History file hoping to find recent
  URLs — the buffer is in Chrome's process memory, not in the file.

## Chrome epoch math

Chrome `last_visit_time` = microseconds since 1601-01-01 UTC.
```
unix_epoch = chrome_time / 1000000 - 11644473600
```
SQLite one-liner:
```sql
datetime(last_visit_time/1000000 - 11644473600, 'unixepoch', 'localtime')
```
To filter for "today only", compute the Chrome-time threshold in Python:
```python
import datetime
chrome_epoch = datetime.datetime(1601, 1, 1)
target = datetime.datetime(2026, 7, 6, 0, 0, 0)  # local midnight
delta = target - chrome_epoch
chrome_threshold = int(delta.total_seconds() * 1000000)
# → use: WHERE last_visit_time > <chrome_threshold>
```

## Safari comparison

Safari's `History.db` (at `~/Library/Safari/History.db`) uses Core Data
epoch (seconds since 2001-01-01):
```sql
datetime(visit_time + 978307200, 'unixepoch', 'localtime')
```
Safari flushes more predictably than Chrome but may still lag by minutes.
