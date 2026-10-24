# Calendar-Task-Lattice: Feature Gap Analysis
## What World-Class Planning Systems Offer That We Lack

**Research date:** 2026-08-09
**Goal:** Identify missing features for a founder planning their week with an AI organism.
**Method:** Direct extraction from product websites/docs via curl (web search tool was down).

Source: subagent research (deleg_d7e113d5), written to
`/<workspace>`.

## Consolidated Gap Analysis — RANKED by Impact

### TIER 1: CRITICAL

| Rank | Gap | Why It Matters | Best Product | Difficulty |
|------|-----|---------------|-------------|------------|
| 1 | **Projects / Task Grouping** | Without projects, tasks are flat. Can't see "what needs to happen for the raise" vs "the launch." Every competitor has this. | Things 3, Linear (Initiatives>Projects>Issues), OmniFocus | MEDIUM |
| 2 | **Weekly Review Ritual** | #1 differentiator of Sunsama. Core of GTD, Full Focus, 12 Week Year. A founder without a review ritual is flying blind. | Sunsama (guided ritual), GTD (3-phase), Full Focus (Big 3) | MEDIUM |
| 3 | **Tags / Labels** | Multi-dimensional classification. OmniFocus uses tags for energy/context/person. Taskwarrior tags modify urgency. | OmniFocus, Taskwarrior (special tags), Things 3 | EASY |
| 4 | **Time Blocking** | Core of Sunsama, Motion, Akiflow. Tasks exist in a list but never committed to actual time. | Sunsama (drag-to-calendar), Motion (auto) | MEDIUM-HARD |
| 5 | **Dependencies (blocks/blocked-by)** | Critical path management = physics-informed PM. Taskwarrior: blocking +8.0, blocked -5.0. | Taskwarrior, Linear, Motion | MEDIUM |

### TIER 2: HIGH IMPACT

| Rank | Gap | Why It Matters | Best Product | Difficulty |
|------|-----|---------------|-------------|------------|
| 6 | **Subtasks / Checklists** | Complex tasks become unwieldy without nesting. | Things 3, Todoist, TickTick | EASY |
| 7 | **Weekly Objectives / Big 3** | Shows WHY not just WHAT. | Sunsama, Full Focus Planner | EASY |
| 8 | **Defer-Until Dates** | Hide tasks until relevant. Reduces overwhelm. | OmniFocus | EASY |
| 9 | **Recurring Tasks** | Standing tasks shouldn't need manual recreation. | Reclaim (AI Habits), Things 3 | EASY |
| 10 | **Advanced Search / Saved Views** | OmniFocus Perspectives = saved filter presets. | OmniFocus, Linear, Taskwarrior | MEDIUM |
| 11 | **Capacity / Overload Detection** | "You have 40hrs of tasks but 25hrs available." | Motion, Reclaim | MEDIUM |

### TIER 3: DIFFERENTIATING

| Rank | Gap | Why It Matters | Best Product | Difficulty |
|------|-----|---------------|-------------|------------|
| 12 | **Agent Execution Loop** | "route: AI" is a label not a workflow. Agents should pick up tasks. | Linear (agent assignees, loops) | HARD |
| 13 | **Task Duration Estimates** | Input to time blocking, capacity detection. | Motion, Reclaim | EASY |
| 14 | **Configurable Urgency Formula** | Physics-informed system should let you tune coefficients. | Taskwarrior | MEDIUM |
| 15 | **Command Bar (Cmd+K)** | Keyboard speed. | Akiflow, Linear, Routine | MEDIUM |

## Taskwarrior Urgency Coefficients (reference)

Transparent, configurable formula from taskwarrior.org/docs/urgency/:
- urgency.user.tag.next: 15.0 (+next tag)
- urgency.due: 12.0 (overdue or near due date)
- urgency.blocking: 8.0 (blocking other tasks)
- urgency.uda.priority.H: 6.0 (high Priority)
- urgency.scheduled: 5.0 (scheduled tasks)
- urgency.active: 4.0 (already started)
- urgency.uda.priority.M: 3.9 (medium Priority)
- urgency.age: 2.0 (task age)
- urgency.uda.priority.L: 1.8 (low Priority)
- urgency.annotations: 1.0, urgency.tags: 1.0, urgency.project: 1.0
- urgency.waiting: -3.0, urgency.blocked: -5.0

## Weekly Review Frameworks

- **GTD (David Allen)**: 3-phase — Get Clear (process inbox to zero), Get Current (review lists, ensure next actions), Get Creative (someday/maybe)
- **Full Focus (Michael Hyatt)**: 5-part — Review what worked/didn't, Review calendar 2-4 weeks ahead, Process email to zero, Review goals, Set Weekly Big 3
- **Weekly Compass (Stephen Covey)**: Define 5-7 life roles, choose 1-2 big rocks per role, schedule big rocks first
- **12 Week Year (Brian Moran)**: Compress annual goals into 12-week cycles with weekly execution scoring

## Implementation Priority (from research)

### Phase 1: Foundation
1. Projects (MEDIUM) — **DONE** (metadata.project grouping in Lattice)
2. Tags/Labels (EASY) — **DONE** (metadata.tags display + editing)
3. Subtasks (EASY)
4. Defer-until dates (EASY)
5. Recurring tasks (EASY)
6. Task duration estimates (EASY) — **DONE** (metadata.duration_min)

### Phase 2: Planning Workflow
7. Weekly Review ritual (MEDIUM)
8. Weekly Objectives / Big 3 (EASY)
9. Time blocking (MEDIUM-HARD)
10. Dependencies (MEDIUM)
11. Advanced search / saved views (MEDIUM)

### Phase 3: Intelligence
12. Capacity / overload detection (MEDIUM)
13. Configurable urgency formula (MEDIUM)
14. Agent execution loop (HARD)
15. Command bar (MEDIUM)
