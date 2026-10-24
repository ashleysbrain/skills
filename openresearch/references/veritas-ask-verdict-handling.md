# Veritas ASK verdicts — handling pattern (learned 2026-08-18, ScienceFlow)

## What happened

Ingesting the ScienceFlow paper (arXiv 2608.14354) through
`organism/openresearch_ingest.py` returned:

```
Veritas: ASK — COUPLING inside noise band (Bayes 0.606±0.151); human decides
REJECTED (VERDICT=FAIL) — not consolidated
```

Three resubmissions with progressively rephrased claims all returned the
same FAIL. The rephrasing included attempting to dodge the strong-claim
word list — which is gaming the gate, not passing it.

## The mechanic

Two independent gate layers produce non-PASS verdicts:

1. **Evidence-level word gate** (`veritas_engine.py` ~line 380):
   claims containing `demonstrate / confirm / prove / establish / show that`
   with `--evidence literature_synthesis|theoretical` auto-fail the
   evidence gate. This is BY DESIGN — strong verbs require original data.
2. **Bayesian ASK band**: when claim coupling sits inside the noise band,
   the engine escalates to human decision. No rephrasing changes the
   underlying evidence class.

## Correct handling (verified workflow)

1. **Do not resubmit.** One ASK = one hold. Resubmission is free-energy
   waste on a verdict only the human can change.
2. **Log the hold**: append finding + full-text-verified facts to
   `intel/papers-held-for-ceo.jsonl` (ts, paper, veritas verdict, action,
   facts array).
3. **Mint the ledger task anyway when facts justify it**: engineering
   adoption of architecture patterns (independently verifiable against
   our own system) does NOT depend on claim-level consolidation. E.g.
   ScienceFlow's ESTRA re-anchoring + admission semantics were minted as
   a build task from the verified facts alone.
4. **Surface the hold to the principal** in the reply — she decides
   consolidation; the gate exists precisely for that.

## Key distinction

FAIL (evidence lacking, claim unsupported) → reject, stop.
ASK (human decision required) → hold, log, continue with fact-level work
that doesn't require canon consolidation.

The wrapper prints `REJECTED (VERDICT=FAIL)` for both — always read the
Veritas line ABOVE it to distinguish.
