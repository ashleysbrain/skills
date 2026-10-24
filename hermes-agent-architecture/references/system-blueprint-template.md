# System Blueprint Template

Use when creating or updating the comprehensive the specialist engine system blueprint.
The blueprint is a living document at `/<workspace>`.

## Structure (7 sections)

1. **Engine Fleet** — table of all 7 engines (port, body system, agent, scientist, status)
2. **the operator agent Agent Fleet** — table of all profiles (8 builder + 1 patient interface)
3. **Two-Silo Architecture** — Engine Fleet (self-healing 24/7) + Patient 0 Health Tracking (user schedule)
4. **Advisory Panel Architecture** — two-layer model: AI-prefix boards (advise) + DS-prefix agents (execute)
5. **Engine Integration Map** — ASCII topology, data flow description, self-healing loop
6. **Cron Job Fleet** — table of all scheduled jobs (job, agent, schedule, purpose) per silo
7. **Remaining Build Items** — categorized as Immediate, Near-Term, Architecture
8. **Governance Rules** — numbered list of hard rules (no Anthropic, boards vs agents, PIML, clinical identity, two-silo isolation, etc.)

## Key Principles

- **Living document** — update whenever engines, agents, or panels change
- **All 7 engines** must appear in the fleet table with current status
- **Governance rules** are hard constraints, not suggestions
- **Two-layer architecture** is non-negotiable: boards ADVISE, agents EXECUTE
- **Clinical engine** must always be listed as "Attending AI Physician"
- **Two-Silo Architecture** — Engine Fleet (Silo 1) and Patient 0 (Silo 2) are completely isolated: different scoring, agents, memory, cron, Telegram routing

## Update Triggers

- New engine deployed or registered
- New the operator agent profile created
- New advisory panel added
- Cron job added/removed/changed
- Governance rule added or changed
- Build item completed (move from Remaining to done)
- Silo boundary change (never merge Silo 1 and Silo 2)
