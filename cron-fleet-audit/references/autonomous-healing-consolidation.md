# Autonomous Healing Consolidation Pattern

When deploying a new autonomous healing system (e.g., Bernard Engine / the specialist engine),
use this pattern to build the closed-loop scanner and consolidate redundant fleet jobs.

## Architecture

```
Advisory Panel Crons → cron/output/*.md
                              ↓
                    Auto-Heal Scanner (Python)
                    ├── pattern-matches infrastructure issues
                    ├── checks engine health endpoints
                    └── writes diagnosis JSON
                              ↓
                    Healing Cron Job (every 4h)
                    ├── reads latest diagnosis
                    ├── reads advisory recommendations
                    ├── deploys fixes autonomously
                    └── writes SOAP clinical notes
```

## Key Design Decisions

1. **Scanner is a standalone Python script** — not an agent. It runs deterministically,
   no LLM needed. Fast, cheap, reliable.

2. **Healing cron IS an agent** — it reads the scanner output + advisory outputs and
   makes decisions about what to fix. This is where reasoning is needed.

3. **Never delete jobs, always pause** — the consolidation is reversible. If the new
   healing system fails, you can resume the old jobs.

4. **Every 4 hours is the sweet spot** — frequent enough to catch issues before the
   next principal advisory board cycle, infrequent enough to not waste API calls.

## What to Pause After Deployment

When the autonomous healing system goes live, immediately pause:
- Fleet health check jobs (VITALS, NEXUS Auto-Remediation)
- Fleet wellness/self-healing cycles (any "self-healing" or "wellness panel" jobs)
- Daytime cron audit jobs (the healing system covers fleet health continuously)
- Any standalone remediation engine that the new system subsumes

Typical result: 4-6 jobs paused, ~20% reduction in active fleet, zero loss of coverage.

## Scanner Script Template

The scanner lives at `ds-clinical-engine/auto_heal_scanner.py` and:
- Scans `<agent-home>/cron/output/*/` for recent `.md` files (last 24h)
- Regex-matches for: cron failures, context limits, panel deaths, engine downs,
  build errors, missing files
- Pings all engine health endpoints (ports 8000, 8089-8094)
- Writes structured diagnosis JSON to `ds-clinical-engine/diagnoses/`

## SOAP Note Format

The healing agent documents every fix as a clinical SOAP note:
- **S**ubjective: What the advisory boards reported
- **O**bjective: What the scanner found (engine status, error counts)
- **A**ssessment: Root cause diagnosis for each issue
- **P**lan: What fix was deployed and verification result

Notes are saved to `ds-clinical-engine/rounds/SOAP_{timestamp}.md`.

## Escalation Rules

The healing agent should only escalate to the principal when:
- A fix requires money or external credentials
- A fix could break production (needs human judgment)
- An engine is fundamentally broken (not just down/restartable)
