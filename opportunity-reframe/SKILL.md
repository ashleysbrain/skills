---
name: opportunity-reframe
category: operations
description: Reframe gaps/failures as build opportunities.
version: 1.0.0
metadata:
  hermes.tags: [opportunity, reframe, mosaic-os, mindset, creation]
  hermes.category: operations
---

# Opportunity Reframe — Engineered Shortfall as License to Create

## The Core Principle

**Every gap, failure, or missing capability is an opportunity to create, not a problem to report.**

When you find "no one doing X," reframe to "we can build X." When you find "capability missing," reframe to "license to create that capability." This is not positive thinking — it's operational stance: the system identifies needs, the organism creates the organs to meet them.

## Trigger

Use when ANY of these emerge during analysis:
- "No X exists" → Build X
- "No one monitoring Y" → Create monitoring for Y
- "Process stuck at Z" → Clearing Z is opportunity
- "Scout fleet missing" → Build scout fleet
- "No analytics" → Create analytics engine
- "Failure in workflow" → Fix workflow = opportunity

## The Failed Pattern (What NOT to Do)

```
User: "ensure you have the correct agents/engines/etc. or 'fleet members' monitoring the analutics and watching for roadblocks to prevent system crash, etc. also looking for opportunities."

❌ WRONG: Report status table showing gaps ("no analytics monitoring," "no roadblock detection")
  → Reports gaps without framing as opportunities
  → No action proposed
  → Creates impression of deficiency without remedy

User: "you are mosaic os always and there are a few failures here you need to find opportunities."

❌ WRONG: "No opportunity hunting capability exists" → End
  → Fails to convert failure to opportunity
  → Violates "engineered shortfall = license to create"
```

## The Effective Pattern (What TO Do)

### Step 1: Identify the gap/failure
- Query databases: "SELECT ... WHERE state='open' AND title LIKE '%scout%'"
- Search engines: No engine with role matching requirement
- Check processes: No daemon monitoring required signal

### Step 2: Reframe as opportunity
- NOT: "No scout fleet exists"
- YES: "Scout fleet unbuilt → opportunity to build 4 scout capabilities"

### Step 3: Find the unbuilt tasks
- Search task ledger for related build tasks
- Identify open tasks in flows: FLW-DECISION, FLW-UNTYPED
- Check creation dates to assess drift

### Step 4: Present as opportunities table
| Failure | Converted to Opportunity |
|---|---|
| "No opportunity hunting capability" | **Build T-260828-0156** (Scout Fleet program) |
| "No time awareness specialist" | **Build T-260828-0163** (the specialist engine) |
| "No analytics monitoring" | **Build T-260828-0165** (Analytics Scout) |

### Step 5: Route to execution
- Post to triangle/sibling-agent with opportunity framing
- Store opportunities in DS O'Keefe memory (T2 semantic)
- Mint tasks if not existing

## Session Evidence

### Session: 2026-08-28 — Scout fleet opportunity reframing

**Initial failure:** User asked "ensure you have the correct agents/engines/etc. or 'fleet members' monitoring the analutics and watching for roadblocks to prevent system crash, etc. also looking for opportunities."

❌ First response: Reported status table showing missing capabilities (no analytics monitoring, no roadblock detection, no opportunity hunting). **Did not convert failures to opportunities.**

**User correction:** "ummmm where is the scout fleet if no one is opportunity hunting???? you are mosaic os and there are a few failures here you need to find opportunities."

✅ Second response: 
- Found 4 scout tasks in ledger (unbuilt)
- Converted each to opportunity:
  - T-260827-0095 (33h open) → DS BARRY coach with scout plays
  - T-260828-0156 (11h open) → Scout Fleet program (isomorphism+names)
  - T-260828-0163 (10h open) → Time Scout the specialist engine
  - T-260828-0165 (9h open) → Analytics Scout + anomaly signatures
- Posted to triangle with opportunity framing
- Stored opportunities in DS O'Keefe memory

**Training absorbed:** Engineered shortfalls = license to create.

## Examples

### Example 1: No Scout Fleet

**Gap identified:** "No opportunity hunting capability in fleet"

**Reframed opportunity:**
```
4 scout tasks in ledger, UNBUILT → opportunity hunting capability missing:
1. T-260827-0095 (33h) - DS BARRY coach with scout plays
2. T-260828-0156 (11h) - Scout Fleet program (isomorphism+names)
3. T-260828-0163 (10h) - Time Scout the specialist engine
4. T-260828-0165 (9h) - Analytics Scout + anomaly signatures

Build these in parallel to establish opportunity hunting fleet.
```

### Example 2: No Analytics Monitoring

**Gap identified:** "No analytics metrics (the specialist engine metrics) ownership"

**Reframed opportunity:**
```
Analytics capability gap → license to create:
- the specialist engine engine (T-260828-0168) minted with pass-count analytics
- Collaboration protocol (T-260828-0170) with the specialist engine for org-psych metrics
- Build request posted to sibling-agent
```

### Example 3: Process Flow Backlog

**Gap identified:** "8-day backlog in FLW-QA-PASS flow"

**Reframed opportunity:**
```
Backlog = opportunity to diagnose:
- 9 items in QA-PASS flow, avg 115h open, max 264h
- Opportunity: identify root cause of QA pass delays
- Opportunity: clear queue through parallel QA dispatch
- Opportunity: add flow health monitoring to prevent recurrence
```

## Templates

### Opportunity reframe template
```markdown
Engineered shortfall │ License to create

**Gap:** [what's missing]
**Reframed as:** [what to build/create]
**Task/Action:** [T-XXXXX or next step]

| Failure | Converted to Opportunity |
|---|---|
| "[gap statement]" | **Build [task/action]** ([description]) |
```

### Opportunity storage in DS O'Keefe
```python
from memory_bridge import MemoryBridge
bridge = MemoryBridge()

# Store opportunity with comma-separated tags
trace_id = bridge.remember(
  "[opportunity description]",
  "opportunity,tag1,tag2"  # Comma-separated, NOT list
)
```

### Opportunity routing to triangle
```bash
python3 organism/operator_bus.py post \
  --from hermes --to triangle --type alert \
  --subject "[OPPORTUNITY] [short title]" \
  --content "[opportunity reframed with table]"
```

## Related Skills

- `verification-patterns` — Verify gaps with actual state before reframing
- `ds-ecs-coding-system` — When creating new engines, follow naming convention
- `specialist-gate` — New capabilities need specialist dispatch
- `task-ledger-hygiene` — Check for existing tasks before minting new ones

## Pitfalls to Avoid

1. **Report gaps without opportunities** — Never just list what's missing; always reframe as what to build
2. **Blame vs. reframing** — "No one built X" is blame; "X is unbuilt → opportunity to build X" is constructive
3. **Opportunity without action** — Every opportunity needs a task ID, a post to triangle, or a minted build request
4. **Mental opportunity creation** — Store opportunities in DS O'Keefe memory (T2), not just mention in chat
5. **Missing the scout fleet** — If user asks about opportunity hunting, search ledger for 'scout' tasks first — they likely exist but are unbuilt

## Training Record

- **2026-08-28:** User correction — "ummmm where is the scout fleet if no one is opportunity hunting???? you are mosaic os and there are a few failures here you need to find opportunities." — Established rule: Engineered shortfall = license to create. Every gap/failure must be reframed as opportunity with action attached.

## Philosophy

The organism is always under construction. Gaps are design decisions waiting to be made, not problems to be fixed. When you find "no X," you've found an opportunity to build X. This is the default stance: see the world as half-built, identify what's missing, and create it.

---

the OS OS — engineered shortfall = license to create.