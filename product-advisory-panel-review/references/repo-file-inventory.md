# CPO Repo File Inventory

Quick reference for the `ds-wave-product-advisory-panel-private` repo. Use this to locate files without guesswork.

## Canonical Files (read every session)

| File | Purpose |
|------|---------|
| `manifest.yaml` | Locked advisor roster, board config. READ FIRST. |
| `PRODUCT_COACHING_CONTEXT.md` | Durable coaching context, 4 coaching modes. |
| `COACHING_CONTEXT.md` | Duplicate of above (identical content). |
| `PRODUCT_THESIS_V1_LOCKED.md` | Locked product thesis v2 (June 10, 2026). |
| `ARCHITECTURE.md` | Resonance + Mastermind model, system overview, data flow. |
| `PERSONALITIES.md` | Personality calibration system, presets, neurodivergent adaptations. |
| `COACHING_QUESTIONS.md` | 5-question set the board tracks answers to (Marty, Ries, Fogg, Topol, Dunford). |
| `CTO_BRIEF.md` | the principal build direction, safety modes (sandbox/review/live), first-release scope. |

## Coach Files

All in `coaches/` directory. Manifest is the canonical roster.

| File | Coach | Lane |
|------|-------|------|
| `coaches/marty-cagan.md` | Marty Cagan | Product Strategy & Operating Model |
| `coaches/eric-ries.md` | Eric Ries | Lean Product Development |
| `coaches/bj-fogg.md` | BJ Fogg | Behavioral Design |
| `coaches/eric-topol.md` | Eric Topol | Health Technology |
| `coaches/april-dunford.md` | April Dunford | Product Positioning |

## Other Files (reference as needed)

| File | Purpose |
|------|---------|
| `HISTORY.md` | Repo change log (short) |
| `DOC_INDEX.md` | Document index |
| `PROCESS.md` | Board process doc |
| `INTEGRATION.md` | Cross-repo integration notes |
| `MARKETING_REVIEW_HANDOFF.md` | CMO board handoff to CPO |
| `FOUNDER_NARRATIVE_OUTLINE.md` | Founder narrative |
| `PIML-STRATEGIC-PIVOT-BRIEF.md` | PIML pivot context |
| `PIML-MARKETING-BRANDING-BRIEF.md` | PIML branding context |
| `PIML-TEAM-STRUCTURE.md` | PIML team structure |

## Known Naming Variations

- Context file: repo has both `PRODUCT_COACHING_CONTEXT.md` AND `COACHING_CONTEXT.md` (identical). Skill says use `PRODUCT_COACHING_CONTEXT.md`.
- Thesis: `PRODUCT_THESIS_V1.md` (draft), `PRODUCT_THESIS_V1_FINAL.md` (pre-lock), `PRODUCT_THESIS_V1_LOCKED.md` (locked v2). Use the LOCKED version.

## PDF Generation

```bash
python3 /<workspace> /tmp/product-review-YYYY-MM-DD.md /tmp/product-review-YYYY-MM-DD.pdf "Product Advisory Panel" "AM"
```

Script location: `/<workspace>`. Confirmed working as of June 2026.

## Repo Staleness Pattern

As of June 2026, this repo goes stale frequently (weeks between commits). The skill's stalemate handling guidance applies: frame reviews around what is stuck, not manufacturing progress. Check `git log --oneline -1` to confirm staleness at start of each run.
