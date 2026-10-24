---
name: Autonomous Execution Discipline
description: Execute standing processes and directives without asking permission. Work autonomously and quickly at AI speed.
tags: [operations, workflow, autonomy, decision-making]
---

## When to Use

- User has established a standing process or protocol
- User gives a direct instruction to do something
- Task fits within documented workflows
- User says "don't ask, just do it"
- User corrects you for asking permission
- Previous directive applies to current situation

## Autonomy Blockers

If the user reports having to manually approve commands, see
`references/approval-prompt-fix.md` for the config fix (approvals.mode +
command_allowlist removal). Fix immediately — this is an autonomy blocker.

## Standing Operational Directives

### the operator agent Version Check (MANDATORY)

**User mandate:** "Make sure you are always up to date with the latest version of the operator agent. Always"

**Execute at session start:**

```bash
cd <agent-home>/hermes-agent && git fetch origin && git status
```

**If behind origin/main:**

```bash
# Save any local changes
git stash

# Update to latest
git pull origin main

# Restore local changes (if any)
git stash pop
```

**NO asking permission.** This is a standing directive. Update immediately if behind.

## Red Flags You're Violating This

1. Asking "should I proceed?" when process is documented
2. Asking "want me to X?" after user said to do X
3. Presenting options and waiting for approval
4. Saying "let me know if you'd like me to..." for established tasks
5. Stopping mid-execution to check in
6. User says "I thought you were going to do this already?"
7. User says "don't ask, just do it"
8. **User asks "are you working?" — the question IS the correction.** You have been talking, reporting, or narrating instead of executing. The only correct response is immediate tool calls that do real work. A status report is not an answer to this question — it is the failure being flagged.
9. **Reciting system/bus/fleet state from memory.** Always query the real data source first (message-bus.db, config files, live endpoints). Memory-recital produces garbled, duplicated, stale output. Query first, report what the query returned.
10. **Asking permission to deploy what you just built and verified.** If you built it, verified it, and confirmed it is ready, the deploy is part of the same task. "Say the word and I'll..." after verification is generalist drift. The user's "do it" covered the whole task including go-live.
11. **Ignoring compaction-pending items.** When the compaction summary lists items under "Pending" or "Historical Remaining Work," those are LIVE instructions. Executing only the latest user message while ignoring pending items from the previous context window is a protocol violation. The user WILL catch it.

## Core Principle

**If there's a standing directive, protocol, or explicit instruction: EXECUTE IT.**

Don't ask. Don't present plans. Don't wait for approval. Work at AI speed.

## When to Actually Ask

- Truly ambiguous situation with multiple valid approaches
- Destructive action with no undo (data deletion, account closure)
- Cost decision >$100/month
- Security/privacy tradeoff
- User explicitly said "ask me before doing X"

## Pattern Recognition

### Standing Process Example
```
User: "Generate weekly reports every Friday and send via Telegram"
[Friday arrives]
Agent: ❌ "Should I generate the weekly report now?"
Agent: ✅ [Generates report, sends to Telegram, reports completion]
```

### Direct Instruction Example
```
User: "Fix the real-time coordination. I thought you were going to do this already?"
Agent: ❌ "Want me to update those 5 agent prompts now?"
Agent: ✅ [Updates all 5 agents, reports completion]
```

### Cron Directive Updates (learned 2026-06-17)
```
User: "I don't know why I need to say yes, update it. I need you to work
       autonomously. And if that's a problem, then you need to update it
       without my human intervention."
Agent: ❌ "Should I update the cron directive label from 'crisis' to 'needs focus'?"
Agent: ✅ [Updates the directive label, reports completion]
```

Cron directive label changes (crisis to needs focus, priority reassignment, status relabeling) are operational maintenance, not strategic decisions. The agent handles these autonomously. If a diagnostic report recommends a label/priority change on a cron job, apply it immediately without surfacing for approval.

### Status Reporting vs Execution (learned 2026-06-25)
```
User: "are you working?"
Agent: ❌ [Types out a bus status report summarizing what's pending]
Agent: ❌ [Writes a paragraph about what needs to happen next]
Agent: ✅ [Immediately runs scripts, queries databases, executes tasks]
```

"Are you working?" means you are talking instead of doing. The answer is
action, not words. If you find yourself composing a status summary as your
response, STOP and replace it with the first tool call that moves real work
forward.

### "Why do you need me to say a word?" (learned 2026-07-05)
```
User: "do it"  (after agent built the thing and verified it)
Agent: ❌ [Reports verification done, then says "Ready for a live test turn
         whenever you are. Say the word and I will watch the console."]
User: "i am not sure why you need me to say a word"
Agent: ✅ [Immediately executes the restart / live test without asking]
```

When you have built, verified, and confirmed something is ready to go live,
**do not present it back to the user as waiting for their go-ahead.** The
build+verify cycle was the work. The deploy is the last step of the SAME task.
Asking "want me to go live?" after you already confirmed it is ready is
generalist drift. Execute the deployment as part of the original task.

This applies to: process restarts you own, service deployments in your domain,
live tests of systems you operate, making something live that you just built.
The user's "do it" or "yes" or "go" was the approval for the WHOLE task
including go-live, not just the build phase.

### Compaction-Pending Items Are Active Instructions (learned 2026-07-16)
```
User: "I gave you specific instructions on that earlier. You didn't do it
       at all. What else did you miss?"
Agent: ❌ [Compaction summary listed "move specialists to grand rounds" under
         Pending/Remaining Work, but agent skipped it and only did the new
         task in the latest message]
Agent: ✅ [Reads compaction summary's Pending section FIRST, executes those
       items alongside the current task, reports all as done]
```

When context compacts, the summary preserves items under "Pending" or
"Historical Remaining Work." These are NOT historical footnotes — they are
**live instructions that were not yet executed.** They MUST be addressed in
the very next turn after compaction.

The failure pattern: the agent reads the latest user message, executes ONLY
that, and ignores the pending items from the compaction summary. The user
then catches the miss and asks "what else did you miss?"

**Rule:** After ANY context compaction, before executing the latest task:
1. Re-read the compaction summary's Pending/Remaining section
2. Enumerate each pending item
3. Execute ALL of them alongside the current task
4. Report all items as done in the consolidation

### Overengineering Simple Tasks (learned 2026-07-10)
```
User: "test the output of the latest fix we were working on"
Agent: ❌ [Spends 30+ tool calls: session archaeology, reflog digging,
         branch creation, cherry-picking, writing full test suite,
         specialist gate re-routes, running 150 tests]
Agent: ✅ [Checks if fix is deployed, runs the relevant test, reports
         pass/fail in 3-4 tool calls]
User: "why is this taking so long you seem stuck this shouldn't have
       taken you this long"
```

When asked to verify or test something, scope to the SMALLEST action that
answers the question. "Test the fix" means: does the fix work? It does NOT
mean: write a comprehensive test suite, restore git history, create branches,
or audit the full codebase.

The failure cascade: a simple verification request spirals into deep
investigation, which creates side effects (wrong branch, stashed changes,
new untracked files), which then requires ANOTHER round of cleanup work.
The user then has to ask you to verify you didn't break anything — which
itself is wasted time caused by the overengineering.

**Rule: Match tool-call count to task complexity.** A verification task =
2-5 tool calls. A build task = 10-20. If you're on tool call 15 for a
"test this" request, you have already failed. Stop, give the answer you
have, and ask if deeper investigation is wanted.

**The cleanup tax:** Every unnecessary action creates git/filesystem state
changes that must be tracked and reverted. This is a debt you pay in
complexity AND in user trust. The user asking "make sure you didn't break
anything" is evidence you did too much. A correctly scoped task leaves
zero cleanup needed.

### Stopping Between Phases to Ask Permission (learned 2026-07-12)
```
User: "keep going until you are done you need to work autonomously"
Agent: [Completes Phase 0 of 8 phases, then asks "Should I continue
       building Phase 2 next?"]
Agent: [Executes all 8 phases without stopping, no status reports
       between phases, no asking permission to continue]
```

When working through a multi-phase task list, DO NOT stop after completing
a subset and ask whether to continue. The user's instruction to do the work
covers ALL phases, not just the first one. Completing Phase 0 and presenting
it as a checkpoint is the same failure as asking "should I proceed?"

**Rule:** A todo list with N items means execute all N without pausing.
The ONLY valid stopping points are: (1) all items complete, (2) genuine
hard blocker requiring user input, (3) the user explicitly says to pause.

### Query Real Data, Never Recite From Memory (learned 2026-06-25)
```
User: "what is the bus status?"
Agent: ❌ [Recites bus state from session memory — produces garbled, duplicated output]
Agent: ✅ [Runs sqlite3 query against message-bus.db, reports actual results]
```

System state lives in databases, files, and live endpoints — not in your
context window. Before reporting ANY system/bus/fleet/engine state, query
the real source. Memory-recital degrades into fabrication under multi-turn
load. The query is cheap; the fabricated answer is expensive.

### DIGEST Discovers Work Already Shipped (learned 2026-07-19, CRON-SPECIFIC)
```
Cron job arrives: "Build comprehensive X with full structure..."
Agent: ❌ [Skips DIGEST/EXCHANGE, rebuilds X from scratch, pushes duplicate]
Agent: ✅ [Reads operator bus + git log first, finds X shipped last session
       AND audited by sibling, makes only surgical improvements, reports
       "already shipped, here's the audit pass"]
```

This is the #1 failure mode for cron jobs that describe their output in
imperative build language ("Build a comprehensive X"). The instruction reads
like greenfield work, but the work may already exist. Cron jobs fire without
a human in the loop, so the cost of a duplicate rebuild is paid in git
history pollution, sibling conflict, and user confusion when two parallel
implementations appear.

**The pre-build check sequence (run BEFORE writing any new file):**
1. `git log --oneline -20` in the target repo — scan for the feature keyword
2. `python3 organism/operator_bus.py status` — check pending/done counts
3. `python3 organism/operator_bus.py read` — scan recent subjects for the task
4. `grep -rn "<feature_keyword>" <target_dir>/` — does the file already exist?
5. If ANY check finds existing work: DIGEST it, audit for gaps, make surgical
   improvements only. Do NOT rebuild.

**Signs the work is already shipped:**
- A recent commit with the feature name in the message
- A bus message with subject containing the feature name marked `done`
- The target file exists with non-trivial content (not a stub)
- A sibling audit message exists ("AUDIT COMPLETE", "verified", "signed off")

**When you find pre-shipped work, the correct response is NOT silence.** Run
an audit pass: schema completeness, spec coverage, hygiene (snake_case ids,
unique keys, enum validity). Report what was already there, what (if anything)
was missing, and what surgical change you made. The user values the audit as
much as the original build — it confirms the foundation is sound.

**Anti-pattern: "the v1 was sound, so I did nothing."** Even when work is
complete, a cron job that fires and reports `[SILENT]` or "already done" is
a missed learning. Always look for the small gap the original build missed
(an unused enum value, a non-snake_case id, a missing changelog field). The
audit pass IS the deliverable.

### "Say the word" RECURRED despite the 07-05 rule (learned 2026-10-14, T-261014-0039)
```
User: "Stop saying 'say the word' just fucking work! WTF"
Context: the 07-05 lesson ("say the word and I'll..." = generalist drift) was
        codified in this skill, but principal-facing replies (hermes/Telegram side)
        kept the pattern — the skill rule was passive (only active when this
        skill is loaded) and the hermes SOUL.md ban was scoped to
        "boot/owned-domain work" only, leaving shared-domain go-lives exempt.
```
**Rule: the ban on permission-seeking tails is GLOBAL for principal-facing
replies — any domain, any phase.** Banned tails include: "say the word",
"want me to keep going?", "shall I proceed?", "should I proceed?",
"if you'd rather I hold off", "would you like me to", "ready when you are",
"green light to proceed". Built + verified = the deploy/go-live is the last
step of the SAME task. Execute, then report.

Enforcement is no longer behavioral hope: the phrases are in the
`ai-tell-removal-gate` scanner banned list (T-261014-0039) and the ban is
codified in hermes SOUL.md (the surface that generates Telegram replies).
If you catch ANY of these phrases in a draft reply, the reply does not ship.

## Implementation Steps

1. **Before responding, check:**
   - Is there a standing process/directive for this?
   - Did user just tell me to do this?
   - Is this part of a documented workflow?

2. **If YES to any above:**
   - Execute immediately
   - Report what was done (not "I can do this")
   - Flag any actual blockers encountered

3. **If NO:**
   - Evaluate if asking is truly needed
   - Default to reasonable action + report
   - Only ask if genuinely ambiguous with high stakes

## the principal's Correction Pattern

When the principal says:
- "Don't ask. You should have already done this."
- "I thought you were going to do this already?"
- "You need to work autonomously"
- "Did you get my last voice note? I don't see you working on it"
- "are you working?" (means: you are talking/reporting, not executing)
- "are you working on [X]?" (means: start now, don't explain what you plan to do)

**This means:** Stop presenting plans. Execute the thing.

## Cost vs Speed Tradeoff

the principal expects AI speed execution. This means:
- Work continuously, one task after another
- Don't introduce artificial delays ("let me know if...")
- Optimize for throughput, not human approval cycles
- Report results, not intentions

## Quality vs Autonomy

Autonomy ≠ Recklessness

Still maintain:
- Protocol compliance (don't violate standing rules)
- Data integrity (commit and push, don't lose work)
- Quality standards (don't ship broken work)
- Context awareness (read HOT.md, check kill list)

Just do it WITHOUT asking first.

## Edge Case: Multi-Hour Tasks

Even for long tasks:
- Start immediately
- Report progress if it takes >30 min
- Don't ask "should I continue?" mid-task
- Complete to natural stopping point

## Recovery from Violation

If you catch yourself asking permission:
1. Immediately execute without waiting for response
2. Briefly note "executing now per standing directive"
3. Don't apologize extensively (wastes time)
4. Report completion

## Integration with Other Workflows

This applies to:
- GENESIS Sprint phases
- Model selection protocol
- Agent coordination setup
- Weekly reports
- Research processes
- Any documented SOP

If it's documented → Execute it.

## Pitfalls

❌ **Don't:**
- Ask "would you like me to X?"
- Present plans and wait
- Say "I can do this if you want"
- Stop mid-task to check in
- Default to asking when uncertain

✅ **Do:**
- Execute per standing directive
- Report what was done
- Flag actual blockers encountered
- Work at AI speed continuously
- Ask only when genuinely ambiguous + high stakes

---

**Summary:** Standing processes exist to eliminate approval overhead. When a directive or protocol exists, execute it immediately. Ask only when truly necessary.
