# Chat Review Memory + Skill Capture

## Durable lesson
When the user asks to "review the conversation above" and update memory/skills, treat it as a curation pass, not a summary request.

## Procedure
1. Audit the immediate user turn and the assistant's last turn for drift.
2. Extract the user's actual ask separately from surrounding context.
3. Save *stable* user preferences to memory.
4. Save *reusable workflow lessons* to the governing umbrella skill.
5. If the user expressed frustration about being stuck, wrong-threaded, or misread, capture the underlying workflow mismatch rather than the transport symptom.

## What to preserve
- context-drift sensitivity
- exact, grounded answer expectations
- the rule that conversation-review requests should result in durable updates when a real lesson exists

## What not to preserve
- one-off topic details
- temporary session outcomes
- environment-specific failures
