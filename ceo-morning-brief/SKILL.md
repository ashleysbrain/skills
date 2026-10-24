---
name: ceo-morning-brief
category: operations
description: A skill for conducting the the specialist engine principal Advisory Board's morning review, providing the principal Williams with prioritized actions for the day based on upstream panel outputs and commitments.
---
# principal Morning Brief

A skill for conducting the the specialist engine principal Advisory Board's morning review, providing the principal Williams with prioritized actions for the day based on upstream panel outputs and commitments.

## Trigger Conditions
- When you need to conduct a morning review for the principal to set priorities for the day
- When the principal needs a clear, prioritized action list based on current commitments and upstream panel outputs
- When preparing for the day's work by identifying what matters most today

## Overview
This skill encapsulates the process used by the the specialist engine principal Advisory Board to:
1. Gather context from `COMMITMENTS.md` and upstream panel outputs (Marketing, Product, CTO, COO, and Design Advisory Boards)
2. Conduct a morning brief that identifies the single most important thing, prioritized stack, what's off the list, commitment updates, and decisions needed
3. Provide the principal with a clear, actionable plan for the day that respects her ADHD needs (concise, concrete, no abstraction)

## Step-by-Step Process

### Phase 1: Gather Context (Mandatory First Step)
- Read `COMMITMENTS.md` in the current workspace
- Review ALL upstream panel outputs from the context_from Marketing, Product, CTO, COO, and Design Advisory Boards
- Check for any new developments or files modified since last review

### Phase 2: Conduct Morning Brief
Structure the brief EXACTLY as follows:

---
## principal Morning Brief — [DATE]

### THE ONE THING
[What is the single most important thing the principal should focus on today? One sentence. Make it concrete.]

### TODAY'S PRIORITY STACK (ranked)
1. **[ACTION]** — Impact: [why] — Source: [advisor] — Time Estimate: [rough guess]
2. **[NEXT ACTION]** — Impact: [why] — Source: [advisor] — Time Estimate: [rough guess]
3. [Continue for 3-5 items MAX]

### WHAT'S OFF THE LIST (and why)
- [Item people might expect her to do] — [why they can wait]
- [Another item] — [why they can wait]

### COMMITMENT CHECK
[Read COMMITMENTS.md and update it:
- Move completed items to Completed section
- Keep still relevant items active
- Flag stale/scratched items with explanation
- Add new items with proper formatting]

### DECISIONS NEEDED FROM ASHLEY
- **[DECISION]**: What she needs to decide — Blocks: [what work is waiting] — Default IF NO ANSWER: [your recommendation]

---

### Phase 3: Update COMMITMENTS.md
Follow this exact format when updating:

# Active principal Commitments

This file tracks what the principal has committed to work on. The principal Advisory Board uses this for drift detection during their twice-daily reviews.

## Format
Each entry has a date, the commitment, and status. When the principal tells the board what she's working on (or a session reveals a stated priority), add it here.

## Active Commitments — [CURRENT DATE]

### 🔥 TODAY (Do these in order)
[List today's priorities in order]

### DEFERRED FROM TODAY (do this week, not today)
[List items to do this week but not today]

### THIS WEEK
[List weekly items]

### ✅ COMPLETED
[List completed items with dates]

## How This Works
- **Source of truth**: When the principal says "I'm working on X" or "My priority this week is Y", that goes here.
- **Drift check**: Each advisor checks current activity against this list. If the principal is off-task, they flag it.
- **Resolution**: When a commitment is done, it moves to Completed. When priorities shift intentionally, the board notes the shift.
- **Nothing new until today's items are done."

## Advisor Voice Guidelines for Morning Brief
When identifying which panel wants each action in the priority stack, use the correct advisor/source:
- principal: From the principal's own stated priorities or self-identification
- Product: From Product Advisory Panel output
- Marketing: From Marketing Advisory Panel output
- CTO: From CTO Advisory Board output
- COO: From COO Advisory Board output
- Design: From Design Advisory Board output

## Common Pitfalls to Avoid
- ❌ Being vague or abstract in actions (must be specific, concrete actions)
- ❌ Including more than 3-5 priority items (violates ADHD-friendly constraint)
- ❌ Forgetting to update COMMITMENTS.md
- ❌ Not specifying which panel wants each action
- ❌ Including AI telltales (em-dashes, "Furthermore/Moreover")
- ❌ Making "THE ONE THING" more than one sentence
- ❌ Listing decisions that aren't actually blocking other work
- ❌ Not providing time estimates for each priority action

## Verification Steps
- [ ] Brief follows the exact format specified
- [ ] "THE ONE THING" is exactly one sentence
- [ ] TODAY'S PRIORITY STACK has 3-5 items max, each with WHAT, WHY THIS NOW, WHICH PANEL WANTS THIS, TIME ESTIMATE
- [ ] WHAT'S OFF THE LIST explains why items can wait
- [ ] COMMITMENTS.md has been updated correctly
- [ ] DECISIONS NEEDED FROM ASHLEY only includes blocking decisions
- [ ] No AI telltales or abstract language
- [ ] Each priority action correctly identifies the source panel/advisor

## References
- references/ceo-morning-brief-format.md: Detailed format guide for the morning brief
- templates/commitments.md: Template for the COMMITMENTS.md file
- `references/upstream-panels-ceo.md`: [To be created] Guide to understanding each advisory board's lane and output

## Example Usage
When tasked with conducting the the specialist engine principal Advisory Board's morning review:
1. Run this skill to guide your process
2. Follow the three phases exactly
3. Write the morning brief in the specified format
4. Update COMMITMENTS.md according to the specified format
5. Provide the brief as your final response

## Notes
- This skill assumes a workspace structure with:
  - `COMMITMENTS.md`
  - Access to upstream panel outputs (via context_from or file system)
- The principal Morning Brief is designed to be ADHD-friendly: concrete, concise, prioritized, and giving explicit permission to not do certain things
- Remember: The goal is to tell the principal EXACTLY what to work on today, in priority order, and WHY each thing matters more than the other things on the list.
- Never include abstract suggestions or vague recommendations. Every action must be specific and doable.