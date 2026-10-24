---
name: hermes-gateway-kanban
description: Configure and use the the operator agent Gateway's embedded Kanban dispatcher for Telegram (and other platform) workflows. Covers dispatcher config, profile skills, routing patterns, and integration with multi-engine architectures.
version: 1.0.0
author: the operator agent Agent
license: MIT
metadata:
  hermes:
    tags: [kanban, gateway, telegram, dispatcher, multi-engine, routing]
    related_skills: [kanban-codex-lane, kanban-worker, hermes-agent, hermes-agent-architecture]
---

# the operator agent Gateway Kanban Dispatcher

## Overview

The the operator agent Gateway includes a **built-in Kanban dispatcher** that runs inside the gateway process (not as a separate agent). It polls the Kanban board at a configured interval, assigns work to worker profiles, and handles task lifecycle. This skill covers configuring the dispatcher, setting up worker profiles with the `kanban-orchestrator` skill, and routing Telegram (or other platform) messages into Kanban tasks.

**Key distinction**: This is NOT the Codex lane pattern (`kanban-codex-lane`). The gateway dispatcher is a native the operator agent feature for orchestrating work across the operator agent profiles. Codex lanes are an optional implementation detail *inside* a worker's run.

## When to Use

- You want Telegram messages to create Kanban tasks automatically
- You have multiple the operator agent profiles (worker pool) that should pull from a shared board
- You need a single Telegram entry point that routes to different engines/profiles via Kanban
- You want the gateway to handle task dispatch, heartbeats, and stale-task recovery

## Gateway Configuration (`config.yaml`)

```yaml
kanban:
  dispatch_in_gateway: true          # Enable embedded dispatcher (default: true)
  dispatch_interval_seconds: 60      # Poll interval (default: 60)
  failure_limit: 2                   # Max failures before task blocked (default: 2)
  worker_log_rotate_bytes: 2097152   # Worker log rotation (2MB)
  worker_log_backup_count: 1         # Keep 1 rotated log
  orchestrator_profile: ''           # Optional: profile name for orchestrator role
  default_assignee: ''               # Optional: default assignee for tasks
  max_in_progress_per_profile: null  # Optional: limit concurrent tasks per profile
  auto_decompose: true               # Auto-decompose parent tasks (default: true)
  auto_decompose_per_tick: 3         # Max decompositions per tick (default: 3)
  dispatch_stale_timeout_seconds: 14400  # Stale task timeout (4 hours)
```

**Restart gateway after config changes**: `hermes gateway restart`

## Worker Profile Setup

Each profile that should execute Kanban tasks needs the `kanban-orchestrator` skill:

```bash
# Create or use existing profile
hermes profile create my-worker --clone
hermes -p my-worker config set model.default "openrouter/nvidia/nemotron-3-ultra:free"

# Install kanban-orchestrator skill
cp -r skills-library/devops/kanban-orchestrator <agent-home>/profiles/my-worker/skills/

# Or if using hub-installed skill
hermes -p my-worker skills install kanban-orchestrator
```

**Profile requirements**:
- `kanban-orchestrator` skill installed
- Appropriate model for task decomposition (Nemotron-3-Ultra recommended)
- Access to any tools/engine APIs the tasks require

## Patient/Interface Profile Pattern (Single Telegram Entry Point)

For a unified Telegram contact that routes to multiple backend engines:

### 1. Create Interface Profile

```bash
hermes profile create patient-interface --clone
hermes -p patient-interface config set model.default "openrouter/nvidia/nemotron-3-ultra:free"

# Core skills
cp -r skills-library/autonomous-ai-agents/hermes-agent <agent-home>/profiles/patient-interface/skills/
cp -r skills-library/devops/kanban-orchestrator <agent-home>/profiles/patient-interface/skills/
# Domain-specific skills (e.g., health tracking)
cp -r skills-library/operations/aisha-md-health-orchestration <agent-home>/profiles/patient-interface/skills/
```

### 2. Set as Telegram Default Profile

```bash
hermes config set telegram.default_profile patient-interface
hermes gateway restart
```

### 3. Define Routing Logic in Profile SOUL.md

The profile's `SOUL.md` should contain routing rules that map message intent to engine APIs:

```markdown
## Routing Logic
Analyze user's message intent, then call the appropriate engine API:

- "health", "vitals", "diagnose" → Bernard (8094) /rounds, /patient/vitals
- "coach", "strategy", "decide" → Wave (8000) /coach
- "tasks", "plan", "schedule" → Quartz (8089) /tasks
- "build", "product", "feature" → Seed (8090) /projects
- "monitor", "stress", "immune" → Allostasis (8091) /organism
- "registry", "fleet", "status" → Morphogen (8093) /organism/map
- "flow", "messages" → Harvey (8092) /fabric/vitals
```

### 4. Kanban Task Creation from Telegram

Two patterns:

**Pattern A: Direct Kanban Creation (via profile skill)**
The `patient-interface` profile receives Telegram message → uses `kanban-orchestrator` to decompose → creates Kanban cards → assigns to worker profiles.

**Pattern B: Gateway Dispatcher (native)**
Gateway Kanban dispatcher polls board → assigns ready tasks to available worker profiles → workers execute with their skills.

**Recommendation**: Use Pattern A for user-facing Telegram interaction (immediate response, kanban-orchestrator handles decomposition). Use Pattern B for background/batch work where gateway dispatcher manages a pool of workers.

## Multi-Engine Architecture Integration

When worker profiles represent different engines (Wave, Quartz, Seed, Bernard, etc.):

1. **Register engines in Morphogen** (registry engine):
   ```bash
   curl -X POST http://127.0.0.1:port/genotypes/register \
     -H "Content-Type: application/json" \
     -d '{"engine_id": "wave", "name": "Wave Engine", ...}'
   ```

2. **Worker profiles call engine APIs directly** (not via Morphogen):
   Each worker profile's skills know the engine endpoints:
   ```python
   ENGINE_ENDPOINTS = {
       "wave": "http://127.0.0.1:port",
       "quartz": "http://127.0.0.1:port",
       "seed": "http://127.0.0.1:port",
       "allostasis": "http://127.0.0.1:port",
       "harvey": "http://127.0.0.1:port",
       "morphogen": "http://127.0.0.1:port",
       "bernard": "http://127.0.0.1:port",
   }
   ```

3. **Kanban cards specify target engine**: Task body includes `engine: "bernard"` or `endpoint: "http://127.0.0.1:port/rounds"`

## Dispatcher Monitoring & Debugging

```bash
# Check gateway logs for dispatcher activity
tail -f <agent-home>/logs/gateway.log | grep -i kanban

# Expected log lines:
# "kanban dispatcher: embedded in gateway (interval=60.0s)"
# "kanban_dispatcher: polling board..."
# "kanban_dispatcher: assigned task_... to profile_..."

# Verify dispatcher is running
ps aux | grep hermes
# Should show gateway process with kanban dispatcher
```

## Common Pitfalls

1. **Dispatcher not running**: Ensure `dispatch_in_gateway: true` and gateway restarted. Check logs for "kanban dispatcher: embedded in gateway".

2. **Tasks not assigned**: Verify worker profiles have `kanban-orchestrator` skill and are not at `max_in_progress_per_profile` limit.

3. **Telegram messages not creating tasks**: The gateway dispatcher only polls existing Kanban board. For Telegram → Kanban, the interface profile must create tasks (Pattern A) or a webhook must create them.

4. **Stale tasks piling up**: Adjust `dispatch_stale_timeout_seconds` (default 4 hours). Increase `failure_limit` if tasks fail transiently.

5. **Profile skill conflicts**: Don't install both `kanban-codex-lane` and `kanban-orchestrator` in same profile unless you understand the ownership rules (Codex lane is an *implementation detail* inside a worker run; orchestrator manages the Kanban lifecycle).

## Verification Checklist

- [ ] `config.yaml` has `kanban.dispatch_in_gateway: true`
- [ ] Gateway restarted after config change
- [ ] Logs show "kanban dispatcher: embedded in gateway"
- [ ] Worker profiles have `kanban-orchestrator` skill installed
- [ ] Interface profile has routing logic in SOUL.md
- [ ] `telegram.default_profile` set to interface profile
- [ ] Engine APIs registered in Morphogen (if using registry)
- [ ] Test message creates Kanban task and completes

## References

- `references/gateway-kanban-config.md` — Full config.yaml kanban section with annotations
- `references/patient-interface-soul.md` — Example SOUL.md for patient interface profile
- `references/engine-endpoints.md` — Standard engine endpoint map for multi-engine architectures
- `references/dispatcher-logs.md` — Expected log patterns and troubleshooting
- `references/principal-interface-pattern.md` — Complete the principal Interface (Patient 0) implementation: profile setup, SOUL.md routing logic, engine endpoints dictionary, clinical engine identity hardening, 12 health system models, evidence synthesis scanner, 26 concept mappings, cross-domain insights, novel approach generator (AOPD), engine fleet startup/recovery patterns

**the principal Interface Deployment (Patient 0 with Telegram + Kanban):**
- See `../hermes-agent/references/telegram-kanban-integration.md` for the complete deployment pattern

## Related Skills

- `kanban-codex-lane` — For workers that want to use Codex CLI as implementation lane *inside* their Kanban run
- `kanban-worker` — General Kanban worker patterns
- `hermes-agent` — Core the operator agent configuration and profile management
- `hermes-agent-architecture` — Class-level architecture patterns