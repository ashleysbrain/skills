# Self-evolution literature foundation (deep-research pass 2026-08-21)

Knowledge bank behind the Cross-Model Critic law + variant_archive organ.
Primary sources ingested live into Research Library `canon.db` (sources
192-199). Synthesis: `research-thread/DEEP-RESEARCH-SYNTHESIS-2026-08-21.md`.

## The five findings that changed our QA design

1. **Family-consistent errors are undetectable within one family.**
   Tan et al., "Too Consistent to Detect" (EMNLP 2025): the same wrong
   answer repeated across stochastic samples does NOT shrink with model
   scale; all four mainstream detection families fail on it; the fix is a
   cross-model probe — a verifier from a DIFFERENT model family.
   Consequence: an N>=3 panel where every seat runs the same family
   (ours: all glm-5.3) has correlated blind spots by construction.
   This is the empirical basis of the Cross-Model Critic law.

2. **Unanimity is a warning, not a pass — in BOTH directions.**
   Refute-or-Promote (arXiv 2604.19049): ten unanimous adversarial
   reviewers endorsed a non-existent vulnerability (killed only by one
   empirical test); and one unanimously-killed finding was later
   resurrected as a real CVE. Kill rate of stage-gated adversarial
   review: 79-83% of LLM candidates. Cross-Model Critic +
   mandatory empirical gate are the load-bearing stages.

3. **The archive is what compounds.**
   Darwin Godel Machine (arXiv 2505.22954, v3 2026): SWE-bench 20->50%
   via self-modification + empirical validation of EVERY change + an
   archive of stepping-stone agents (never discard variants). Our
   implementation: organism/variant_archive.py + telemetry.db table.

4. **Agent = FM + scaffold; improvement = update operator on scaffold.**
   Self-Improvements in Modern Agentic Systems survey (arXiv 2607.13104,
   Schmidhuber co-author): organize self-improvement by update target x
   driving signal. Confirms the scaffold-not-weights lane for a
   weight-frozen organism: skill patches, flow updates, prompt edits.

5. **Judging intermediate steps beats judging outputs.**
   Agent-as-a-Judge (ICML 2025, arXiv 2410.10934): grade tool-call
   provenance per claim, not final prose. We already do this informally
   via evidence packs; formalize when extending rubric_judge.

Supporting: MAPE-K agentic loops (arXiv 2506.22185) — watchdog is already
MAPE-K, .repair_state.json = Knowledge. SCL (ACL Findings 2025) —
self-correction is learnable from trajectories (our QA-LOG + suites are
the trajectory bank). STELLA (arXiv 2507.02004) — repeated gaps should
mint reusable tools/skills, not one-off patches.

## Built from this literature (2026-08-21)

- **Cross-Model Critic law + unanimity rule** patched into
  `elite-panel-chain-of-custody` skill (every >=3-seat panel ends with
  one cross-family critic seat, kill mandate only; unanimity = flag).
- **check_panel_critic** in qa_tick.py — enforcement backstop, anchored
  to the "Cross-Model Critic law SHIPPED" marker in QA-LOG.md so
  pre-law panels are exempt (falsified both directions live).
- **variant_archive** organ (see SKILL.md Organs table).
- Ledger: T-260821-0164 (cross-family rubric scoring; provider choice
  parked for principal), T-260821-0165 (S8 cross-family mint check),
  T-260821-0166 (canon residue rename).

## Where we already matched the frontier (do not rebuild)

Empirical validation of every change (regression suites as gates),
adversarial panels with kill mandates, live-proof law (= their mandatory
empirical gate), MAPE-K watchdog, predicament->research scan (S8).
The critic law closed the single literature-validated hole.
