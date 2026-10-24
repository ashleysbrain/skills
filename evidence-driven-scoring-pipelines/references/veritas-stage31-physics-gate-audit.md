# VERITAS Stage 3.1 Physics Gate — Operationalism Audit (2026-08-16)

Grader: the specialist engine (DS-ECS-SUB-04.09.04-v1.0.0), Percy Bridgman operationalism —
a claim is its measurement. Case: two principal-initiated Writing Studio runs killed at
Stage 3.1 by the four-approach physics gate. Companion to
`veritas-stage7-gate-audit.md` (stage 7 asked "does the gate block?"; this audit
asks "does a blocking verdict measure what it claims?"). A gate can be fully
enforced and still invalid.

## Where the code is

- `/<workspace>` — `validate()` (~L354-455):
  four approaches, synthesis pass-count.
- `/<workspace>` — run loop ABORT-ON-FAIL guard
  (L5244-5256, bus msg 1691 #7 + PATCH 3): `if stage_num in (0, 3, 3.1) and
  str(verdict).startswith("FAIL")` → hard stop.
- Blueprint copies (do NOT edit as fix targets): `gigi3/organism/veritas_process.py`,
  `gg3-blueprint/organism/veritas_process.py` (see pipeline-file-routing skill).

## The scored scenario (exact reproduction)

Inputs: FE F=0.18 / info_gain=0.24 → verdict "SKIP — cost exceeds info gain…";
COUPLING coherence 6.04 → "PARTIAL"; CRIT → "NO HISTORY — first review round";
BAYES posterior 0.493 ± 0.177.

Synthesis Booleans (veritas_engine.py ~L428-432):

- `fe_pass = "PROCEED" in verdict` → **False** (SKIP ≠ PROCEED)
- `cp_pass = "COHERENT" in verdict` → **False** (PARTIAL lacks the substring —
  note "INCOHERENT" *contains* "COHERENT", a separate latent bug)
- `crit_ok = "TIPPING" not in verdict` → **True** (verb-absence: no data = pass)
- `bay_pass = posterior > 0.5` → **False** (0.493 < 0.5 by 0.007, σ=0.177)

`passes = 1` → "FAIL — majority of approaches reject", confidence 0.15 →
ABORT-ON-FAIL fires on the principal's runs.

## Findings (the five rules)

1. **Vote-counting over incommensurables.** FE measures the economics of
   *running* the validation; coupling measures reviewer agreement; criticality
   measures time-series convergence through data that does not exist; Bayes
   measures the claim. Summing them adds meters to kilograms. The verdict text
   ("majority of approaches reject") was false against its own inputs: zero
   approaches had measured rejection (SKIP, PARTIAL/investigate, no-data,
   borderline). Valid vote-count requires every Boolean to share one referent.
2. **SKIP-as-reject / NO-HISTORY-as-pass.** FE SKIP asserts a property of the
   instrument (cost > info gain), not of the claim — scoring it as a reject vote
   measures the gate's economics disguised as specimen quality. Meanwhile CRIT
   "NO HISTORY" *passes* because the failing verb is absent: a non-measurement
   cast as affirmative evidence. Same word, two opposite meanings: `pre_flight`
   SKIP → early return, confidence 0.0, no vote; `free_energy_validation` SKIP
   → failure vote. Rule: abstention shrinks the denominator; it never signs
   either side.
3. **Threshold inside its own noise band.** |0.493 − 0.5| = 0.007 ≪ σ = 0.177;
   P(θ>0.5) ≈ 0.5. The instrument reports no information. The bayesian module's
   own verdict logic says "BORDERLINE"; `validate()` overrides it with a hard
   `> 0.5` cut. Correct treatment: INCONCLUSIVE → gather evidence or escalate.
4. **confidence=0.15 is a bucket label, not a probability.** Keyed to pass-count
   (0.95/0.75/0.45/0.15), it measures the arithmetic of the voting procedure —
   and the ABORT guard treats it as ground truth sufficient to kill
   human-initiated runs.
5. **The killing number was priors.** F = cost − T·info_gain = 0.2 − 0.5·0.24 =
   0.18: dominated by the hand-set constants cost=0.2 and T=0.5, not by claim
   data. The gate killed runs on its own assumptions about itself.

## Prescribed fix semantics (minimal, solo-founder writing tool)

- **ABORT** — only performed, decisive, unambiguous measurements. Exemplar that
  qualifies: Stage 0 evidence gate (strong-claim word + no original data is a
  verifiable linguistic fact).
- **Downgrade to FLAG** — FE SKIP (instrument economics), COUPLING PARTIAL,
  CRIT NO HISTORY (missing data). Annotate the artifact; never kill the run.
- **Ask-the-human** — any statistic inside its own noise band; the human who
  launched the run is the other available instrument.
- Optionally: abstaining approaches shrink the vote denominator; substring
  matching on verdicts is fragile (INCOHERENT ⊃ COHERENT) — match on an enum
  field, not prose.

## Grade

Rule: **F** (invalid measurement operation feeding a hard abort). Parts:
**A** (each approach honestly labeled its own state; the modules were right,
the synthesis was wrong).
