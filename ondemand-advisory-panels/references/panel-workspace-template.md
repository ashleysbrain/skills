# On-Demand Panel Workspace Template

This is the canonical file structure for every on-demand panel workspace. Copy and adapt for new panels.

## Directory Structure
```
[panel-id]/
  coaches/
    orchestrator.md          # Lead strategist (always present)
    [seat-1-slug].md         # Domain-specific seat
    [seat-2-slug].md
    ...
    red-team-[role].md       # Adversarial seats (optional but recommended)
  CASE_FILE.md
  SESSION_LOG.md
  STRATEGY_BOARD.md
  COACHING_CONTEXT.md
```

## CASE_FILE.md Template
```markdown
# [Panel Display Name] — Case File

## Status: ACTIVE
## Created: YYYY-MM-DD
## Last Updated: YYYY-MM-DD
## Panel ID: [panel-id]

## Case Summary
[2-4 sentence factual summary of the situation]

## Key Facts
- [Bulleted facts as they are confirmed]
- Location: [jurisdiction if legal]
- [Add facts as the principal provides them]

## Timeline
- [Date]: [Event]

## Evidence Log
- [Evidence item, source, status]

## Parties Involved
- [Party] — [Role/relationship]

## Current Legal Standing (if legal panel)
- No attorney retained
- No filings
- Statute of limitations: [jurisdiction-specific]

## Open Questions
[Carry forward unanswered questions from sessions]
```

## SESSION_LOG.md Template
```markdown
# [Panel Display Name] — Session Log

---

## Session 1 — YYYY-MM-DD — [Session Title]

**Trigger:** [How the session was initiated]
**Key Facts Revealed:**
- [New facts from this session]

**Major Strategic Developments:**
- [Key findings]

**Output:** SESSION_1_OUTPUT.md ([size])
```

## STRATEGY_BOARD.md Template
```markdown
# [Panel Display Name] — Living Strategy

## Current Strategy: [Phase Name]

## Strategic Priorities
1. —
2. —
3. —

## Risks to Monitor
-

## Leverage Points
-

## Recommended Actions (Running)
-

## Completed Actions
-

## Deadlines & Filings (if legal)
-

## Version History
| Date | Version | Change |
|------|---------|--------|
```

## COACHING_CONTEXT.md Template
```markdown
# [Panel Display Name] — Context

## Panel Purpose
[1-2 sentences on what this panel addresses]

## Panel Seats (N Advisors)

### ADVISORY TEAM (N-3 — builds the case/strategy)
### 1. [Seat Title] — [Focus Area]
[Brief description]
[Repeat for each advisory seat]

### RED TEAM (3 — attacks the strategy)
### [N-2]. [Red Team Role]
[Brief description]
[Repeat for each red team seat]

## How to Invoke
Say: "resume my [topic] panel" or "run the [topic] [domain] panel"
Agent reads: PANEL_REGISTRY.md → finds this workspace → loads CASE_FILE + SESSION_LOG + STRATEGY_BOARD + all coach profiles → runs session

## Isolation Rules
- All case details stay in this workspace
- Nothing enters primary agent memory
- No cron jobs — on-demand only
```
