# QA Fleet Build Session — 2026-08-20

Session: principal Telegram directives on QA-as-ecosystem; TSC designer-pack PDF
render; brainstorm.db empty-shell discovery. All verified live unless marked.

## principal rulings (verbatim intent, binding)

- D1: "Why do I have to approve engineer builds? ... build it if needed." —
  seat/engine minting autonomous; talent gate still applies; principal sign-off
  only for genuinely-principal matters (renames, publishing, legal).
- D2/3: "I want the qa group to run 24/7. It needs a project and program
  manager ... an entire ecosystem that fuels our organisms trajectory."
- D4: "at least 3" — variance law N>=3 for improvement closure.
- Overnight correction: 24/7 self-correction is an OS property, NOT a
  special overnight watch the agent "sits". Never frame it as overnight idling.

## Historical gap census (the specialist engine, read-only; full text in
## .hermes/cache/delegation/subagent-summary-0-20260820_153956_018159.txt)

1. B2BU organism collaboration — MISSING (4 users share one PIN hash shim)
2. Deep Brainstorm Workbench — PARTIAL (session/split+merge never built;
   workbench tables 2 test rows; brainstorm.db empty orphan, 11 real rows
   in drafts.db)
3. FLW-BRAINSTORM — PARTIAL (Wave :port / Genesis :port named, never called)
4. brainstorm_seeder chain — BUILT-BUT-NEVER-RUN (zero seeds, no cron)
5. Per-angle model override — PARTIAL (models/refresh, model_run,
   model_angles absent from pipeline_api.py)
6. Research DB under-delivery — recurring trust gap since 08-07
7. LinkedIn pipeline — PARTIAL (template built; live run stalled 12 polls
   at 0 chars)
8. Bulk/batch brainstorm — BUILT (fully landed)
9. Topic recommendation — BUILT (verified)
10. gap_hunter "5x/day" — claimed before it existed (real: 4x/day)
11. qa_verdicts.db / pipeline_runs.db / build_queue.db — empty shells

## Five failure patterns (detector signatures for S8/S9)

1. built-but-never-run (DOMINANT; empty DB shells are the smoking gun;
   invariant = usage-verification: row counts, cron registration,
   live-call proof)
2. designed-documented-never-wired
3. claimed-live-before-verification
4. delivered-then-lost (auto-save missing; route shadowing; evidence
   flattened to string)
5. silent-degradation (stalls without failure signal; poll loops showing
   running/0-chars forever)

## Exact mint recipe (what submit() enforces, learned by rejection)

- Lane must exist in stores/task-taxonomy.json `lanes` first, else
  ValueError: unknown lane.
- kind=build REQUIRES GENOME block in detail WITH the 8d field:
  `GENOME: body=immune scientist=the specialist engine physics="..." 8d=intellectual`
  (missing 8d = gate rejection; the error message omits it — see below)
- Flow stages: submit(stage="minted") warns off-vocabulary for
  FLW-QA-FLEET (its stages are sense/appraise/mint/dispatch/verify/learn);
  normalize with task_ledger.set_stage(c, tid, "mint").
- ORGANS.json: dict with `organs` list + `organ_count` to update.
- REAL ledger: your-stack/stores/task-ledger.db (tl.LEDGER).
  organism/task-ledger.db is an empty-shell path with no tasks table —
  never verify against it.

Minted this session: FLW-QA-FLEET (flow-registry 1.1.0 -> 1.2.0), immune
lane (taxonomy 1.1.0), seats the specialist engine (DS-ECS-IMM-13.08.01) + the specialist engine
(DS-ECS-IMM-03.07.01), tasks T-260820-0145..0148.

## Genome-gate error message quirk

The rejection message shows the format WITHOUT the 8d field:
`Format: GENOME: body=<system> scientist=DS <Name> physics="<principle>" 8d=<dimension>`
— actually it does show 8d. First attempts failed because the GENOME
constant lacked ` 8d=intellectual`. Always include all four fields.

## PDF render session notes (ds-branded-pdf-render companion)

- scripts/ds-md-to-pdf.py had a genuine SyntaxError (f-string backslash,
  invalid pre-3.12; venv python is 3.11). Fixed in place 2026-08-20:
  hoist `re.sub` into a plain variable before the f-string. Pattern for
  any future f-string backslash error in that script family.
- WeasyPrint lives in /<workspace> (69.0),
  NOT the default interpreter.
- Verification without vision tool: pdftoppm -png + PIL pixel sampling
  (cover: dark-navy ratio ~87%, gold accents; content pages: light-paper
  ratio >95%) + pdftotext greps (brand words present, zero raw table
  pipes). Cheap and quantitative.
