---
name: agent-failure-output-continuity
description: Procedure for maintaining required output production when the responsible agent is in failure state, using alternative intelligence sources
trigger: Designated agent for a recurring task shows persistent errors in coordination logs or fails to produce expected outputs
version: 1.0
---

# Agent Failure Output Continuity Procedure

## 🎯 WHEN TO USE
When the agent responsible for producing a recurring output (daily brief, report, update, etc.) is in a persistent failure state (showing consecutive errors in coordination logs, missing expected outputs, etc.) but the output still needs to be produced for stakeholders.

## 🚨 CRITICAL PRINCIPLES
1. **Never fabricate information** - Only report what is actually present in available intelligence sources
2. **Document the failure situation** - Clearly indicate in the output that the responsible agent is experiencing issues
3. **Maintain stakeholder trust** - Provide useful contextual information even when automation is degraded
4. **Follow all output formatting and content rules** - Adhere to existing standards for the output type
5. **Avoid PHI/sensitive data** - Keep outputs partner/stakeholder-safe per existing guidelines

## 📋 PROCEDURE

### 1. Verify Agent Failure State
- Check coordination logs for consecutive error counts from the responsible agent
- Look for timeout errors, authentication failures, or other persistent issues
- Note the error duration and pattern (from journal entries if available)
- Example command: `tail -50 /path/to/coordination.log | grep "agent-name"`

### 2. Gather Available Intelligence
Since the agent cannot run its normal intelligence gathering:
- **Check for expected inputs** (standup transcripts, sensor data, etc.) - note if missing/outdated
- **Review coordination logs** for recent scans, alerts, and updates from OTHER agents
- **Read latest journals** from related agents (especially the failing agent's own journal)
- **Look for health alerts, dimensional focuses, scan results** in the intelligence feed
- **Check for wellness/vital data** through alternative means if normally agent-collected

### 3. Extract Required Output Components
From the gathered intelligence, extract:
- **Energy/mood observations**: From coordination logs, journals, or noted patterns (do NOT invent)
- **Work summary**: What intelligence was processed, what alerts were seen
- **Dimension focus**: Which of the 8D dimensions appeared most/least in recent intel
- **Patterns for stakeholders**: Systemic issues, recurring alerts, risk factors identified
- **Tomorrow's focus**: Infer from pending scans, stated intentions in journals, or ongoing projects
- **Schedule adjustments**: Based on observed failure patterns or recommended remedies

### 4. Produce the Output Document
- Use the standard format/template for the required output type
- Clearly contextualize that this was produced during agent downtime
- Include only verified information from logs/intel
- Follow all tone, formatting, and content rules for the output type
- Example section headers to adapt:
  - Energy and Mood Observations
  - What [Person] Worked On Today
  - Dimension Focus and Neglect
  - Patterns for [Stakeholder] Awareness
  - Tomorrow's Focus Areas
  - Schedule Adjustments Recommended

### 5. Execute Required Follow-up Actions
- Perform any mandatory posting/committing steps (git push, message sending, etc.)
- Write an entry in the failing agent's own journal documenting:
  - The failure state persisted
  - What alternative intelligence sources were used
  - What output was produced manually
  - Recommendations for restoring normal operation
- Follow any established journaling format for the agent

### 6. Recommend Restoration Actions
Based on observed failure patterns:
- Suggest specific configuration fixes (API keys, auth files, etc.)
- Recommend error escalation protocol improvements if not present
- Suggest validation checks for future early detection
- Note if centralized remediation would be more efficient than agent-by-agent

## 📝 EXAMPLE: AISHA-MD FAILURE STATE
*(Based on actual 2026-04-09 execution)*

When AISHA-MD showed 10+ consecutive errors due to missing Google API key:
1. Verified failure via coordination logs showing "FailoverError: No API key found"
2. Gathered intel from:
   - Coordination logs (environmental, epigenetics, neurodivergence scans)
   - Latest AISHA-MD journal (2026-04-05 documenting error state)
   - Absence of today's standup transcript (indicating collection failure)
3. Extracted:
   - Energy/mood: Agent error state + ADHD-suicide genetic link alert
   - Work: Processing intelligence feeds from other agents via logs
   - Dimension focus: ENV, PSY, GENOME prominent; PHY less represented
   - Patterns: Systemic agent reliability issues (multiple cron jobs with high CE)
   - Tomorrow's focus: Error resolution + risk monitoring protocols
   - Schedule rec: Prioritize auth config repair, consider manual check-ins
4. Produced daily update to the principal's partner hub following all formatting rules
5. Wrote AISHA-MD journal entry documenting failure and manual output
6. Recommended: Fix Google API key in auth-profiles.json, implement error escalation

## ⚠️ PITFALLS TO AVOID
- **Do not speculate** about medical conditions, medication changes, or unverified symptoms
- **Do not hide** the agent failure situation - stakeholders need to know automation is degraded
- **Do not skip** output formatting rules just because manual production was needed
- **Do not neglect** to document the failure in the agent's own learning journal
- **Do not assume** that missing data means nothing happened - report the absence itself as data
- **Do not violate** PHI restrictions - when in doubt, leave it out

## ✅ VERIFICATION
Before considering the task complete:
- [ ] Output contains only information actually found in logs/intel
- [ ] Agent failure situation is clearly acknowledged
- [ ] All required output sections are addressed with available data
- [ ] Tone and formatting match the standard for this output type
- [ ] No PHI, medication names, dosages, or diagnosis labels included
- [ ] Required follow-up actions (commit/push, journaling) were executed
- [ ] Agent's own journal documents the failure and manual work performed