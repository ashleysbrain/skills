---
name: mosaic-conductor-voice-capture
description: Route voice transcripts to the OS Conductor calendar.
---

# the OS Conductor Voice Capture

## Trigger
When the user sends a voice message via Telegram that arrives as transcribed text
containing actionable content (tasks, deadlines, commitments).

## Process

1. **Assess actionability.** If transcript contains action verbs, deadline
   language, or commitments, proceed. If it's venting/questions/status, respond
   normally and do NOT capture.

2. **POST to capture endpoint:**
   ```bash
   curl -s -X POST "http://localhost:port/api/capture" \
     -H "Content-Type: application/json" \
     -d '{"text": "<text>", "source": "voice", "silo": "gg3"}'
   ```

3. **Report tersely.** "Captured 3: [high] Call the principal, [standard] Review TSC"
   No AI telltales. No "I've successfully."

4. **No duplicates.** Skip if similar task already typed this conversation.

## Collaborator Intake
the principal's messages go to `/api/intake` (trust-tier system), NOT `/api/capture`:
```bash
curl -s -X POST "http://localhost:port/api/intake" \
  -H "Content-Type: application/json" \
  -d '{"text": "<message>", "proposed_by": "principal", "silo": "gg3"}'
```

## Guardrails
- Never POST questions, completed actions, venting, or PHI
- If ambiguous, ask before creating tasks
