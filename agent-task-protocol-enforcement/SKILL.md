---
name: agent-task-protocol-enforcement
description: Mandatory pre/post task protocol for all AI agents — read profile, check journals, identify personality version, verify scope, journal after. Prevents task loss, scope creep, and history loss.
tags: [sibling-agent, agents, protocol, journaling, personality, task-routing, compliance]
version: 1.0
---

# Agent Task Protocol Enforcement

Use when spawning agents, creating cron jobs, or delegating tasks. Every agent must follow this protocol before and after every task.

## When to Use
- Spawning any new agent (cron or delegate_task)
- Creating or updating cron job prompts
- the principal says agents need to "read their profile" or "journal" or "know their personality"
- Tasks are getting lost, agents are doing work outside their scope, or history is being forgotten
- Validating a runtime-facing agent package against its docs index or startup read list

Support file: `references/runtime-package-audit.md`

## The Protocol (from AGENT-TASK-PROTOCOL.md)

Protocol file: `~/.sibling-agent/workspace/intel/agents/AGENT-TASK-PROTOCOL.md`

### Pre-Task Block (inject into EVERY agent prompt)

```
MANDATORY PRE-TASK PROTOCOL:
1. Read your profile: /<workspace>[CODENAME]-profile.md
2. Read your state file: /<workspace>[CODENAME]-state.json
   This tells you your last persona variation, last actions, pending items, and context notes.
3. Identify your active personality version (V1-V10) based on task type — reference your S3 and S15
4. Resolve the task mode before starting:
   - `base` for ambient maintenance or reading-only work
   - `project` for scoped, multi-step, or named initiatives
   - `task` for a discrete delegated action that should not inherit the whole project frame
5. Verify this task is in your job description (S2). If NOT:
   - Write reassignment request to intel/agents/talent-requests/[DATE]-[CODENAME]-reassign.md
   - Do NOT attempt the task. Route back for proper assignment.
   - Tasks must NOT get lost.
```

### Post-Task Block (inject into EVERY agent prompt)

```
MANDATORY POST-TASK:
Update your state file at /<workspace>[CODENAME]-state.json
Include: current_variation, last_run timestamp, last_actions (list), pending_items, context_notes for next run.
Keep it concise and machine-readable.
If you learned something important or encountered a problem, add it to context_notes.
```

**Note on journals vs state files (updated 2026-06-10):** The old journaling system (300-word essays in learning-journals/) had 0.12% compliance. Agent state files (JSON) replaced journals as the continuity mechanism. State files are maintained by the Fleet Wellness Panel daily. Legacy learning-journals/ directories are archived but not deleted. New agents and cron jobs should use state files, not journal prompts.

## Why This Matters (learned 2026-03-30)

the principal's directives:
1. "Before handling tasks, all AI agents need to read their own profile, prior journals, and task descriptions with personality version identification assigned (V1-V10) before each and every task"
2. "They need to make sure they are doing what's in their job description and if not they need to send the task back through to you for proper reassignment"
3. "Make sure tasks don't get lost"
4. "Then have them journal after every task so history doesn't get lost"

## Scope Boundary Enforcement

Critical lesson from AISHA-MD (2026-03-30): FORGE wrote AISHA-MD's profile with fleet-wide responsibilities (validating all agent scores, fleet wellness reports). the principal corrected this — AISHA-MD is ONLY for the principal's personal health. The task protocol catches this: agents read their profile, verify scope, and reject out-of-scope work.

**Common scope violations to watch for:**
- AISHA-MD doing fleet wellness (that's AISHA/the operator agent)
- Agents doing work in the wrong business world (GD vs DS firewall)
- Generalist agents attempting specialist tasks without panel consultation
- Any agent claiming fleet-wide authority without explicit mandate

## Panel Consultation Pattern

When an agent hits a question outside their confidence threshold:
1. Agent identifies the knowledge gap
2. Files talent request to `intel/agents/talent-requests/[DATE]-[CODENAME]-request-[SPECIALIST].md`
3. Request includes: PURPOSE, TASK_COMPLEXITY, REQUIRED_EXPERTISE, DURATION, URGENCY, JUSTIFICATION
4. FORGE+ARBITER evaluate and dispatch the specialist
5. Results come back through coordination file or direct file output
6. Original agent incorporates verified findings

Example: AISHA-MD convenes panels with HALO (wellness science), DARK-MATTER (literature review), AURORA (psychology) to triple-check health math and science before clinical recommendations.

## Cron Job Template

When creating cron jobs, use this template structure:

```
You are [CODENAME] (E-[###]), [ROLE].

MANDATORY PRE-TASK PROTOCOL:
1. Read your profile: cat ~/.sibling-agent/workspace/intel/agents/codes/[CODENAME]-profile.md | head -150
2. Read your state file: cat ~/.sibling-agent/workspace/intel/agents/state/[CODENAME]-state.json 2>/dev/null
   This tells you your last persona variation, last actions, pending items, and context notes.
3. Active personality version: V[#] ([NAME]) for this task type
4. Verify task is in your job description: [YES/NO reasoning]

TASK: [task description]

MANDATORY POST-TASK:
Update state file at ~/.sibling-agent/workspace/intel/agents/state/[CODENAME]-state.json
Include: current_variation, last_run, last_actions, pending_items, context_notes.
Keep concise and machine-readable.

TALENT GATE: If you need another agent, write request to intel/agents/talent-requests/
Do NOT spawn agents yourself. FORGE+ARBITER evaluate and dispatch.
```

## Task Loss Prevention

- Every task entering the system must be COMPLETED or REASSIGNED (never silently dropped)
- Reassignment requests go to `intel/agents/talent-requests/` with full context
- SENTINEL audits task completion rates weekly
- Timed-out tasks require partial journal + reassignment request

## Pitfalls

1. **Don't skip the profile read for "simple" tasks.** The profile read IS the scope check. Without it, agents drift.
2. **State files replaced 300-word journals (2026-06-10).** The old journaling system had 0.12% compliance. Agent state files (JSON) are the new continuity mechanism. New cron jobs should use state file reads/writes, not journal prompts.
3. **Personality version must be logged.** If the agent doesn't state which V# they're operating as, they're not following protocol.
4. **Reassignment requests must include SUGGESTED_AGENT.** The agent rejecting the task should know enough about the fleet to suggest who SHOULD do it.
5. **Coordination file is append-only JSONL.** Agents should never overwrite it.
6. **Runtime wrappers can drift from docs indices.** If `AGENT.md`/`SOUL.md` lists startup reads, verify them against the docs index and patch missing core support docs instead of assuming the wrapper is complete.
