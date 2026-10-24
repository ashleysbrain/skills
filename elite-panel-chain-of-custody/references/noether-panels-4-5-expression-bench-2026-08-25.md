# Panels 4-5 + Expression Bench naming case (2026-08-25 PM)

Continuation of `noether-math-custodian-chain-2026-08-25.md` (panels 1-3). Same day, PM session.

## Panel 4 — Tarski/Gödel/Zorn/Banach/Hilbert/Nakamoto/Neumann/Perelman/Wiles/Tao (10/10 verified)

All ten implemented same-session:

| Brain | Finding | Implementation |
|---|---|---|
| Wiles (sev1) | invariant_probes stored as strings, never executed | N8 check runs every probe per pass; first run caught 4 path bugs + 1 dead probe (sigmoid pointed at ORGANS.json; real consumer = self_healing_loop.py) |
| Gödel (sev1) | custodian validates registry it also writes | `--selftest` known-answer mode (4 checks) |
| Neumann (sev1) | mass-falsify attack: inlet could remove ALL equations in one pass | falsify budget 1/scan; excess quarantined. LIVE-PROVEN: 3-falsify attack sim → 1 applied, 2 quarantined, sev-1 event |
| Tarski (sev1) | "verified" = grep found a string; presence ≠ truth | truth_tiers: presence (all) / numerical (bench) / semantic (advisor sustained) |
| Zorn (sev2) | no precedence ordering on conflicting equations | precedence law: N8 sev1 > free-energy termination > Lyapunov > opportunity weight > throughput |
| Banach (sev2) | crash mid-write tears the rulings inlet | tmp+rename atomic write |
| Hilbert (sev2) | axioms unstated | 5 axioms (cost, T range, info_gain, monotonicity, tier semantics) |
| Nakamoto (sev2) | any process can forge advisor rulings | principal auth: ceo/advisor-anantua/gg-live-aggregate only |
| Tao (sev2) | symmetry/conserved as free prose | structured fields split from noether_check |
| Perelman (sev3) | full dossier regeneration per pass for static content | registry-hash guard |

## Panel 5 — layered: Chebyshev/Runge/Hamming/Bode/Nyquist/Kalman/Huygens/Fresnel/Abel/Galois (9/10, 1 correct kill)

Layers: math (Chebyshev, Runge, Abel) → physics (Huygens, Fresnel) → systems (Hamming, Bode, Nyquist) → adversarial (Kalman, Galois).

- **Huygens (sev1):** kuramoto-order + max-flow-min-cut had NO numerical bench but sat in the registry implying verified. Built real benches: Kuramoto r over phase sets (identical=1, uniform=0, cluster>0.9, bounded 100 trials); Edmonds-Karp max-flow on hand-cut toy graphs including the lint's own law (non-bottleneck upgrade saves ZERO). Registry reached 6/6 numerical PASS — full coverage.
- **Gate kill done right:** Kalman claimed F=0 boundary untested — it WAS tested at (4,2,0.5)→0.0. Gate rejected; kill confirmed correct. Hardened with near-boundary determinism trial (|F|~1e-12) anyway.
- Abel: composition trial — precedence axiom numerically asserted (termination dominates weights up to 10,000×).
- Runge: registry wording de-fantasized (clamped log-linear has derivative kinks; NOT sigmoid-smooth).
- Fresnel: glymphatic K = principle-tier (implementation is a counting proxy — stated honestly).
- Hamming: N9 escalation — FAIL stamps surface sev-1 every scan until fixed/demoted; never-benched entries surface sev-2.
- Bode: bench stamps registry only on tier CHANGE (was 96 rewrites/day).
- Nyquist: bench extracts+execs consumer function source in isolation; dependency crash degrades to contract fallback, never kills the bench (rc=2 = all verification down).
- Galois: typed symmetry schema (`type:`/`quantity:` prefixes + 8-class invariance taxonomy).
- Chebyshev: tolerance 0.05 → 1e-6 (sqrt computed, not truncated).

## The Expression Bench naming case (principal challenge, first-class lesson)

Built as "bernoulli_harness.py". principal: "is it REALLY a harness?" — No. Software jargon
("test harness" tests CODE) misdescribed an organ that tests CLAIMS. Isomorphism:
registry = genome (claims/genes); the organ = EXPRESSION (runs the gene, checks the
phenotype against hand-computed truth). Renamed `expression_bench.py` = the specialist engine's
Expression Bench (law of large numbers: 200 randomized trials/equation).

**Law: name organism organs by isomorphism, never by software-industry jargon.**
When the principal questions a name, the question is usually a naming-law violation
signal. Same class as the DS-prefix and scientist-name laws.

## Its first catch (proof of value, day one)

Bench run #1: sigmoid trial FAILED — registry claimed [0,1] low=healthy; real code
returned 10.0 for healthy input (1-10 scale, 10=healthy, log-interpolated). Nobody
knew until a machine checked the arithmetic. Fix direction per the
registry-reality alignment law: registry describes the real code; never the reverse.

## Final state after 5 panels

6/6 equations numerical PASS (40+ trials), 50 brains, 50 findings, 49 gate-verified,
all implemented or minted-open with severity held. Selftest PASS. Daemon passes:
noether_scan (N1-N9) + expression_bench wired.
