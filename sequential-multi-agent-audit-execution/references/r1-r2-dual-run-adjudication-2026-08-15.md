# R1/R2 Dual-Run Adjudication — Funding Strategy Session (2026-08-15)

Session case where a forced re-run converted a single reading into a two-run
experiment. Companion to the "R1/R2 Dual-Run Adjudication" section in SKILL.md.

## The trigger chain

1. **v1 (timeout):** research subagent told to web-research with native web tools
   burned the full 900s fighting empty-return tool failures, found the working
   path (urllib via execute_code) 22s before the cap. Zero output.
2. **v2 (corruption):** re-dispatch arrived with garbled context (audio-transcript
   fragments, unrelated session text). Zero output, discarded unread.
3. **v3 (clean, gate-FAIL):** parent pre-fetched 6 sources into a 35KB source
   pack on disk; child got a minimal file-pointing brief. Completed clean, 499s,
   11 API calls. Banked as R1 with gate state noted. Gate FAIL was real: the
   minimized brief had stripped the persona-spec markers the brain-integrity
   gate greps for (PhD / institution / credential strings).
4. **v4 (clean, gated PASS):** same pack, full persona spec restored, 799s.
   Served as R2 — an independent confirmation run on identical data.

## The divergence table

| Question | R1 (v3) | R2 (v4) | Resolution |
|---|---|---|---|
| Instrument #1 | NIH SBIR Phase I | NIH SBIR Phase I | AGREED — locked |
| Grants-first sequencing | yes | yes | AGREED — locked |
| the external advisor = NIH door | yes | yes | AGREED — locked |
| #1 credibility asset | federal award | validation cohort paper | compatible — merged |
| Hub vehicle | SPV under parent | subsidiary LLC ("SPV overkill") | ADJUDICATED → LLC |
| First-raise range | $750K–1.5M | $323K–500K | ADJUDICATED → smaller |

## The adjudications (principles, not preferences)

- **SPV vs subsidiary LLC:** adiabatic principle — the LLC achieves the same
  ring-fence (investors buy sub shares; parent keeps 100% core IP) at a fraction
  of the legal overhead for a solo-principal pre-award lab. SPV deferred until a real
  securitization need emerges.
- **Raise range:** pre-validation dilution risk — stacking SAFEs before the
  validation cohort exists dilutes at the worst moment. Aim at the number the
  structure requires, not a portfolio maximum.

## Rules extracted

1. Re-run on the SAME data (source-pack file) or agreement is meaningless.
2. Lock agreement zones as dual-run-locked; report verification state per verdict.
3. Adjudicate divergences on stated principles; name the principle in the writeup.
4. A gate-FAIL that forces a re-run is an upgrade, not a setback.
5. Minimal brief = data-externalized, NOT persona-spec-externalized — the gate
   greps the kickoff for persona markers, so the full spec must survive
   minimization (this is what forced v4 and accidentally produced R2).

## Artifact paths (this session)

- Source pack: `/<workspace>`
- R1 summary: `<agent-home>/cache/delegation/subagent-summary-0-20260815_130514_709262.txt`
- R2 summary: `<agent-home>/cache/delegation/subagent-summary-0-20260815_132045_921822.txt`
- Verdicts banked to O'Keefe: mem 85 (R1), mem 90 (locked B)
