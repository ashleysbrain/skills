# Sequential adversarial wave — 2026-08-27 session (platform-integration layer)

Session record for the 30-seat sequential wave (R1-R10 research, A1-A20
adversarial) run under the chain-of-custody law. Numbers and failure modes
below are from this session's live logs.

## Wave shape that worked

- Target files: research corpus and adversarial findings file, one file each;
  every seat APPENDS a `## <seat> — <angle>` section. This gives free
  crash-recovery state: the file itself is the ledger of what completed.
- Seat contract skeleton (kept identical across all 30, only the ANGLE and
  the prior-seat list changed):
  - seat id + "SEQUENTIAL wave (chain-of-custody — never parallel; each seat
    reads prior findings before starting)"
  - persona (DS <Scientist>), READ FIRST list (corpus + findings file),
    "do not duplicate A<n> (covered X)"
  - ANGLE (yours alone): numbered attack list specific to the angle
  - OUTPUT: append section header exactly; entries format (failure | gap |
    missing spec); one-line wave summary; "Verify section + last 3 lines on
    disk. Known harness bug may corrupt summary; on-disk section is the
    deliverable."
- One seat ≈ 95-220s, 9-17KB per section. 20 adversarial seats produced
  272KB of findings with 13 blocking items.
- Anti-duplication line is load-bearing: "A3 covered single-user perf
  numbers; do not duplicate" kept 20 seats from converging on the same
  findings.

## Failure modes hit (and the response that worked)

1. **Parallel dispatch during mandated-sequential wave (twice).** Trigger
   both times: the async drain message arriving while I was mid-flow —
   treated it as "dispatch next N seats now". Correct response: verify the
   drained seat's section on disk, stop any parallel-dispatched extras,
   log the training failure to the ledger, continue solo.
2. **Harness summary corruption (`max_iterations` NameError)** on every
   seat R3 onward. status=error, no summary — but sections landed fine.
   Response: on-disk verification became the only acceptance gate; never
   re-dispatched a seat whose section existed.
3. **Rate limits (external providers).** A1 logged 11 rate-limit warnings;
   aggregate across session: 38 delegations with 429s. Adversarial seats
   were steered to read the corpus instead of searching; research seats
   (R3: 15 rate-limit hits) were the ones that needed the web.
4. **principal ping needed to resume after crash.** Machine died mid-wave; on
   restart no automatic resume happened because nothing polls the wave
   state. Stopgap (this session): rebuild wave state by enumerating
   sections in the findings file vs the roster. Systemic fix belongs to a
   durable chain-checkpoint (distinguish from estra_reanchor.py, which
   checkpoints the OS bus dispatch chains, NOT delegate_task chains).

## Per-seat angle roster (for reuse as a template)

falsification/truth-gate, security (XSS/backdoors/token theft), performance
quantification, privacy contagion/inference, accessibility (WCAG 2.2),
data quality/schema forensics, integration/vendor drift, mobile/touch,
edge cases/outage recovery, honesty/plain-words trust contract, scale +
growth trajectory (B2C/B2B multiplicity, cutover triggers), substrate fit +
buildability (against live code, dual-writer hazards), dependency +
supply chain (OAuth libs, MCP sandboxing, pinning), cognitive load / ADHD
law (state vocabulary, affordance budgets), i18n/RTL, auth expiry +
revocation cascades, UI truth-gate render path (gate location, cache
invalidation), scale x data-quality intersection (reaper cadence, sampling,
tier-entry gates), substrate conformance (column types, portable SQL,
pragmas, migration versioning).

## Related records

- Laws pinned to `stores/glia/memory-pins.jsonl` (chain-of-custody,
  footer/human-surface law).
- Ledger task T-260827-0145 (triangle volley) carries the training events.
