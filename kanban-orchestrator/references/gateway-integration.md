# Kanban + Gateway (Telegram/Discord/Slack) Integration

## The Problem

Kanban is **not automatically triggered by incoming gateway messages**. The gateway's normal message flow is:

```
Telegram message → TelegramAdapter.handle_message() → GatewayRunner._handle_message() → Agent conversation
```

Kanban tasks are only created when:
1. A human uses `/kanban create` slash command
2. An orchestrator profile receives a message and explicitly calls `kanban_create`
3. A cron job or webhook creates a task

## Solution: Orchestrator Profile Pattern

Create a dedicated **orchestrator profile** that receives gateway messages and routes them to Kanban.

### Step 1: Create Orchestrator Profile

```bash
hermes profile create orchestrator --clone
hermes -p orchestrator skills install kanban-orchestrator
```

### Step 2: Configure Gateway to Route to Orchestrator

In `<agent-home>/config.yaml`:

```yaml
gateway:
  platforms:
    telegram:
      default_profile: "orchestrator"  # All Telegram messages go to orchestrator
    discord:
      default_profile: "orchestrator"
    slack:
      default_profile: "orchestrator"
```

### Step 3: Ensure Specialist Profiles Exist (Body System Architecture)

**For Divinity Science body-system architecture**, use the profile mapping from `hermes-agent-architecture` skill:

| Body System | the operator agent Profile | Kanban Assignee | Skills |
|---|---|---|---|
| Brain/CNS (Coaching) | `cns` | `cns` | `kanban-orchestrator`, `ds-wave-coaching` |
| Autonomic NS (Regulation) | `autonomic` | `autonomic` | `kanban-worker`, `quartz-lattice` |
| Endocrine/Immune (Health) | `endocrine-immune` | `endocrine-immune` | `aisha-md-health-orchestration`, `sentinel-compliance-sweep` |
| Circulatory/Skeletal (Fleet) | `circulatory-skeletal` | `circulatory-skeletal` | `hermes-agent`, `sibling-agent-fleet-analytics` |
| Integration (Orchestrator) | `orchestrator` | `orchestrator` | `kanban-orchestrator`, `sibling-agent-talent-gate-protocol` |

Create them using the automated script:
```bash
# From hermes-agent-architecture skill
skills-library/autonomous-ai-agents/hermes-agent-architecture/scripts/create-body-system-profiles.sh
```

Or manually for custom setups:
```bash
hermes profile create researcher --clone
hermes profile create engineer --clone
hermes profile create reviewer --clone
# Add appropriate skills to each
```

See `hermes-agent-architecture` skill (`references/body-system-mapping.md`) for complete physiological rationale.

### Step 4: Orchestrator Behavior

The orchestrator profile (with `kanban-orchestrator` skill) will:
1. Receive the Telegram message
2. Decompose the request into lanes (research, implementation, review)
3. Create Kanban tasks assigned to specialist profiles
4. Report back to user with task IDs

Example decomposition (from kanban-orchestrator skill):

```python
t1 = kanban_create(
    title="research: Postgres cost vs current",
    assignee="researcher",
    body="Compare estimated infrastructure costs...",
)
t2 = kanban_create(
    title="research: Postgres performance vs current",
    assignee="researcher",
    body="Compare query latency, throughput...",
)
t3 = kanban_create(
    title="synthesize migration recommendation",
    assignee="analyst",
    body="Read findings from T1 and T2...",
    parents=[t1, t2],
)
```

## Alternative: Pre-Gateway Dispatch Hook

For simpler auto-routing without a full orchestrator profile, add a plugin hook:

```python
# <agent-home>/plugins/telegram_kanban_hook.py
from hermes_cli.plugins import hook

@hook("pre_gateway_dispatch")
def telegram_to_kanban(event, gateway, session_store):
    if event.source.platform.value == "telegram":
        text = (event.text or "").lower()
        work_keywords = ["build", "fix", "research", "analyze", "create", "implement", "deploy"]
        if any(kw in text for kw in work_keywords):
            return {"action": "rewrite", "text": f"/kanban create \"{event.text}\" --assignee engineer"}
    return {"action": "allow"}
```

## Kanban Notifications via Gateway

The gateway runs a **Kanban notifier** (`_kanban_notifier_watcher` in `kanban_watchers.py`) that:
- Polls `kanban_notify_subs` every 5 seconds
- Delivers `completed`, `blocked`, `gave_up`, `crashed`, `timed_out` events to users
- Subscriptions are created when a user is assigned a task or subscribes via `/kanban watch`

Users receive notifications in their gateway chat (Telegram DM, Discord, etc.) when tasks they care about change state.

## Multi-Board Support

Each Kanban board is a separate SQLite database. The notifier iterates all boards on disk. Configure multiple boards for different teams/projects:

```bash
hermes kanban init --slug team-alpha
hermes kanban init --slug team-beta
```

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Orchestrator profile doesn't exist | Create it with `hermes profile create orchestrator` |
| Specialist profiles don't exist | Create `researcher`, `engineer`, `reviewer` profiles |
| Kanban dispatcher not running in gateway | Ensure `kanban.dispatch_in_gateway: true` in config (default) |
| Gateway allowlist blocks messages | Add `TELEGRAM_ALLOWED_USERS=your_id` to `.env` and restart gateway |
| Tasks stuck in `ready` | Check dispatcher logs; verify assignee profile names match exactly |
| No notifications received | Check `kanban_notify_subs` table; ensure gateway has active adapter for platform |

## Verification Checklist

- [ ] Orchestrator profile exists and has `kanban-orchestrator` skill
- [ ] Specialist profiles exist (`researcher`, `engineer`, `reviewer`, etc.)
- [ ] `config.yaml` routes Telegram to orchestrator profile
- [ ] Gateway allowlist configured (`TELEGRAM_ALLOWED_USERS`)
- [ ] Gateway restarted after config changes
- [ ] Test: Send "Research GRPO papers" to Telegram bot → should create Kanban task
- [ ] Test: Check `/kanban list` shows the task assigned to researcher