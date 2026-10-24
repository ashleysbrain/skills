---
name: external-coding-agent-integration
description: Evaluate and integrate external coding agents into the DS organism.
version: 1.0.0
author: the operator agent Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [coding-agent, organism-integration, body-part-mapping, antigravity, claude-code, codex]
    related_skills: [body-part-tackle-workflow, agent-consortium-design, ai-organism-neural-process-architecture, hermes-agent-architecture]
---

# External Coding Agent Integration

Framework for evaluating a new external coding agent (Antigravity, Claude
Code, Codex, Blackbox, etc.) and integrating it into the DS organism as a
body-part analog. Covers capability assessment, anatomical mapping, staged
integration planning, and autonomous task-pickup evaluation.

## When to Use

- User asks "can we use X as another layer?"
- Evaluating whether a new coding agent fits the organism
- Planning integration stages for an external CLI/IDE agent
- Deciding body-part analog for a new tool
- Assessing whether an agent can pick up tasks autonomously

## Core Principle

Every external coding agent maps to a biological structure, not a vague
role. The mapping must be anatomically accurate. The agent must fill a
functional gap the organism does not already cover.

## Step 1: Capability Assessment (Inspect Before Proposing)

NEVER propose integration until you have inspected the tool's actual
capabilities. Use `web_search` and `web_extract` to research:

- Does it have a CLI? Can it run headless (non-interactive)?
- Does it support autonomous completion without plan approval?
- Can it spawn subagents for parallel work?
- Does it speak MCP (Model Context Protocol)?
- Does it have browser control / verification capabilities?
- What auth model does it use (API key vs OAuth)?

Record findings in a reference file, not in the conversation.

## Step 2: Body-Part Mapping

Map the tool to a biological structure using these criteria:

| Criterion | Question |
|-----------|----------|
| Initiation | Does it self-initiate, or does it get triggered by cortex/autonomic? |
| Coordination | Does it coordinate multiple parallel processes? |
| Feedback | Does it refine output based on sensory verification? |
| Autonomy | Can it run routine programs without conscious supervision? |
| Scope | Is it a full organ or a specialized substructure? |

### Known mappings

| Tool | Body-Part Analog | Why |
|------|-----------------|-----|
| the operator agent | Peripheral + autonomic nervous system | Continuous monitoring, reflexes, patient-facing comms, heartbeat |
| Opencode | Central cortex (motor + prefrontal) | Conscious deep thought, planning, surgery, voluntary action |
| Antigravity (`agy`) | Cerebellum | Coordinates parallel subagents, refines output via browser verification, handles complex goal execution without initiating action |

The cerebellum analogy is strong because: (1) it does not initiate action
(the cortex decides), (2) it coordinates dozens of parallel processes, (3)
it runs autonomously once given a goal, (4) it refines via proprioceptive
feedback (Antigravity's browser verification), and (5) it handles routine
motor programs while the cortex focuses on higher-level work.

## Step 3: Integration Stages (Adiabatic Path)

Physics gate: change parameters slowly, stay in ground state. Never
big-bang an integration. Follow these stages from smallest to largest
footprint:

### Stage 1: Headless Delegate (zero architecture change)

Call the agent's CLI through the `terminal` tool in one-shot mode. The
agent runs autonomously, returns a result. This is just another terminal
command.

```
terminal(command="agy -p 'task description'", workdir="/path/to/project")
```

For agents that support autonomous completion (Antigravity's `/goal`
prefix), use it to skip plan approval:
```
terminal(command="agy -p '/goal task description'")
```

### Stage 2: MCP Bridge (typed contract)

If the agent speaks MCP, connect it to the operator agent's MCP client. The agent can
discover and call the operator agent-owned tools. Creates a typed contract without
hard coupling.

### Stage 3: Scheduled Autonomous Pickup

the operator agent cron jobs detect work and dispatch to the agent headlessly. The
agent orchestrates its own subagents. Result re-enters the the operator agent
conversation. Full autonomy between dispatch and completion.

## Step 4: Autonomous Task-Pickup Assessment

Can the agent pick up tasks without human intervention?

Check:
1. Does it support a "run to completion" mode (no approval pauses)?
2. Is auth persistent (keyring, not per-session browser login)?
3. Can the operator agent dispatch it via terminal headlessly?
4. Does it return structured output the operator agent can parse?

If all yes: the agent can be wired into cron jobs for fully autonomous
task pickup. If auth requires manual setup: the initial setup is a
one-time human step, then autonomy is possible.

## Step 5: Specialist Routing for Implementation

Strategic assessment and body-part mapping is the operator agent's to give. But the
actual deep system integration (MCP bridge wiring, cron dispatch plumbing,
system-level wiring) is sibling-agent's domain. Hand the build plan to sibling-agent
via the operator bus. the operator agent operates its side: skill activation, cron
dispatch from owned domain, monitoring.

## Pitfalls

1. **Proposing before inspecting.** Never propose integration architecture
   from assumptions. Research the tool's actual capabilities first.
2. **Wrong body-part mapping.** If the tool does not coordinate parallel
   processes, it is not a cerebellum. Map accurately or the integration
   plan will be wrong.
3. **Big-bang integration.** Do not wire MCP bridges and cron dispatch on
   day one. Start with stage 1 (headless delegate), verify, then expand.
4. **Forgetting auth prerequisites.** OAuth-based agents (Antigravity,
   Claude Code) need one manual sign-in before headless operation works.
5. **Duplicating existing organism capability.** Before adding a new agent,
   check whether the operator agent or sibling-agent already covers the function. The
   cerebellum does not replace the cortex; it coordinates what the cortex
   initiates.

## Verification

After planning an integration:
- [ ] Tool capabilities confirmed via research (not assumed)
- [ ] Body-part analog is anatomically defensible
- [ ] Integration starts at stage 1 (smallest footprint)
- [ ] Auth model understood and documented
- [ ] Implementation handoff routed to the correct operator

## Reference

- Antigravity cerebellum analysis: `references/antigravity-cerebellum-analysis.md`
- Body-part mapping methodology: `body-part-tackle-workflow` skill
- Agent consortium design (ephemeral swarms): `agent-consortium-design` skill
