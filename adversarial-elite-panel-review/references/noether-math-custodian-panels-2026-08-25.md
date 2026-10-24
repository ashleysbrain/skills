# the specialist engine/Physics Custodian — 4-Panel Build (2026-08-25)

principal directive (verbatim intent): a QA fleet engine responsible for the math
and physics of the ENTIRE ecosystem. Scientifically and mathematically
accurate; physics LAWS abided. Role evolves to world models. Regular scans
for new research/equations that optimize the system or enhance UX. Math is
"super important all the way around." Human physics guidance incoming
(Dr. Anantua, EHT astrophysicist, willing reviewer, physics-credibility
door for funding) — the seat must PRESENT our math to him, in his own
B2BU organism under the operator agent-Live (future state, architecture-only).

## Organ shape

- **Seat:** the specialist engine (DS-ECS-IMM-13.19.01-v1.0.0, FLW-QA-FLEET math lane,
  FLW-MATH flow). Noether's theorem IS the role: every claimed symmetry
  must have a conserved quantity; prose physics = decoration.
- **Store:** `your-stack/stores/equation-registry.json` — harvested from
  code (never invented), each entry: claim + used_by + source citation +
  units + symmetry/conserved (structured fields) + invariant_probe
  (executable grep) + registered date.
- **Scanner:** `organism/noether_scan.py`, daemon-wired (`noether_pass`).
- **Advisor artifacts:** PHYSICS-DOSSIER.md + PHYSICS-DOSSIER.export.json
  (schema 1.1), regenerated only on registry hash change (Perelman).
- **Feedback inlet:** `stores/advisor-rulings.jsonl` → B2BU → parent B2B →
  the operator agent-Live → registry (never direct to core).

## Census-first law (before minting any custodian)

12 organs claimed physics; only 4/12 contained actual math. Zero equation
registry existed. No math research-scan lane. ALWAYS census what exists
before building — the gap report IS the build justification.

## The check families (N1-N8, each earned its place from a panel finding)

| Check | Law | Origin brain |
|---|---|---|
| N1 registry-claims-in-code | registry drifts from code; whitespace-normalized probes (`_norm`) | Poincaré |
| N2 unregistered-physics | physics-bearing code lines not in registry | build |
| N3 prose-physics | claims without equation tokens; OPERATORS not words count ("theorem" alone passes nothing) | Grassmann |
| N4 invariant-format | noether_check must name symmetry AND conserved | build |
| N4b invariant-operational | probe FIELD present (N8 executes it) | Cartan |
| N5 scan-lanes | research lanes configured | build |
| N6 research-runner | lanes FETCH (arXiv encoded URLs; query rot surfaces) | Riemann |
| N7 advisor rulings | falsify→archive+remove, replace→swap, replace-after-falsify→re-admit; idempotent | Turing |
| N8 execute-invariants | probes RUN every pass; broken invariant = sev-1 | Wiles |

## Panel findings → implemented fixes (all four panels same day)

**Panel 2 (Poincaré fresh pass):** no fixed point (added executable
demotions path — N3 honors it); telemetry recurrence (120 duplicate N2s →
recurrence-suppression logging, only state changes recorded);
whitespace-fragile probes (`_norm()`).

**Panel 3 (Kolmogorov/Germain/Cartan/Wiener/Gromov/Hardy/Mandelbrot/
Riemann/Grassmann/Navier):** Wiener — scan logged but minted nothing (open
feedback loop = the 27%-closure disease; now mints class-fixes per
check-family). Cartan — invariants asserted not operational. Grassmann —
EQ_TOKENS gaming surface. Riemann — lanes without a runner. Dirac — units
required (cost [compute-seconds], T dimensionless, info_gain [bits]).
Boltzmann — admission law: 5 gates for entry (named math, citation,
verified consumer, symmetry+conserved, units).

**Panel 4 (Tarski/Gödel/Zorn/Banach/Hilbert/Nakamoto/Neumann/Perelman/
Wiles/Tao) — 10/10 verified, 10/10 implemented:**
- Tarski: truth_tiers (presence = grep-verifiable; numerical = NOT YET,
  stated honestly; semantic = advisor sustained). Grep ≠ truth.
- Gödel: `--selftest` known-answer mode (custodian detects own corruption).
- Neumann: mass-falsify guard — max 1 removal/scan, excess quarantined
  (LIVE-PROVEN with 3-falsify attack sim: 1 applied, 2 quarantined).
- Wiles: N8 EXECUTES probes — first run caught 4 path bugs + 1 dead probe
  (sigmoid pointed at ORGANS.json; re-targeted to real consumer
  self_healing_loop.py). Proof the check works is it failing correctly.
- Zorn: precedence law (N8 sev1 > free-energy termination > Lyapunov
  stability > opportunity weight > throughput; termination dominates
  continuation per principal law-block axiom).
- Hilbert: 5 axioms declared (what cost/T/info_gain MEAN, monotonicity).
- Nakamoto: rulings require authorized principal (ceo, advisor-anantua,
  gg-live-aggregate); unauthorized rejected and marked.
- Banach: atomic inlet writes (tmp+rename). Laplace: atomic registry writes.
- Tao: symmetry/conserved as structured machine-readable fields.
- Perelman: dossier regenerates only on registry hash change.

## Advisor-liaison law (Anantua)

The dossier's questions are ASKS not claims: falsify our analogies, find
missing invariants, judge the Friston free-energy adaptive-analog usage,
specify latent-variable structure before trusting world models. Q5 asks
outright "which registered equations would you reject as physics-washing?"
His rulings become MECHANICAL: falsify removes an equation from the
registry next scan (conserved quantities enforced by code, not debated).
Feedback path B2BU→B2B→the operator agent-Live→registry per B2BU feedback law; export
content scoped to physics/math only (firewall: no internal organism state,
no task IDs, no harness names).

## Transferable laws (apply to ANY claim-registry system)

1. Presence-tier verification (grep) is the FLOOR, not verification. State
   truth tiers honestly; a registry that overstates provenance repels the
   exact expert it was built for.
2. A verifier that writes what it verifies needs a selftest with known
   answers (Gödel); author ≠ verifier otherwise undetectable corruption.
3. Any inlet that can delete needs: principal auth, rate limit on
   destructive ops, quarantine for excess, atomic writes.
4. Config without a runner is prose (Riemann): every "we scan X" claim
   needs executing code or it's decoration.
5. Stored checks must be EXECUTED checks (Wiles): a probe field that is
   never run is a worse lie than no probe — it looks operational.
6. Units first (Dirac): a physicist's first question; annotate every
   equation or lose credibility immediately.
7. Recurrence suppression in scanner telemetry: identical findings every
   pass are the cron.bak disease in log form.
8. Round-trip test destructive paths with synthetic data, then CLEAN UP
   (attack sims, test rulings, test mints) — production state restored,
   archive/history keep the trace.
