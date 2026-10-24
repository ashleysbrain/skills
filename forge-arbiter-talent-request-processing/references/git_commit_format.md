# Git Commit Message Format for Talent Request Processing

Use the following format when committing changes after processing a talent request:

```
Process talent request: <request-filename>.md; dispatched to <agent>; no spawn
```
or if an agent was spawned:
```
Process talent request: <request-filename>.md; spawned <agent>
```

Examples:
- Process talent request: 2026-05-30-hydra-gd-payment-migration.md; dispatched to the specialist engine; no spawn
- Process talent request: NEW-AGENT-PROPOSAL.md; spawned DS NEWAGENT

Keep the message concise and under 72 characters if possible.