# principal Respond Limb — conductor :port (2026-08-26)

Session: principal correction — ruling cards offered only Approve/Reject/Defer with
no way to send context back to the engine that asked ("ability to add a
comment to add context for training the os on the user needs"). Built
`/api/respond` + `respondTo()` modal, wired into 4 surfaces.

## The capability (reusable pattern: human efferent limb beyond ruling)

A ruling closes work; a response teaches. Every surface where a question
reaches the human needs BOTH. The four mounts: ruling cards, task drill,
context drawer, bus drill (Respond-to-sender routes on `from_op`).

## Endpoint shape (`/api/respond` in conduction_daemon.py)

One motion, four durable writes, degrade-don't-block:

1. **message-bus** `INSERT INTO messages` — `from_op='ceo'`,
   `to_op=<asking engine or fallback>`, `msg_type='ceo-response'`, status
   pending. Bus-down → `bus_id: null` in response, never an exception.
2. **ledger** `task_events` append — event `ceo-response`, actor
   `ceo/human`, detail = text[:500]. Only when task_id matches
   `T-\d{8}-.+` AND the row exists. Returns `ledger_event: true/false`.
3. **guidance-inbox.jsonl** — the steer/teaching pipe (append jsonl rec).
4. **glia/memory-pins.jsonl** — ONLY when user picks "Send + pin" (opt-in,
   not default).

Response JSON surfaces every leg's truth (`bus_id`, `ledger_event`,
`memory_pin`) so the UI confirm line can say exactly what landed:
`Sent. The engine has your reply (bus #4335) · pinned to memory.`

## Modal (ADHD buttons-law)

Preset chips (`more detail`, `wrong priority`, `do it differently`,
`not now`, `this worked — keep doing it`) + free textarea + three buttons:
Send / Send + pin to memory / Cancel. Chips APPEND to the textarea, never
replace. Built with data-attrs + addEventListener (no nested onclick
quotes — see SKILL.md authoring rule).

## Verification battery (all legs, read-back not 200)

- Modal opens via REAL coordinate click (locator.click failed on re-render
  poller; fresh-geometry mouse.click in same tick worked).
- Chip click fills textarea (`"more detail"`).
- Send+pin → confirm text carries bus id + pin flag.
- Read back all four stores: `sqlite3 message-bus.db "SELECT ... WHERE
  id=<bus_id>"`, `tail -1 guidance-inbox.jsonl`, `tail -1 memory-pins.jsonl`,
  `SELECT event FROM task_events WHERE event='ceo-response'`.
- Zero page errors asserted at end.

## Battery traps hit (all now in SKILL.md pitfalls)

uppercase CSS transform vs exact-match probe; 1280 viewport clipping the
right drawer; closeDrawer() killing the modal inside it; pkill missing the
venv-python pid so served bytes stayed stale.
