---
name: thalamus-gate
category: operations
description: Step 0 input classifier. Runs BEFORE the specialist gate. Determines which organism/product/domain the user's message belongs to, then routes all work output, artifacts, and memory to the correct namespace.
version: 1.0.0
---

# Thalamus Gate — Input Router

**MANDATORY:** Run this BEFORE the specialist gate. This is Step 0.

## What This Does

The user sends everything through one input (Telegram or desktop). This gate classifies what the message is about and routes all subsequent work to the correct workspace, repo, and memory namespace.

## The Classification (Run on Every Input)

Ask: "What organism or product is this about?"

### Domain Routes

| # | Domain | Signal Words | Routes To | Workspace | GitHub | Memory |
|---|--------|-------------|-----------|-----------|--------|--------|
| 1 | **the operator agent Organism** | body parts, engines, tissue, neuroanatomy, hippocampus, cortex, organ, vessel, connective, epithelial, glial, muscle, ECS, fleet | the operator agent's brain | ~/your-workspace/agent-organism | your-org/the operator agent | the operator agent namespace |
| 2 | **8D Womb** | 8D, 8D sleep, divinity health, sleep product, insomnia, womb product | 8D product (Divinity Health womb) | ~/your-workspace/8d-sleep or divinity-health | your-org org (8D product repo) | Product memory |
| 3 | **Future Product Wombs** | other products, new product, product launch | Their respective womb | Product-specific workspace | your-org org (product repo) | Product memory |
| 4 | **Personal Health** | symptoms, tracking, my health, wellness, medication, sleep (personal), body (personal) | AISHA-MD | ~/your-workspace (health dir) | Private | Health memory |
| 5 | **Operations** | cron, fleet, skills, agents, config, gateway, scheduling | Infrastructure | <agent-home>/ | Internal | the operator agent memory |
| 6 | **General/Research** | research, papers, question, learning, no specific organism | Shared | ~/your-workspace/docs | Varies | Shared memory |

### Classification Rules

1. **Default to the operator agent** unless the signal clearly indicates otherwise. Most work is organism building. All the operator agent work goes to your-org/the operator agent.
2. **Product mentions override the operator agent.** If the user says "8D" or "8D sleep" or "divinity health" or a product name, route to that product womb. Products live in the your-org org under their own repo.
3. **Health mentions are personal.** "My sleep" vs "sleep engine" are different domains. Personal health = AISHA-MD.
4. **the operator agent work never goes to AISHA repos.** the operator agent organism work goes to your-org/the operator agent only.
5. **When ambiguous, ask.** Don't guess and route wrong.
6. **Never call real engines/profiles "stale."** Engines in the registry ARE the organism's body parts. Check the ECS registry for active fleet status, not assumptions from folder names or timestamps. User corrected this on 2026-06-21: profiles that look unused may be real anatomical AI parts.

### Routing Actions

After classification, ALL subsequent work follows the route:

- **Files** written to the domain's workspace path
- **GitHub pushes** go to the domain's repo
- **Memory updates** go to the domain's memory namespace
- **Specialist gate** loads within the domain context
- **Cron jobs** deliver to the domain's channel if domain-specific

### Product Confusion — The Critical Danger Zone

**THE PATTERN:** Multiple products in the same ecosystem can have similar-looking architecture, conflicting dimension systems, and overlapping naming. When you hit uncertainty about which product is the target, STOP and verify.

**RED FLAGS for product confusion:**
- You're looking at BUILD-DIRECTION files and unsure if they apply
- You see "8 dimensions" in one place and "6 dimensions" in another
- You're unsure whether work should go to `divinity-health` or `the operator agent`
- API contracts exist for both human wellness and AI health
- The task mentions multiple "options" that could apply to different products

**VERIFICATION PROTOCOL (when you hit a product-confusion red flag):**
1. **Read the BUILD-DIRECTION-STATEMENT.md** for the product you THINK is the target — check the approved status date
2. **Compare dimension systems** in the relevant files (8 human dimensions vs 6 AI dimensions)
3. **Check which product the user's OPTIONS refer to** — look for product names in the task description
4. **Ask clarification BEFORE proceeding** — do not guess and route to the wrong workspace

**THE INCIDENT (2026-07-06):** While executing 4 options with specialist routing (Tawara → Andreasen → Wernicke → Luria), the agent hit a critical confusion:
- **Option 1** involved approving BUILD-DIRECTION and creating API function-calling schemas
- **BUILD-DIRECTION-STATEMENT.md** listed 8 human wellness dimensions (sleep, circadian, physical, emotional, cognitive, financial, environmental, social)
- **The agent had previously created 6+1 AI dimensions** (COG, PIP, RES, KNW, ALN, ADP + INT) for the operator agent Organism
- **API-CONTRACT.md v2.0.0** existed for human wellness product

The agent correctly paused and asked: "Which product are you asking me to work on? Divinity Health (human wellness with 8 dimensions) or the operator agent Organism (AI health with 6+1 dimensions)?"

**THE LESSON:** When dimension systems, API contracts, and build directions conflict between products, assume you don't know. Verify by reading the approved build-direction and dimension definitions, then ask if still unclear.

## Desktop/Telegram Synergy

Both the Telegram the operator agent and desktop the operator agent instances:
- Share the same filesystem (~/your-workspace)
- Share the same memory (<agent-home>/)
- Share the same skills (skills-library/)
- Share the same cron jobs

They are two sensory inputs to one brain. When desktop is working on something, Telegram can see the same files. When Telegram builds something, desktop can continue it.

For handoff: use session_search to find what the other instance was working on. The checkpoint file (from reboot mitigation plan) will eventually make this automatic.

## Anti-Patterns

1. **Saving the operator agent work under AISHA repos** — the operator agent organism work goes to your-org/the operator agent ONLY
2. **Calling 8D "AD"** — it is 8D (the number 8, letter D), not AD. 8D Sleep is the Divinity Health womb product.
3. **Mixing product work with organism work** — products have their own repos in your-org org
4. **Saving health data to the operator agent memory** — health is private, goes to AISHA-MD
5. **Cross-contaminating memory namespaces** — each domain has its own memory
6. **Creating scattered files across workspaces** — route to the correct workspace first

## The Exchange Step (MANDATORY — runs between Thalamus and Specialist)

Before proposing ANY architecture, code, or workflow, you MUST check what already exists in the workspace. This is not optional. This is the step that prevents you from proposing to rebuild infrastructure that is already built.

**On every non-trivial task, run these checks before proposing anything:**

1. **Search the workspace**: `find <workspace> -type f \( -name "*.py" -o -name "*.md" -o -name "*.yaml" \) | grep -v venv | grep -v node_modules` to see what's there
2. **Check the organism directory**: `ls organism/` — this is where shared infrastructure lives (operator_bus.py, agents.yaml, bootstrap.sh, etc.)
3. **Read the operator bus**: `python3 organism/operator_bus.py status` — see if communication infrastructure exists
4. **Check git log**: `git log --oneline -10` — see what was recently built
5. **Search for keywords**: `grep -rl "<key concept>" --include="*.py" --include="*.md" . | grep -v venv` before proposing to build anything related to that concept

**The incident that created this rule (2026-06-22):** The user asked about inter-agent communication architecture. the operator agent ran a research subagent, got back a detailed proposal, and was about to propose building a "Gap Junction Protocol" with heartbeat files, message buses, and a state store. The user stopped it and said "I feel like we already built something like this." the operator agent checked and found:
- `organism/operator_bus.py` — a FULL SQLite message queue for inter-agent communication (already built)
- `organism/agents.yaml` — a complete manifest with failover rules, health checks, and organ ownership (already built)
- `<agent-home>/state/checkpoint_store.py` — a working memory analog that survives crashes (already built)

All three pieces of infrastructure existed. the operator agent nearly proposed rebuilding them from scratch because it skipped the exchange step. The user's words: "you need to look at what we've already built and make absolutely sure that this list is correct."

**The rule: if you haven't read the workspace, you haven't done the Thalamus gate.**

## Execution Order

```
0.   THALAMUS GATE: What domain? (this skill)
0.5  EXCHANGE: Read existing workspace files, check git log, search for existing infrastructure
0.75 PHYSICS DECOMPOSITION: Break into micro-tasks
1.   SPECIALIST GATE: Which specialist within that domain?
2.   TALENT PROTOCOL: Which variation (V1-V10)?
3.   EXECUTE with correct workspace, repo, memory
```
