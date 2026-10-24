# Multi-pass sweeps: falsify before fix + verify the verifier (2026-08-25 session pattern)

The layered flow-sweep arc that survived principal scrutiny. Encode this shape for any corpus-wide audit (flows, laws, skills, engines, cron jobs).

## The pass structure (principal order: "multiple passes — I don't trust the first pass")

1. **PASS A — broad census** (sweep-first law): every item enumerated, one table row each, health verdict + failure lenses + success signal. Counts per class, top-N candidates, top working patterns. No drilling before sweeping.
2. **PASS B — deep drill** on the top candidates: root cause with Nullius pointers, opportunity reframe (O-number, principal's failures=opportunities law), concrete fix proposal (who/what/gate).
3. **PASS C — second-round catch pass, fresh process**: (a) spot-check-verify 4 of Pass B's claims by independent re-derivation — a REFUTED claim is a high-value find; (b) hunt missed angles (cross-item interactions, temporal degradation, unaccounted buckets, success-pattern blind spots like rubber-stamp closes); (c) pick the working pattern with most growth headroom.
4. **PASS A-RERUN if protocol was violated**: if any pass was self-executed by the orchestrator instead of dispatched (protocol violation), the analysis re-runs protocol-correct, and explicitly judges the bypassed analysis: clean / biased-toward / missed.
5. **ADVERSARIAL PANEL — prove-wrong mandate** (10 seats): findings attacked with live re-derivation (SURVIVES/DIES/DOWNGRADED); the FIX PROPOSALS attacked too (what does each gate starve/deadlock/over-gate — some fixes must NOT ship); the success list attacked (less-broken ≠ working); the sweep METHOD attacked (shared-lens blind spots — SQL census can't see code, runtime, or traffic).

## Falsification before fixing (the discipline that earned its keep)

Before building any surviving fix, run one-command live tests that would prove each finding WRONG if it's wrong. A test that kills a finding kills its fix. Nothing gets fixed that can't survive being attacked twice. Tests run IMMEDIATELY — never scheduled for tomorrow (AI-timeline ruling).

## Verify the verifier

Every pass contained errors in a different direction: Pass B inflated magnitudes 2–28x (counted cancelled as open), Pass C "refuted" a flagship stat with a claim that itself failed direct re-derivation (zero evidence for its ghost-replay claim), Pass A was biased-toward-failure by its bypassing author. Verification is reflex, not a step: re-derive the number, then re-derive the refutation.

## Live results from the source session (proof the pattern works)

- 10 findings attacked: 5 survived + fixed (top: 75% of one day's mints untagged; unbounded QA mint storm), 2 died, 3 downgraded as too-young-to-judge (retest at 72h/7d).
- 4 proposed fixes BLOCKED by the fix-attack seat (terminal_flow hard requirement, decision auto-expiry, severity pre-mint gate, bulk backfill).
- The flow-tag gate built from the top finding rejected its own author's mint within the hour — laws as code, not intentions.

## Anti-patterns caught mid-sweep

- **Self-redo on subagent failure:** when a sweep subagent died at its iteration cap, the orchestrator re-did the work itself — principal: "direct violation of our protocols... whatever iteration limit you think you're hitting isn't even real." Re-dispatch through the same flow at smaller scope, never author the delegated deliverable. Also: verify claimed limits against raw counters (config said 250; subagent used ~7 — the label was a misattributed API timeout).
- **Counting cancelled as open:** inflates failure magnitudes; always split state counts exactly.
- **Cancellation-as-waste assumption:** shared unproven lens; some cancellation is legitimate triage.
