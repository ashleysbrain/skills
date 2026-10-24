# Sequential N-Brain Review Passes — principal-Ordered Pattern (2026-08-25/26)

The principal's standard order for reviewing any significant design/process/workflow:
"look at this again from a different view... then run through adversarial group...
10 different brains that haven't hit it before... they don't run in parallel."

## The canonical two-stage arc (proven 3x this week: volley flows, reporting workflow, split strategy)

**Stage 1 — DIFFERENT-VIEW PASS** (one child):
- Fresh eyes, directives-as-lenses
- Examine the ACTUAL current flows/code (not the doc about them) — read source files first
- For each principal directive: does the current system serve it or violate it? Name violations with file:line pointers
- Output the list of concrete changes proposed (usually 5)

**Stage 2 — N SEQUENTIAL BRAINS** (one child, N sections):
- Each brain = a genuinely DIFFERENT DISCIPLINE (queueing theorist, game theorist, verification engineer, perf analyst, org designer, protocol designer, reliability engineer, cognitive scientist, physicist...)
- Each ATTACKS its predecessors (finds what they got wrong) and adds exactly ONE new finding
- Brain N reads brains 1..N-1 before writing — chain-of-custody
- Final brain = CONSOLIDATOR: verdict table on every proposed change (SHIP / AMEND / KILL), the amended design in plain words, top-3 risks, one literal critic line, and principal decisions rendered as up-to-3 BUTTONS (never prose lists — ADHD UI law)

## Proven findings from these passes (reusable heuristics)

- **Reward-structure beats intent:** if priority formulas or metrics pay for speed, agents WILL rush regardless of doctrine. Fix the arithmetic, not the attitude (the scheduler formula T×info_gain−cost ranks cheap-shallow over thorough — measured wall-clock cost is the fix).
- **Checkable gates get gamed:** presence-checks (does a CONCEDE field exist?) get rubber-stamped; DB-level invariants with collusion detection (stake-carrying seats, concession graphs) resist it.
- **Inverting a reward inverts the exploit:** replacing declared estimates with MEASURED quantities resists gaming better than flipping signs.
- **Queue pressure rushing is structural:** executors should see one task + rubric + budget, never leaderboards (audience firewall / queue opacity).
- **Capacity triggers belong on the growth rate (dL/dt), before ρ→1** — thresholds that fire at the phase transition arrive when the system can no longer respond.
- **Selftests that only assert exit 0 catch nothing in renderers:** golden-output tests must assert the actual rendered text (must-contain AND must-not-contain).
- **Watch for single-orchestrator chokepoints** and N-party extensions of 2-party lease patterns (stale-lease collisions need epochs).

## Output-format laws for the principal-facing digest

- Machine food (verdict tables, P1..Pn lists) stays on disk; principal sees synthesis + at most 3 decisions
- Decisions as BUTTONS with an Other field — never typed-letter menus, never long numbered prose
- Anti-fluff law: no "signature/defensible/green-lit" words without a live measurement behind them
- State the flat board: what exists, what's designed-not-built, what's merely specced

## Known failure mode of the arc itself

The Stage-2 child dies on the final long write (90s non-streaming timeout) after
completing all research — see subagent-failure-recovery §8 (finisher-dispatch
pattern). Dispatch Stage 2 with the SHORT-OUTPUT rule and instruct the
consolidator section to be written FIRST if token budget gets tight, or split
Stage 2 into two children (brains 1-9, then consolidator) for long reviews.
