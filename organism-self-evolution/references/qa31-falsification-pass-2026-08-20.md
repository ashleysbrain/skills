# QA-31 Falsification Pass — 2026-08-20 (hermes / the specialist engine)

the specialist engine (rotated reviewer — builders were the specialist engine/the specialist engine, reviewer
must differ) falsified the same-day build of the self-evolution
ecosystem. Verdict: FIX-FIRST → 6 self-defects found, all fixed
live. Full doc: `~/your-org/your-stack/audit/
QA-PASS-31-SELF-EVOLUTION-2026-08-20.md`. This reference carries the
pitfall detail the SKILL.md summarizes.

## The six findings (all fixed + live-verified)

- **F1 sev2 — daemon-restart race.** Patched `anabolic_pass()` while the
  daemon was mid-restart; restart loaded OLD code; "wired" claim was false
  ~90 min. Fix: kickstart, then grep `iteration-log.jsonl` for the new
  `qa_rc`/`ci` keys. Verified 17:31:00Z entry shows both batteries.
- **F2 sev2 — evidence sink with no writer.** qa_meta M2 read
  `qa-meta-judge-scores.jsonl`; nothing wrote it. A detector that can
  never clear = permanent alarm = decorative. Fix: M1 appends every judge
  score as a side effect.
- **F3 sev2 — claim inflation in the mission law itself.** Manifest
  `enforced_by` cited "improvement_scan appraisal (info_gain semantics)"
  which did not exist — L11 violation by the builder. Fix: cite only real
  mechanisms (genome_gate minting, R8 axis, S7 scan).
- **F4 sev2 — gate without selftest broke the volley battery.**
  `build_forward_gate.py` exited 2 on `--selftest`; volley logged
  "selftest failures: 1" for hours. Fix: fixture selftest (detect /
  allowlist-exempt / clean-tree). Two fixture attempts failed first:
  bare PIN literal matched no signature regex; allowlist keyed on absolute
  path while scan keys on relative. Third passed; volley 0 failures.
- **F5 sev3 — cloud/local CI split-brain.** ci_battery ran only in GitHub
  Actions; M3 reads LOCAL telemetry/ci-battery-last.json. Evidence would
  rot past 7d. Fix: `ci_battery_daily()` in the iteration daemon, once per
  UTC day, rollover guard. Composition, not a new cron (principal pref).
- **F6 sev3 — new gates absent from GATE_TESTS.** steer, qa_meta,
  build_forward missing → M3 flagged them. Fix: added to GATE_TESTS; also
  learned task_events schema the hard way (actor_kind NOT NULL).

## Adversarial physics panel (salvage pattern)

Dispatched 4-lens panel (Tanenbaum/Scheffer/Bridgman/Lyapunov) timed out
at 1800s with 13 API calls done — all targets read, several adversarial
queries executed, no verdict written. Salvage instead of blind re-dispatch:
read the live transcript (`<agent-home>/cache/delegation/live/<id>/task-0.log`),
harvest executed evidence, run the panel's unfinished adversarial tests
yourself (free-energy edge inputs, scheduler claim races, dedupe
malleability), consolidate the verdict with explicit provenance note that
the dispatching reviewer completed the timed-out panel's program. Verdict:
SHIP WITH BINDING FIXES, 8 findings (F2 schema guard fixed live; F3 dedupe
by (origin,kind,subject); F4 log measured values with alarms; F5 mint-rate
cap; F6 F=0 tie → document or SKIP; F7 record T_eff trajectory; F8 poke
retry x1). All minted to ledger T-260820-0094..0099 with lens provenance.

## Market comparison method (arXiv primary sources, keyless)

web_search/web_extract billing-blocked → arXiv API via curl works:
`curl -sL "https://export.arxiv.org/api/query?search_query=all:%22self-improving+agents%22&sortBy=submittedDate&sortOrder=descending&max_results=8"`
then regex `<title>`/`<published>` (parse as text, not JSON). 2026 frontier
vs our build produced the ranked gap register: GAP-A variance-aware
acceptance (N>=3 deltas before an improvement closes; fragility paper
08-18), GAP-B skills-library drift detector (05-19), GAP-C anabolic
knowledge loop (07-21), GAP-D harness self-optimization (SBCO 08-10, defer).
Where we are ahead: verification is never self-authored — deterministic
gates + rotation law (reviewer differs from builders).

## principal ruling surface

Only kind=decision tasks reach the principal (conductor Immune view filters on
kind='decision'). Everything else executes autonomously. principal explicitly
rebuked padding the ruling queue: "ONLY if it REALLY needs my approval not
because you are lazy" — a stuffed decision queue is delegation failure.
