# Veritas Chain-of-Custody Audit — 2026-08-15 Pattern Reference

Source session: Writing Studio / Veritas pipeline QA (writing-day prep). 8-brain sequential
chain over `/<workspace>` (~5,900 lines) + `pipeline_api.py`.
Every verdict line-number-anchored; the pattern transferred to any multi-stage pipeline.

## The chain (one stage cluster per brain, verdicts passed forward compressed)

| Seat | Scope | Verdict | Signature findings |
|---|---|---|---|
| the specialist engine | S0-2 intake | S0 DECORATIVE, S1 SOUND, S2 PARTIAL | dead abort gate (no verdict key), zero-drift refinement, UnboundLocalError on pre-evidence path, circular auto-verify |
| the specialist engine | S3 physics gate | DECORATIVE | triply-dead abort (stage key 3.1 vs tuple (0,3); "FAIL — ..." never == "FAIL"; no verdict key), consumers read stage_results[3] not [3.1] → "unknown" forever |
| the specialist engine | S4 drafting | PARTIALLY SOUND | base path discards Toulmin skeleton + no VERIFIED citation filter; 4.6 progressive path strong (citation discipline enforced, graceful retry) |
| the specialist engine | S5 adversarial panel | PARTIALLY SOUND | enforcement spine REAL (FAIL→revision, terminal after 2); half the 11 seats theater (domain seats PASS on routing success; Popper seat hardcoded constants, never sees draft; "Bentham" is a brand review; no seat-trust persistence despite UI claim) |
| the specialist engine | S6 revision loop | PARTIALLY SOUND (laundering) | FAIL-seat critiques never shown to reviser (filter passes REVISE only; hard-gate rewrite mutates panel_verdict not seat verdict); critiques truncated [:100]; citation guard count-not-set; unchanged draft re-paneled; final_panel_verdict has zero readers |
| the specialist engine | S7 output gate | DECORATIVE as gate | thresholds computed then "don't block — surface for human decision" (comment admits it); gate reads `weak` not `phantom` so fabricated citations can't trip it; UI poller green-lights complete_with_errors; quality_warnings never rendered |
| the specialist engine | orchestration | PARTIALLY SOUND | scheduler real, process manager decorative: second 3-vs-3.1 mismatch; stage 5.5 dispatched but never completes; /tmp checkpoints display-only (no loader); daemon threads die on restart; stale "running" rows forever; run() returns "complete" despite complete_with_errors |
| the specialist engine | closer | state machine + safety + patch order | "a Paxos with one acceptor, no ballot numbers, and a single absorbing state named complete"; 4 hazards all POSSIBLE with enabling chains; min-viable patch set ranked by risk/effort |

## The dead-gate defect signature (watch for these in ANY gated pipeline)

1. **Reader/writer key mismatch** — gate registered as 3.1, abort tuple tests (0, 3);
   consumers read a different key than the writer. Grep both sides.
2. **Verdict-string equality** — code emits "FAIL — majority reject", guard tests == "FAIL".
   Use `.startswith("FAIL")`.
3. **Missing verdict key** — result dict never carries `verdict`, so the guard falls through
   to `result.get("name")` which is never "FAIL". Patching the guard is moot until the
   writer emits the key.
4. **Enforcement opt-out comments** — "don't block — surface for human decision" means the
   gate is advisory; if the UI then renders success, failure is unwitnessable by construction.
5. **Success-theater seats** — PASS on routing-success/stdout-length rather than critique
   content. A scathing 500-word critique counts as PASS.
6. **Truncation amputating the signal** — [:100] per seat destroys the actionable part
   (which claim, which objection) before its only consumer reads it.
7. **Count-not-identity guards** — citation guard checking count lets the reviser swap
   real refs for invented ones. Compare SETS.
8. **REPLACE-wipe persistence** — INSERT OR REPLACE deletes+reinserts, nulling columns the
   row previously carried. Use ON CONFLICT DO UPDATE.

## Lamport's closing deliverable shape (the pattern to reuse)

1. The ACTUAL state machine (terminal states and their meaning; missing transitions that
   make error states non-terminal or success states lie).
2. Safety analysis: for each hazard, POSSIBLE today? One line + enabling defect chain.
3. Patch order ranked by (risk-reduced / effort): min-viable set for the immediate window,
   then full repair list. Numbered, no hedging.

## Min-viable patch set that came out (all applied + live-verified)

1. Persist draft to durable DB after S4 and every S6 pass (crash loses draft).
2. S6 feedback: ALL FAIL+REVISE critiques, untruncated (cap 4000).
3. Abort guard: `stage_num in (0, 3, 3.1) and str(verdict).startswith("FAIL")`.
4. Truthful status: return `self.state.status or "complete"`; error path early-returns.
5. Phantom gate: read phantom not weak; block on phantom>0.
6. Crash guard: initialize `search_result = {...}` before the pre-evidence branch.

Then Popper's falsification pass found 3 residuals (FAIL-first sort, verdict-key emission
for S0/S3, ON CONFLICT persist) — applied and verified in the live DB.

## UI truth-rendering (same session, Studio side)

The pipeline's API telling the truth is half the fix; the poller must render it. The Studio
poller was patched to handle 4 statuses: completed (green), complete_with_errors (amber),
complete_with_quality_issues (amber + review warnings), blocked_phantom_citations (red,
draft NOT loaded). Green-lighting a failed run is the compound lie — fix both ends.

## Timing data

- Brevity-capped stage audits (350-400 word caps, numbered questions): 95-225s each.
- Uncapped 6-patch delegation: hit the 900s wall on re-location alone (31 API calls, no edits).
- Anchor-pattern + line-number dispatch (3 patches): 184s complete with syntax check.
- Two-wave concurrent panel (user-directed) for independent lenses; sequential for custody.
