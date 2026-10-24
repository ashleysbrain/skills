# Numeric QA + Calibration Gate — revenue panel 2026-08-20

Trigger: principal challenge after a 9-seat panel shipped its dossier — "do a thorough qa pass on your review as your past numbers have not been accurate for real world scenarios." Known lane failure mode (glm-5.3/llm-vendor fabricated outputs 08-18/08-20) made this a first-class gate, not a courtesy pass.

## The three-stage numeric QA (all stages RUN LIVE, in code)

### Stage 1 — Mechanical arithmetic audit (execute_code, never by eye)
Recompute EVERY derived number in the chain (seat verdicts + dossier): funnel products, probabilities, ASPs, rates, hour budgets, EVs. Tolerance 3%; label PASS/FAIL.

Result on this run: **22 checks, 11 FAIL.** The pattern was directional, not random:
- Every funnel expectation rounded UP toward "≈1 deal" (30×25%×30%×30% = 0.675 stated as "≈1", +48%; dossier EV $4,750 where true product = $3,206, −32%).
- Cost/effort numbers rounded in the principal's favor ($425/h stated where $9.5K/20h = $475/h).
- Points stated where intervals belong ("$200K/yr run-rate" — $180K–228K depending on price mix).

Rule: a deliverable containing a derived number that was not recomputed in code has not been QA'd. Optimism direction across multiple independent FAILs = systematic bias in the generating personas, fix the class not the instances.

### Stage 2 — Source-trace every state/census claim to PRIMARY evidence
Grep the claim's provenance. Panel-file-citing-panel-file = circular = downgrade to UNVERIFIED.
- "75 services / 62 live ports" traced only to the panel's own files. Live measurement: `netstat` 67 listening in 8xxx range, `lsof` 46 python/node listeners, `launchctl list | grep` 36 ds-/divinity entries. Right ballpark, zero provenance — and the cold-email skeleton put "75-service organism" in line 2 of a pitch.
- Fix: live-measure (netstat/lsof/launchctl/yaml grep) and correct the language, or label MEASURED-pending/ASSUMPTION. A fleet census job is a prerequisite for any external artifact carrying fleet-size claims.
- Claims that DID verify cleanly: PIML 4.2x (file on disk), SBIR $323K (strategy doc), ARC essay absent (confirms "0% until on disk" grade).

### Stage 3 — Calibration regrade of the priors themselves (rotated brain, different seat)
Domain personas (sales/pricing/revenue seats) assert priors from the INSIDE view. A calibration seat (the specialist engine, adjunct, superforecasting method) regrades them against reference classes with intervals.

Findings on this run: the 25/30/30 funnel was 2–25x optimistic vs published cold-outreach base rates (calibrated cold reply 4% [2–8%], unknown-sender close-given-call 10% [5–15%]); realistic first-deal price $5.5K [4–7K] vs $9.5K card; the D30 <$5K SAFE "trigger" fires at P≈80–90% — it is the base plan, not a trigger; warm asks carry ~21x per-ask EV of cold (computed 21.4x, stated ~20x — confirmed). Structure survived, magnitude did not: services lane reframed as evidence machine, burn deferral + SAFE prep as the actual cash levers.

## Pitfalls hit (each cost a fix — bank them)

1. **Registry/adjunct personas need PhD layering in the dispatch.** brain_integrity_gate greps the transcript for credential markers; a Tetlock dispatch with mode/method but no "PhD (Yale 1981), Annenberg Professor, Superforecasting" layering X-blocked PERSONA-SPEC-MISSING and forced a v2 re-dispatch. The SKILL.md main body already says "full 15-20 PhD layering" for adjuncts — it applies to QA/calibration seats too, including DS-registry codes (CAL-02). Include it EVERY time; it is what the gate matches.
2. **Write cited files BEFORE dispatching the seat that cites them.** Tetlock v1's brief cited QA-ARITHMETIC-AUDIT.md "if missing, findings are: <inline>" — worked, but fragile. Persist the audit to disk first; the brief then points at a real file (and later seats can read it).
3. **Verify the subagent's math independently before folding.** Parent-side recompute (Beta prior predictives, binomials, funnel products) confirmed 5 of 6 v1 claims and caught one silent assumption: v1's D30 EV ≈$700 vs computed $1,446 warm-only implies an unstated ~50% timing discount (payment-lands-by-D30). EV numbers must show their discount assumptions explicitly.
4. **Falsifier semantics change with the prior.** Under calibrated Beta(1.5,28.5), 0/30 cold replies is the MODAL outcome (P≈29–34%), not evidence the lane is dead — the D14 branch becomes rewrite + 30 more touches, not kill. Under Beta(3,9) the same observation was a 5-sigma rejection. Recompute falsifier thresholds whenever the prior moves.
5. **Specialist-gate 5-minute windows expire mid-QA.** Long audit chains re-trip "Sherman routing expired" on execute_code/patch — re-route (`specialist_gate.py --route --situation ... --specialist "DS <name>"`) and continue; batch the gate re-route with the next terminal call when possible.

## Fold discipline
One fold, same doc (locked principal preference): corrected arithmetic + calibrated priors + census downgrade go into the dossier in a single pass — never a second parallel document. QA verdicts carry intervals; the dossier keeps MEASURED/ASSUMPTION labels.
