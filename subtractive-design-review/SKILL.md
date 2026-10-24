---
name: subtractive-design-review
category: creative
description: Audit and cut non-essential dashboard elements.
version: 1.0.0
author: the operator agent Agent
license: MIT
metadata:
  hermes:
    tags: [ux, dashboard, research, subtraction, qa]
---

# Subtractive Design Review

Use this skill when reviewing human-facing surfaces — dashboards, workspaces, research studios — where your instinct is to ADD. This skill forces you to SUBTRACT first. More is not better.

## Trigger Conditions
- User says "there's too much here" or "this is cluttered" or "what am I actually supposed to use?"
- User rejects your additive approach: "you just added X, you didn't review and surgically edit"
- A surface has accumulated features across multiple passes without a fresh coherence pass
- The principal says "we need fun, not warehouse counts" or "this isn't exciting"

## When to Use
- Before releasing a new dashboard or workspace version that has accumulated features
- When you or a user feels a surface has become cluttered or confusing
- After any major feature pass (e.g., adding momentum analytics, new cards) — review the whole surface, not just what was added
- When metrics are inventory counts rather than human stories (the principal's "the numbers don't add up" signal)

## Core Philosophy

**Three questions for every element:**
1. Does a human make a decision from this right now?
2. Does this tell a human something new and actionable?
3. Does this repeat what another element already says?

If the answer is NO to all three, CUT IT.

## Subtractive Audit Workflow

### Step 1: Full Inventory
List EVERY element a human sees — not just what's added in this pass. Use a systematic extraction:
- Metric values and their labels
- Cards (name, value, sub-text)
- Chips, badges, status indicators
- Buttons and primary CTAs
- Hero text and descriptions
- Section headers and cards

For the Writing Studio dashboard (as a canonical example), the inventory revealed:
- 4 metric cards (Pipeline Output, Evidence, Searches, Run Status)
- Momentum strip with 5 chips
- Pipeline bar ("15-stage pipeline ready | 0 runs")
- Hero title+description
- Intelligent Discovery card
- Recent Activity section
- Trending Topics card
- 3 primary CTAs (Brainstorm, Browse Topics, Recommendations)

### Step 2: Consumption Audit
Judge each element against the three questions:

| Element | Live value | Decision | Reason |
|---------|-----------|----------|--------|
| Pipeline Output | 20 runs | KEEP | Tells human whether pipeline is running and what completed |
| Evidence | 1,305 papers "Papers cached" | CUT LABEL | Warehouse count, not motion; humans don't act on "cached" |
| Searches | 430 queries | CUT | Inventory count; no actionable story |
| Run Status | 0 REVIEW | CUT | Duplicate of Pipeline Output; engineering detail at this volume |
| Pipeline bar | "15-stage pipeline ready | 0 runs" | CUT | Engineering detail, contradicts card above it |
| Hero copy | "A unified research pipeline..." | REWRITE | Describes the machine, not the human's day |
| Momentum chips | +52 papers today ▼377, 7-day streak, 1305 this week, 58.2% cutting-edge, 3 workbench moves | CUT 2 | "this week" repeats Evidence; "workbench moves" noise at current volume |

### Step 3: Surgical Cuts
Apply cuts directly to the baseline file. Do NOT rebuild from memory.

- **Cut metric cards 3+4**: Delete the full `<div class="dash-metric m-topics">` and `<div class="dash-metric m-inst">` blocks. Do not remove only the text — remove the entire card structure.
- **Cut the pipeline bar**: Delete the entire div with "15-stage pipeline ready | 0 runs" text.
- **Cut momentum chips**: Delete the lines in `_paintMomentumStrip` that push "this week" and "workbench moves" chips.
- **Simplify hero**: Change "A unified research pipeline grounded in a living knowledge base" → "What's moving in your research today."

### Step 4: Dead Code Cleanup
After cutting UI elements, remove the JS that writes to them:

- Remove dead card-writers from `paintMetrics` (the blocks that write `mTopics`, `mTopicsSub`, `mAttention`, `mAttAlert`, `mAttSub`).
- Remove the pipeline bar JS that writes `vRuns` and `vFill`.
- Remove orphaned drill handler references (`drillSearches`, `drillAttention`) if their DOM targets are gone.

### Step 5: Verify the Baseline
- Count the metric card divs: should be 2, not 4.
- Count `parts.push` calls in momentum painter: should be 3, not 5.
- Verify the rendered text (strip tags): no "Run Status", no "Searches", no "15-stage pipeline".
- Verify the hero text has the human-first revision.

## Pitfalls

### Pitfall 1: Layering Without Auditing
**Symptom**: You add new features (chips, cards, buttons) without reviewing what already exists.
**User signal**: "you just added buttons, you didn't review and surgically edit for human consumption."
**Fix**: ALWAYS run the full inventory before adding anything. The subtractive audit comes first.

### Pitfall 2: Partial Cuts
**Symptom**: You remove only the text label but leave the card div, button, or JS writer.
**Result**: Ghost elements that occupy space, show "0", or throw console errors.
**Fix**: Delete the ENTIRE block from the opening tag to the closing tag. Use depth counting to find the matching `</div>`.

### Pitfall 3: Inventory Numbers as Human Stories
**Symptom**: Surface counts like "1,305 papers cached" or "430 queries" as primary metrics.
**User signal**: "the numbers don't add up in my brain... they aren't exciting and don't help me feel accomplished."
**Fix**: Count as human stories, not warehouse size. Replace with:
- Velocity: "+52 papers today" (with delta arrow)
- Freshness: "58.2% cutting-edge finds (2025+)"
- Streak: "7-day research streak"
- Never show absolute inventory without a delta or freshness context.

### Pitfall 4: Engineering Details in Human-Facing Surfaces
**Symptom**: "15-stage pipeline ready | 0 runs", "Run Status: 0 REVIEW", or detailed state machine visualization.
**Fix**: These belong in admin surfaces or debug logs. The human-facing surface shows:
- Running count (simple)
- Completed count
- Any blocking item (e.g., "1 REVIEW" - but only when > 0)
- Remove when zero.

### Pitfall 5: JS-Only Cuts Without DOM Verification
**Symptom**: You remove the JS writer but the HTML element remains.
**Result**: The element renders with its static "0" or "Loading..." text forever.
**Fix**: Delete both. Verify the element is gone by searching for its unique class or ID in the rendered HTML.

## Examples

### Dashboard After Subtraction
**Before**: 4 metric cards, pipeline bar, 5 momentum chips, hero describing the machine
**After**: 2 metric cards, 3 momentum chips, hero speaking to the human

**Elements humans actually see and use:**
- 2 metric cards: Pipeline Output (runs), Evidence Library (pools/sources)
- 3 momentum chips: today's paper delta (▲/▼), research streak, cutting-edge finds
- Intelligent Discovery card (discovered fields)
- Recent Activity (work trail)
- Trending Topics (actionable: click to write/build)
- Primary CTAs: Brainstorm, Browse Topics, Recommendations

### Momentum Analytics Subtraction
**Before**: Inventory counts (papers_cached, queries_searched), warehouse-averaged freshness (3.7% over all 1,305 papers including 2021-2023 stock)
**After**: Velocity metrics (papers_today vs yesterday, 7d total), discovery freshness (scan-engine 58.2% over recent finds), streak, workbench moves

The subtraction answered the user's question: "the numbers don't add up... they aren't exciting and don't help me feel accomplished."

## Verification Checklist

- [ ] Inventory extracted for the entire surface (not just new elements)
- [ ] Every element judged against the three questions
- [ ] Full blocks removed, not partial text-only cuts
- [ ] Dead JS writers deleted alongside their DOM targets
- [ ] Metric/value counts verified (e.g., 2 cards, 3 chips)
- [ ] Rendered text stripped of tags to confirm deletion
- [ ] No orphan references in drill handlers or paint functions
- [ ] Hero copy speaks human-first, not machine-first

## References

### Session-Specific Transcripts
- `writing-studio.html` — baseline and subtracted state (Writing Studio dashboard)
- `pipeline_api.py` — momentum analytics endpoint (`/api/stats/momentum`) with discovery freshness metric
- `audit/QA-PASS-15-2026-08-18.md` — run record of the subtractive design pass

### External Sources
- Don Norman: "Good design is actually invisible" — if people notice the design, you've already lost
- John Maeda: "Simplicity is about subtracting the obvious and adding the meaningful" — the subtractive philosophy
- Baseline-First Surgical Precision skill — the discipline of patching the baseline rather than rebuilding

## Related Skills

- `baseline-first-surgical-precision` — ensures you patch the actual file, not memory
- `design-advisory-board-review` — for structured multi-advisor design feedback (use when you need elite design voices)