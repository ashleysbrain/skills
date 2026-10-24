# Artifact Family Disambiguation

Use this note when a user asks for the "full process" or says the prior answer is incomplete.

## Rule

Before summarizing, identify *which engine family* the user is actually referring to.

Common split in this repo:
- **8D Coaching / the specialist engine** — question flow, intake, advisor selection, state machine, response rules, handoff
- **AISHA-MD / health-self-healing loop** — always-on health monitoring, standup breakdown, 8D validation, cron cadence, support profiles, research-to-experiment iteration

## Why this matters

A nearest-match answer can be wrong even if the docs are internally consistent.
If the user points to a process and says "this isn’t the full process," re-check the artifact family before continuing.

## Practical check

Look for runtime-facing files, not just overview docs:
- coaching: `agents/ds-wave/SOUL.md`, `agents/ds-wave/AGENT.md`, `docs/your-org/coaching-engine/*`
- health loop: `agents/AISHA-MD.md`, `memory/engines/aisha-md.md`, health overlay notes, cron/task sections

## Failure mode to avoid

Do not answer the coaching process when the user is asking about the health/self-healing loop, or vice versa.
