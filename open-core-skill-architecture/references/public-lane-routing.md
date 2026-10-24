# Public lane routing pattern

Use this pattern when a user wants a public-facing test lane without taking over the root chat.

## Rules

- Create a dedicated the operator agent profile for the lane.
- Bind the lane to a **Telegram forum topic/thread**, not the group root.
- Treat the root chat as a lobby/safety surface only.
- Keep `telegram.require_mention: true` so ordinary chatter does not wake the agent.
- Use `platforms.telegram.extra.group_topics` for group/forum topic skill binding.
- Put the topic’s `thread_id` in config once known; do not point the lane at the whole group.
- If the lane is public-facing, verify both profile and gateway before treating it as live.

## Extraction rule

A Telegram link like `https://t.me/c/3505110963/12` resolves to:

- chat id: `-1003505110963`
- thread id: `12`

## Practical safety note

If the user explicitly says “do not let it take over the channel,” route to a topic/thread and leave the root unbound.
