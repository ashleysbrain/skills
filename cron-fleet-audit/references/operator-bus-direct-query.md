# Operator Bus Direct DB Query Workaround

## Problem

`operator_bus.py read` truncates message content at ~200 chars. When you need the full content of a bus message (e.g., a design_request with detailed requirements), the CLI output cuts off mid-sentence.

## Solution: Query the SQLite DB directly

The bus database is at `/<workspace>` (NOT `organism/bus.db` which is empty). Schema:

```
Tables: messages, sqlite_sequence, operator_health
```

To read full message content:

```bash
python3 -c "
import sqlite3
db = sqlite3.connect('/<workspace>')
for mid in [18, 21, 22]:
    row = db.execute('SELECT id, from_op, to_op, msg_type, subject, content, status FROM messages WHERE id=?', (mid,)).fetchone()
    if row:
        print(f'=== MSG {row[0]} | {row[1]}->{row[2]} | {row[3]} | status={row[6]} ===')
        print(f'SUBJECT: {row[4]}')
        print(f'CONTENT: {row[5]}')
        print()
"
```

## Key paths

| Item | Path |
|------|------|
| Bus DB | `/<workspace>` |
| Bus script | `/<workspace>` |
| Empty DB (NOT this) | `/<workspace>` |

## Bus CLI commands (reference)

```bash
# Status overview
python3 /<workspace> status

# Health check
python3 /<workspace> health

# Read messages (NOTE: truncates content!)
python3 /<workspace> read --to hermes --status pending

# Claim a message
python3 /<workspace> claim --by hermes <msg_id>

# Post a message
python3 /<workspace> post --from hermes --to sibling-agent --type design_spec --subject "..." --content "..."

# Complete a message
python3 /<workspace> complete <msg_id> --result "..."
```

## Message types

| Type | Purpose | Response Type |
|------|---------|---------------|
| `handoff` | Work transfer between operators | `handoff` (R2 response) |
| `result` | Result delivery | (acknowledge + complete) |
| `alert` | System alert | `handoff` (acknowledgment) |
| `status` | Progress update | (acknowledge + complete) |
| `design_request` | Request body analog / design spec | `design_spec` |
| `design_spec` | Return body analog design | (complete) |

## R2 Response Pattern (the operator agent as peripheral/autonomic)

1. `status` -> read bus -> claim pending/claimed messages -> read full content via DB query
2. Process each message: handoffs get R2, alerts get acknowledgment, status gets noted
3. Post responses via `operator_bus.py post`
4. Complete originals via `operator_bus.py complete`
5. Ping heartbeat to maintain alive status
