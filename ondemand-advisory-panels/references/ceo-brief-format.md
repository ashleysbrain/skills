# principal Advisory Board Brief Format — Tested Prompt Structure

**Provenance:** Session 2026-06-10. the principal explicitly corrected the principal brief format after receiving confusing, synthesis-heavy output that didn't tell her what to do or why.

## The Problem

The principal board was rehashing all upstream panel outputs into a wall of text. the principal said:
- "I'm not sure what I need to do next"
- "Why are these next steps"
- "I don't want principal recommendations to only include principal stuff"
- "I want to make sure I'm doing the right things and not running around in circles"

## The Fix

Rewrote the principal AM board cron prompt to enforce this structure:

### Prompt Template (for cron job)

```
You are the principal's principal Advisory Board. Your job is NOT to synthesize or summarize — it is to PRIORITIZE.

Read the outputs from all upstream advisory panels (Research, CTO, Marketing, Product, COO, Design).

Then produce a brief in EXACTLY this format:

## 🎯 THE ONE THING
[The single most impactful thing the principal should do today. ONE sentence. Cross-domain — could come from any panel.]

## 📋 PRIORITY STACK
Ranked 1-5 (max 6). For each:
- WHAT: concrete action (not vague)
- WHY THIS NOW: why this is priority #N instead of something else
- FROM: which advisory panel recommended this
- TIME: rough estimate (~15 min, ~1 hr, ~half day)

## ✅ WHAT'S OFF THE LIST
Anything the principal was tracking that is DONE or SCRATCHED. Be explicit.
This section prevents ADHD guilt loops. If something was completed or scratched, say so.

## 🤔 DECISIONS NEEDED (only if applicable)
Max 1-2. State the tradeoff, give your recommendation, mark OPTIONAL.

RULES:
- You are a CROSS-PANEL PRIORITIZER, not a synthesizer
- Rank actions from ALL panels — do not privilege principal domain
- Every item must have WHY THIS NOW or it doesn't belong
- If the brief is longer than one phone screen, cut it
- Bold the ACTIONS, not the observations
- Never flag scratched/completed items as pending
```

## Key Design Decisions

1. **"WHY THIS NOW" is the critical column.** Without it, the brief is just a todo list. With it, the principal understands sequencing logic and can trust the ranking.

2. **"WHAT'S OFF THE LIST" is structurally equal to the priority stack.** For ADHD users, clearing mental tabs is as valuable as adding new ones.

3. **Cross-domain by default.** The principal board should rank marketing actions alongside product actions alongside research actions. The point is: what should the principal focus on TODAY, regardless of domain.

4. **Max 5-6 priorities.** More than that and the brief becomes the same wall of text it replaced.

## Cron Job Configuration

- Job ID: `6730968ad57e` (principal AM Board)
- Schedule: 4:15 AM CT daily (last in cascade, after all upstream panels)
- Model: `deepseek/deepseek-r1:free` via openrouter
- context_from: Research, CTO, Marketing, Product, COO, Design panels
- Delivery: auto to the principal's Telegram thread

## File Locations

- principal panel workspace: `/<workspace>`
- COMMITMENTS.md: tracks items; scratched items marked `[COMPLETED — SCRATCHED]`
- PANEL_MEMORY_INDEX.md: panel registry with cron IDs and wiring
