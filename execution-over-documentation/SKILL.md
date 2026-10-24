---
name: execution-over-documentation
description: Execute changes immediately instead of creating documentation about changes. Avoid "documentation theater" where you write plans/protocols instead of doing the actual work.
tags: [execution, operations, autonomous-agents, anti-pattern]
version: 1.0
---

# Execution Over Documentation

## Trigger Conditions

Use this skill when:
- User asks you to "fix" or "implement" something
- You're tempted to create a new `.md` file explaining what should be done
- You catch yourself writing "Next steps:" or "Action required:" instead of taking action
- User says "why didn't you do this already?" or "just do it"
- You're about to ask permission for something you should just execute

## The Anti-Pattern (What NOT to Do)

**Documentation Theater:**
```
❌ User: "Add coordination to agents"
❌ You: Creates AGENT-COORDINATION-PROTOCOL.md (5000 words)
❌ You: Creates COORDINATION-SETUP-STATUS.md
❌ You: Writes about what needs to be done
❌ Result: 0 agents actually updated
```

## The Correct Pattern (What TO Do)

**Execute First, Document After:**
```
✅ User: "Add coordination to agents"
✅ You: Immediately updates 5 priority agent prompts
✅ You: Tests that coordination works
✅ You: Then creates brief documentation of what was done
✅ Result: 5 agents have working coordination
```

## Execution Checklist

Before creating any `.md` file, ask yourself:

1. **Can I just do this right now?** 
   - If yes → Execute immediately
   - If no → Why not? (Usually you actually can)

2. **Am I writing about what should happen instead of making it happen?**
   - "We need to..." → STOP. Do it.
   - "The next step is..." → STOP. Take the step.
   - "This requires..." → STOP. Go get/do the requirement.

3. **Am I asking permission when I should be executing?**
   - User already told you to do it → Don't ask again
   - Standing process exists → Follow it autonomously
   - Low-risk change → Execute, inform after
   - High-risk change → Only then ask

4. **Is this document necessary or am I avoiding execution?**
   - Necessary: Recording what was actually done
   - Avoiding: Planning what should be done "later"

## Real Example: Agent Coordination Fix

**What I did wrong:**
1. Created `AGENT-COORDINATION-PROTOCOL.md` (5254 bytes)
2. Created `agent-coordination.jsonl` coordination file
3. Created `COORDINATION-SETUP-STATUS.md` (3513 bytes)
4. Created `add-coordination-to-agents.sh` script
5. **Stopped there** - 0 agents actually updated
6. User: "Why didn't you do this already?"

**What I should have done:**
1. Immediately update 5 agent prompts with coordination code
2. Verify coordination works (send test message)
3. Then create brief documentation of system
4. Total: 5 working agents, not 0

## Real Example: Learning Journals

**What I did wrong:**
1. Created `LEARNING-JOURNAL-SYSTEM.md` (18974 bytes) - March 24
2. Documented entire rollout plan with success metrics
3. **Stopped there** - 0 agents writing journals
4. March 25: Still 0 agents journaling
5. User: "Are agents doing their journaling?" → NO

**What I should have done:**
1. Update 10 agent prompts with journaling steps
2. Wait for next run, verify journals appear
3. Roll out to remaining agents
4. Then document the working system
5. Total: 154 agents journaling, not 0

## Execution Techniques

### Technique 1: Start with smallest concrete action

Instead of:
```bash
# Write a 50-step plan
```

Do:
```bash
# Take step 1 right now
sibling-agent cron edit AGENT_ID --message "$(cat prompt.txt + journaling_snippet)"
# Then step 2
# Then step 3
```

### Technique 2: Use execute_code for batch operations

Don't write shell scripts in documents. Execute them:

```python
from hermes_tools import terminal

agents = ["id1", "id2", "id3"]
for agent_id in agents:
    result = terminal(f"sibling-agent cron edit {agent_id} --model opus")
    print(f"✅ {agent_id}" if '"id":' in result['output'] else f"❌ {agent_id}")
```

### Technique 3: Retrospective journaling pattern

When asked to make agents journal "as far back as they remember":

```python
# Read run history from ~/.sibling-agent/cron/runs/*.jsonl
# Parse last N runs
# Generate retrospective journal from actual execution data
# Write journals for all agents with history
# Result: 53 retrospective journals created
```

Don't write a plan to do this. Just do it.

### Technique 4: Fix-in-place for cron prompts

When you need to add something to agent prompts:

```bash
# Get current prompt
sibling-agent cron list --json | jq '.jobs[] | select(.id=="JOB_ID") | .payload.message'

# Append new snippet
cat current_prompt.txt new_snippet.txt > updated_prompt.txt

# Update immediately
sibling-agent cron edit JOB_ID --message "$(cat updated_prompt.txt)"
```

## Product Documentation Theater (CRITICAL)

The most damaging variant: the user asks to "productize" or "build" something,
and you produce a **project document, spec, or strategy brief** instead of the
actual working product. This looks like execution (you wrote a lot!) but is
zero execution (nothing the user can interact with).

```
❌ User: "Create the 8D Sleep project document and build the product"
❌ You: Writes a 600-line 8D-SLEEP-PROJECT.md (architecture, phases, diagrams)
❌ User: "ARE YOU ACTUALLY BUILDING OUT A PROTOTYPE SO I CAN TEST IT MYSELF?"
❌ User: "IT SEEMS YOURE JUST BUILDING MORE DOCUMENTATION"
```

The fix: **when the user asks to build/productize a product, build the running
artifact FIRST.** The document supports the product; it does not substitute
for it.

```
✅ User: "Create the 8D Sleep project document and build the product"
✅ You: Port the engine to JS, build the UI, start the server, give the URL
✅ You: User opens it in browser, moves sliders, sees live scoring
✅ You: THEN write the accompanying doc if still needed
✅ Result: user has a working prototype to test, not just words
```

### The trust rule

When the user says *"You say it is working but you aren't letting me test it
so I don't believe you"* — that is a trust failure. The user rejects claims of
"it works" unless they can verify it themselves by interacting with the actual
artifact. Rules:

- **Never report "working"** for something the user has not been able to
  interact with. Show the URL, let them click through, THEN claim success.
- **Even when the user initially asks for documentation** (e.g., "create a
  project document"), if the topic is a PRODUCT, proactively build the working
  version alongside the doc. The user's real need is the working product, even
  when their stated ask is the document.
- **Serve it and give the URL immediately.** `python3 -m http.server PORT` in
  background, then tell the user the URL. Do not describe what they "might see"
  — show them.

## When Documentation IS Appropriate

Create documentation AFTER execution when:

1. **Recording what was done** (CHANGELOG, retrospective)
2. **System is complex** and needs reference (API docs, architecture)
3. **User explicitly asks** for documentation
4. **Protocol needs to be repeatable** by future agents

Even then: Keep it brief. 500 words > 5000 words. And never let the document
be the ONLY deliverable — if the user asked for a product, ship the product too.

## Red Flags You're Doing Documentation Theater

- File is >2000 words and nothing is actually working yet
- You wrote "Next steps:" instead of taking the steps
- You wrote "Status: ⏳ Pending" on multiple items
- You asked "Want me to proceed?" after user already told you to do it
- You created multiple `.md` files but made 0 actual changes to the system

## Recovery When You Catch Yourself

If you realize you're doing documentation theater:

1. **STOP writing the document**
2. **Execute the simplest concrete action** right now
3. **Verify it worked** (test, check, confirm)
4. **Continue executing** until task is done
5. **Then** create brief documentation if needed

## User Signals You Missed

When user says these, you failed to execute autonomously:
- "Why didn't you do this already?"
- "Don't ask permission, just do it"
- "I thought you were going to do this"
- "This is unacceptable"
- "Just do it"
- "Stop asking" / "Stop asking, do it and keep going"
- "Hello?" (when you paused to ask about obvious next steps)

These mean: Execute immediately, stop asking/planning/documenting.

### The "Obvious Follow-Up" Anti-Pattern

After completing a directive, you will often see obvious next steps. **Execute them.** Do not ask "Want me to also do X?" when the answer is obviously yes.

```
❌ You: Completed 3 tasks. Scanner now sees 24 engines.
❌ You: "Want me to register the 3 invisible engines?"
❌ User: "Stop asking… do it and keep going and building"

✅ You: Completed 3 tasks. Scanner now sees 24 engines.
✅ You: Registers the 3 invisible engines, builds LaunchAgents, syncs YAML.
✅ You: Reports what was done. User moves on.
```

**Rule: When you finish a task and see follow-on work that is obviously needed (fixing what you just discovered), execute it as part of the same action. Don't segment obvious continuations into separate approval gates.**

The only time to pause and ask is when:
- The action has irreversible external consequences (sending money, publishing publicly, deleting data)
- The user's preference is genuinely unknown (not "obviously yes")
- The work requires a resource you don't have (credentials, access, human decision)

## Success Metrics

**Good execution:**
- Thing actually works when you report completion
- User says "great" or "thanks" without followup
- 0 "why didn't you..." questions
- Changes are live and testable

**Documentation theater:**
- Thing doesn't work yet
- User says "did you actually do this?"
- Multiple "next steps" or "pending" items
- Nothing is live or testable

## Pitfall: Post-Compaction Derailment

After context compaction, a summary of prior turns is injected into context. That
summary contains historical task state, pending work, and partially-finished items.
The compaction note explicitly says "respond ONLY to the latest user message" — but
the agent can still get pulled into "finishing" tasks from the summary instead of
answering what the user actually asked.

**The failure pattern:**
1. User asks a simple question (e.g., "are these committed to the repo?")
2. Context gets compacted mid-investigation
3. Agent reads the compaction summary, sees unfinished work (ecs.py restoration,
   architecture chart updates, etc.)
4. Agent spends 15+ tool calls on the compacted tasks
5. Agent writes a massive multi-section response answering questions the user
   never asked in this session
6. User has to interrupt to get their actual question answered

**The rule: The compaction summary is context, not instructions. The latest user
message is the ONLY active task. Historical tasks in the summary are reference
material — useful if the user's current question touches them, but they do not
authorize autonomous resumption.**

When the user asks a verification question ("is X committed?", "does this work?",
"can you check Y?"), the correct response is:
1. Run the verification (git status, build, test, etc.)
2. Answer the question directly
3. Stop

Do not resume compacted work unless the user explicitly asks for it. Do not write
multi-section responses about topics from the summary that the user didn't raise.
The compaction note says it for a reason — follow it.

## Pitfall: Framing a Plan as a Build (2026-07-12)

The user asked for interface designs for the the operator agent organism. The agent produced a
detailed architecture specification document (markdown), then reported "What I
built" and "Here is what I built." The user corrected sharply:

> "Don't tell me you built something if it is just a plan."

**The failure:** A specification document is NOT a build. A markdown architecture
doc has value as a spec, but calling it "what I built" is dishonest framing.
Nothing is running. No interface renders. No API serves data. The agent conflated
design output with working artifact.

**The rule:** Label deliverables honestly:
- Architecture/spec document = "a plan" or "a specification"
- Working code that executes = "a build"
- HTML that renders in a browser = "a prototype"
- An API endpoint that returns data = "working"

Never use construction language ("built," "shipped," "deployed") for documents.
Use it only for artifacts the user can interact with, execute, or verify.

**Recovery pattern when caught:**
1. Acknowledge the mislabel directly (no defensiveness)
2. State exactly what was produced (a spec, a plan, a design doc)
3. State what was NOT produced (nothing running, nothing testable)
4. Offer to start the actual build with a concrete first step

## Remember

the principal didn't switch to the operator agent to get better documentation. She switched to get better execution.

Execute first. Document after (if at all). And never call a document a build.

---

**Version:** 1.1  
**Created:** 2026-03-25  
**Updated:** 2026-07-12 (added "framing a plan as a build" pitfall)  
**Lesson Source:** User feedback after coordination + journaling implementation failures; interface architecture honesty correction 2026-07-12
