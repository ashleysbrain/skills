# the operator agent coaching-engine end-to-end verification

## What this checks
Use this when validating a persona-driven coaching engine or a long-running coaching thread inside the operator agent itself.

It verifies two separate behaviors:
- **short-form coaching**: one-turn, direct, actionable response
- **long-form continuity**: resumed session keeps state and updates the same thread rather than restarting

## Practical verification pattern
1. Run a short prompt that forces a concise coaching answer.
2. Run a longer prompt that asks for a plan or structure and confirms the smallest useful question is asked.
3. Resume the same session with a new constraint.
4. Confirm the agent updates the existing thread instead of resetting it.

## Example command shape
```bash
hermes chat -q --profile default "<prompt>"
hermes chat --resume <session_id> --profile default -q "<follow-up constraint>"
```

## What to look for in the output
- The coach stays on persona and avoids generic assistant drift.
- The short answer is compact and actionable.
- The long thread stores state and can be resumed.
- The follow-up modifies the current plan rather than starting over.
- The reply includes the smallest useful next question when the goal is still underspecified.

## Common pitfalls
- Passing the resume flag to a fresh session does not test continuity; you must reuse the session ID from the prior run.
- If the prompt is too broad, the thread may become generic; keep the verification ask narrow.
- A good long-thread test should include at least one follow-up constraint that changes the plan without changing the goal.
