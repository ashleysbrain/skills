# Telegram + Kanban Integration for the principal Interface

## Overview
This document describes the working pattern for routing Telegram messages through an principal-interface profile that auto-creates Kanban tasks for work requests.

## Architecture

```
Telegram → Gateway → principal-interface profile → Agent loop → kanban_create tool → Kanban board → Dispatcher → Specialist profiles
```

## Profile Configuration

### principal-interface Profile
- **Model:** `openrouter/nvidia/nemotron-3-ultra:free`
- **Skills:** `hermes-agent`, `kanban-orchestrator`, `kanban-worker`, `aisha-md-health-orchestration`, `aisha-three-sisters-architecture`, `sentinel-compliance-audit`
- **SOUL.md:** Contains auto-create Kanban instructions + engine routing logic

### Gateway Config
```yaml
telegram:
  default_profile: "principal-interface"
```

### Kanban Config
```yaml
kanban:
  dispatch_in_gateway: true
  dispatch_interval_seconds: 60
  orchestrator_profile: "principal-interface"
  auto_decompose: true
  auto_decompose_per_tick: 3
  board: "ds-organism"
```

## SOUL.md Auto-Create Instructions
The principal-interface SOUL.md contains explicit instructions for the agent to auto-create Kanban tasks:

1. **Trigger:** Any work request keyword detected (build, fix, research, analyze, create, implement, deploy, design, plan, etc.)
2. **Action:** Call `kanban_create` tool with title, assignee, body
3. **Assignee mapping:** Keywords → profile names (researcher, engineer, designer, reviewer, planner, bernard, allostasis, quartz, seed, wave, morphogen, harvey)
4. **Multi-step:** Decompose into linked tasks with parent/child relationships

## Engine Routing Logic
The principal-interface also routes non-Kanban requests to engine APIs:

| Keywords | Engine | Endpoint |
|----------|--------|----------|
| health, vitals, diagnose, clinical, rounds | Bernard (8094) | `/patient/vitals`, `/rounds` |
| coach, strategy, decide, mastermind | Wave (8000) | `/v3/workspaces/.../chat` |
| tasks, plan, schedule, lattice | Quartz (8089) | `/v1/tasks`, `/v1/lattice/state` |
| build, product, feature, growth | Seed (8090) | `/v1/engines`, `/landau` |
| monitor, stress, immune | Allostasis (8091) | `/organism` |
| registry, fleet, status, map | Morphogen (8093) | `/organism/map` |
| flow, messages, circulation | Harvey (8092) | `/fabric/vitals` |

## Verification Checklist

- [ ] `principal-interface` profile exists with `kanban-orchestrator` skill
- [ ] `config.yaml` has `telegram.default_profile: "principal-interface"`
- [ ] `config.yaml` has `kanban.orchestrator_profile: "principal-interface"`
- [ ] SOUL.md contains auto-create Kanban instructions
- [ ] Gateway logs show "kanban dispatcher: embedded in gateway"
- [ ] Test message "Research X" creates Kanban task with assignee=researcher
- [ ] Test message "health check" routes to Bernard engine

## Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| No Kanban task created | SOUL.md missing instructions | Add auto-create instructions to SOUL.md |
| Wrong assignee | Keyword not in mapping | Add keyword to SOUL.md mapping |
| Gateway not routing to principal-interface | Config missing | Set `telegram.default_profile` |
| Kanban dispatcher not running | Gateway restart needed | Restart gateway, check logs |
| Tasks stuck in "ready" | Specialist profile doesn't exist | Create profile or change assignee |

## Gateway Restart Pattern
```bash
pkill -f "gateway run" 2>/dev/null; sleep 2
cd /<workspace> && /<workspace> -m hermes_cli.main gateway run &
```

## Test Commands
```bash
# Direct Kanban create (CLI)
hermes kanban create "Test task" --assignee engineer

# Via Telegram (should auto-create)
send_message "Build a dashboard for monitoring engine health" to telegram

# Check board
hermes kanban list
```