---
name: organ-seating-and-census
category: devops
description: Use when naming or auditing organism organs.
---

# Organ Seating and Census

TRIGGER: about to call something an "organ"; about to write a new
module directly into organism/; asked to audit or "fix prior organs";
remediating out-of-process builds.

## The rule (seat before name)

"Organ" is a methodology term, never a filename or docstring. An organ
= a task-ledger seat + a run-record close with live execution evidence.
Birth order:

1. **MINT** via `gates/task_ledger.py submit(c, title, kind, lane,
   origin, created_by, flow='FLW-ACTION', detail=...)` — the ONLY birth
   path; raw INSERT is trigger-blocked.
2. **CLAIM** via `claim(c, actor, actor_kind, task_id=tid)` — mind the
   argument order.
3. **BUILD / VERIFY** — gate selftests AND a real run.
4. **CLOSE** via `complete(c, tid, outcome, actor)` citing live
evidence: launchd label + PID for daemons, run counts for batch
organs. Then read the row back with SELECT — never trust `closed=True`
alone.

A .py written straight into organism/ and named an organ violates this
regardless of code quality. If the seat does not exist at birth, mint
it in the same turn or the build is out-of-process.

## Census method (what is actually an organ?)

1. **Ledger check**: for every file, query the ledger for
   `title LIKE '%<basename>%' OR detail LIKE '%<basename>%'`. No rows
   and no live daemon = not an organ, whatever the filename says.
2. **Recursive glob**: census `organism/**/*.py` — flat passes miss
   subdirectory files.
3. **launchd liveness map**: parse every `com.divinity*.plist` →
   ProgramArguments → the actual .py path it runs. A file can sit
   inert in organism/ while its ds-*-engine launchd label runs a copy
   from another path; a filename-only census therefore undercounts
   live surfaces. Cross-reference with `launchctl list` for live PIDs.

## Cross-registry diff (citable catalog, T-261021-0063)

Census now includes a MitoCarta Tree-of-Life style cross-registry diff
(`your-stack/gates/registry_diff.py`): presence/absence matrix of
scientist-seated organs across the Mosaic / the operator agent / Divinity Science
registries, unique sets per registry (specializable-function markers),
same-lineage drift (the operator agent vs DS snapshot), and the Chao/Fry two-lens rule
— an organ<->engine coupling is CLAIMED only with BOTH structural
(scientist seat or identical DS-ECS code) AND compositional
(discipline-token) evidence; single-lens matches are uncorroborated
candidates, never claims.

- The citable catalog regenerates hourly via the census-sweep daemon
  (`stores/registry-diff-YYYY-MM-DD.json`, keep-8, 48h staleness alarm).
- CITE the artifact in census/audit handoffs:
  `python3 gates/registry_diff.py --cite` → path + sha256 + task ref.
- `--verify` re-checks the artifact self-hash AND that every pinned
  source registry still matches its recorded sha256 (a drifted pin
  means the catalog is stale — re-run `--diff`, don't cite the old one).

## Remediation pattern (census → seat → register)

- **Retro-seat live daemons** found without birth certificates: one
  task each citing launchd label + PID, or a batch digest when there
  are many.
- **Register non-daemon files** in a script registry store
  (script-registry.store.json) with dispositions: script-with-provenance
  (ledger tasks reference it) / inert-script / test. Scripts are
  scripts — never organ claims. The registry is the complement that
  keeps "what is actually an organ" auditable in one file.
- **Batch by default**: N findings of one class = ONE digest task
  listing the items. Mint-rate caps are per-origin per-day across all
  lanes; bulk individual minting mid-remediation hits the cap and the
  script dies whole. When the gate refuses, its error names the remedy
  — follow the batch shape it asks for and fold stragglers into the
  registry digest; never force past the cap.

## Mint-mechanics pitfalls (bit repeatedly)

- Title ≤ 200 chars — a label, not a document; content goes in
  `detail=`.
- `kind`/`lane`/`flow` are validated against the JSON registries; when
  a mint is rejected, fix the exact field the error names — never
  retry blindly.
- Avoid port literals (`:NNNN`) and delivery-mechanism verbs (daemon,
  carries, delivers, watchdog...) in detail/outcome prose — mechanical
  gates pattern-match them and refuse or re-probe.
- A mint+amend script dies WHOLE when any mint is rejected — re-run
  amendments after any re-mint and read back every marker.

## Execution mechanics

- Write multi-line Python to a file and run it — heredoc/piped
  `python3 << EOF` through a shell can no-op silently (empty stdout,
  exit 0) or die to shell quoting of embedded parentheses, and a silent
  no-op looks exactly like success.
- Verify by direct read-back keyed on a unique token/dedup_key, never
  `SELECT max(id)` — concurrent posters make the newest row a false
  confirm.
