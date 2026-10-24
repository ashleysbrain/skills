# Telegram Question/Response Coaching Flow Pattern

## When to use
Use this pattern when the user wants a Telegram-first coaching engine but wants to *exclude* button/tap UI for now. The first deliverable should be a question-and-response flow that any the operator agent agent can continue.

## Core rule
Keep the product framed as a conversational engine, not a UI system.

- Ask one question at a time
- Accept free-text replies
- Respond with the next best question or the next best action
- Avoid menu trees, inline buttons, or tap-based navigation until explicitly requested

## Doc set to produce
When the repo is intended for a broader team or multiple agents, write docs that are agent-agnostic:

- `README.md` — project purpose and how any agent should use the repo
- `docs/overview.md` — scope, boundaries, and operating assumptions
- `docs/process-flow.md` — end-to-end conversation journey
- `docs/question-flow.md` — question order, branching, and follow-up logic
- `docs/response-rules.md` — how the engine should answer, summarize, and redirect
- `docs/state-machine.md` — session states and transitions
- `docs/agent-contract.md` — what any the operator agent agent must do when picking up the repo
- `docs/persona-guidelines.md` — voice, tone, and boundaries for the specialist engine and siblings

## Practical flow shape
1. Open with a broad starter question.
2. Narrow with one clarifying question if needed.
3. Respond with a short summary, a recommendation, or a next-step prompt.
4. Continue until the user has enough clarity or action.
5. Preserve a simple handoff format so another agent can resume without context loss.

## Pitfall to avoid
Do **not** draft Telegram button maps, tap hierarchies, or UI navigation docs unless the user explicitly asks for UI work. If the user says "for now" or "just questions and response," treat that as a scope lock.

## Handoff expectation
The docs should be written so that:
- the principal's the operator agent agent can execute them
- other the operator agent agents can execute them
- the repo can later become a team-wide shared coaching engine without rewriting the foundation

## Good wording patterns
Prefer terms like:
- conversational flow
- question sequence
- response rule
- handoff contract
- agent-agnostic process
- session state

Avoid over-committing to:
- Telegram UI
- buttons
- taps
- menus
- screen-by-screen navigation
