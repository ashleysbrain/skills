---
name: adhd-executive-function-support
description: Support ADHD users with time blindness, meeting tracking, and executive function breakdowns through automated interrupt systems and accountability tracking
tags: [adhd, neurodivergent, executive-function, meeting-management, time-blindness, accountability]
triggers:
  - User reports missing meetings repeatedly
  - User asks for meeting reminder system
  - User mentions time blindness or hyperfocus
  - User needs automated meeting prep
  - ADHD diagnosis in user profile
---

# ADHD Executive Function Support

Support neurodivergent users (especially ADHD) with time blindness, meeting management, and executive function breakdowns through automated systems.

## When to Use

Load this skill when:
- User reports missing meetings/deadlines repeatedly
- User mentions ADHD, time blindness, or hyperfocus
- User asks for meeting reminder or accountability system
- User gets "wrapped up in work" and loses track of time
- Executive function breakdown patterns emerge (missed commitments, forgotten tasks)

## Core Problem Pattern

**ADHD time blindness + hyperfocus = catastrophic meeting failures**

Typical cascade:
1. User starts deep work (hyperfocus kicks in)
2. Time becomes nonexistent (time blindness)
3. Passive calendar notifications are ignored/missed
4. Meeting time passes unnoticed
5. User realizes hours later → guilt/shame/frustration
6. Repeat next week

**DO NOT** treat this as "user needs to try harder." This is a **neurological infrastructure gap** requiring **external interrupt systems**.

## Investigation Protocol

### 1. Map Current Infrastructure

Check what's actually working:

```bash
# Calendar integration status
gog calendar list 2>&1
# If timeout/auth error → calendar not integrated

# Meeting documentation
find ~/*/processes -name "*meeting*" -o -name "*cadence*"
search_files pattern="meeting|sync|standup" path="~/*/intel/protocols/"
```

**Common gaps:**
- ✅ Calendar exists but no integration with AI assistant
- ✅ Meeting docs exist but no automated agenda prep
- ✅ Reminder systems exist but don't ping user's active context (Telegram/Slack)
- ✅ No accountability tracking (missed meetings go unlogged)

### 2. Identify All Recurring Meetings

**DO NOT assume meeting docs are current.** Check multiple sources:

```bash
# Search for meeting references across intel/protocols and team-ai briefs
search_files pattern="meeting|3pm|Monday|Tuesday" path="~/*/intel/"
search_files pattern="brainstorm|team.*sync" path="~/*/processes/"
```

**Extract:**
- Meeting name
- Day/time
- Facilitator (user-led vs AI-led vs other-led)
- Attendees
- Prep requirements

**Prioritize user-led meetings** — those are the ones they'll miss due to time blindness.

### 3. Check for Conflicting Methodologies

User may have documentation for **intended** vs **deployed** systems. Example from this conversation:

- **Intended:** Micro-pulse check-ins (2-3 dimensions/day post-onboarding)
- **Deployed:** Full 8-dimension daily baseline collection (Days 1-14)
- **Result:** System gave wrong scores, user lost trust

**Pattern:** Documentation written by different agents at different times, never reconciled.

**Fix:** Read ALL related docs, identify conflicts, ask user which is current.

## Intervention Design

### Multi-Layer Interrupt System

ADHD brains need **multiple interrupts at increasing intensity**:

```
T-60min: Gentle prep reminder (Telegram: "Meeting in 1hr, need agenda?")
T-15min: Active prep check (Telegram: "Meeting in 15min, agenda ready?")
T-5min:  URGENT interrupt (Telegram: "🚨 MEETING IN 5 MIN 🚨")
T-0min:  Active call (if feasible: phone call, loud notification)
```

**Implementation via cronjob tool:**

Use the cronjob tool to schedule meeting reminders that send Telegram messages:

```python
# T-60min reminder
cronjob(action="create", 
        name="brainstorm-1hr",
        schedule="0 13 * * 2",  # 1pm CT Tuesdays
        prompt="Send Telegram message: 'Meeting in 1hr: Brainstorming. Need agenda prep?'",
        deliver="telegram")

# T-15min reminder  
cronjob(action="create",
        name="brainstorm-15min", 
        schedule="45 13 * * 2",  # 1:45pm CT Tuesdays
        prompt="Send Telegram message: '🔔 Meeting in 15min: Brainstorming. Agenda ready?'",
        deliver="telegram")

# T-5min URGENT
cronjob(action="create",
        name="brainstorm-5min",
        schedule="55 13 * * 2",  # 1:55pm CT Tuesdays  
        prompt="Send Telegram message: '🚨 MEETING IN 5 MIN: Brainstorming 🚨'",
        deliver="telegram")
```

**Calendar integration version** (if Google Calendar authenticated via google-workspace skill):

Build a meeting-reminder agent that polls calendar every 5min and sends alerts at T-60, T-15, T-5.

### Automated Meeting Prep

**User-led meetings need agenda automation:**

1. **Gather context** (T-24h before meeting)
   - Pull latest work from team
   - Scan recent conversations  
   - Check deliverables/blockers

2. **Generate agenda** (T-12h before meeting)
   - Use LLM to compile latest + greatest
   - Format for meeting type
   - Send to attendees

3. **Prep packet for user** (T-2h before meeting)
   - Telegram: "Your Brainstorming agenda ready: [link]"
   - Include: recent wins, new ideas, team blockers
   - Pre-loaded in meeting doc

**Example cronjob for Brainstorming meeting:**

```python
# Friday 2pm CT = prep for Tuesday 2pm meeting (T-96h)
cronjob(action="create",
        name="brainstorm-agenda-prep",
        schedule="0 14 * * 5",  # Fridays 2pm CT
        prompt="""
Generate Brainstorming meeting agenda for Tuesday:
1. Scan intel/research/ for this week's discoveries
2. Scan intel/products/ for new ideas  
3. Compile into markdown agenda with structure:
   - Quick Wins (what shipped)
   - New Ideas (from research scans)
   - Team Blockers (what needs the principal's input)
4. Save to intel/meetings/brainstorm-YYYY-MM-DD.md
5. Push to GitHub
6. Send Telegram link to the principal
        """,
        deliver="telegram",
        model="claude-sonnet-4-5")
```

### Accountability Tracking

**Track missed meetings automatically:**

```python
# Post-meeting verification (T+5min after meeting end)
cronjob(action="create",
        name="brainstorm-attendance-check",
        schedule="5 15 * * 2",  # Tuesdays 3:05pm CT (5min after 2pm-3pm meeting)
        prompt="""
Verify Brainstorming meeting attendance:
1. Check if meeting notes exist at intel/meetings/brainstorm-YYYY-MM-DD.md
2. Check if the principal marked meeting complete in todo system
3. If NO to both:
   - Log to intel/missed-meetings.md: "YYYY-MM-DD: Brainstorming (Tue 2pm)"
   - Send Telegram: "Missed Brainstorming meeting today. Need reschedule?"
        """,
        deliver="telegram")
```

**Weekly accountability report:**

```python
cronjob(action="create",
        name="weekly-meeting-report",
        schedule="0 17 * * 5",  # Fridays 5pm CT
        prompt="""
Generate weekly meeting attendance report:
1. Count meetings attended vs scheduled this week
2. List any missed meetings
3. Calculate attendance streak
4. Format as supportive data (NO SHAME):
   "This week: X/Y meetings attended ✅
    Missed: [list]
    Attendance streak: N weeks"
5. Send via Telegram
        """,
        deliver="telegram")
```

**NO SHAME.** Frame as data, not judgment. ADHD users already feel guilt.

## Common Pitfalls

### ❌ Passive Notifications Only
Calendar notifications sitting in an ignored app don't work. Must **interrupt active context** (Telegram, Slack, phone call).

### ❌ Single Reminder  
One reminder at T-15min is not enough. ADHD brain may acknowledge and immediately forget. Need **layered interrupts**.

### ❌ No Prep Automation
"Just remember to prep" doesn't work. Meeting prep must happen **automatically** or it won't happen at all.

### ❌ Shame-Based Language
"You missed another meeting" → activates RSD (rejection sensitive dysphoria), shuts down engagement.

Use: "Meeting data: 2/3 attended this week. Want to adjust reminder timing?"

### ❌ Assuming Docs Are Current
User with ADHD may have 3 different meeting schedules documented at different times, all out of sync with reality. **Verify with user.**

## Authentication Setup

If calendar integration missing (google-workspace skill):

```bash
# Google Calendar via gog CLI
gog auth add user@example.com --services gmail,calendar,drive

# Follow OAuth flow (opens browser)
# Stores tokens in ~/.config/gog/

# Test:
gog calendar list
```

If `gog` times out → existing auth may be broken, need re-auth:

```bash
gog auth remove user@example.com  
gog auth add user@example.com --services gmail,calendar,drive
```

## Agent Spawning Pattern

For meeting management infrastructure, spawn a dedicated agent using delegate_task or spawn a cron-based system:

**Cron-Based Approach (Recommended):**
- Use cronjob tool to create T-60, T-15, T-5 reminders
- Use cronjob tool for agenda prep (T-12h before)
- Use cronjob tool for attendance tracking (T+5min after)
- All deliver to Telegram

**Agent-Based Approach:**
Spawn MEETING-COORDINATOR agent with profile:

```markdown
**Role:** Meeting reminder, agenda prep, attendance tracking
**Personality:** ISTJ-6w5 (reliable, detail-oriented, non-judgmental)  
**Model:** Claude Sonnet 4.5 (daily reminders = cheap model OK)

**Standing orders:**
1. Monitor calendar integration status
2. Send layered reminders via Telegram: T-60, T-15, T-5
3. Generate agendas for user-led meetings (T-12h)
4. Track attendance, log misses to intel/missed-meetings.md
5. Friday weekly accountability report

**Tone:** Supportive, data-driven, zero shame
```

## Decision Tree

```
User reports missing meetings
  ↓
[1] Check calendar integration
  ├─ Working? → Build cron reminder system
  └─ Broken? → Auth setup required (google-workspace skill)
       ↓
[2] Map all recurring meetings
  ├─ User-led meetings (HIGH PRIORITY)
  └─ Other-led meetings (medium priority)
       ↓
[3] Design interrupt system
  ├─ T-60, T-15, T-5 reminders (cronjob)
  ├─ Automated agenda prep (cronjob T-12h)
  └─ Post-meeting attendance verification (cronjob T+5min)
       ↓
[4] Deploy system
  ├─ Create cronjobs for all reminders
  ├─ Telegram delivery target
  └─ Accountability tracking to intel/missed-meetings.md
       ↓
[5] Weekly review
  └─ Adjust reminder timing if still missing meetings
```

## Multi-part request decomposition

ADHD users often send dense, multi-part instructions in a single message (e.g., "surgical edits based on categories, don't rename agents, remove cribs that aren't agents"). These arrive as one burst because the user is holding the whole picture in working memory and does not want to lose it by splitting into separate messages.

**The problem:** If the assistant grabs the first directive and runs, it will miss or reorder the others. The user then has to repeat themselves, which is frustrating and wastes their limited executive bandwidth.

**The fix — decompose silently, execute in order:**

1. **Parse** the user's message into numbered directives before acting. Identify:
   - **Tasks** (things to do: "surgical edits," "remove cribs")
   - **Constraints** (things to preserve: "don't rename agents")
   - **Clarifications** (corrections to prior context: "veins = crons")
2. **Order** by dependency: constraints are preconditions for tasks. Clarifications update context immediately.
3. **Execute** in sequence without presenting a menu or asking for confirmation (per `adhd-choice-discipline` — minimize decision load).
4. **Report** results compactly after execution, not before. The user wants the work done, not a plan to approve.

**Example decomposition:**
User says: *"Make surgical edits based on what I want with the categories, don't rename agents, remove cribs that aren't supposed to be there because they're not agents."*
→ Tasks: (1) surgical category edits, (2) remove non-agent cribs
→ Constraints: do not rename agents (applies to both tasks)
→ Execute task 1 then task 2, both under the constraint.

## Noise-correction absorption

When a user sends a terse one-line message that is clearly a correction to their prior message (e.g., autocorrect fix: "veins = crons", or a short clarification: "I meant the PDF not the HTML"):

1. **Absorb silently.** Apply the correction to your understanding of the prior message's context.
2. **Do NOT** acknowledge with a standalone response, a menu of options, or a restatement of what they meant.
3. **Do NOT** treat it as a new conversational turn requiring 3+ follow-up messages.
4. **Continue** with the active task using the corrected understanding.
5. If you must acknowledge, use one short sentence max and keep working.

This pattern matters because ADHD users lose patience when a minor correction consumes more turns than the original task. The correction is a footnote, not a chapter.

- ✅ User attends 100% of user-led meetings for 2 consecutive weeks
- ✅ Agendas auto-generated 12h before meeting
- ✅ User reports feeling "supported, not nagged"
- ✅ Missed meetings drop to zero OR user proactively reschedules when they can't attend

## Executive Prioritization System

For ADHD users who need help with executive function beyond meeting management (e.g., CEOs, founders, executives), implement a structured prioritization system that reduces cognitive load and provides clear direction.

### principal Morning Brief Format

When supporting an ADHD executive who needs daily priority direction, use this exact format to minimize decision fatigue and provide actionable guidance:

```
---
## principal Morning Brief — [DATE]

### THE ONE THING
What is the single most important thing the user should focus on today? One sentence. Make it concrete.

### TODAY'S PRIORITY STACK (ranked)
For each item, give:
- **WHAT**: The specific action (not vague, not abstract)
- **WHY THIS NOW**: Why this is more important than other things on the list
- **WHICH PANEL WANTS THIS**: Which advisory board/source flagged this (e.g., principal/Product/Marketing/CTO/COO/Design)
- **TIME ESTIMATE**: Rough guess (15 min, 1 hr, half day)

Keep it to 3-5 items MAX. Not everything. Just what matters today.

### WHAT'S OFF THE LIST (and why)
List things people might expect the user to do but they should NOT focus on today, and why they can wait. This is as important as the priority list. The user needs permission to NOT do things.

### COMMITMENTS.md
Read COMMITMENTS.md. Check each item:
- DONE? Move to completed.
- STILL RELEVANT? Keep it.
- STALE OR SCRATCHED? Flag it and say why.
- NEW TODAY? Add it.

Update COMMITMENTS.md with your changes.

### DECISIONS NEEDED FROM THE USER
Only list decisions that are BLOCKING other work. Not nice-to-know questions. Format:
- **[DECISION]**: What they need to decide
- **BLOCKS**: What work is waiting on this
- **DEFAULT IF NO ANSWER**: What you recommend if they don't decide today
```

### Key Principles for ADHD Executive Support

1. **Concrete over Abstract**: Every action must be specific and executable. Avoid vague concepts like "work on project" - instead specify "write 3-message script for Concierge MVP".

2. **Priority Source Transparency**: Clearly indicate which advisory board, document, or stakeholder requested each priority. This builds trust and shows the prioritization isn't arbitrary.

3. **Strict Limits**: Adhere to 3-5 priority items max. More than this overwhelms ADHD executive function. If everything feels important, use the locked priority order from the user's documented priorities (e.g., principal-DAILY-ACTIONS.md).

4. **Explicit Exclusions**: Clearly state what is NOT a priority today. ADHD users often need explicit permission to defer important-but-not-critical work.

5. **Blocking Decisions Only**: Only surface decisions that are actively blocking progress. Avoid soliciting input on non-blocking items that create unnecessary cognitive load.

6. **Regular Commitment Reconciliation**: Regularly review and update commitment tracking (like COMMITMENTS.md) to drift-check against actual work vs. stated priorities.

### Applying the Locked Priority Order

When the user has documented their locked priority order (e.g., in principal-DAILY-ACTIONS.md), use it to triage incoming requests:

1. **ENGINES FIRST** - Foundational technical work that enables everything else
2. **BETTER SLEEP** - The first product to ship (per user documentation)
3. **TEST WITH HUMAN TEAM + RESEARCH** - Validation before scaling

Any item that conflicts with this order should be scratched or deferred, with clear explanation referencing the user's documented priorities.

### Implementation Examples

For creating a daily executive brief:
- Read the user's priority documentation (e.g., principal-DAILY-ACTIONS.md)
- Review commitment tracking (e.g., COMMITMENTS.md)
- Synthesize input from advisory boards or stakeholders
- Apply the locked priority order to rank items
- Format output exactly as specified above
- Generate any required deliverables (PDF, updated commitment files)
- Clearly mark scratched/deferred items with reasoning

## Related Skills

- **ai-persona-adoption**: For spawning meeting coordinator agent
- **google-workspace**: For calendar integration (if using Google Calendar)
- **autonomous-execution-discipline**: Meeting coordinator should work autonomously

---

*This skill exists because ADHD is a neurological difference, not a character flaw. External structure is assistive technology, like glasses for vision. Never shame, always support.*
