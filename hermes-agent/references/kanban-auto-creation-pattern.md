# Kanban Auto-Creation Pattern — Working Implementation

## Problem
Automatically create Kanban tasks from incoming Telegram messages without manual `/kanban create` commands.

## Working Pattern (Validated June 2026)

### 1. Profile Configuration (`config.yaml`)
```yaml
toolsets:
  - hermes-cli
  - kanban        # REQUIRED: enables kanban_* tools for this profile
kanban:
  orchestrator_profile: "principal-interface"  # Profile that receives gateway messages
```

### 2. SOUL.md Instruction (Critical)
Add explicit instruction to the profile's SOUL.md:

```markdown
## Kanban Integration — AUTO-CREATE TASKS FOR WORK REQUESTS
When the principal gives ANY work request (build, fix, research, analyze, create, implement, deploy, design, plan, schedule, write, code, develop, launch, optimize, refactor, test, debug, investigate, review, document, migrate, upgrade, configure, integrate, automate):

**IMMEDIATELY create a Kanban task** using the kanban_create tool:
1. Analyze the request and determine the appropriate assignee profile
2. Call `kanban_create` with title, assignee, and body
3. For multi-step requests, decompose into multiple linked tasks
4. Report the task ID(s) to the principal

**Assignee Mapping:**
- research, investigate, analyze, study → researcher
- design, ui, ux, mockup, wireframe → designer
- review, audit, test, qa, quality → reviewer
- plan, strategy, roadmap, prioritize → planner
- build, fix, implement, code, deploy, develop, launch → engineer
- health, vitals, diagnose, clinical → bernard
- monitor, stress, immune, surveillance → allostasis
- tasks, plan, schedule, lattice → quartz
- build, product, feature, growth → seed
- coach, strategy, mastermind → wave
- registry, fleet, status, map → morphogen
- flow, messages, circulation → harvey

**For multi-step requests:** Decompose into linked tasks with parent/child relationships.
```

### 3. Gateway Config (`config.yaml`)
```yaml
telegram:
  default_profile: "principal-interface"  # All Telegram messages route here
```

### 4. Gateway Restart Required
After config changes:
```bash
hermes gateway restart
# Or for clean restart:
pkill -f "gateway run"
hermes gateway run
```

### What Doesn't Work
- **Pre-gateway-dispatch hooks** - Hooks run in gateway process, cannot call the operator agent tools (kanban_create). The hook approach rewrites the message to a slash command but the slash command still needs the agent to execute it.

### Verification
Test with a work request message:
```
"Build a monitoring dashboard for engine health metrics"
```
Should create Kanban task assigned to `engineer` profile.

### Session Evidence
- Session `20260614_070532_4c526f` - Kanban task `t_a9b0b19d` created for "Test dashboard monitoring task" assigned to `engineer`
- Gateway log shows: `1 hook(s) loaded` + `kanban dispatcher: embedded in gateway (interval=60.0s)`

### Profile Setup Checklist
- [ ] Profile exists: `hermes profile create principal-interface --clone`
- [ ] Model set: `hermes -p principal-interface config set model.default "openrouter/nvidia/nemotron-3-ultra:free"`
- [ ] Skills copied: `hermes-agent`, `kanban-orchestrator`, `aisha-md-health-orchestration`, `sentinel-compliance-audit`, `aisha-three-sisters-architecture`
- [ ] Toolsets: `hermes-cli`, `kanban`
- [ ] SOUL.md with auto-create instruction
- [ ] Kanban config: `orchestrator_profile: "principal-interface"`
- [ ] Gateway: `telegram.default_profile: "principal-interface"`
- [ ] Gateway restarted after changes