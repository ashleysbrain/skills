# Pending skill updates (2026-08-18 evening session) — merge into targets when foreground edit unblocks

Curator note: background _read_before_write guard refuses patches to
existing files this session (dedup views never count). Content below is
final; merge verbatim into the named target sections.

## TARGET 1: references/org-relocation-2026-08-18.md
Append after "Dead mirror detection" decision rule:

### Post-deletion: presence via symlink (2026-08-18 follow-up)
principal follow-up: "Mosaic is methodology with the desktop thread" — the
Desktop INTELLIGENT-OS thread keeps PROCESS-FLOWS.md as its own working
draft and must retain ACCESS to the methodology. Deleting the dead
mirror was right; leaving nothing behind was not. Fix:
`ln -s ~/your-org/your-stack ~/Desktop/INTELLIGENT-OS/your-stack`
- A symlink makes divergence physically impossible: one source of
  truth, every entry path converges on canonical.
- ROOT CAUSE of the mirror's reappearance hours after deletion: a
  sibling session still pointed at the old path minted T-260818-0167
  into it, recreating empty stores/. Stale-path writers KEEP
  resurrecting shells until every path converges — the symlink IS the
  convergent fix, deletion alone is not.
- Gotcha: `ln -s` into an existing dir puts the link INSIDE it. Remove
  the dir first, then link.
- Verify live THROUGH the symlinked path (task count, git log, store
  health) — proof must come from the door users actually enter.

## TARGET 2: references/ledger-api-gotchas-2026-08-18.md
Insert before "## Surgical gate":

### Exact call signatures (re-verified 2026-08-18)
- `submit(c, title, kind, lane, origin, created_by, **fields) -> str`
  — kind/lane/origin/created_by ALL required. kind must exist in
  stores/task-taxonomy.json; valid kinds (2026-08-18): build, defect,
  gap, verify, probe, decision, question, maintenance. There is NO
  'feature' kind — use 'build'. Unknown kind → ValueError naming the
  taxonomy file to edit (data, never code).
- `complete(c, task_id, outcome, actor='unknown') -> bool` — NO
  close() function, NO detail= kwarg. Close narrative goes into
  task_events / run-records, not complete().
- `claim(c, actor, actor_kind, task_id=...)` — actor before
  actor_kind, task_id is kwarg.

## TARGET 3: SKILL.md body — new QA subsection
Add under a "## Adversarial self-review of reviews" heading:

- Before publishing ANY census/review/architecture claim, run a
  multi-brain falsification pass (Popper/Tanenbaum/Andreasen lenses)
  minted as a ledger 'verify' task — it catches real errors: this
  pattern falsified "110 engines" (12), "190 tasks" (194), "12 ports"
  (~40), and one critical inversion (claimed all 5 arcs lacked
  north-star metrics; they ALL have them under the `north_star` key —
  I had queried `north_star_metric`).
- SCHEMA-INTROSPECTION RULE: never trust remembered field names for
  JSON/DB claims. `PRAGMA table_info` / `list(obj.keys())` FIRST, then
  query what actually exists. A falsified census claim published to
  the principal costs more trust than the query costs compute.
- Relationship direction matters in data models: arcs.json `serves`
  means arc → workstreams (strategic goal is served BY campaigns), NOT
  workstream → arc. Read the field semantics from the schema owner's
  data before drawing maps.
- Docs-only commits (docs/**) legitimately skip CI via paths-filter —
  do not wait on or report a CI run for them (0 runs for the sha is
  expected, not a defect).

## TARGET 4: SKILL.md References list
Add pointers to:
- references/desktop-symlink-doctrine-2026-08-18.md (see TARGET 1)
- ledger signatures (TARGET 2, extends ledger-api-gotchas)
- falsification-panel pattern (TARGET 3)

## Session context (O'Keefe cross-ref)
QA task T-260818-0166 (partial) documents the panel run; corrected
review committed as 1bfc9bd (docs/ORGANISM-ARCHITECTURE-REVIEW-v2.md);
symlink restore recorded same day.
