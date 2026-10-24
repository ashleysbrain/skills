---
name: voice-message-diagnosis
description: Diagnose and fix voice message transcription issues when user reports messages are not being received
triggers:
  - User reports sending voice messages that agent did not receive
  - Voice transcription appears broken
  - Agent missing context from voice content
category: troubleshooting
platforms: [gateway, telegram, discord, whatsapp, signal]
---

# Voice Message Diagnosis & Recovery

## Problem Pattern

User sends voice messages but agent responds as if no message was received. Agent has no context from the voice content.

## Diagnostic Steps

### 1. Check Gateway Logs
Check if voice messages were received and transcribed:
- Look for "Cached user voice at" entries
- Look for "Processing audio with duration" entries
- Look for "Detected language" entries

### 2. Check Audio Cache
Verify audio files exist in cache directory (shows messages were received)

### 3. Manually Transcribe Cached Audio
Use transcription tools to manually recover transcripts from cached audio files

### 4. Batch Recovery of Recent Messages
Script to transcribe multiple recent cached audio files in chronological order

## Common Root Causes

### Gateway Transcribing But Agent Not Receiving

**Symptoms:**
- Gateway logs show transcription completed
- Audio cache has files
- Manual transcription works
- Agent still has no context

**Cause:** Enrichment happening but not passed to agent conversation history

**Fix locations:**
- Check enrichment call in gateway run file
- Check enrichment function implementation
- Verify enriched text added to conversation history before agent call

### Configuration Issues

Check STT enabled in config and verify local transcription provider installed

## Recovery Protocol

1. **Acknowledge the gap immediately**
   - Never pretend you got context you do not have

2. **Manually recover transcripts**
   - Use transcription tools to extract content from cached audio
   - Present full transcripts to user

3. **Act on recovered content**
   - Execute instructions from the transcripts immediately
   - Do not ask permission again if user already gave it

4. **Document the failure**
   - Note exact failure point (enrichment, handoff, config)
   - Include relevant log information
   - Track which messages succeeded vs failed

5. **Fix root cause**
   - Address identified issue
   - Add monitoring for transcription to context handoff
   - Test with new voice message before declaring resolved

## User Communication Best Practices

**Avoid:**
- Dismissing user report
- Claiming system works when user says it does not
- Asking user to resend messages

**Do:**
- Investigate logs immediately
- Show recovered transcripts
- Execute on recovered instructions without delay

## Prevention

Add health checks to verify voice message enrichment reaches agent context. Test periodically with voice messages to catch failures early.

## When to Use This Skill

- User explicitly reports sending voice messages
- User references content you have no context for
- Pattern of conversation gaps
- User frustration about repeating themselves

## Success Criteria

- All recent voice messages recovered and transcribed
- User instructions from voice messages executed
- Root cause identified and documented
- Fix deployed or escalated
- User confidence restored

---

**Key Insight:** Voice transcription can succeed at gateway level but fail to reach agent context. Always verify BOTH gateway logs AND agent received context.
