# Review-2 panel: 10-seat re-review of shipped work — 2026-08-27

Session: principal ordered a second full adversarial review of already-shipped
conductor-surface work ("10x different brains... world class credentialed
and layered phds agents... not by you but by the right engines"). Verdicts:
`~/your-workspace/relabel-work/verdicts/review2-seat-01..10.json`.

## Seat taxonomy for RE-REVIEWS (distinct judgment types, not task count)

Wave 1 (6): frontend wiring architect · backend endpoint integrity ·
data-integrity scientist · security adversarial · HCI professor (question
process as first-class deliverable) · accessibility engineer.
Wave 2 (4): iconography coherence · performance hot-paths · provenance
auditor · red-team captain (pass-3: compares prior findings vs live state,
hunts one NEW defect class).

Waves sized to `delegation.max_concurrent_children` (6) — dispatch wave 2
immediately after wave 1 so both run while the orchestrator works.

## Per-seat dispatch contract (what every seat got)

1. Live URLs + exact file paths + the daemon PID lane.
2. Credential persona in the dispatch ("SEAT: BACKEND SYSTEMS ENGINEER
   (distributed systems PhD)").
3. An OUTPUT verdict file path + JSON schema hint.
4. A SAFETY contract: READ-ONLY, or test payloads prefixed `review2-seatNN`,
   or /tmp store copies with md5 verification live stores untouched.
   Data-integrity seat ran 12 constructed edge cases against /tmp COPIES.
5. Explicitly test both VALID and INVALID inputs (empty, bogus ids,
   oversized, wrong methods) — the invalid half found the honest-reporting
   defects the valid half never could.

## What each seat caught (scorecard)

- Wiring: PASS (36 buttons, zero dead) — confirmed structure.
- Backend: FAIL — ledger write 100% broken since first build (vacuous
  self-verification had reported it working); swallowed exceptions;
  hardcoded `guidance: true`.
- Data integrity: FAIL — dedupe over-collapse (min-denominator supersets),
  dedupe losers never archived (violates own nothing-lost law), corrupt
  lines silently dropped, no concurrency lock (lost updates 4/20 trials).
- Security: HIGH — CSRF on every POST (text/plain JSON is preflight-free);
  XSS/SQLi held; clickjacking headers missing.
- HCI: 7/10 — Ask modal had no chips while Respond/Research did; jargon at
  the commitment moment; count bug.
- A11y: FAIL — glyphs unlabeled, 31 non-focusable onclick elements, no
  focus trap, Escape closes drawer over half-typed modal.
- Iconography: PASS_WITH_NOTES — stroke ramp is deliberate; pin glyph
  weakest.
- Performance: PASS_WITH_NOTES — daemon 0% CPU; real risk was the same
  missing lock the data seat found, plus O(n²) overlap matching (fine at
  cap 60), events_24h unindexed scan (watch at ~100k).
- Provenance: PASS — ledger chain intact, all 8 openDrawer call sites carry
  the voice bar structurally; caveat: dvTarget only task-complete.
- Red-team captain: PASS-WITH-CONDITIONS — DESIGN stubs still on default
  view (2x-flagged trust breaker), count mismatch, hash-state loss (NEW
  defect class: navigation memory loss — refresh bounces to default view).

## Fix-then-falsify ordering after verdicts

1. P0 root causes (not symptoms): make silent failures VISIBLE first (error
   surfacing in API responses), THEN fix the mechanism (regex widened to
   the store's real ID shapes — both 6-digit legacy and 8-digit canonical).
2. Ship-blockers (DESIGN stubs, count integrity, hash-state) next.
3. Concurrency/security hardening (flock+atomic rename, Origin gate,
   frame-headers) — verify each with a live probe (evil origin 403; 7-thread
   race test zero losses).
4. Queue the rest in the ledger with explicit status; never silently drop.

## Key lessons

- The vacuous-verification catch (backend seat) was about the OPERATOR's
  method, not the product. A re-review panel MUST include a seat that
  re-audits the operator's own verification claims.
- Two independent seats (data-integrity, performance) found the same
  missing lock from different angles — convergent findings are high
  confidence.
- The red-team captain's NEW defect class (hash-state) was in nobody's
  prior findings — always ask the captain for one novel class, not just
  regression checks.
- Panels reviewing a moving target: re-dispatch rate-limited (429) seats
  with UPDATED context including fixes already shipped mid-review, or they
  report stale findings.
