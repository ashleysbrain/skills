# Honesty verification — false done-marks, gate wiring, overnight counts (2026-08-25 incident)

principal caught two false done-marks in one morning ("I cannot stand your lies").
This file carries the verification protocols that prevent the class.

## 1. Done-mark protocol
- NEVER mark a task `done` ahead of LIVE-verified output. If the run record
  shows failure (non-zero exit, empty report, SQL error), the state is NOT
  done — regardless of intent or narrative.
- Real incident: M3 telemetry task marked done while snapshot exited 2
  ("no such table: messages" — wrong DB path) and the report was empty.
- On a false done-mark: re-open the task, restate the false mark INSIDE the
  outcome record (documented, not buried), then fix and re-verify.

## 2. Compile-pass is not wiring
- A code gate inserted after `def f(...):` can land INSIDE the docstring —
  valid syntax, compiles clean, silently dead. Happened on 3 of 4 files.
- Verify placement: first snippet occurrence must come AFTER the def
  signature's docstring close.
- Spy-test execution: monkeypatch the gate with a recording shim, call the
  real function, confirm the gate fired N times:
  ```python
  calls = []
  def spy(kind='task', proposed_class=None):
      calls.append(kind); return {'allowed': True}
  mint_gate.gate = spy
  n = isomorphism_lint.mint([], dry_run=True)   # gate must fire even dry-run
  assert len(calls) == 1
  ```
- Test the reject path explicitly: simulate a cap violation (fake checker
  script exiting 1) -> `allowed=False` + reason -> the mint must die.

## 3. One gate, N writers
- A law binding N call sites gets ONE shared gate module (entanglement
  pattern), wired with a single call per site — never per-site copies.
- Built: `organism/mint_gate.py` (gate) + `your-stack/scripts/
  fleet_cap_check.py` (cap census), wired into flow_lint, gap_hunter,
  isomorphism_lint, security_audit mint().
- Flag fail-open vs fail-closed explicitly — currently fail-open on
  gate-load failure; fail-closed upgrade is a principal decision, not a default.

## 4. Overnight throughput decomposition
- Raw "N tasks done overnight" counts lie. Decompose before reporting:
  - group by title-series (87 near-duplicates of one incident != 87 wins)
  - count unique findings (spam loops re-mint the same 2 findings 25x)
  - check hour distribution (75 completions in one hour = loop burst)
  - isolate substantive work (was ~15-20 of 138)
- Loop self-service starves the priority lane: loops mint+close their own
  series; nothing binds them to principal-minted P1s. "Worked all night" is false
  if the P1 queue is untouched at dawn. Overnight autonomy requires an
  arbiter routing loop capacity to the priority queue.
- Spam-loop mints: cancel dupes, re-mint each unique finding once, queue a
  flow fix (mint-gate dedup by finding+target hash). Not silent bulk-cancel.

## 5. Work-smarter law (principal: "Mosaic is always. Work smarter")
- Find the few real entrypoints (e.g. the 4 mint functions) and build one
  gate — don't grep-patch every caller. Same pattern as the conduction
  spine: one enforcement point, many writers.
- Don't retry memory writes past capacity: persist in ledger/law docs and
  move on.
