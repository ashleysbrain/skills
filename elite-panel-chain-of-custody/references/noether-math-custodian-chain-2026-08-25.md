# the specialist engine-Custodian Chain (2026-08-25) — 3 Panels, 30 Brains, Gate Self-Hardening

The full-day build of the math/physics custodian (the specialist engine, DS-ECS-IMM-13.19.01)
for the the OS QA fleet, reviewed by THREE sequential 10-brain adversarial panels
with ZERO brain reuse across panels. This reference captures what each panel caught
that the builder and prior panels missed — the strongest evidence yet for the
rotate-brains-every-pass law.

## Panel roster (all distinct, 30 total)

**Panel 1 (build QA):** Popper, Shannon, Tanenbaum, Shewhart, Bridgman, Scheffer,
Lyapunov, Saltzer, Ravine, Nullius
**Panel 2 (custodian's own dynamics):** Kolmogorov, Germain, Cartan, Wiener, Gromov,
Hardy, Mandelbrot, Riemann, Grassmann, Navier
**Panel 3 (future/adhesion):** Feynman, Einstein, Dirac, Turing, Lovelace, Bernoulli,
Gauss, Laplace, Maxwell, Boltzmann

## What each layer caught that earlier layers could NOT

- Builder's own 9/9 battery passed; **Shannon** still found remediation-noun false
  positives ("the quick fix menu at the diner" minted a BUILD task).
- **Poincaré pass** (between panels 2 and 3) found: no fixed point (scan could never
  reach clean — demotion was prose not code), telemetry recurrence (120 duplicate
  entries/day — the cron.bak disease in jsonl form), whitespace-fragile probes.
- **Panel 2 caught the open feedback loop** (Wiener: scan logged but never minted to
  ledger) — the same 27%-closure disease the adversarial fleet had.
- **Panel 3 caught the one-directional bond** (Israelachvili pre-pass: no advisor
  feedback inlet) and the deepest physics defects: no units (Dirac), no admission
  rule for registry growth (Boltzmann), falsification not mechanical (Turing).

## Evidence-pointer polarity law (the hardest-won lesson)

The Nullius replay gate verifies PRESENCE by default. Absence claims ("X is never
called", "no reader exists") filed as presence greps get **rejected while being
TRUE**. Three failure shapes observed:
1. Absence claim, presence pointer → rejected wrongly. Fix: `expect_absent: true`
   mode on file_exists/grep/cmd/sqlite evidence types.
2. `DANGEROUS` wordlist false-positives on python builtin `open()` inside `-c`
   code — blocks legitimate read-only probes. Fix: mask `open(` before wordlist
   check; bare `open` as a command stays blocked.
3. `python3 -c "code with 'nested quotes'"` — shlex strips inner quotes, the probe
   fails with a misleading error. Fix: pass the code string as ONE argv element
   when cmd starts with `python3 -c `.
4. A finding can also be true with a pointer that matches LAW PROSE in a doc rather
   than the implementation gap — when the gate rejects but manual grep confirms,
   implement directly and record; don't fight the pointer.

## Gate self-hardening loop

When the panel attacks the gate itself and findings verify, the gate gets fixed in
the same session — expect_absent mode, wordlist mask, argv fix all landed mid-panel.
Result: panel 3 ran 10/10 verified with zero hallucinations on first filing. The
gate's precision improved because adversarial pressure was applied TO it.

## Falsifiable-registry pattern (advisor rulings)

For any registry presented to an external expert: verdict schema
(sustain | falsify | replace | demote), `falsify` → archive + remove next scan
(idempotent, marked applied), `replace` → swap math and credit the ruling id,
`replace`-after-`falsify` → re-admit from archive. Round-trip proven live:
kuramoto-order removed → archived → history-diffed → restored → rerun idempotent.
Units annotation + admission law (5 gates) + history jsonl + atomic writes are the
minimum physics-grade hygiene: a physicist's first questions are units, sources,
and what kills an entry.

## Dated artifacts (live organism, not this skill)

- organism/noether_scan.py — N1-N7 checks incl. research runner + rulings application
- your-stack/stores/equation-registry.json + .archive.json + .history.jsonl
- your-stack/audit/PHYSICS-DOSSIER.md + .export.json (B2BU twin, schema 1.1)
- organism/nullius_gate.py — the replay gate (expect_absent, wordlist mask, argv fix)
