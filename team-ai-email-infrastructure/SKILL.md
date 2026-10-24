---
name: team-ai-email-infrastructure
description: Deploy bidirectional email system for Team AI personal assistants (send + receive)
version: 1.0
platform: any
tags: [team-ai, email, infrastructure, deployment]
---

# Team AI Email Infrastructure Deployment

## When to use this skill
- Deploying personal AI assistants that need to communicate via email with team members
- Setting up bidirectional email (not just sending, but also reading replies)
- Discovering agents can send but not receive (one-way communication gap)

## Critical principle
**Bidirectional communication is NON-NEGOTIABLE for personal AI assistants.** If agents can't read replies, team members think they're being ignored. This breaks trust immediately.

## Prerequisites check
Before deploying ANY Team AI email system:

1. **Verify authentication status:**
   ```bash
   gog auth list  # Check if Google Workspace is authenticated
   gcloud auth list  # Check if gcloud credentials exist
   ```

2. **Identify what you CAN'T automate:**
   - gog OAuth flow requires BROWSER popup (user must click "Allow")
   - Cannot be delegated to subagents or automated
   - Plan for manual user intervention

3. **Check if problem already solved:**
   - Search memory, GitHub, logs for existing solutions
   - Don't spawn agents for already-fixed problems (waste of Opus credits)

## Deployment phases

### Phase 1: Audit current state (DO THIS FIRST)
Create comprehensive email audit showing:
- All emails sent (with timestamps, recipients, content summaries)
- All emails pending (blocked by what?)
- Infrastructure gaps (auth issues, polling missing)
- Credibility check (consistency, quality, transparency)

**Deliverable:** PDF report via Telegram

**Why:** User needs visibility before fixing gaps. Shows you understand the problem.

### Phase 2: Immediate workarounds (while fixing infrastructure)
If emails need to go out TODAY but gog isn't configured:

```bash
# Use sendmail as temporary solution
sendmail -t < /tmp/email_with_headers.txt
```

**Template:**
```
From: principal.williams@divinityscience.com
To: recipient@domain.com
CC: principal.williams@divinityscience.com
Subject: [AGENT NAME] — [Purpose]

[Email body]

---
This email was sent by [AGENT NAME], your AI personal assistant.
Questions? Reply directly or reach the principal Williams.
```

**Critical:** Always CC the human manager. Always include AI disclaimer.

### Phase 3: Request user action (gog OAuth)
**Don't just tell them it's broken. Give them EXACT steps:**

```
You need to authenticate gog (2-minute browser flow):

OPTION 1 (easiest):
bash /tmp/get_my_calendar.sh

OPTION 2 (if Terminal feels hard):
Just tell me when you're ready and I'll walk you through it step-by-step.

OPTION 3 (skip for now):
I'll set up manual reminders while we wait for auth.
```

**Key:** Offer easy path, harder path, and "skip for now" option (ADHD-aware).

### Phase 4: Build inbox polling system
Once gog is authenticated, build:

1. **Email checker script** (Python):
   ```python
   # Check inbox for replies from team members
   # Extract message content
   # Route to appropriate agent
   # Store conversation thread
   ```

2. **Response generator:**
   - Spawn agent with full context (their profile + conversation history)
   - Generate response
   - Send via authenticated method

3. **Cron job:**
   ```bash
   # Run every 5-10 minutes
   */5 * * * * /path/to/email_polling_script.py
   ```

### Phase 5: Test with real replies
- Retrieve actual replies from team members
- Have agents respond to them
- Verify responses are appropriate
- Check team member satisfaction

## Common pitfalls

### ❌ Spawning agents without checking infrastructure
**Symptom:** Agent profile created but can't actually do its job  
**Example:** IP-SCRUBBER spawned to fix problem already solved 3 hours earlier  
**Fix:** Always check memory/GitHub/logs BEFORE spawning

### ❌ Delegating when you should execute directly
**Symptom:** Multiple delegation attempts, all interrupted  
**Example:** EMAIL-BRIDGE delegated to Claude Code 2x, both interrupted  
**Fix:** If task is <10 steps, just do it yourself. Delegation has overhead.

### ❌ One-way communication
**Symptom:** Emails sent, no replies processed  
**Impact:** Team members think agents are ignoring them (CRITICAL trust gap)  
**Fix:** Build inbox polling IMMEDIATELY, not "eventually"

### ❌ No AI disclaimer in early emails
**Symptom:** Team member didn't know they were talking to AI  
**Legal exposure:** Transparency violation  
**Fix:** Mandatory disclaimer footer on ALL team emails

### ❌ Stale data in reports
**Symptom:** User asks for scores, agent shows cached/old data  
**Example:** Fleet TWC reported as 8.4 (actually 7.41)  
**Fix:** Always read source files fresh. Never cache scores.

## Quality checklist

Before marking Team AI email system as "deployed":

- [ ] Agents can SEND emails (authenticated method working)
- [ ] Agents can READ replies (inbox polling active)
- [ ] All emails include AI disclaimer
- [ ] Human manager CC'd on all team emails
- [ ] Email audit document created (shows transparency)
- [ ] Conversation threading works (agents remember context)
- [ ] Cron jobs scheduled (automated, not manual)
- [ ] Test with real team member (not just hypothetical)
- [ ] Escalation protocol (if team member frustrated, alert human manager)

## Success metrics

After 1 week of deployment:
- Team members feel heard (agents respond within 2 hours)
- Zero "my agent is ignoring me" complaints
- Email audit shows consistent quality/timing
- No stale data in reports
- Trust established (team members engage with agents)

## Recovery from trust breakdown

If team member already thinks agent is broken:

1. **Acknowledge immediately:**
   "You're right - [AGENT] couldn't see your replies. That's a system gap, not you being ignored."

2. **Show receipts:**
   Email audit showing what WAS sent, what WASN'T received

3. **Fix publicly:**
   "I'm building inbox polling now. You'll get a response to your [specific question] within 30 minutes."

4. **Follow through:**
   Actually respond to their backlog of unanswered messages

5. **Prevent recurrence:**
   Set up monitoring so gap never happens again

## Related skills
- `operations/autonomous-execution-discipline` - Don't ask permission for fixes you can do yourself
- `operations/execution-over-documentation` - Build the system, don't just document the gap
- `operations/conversation-archival-before-compression` - Email audit is a form of archival

## Notes
- Email infrastructure is FOUNDATIONAL, not optional
- Users judge AI quality by responsiveness
- One-way communication is worse than no communication (creates false expectations)
- Always offer ADHD-friendly options (easy path, hard path, skip-for-now path)
