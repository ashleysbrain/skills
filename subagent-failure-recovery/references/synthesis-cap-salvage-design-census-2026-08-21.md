# Synthesis-cap salvage: design census 2026-08-21

Child deleg_42d8cc65 (the specialist engine census + the specialist engine cross-exam seats,
glm-5.3, single child per 429 law) ran 24m17s and hit max_iterations at
the SYNTHESIS step; its final API call also timed out (60s threshold,
3 retries). The completion echo said "completed" + "TRUNCATED: hit
max_iterations" — a self-report, not evidence.

## What was on disk when the child died
- probe-raw.jsonl: 74 live probe rows (seat 1)
- popper-reprobe.jsonl: 46 Popper re-probes (seat 2)
Missing: both deliverables (JSON + MD), both ledger completes, bus post.

## Orchestrator takeover (deterministic code, zero LLM calls)
1. Dedupe raw rows by id, LATEST probe wins: 74 -> 57 unique (8 ids had
   been re-probed by the child itself).
2. Grade from measurements only: HTTP 200 + latency < 8s = A; 200-slow
   or 429 = B; else C. Result: A=47 B=4 C=6.
3. Coverage check against protocol: 4 A-grades had no Popper re-probe
   (cap interrupt) -> orchestrator re-probed them directly (all
   CONFIRMED). Final coverage 47/47, zero downgrades.
4. Assembled census JSON + MD format-matched to the sibling finance
   census so Studio wiring stays uniform.
5. Output-law gate on the ASSEMBLED deliverable: em-dash scan caught a
   violation in the orchestrator's own MD -> fixed, rechecked CLEAN.
   Run output laws on your own assembly too, not just on child output.
6. Provenance meta block in the JSON records exactly which measurements
   came from the child vs closed by the orchestrator. Zero fabrication.
7. Ledger rows T-260821-0142/0143 completed with the takeover
   disclosed; bus post 2893 to sibling-agent carries the same disclosure.

## Why mechanical assembly beat re-dispatch
All measurement cost was already sunk and valid; synthesis from rows is
deterministic; a re-dispatch would re-run 74 probes and re-risk the
same glm-5.3 timeout on the identical synthesis step. Free energy
strongly negative for re-dispatch.

## Artifacts
/<workspace>{census-design-2026-08-21.json,
CENSUS-DESIGN-SOURCES-2026-08-21.md, probe-raw.jsonl, popper-reprobe.jsonl}
