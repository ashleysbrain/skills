# Task Planning Product Gap Analysis (2026-08-09)

Session-derived reference for competitive gap analysis of task-management and
weekly-planning products. All data fetched via curl + HTML stripping only
(web_search and web_extract were down with Firecrawl billing errors).

## Products researched (with primary source URLs)

| Product | URL fetched | Key data extracted |
|---------|------------|-------------------|
| Sunsama | sunsama.com | Weekly Objectives, daily planning ritual, shutdown ritual, time blocking, time analytics, multi-tool inbox |
| Motion | usemotion.com | AI auto-scheduling, at-risk prediction, auto-rescheduling, project ETA, capacity balancing |
| Reclaim.ai | reclaim.ai | AI Habits, AI Focus Time, AI Buffer Time, Deep Work Index, AI Agent Library |
| Linear | linear.app, linear.app/features | Cycles, Triage Intelligence, agent dual-lane, Initiatives, Pulse, Loops |
| OmniFocus | omnigroup.com/omnifocus | Custom Perspectives, Review system, Defer-until dates, sequential/parallel projects, nested tags |
| Things 3 | culturedcode.com/things | Projects + Areas, checklists, tags, Today/Upcoming/Anytime views |
| Akiflow | akiflow.com | Universal Inbox, Cmd+K, Smart Time Slots, Daily Rituals, AI Sidekick |
| Routine | routine.co | Universal inbox, quick capture hotkey, time blocking, labels/priorities/projects, AI agents, custom data model |
| Taskwarrior | taskwarrior.org/docs/urgency/, /hooks/ | Urgency formula (12+ coefficients), dependencies, hooks (on-add/on-modify), context filters, special tags |
| 12 Week Year | 12weekyear.com | 12-week cycles, weekly execution scoring |
| GTD | gettingthingsdone.com | 3-phase Weekly Review (Get Clear / Get Current / Get Creative) |

## Gap analysis output structure (reusable)

For a competitive feature gap analysis, this structure worked well:

1. **Per-product feature tables** — each product gets a table: `# | Feature | We Have It?`
2. **Top 3 gaps per product** — distilled from the table
3. **Consolidated ranked gap list** — all gaps merged, ranked by impact on the specific goal
4. **Tier system** — CRITICAL / HIGH IMPACT / DIFFERENTIATING / NICE TO HAVE
5. **Each gap entry**: name, why it matters, best product doing it, difficulty (easy/medium/hard)
6. **Implementation phases** — group gaps into buildable phases (Foundation → Workflow → Intelligence → Polish)

## Key reusable technique: batching curl calls

Multiple product pages fetched in a single terminal call using a `for` loop.
This is more efficient than one call per page and avoids context-window
flooding. See the batch-fetch pattern in the SKILL.md technique #3.

## Weekly review frameworks captured

- **GTD Weekly Review**: 3 phases — Get Clear (process inbox to zero), Get Current
  (review all lists, ensure every project has a next action), Get Creative
  (someday/maybe review)
- **Full Focus Planner (Hyatt)**: 5 steps — review results, review notes/calendar
  2-4 weeks ahead, process email, review goals/projects, set Weekly Big 3
- **Covey Weekly Compass**: Roles (5-7) → big rocks per role → schedule big rocks first
- **12 Week Year (Moran)**: Compress annual goals to 12-week cycles, weekly
  execution scoring (% completion)

## AI-agent dual-lane pattern (from Linear/Reclaim/Routine)

The emerging industry pattern for human+AI task management:
1. Same task surface, different assignee types
2. Agent-specific velocity analytics
3. Recurring agent loops (agents own repeating patterns)
4. Agent-initiated task creation
5. Triage layer (auto-route to human or agent)

## Taskwarrior urgency formula (reference values)

Default coefficients from taskwarrior.org/docs/urgency/:
- +next tag: 15.0
- due date proximity: 12.0
- blocking other tasks: 8.0
- high priority: 6.0
- scheduled: 5.0
- active: 4.0
- medium priority: 3.9
- age: 2.0
- low priority: 1.8
- annotations/tags/project: 1.0 each
- waiting: -3.0
- blocked: -5.0

This transparent, configurable polynomial is a strong model for any
urgency-based task sorting system.
