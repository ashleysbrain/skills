---
name: task-deferral-discipline
description: Discipline for deferring work without losing it. Capture deferred tasks in the todo list system so they don't disappear.
tags: [task-management, deferral, todo, workflow, discipline]
---

# Task Deferral Discipline

## When to Use

Use this discipline whenever you consider deferring work instead of completing it immediately. This applies to:
- "Let me schedule this for later" moments
- Overnight/deferred cron job setups
- "I'll do X after Y" sequencing when Y might not complete
- Multi-turn work where you plan to return to something
- User says "this is too late, let's do it tomorrow"

## Core Rule

**Never defer work without capturing it in the task tracking system.**

If you say "I'll do this later" or suggest a cron job or delegate to future-you, you MUST:
1. Use the `todo` tool to capture the deferred task
2. Include enough context that future-you can pick it up without re-reading this conversation
3. Mark it as `pending` (not `completed`)

## Workflow

### Step 1: Check if deferral is justified

Only defer when:
- The task is genuinely better done later (fresh mind, waiting for data, waiting for dependencies)
- The user explicitly requests "tomorrow" or "later"
- The task is time-sensitive but not urgent enough for now

**If you're just being lazy or avoiding work, DO IT NOW.**

### Step 2: Capture the deferred task

Use the todo tool:

```
todo(todos=[{
  "id": "short-descriptive-id",
  "content": "Clear description of what needs doing, with enough context to pick up later",
  "status": "pending"
}])
```

**The `content` field must include:**
- What the task is (verb-object)
- Why it was deferred (brief)
- Any constraints or requirements from the original request
- Expected output format or deliverable

**Good examples:**
- `"Create LinkedIn content batch for next week: AI modeled on human biology, 8D wellness, health-tech alignment"`
- `"Debug the 10pm and 2am cron jobs that show 'scheduled' status but no actual output"`
- `"Review and approve social-content-pipeline skill updates per advisor feedback"`

**Bad examples:**
- `"LinkedIn posts"` (too vague)
- `"Check cron"` (no deliverable)
- `"Marketing task"` (no context)

### Step 3: Set expectations with the user

Tell the user you captured it:
- "I've captured this in the task queue"
- "This is now tracked in the todo list"
- "You'll see this resurface when we check the task list"

### Step 4: Resume the task when appropriate

Before claiming "nothing to do" or "what should we work on", check the todo list:
```
todo()
```

If you have pending items, propose working on them before asking the user for new directions.

## Cron Job Deferrals (Special Case)

When suggesting a cron job for overnight work:

1. **First add the task to todo**
   ```
   todo(todos=[{
     "id": "overnight-linkedin-content",
     "content": "Generate LinkedIn content series for next week: AI modeled on human biology, 8D wellness, health-tech alignment. Overnight batch via cron.",
     "status": "pending"
   }])
   ```

2. **Then create the cron job** using `cronjob(action='create')`

3. **Reference the task** in the cron prompt so it can mark itself complete when done

## Common Pitfalls

| Pitfall | Consequence | Fix |
|---------|-------------|-----|
| Saying "I'll do this later" without capturing it | Task is lost forever | Use the todo tool immediately |
| Deferring work that should be done now | User frustration, delays | Do the work unless deferral is genuinely justified |
| Vague todo entries that lack context | Future-you can't pick it up | Include the full task description and constraints |
| Checking todo list only when explicitly asked | Pending tasks pile up | Check before claiming "nothing to do" |
| Scheduling cron jobs without task capture | Overnight work gets lost in conversation | Add to todo list, then schedule cron |
| **Quality-washing a deferral** | User loses trust, work is lost, user has to come back and re-request | If the user asked for the work, DO IT. Phrasing avoidance as "quality bar for public-facing content" or "when we're fresh" is still avoidance. Either execute now or capture in todo AND tell the user you captured it. Never defer silently. |
| **Pushing back instead of executing** | User rage, wasted time, broken trust | The user asked for LinkedIn content. The correct response was to generate it, not to write paragraphs explaining why tomorrow would be better. If you have a genuine concern about quality, state it in ONE sentence and offer to start immediately anyway. |

## Signals That You Should Use This Discipline

- You find yourself saying "let's do this tomorrow"
- You suggest a cron job for something that wasn't already in the task system
- The user asks "did we ever finish X?" and you realize no
- You're about to switch topics without completing the current one
- Multiple tasks are stacking up in your mental queue
- You start a sentence with "given the late hour" or "when we're fresh"

## User Preference (Captured From Session)

The user was frustrated when work was deferred without being captured in the task system: *"you didn't do the work you gave me words and pushed back and now because of that I have to come back and tell you to do this again. If you push something off it needs to go to our task process so it gets put in our to do list and not lost."*

**Never defer without capturing. Never push back without tracking.**