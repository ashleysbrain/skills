# Document Versioning Convention

**Established:** 2026-06-10 (session with the principal Williams, principal)

## Naming Format

```
{DOC_TYPE}_v{MAJOR}.{MINOR}_{YYYY-MM-DD}T{HHMM}.pdf
```

## Document Type Prefixes

| Prefix | Description |
|--------|-------------|
| `THESIS` | Product thesis / strategy docs |
| `CEO_BRIEF` | principal daily briefs |
| `BOARD_BRIEF_{BOARD}` | Board review outputs (e.g., `BOARD_BRIEF_MARKETING`, `BOARD_BRIEF_PRODUCT`) |
| `CHECKLIST` | Action checklists / MVP checklists |
| `REVIEW` | Review outputs |
| `SCORECARD` | TWC / 8D scoring outputs |
| `PROTOCOL` | Process protocols / SOPs |
| `SPEC` | Technical specifications |
| `TALENT` | Talent requests / agent profiles |
| `MEMORY` | Memory updates / context dumps |

## Version Rules

- **Major (vX.0)**: Fundamental restructure, new scope, locked thesis
- **Minor (vX.Y)**: Updates, additions, clarifications within same scope
- **Patch (vX.Y.Z)**: Typo fixes, formatting only

## Examples

```
THESIS_v1.0_2026-06-10T1145.pdf      # Locked product thesis v1
THESIS_v1.1_2026-06-11T0930.pdf      # Added competitive analysis
THESIS_v2.0_2026-06-15T1400.pdf      # Post-MVP scope expansion

CEO_BRIEF_v1.0_2026-06-10T0600.pdf   # Morning principal brief
CEO_BRIEF_v1.1_2026-06-10T1200.pdf   # Midday update
CEO_BRIEF_v2.0_2026-06-11T0600.pdf   # Next day brief

BOARD_BRIEF_MARKETING_v1.0_2026-06-10T1000.pdf
BOARD_BRIEF_PRODUCT_v1.0_2026-06-10T1000.pdf

CHECKLIST_v1.0_2026-06-10T0800.pdf   # MVP checklist
CHECKLIST_v1.1_2026-06-10T1500.pdf   # Updated after thesis lock
```

## Telegram Delivery

Every document sent to Telegram uses this naming. The file name itself carries the version history. No need for separate version tracking — just search Telegram for the doc type + date.

## Auto-Generation

Cron jobs that produce deliverables MUST include the versioned filename in their output path. The agent generating the doc determines the version based on:
1. Does a vX.0 for this date exist? → vX.1
2. Is this a new scope/lock? → vX+1.0
3. First of its kind today? → v1.0

## Related Files

- `FOUNDER_NARRATIVE_v1.0_2026-06-10T1230.pdf`
- `PRODUCT_THESIS_v1.0_2026-06-10T1145.pdf`
- `CEO_DAILY_ACTIONS_v1.0_2026-06-10T0600.pdf`
- `DOCUMENT_VERSIONING.md` (in product advisory panel repo)