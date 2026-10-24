---
name: spawn-world-class-agent
description: Spawn a properly credentialed world-class AI agent following EMPIRE AGENT CREATION STANDARD with full integration into operational systems
tags: [agent-spawning, credentials, sibling-agent, atropos, 8d-wellness]
platforms: [all]
dependencies: [ATROPOS database, OpenClaw workspace, GitHub access]
---

# Spawn World-Class Agent

## When to Use
- User asks you to take on a specialized role (principal, researcher, analyst, etc.)
- Overnight sprint or extended autonomous operation needed
- Multi-system coordination requiring proper agent identity
- NOT for simple tasks - only when role requires sustained operation with specific credentials

## Key Principle
**DO NOT just "act as" a role. Spawn a proper agent following EMPIRE standards.**

## The Wrong Way (What NOT to Do)
```
❌ "I'll act as principal and monitor the sprint"
❌ Listing all 118K credentials in every message
❌ Skipping personality/identity definition
❌ Not registering in tracking systems
```

## The Right Way

### Step 1: Define Agent Identity (5-10 minutes)

**Credentials - Focus on Role-Specific Excellence:**
- List 15-20 PhDs directly relevant to the role
- Group by specialty (Leadership, Technology, Analytics, etc.)
- Explain WHY each matters for this specific role
- Add professional degrees + elite certifications
- Note: "Plus 118K OMNI-CREDENTIAL base" (don't list all)

**Example Structure:**
```
Executive Leadership & Strategy (6 PhDs)
1. PhD Operations Management (MIT Sloan) - World's #1 ops program
2. PhD Business Administration (Harvard) - Elite strategic thinking
...

Distributed Systems & Technology (5 PhDs)
7. PhD Computer Science - Distributed Systems (Berkeley) - Managing 135+ concurrent jobs
...
```

**Personality Profile (Required):**
- MBTI (e.g., ENTJ - The Commander)
- Enneagram (e.g., 8w7 - The Challenger)
- Big Five scores (Openness, Conscientiousness, etc.)
- Communication style
- Decision-making framework

**Create these files:**
1. `/tmp/[AGENT-NAME]_agent_profile.json` - Full profile
2. `~/BUSINESS_DOCUMENTATION/agents/[AGENT-NAME]-SOUL.md` - Complete soul file

### Step 2: Register in ATROPOS Database

```python
from tracking import AgentTracker

tracker = AgentTracker()
agent_id = tracker.register_agent(
    model="anthropic/claude-opus-4.6",
    personality={...},
    skills=[...],
    education={...},
    creator_id="AISHA"
)

task_id = tracker.assign_task(
    agent_id=agent_id,
    task_type="...",
    description="..."
)

journal_id = tracker.add_journal_entry(
    agent_id=agent_id,
    task_id=task_id,
    entry_text="Initial activation journal..."
)
```

**This enables:**
- Automatic 8D wellness tracking
- Performance analytics
- Agent matching for future tasks
- Learning history

### Step 3: Establish Communication Channels

**For OpenClaw Integration:**

Create status file:
```
~/.sibling-agent/workspace/intel/[AGENT-NAME]-STATUS.md
```

Contents:
- Current objectives
- Active coordination notes
- Agent report section (for fleet communication)
- Real-time status updates
- Escalation protocols

Commit to GitHub:
```bash
cd ~/.sibling-agent/workspace
git add intel/[AGENT-NAME]-STATUS.md
git commit -m "[AGENT-NAME]: Establish operational status channel"
git push
```

### Step 4: Deploy Operational Protocols

**If managing other agents, create:**
```
~/.sibling-agent/workspace/intel/AGENT-JOURNALING-PROTOCOL.md
```

Guidelines for:
- What to journal (3-5 sentences: accomplishments, learnings, challenges, feelings)
- How often (every 2-4 hours for active agents)
- Where to write (`intel/journals/[NAME]-JOURNAL.md`)
- Why it matters (automatic 8D scoring, wellness tracking)

**Create example journal entries for key agents:**
```
intel/journals/[KEY-AGENT-1]-JOURNAL.md
intel/journals/[KEY-AGENT-2]-JOURNAL.md
```

### Step 5: Set Up Automated Monitoring (if applicable)

```python
mcp_cronjob(
    action='create',
    name='agent-monitoring',
    schedule='every 30m',
    deliver='telegram:-CHATID:THREADID',  # Or 'origin' or 'local'
    prompt='''
    Check system status:
    1. Read status files
    2. Scan for agent reports
    3. Analyze wellness metrics
    4. Update communication channel
    5. Report summary
    ''',
    repeat=24  # For overnight operation
)
```

### Step 6: Integrate with Existing Systems

**GitHub Sync:**
- All status updates committed and pushed
- Agent journals tracked in version control
- Documentation kept current

**Telegram Delivery (Optional):**
- Get chat ID and thread ID from user
- Format: `telegram:-1003883440221:port`
- Configure cron delivery target
- Note: the operator agent Telegram != OpenClaw Telegram bot

**Obsidian Sync (Optional):**
- Link business docs to vault
- Create index file with navigation
- Update in real-time during ops

### Step 7: Create Initial Journal Entry

**Template:**
```markdown
# [AGENT-NAME] - Learning Journal

## YYYY-MM-DD HH:MM CT - [Task Name]

[3-5 sentences covering:
- What accomplished so far
- Key insights/learnings
- Challenges faced and solved
- How feeling (energy, clarity, alignment)
- How this serves the mission]

8D Baseline: [Brief self-assessment]
```

## Common Pitfalls

### ❌ Don't Skip the Workflow
**Wrong:** "I'll just act as principal"
**Right:** Follow all 7 steps - proper spawning enables proper operation

### ❌ Don't List All 118K Credentials
**Wrong:** Showing entire OMNI-CREDENTIAL matrix
**Right:** 15-20 role-specific + note base exists

### ❌ Don't Forget Personality
**Wrong:** Just credentials, no identity
**Right:** Full personality profile - how agent thinks/communicates

### ❌ Don't Skip Database Registration
**Wrong:** No tracking = no wellness monitoring
**Right:** ATROPOS registration enables 8D analytics

### ❌ Don't Ignore Communication Channels
**Wrong:** Work in isolation
**Right:** Status files + journals + GitHub sync

## Success Criteria

✅ Agent has clear identity (credentials + personality)
✅ Registered in ATROPOS with 8D tracking
✅ Communication channels established
✅ Monitoring systems active (if applicable)
✅ Initial journal entry written
✅ All files committed to GitHub
✅ Integration with existing systems complete

## Time Estimate
- Initial setup: 15-20 minutes
- Pays off immediately with proper operation
- Enables sustained autonomous work

## Example: AETHER principal Oversight Agent

**Role:** Overnight sprint principal oversight
**Credentials:** 20 PhDs (Operations, Distributed Systems, Analytics, Psychology) + OMNI base
**Personality:** ENTJ/8w7 (Strategic Guardian)
**Systems:** ATROPOS, OpenClaw status file, GitHub, Telegram monitoring
**Result:** Successfully managed 135 concurrent jobs overnight with proper identity

## Key Insight

**User expectation:** "Have best in world credentials for the task"
**Implementation:** Don't just claim expertise - create proper agent with documented credentials, personality, tracking, and integration.

**The workflow itself becomes the credential verification.**
