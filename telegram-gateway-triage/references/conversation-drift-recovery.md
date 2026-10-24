# Conversation drift recovery notes

## Session pattern
- The user said the chat was "stuck".
- I incorrectly shifted into Telegram delivery triage and then into an unrelated repo/board task.
- The user corrected that: the issue was *not* Telegram triage.
- The right recovery was to stop the stale thread and ask for the actual task to retry.

## Recovery rule
When the user rejects the current interpretation, do not keep elaborating on the stale interpretation. Reset to the latest valid user instruction and restate it briefly before acting.

## Bad follow-up to avoid
- Do not continue diagnosing Telegram if the user says that is not the task.
- Do not invent a related task from stale context.
- Do not answer a different repo or workflow than the user explicitly named.

## Good recovery response shape
- Acknowledge the mismatch in one short sentence.
- State the current task boundary.
- Ask for or restate the exact thing to redo.
