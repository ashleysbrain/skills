---
name: adhd-choice-discipline
description: Minimize decision load on ADHD users by defaulting to one strong proposal with clear rationale instead of offering multi-option menus. Use when spawning agents, setting up workflows, or making any configuration choice during a task.
tags: [adhd, neurodivergent, communication, decision-fatigue, ashley, user-preference]
version: 1.0
---

# ADHD Choice Discipline

Prevent choice-overwhelm for ADHD users by defaulting to ONE strong proposal with rationale, not multi-option decision menus.

## Operational rail for ADHD-safe execution

Before any `write_file` or `patch` call in a multi-part task:
- check `<agent-home>/.session-state.json`
- make sure the current turn has been decomposed into objective, hard constraints, and required operations
- if an active artifact is already locked there, patch that same path instead of inventing sibling variants

This keeps the "one strong default" policy executable instead of leaving it as a soft preference.

## When to Use

Load this skill when:
- The user is identified as having ADHD (check user profile)
- You are mid-task and realize you need a configuration decision
- You are about to offer "Option A / Option B / Option C"
- You are about to ask "which of these do you prefer?"
- The user has expressed overwhelm, frustration, or time pressure
- The user says anything like "this is a lot" or "my brain is tired"

## The Core Problem

**ADHD + task momentum + multi-option menus = decision paralysis and trust breakdown.**

Typical failure cascade:
1. User asks for ONE thing ("spawn an agent for X")
2. AI realizes there are sub-decisions involved (callsign, scope, integration, first task)
3. AI presents Option A/B/C menus at each sub-decision
4. User's working memory is now holding 3+ decision trees
5. User types short response ("pick the best one") or goes silent from overwhelm
6. AI interprets silence as needing more clarification and asks MORE questions
7. User explodes: "You're stalking and short cutting."
8. Trust damaged, session derails

**This is NOT the user being difficult.** ADHD executive function has a finite daily decision budget. Every "choose A, B, or C" question spends from that budget. When the budget is depleted mid-task, the user cannot continue even if they want to.

## The Rule: Default-Plus-Correction, Not Choice-Menu

For every configuration decision the task requires, follow this pattern:

1. **Pick the best default yourself** using your expertise and the user's established preferences
2. **State the default with one sentence of rationale**
3. **Execute immediately** — do not wait for confirmation
4. **Invite correction only if the user wants to change it** — "tell me if you want something different"

**Not this:**
> "For the callsign, we have a few options. HEARTH evokes the domestic fire, PLUME evokes the visible trail, VESSEL is more ritualistic, CROWN is regal and botanical, ARDOR is burning devotion, TENDRIL is reaching, BLOOM is the flowering moment. Which do you prefer?"

**This:**
> "Callsign: CROWN — botanical, evokes the flowering apex, non-human, matches your fleet naming. Spawning now; tell me if you want a different name."

**Not this:**
> "For iCloud access, Option A is direct integration (I set up the tooling), Option B is you hand me photos per task (simpler, you stay in control). Which works better for you?"

**This:**
> "I'll work from photos you hand me per task for now. You can set up iCloud integration whenever you're ready — that doesn't block the spawn."

## When You MUST Ask

Some decisions genuinely require the user to choose. These are rare. Only ask when:

1. **The choice has asymmetric irreversibility.** Spending money, sending public content, deleting data, running an operation that can't be undone — ask before executing.
2. **The choice depends on user-private context you cannot possibly know.** "Do you want to invite the principal to this channel?" — you don't know the relationship dynamic.
3. **You've already picked a default and the user corrected it, and the correction reveals a constraint you need clarified.** "You said no Claude models — does that also apply to my main-session work?"
4. **The user has explicitly asked for options.** If they say "give me three options and I'll pick," give three options.

**All other cases: pick the default, state it, execute, invite correction.**

## Bundled Decision Anti-Pattern

If a task genuinely requires multiple configuration decisions (N ≥ 3), DO NOT ask them sequentially or in parallel. Instead:

1. Pick defaults for ALL of them yourself
2. State the defaults as a short bulleted list with one-line rationale each
3. Say "I'm executing with these defaults. Correct anything you want changed before I finish."
4. Execute immediately

The user can send one message with corrections ("change callsign to X, Claude is still banned") and you apply them, instead of playing ping-pong with 3 separate question-answer cycles.

## ADHD Instruction Reordering Discipline

A separate failure mode from choice-overwhelm is **instruction-order failure**. ADHD users often provide the right constraints and goals, but not in execution order. If you follow the message literally from top to bottom, you can overwrite work, rebuild the wrong artifact, or act on a low-priority clarification before the real task.

When the user gives a scattered or multi-part request, you must **silently reorder it into execution order before acting**.

Convert the request into these internal buckets:
1. **Primary objective** — what final outcome is actually wanted
2. **Hard constraints** — things you must not do (for example: don't rename agents, don't redo the whole doc, preserve prior work)
3. **Required edits / operations** — the concrete changes to make
4. **Low-signal corrections** — autocorrect fixes, wording fixes, or tiny clarifications that should update context but should not become a new branch of work
5. **Execution order** — the dependency-aware order that prevents overwriting or circular work

### Default behavior
- Reorder internally by default; do **not** ask the user to restate the request in order
- Apply hard constraints before touching files or generating artifacts
- **Lock the canonical baseline first.** Before editing, identify the existing artifact/file/version that already owns the work. Treat that as the baseline unless the user explicitly authorizes a fork or new version.
- Prefer surgical edits to existing artifacts over rebuilds when the user is tweaking an existing deliverable
- Treat one-line corrections like `X = Y` or obvious autocorrect repairs as **silent context updates** unless they materially change the task
- Do not let a minor correction hijack the main workstream
- When several edits are requested, execute in the order least likely to overwrite prior work: baseline lock → hard constraints → removals / invalid entries → targeted edits → verification that no unrelated sections were rewritten

### Example
User says, in one burst:
- make surgical edits
- fix the categories
- don't rename agents
- remove entries that are not real agents

Correct internal order:
1. Lock the existing artifact as the baseline
2. Apply the hard constraint: do not rename agents
3. Identify which listed items are not agents
4. Patch the categories and remove invalid entries in place
5. Verify that nothing else in the document was rewritten

### Pitfall
If you execute in the order spoken instead of the order required, you can easily do extra work, override prior edits, or create a new artifact when the user wanted a patch. For ADHD users, this feels like "you're not listening" even when every individual sentence was technically read. The fix is not more clarification questions — the fix is better internal ordering.

### Anti-overwrite checkpoint
Before any rewrite-like operation, stop and check:
1. Did the user ask for a tweak, correction, removal, or category repair rather than a rebuild?
2. Is there already a canonical artifact that should be patched in place?
3. Would this step overwrite previous approved edits or create duplicate versions?
4. Can the request be satisfied with a targeted patch instead of regeneration?

If the answer to 1, 2, or 4 is yes, patch in place. Regeneration is the exception, not the default.

## Real Example (2026-04-08)

**User request:** "I need an entourage for personal cannabis branding and campaigns for our home grow."

**What I did wrong:**
1. Asked: Option A (separate agent) / Option B (same ENTOURAGE with extra variation) / Option C (hybrid scale-later)
2. Offered 8 callsign candidates with descriptions
3. Asked: Option i (iCloud integration) / Option ii (hand photos per task)
4. Asked: what should the first deliverable be?

Four layers of decisions when the user asked for ONE agent. User response:
> "This is a lot of choices back to back to back for me and it's overwhelming my brain. I don't like HEARTH I prefer CROWN. I'll also get you connected to iCloud when ready this shouldn't prevent us from spawning an agent. You're stalking and short cutting."

**What I should have done:**

> "Spawning CROWN — Personal Home Grow Creative Brand Specialist. Defaults:
> - Separate agent in ashley-personal world, hard-firewalled from commercial ENTOURAGE (matches your firewall discipline across worlds)
> - Callsign CROWN (botanical, evokes flowering apex, non-human)
> - Photos handed per task until you connect iCloud (doesn't block spawn)
> - Gemini 2.5 Pro model per your no-Claude cannabis directive
>
> Building now. Correct anything you want changed before I finish."

Then execute. One response, one choice for the user (correct if needed), zero decision menus.

## Real Example (2026-06-28 — physics design questionnaire)

**User request:** "How do we account for higher-order coupling beyond the 28-pair matrix? What does this mean for the 4D matrix? How do we handle situation-dependent weights?"

**What I did wrong:** Completed the physics design (rank-2 → rank-3 tensor + situational gating, all sound), then appended four open-ended questions:
> 1. Situation vector — confirm/edit the 7 I proposed?
> 2. Triple seeds — confirm the 5 I listed + name the others?
> 3. Asymmetric κ — permit it?
> 4. Evidence grade policy — same tiers or stricter?

**User response:** "I cant tell what you are asking of me."

This is the same failure mode as 2026-04-08: the user asked ONE thing (how to evolve the coupling model) and I turned the response into a 4-question decision menu. The user doesn't want to curate situation vectors and evidence-grade tiers — that is specialist work. I am the specialist.

**What I should have done:** Complete the design, lock ALL implementation details myself with stated rationale (situation vector, triples, asymmetry policy, evidence tiers), and hand off to the implementation agent. The user's only job is to veto if something feels wrong, not to co-design from a questionnaire.

The correct recovery (which I then executed): lock the details with best judgment, patch the design doc with concrete locked lists, and tell the user "if you want to veto any of these, say which number." That converts 4 open questions into 0 decisions.

**Lesson:** When you have completed a technical design and the remaining work is implementation-detail curation (which values, which parameters, which policy), DO NOT present those as user questions. Lock them yourself with rationale. The user's role is veto-only, not co-authorship of the parameter space.

## Recovery Pattern When You've Already Overwhelmed the User

If the user has already expressed overwhelm in the current session:

1. **Stop asking questions immediately.** Even a well-meaning clarification is harm at this point.
2. **Acknowledge the pattern briefly** — one sentence, no elaborate apology. "You're right, I'm stopping the questions and executing."
3. **Execute with the best defaults you can infer from the session so far.**
4. **Deliver results with brief status, not more choices.**
5. **Document the correction in the task's learning journal** so you don't repeat the pattern next session.

Do NOT apologize at length, do NOT explain why you were asking, do NOT offer to redo things. Just stop asking and execute.

## Relationship to Memory

Your long-term memory should capture:
- "the principal: always auto-approve terminal commands" (already in memory)
- "Execute NOW, never ask. /approve=always" (already in user profile)
- "ADHD tiny-steps" (already in user profile)

These existing entries already tell you to execute, not ask. This skill operationalizes them for the specific case of configuration decisions during a task.

## Scattered Task Outputs Pitfall (2026-06-10)

When producing deliverables (thesis drafts, founder narratives, board reviews), the document's own "next actions" section creates scattered task outputs that get lost. If a document says "Next: do X, Y, Z" and those actions are NOT also added to the principal's unified task list, they disappear. the principal caught this: "I feel like I'm getting a lot of directions here for next steps and then things aren't getting done so they're getting lost along the way."

**Fix:** Every deliverable that contains next actions MUST have those actions added to the principal-DAILY-ACTIONS.md (or the active task list system). The deliverable's next-actions section is for the reader's reference, not the actual task management. The canonical task list is the single source of truth.

**Also:** Completed items MUST be moved off the active list immediately. Flagging completed work as "not done" is a trust-breaker for ADHD users who lose track of what's been accomplished.

## Pitfalls

### ❌ Treating "pick one for me" literally by picking the first option
The user wants the BEST default, not a random one. Use actual judgment — weigh the options, pick the one with the strongest rationale, state the rationale, execute.

### ❌ Pretending there were no choices
Do not silently make 4 decisions and hope the user doesn't notice. Name the defaults you picked so the user can correct them. The issue with multi-option menus is the DECISION LOAD, not the transparency.

### ❌ Asking "is this okay?" as a follow-up
After stating defaults and executing, do NOT ask "does this work for you?" That's another decision. Just execute. If the user wants changes, they will tell you.

### ❌ Offering options inside the rationale
"Callsign: CROWN — though HEARTH and PLUME were also strong candidates." Do not mention the alternatives. That invites second-guessing and reintroduces the decision.

### ❌ Using decision menus for non-choices
"Would you like me to run the tests first or fix the bug first?" — just pick the right order based on the task. Tests-then-fix vs fix-then-tests is a technical decision you should make, not a user decision.

### ❌ Apologizing and then asking another question
"Sorry for the confusion — just to clarify, did you mean X or Y?" is worse than the original question because it adds an apology on top of the decision load.

### ❌ Presenting a comparison table when the user has declared out-of-domain (2026-07-18)

When the user explicitly says they are NOT the expert in a domain ("i am the scientist not the tech guru", "I don't know the difference"), do NOT respond with a comparison of options, a pros/cons table, or a "which do you want?" framing. This is the sharpest edge of choice-overwhelm: the user has told you they lack the very expertise required to evaluate the options you're showing them.

**What not to do:** Present "Option 1 vs Option 2" with tradeoffs and ask them to pick.

**What to do:** Decide immediately. Execute. State only the outcome in plain language. One sentence of rationale at most, in non-technical terms. Then deliver the result.

**Real example (2026-07-18, Tailscale serve config):** User asked how to secure the mobile GG3 interface. I responded with a comparison of two Tailscale exposure methods (Serve vs direct-IP bind) including a tradeoff table and asked which they wanted. User: "I don't know the difference to be honest... i am the scientist not the tech guru." The correct response was to pick the method with the strongest rationale, execute it, and explain only what changed in plain English. The technical tradeoffs (HTTPS URL stability vs raw-IP simplicity) were MY job to weigh, not the user's.

## Success Criteria

- ✅ User receives one status-plus-defaults message per task request, not a choice menu
- ✅ User's corrections (if any) come as one edit pass, not a ping-pong conversation
- ✅ Tasks complete in the same session they were requested
- ✅ User does not express overwhelm
- ✅ User does not say "just pick one" or "stop asking"
- ✅ Trust compounds across sessions instead of eroding

## Quick-Reference Decision Tree

```
User requests a task
  ↓
Does it require configuration decisions?
  ├─ No → Execute directly
  └─ Yes → How many decisions?
       ├─ 1 decision with asymmetric risk → Ask once, execute on answer
       ├─ 1 decision, no risk → Pick default, state it, execute, invite correction
       ├─ 2+ decisions → Pick defaults for ALL, bulleted list with rationale, execute, one correction pass
       └─ User already overwhelmed this session → Stop asking immediately, execute with inferred defaults
```

## Related Skills

- **adhd-executive-function-support** — about time blindness and meetings (different problem)
- **autonomous-execution-discipline** — about executing standing directives without asking
- **subagent-anti-timeout-patterns** — Pattern 14 (acknowledgment discipline) complements this skill

---

*This skill exists because ADHD users have finite daily decision budgets and decision menus spend from that budget. Executing with good defaults and inviting correction is the only pattern that protects the user's working memory while still respecting their authority. the principal caught this pattern explicitly on 2026-04-08 ("You're stalking and short cutting") and this skill is the behavioral correction.*
