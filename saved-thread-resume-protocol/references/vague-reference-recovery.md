# Vague-Reference Recovery (No .md File)

The main protocol covers resuming a saved `.md` thread file. This reference
covers the harder case: the user references a past conversation with NO .md
file — just a vague description ("we were working on a thread yesterday and
you gave me options starting at the number 10"). There is no file to read.
You must reconstruct the conversation from the session DB.

## When to Use

The user says any variant of:
- "we were working on X yesterday"
- "pick back up that conversation about Y"
- "you gave me options and I need to ask about Z"
- References specific content (a number, a phrase, an error) but does NOT
  name a `.md` file

## The Escalation Path (4 Steps)

### Step 1: Discovery queries with keyword combinations

Start with `session_search` in discovery mode. Try multiple query shapes:

```
session_search(query="options numbered list 10 11 12", limit=5, sort="newest")
session_search(query="the specific phrase the user remembers", limit=5)
session_search(query="topic keywords the user mentioned", limit=5)
```

Vary the query — FTS5 requires all terms for AND queries. Use `OR` for
broader recall. Try the user's exact words as a quoted phrase.

### Step 2: Browse recent sessions chronologically

If discovery queries return nothing useful:

```
session_search()  # no args = browse mode, returns recent sessions
```

Look at timestamps. If the user says "yesterday," filter mentally to that
date range. Check `source` (telegram, tui, cron) — the user's main channel
is usually Telegram or TUI.

### Step 3: Scroll through candidate sessions

Once you find a candidate session, read it:

```
session_search(session_id="<id>")  # full read
session_search(session_id="<id>", around_message_id=<id>, window=10)  # scroll
```

If the session has context compaction (a long `[CONTEXT COMPACTION]`
summary), scroll FORWARD from the compaction message to find the actual
exchange the user remembers.

### Step 4: Direct SQLite query (when session_search truncates)

Large sessions produce truncated results from `session_search`. When you
need to see full message content or find a specific exchange that the tool
interface is hiding, query `state.db` directly:

```python
import sqlite3
con = sqlite3.connect(str(get_hermes_home()) + '/state.db')
cur = con.cursor()

# List all messages in a session with lengths (find the big ones)
sid = '<session_id>'
cur.execute(
    'SELECT id, role, length(content) FROM messages WHERE session_id=? ORDER BY id',
    (sid,)
)
for r in cur.fetchall():
    print(f'id={r[0]} role={r[1]} len={r[2]}')

# Read specific message content
cur.execute('SELECT id, role, content FROM messages WHERE id=?', (<msg_id>,))
print(cur.fetchone())

# Read tool_calls to see what files were read/written
cur.execute('SELECT id, tool_calls FROM messages WHERE id=?', (<msg_id>,))
```

**Key facts about the DB:**
- Database path: `<agent-home>/state.db` (or `get_hermes_home() / 'state.db'`)
- Table: `messages` (columns: `id`, `session_id`, `role`, `content`,
  `tool_calls`, `timestamp`)
- Table: `sessions` (session metadata)
- FTS5 tables: `messages_fts`, `messages_fts_trigram` (used by
  `session_search` internally)
- Run from terminal, not `execute_code` (cron mode blocks arbitrary Python)

## Real Example (2026-06-29)

User said: "we were working on a thread yesterday and you gave me options
starting at the number 10 and I needed to ask you what was 1-9."

Recovery path:
1. Discovery queries: "options starting at number 10" → hit a cron session
   (wrong one). "numbered list 10 11 12 choices" → no results.
2. Browse recent: found session `20260628_214950_33101d` ("Status check on
   project artifacts #2") from the right date.
3. Read the session: hit a context compaction wall. Scrolled forward.
4. Found the answer in message id=221777: nine new publication topics
   numbered 9-17 were presented, but the prior topics 1-8 existed in a
   different file. The user never saw 1-8, hence the confusion.

Root cause was a fragmented list across two files — see the "Fragmented
List Reconciliation Pitfall" in `ds-organism-architecture-workflow`.

## Anti-Patterns

- **DO NOT** ask the user to clarify what they were working on before
  searching. Try recovery first — the session DB usually has the answer.
- **DO NOT** give up after one failed `session_search` query. Try 3-4
  different query shapes, then browse, then scroll, then direct DB query.
- **DO NOT** assume `session_search` shows you everything. It truncates
  large sessions and large messages. The direct SQLite query is the
  reliable fallback.
