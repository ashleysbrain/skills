# Clinical Workflow Layer — Four-Brain Chain (2026-08-14)

Chain: the specialist engine (medical) -> the specialist engine (engineering) -> the specialist engine (OS/functionality) -> the specialist engine (physics verification). Consolidated into `organism/AI-HEALTH-BENCHMARK-STAGED-ROADMAP.md` v3.2.0. This reference preserves the per-brain detail.

## Osler: the six clinical gaps

1. **Screening/diagnostic/monitoring conflated.** Medicine separates cheap universal screens (high-sensitivity, tolerate false positives, escalate never diagnose) from expensive confirmatory diagnostics from continuous monitoring of known problems (trend thresholds, not state). The roadmap had all three instruments with no protocol for which fires when. Referral rule required: screen-positive -> diagnostic run -> diagnosis -> monitoring regime.
2. **No differential diagnosis (biggest structural gap).** Root-cause attribution is after-the-fact; medicine's core move is presenting-complaint pattern -> cause family BEFORE confirmatory tests. Example grammar: "rising p99 + flat seeded-R_0 + rising cost = impedance family, NOT cascade family — order swap-delta, skip SIR." 6-10 canonical syndromes as vital-sign vectors.
3. **No acuity tiers.** Scores without urgency; SREs act on sev levels not scores.
4. **No epidemiology.** A bad model version rolling out = an outbreak (correlated exposure, incubation lag, cluster detection). Registry forecasts; nothing surveils. Second unforkable data moat.
5. **No treatment formulary.** "Diagnosis that ends at the number is an autopsy service." Etiology family -> intervention class -> measured effect size.
6. **Smaller transplants:** iatrogenic harm (probes disturb the patient — track probe-induced degradation), second opinions (two harnesses on high-acuity verdicts), measurement consent fields.

## Bell: the engineering

**Build costs:** state machine M; differential YAML S; acuity S (pure function over existing quantities); fleet surveillance S-M and **80% free** (windowed consumer on the registry feed that already exists); formulary S but data-starved until 90-day registry depth. Dependency order: state machine -> acuity -> differential YAML -> surveillance -> formulary.

**State machine:** NORMATIVE -> WATCH -> DIAGNOSTIC -> MONITORED -> {RESOLVED|DECAYED}, 5 states ~8 transitions deliberately. WATCH entry: vital threshold OR L2 drift sign-flip 2 consecutive windows. DIAGNOSTIC referral: drift_rate > class-null 90th pct AND specificity gate. MONITORED: confirmed etiology, own-baseline tracking; exit = k windows within baseline band.

**Schemas:** differential YAML (schema differential/v1; pattern_id, vital_vector, etiology_family, confirming_instrument, refutation_test, prior — prior REQUIRED, no magic). Formulary rows with effect_size (CI, n) or rendered "unmeasured". Acuity = g(drift_rate, containment_status, forecast_p x severity) as label+inputs.

**Surveillance MVV:** single CUSUM on two vitals (p99, R_0) over version cohorts, batch daily, one alert channel. No streaming infra needed at n < 100 meshes.

**Engineering risks Osler missed:** state-machine flapping (needs hysteresis), alert fatigue (per-family alert budgets), YAML entropy (admission criteria, prune by registry-measured PPV), fleet privacy (k-anonymity), referral-rule Goodhart (meshes optimize to stay out of MONITORED; seeded harness stays held-out).

## Da Vinci: the OS surface

- **Health as OS primitive:** real OSes expose structured liveness states + transition rules + enforcement hooks (process states, load averages, cgroups, OOM killer, SMART daemons) — never "health" as a number. meshctl status (state + 5 vitals), meshctl why (differential = the dmesg of health), meshctl top (queue load, cost burn). Like load average: publish the trajectory, never a fused scalar.
- **UX rule:** severity maps to who initiates. Sev-3 OS observes (dashboard note); Sev-2 OS asks (one-tap consent); Sev-1 OS acts first + logs justification + retroactive veto (OOM-killer model). NORMATIVE = silence; the OS's job is to be boring.
- **Permission model:** autonomous = reversible-within-OS (throttle, rollback, re-run diagnostics); consent-gated = identity-changing (block swaps — "composition is identity, not ops"); marketplace = public acts (vendor re-ratings affect other users). Rollback snapshot before every intervention = do-no-harm primitive; every action undoable by construction.
- **the OS as health-native reference:** screening kernel daemon (~zero marginal cost), diagnostics idle-priority background workload, state machine in orchestrator, users instrumented by default — kills the setup doc's #1 risk (telemetry friction). One lattice node among >=3 (decoupling intact).

## Arnold: the verification (4 verdicts + 3 own findings)

1. **CUSUM ARL0: DECORATIVE** — no false-alarm budget = Goodhart's doorway. Patch: declare ARL_0 per cohort (500-1000 windows), derive h from Wald: ARL_0 ~= (e^(2kh)-1-2kh)/(2k^2), k = delta/2, invert numerically. Multiplicity: family false-alarm rate ~= N_cohorts/ARL_0; allocate or fold into Stage 0 BH.
2. **Hysteresis dwell-time: DECORATIVE** — naming flapping as a risk is not a guard. Patch: tau_min >= ln(mu)/lambda_0 windows (Hespanka-Morse) before ANY exit transition; rate beyond ADT budget = left planned-switching regime -> JSR re-analysis. Express windows in units of tau_acf.
3. **Score validity for auto-remediation: DECORATIVE as written** — an actor on an anecdote. Patch: mechanical provenance gate before Sev-1 (L2 tag + ICC on file, registry calibration ID, pinned version); no valid tag -> observe-only.
4. **Rollback as conservative perturbation: SOUND, one missing measurement** — patch: check post-rollback divergence D(post, snap) < epsilon (Stage 0 linear-response radius); D >= epsilon -> non-perturbative label, no L2 claim.

Own findings: (1) new magic numbers (90th pct, 2 windows, k windows, n_cell) -> route through Stage 0 calibration; (2) CUSUM residuals "vs class null" was ill-posed cross-system comparison -> residuals vs OWN baseline, class null for dispersion only, cohorts class-scoped; (3) DECAYED was absorbing with no re-entry -> recommissioning transition or explicit terminal-with-replacement.

**Verdict:** one more fix pass, small and localized — executed in the same consolidation. ARL formula and dwell formula went into the roadmap verbatim as required.

## The reusable pattern

Four-brain perspective chain: sequential dispatches, each carrying prior findings + explicit HANDOFF section for the next brain, physicist always closes with SOUND/DECORATIVE verification and exact patches. All patches applied in the parent-session consolidation. Word caps kept every brain under 70s.
