# Sequential Research Chain Pattern (chain-of-custody)

principal correction 2026-08-27, verbatim: "why are they running in parallel??? you
know I don't like this.. it waters down the outputs... this is not how we
operate for these types of tasks."

## When this pattern governs

Any multi-seat RESEARCH or REVIEW wave whose seats contribute sections to a
shared, growing document. The ratio-request shape ("10x researchers, 20x
adversarials, 25x glial rounds") is the canonical trigger: each GROUP'S seats
run sequentially; groups may hand off to each other in triangle order.

Not to be confused with concurrent-blind adversarial panels (seats attacking
a FROZEN artifact blind, no shared document) — those stay parallel by design.
Discriminator: building a growing corpus = chain; attacking a frozen artifact
blind = panel.

## The pattern (proven live 2026-08-27, R1..R10 platform-layer research)

1. ONE shared target file, one section per seat, sections labeled (R1, R2...).
   Section order in the file need not match dispatch order — labels carry the
   chain. (R10 landed first from a killed parallel wave and R1 built on it fine.)
2. Dispatch seat N ALONE. Its brief says: READ the target file FIRST; cite and
   build on prior sections explicitly; flag contradictions, extend, never
   replace.
3. On completion, verify the SECTION ON DISK (header present, size sane,
   cross-citations present, recommendations block present). Never trust the
   child's final chat report — harness bugs corrupt reports while the work is
   fine (see pitfall below).
4. Only then dispatch seat N+1, its brief naming the now-complete sections.
5. Repeat until the chain closes; then the next group (adversarial, glial)
   attacks the completed corpus the same sequential way.

## Why sequential (measured)

Parallel seats each start from the same baseline; the corpus becomes N
independent takes with no compounding. Sequential seats read prior output:
the 2026-08-27 chain produced sections averaging 13KB with explicit
cross-citations (R2 extends R10's registry schema; R3 stress-tests R2's
contract; R5 wires R4's UI states to token reality; R6 extends R2's state
machine with ALTER-level migrations). principal's verdict: parallel "waters down
the outputs."

## Pitfalls (all hit live, 2026-08-27)

- dispatch_task rejects >6 tasks in one call — do NOT "fix" this by splitting
  into two parallel waves; that is the violation itself. Dispatch one seat
  per call and wait.
- Stopping a wrongly-parallel wave: children stop at iteration boundaries;
  their drain messages arrive later as status=error completions. Before
  assuming loss, check the shared file for partial pollution (grep section
  headers). Keep any seat that landed COMPLETE; discard only partials.
- Final-report corruption (NameError at the report step) makes completed
  children report status=error. The on-disk section is the deliverable:
  verify the file, not the report. Verify-by-disk was the standing bridge
  until the patched gateway code was loaded.
- Write-path schema mismatches: before inserting into a shared store
  (operator bus, ledger), read the ACTUAL schema (PRAGMA table_info) from the
  live file the writer code uses — guessed schemas write nothing (IntegrityError
  or silent null). Resolve store paths from the writer code's own constants,
  never from recall; three plausible-looking DB paths existed and only the one
  the code referenced was real.
- Rate-caps on automated minters: a false-positive flood (38 wrong mints from
  an over-broad error regex) exhausted a per-origin daily mint cap (40/40) so
  later legitimate mints failed. Two lessons: (a) match only final-status
  lines, never tracebacks mentioned anywhere in transcripts — children
  analyzing files that contain tracebacks false-positive; (b) visibility
  (bus posts) must never depend on mint success — link an existing task and
  post regardless.
- Watchdog/monitor wiring (proven 2026-08-27): automated catchers (stall
  watchdog) ship as monitor-mode cron jobs — the scan script runs every tick
  and only NEW catches change its output, so healthy ticks cost zero LLM
  (principal law: healthy = zero output). The catcher's triangle-response prompt
  must carry the corrected group mapping (adversarial finds gap → agent
  researches → glial fixes), or every catch routes wrong by default.
- Harness-bug lineage (failure-as-opportunity contract, T-260827-0142):
  when a harness defect corrupts child final reports (NameError class), the
  complete remediation is root cause + minimal patch + test suite + exact-
  condition repro + audit doc + ledger/bus closure + an OS adaptation
  (watchdog + on-disk verification bridge). Log the training failure to the
  tracking task's task_events; close the loop only when every leg lands.

## Adversarial chain wave (proven live 2026-08-27, A1..A20 platform-layer)

The SAME chain law governs the adversarial group after research closes. The
corpus freezes; seats attack it sequentially, each building a FINDINGS file
(not the research doc). Mechanics that made it work:

1. One findings file (e.g. `audit/PLATFORM-LAYER-ADVERSARIAL-<date>.md`),
   one section per seat (A1, A2...). Seat N's brief: read the full research
   corpus AND the findings file; do NOT duplicate prior seats' findings.
2. ONE DISTINCT ANGLE per seat, named in the brief ("yours alone; other
   seats take other angles"). Proven angle taxonomy: falsification,
   security, performance, privacy-contagion, accessibility+ADHD-law,
   data-quality, then continue (edge cases, mobile, cognitive load,
   honesty, integration, sync-conflict, auth-expiry, scale,
   failure-mode, dependency, API-drift, substrate-fit).
3. Feed prior findings FORWARD: seat N+1's brief cites the headline of
   every prior finding (e.g. "A1 found truth-gate empty-string defeat; A2
   found 3 P0s: registry probe shell-backdoor, privacy-flag tampering,
   render XSS no-owner — do not duplicate"). Compounding without pollution.
4. Findings only, never fixes: seats produce (vector/gap/severity/missing
   spec) entries; the glial build rounds implement. Adversarial seats
   editing the artifact they are attacking destroys independence.
5. Verdict vocabulary that worked (falsification seats): SOUND /
   FALSIFIED / UNVERIFIABLE-TIME-SENSITIVE / CONTRADICTS-SUBSTRATE.
   Severity vocabulary: P0-P3. Substrate verification beats doc critique:
   A1's best catch (truth-gate `IS NOT NULL` defeated by empty-string
   schema defaults) came from running the claim against the live DB.
6. Verify each section on disk (header, verdict/severity tags present,
   prior-seat citations present) before dispatching the next seat; log
   phase transitions (research closed / adversarial opened) to the
   tracking task's task_events so mid-wave stalls are recoverable.

Drain-message discipline: seats stopped from a killed parallel wave keep
arriving for minutes as status=error completions (iteration-boundary stops
+ the final-report NameError class). Acknowledge, re-verify the shared file
is unpolluted, continue the chain — never re-dispatch on a drain message.

## Chain mechanics at scale (proven live 2026-08-27, 10 research + 12+ adversarial seats)

- SPECIALIST-GATE EXPIRY: the gate unlock lasts 5 minutes; a sequential
  seat (2-3 min run + verification) reliably crosses the expiry before the
  next dispatch. Every seat needs a fresh
  `specialist_gate.py --route --situation "<seat N of M>: <angle>" --specialist "<DS name>"`
  call. Batch it into the SAME terminal invocation as the prior seat's
  on-disk verification (verify-Python + gate-route in one command) to save a
  round-trip — the pattern the chain converged on by seat 3.
- A DEGRADED sherman verdict still returns GO and the seat runs fine
  (observed on the honesty-seat route) — note it, proceed, no re-route.
- Angle-to-engine assignment per seat (OS picks, principal never routes):
  falsification→Popper, security→Saltzer, performance→Deming,
  privacy-contagion→Semmelweis, a11y→Luria, data-quality→Virchow,
  integration/drift→Tanenbaum, mobile→Kanwisher, failure-modes→Buck,
  honesty→Broadbent, scale→Haldane, buildability→Nedergaard.
- Research-seat briefs stay UNDER ~350 words of instruction + one file
  pointer; the shared doc IS the context. Adversarial briefs carry the
  prior-findings headlines (one line each) so seats don't duplicate.

## Verification battery (per seat, before dispatching the next)

```
python3 - << 'PY'
from pathlib import Path
import re
txt = Path("<target file>").read_text()
sections = re.findall(r"^## (R\d+) — (.+)$", txt, re.M)   # adjust label pattern
print("sections:", sections)
if "## <SEAT HEADER>" in txt:
    s = txt.split("## <SEAT HEADER>")[1]
    print(len(s), "cites prior:", "R<prev>" in s, "recs:", "recommendations" in s)
PY
```

Then log progress to the tracking task (task_events) so a mid-chain stall is
recoverable from the ledger alone.
