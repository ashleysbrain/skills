# Cross-Repo Advisory Handoffs

## Pattern
When a workflow is split across private advisory repos (for example: principal, product, marketing, elite), do not rely on chat history alone.

Create a small, repo-local artifact in the receiving repo that makes the upstream review actionable.

## Recommended artifact types
- `*_HANDOFF.md` — one upstream board’s review turned into downstream next steps
- `COACHING_QUESTIONS.md` — the first question set for the receiving board
- `COACHING_CONTEXT.md` — durable repo-local reminders about how to use upstream context
- `HISTORY.md` — a short factual note that the handoff exists

## Sequence
1. Read the receiving repo’s README / PROCESS / existing context.
2. Write a handoff note that translates upstream review into downstream next steps.
3. Add a first-round question set so the board can answer one seat at a time.
4. Update repo-local coaching context so future sessions know to use the upstream review.
5. Add a brief history entry.
6. Verify the repo is clean and push the repo itself only.

## Useful constraints
- Keep advisor outputs separate unless synthesis is explicitly requested.
- Ask one useful question at a time in coaching mode.
- Preserve the distinction between boards: upstream review informs the next board, but does not replace its judgment.
- Keep each repo private and scoped to its own lane.

## Example handoff flow
- Marketing review → product next steps
- Product review → marketing launch/message refinements
- principal review → product/marketing direction guardrails

## Notes
This pattern is especially useful when the user wants "Wave mode" or another multi-board operating mode activated again after a handoff.
