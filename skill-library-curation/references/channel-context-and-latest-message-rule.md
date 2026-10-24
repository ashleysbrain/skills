# Channel context and latest-message rule

## Why this note exists
This session surfaced a common curation failure mode: a user may report that Telegram or another channel feels "stuck" when the real issue is stale context, a missing file, or the assistant responding to summary state instead of the latest user message.

## Durable lesson
- Treat the latest user message as the source of truth when a context summary conflicts with it.
- If the user says the assistant is stuck, capture the underlying workflow lesson rather than just the symptom.
- When the user signals frustration, the session often contains a reusable skill update even if the change is small.
- Prefer a class-level umbrella patch plus a concise reference note over a narrow one-off skill.

## Curation pattern
1. Patch the umbrella skill that governs the task class.
2. Add a short reference file with the concrete lesson or edge case.
3. Avoid encoding transient channel failures or environment-specific issues as permanent policy.

## Example triggers
- "why are you stuck?"
- "my telegram is stuck"
- "you're responding to the wrong thing"
- "be active"
- "update the skill library"
