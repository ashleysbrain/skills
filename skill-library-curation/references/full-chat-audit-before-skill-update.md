# Full chat audit before skill updates

## Trigger
Use this note when the user asks to review the conversation above, find everything that matters, or says the assistant missed part of the ask.

## Lesson
Do not update the skill library from the most obvious fragment only. First audit the full thread for:
- explicit user corrections
- implied workflow changes
- tone/verbosity complaints
- scope-expansion language such as "everything", "all of it", or "don't be lazy"

## Practical checklist
1. Read the latest user message in full.
2. Read the surrounding conversation for earlier corrections or constraints.
3. Separate the immediate symptom from the durable workflow lesson.
4. Save the durable lesson in the class-level umbrella skill.
5. Put session-specific detail in a reference file instead of the main SKILL.md.

## Why it matters
The user may be correcting the breadth of the audit, not just the final answer. Capturing only the narrowest issue leaves the skill library blind to the real failure mode.