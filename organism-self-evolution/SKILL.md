---
name: organism-self-evolution
description: "Build organism self-improvement scans and steer lanes."
version: 1.1.0
metadata:
  hermes:
    tags: [organism, self-evolution, anabolic, meta-qa, steer, deming, gap-scan]
    category: devops
---

# Organism Self-Evolution Ecosystem (the Anabolic Arc)

The proactive half of organism health. `organism-reflex-arc` is the
CATABOLIC loop (detect defects, heal, repair). This is the ANABOLIC loop:
scan for gaps, stagnation, and improvement opportunities 24/7, appraise
them with physics, mint them as typed work, and drive evolution without a
human relaying every idea. Built 2026-08-20 from principal directive #17
("the OS OS = brain forever: self-evolve + self-heal + self-correct").

Design doc (canonical): `~/your-org/your-stack/SELF-EVOLUTION-ECOSYSTEM.md`.

## When This Skill MUST Load

- Building or operating `organism/improvement_scan.py` (7-scan battery)
- Building or operating `gates/qa_meta.py` (QA-on-QA, the specialist engine)
- Adding principal steering ("give the agents a direction") via `gates/steer.py`
- Extending the rubric judge (mission/genome axes) or mission enforcement
- Designing any autonomous improvement/self-evolution loop for an organism
- Wiring new scans into existing daemons without minting new crons

## The Loop

```
SENSE -> APPRAISE -> MINT -> DISPATCH -> VERIFY -> LEARN
7+5      free energy  typed    existing     rubric     methodology
scans    + steer T    tasks    efferent     judge R8   L2 patch
```

**Anabolic vs catabolic split is the architecture.** The old unified
`self_healing_loop.py` livelocked (150,849 heartbeats, 1 repair) because
growth and repair shared one loop. Keep them separate: ORA heals what is
broken; this arc grows what is whole.

## The Organs

| Organ | Location | Role |
|---|---|---|
| improvement_scan.py | `your-org/organism/` | S1 stagnation, S2 unprobed capability, S3 defect recurrence, S4 gap aging, S5 sensor seizure, S6 dormant lane, S7 physics decay (gates that never SKIP, detectors that never fire) |
| qa_meta.py | `your-stack/gates/` | M1 judge rubber-stamp, M2 judge coverage, M3 gate selftest rot, M4 QA-pass nullity, M5 defect escape |
| steer.py + steer.json | `your-stack/gates/` + `stores/` | principal attention as temperature; ideas become trajectory without commanding builds |
| rubric_judge.py R8 | `your-stack/gates/` | done builds must honor the 8D genome they were minted with |
| manifest mission block | `mosaic.manifest.json` | mission as data ("8D health for humanity through healthy technology, from the middle out"), with enforcement chain |
| ci-battery-last.json | `your-stack/telemetry/` | selftest evidence contract written by ci_battery.py, read by qa_meta M3 |

## Steer Physics (principal steering lane)

A steer is attention, and attention is TEMPERATURE in the free-energy
gate: F = cost − T·info_gain. A steer raises T for its domains so more
candidates there GO — it changes the physics the gates run; it NEVER
bypasses gates.

**Afferent limb (built 2026-08-22):** `gates/steer_intake.py` +
`your-stack/stores/guidance-inbox.jsonl`. Human directives appended to
the inbox (one JSON line: {"from","source","text"}) are drained EVERY
anabolic pass by `autonomous_iteration.anabolic_pass()` — detect (is it a
directive?) → distill (domains + urgency→T, cap 2.0) → dedupe (domain
overlap + Jaccard ≥0.6) → mint via steer.py. Consumed lines archived to
`guidance-processed.jsonl`. Provenance law enforced at intake: no --source
⇒ exit 2 (fabrication), logged as a defect. Guidance enters as physics,
never as manual triggering (principal law 2026-08-22: "run 24/7 without my
direction; human guidance provides context").

- Linear decay from mint to expiry, floor T=1.0 (attention fades
  adiabatically, never snaps).
- **Provenance law**: every steer carries a stated human source
  (`--from ceo --source "telegram 2026-08-20"`). Agent-minted steers
  without a human source are fabrication.
- Mint: `python3 gates/steer.py --add --text "..." --domains fleet --temp 1.8 --days 90 --from ceo --source "..."`
- Live-verified physics: marginal candidate cost=1.0 info=0.8 flips
  SKIP (F=+0.20 at T=1.0) to GO (F=−0.44 at T=1.8); unmatched domains
  stay T=1.00 and their verdicts are unchanged.
- **Regex pitfall (2026-08-22)**: when a domain map lists multiple
  alternatives, wrap the whole group `(?:a|b|c)` in word boundaries —
  `\bui\b` style. Un-bounded alternations match substrings inside
  unrelated words ("g**ui**dance" → design domain, "b**ui**lding" →
  build) and mis-tag steers. Caught live when STEER-4/5 minted with
  wrong domains; corrected in steer_intake.py DOMAIN_MAP.

## Multiple QA Layers (principal directive: QA on our QA)

1. **L-micro** — rubric judge, deterministic, per-task (8 axes incl. R8).
2. **L-macro** — qa_meta.py, the specialist engine (DS-ECS-SUB-04.06.08): the QA
   system measures itself. Rubber-stamp detection: PASS rate > 0.97 on
   >30 scored tasks = broken gauge (Shewhart special cause), not a
   perfect fleet.
3. **L-panel** — rotating elite adversarial panels (fresh lenses each
   pass; e.g. Tanenbaum/Scheffer/Bridgman/Lyapunov physics reviews).

PDSA the system itself: Plan (rubric) → Do (build) → Study (qa_meta) →
Act (rubric patch).

## Extending the Arc (the working sequence)

1. Write the scan as a pure function returning a list of finding dicts
   (serializable evidence inside each).
2. Add to the battery list; extend `--selftest` (physics of the scan on
   synthetic input: alarm case MUST fire, varied-healthy case MUST NOT).
3. `--dry-run --verbose` against live data; READ every finding and
   verify it is real before trusting the scan.
4. Mint path: dedupe against open ledger titles (prefix match), then
   `task_ledger.submit(...)` with evidence in detail and origin
   `event:<organ>`.
5. Register the organ in `ORGANS.json` (name, kind=gate, path,
   selftest command).
6. Wire into the EXISTING daemon pass (e.g. `anabolic_pass()` in
   `autonomous_iteration.py`) — never a new cron (principal standing pref).
7. Reload: `launchctl kickstart -k gui/$(id -u)/<label>`; verify with
   `pgrep -fl <script>` that the new PID is live.
8. Re-run ci_battery; if pin DRIFT, re-mint the chain (see pitfalls).

## Exit-Code Contract (for daemon callers)

0 = clean, 1 = findings (HEALTHY — the scanner worked), 2 = broke.
Callers treat `rc in (0,1)` as ok; only 2 mints a defect. A scanner that
exits 0 on its own crash is a supervisor lying to its supervisor.

## Pitfalls

### Isomorphism warning: don't force names onto reality (2026-08-25 lesson)
The "NK Cascade" error: named a fleet after a 15-cell biological system when only 7 brains existed. Isomorphic names must match EXISTING state, not aspirational state. When the fleet grows, rename it. Pattern: design around what EXISTS, then provide upgrade path for future state.

### Collaborative compromise pattern (multi-brain reviews, 2026-08-25)
When doing design reviews, use multiple brains in COLLABORATION, not override. Pattern: Thompson finds the isomorphism error, Ravine proposes a correction, Nullius validates evidence — COMPROMISE emerges (Adversarial Cluster instead of NK Cascade). No brain overrules the others. The output documents each reviewer's view AND the compromise. Mastermind + entourage are MEASURED (closure rate, precision ledger), not asserted.

### Measure mastermind + entourage, don't assert (2026-08-25 lesson)
The "entourage effect operationalized" error: claimed operationalization without measurement. Correct pattern: mastermind = "together achieve what neither can alone" (proven via three-cytokine loop); entourage = high-quality reviewers elevate precision (measured via precision ledger). Any principle without a measurement channel is aspirational, not operational.

### Finding-vocabulary false positives (M4 lesson, 2026-08-20)
First live qa_meta run flagged 12 QA passes as "nullity" because the
detector hunted F-numbered findings while this corpus files G-numbered
gaps. RULE: before writing any content-matching detector, sample the
corpus vocabulary first (F#, G#, M#, DEF-#) and test the regex against
known-good documents that DO contain findings. A meta-scanner with false
positives is the same disease it hunts.

### Evidence source must be a file something actually writes
M3 originally read a telemetry stream nothing writes — every gate read as
rotted. Two-part fix: (1) make ci_battery.py persist
`telemetry/ci-battery-last.json` (results + ran_at per gate), (2) point
the scan at that. Never build a detector on an evidence channel that has
no writer.

### sqlite3.Row is not a dict
`row.get(...)` raises AttributeError. Values computed in a helper must be
consumed in the SAME function that computed them, or convert to dict
first. Hit live in rubric R8 (crossed-function `_genome_ok` was silently
never read — compute-at-point-of-use).

### Registry edits require pin re-mint
Adding a specialist to `personas/registry.json` makes ci_battery pin-diff
go DRIFT (by design — pins exist to catch registry drift). After any
registry edit: `python3 ledger/ledger_init.py --pin <n+1>` (next chain
number), then ci_battery must end `BATTERY PASS`. Verified 2026-08-20:
chain-5 minted after the specialist engine entered the registry.

### Postcondition-driven, never heartbeat-driven
A loop is alive only if its POSTCONDITION tables grow (findings resolved,
lessons learned), never because heartbeat rows accumulate. Every new
scan must terminate in a mint or a recorded SKIP — no observe-only modes.
Full livelock autopsy: `organism-reflex-arc` skill.

### Healthy scanners exit 1 on findings — do not "fix" that to 0
Findings are the scanner succeeding. Only exit 2 (crash) is failure.
See Exit-Code Contract above.

### Gap scans must terminate in SATISFACTION, not mint-piles (2026-09-02 lesson)
The isomorphism lint minted 113 "EVOLVE: isomorphism gap" tasks over
weeks; nobody did the science, and they piled at tri:review waiting for
the principal ("a lot of isomorphism gap tasks in there for me that should not
be for me... you are the one that should investigate"). A scan whose
findings are never SATISFIED is a mint-treadmill — same disease class
as the R2 volley treadmill. When a gap scan's findings name missing
KNOWLEDGE (register entries, mappings, docs), the operator AUTHORS the
missing content, re-runs the scanner to exit 0, then closes the minted
tasks citing that proof — the principal is never the gap-filler of last
resort. Falsifiability floors implemented as token lists lag the actual
domains in use (the lint's nature lexicon knew 10 tokens; honest
deformations using protein/gene/entropy/symmetry vocabulary were flagged
as metaphor drift) — widen the lexicon to the kingdoms actually present;
NEVER weaken the both-terms-required floor itself. Expect a re-mint race
window: a daemon-driven lint can mint new findings between your register
write and the next sweep — close residue in a second pass after a clean
exit-0. Full batch record:
`references/isomorphism-register-batch-2026-09-02.md`.

## Verification Commands

```bash
cd ~/your-org
python3 organism/improvement_scan.py --selftest
python3 organism/improvement_scan.py --dry-run --verbose
cd your-stack
python3 gates/qa_meta.py --selftest
python3 gates/qa_meta.py --dry-run --verbose
python3 gates/steer.py --selftest
python3 gates/steer.py --list
python3 gates/ci_battery.py                    # must end BATTERY PASS
```

## Related Skills

- `organism-reflex-arc` — the catabolic twin (healing, ORA, Virchow)
- `mosaic-surgical-edit-discipline` — how to edit your-stack files
- `elite-orchestration-default` — L-panel dispatch of adversarial panels
- `benchmark-analytics-self-evolution` (extension below) — specific instance for OS benchmarking

## Benchmark Analytics Self-Evolution (Extension 2026-08-27)

A specific instance of the anabolic arc for the OS OS benchmarking and self-evolution.

**principal directive:** "I don't want to see that we simply meet the benchmarks... I need in depth analytics on where we stand and then this should feed into the research studio and other process flows to find optimal ways to improve our standing on each benchmark... this should feed into the glial fleet queue and go through process and change improvement to self evolve, self correct, self heal, etc."

### The Benchmark Loop

```
BENCHMARK EXECUTION → RESULTS DB → BENCHMARK ANALYTICS
                                        ↓
                            ┌───────────┴───────────┐
                            │                       │
                            ▼                       ▼
                    RESEARCH STUDIO          GLIAL QUEUE
                    (improvement proposals)  (process improvement)
                            │                       │
                            └───────────┬───────────┘
                                        │
                                        ▼
                              CONTINUOUS BENCHMARKING
                              (daily/weekly cron jobs)
                                        │
                                        ▼
                              SELF-EVOLUTION CLOSED LOOP
```

### Components Built (2026-08-27)

**Execution layer:**
- `your-stack/gates/benchmark-execution.py` — runs benchmarks, stores results in `benchmark-results.db`
- Supports on-demand runs (`python3 benchmark-execution.py run --benchmark <id>`) and batch runs (`--all`)
- Benchmark runners: OS-CONDUCTOR-SURFACE, OWASP-LLM-TOP10-2025, NIST-CSF-2.0, PQC-READINESS

**Analytics layer:**
- `your-stack/gates/benchmark-analytics.py` — computes metrics, gaps, insights
- Metrics: pass rate, coverage, score distribution
- Gaps: weak benchmarks, regressions, anomalies
- Insights: trend summary, top gaps, recommendations
- Priority routing: HIGH (declining benchmarks), MEDIUM (weak benchmarks), LOW (stable)

**Integration layer (pending):**
- Research studio integration: create research tasks for gap analysis
- Glial queue integration: feed improvement tasks to glial fleet
- Continuous benchmarking: register cron jobs for daily/weekly runs
- Dashboard UI: show analytics on conductor screen (benchmarks drawer)

### Gap Analysis → Minting Pattern

Benchmark analytics identifies gaps and automatically mints improvement tasks:

```python
# From benchmark-analytics.py
if insights.get("priority") in ["HIGH", "MEDIUM"]:
    for i, rec in enumerate(insights.get("recommendations", [])):
        task_id = task_ledger.submit(
            title=f"[BENCHMARK] Improve benchmark standing ({i+1})",
            kind="research",
            lane="nervous",
            severity=1,
            origin="benchmark-analytics",
            flow="FLW-DECISION",  # or FLW-ADV for glial queue
            detail=f"Recommendation: {rec}\n\nMetrics: {metrics}\nTrends: {trends}\nGaps: {gaps}"
        )
        # Feed to glial queue
        _feed_glial_queue(task_id, priority=insights.get("priority", "MEDIUM"))
```

### Neuroplasticity: Effective Patterns

**From this session:**
1. Measure before visualize — build analytics layer before dashboard
2. Connect analytics to research studio + glial queue for self-evolution
3. principal wants deep insights, not just "meet benchmarks"
4. Close the loop: execute → analyze → improve → repeat

### Pitfalls (from this session)

**Import hell:**
- Multiple attempts failed because `from benchmark_execution import get_benchmark_results` failed
- **Solution:** Connect to database directly instead of importing from same directory
- **Pattern:** When both scripts are in same directory, connect to DB directly rather than import

**Type coercion errors:**
- `sorted_runs = sorted(runs, key=lambda r: r["ts"])` failed when `runs` was not a list of dicts
- **Solution:** Group results correctly before sorting
- **Pattern:** Verify data structure before operations

**Verification gaps:**
- Assumed "principal report = system state" without verifying what principal actually saw
- Assumed "patched code = daemon using new code" without verifying restart
- **Pattern:** Always verify live state, never assume

### Extension Files

- `references/benchmark-analytics-loop-2026-08-27.md` — detailed build log, error patterns, verification steps

## References

- `references/ecosystem-build-record-2026-08-20.md` — session build log:
  live verification outputs, the M4 false-positive autopsy, pin chain-5
  mint, steer SKIP→GO proof
- `references/adversarial-compromise-closure-loop-2026-08-25.md` — collaborative compromise pattern (Thompson + Ravine + Nullius), isomorphism warning, fleet-agnostic cytokine protocol, adversarial closure loop scan pattern
- `references/isomorphism-register-batch-2026-09-02.md` — the 113-task gap-pile satisfaction: register 14→55 entries authored, lint lexicon widening, re-mint race window, close-out sequence with wiring-gate wording fix