# Mint storm, absence-claim audit, and the approval-drain loop (2026-08-28 session)

## The mint storm (22 duplicates)

**Sequence:** principal audio directives landed in a desktop sister thread Thursday.
principal asked next morning "you missed my audio callouts." Orchestrator queried
the task ledger with `origin LIKE 'ceo%' AND date(created_at) >= ...` — the
overnight bridge-responder mints used different origin strings and fell
outside the filter. Conclusion "never minted" was WRONG; the orchestrator
minted all 14 again, joining 2 earlier duplicate batches (T-260828-0058..0079
were themselves re-mints of T-260827-0084+ items).

**Dedup pattern (worked clean):**
1. Build `CANONICAL = {title-prefix-40-chars: keep-ticket}` keeping the
   richest batch (GENOME block + full audio context).
2. `UPDATE tasks SET state='cancelled', outcome='dup-of <canonical>'`.
3. Log a `dedup` task_event per row explaining why.
4. Verify: `SELECT id, state` on sample ids — cancelled vs open.

**Prevention laws minted in-session:**
- principal directives mint AT RECEIPT in every thread; weekly sweeps are backstop
  only (the Tuesday-only sweep was why nothing caught the gap).
- Batch mints run through the premint dedup scan (title-similarity) — the
  gate existed for single mints; batches bypassed it.

## Absence-claim verification law

"Never minted" was asserted from one filtered query. Absence claims need the
widest net: content-prefix search across ALL origins, all dates, sibling
stores. See verification-patterns §BUILT ≠ WIRED ≠ RUNNING.

## The approval-drain loop (principal directive, T-260828-0106)

principal approvals/notes were landing as bus messages and sitting pending (e.g.
#5780 $300 budget approval stagnant hours). principal law: approvals must be
ACTIONED immediately and cleared from the approval inbox — never stagnant.

Build shape: watch principal-approval events on every surface (bus acks, telegram
button presses, desktop approvals) → immediately action the underlying task
(execute decision, apply note, mint follow-on) → mark approval consumed →
surface confirmation. Stagnant-approval detector: awaiting-principal >2h while principal
active = alert.

Related context-not-skill items (task ledger, not skill): dynamic data views
T-260828-0101; QA extensiveness law T-260828-0104 (glial/QA reviews MORE
extensive than research+adversarial combined).
