# Paper-digestion loop + ledger mint pitfalls (2026-08-20)

Session: two papers relayed by principal (arXiv 2608.13331 Replica/Faraday,
arXiv 2608.03702 FNO quantum control), both processed under the
"digest and process, the OS always" directive.

## The four-stage loop (binding definition)

A relayed paper is NOT done until all four stages close:

1. **DIGEST from primary source.** arXiv API
   (`http://export.arxiv.org/api/query?id_list=<id>`) for metadata,
   `https://arxiv.org/html/<id>` for full text via curl. Strip
   script/style before tags; the HTML TOC repeats section names —
   take the SECOND occurrence for section bodies.
2. **Record OUR process weaknesses explicitly** (W1..Wn), each mapped
   to the paper's method — not vibes.
3. **INGEST**: Research Library (`research-library.db`) source row +
   finding row. Real schema: `sources.credibility_weight` (NOT
   `credibility`), `findings(domain_id, source_id, title, body,
   confidence, tags, date_observed)` — title is NOT NULL; findings
   reference domains(id), not a domain string.
4. **MINT typed tasks** in the ledger citing the finding id
   (origin='ceo:arxiv-<id>', kind/lane from task-taxonomy.json).

Failure this session: paper 2608.03702 was digested + ingested
(finding 396) but tasks were not minted before reporting done; the principal
re-sent the identical URL with "Mosaic methodology always." Stage 4 is
the stage that makes it real.

## Ledger mint pitfalls (each hit live, 2026-08-20)

- **ID race**: auto-minting watcher organs (research scans) consume
  T-2608NNN-NNNN ids continuously. Two mints collided with ids taken
  mid-turn (T-260820-0080, T-260820-0094). Protocol: query
  `SELECT MAX(CAST(SUBSTR(id,10) AS INTEGER)) FROM tasks WHERE id LIKE
  'T-260820-0%'` immediately before insert; on UNIQUE failure re-query
  and take the new max + 1. Never carry a precomputed id across steps.
- **Non-atomic task+event inserts**: an exception after the tasks INSERT
  can commit the task row while the task_events row is lost. On
  IntegrityError, query the task id: if present, backfill the event row
  instead of re-inserting the task.
- **Schema (PRAGMA user_version=2)**: `tasks.state` (NOT status),
  CHECKed open/claimed/done/blocked/cancelled; severity INTEGER 1-4;
  `actor_kind` (CHECK 'ai'/'human') lives in task_events only.
  task_events is append-only (DELETE trigger aborts).

## QA gauntlet pattern that worked (TSC explainer)

Sequential different-elite-brain passes, read-only reviewers, verdict +
numbered defects + exact replacement wording; parent folds fixes, then
next brain re-verifies from sources. Popper pass 1 on the explainer
returned FAIL with 9 defects — all real (invented firefly claims,
blanket "biology IS the math" overclaim vs 2-of-9-audited physics
audit, wrong engine count vs own cited source, unchecked-submit
overclaim "presents at TSC"). Falsification-before-render is not
optional for any external-facing artifact.
