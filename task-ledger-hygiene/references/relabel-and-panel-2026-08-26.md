# Relabel + 12-seat panel session — 2026-08-26

Full session record backing the task-ledger-hygiene skill.

## Census (before → after)
- Active tasks 558 → 535 (23 true dupes/double-tracks retired)
- Titles >100ch: 247 → 0. Titles >80ch: 177 → 0. No-signal: 113 → 0.
- Identical-title clusters: 9 → 0. Off-taxonomy lanes: 70 → 0.
- Unfenced archives: 245 → 0 (all fenced + moved to bottom of detail).
- Relabel events: 946 (append-only; sha256 anchors).
- Backup: `stores/task-ledger.db.bak-260826-relabel`.

## Defect classes found (12-seat panel, 66 findings → 7 root causes)
A. Duplication (9 seats): 12x organ cluster flattened by mechanical cut;
   5x THINKERY passes; 7 epoch-dup pairs; 5 GAP+BUILD double-tracks.
B. kind=build misfiles: doctrine/umbrella/readout/spec-study/daemon rows.
C. Signal grammar drift: EVOLVE(45) QA-META(24) DECISION(7) NOETHER/SEC/WAVE/
   [AUTO]/[bus N] as primary signals; coverage was 52%.
D. Archive at top of detail burying live content; no end fence.
E. Ceiling: stats seat REJECTED 70/60 (marginal gain vs 3x rewrite cost); 80 held.
F. Mint gate absent: 30 new >80ch titles regrew DURING the panel.
G. Machine consumers: grammar fold blinded law_state.py (LIKE 'DECISION:%').

## Fixes applied (order)
1. Lane rulings (70 rows, per-row content read, S1 specialist)
2. Format spec (10 kinds, S2 specialist) + mechanical verbatim-substring
   rewrite engine (orchestrator-built — principal correction: build, don't only delegate)
3. Disambiguation passes (organ tokens from detail JSON)
4. Epoch-dup closures: `dup-of` outcomes, older epoch survives
5. Grammar fold: rogues → trailing [qualifiers]
6. Archive rework: fence + move to bottom + sha256 anchors
7. Mint gate in submit(): hard >200, advisory log >80/no-signal; 4-case battery
8. Consumer grep-and-patch (law_state.py DECIDE:)

## Panel verdicts
12/12 completed (1 rate-limited summary, file intact). All REVISE or
PASS_WITH_NOTES. Late async reports post-revision yielded 14 more fixes —
late-report ingestion is mandatory, not optional.

## Residuals (filed in audit/RUN-RECORD.md, honest queue)
- kind misfiles need taxonomy ruling (GENOME gate consequence)
- 25 all-caps titles (acronym risk in mechanical case-fold)
- 18 raw [ML-watch] bookmark rows (intake design question)
- `legal` lane used but never canonized in task-taxonomy.json
- dep-stale state semantics (19 rows) → sibling-agent lane
