# the specialist engine-Silo System Map Pattern

## Context
The Divinity Science ecosystem has two isolated silos that run in parallel:
- **Silo 1: AI Organism Engine Fleet** — 7 physics engines representing body systems, self-healing via Bernard (AI Clinical)
- **Silo 2: Patient 0 Health Tracking** — the principal's personal 8D wellness scoring via AISHA-MD

The two silos share a Telegram gateway but never exchange data directly. A synergy layer at the bottom shows routing logic.

## Diagram Structure

```
viewBox="0 0 1300 1000"

LEFT (x:30-610)        RIGHT (x:650-1230)       BOTTOM (x:50-1230)
┌─────────────────┐    ┌─────────────────┐     ┌────────────────────────┐
│  SILO 1 (green)  │    │  SILO 2 (violet) │     │  SYNERGY (orange dashed)│
│                 │    │                 │     │                        │
│  Engine row 1   │    │  Telegram GW    │     │  "How am I?"→AISHA-MD  │
│  Engine row 2   │    │  Advisory Pan.  │     │  "Engines?"→Bernard    │
│  Morphogen hub  │    │  AISHA-MD       │     │  Cross-pollination     │
│  Bernard (rose) │    │  8 Dimensions   │     └────────────────────────┘
│  Cron box       │    │  Obsidian Vault │
│  Planned (gray) │    │  Cron box       │
│                 │    │                 │
│  Legend (bottom │    │                 │
│   right corner) │    │                 │
└─────────────────┘    └─────────────────┘
```

## Color Mapping for the specialist engine
| Component | Fill | Stroke | Hex |
|-----------|------|--------|-----|
| Engine / Gateway | cyan-tinted | cyan-400 | #22d3ee |
| Registry / Hub (Morphogen) | amber-tinted | amber-400 | #fbbf24 |
| AI Clinical (Bernard) | rose-tinted | rose-400 | #fb7185 |
| Patient 0 Health Data | violet-tinted | violet-400 | #a78bfa |
| Orchestrator (AISHA-MD) | emerald-tinted | emerald-400 | #34d399 |
| Cron Fleet | orange-tinted | orange-400 | #fb923c |
| Planned / Inactive | slate-tinted | slate-500 | #475569 |

## Key Elements
- Morphogen (hub) sits center-left with faint arrows from all engines pointing into it
- Bernard sits below Morphogen with a dashed rose arrow going UP (heal loop, every 4h)
- Synergy boxes use the "question → routing" pattern, not data-flow arrows
- Legend goes inside the SVG at bottom-right of Silo 1 area (outside both silo boundaries)

## File Location
Output saved to: `/<workspace>`

## Naming Conventions (CRITICAL)
The clinical engine MUST always be labeled:
- Engine name: **Bernard (AI Clinical)** — never just "Clinical" or "Bernard"
- Agent name: **the specialist engine (AI Physician)** — never just "Physician" or "the specialist engine"

This matches the identity hardening in the engine code: it always identifies as an
"Attending AI Physician" and never claims to be a real human physician.
