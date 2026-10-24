# Agent-Agnostic Coaching Engine Doc Pack

## Use case

Use this pattern when the user wants a repo-ready document set for a coaching engine that any the operator agent agent can continue.

## Naming pattern

- Put the exact branded product line in the top-level title.
- Keep the lead coach name visible, but separate from the repo label.
- Keep the docs usable by any agent, not just the named lead.

Example structure:
- `the specialist engine Engine`
- brand: `Divinity Science`
- lead coach: `the specialist engine`
- scope: `question and response only`
- exclude UI until the conversation contract is stable

## Required docs

- `README.md`
- `process-flow.md`
- `question-flow.md`
- `response-rules.md`
- `state-machine.md`
- `agent-contract.md`
- `persona-guidelines.md`

## Content rules

- Define the product as an agent-agnostic operating system.
- State what is included and what is not.
- Keep the process flow simple and linear.
- Ask one question at a time.
- Keep the response rules direct and usable.
- Include a handoff format so another agent can continue cleanly.

## Good README sections

- Purpose
- Scope
- Operating principle
- Primary use case
- Core docs
- Working rule for all agents
- Naming convention

## Good process docs

- Session start
- Determine if more context is needed
- Narrow the coaching mode
- Gather minimum useful context
- Respond with value
- Continue or close

## Good handoff fields

- Current topic
- User goal
- What we know
- What is still unclear
- Next best action
- State

## Common pitfall

Do not write the pack as if the UI already exists. When the user says to remove taps or buttons, keep the docs strictly conversational until the core flow is stable.
