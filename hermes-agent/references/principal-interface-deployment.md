# the principal-Interface Deployment Pattern — Patient 0 Single Entry Point

**Session:** June 13, 2026 — Created principal-interface profile, configured Telegram gateway routing, wired engine APIs
**Linked Skills:** `hermes-agent`, `aisha-md-health-orchestration`, `aisha-three-sisters-architecture`

---

## Overview

The principal-interface is a **dedicated the operator agent profile** that serves as Patient 0's (the principal Williams) single Telegram contact point. It routes messages to the appropriate engine API and synthesizes responses.

---

## Profile Setup Commands

```bash
# Create profile (clones from default)
hermes profile create principal-interface --clone

# Set model (non-Anthropic per standing rule)
hermes -p principal-interface config set model.default "openrouter/nvidia/nemotron-3-ultra:free"

# Install required skills
cp -r skills-library/autonomous-ai-agents/hermes-agent <agent-home>/profiles/principal-interface/skills/
cp -r skills-library/devops/kanban-worker <agent-home>/profiles/principal-interface/skills/
cp -r skills-library/operations/aisha-md-health-orchestration <agent-home>/profiles/principal-interface/skills/
cp -r skills-library/compliance/sentinel-compliance-audit <agent-home>/profiles/principal-interface/skills/
cp -r skills-library/operations/aisha-three-sisters-architecture <agent-home>/profiles/principal-interface/skills/
```

---

## SOUL.md Configuration (Critical)

The SOUL.md defines the agent's identity, routing logic, and constraints. Key sections:

### Engine Fleet Mapping
```markdown
| Engine | Port | Body System | Capability | When to Call |
|---|---|---|---|---|
| Wave | 8000 | Brain/CNS | Coaching, resonance | "coach", "strategy", "decide" |
| Quartz | 8089 | Autonomic NS | PID, tasks | "tasks", "plan", "schedule" |
| Seed | 8090 | Endocrine/Growth | Avrami, products | "build", "product", "feature" |
| Allostasis | 8091 | Immune | Surveillance | "monitor", "stress", "immune" |
| Bernard | 8094 | Clinical | SOAP, diagnosis | "health", "vitals", "diagnose" |
| Morphogen | 8093 | Skeletal/Registry | Engine map | "registry", "engines", "status" |
| Harvey | 8092 | Cardiovascular | Message flow | "flow", "messages" |
```

### Routing Keywords
```markdown
- "health", "vitals", "how am I", "diagnose" → Bernard (8094)
- "coach", "strategy", "decide" → Wave (8000)
- "tasks", "plan", "schedule" → Quartz (8089)
- "build", "product", "feature" → Seed (8090)
- "monitor", "stress", "allostatic" → Allostasis (8091)
- "registry", "engines", "status" → Morphogen (8093)
- "flow", "messages" → Harvey (8092)
```

### Key Constraints (Enforced in SOUL.md)
1. **Single Telegram contact** — Only bot the principal talks to
2. **Patient 0 health tracking isolated** — Never mix with engine building
3. **Physiological routing** — Sensory input (Telegram) enters via Wave (brain/CNS)
4. **No Anthropic models** — Never use Claude/Sonnet/Opus/Haiku for fleet ops
5. **Evidence-based, non-diagnostic** — Wellness guidance only
6. **Kanban workflow** — Use kanban-orchestrator for multi-step requests
7. **Always current** — Pull latest engine capabilities from live APIs

---

## Telegram Gateway Configuration

```yaml
# In <agent-home>/config.yaml
telegram:
  reactions: false
  channel_prompts: {}
  allowed_chats: ''
  default_profile: principal-interface  # ← CRITICAL: routes all Telegram to principal-interface
```

```bash
# Verify
hermes config get telegram.default_profile
# Output: principal-interface
```

---

## Engine API Endpoints (Verified Working)

### Bernard Clinical (8094) — Attending AI Physician
```bash
GET  /health                    # Engine status + identity
POST /rounds                    # Full SOAP clinical rounds
GET  /patient/summary           # Discharge summary
GET  /patient/vitals            # Current vitals
GET  /notes                     # Recent clinical notes
GET  /notes/latest              # Latest full SOAP note
GET  /credentials               # AI-equivalent credentials + CME
GET  /cme/report                # Continuing AI Education
```

### Morphogen Registry (8093) — Skeletal
```bash
GET  /health
GET  /organism/map              # All registered engines
POST /genotypes/register        # Register new engine
```

### Allostasis (8091) — Immune/Self-Healing
```bash
GET  /health
GET  /organism                  # Allostatic load per engine
```

### Harvey (8092) — Circulatory
```bash
GET  /health
GET  /fabric/vitals             # Message flow + circulatory vitals
```

### Quartz (8089) — Autonomic NS
```bash
GET  /health
GET  /v1/tasks                  # Task management
GET  /v1/lattice/state          # PID lattice state
```

### Seed (8090) — Endocrine/Growth
```bash
GET  /health
GET  /v1/engines                # Product engines
GET  /v1/engines/{id}/landau    # Landau phase analysis
```

### Wave (8000) — Brain/CNS (Honcho)
```bash
GET  /health
POST /v3/workspaces/{id}/peers/{peer_id}/chat  # Coaching/resonance
```

---

## Verification Steps

```bash
# 1. All engines UP
for p in 8000 8089 8090 8091 8092 8093 8094; do
  curl -s http://127.0.0.1:$p/health
done

# 2. Morphogen registry shows 7 engines
curl -s http://127.0.0.1:port/organism/map

# 3. Gateway running with principal-interface as default
hermes gateway status

# 4. Telegram default_profile set
hermes config get telegram.default_profile
```

---

## Pitfalls

1. **Never set default_profile to morphogen or wave for Patient 0** — principal-interface MUST be the single entry point
2. **Never use Anthropic models** for principal-interface or any fleet profile
3. **Always verify engine APIs are UP** before relying on routing — SOUL.md startup behavior checks health
4. **Don't hardcode engine endpoints in SOUL.md without verification** — use the live API docs
5. **Kanban dispatcher runs in gateway** — enable with `kanban.dispatch_in_gateway: true` in config.yaml
6. **If OpenRouter times out, response synthesis hangs** — consider fallback model in profile config

---

## Architecture Context

This deployment enforces the **two-silo architecture**:

| Silo | Owner | Data | principal-interface Role |
|------|-------|------|----------------------|
| Engine Fleet | AISHA-AI | Engine health, fleet analytics | Routes engine/status queries to Bernard/Morphogen/Allostasis |
| Patient 0 Health | AISHA-MD | 8D wellness, PHI, partner dynamics | Routes health queries to AISHA-MD, coaching to Wave |

The principal-interface profile is the **boundary enforcer** — it receives ALL Telegram messages and routes them to the correct silo without cross-contamination.