# Operator Bus — Neural Signaling Infrastructure

## Overview

The **Operator Bus** is a SQLite-based message queue at `/<workspace>` that serves as the organism's neural signaling layer. It enables real-time handoffs between all operators: **hermes** (peripheral/autonomic), **sibling-agent** (central/cortical), **sibling-agent** (fleet management), and **openresearch** (intelligence gathering).

This is NOT documentation or aspiration — it's the actual synergy infrastructure. Real messages, real handoffs, real coordination.

## Architecture

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────┐
│   hermes    │────▶│  message-bus.db │◀───▶│  sibling-agent   │
│ (peripheral)│     │  (SQLite WAL)    │     │ (cortical)  │
└─────────────┘     └──────────────────┘     └─────────────┘
                           ▲
                           │
                    ┌─────────────┐
                    │  sibling-agent   │
                    │ (fleet mgmt)│
                    └─────────────┘
                           ▲
                           │
                    ┌─────────────┐
                    │ openresearch│
                    │ (intel)     │
                    └─────────────┘
```

**DB Schema:**
- `messages` — id, timestamp, from_op, to_op, msg_type, subject, content, status (pending/claimed/done), claimed_by, claimed_at, done_at, result
- `operator_health` — operator, last_seen, status (alive/down)

**Message Types:** `handoff`, `result`, `status`, `alert`, `ping`, `pong`, `design_request`, `design_spec`, `build_request`

## CLI Interface (`organism/operator_bus.py`)

```bash
# Post a message
python3 organism/operator_bus.py post --from hermes --to sibling-agent --type handoff \
  --subject "R2: Design request" --content "Body analog needed for..."

# Read pending messages for an operator
python3 organism/operator_bus.py read --to sibling-agent --status pending

# Read ALL pending messages
python3 organism/operator_bus.py read --to all --status pending

# Show bus status (pending counts, operator health, recent activity)
python3 organism/operator_bus.py status

# Claim a message (atomically mark in-progress)
python3 organism/operator_bus.py claim 42 --by sibling-agent

# Complete a claimed message
python3 organism/operator_bus.py complete 42 --result "Built and verified"

# Block until message arrives (for autonomous polling)
python3 organism/operator_bus.py wait --to sibling-agent --timeout 60

# Ping an operator
python3 organism/operator_bus.py ping --to sibling-agent --by hermes

# Record heartbeat
python3 organism/operator_bus.py heartbeat --operator hermes

# Check operator health (last seen vs timeout)
python3 organism/operator_bus.py health
```

## Opencode's Autonomic Bus Reader (`organism/opencode_bus_read.py`)

Opencode surfaces its pending messages automatically at session start and before each action — mirroring hermes's 2-min autonomic bridge.

```bash
# Surface pending messages for sibling-agent
python3 organism/opencode_bus_read.py

# Machine-readable JSON
python3 organism/opencode_bus_read.py --json

# Only messages with id >= N
python3 organism/opencode_bus_read.py --since 100
```

**Action-needed types** (require R2/synthesis): `design_request`, `handoff`, `alert`
**Informational types** (auto-ack eligible): `result`, `status`, `ping`, `pong`

## Diagnostic Pattern — Bus Health Check

Run this sequence to diagnose multi-operator coordination issues:

```bash
# 1. Overall bus status
python3 organism/operator_bus.py status

# 2. Check pending per operator
python3 organism/operator_bus.py read --to hermes --status pending
python3 organism/operator_bus.py read --to sibling-agent --status pending
python3 organism/operator_bus.py read --to sibling-agent --status pending
python3 organism/operator_bus.py read --to all --status pending

# 3. Check operator heartbeats (health)
python3 organism/operator_bus.py health

# 4. Check for stuck/duplicate messages
python3 organism/operator_bus.py read --to sibling-agent --status pending | grep -c "VERITAS-003"
```

## Key Findings from This Session (2026-06-25)

### 1. Opencode Not Picking Up Messages
- **181 pending for sibling-agent** — all from hermes, mostly VERITAS-003 duplicates
- **Last sibling-agent heartbeat:** 2026-06-23T16:20:01Z (over 24h ago)
- **0 pending for hermes** — sibling-agent has sent 200+ completed messages to hermes (all in `done`)

### 2. VERITAS-003 Duplicate Spam (Msg 315-426)
- 112 duplicate `handoff` messages from hermes→sibling-agent with identical subject
- Caused by a runaway loop in hermes's cron/automation
- **Remediation:** Claim + complete all duplicates in batch:
  ```bash
  for id in {315..426}; do
    python3 organism/operator_bus.py claim $id --by hermes
    python3 organism/operator_bus.py complete $id --result "Duplicate cleared - VERITAS-003 registered"
  done
  ```

### 3. Message Flow Asymmetry
- **hermes → sibling-agent:** Working (messages post successfully)
- **sibling-agent → hermes:** Working (200+ done messages)
- **sibling-agent → sibling-agent:** Working (internal thread coordination)
- **sibling-agent reading bus:** NOT working (no recent heartbeats, pending piling up)

## Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Using stale `organism/operator_bus.db` (0 rows) | Bus appears empty | Use workspace ROOT DB: `/<workspace>` |
| Opencode not running autonomic reader | Pending messages accumulate indefinitely | Ensure `opencode_bus_read.py` runs at session start + before actions |
| Duplicate message loops | Hundreds of identical pending messages | Add idempotency keys; claim+complete duplicates in batch |
| No operator heartbeat | Health check shows "down" | Each operator must call `heartbeat()` periodically (cron or on action) |
| Messages stuck in `claimed` | Forgotten `complete()` | Add timeout-based auto-complete or manual audit |

## Integration with the operator agent Architecture

| Layer | Operator Bus Role |
|-------|-------------------|
| **Kanban as Endocrine** | Kanban tasks = hormones; Operator Bus = fast neurotransmission (event-driven, not circadian) |
| **Cron Rhythms** | Cron = circadian/ultradian clocks; Bus = millisecond neural spikes between cycles |
| **Memory Isolation** | Bus crosses profile boundaries — the only sanctioned cross-profile communication channel |
| **Proprioception** | Bus health = nervous system integrity check; operator heartbeats = vital signs |
| **Two-Silo Architecture** | Engine Fleet (Silo 1) ↔ Patient 0 (Silo 2) coordination via bus |

## Related Files

- `organism/operator_bus.py` — Main bus CLI and library
- `organism/opencode_bus_read.py` — Opencode's autonomic reader (PROC-003)
- `organism/message-bus.db` — SQLite database (workspace root)
- `organism/sibling-agent-heartbeat.py` — Openclaw heartbeat emitter
- `references/kanban-as-endocrine-signaling.md` — Kanban as slower hormonal signaling
- `references/proprioception-fix-session-2026-06-17.md` — Body self-awareness pattern (applies to bus health too)

## Verification Checklist

- [ ] `operator_bus.py status` shows reasonable pending counts (<50 per operator)
- [ ] All operators have recent heartbeats (<5 min for active, <1h for cron-driven)
- [ ] No duplicate message storms (same subject >5x pending)
- [ ] `opencode_bus_read.py --json` returns actionable messages for sibling-agent
- [ ] Cross-operator handoffs complete (hermes→sibling-agent→hermes roundtrip <2 min)
- [ ] Bus health check runs in SENTINEL compliance sweep