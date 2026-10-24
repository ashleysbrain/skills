# Todo Entry Examples

## Good Todo Entries

These examples show clear, actionable todo entries with full context.

### Social Media Content
```json
{
  "id": "linkedin-content-week-1",
  "content": "Generate LinkedIn content batch (8-10 posts) for next week: AI modeled on human biology, 8D wellness, health-tech alignment. Read positioning docs from /<workspace>, deliver as PDF with post text, cadence recommendations, image concepts.",
  "status": "pending"
}
```

### Overnight Build
```json
{
  "id": "overnight-wave-engine-phase2",
  "content": "Build Wave Engine Phase 2: SDT, TTM, Flow science layers with full pytest suite. Physics fidelity target: 8/10. Deliverable: working Python in src/ with passing tests, not docs.",
  "status": "pending"
}
```

### Cron Job Debug
```json
{
  "id": "debug-10pm-2am-cron-jobs",
  "content": "Debug the 10pm and 2am cron jobs showing 'scheduled' status but no actual output. Check cron logs, verify script execution, test manually if needed.",
  "status": "pending"
}
```

### Marketing Deliverable
```json
{
  "id": "your-org-brief-pdf",
  "content": "Create principal brief PDF for Divinity Science: 8D360 unified scoring pipeline, health scoring daily pipeline, proprietary TWC formula. Include: methodology summary, current metrics, improvement recommendations. Format: Da Vinci PDF with proper branding.",
  "status": "pending"
}
```

## Bad Todo Entries

These are examples of what NOT to do.

### Too Vague
```json
{
  "id": "linkedin-posts",
  "content": "LinkedIn posts",
  "status": "pending"
}
```

**Problem**: No scope, no constraints, no deliverable format.

### Missing Context
```json
{
  "id": "check-cron",
  "content": "Check cron jobs",
  "status": "pending"
}
```

**Problem**: Which cron jobs? What to check? What's the expected output?

### No Deliverable
```json
{
  "id": "marketing-task",
  "content": "Marketing",
  "status": "pending"
}
```

**Problem**: What marketing? What's the deliverable?

## Todo Entry Structure

Every todo entry must answer:
1. **What** (verb-object: "Generate X", "Build Y", "Debug Z")
2. **Scope** (how many, which parts, specific dimensions)
3. **Why** (brief justification for why it was deferred)
4. **Constraints** (format requirements, fidelity targets, brand guidelines)
5. **Deliverable** (PDF, working code, markdown, both)
6. **Timeframe** (by when, if applicable)

## When to Use Todo List

Use the todo list when:
- User requests work and you propose deferring it
- Scheduling cron jobs for overnight work
- Multi-turn conversations where you'll return to a task
- User says "let's do this tomorrow" or "handle this later"
- Switching topics before completing current work

## After Task Completion

When you complete a task from the todo list:

1. Mark it as `completed`:
```
todo(todos=[{
  "id": "linkedin-content-week-1",
  "content": "...",
  "status": "completed"
}])
```

2. Deliver the actual output (PDF, working code, etc.) to the user

3. Confirm completion: "Marked todo item 'linkedin-content-week-1' as complete."