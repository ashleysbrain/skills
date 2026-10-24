# Adversarial Panel Pattern (concurrent-blind, wave-scaled)

Proven 2026-08-26 (12 seats, 2 waves × 6, 66+ findings, 0 unactioned). principal directives
2026-08-23 + 2026-08-26 sanction PARALLEL seats for adversarial panels even though
production/strategy dispatches stay sequential (see Core rule 1 carve-out).

## Preconditions
1. Check `delegation.max_concurrent_children` in <agent-home>/config.yaml FIRST.
   (Was 1 on 2026-08-26 — had to raise to 6 before any wave could run.)
2. Write a BRIEFING PACK file (PANEL-BRIEF.md) with MEASURED state only:
   counts, before/after metrics, the design under review, verdict schema,
   read-only/write contract. Seats read the pack — they must get measurements,
   never the orchestrator's narrative summary (ENTOURAGE dynamic).
3. Export a fresh data slice (CSV of the newest N rows) for seats to chew.

## Seat taxonomy (reuse per attack surface; add domain seats as needed)
Wave-1 (correctness of what exists):
  1. semantic integrity — does compression lose/twist meaning?
  2. duplication ecologist — true dupes vs distinct-but-flattened
  3. taxonomy coherence — kinds/lanes/enums vs scheduler physics
  4. human factors — scan the list cold as the ADHD human reader
  5. machine parsability — consumers, parsers, grep-based queries
  6. provenance auditor — chain of custody, events, backups, loss
Wave-2 (systemic/failure):
  7. signal grammar — closed vocabulary, rogue prefixes, alias collisions
  8. failure modes — how does this break next week? likelihood × damage
  9. statistics — before/after distributions, honest metric deltas
  10. dispatcher reality — simulate real consumers claiming work
  11. archivist — memory-of-record integrity, fences, anchors
  12. fresh-eyes red team — no stake, no hints, "what's the dumbest thing here?"

## Verdict file schema (one JSON per seat, deterministic path)
{"seat": "<name>", "findings": [{"id": "<row-id>", "severity": 1-4, "issue": "...",
 "fix": "..."}], "verdict": "ACCEPT|REVISE|REJECT", "panel_note": "<=50 words"}
Severity: 1=fabrication/loss, 2=broken/lying, 3=degraded, 4=cosmetic.
Every finding grounds a REAL id the seat actually read.

## Dispatch contract per seat
- Context = briefing path + data slice path + seat-specific hunt list.
- Read-only on production stores; write ONLY their one verdict file.
- When concurrency is 1: waves still work — they just serialize (slower, same output).

## Consolidation (mechanical, never by vibes)
1. Load all verdict JSONs; flatten findings.
2. Cluster by root-cause keywords (duplication/grammar/archive/gate/consumer/...).
3. Report per cluster: count, severities, distinct seats agreeing (consensus weight).
4. Apply fixes in dependency order; re-measure headline metrics after EACH fix
   class so new collisions surface immediately (label disambiguation can create
   new duplicate titles — handle in the same pass).

## Late-report ingestion (MANDATORY)
Async batch reports land AFTER revision passes. On each landing:
- verify each cited finding against CURRENT state (some already fixed),
- extract only NEW actionable items,
- apply, re-verify headline metrics.
Both 2026-08-26 waves yielded post-revision fixes (14 total), including a
consumer regression the orchestrator had introduced mid-fix.

## Truncated-report rule
A rate-limited final summary does NOT mean failed work: check the expected
verdict file on disk first (one wave-2 seat had a complete file and a truncated
summary — re-dispatch would have wasted the run). Also scan for path drift
(seats writing one dir too high) — recover files, don't re-run.

## Known metric trap
uniq-first-8-chars DROPS when you close a signal vocabulary (10 signal words
now dominate the prefix distribution) — that is by design. Honest
discriminability metric after vocabulary closure: uniq16 (0.741 post-fix vs
0.681 pre-fix). Tell statistics seats this before they flag it.

## Discriminator: panel (parallel) vs chain (sequential) — principal correction 2026-08-27

Parallel is sanctioned ONLY for concurrent-blind seats attacking a FROZEN
artifact with NO shared growing document (verdict JSONs per seat, independent
attack surfaces). The moment seats contribute sections to one accumulating
corpus — research doc or findings file — it is a CHAIN: one seat in flight,
each reads all prior sections before starting. Dispatching chain seats in
parallel "waters down the outputs" (principal, verbatim, repeat offense). If a
parallel wave was started in error on chain work: live-stop every seat,
verify the shared file for partial pollution, keep only seats that landed
complete, log the training failure, restart as a chain. Full chain pattern:
references/sequential-research-chain.md.
