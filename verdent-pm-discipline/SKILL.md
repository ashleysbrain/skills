---
name: verdent-pm-discipline
version: 1.0.0
category: productivity
description: >
  Operating procedure for project management inspired by Verdent.ai's Manager
  architecture, mapped to the prefrontal executive cortex. Embodies four core
  patterns: decompose before prioritize, never block on a fork, To-Review gate,
  and compounding project memory.
---

# Verdent PM Discipline Skill

## When to Use
- Managing any project or goal that requires decomposition into subtasks
- Working with agent teams or subagents where output verification is needed
- When you want to avoid re-explaining context between related tasks
- Anytime you need to track work with clear acceptance criteria and fork handling

## Core Patterns (Non-Negotiable)

### 1. Decompose Before Prioritize
**Never** start with a flat task list or priority ordering.
- Take any goal (plain language outcome, not steps)
- Decompose into stages → subtasks → dependency DAG
- Attach acceptance criteria to each leaf subtask
- Only then consider priority, resource allocation, or sequencing
- Body analog: dlPFC executive planning

### 2. Never Block on a Fork
When any subtask encounters a missing detail, design choice, or permission:
- Queue the specific question against THAT subtask
- Continue every independent branch that doesn't depend on the blocked subtask
- Surface all open questions in one batch "fork banner" for efficient resolution
- Never halt the entire workflow waiting for one clarification
- Body analog: Anterior cingulate conflict detection → queue interrupt

### 3. To-Review Gate on All Delegated Work
Treat all agent/subagent output as self-requiring verification:
- Nothing is "done" until it passes review against acceptance criteria
- Verify: output matches criteria, files touched are correct, decisions summarized
- Reject and send back to source with specific feedback if criteria unmet
- Body analog: dlPFC outcome monitoring + OFC value assessment

### 4. Memory Compounds Per Project
Stack choices, conventions, and decisions persist across related tasks:
- Store project-scoped preferences (frameworks, naming, architecture decisions)
- Next similar project starts from what was learned, not from scratch
- Reduces re-explaining and increases consistency over time
- Body analog: Hippocampal encoding during consolidation

## Anti-Temptation Rules
- ❌ Do NOT give flat task lists without decomposition
- ❌ Do NOT block all work waiting for one fork clarification
- ❌ Do NOT accept subagent output without verification against criteria
- ❌ Do NOT re-explain context that should be in project-scoped memory
- ✅ DO decompose first, then prioritize
- ✅ DO queue forks and continue independent work
- ✅ DO verify everything against acceptance criteria
- ✅ DO persist project-specific learnings

## Verification Steps
When you finish a work session using this skill, verify:
[ ] Goal was decomposed into stages + subtasks + DAG (not a flat list)
[ ] Acceptance criteria attached to each subtask leaf
[ ] Any forks were queued and independent work continued
[ ] All completed work was verified against acceptance criteria
[ ] Project-scoped preferences were updated for future sessions
[ ] No re-explaining of known context occurred

## Connection to Organism Architecture
This skill implements the prefrontal executive function (dlPFC + Salience Network + OFC) as an application layer that orchestrates existing cognitive engines:
- Decompose → Luria-executive (when available)
- Dispatch → Thalamus/Mountcastle (routing)
- Fork queue → Sridharan (salience/interrupt)
- Review → Luria-executive + Damasio (evaluation)
- Consolidate → Scoville (episodic memory)
Works with local fallbacks when engines are not yet built.

## Connection to Physics Layer
The work spine (`the operator agent-work-spine.py`) has a `compute_physics()` function
(line ~462) that feeds subtasks into Quartz's lattice engine, then runs
project-level free energy, critical path, stress/strain, critical slowing,
and the quantum layer (superposition, entanglement, tunneling, coherence).

The current CLI exposes `--goal`, `--status`, `--kanban`, `--forks`, `--health`.
Physics is invoked programmatically via `compute_physics(project)` or
verified across all projects using the probe script:
`scripts/verify_physics_on_projects.py` in the
`physics-informed-project-management` skill.

## Example Usage
For goal "Ship 8D Sleep MVP":
1. Decompose: Setup (scope, deps) → Core (algorithm) → Integration (thalamus wiring) → Validation (acceptance criteria, brand check) → Ship (final review, memory encode)
2. Dispatch ready subtasks (those with no deps) immediately
3. If Validation subtask forks on "what are the exact acceptance criteria?", queue that question and continue Core and Integration work
4. Review each completed subtask against its criteria before marking APPROVED
5. Encode outcome learnings to help future similar projects (e.g., "WAVE-COACHING")