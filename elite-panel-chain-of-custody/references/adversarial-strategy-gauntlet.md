# The Adversarial Strategy Gauntlet (proven 2026-08-15/16, funding-strategy build)

Pattern: a strategy/plan the principal will execute gets attacked by N sequential specialist brains BEFORE the principal reads it. The principal explicitly demands multiple rounds ("do another thorough QA pass", "there should be more adversarial rounds"). Two rounds minimum; five is the proven full ladder.

## The round ladder (each = one brain, one microtask, gated before the next dispatches)

1. **FALSIFIER (the specialist engine, she)** — attack the plan's structure: wrong instrument, shell entities, unanswerable questions, missing evidence artifacts, framing collisions. Output: kill-level gaps ranked, microtasks to add/reorder/cut, survives/does-not-survive verdict.
2. **CALIBRATOR (the specialist engine)** — stress-test the rebuild with numbers: probabilities per instrument, EV = p × size × speed, calibrated replacement sentences for every certainty claim ("will REQUIRE" → p-stated / conditional / base-rate versions), confidence intervals on the timeline, the kill-shot assumption + its early indicator.
3. **DELETER (Musk seat)** — first-principles deletion pass: which microtasks are ceremony (data room with no investor, cap stub with no raise, registrations for instruments that don't need them), structure derived from constraints (principal-hours/runway/credibility) instead of option menus, trigger-events instead of debates, the one cash path the EV table missed.
4. **DOMAIN REALIST (Program-Officer / money-side seat)** — does the real world accept the plan: eligibility traps (ARIA UK-only, Schmidt needs institutional home, SBIR wants for-profit), what survives triage (artifact + name, not prose), entity-timing traps, the underweighted shared failure point.
5. **DECISION SCIENTIST (Kozyrkov seat)** — convert the surviving plan into an operating design: the portfolio cut by EV-per-principal-hour, principal-only irreversibles vs delegables, pre-commitments locked while calm (park rules, tie-breakers, auto-park triggers), the weekly 12-min hour-gate ("deliverables lie; calendars don't").
6. **CONSOLIDATOR (the specialist engine)** — fuse all rounds into ONE executable document (see THE-BUILD-COMPANY-STRUCTURE-AND-ROADMAP.md pattern): structure decided, week-by-week microsteps with named lanes + hours caps, operating rules, a 5-line emergency card for overwhelmed weeks.

## Binding rules learned

- **SEQUENTIAL ONLY.** principal corrected parallel dispatch mid-session ("Not in parallel"). One brain in flight per microtask; next dispatches only after the previous lands AND passes the brain-integrity gate. R2 refines R1's output — parallel dispatch destroys the dependency chain.
- **Disagreement is the product.** When two gated brains split (e.g. Karpathy "use it later" vs Popper "park it"), the consolidation ruling synthesizes: unanimous core governs now, the minority's execution spec gets banked, an explicit re-entry condition (demand-pull OR calendar slot) decides revival.
- **The principal reads nothing until the gauntlet completes.** Stated explicitly: "I'm not even reading this until we go through this a couple of times."
- **Every round gated.** brain_integrity_gate.py after each landing; gate false-positives get manually verified against the transcript (see brain-integrity-self-healing-gate pitfalls).
- **Live data before dispatch.** Pull the real landscape (APIs, disk state, DB queries) BEFORE the specialist runs, and embed the verified numbers in the dispatch context. Specialists reason; the parent verifies ground truth.
