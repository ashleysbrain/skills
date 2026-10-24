# Bus posts from subagent briefs + Sherman gate expiry (2026-08-21)

Two traps hit during the a teammate design-lane spin-up, both in the
orchestration layer around children.

## 1. Children cannot see this skill and guess the bus schema

Census briefs commonly end with "post a completion summary to the operator
bus (sqlite insert into message-bus.db)". Children do NOT have this
skill loaded; they invent the schema from the phrase. Observed guesses:
column `body` (does not exist), `created_at` (is `timestamp`),
`msg_type` values outside the CLI-enforced set (`build` is NOT a valid
type — the CLI accepts handoff/result/status/alert/ping/pong/
design_request/design_spec/build_request only).

The child hit "table messages has no column named body" and died before
posting; the orchestrator had to post (msg 2893).

Fix in the BRIEF, not the child: embed the exact working command:

```bash
cd /<workspace> && python3 organism/operator_bus.py post \
  --from hermes --to sibling-agent --type result \
  --subject "CENSUS: ..." --content "<counts + artifact paths>"
```

If raw SQL is genuinely required, give the column list verbatim:
(timestamp, from_op, to_op, msg_type, subject, content, status) and note
`msg_type` must be one of the CLI choices even in SQL (pollers filter on
the known set).

## 2. Sherman gate expiry blocks MONITORING calls too

The specialist gate unlocks for 5 minutes after a route. `delegate_task
action=list` (a read-only liveness check) is gated the same as a spawn.
Mid-campaign, after >5 min of child runtime, a status check fails with
"SPECIALIST GATE BLOCKED: delegate_task. Sherman routing expired".

Fix: re-route cheaply before any delegation-family call that follows a
quiet period:

```bash
python3 <agent-home>/agent-hooks/specialist_gate.py --route \
  --situation "monitor live delegation (liveness check, not new work)" \
  --specialist "DS <current specialist>"
```

Reusing the CURRENT specialist keeps the routing ledger coherent; do not
mint a new route for a monitoring call. Alternative signal that avoids
the gate entirely: transcript mtime + wc of the live log at
<agent-home>/cache/delegation/live/<deleg_id>/task-0.log (per pitfall 1 of
this skill's SKILL.md: transcript growth, not status field).
