# Session History Store — where cross-thread counts actually live (2026-09-05)

Discovered while recounting principal asks across sessions. Verified live, not assumed.

## Authoritative store

`<agent-home>/state.db`, table `messages` — columns `session_id, role, content,
tool_calls, timestamp, ...` with FTS index `messages_fts` (trigram variant
`messages_fts_trigram`). ALL sessions (CLI, TUI, gateway, telegram) land here.
`hermes sessions list` reads the `sessions` table of the same DB.

## Dead ends (do not re-probe — each verified empty/legacy this session)

- `<agent-home>/sessions/*.jsonl` — legacy per-session exports, newest is 2026-05-29.
  Grepping these for current-era user messages returns zero hits.
- `<agent-home>/sessions/sessions.db`, `sessions.json` — sessions.json is a LEGACY
  MIRROR of the gateway routing index (per its own `_README`); points to state.db.
- `<agent-home>/hermes_sessions.db`, `<agent-home>/messages.db`, `sessions/sessions.db` —
  zero tables / 0 bytes.
- Broad `find`/`grep -r` across `<agent-home>` or `~/Library` times out (90-300s) —
  query the DB instead.

## Working query pattern

```python
import sqlite3
db = sqlite3.connect('file:/<workspace>?mode=ro', uri=True)
rows = db.execute("""SELECT DISTINCT session_id, timestamp, substr(content,1,700)
    FROM messages WHERE role='user'
    AND content LIKE '%<keyword>%'
    AND timestamp BETWEEN <epoch_lo> AND <epoch_hi>
    ORDER BY timestamp""").fetchall()
```

Notes:
- `messages_fts MATCH` works but floods with cron-skill prompts; LIKE + window is
  quieter. Filter out `CONTEXT COMPACTION` and `[ASYNC DELEGATION` wrappers.
- Timestamps are epoch floats. Same user message delivered to multiple sessions
  shares one timestamp — dedupe on content, not rows.
- session_search (tool) searches the same store but returns wrapped compaction
  blocks; direct SQL is better for counting.

## Worked example

"How many times has the principal asked about bus numbering?" → 8 distinct asks over 19
days, 4+ threads (Aug 17 ×2, Aug 18 voice msg delivered to 6 sessions = 1 intent,
Aug 31 ×2 sessions, Sept 1, Sept 3, Sept 5 ×2). Parroted "four" was the defect
that motivated this reference.
