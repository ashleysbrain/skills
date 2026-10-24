# VERITAS Stage 7 Output-Gate Audit — the specialist engine, 2026-08-15

Chain-of-custody QA of `/<workspace>` (stage-by-stage,
8 microtasks). Verdict ledger: S0 DECORATIVE (dead abort), S1 SOUND, S2 PARTIALLY SOUND,
S3 DECORATIVE, S4 PARTIALLY SOUND, S5 PARTIALLY SOUND, S6 PARTIALLY SOUND,
**S7 DECORATIVE-as-gate** (instrumentation real, enforcement nil).

## Line evidence (veritas_process.py unless noted)

- Check inventory L4692–4955: Luria review L4694 (stored, never read); AI-tell gate
  L4703; voice check L4735–4745; term sweep/prior art/metaphor/fact-check/citation
  audit L4807–4811; bigram citation support L4816; metric grounding L4819; 5-dim
  review L4822; citation quality L4825. Only STYLE checks enforce (deterministic
  cleanup L4749–4799, real). All substance checks advisory.
- Quality gate L4934–4952 computes real thresholds (unsourced>60%, 5-dim FAIL/avg<7,
  weak citations, <5 refs) but L4951 comment admits "don't block — surface for human
  decision" → ships as status string `complete_with_quality_issues`.
- **L4931 gates on `weak` count, never `phantom`** — fabricated author-year citations
  (detected L5804–5807) cannot trip the gate at all. Classic computed-but-unused signal.
- Stage-7 EXCEPTION path (L5196–5202) still outputs the raw stage-4 draft as
  `complete_with_errors` — crash becomes pseudo-success.
- Citation-support matcher limits: only first 20 citations indexed (L5715); markers
  >[20] silently skipped (L5741); findings capped at 20 (L5815); bigram overlap ≥0.2
  trivially gamed by restating abstract vocabulary (L5761, L5795).
- Provenance IS in the package dict (L4874–4906, quality_gate copied L4966) — audit
  trail exists, nothing enforces on it.
- UI: `writing-studio.html` `_pollPipelineIntoDraft` L8128 treats
  `complete_with_errors` as success (green banner L8154);
  `complete_with_quality_issues` matches no polled status (silent timeout);
  `quality_warnings` (pipeline_api.py L311–312) has ZERO readers in the UI.

## Prescribed fixes (not yet applied — read-only audit)
1. L4931: use `phantom + weak` as phantom_count.
2. L4943: phantom>0 OR unsourced>60% OR dim-FAIL → return failed, not tag.
3. Studio L8128: match quality-issue statuses, render `quality_warnings`, never
   green-light `complete_with_errors`.

## Generalizable gate-audit method (any pipeline)
1. Trace READERS of every check result — zero readers = decorative.
2. Classify each check enforced (return/abort/rewrite) vs advisory (log/status tag).
3. Exception handlers that still emit output convert crashes into pseudo-success.
4. Computed-but-unused signals (phantom counted, never gated on) = gate wired for show.
5. Diff backend's settable status strings against frontend poller's matched statuses;
   unmatched statuses fall through silently into a synthesized success narrative.
6. Verdict vocabulary: SOUND / PARTIALLY SOUND / DECORATIVE / BROKEN.
