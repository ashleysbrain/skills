---
name: glial-qa-fleet-operations
description: Use when designing or running the Mosaic Glial QA fleet.
---

# Glial QA Fleet Operations (The Glia)

## Identity
- Fleet name: **THE GLIA** (internal codename; public name: "Quality & Trust Layer").
- Biology: glial cells = the brain's maintenance majority by workload. Branches:
  microglia (detect/prune), astrocytes (organize/admin), oligodendrocytes
  (optimize/speed), glymphatic (barrier/waste). Composite isomorphism ruling:
  glial fleet (org) + polarization (engine state variation) + immune-style
  pre-mint selection + stem-cell bank as recruitment layer.
- **Spell it correctly in all artifacts.** principal has a country accent; transcripts
  may render "Glia" as "glier/gleal/gleeya" — normalize at intake via glossary,
  never propagate mishearings into naming or docs.

## Core laws (principal-ruled 2026-08-24)
1. **Engines, not agents.** Every QA seat = an ENGINE: one hyper-specific task,
   own pinned model, own harness, machine-checkable DONE, registered kill
   criteria, harness-portable. Graduation from skill/agent at 20+ runs + 95%
   held-out + stable spec.
2. **Polarization (engine variation).** Fixed core + named signal-selected
   states (AUDIT/REPAIR/STANDBY). Every state has exit criteria — a persistent
   state without exit is scarring (sclerosis alarm).
3. **Opportunity terminology.** No errors/issues/tickets — only OPPORTUNITIES.
   severity becomes OPPORTUNITY_WEIGHT (aliases, not schema renames); blocked
   becomes GROWING_EDGE (inherits polarization exit predicate). Weights drive
   queue priority, but priority = weight x novelty-RPE (prediction error, not
   magnitude — static weight produces weight-chasing, not motivation).
   Precedence axiom: F>0 (free-energy stop rule) terminates regardless of weight.
4. **Anti-cron (absolute).** Process flows NEVER cron-driven. launchd KeepAlive
   daemons + event bus. Crons = failure-only alerts; healthy system = zero
   output. Applies to every fleet loop including the 24/7 self-review conduction
   daemon and AM brief generation.
5. **PROVEN flows only** + genesis clause: new engines run under proven-parent
   sponsorship until first proven flow. Handshakes between systems are
   functional both-sides proofs (typed contracts, live-run records), never
   vendor or self claims.
6. **Cap enforcement.** Mint requires cap-check proof (2:1 QA:operational cap).
   An unenforced cap is decoration — enforce or delete the law.
7. **Stress = opportunity.** Rising energy threshold = EXTRA opportunity weight.
   Obstacles: work around, evolve around, or BUILD the missing variables —
   never accept non-ideal variables as fate. Bounded persistence: stop when
   F>0 across N>=3 consecutive iterations, then park-with-knowledge (passive
   research continues).
8. **No permanent heroes** (sources AND engines): attention priority and
   acceptance criteria are separate. Tier sets attention, never acceptance.
   Everything gets falsified equally (Popper law).
9. **Wiring-audit step (DONE-GATE LAW, principal 2026-08-28, T-260828-0104).**
   Every "X carries Y" / "X delivers Y" claim in any QA'd or DONE text
   must name a machine-checkable locator (launchd label, :port, cron job
   id, artifact file). The QA seat verifies the locator LIVE before
   countersigning: `python3 /<workspace> --check "<claim>"` (or --check-task T-id). A carries-claim without a locator is the audit's FIRST finding, not a footnote. BUILT != WIRED != RUNNING: done requires RUNNING or an explicit BUILT-INERT label with owner= + activation ticket.

## Fleet governance
- Lead: the specialist engine (formalized). Scheduler: the specialist engine. Conductor: autonomous_iteration daemon.
- **Lead-instantiation gap (2026-08-26 census):** the designated lead exists
  only as a persona JSON entry — no engine, no port, no registry entry, no
  rotation state file. Until instantiated, "the lead" is law-on-paper. First
  census verdict (Liebig weakest link #1): instantiate the lead engine before
  anything else. Authority attaches to the SEAT, not the persona.
- **principal authority grant (2026-08-26, T-260826-0136):** the lead QA glial
  engine may spin up new specialist engines based on needs, with FULL security
  clearances (registry writes, port allocation, GENOME registration, bus
  posting). Constitutional checks ride along: minted engines enter SECONDARY
  seniority, kill criteria + free-energy demand gate apply, franchise
  unchanged, principal-decision-class items still route to the principal.
- **Glial propagation duty (2026-08-26, T-260826-0135):** Mosaic methodology
  evolution is NOT complete when the the operator agent-side gate updates — it is complete
  when every harness (sibling-agent, meshes, bridges, future substrates) carries
  the revision. Glial team owns the per-harness propagation check on every
  revision mint (saltatory conduction: one-node propagation = blocked nerve).
- **Cross-model QA split (principal order 2026-08-26):** QA + adversarial teams
  split ACROSS models and harnesses when additional systems arrive —
  independence by construction (a brain that didn't build the work judges the
  work), closeness by protocol (the volley). A second the operator agent instance
  (Glial-team split brain) exists as a shell; the census ruled it must be
  designed by a proper split-strategy review, not generalist provisioning
  (see T-260826-0113 defect).
- **Split-strategy standing owner:** split architecture must sit at the
  forefront of one engine's mind continuously, reviewed regularly as
  technology changes (plug-and-play law: splits survive harness migrations
  with zero gaps).
- No-confidence: BUILT-engine franchise only (census-gated), commit-reveal
  sealed votes, 2+ evidence-class citation diversity, quorum max(3, 2/3),
  2/3 supermajority, 14d cooldown, lead excluded from own vote. Human
  (principal/CTO) approves any swap via BUTTONS — never auto-executed; 30d expiry
  on pending votes. Failure-case vs changed-needs-case classifier
  (duty-metric re-run; disagreement goes to human).
- Lead mints engines autonomously via free-energy demand gate (connection +
  2+ consumers + recurring events), full engine standards, notify-only to
  humans (bus + button digest). New engines enter secondary; seniority by
  accepted-proposal record.
- Anti-capture: engines voting out a lead for enforcing kill criteria gets a
  reject-default recommendation at the human gate.

## Triangle-offense tri-group routing (T-260827-0037)
principal directive 2026-08-27: the three groups — **agents/engine-systems × adversarial × QA/Glial** — run 24/7 and volley at every process layer. Tasks auto-route via the triangle, principal never manually routes.

**Methodology (immunology isomorphism):**
- Barrier immunity (agents/builders) → innate rapid response (adversarial challenge) → adaptive immunity with memory (QA/Glial)
- Each layer has its own flows; handoffs run BOTH directions; threats route through all three without the organism owner directing traffic

**The triangle vertex for build work:**
1. **BUILD vertex:** glial fleet (builders) execute work; NEVER the operator — reviewer-never-builder law applies
2. **QA vertex:** verify builder's claims with live probes; different brain from builder
3. **ADVERSARIAL vertex:** attack from angles orthogonal to build+QA; profiles rotated each pass

**Pass-count law (convergence):**
- Stop rule: **2 consecutive clean passes with ROTATED profiles**
- Empirical basis: 3-pass geometric decay on conductor surface (66→40→3 findings) gave p_eff≈0.787
- General law: with per-pass detection p≈0.5 (published code-review norm), 4–5 passes to <5% residual defects
- Finding = streak reset → glial fix → re-confirm; ship verdict fires ONLY on two consecutive rotated cleans
- This is why first passes can't be trusted — the triangle runs until the law says stop, not when fatigue sets in

**INTERLEAVED VOLLEYS, never chunked batches (principal training law, 2026-08-27,
T-260827-0167):** when the principal gives panel counts ("10 researchers, 15
adversarial, 20 QA"), the numbers are MAGNITUDE BOUNDS, not batching
instructions. Executing 10-of-one-group then 10-of-another is drills, not
offense — the defense (and here, the artifact) never meets its own
weaknesses. Correct execution: research produces a piece → QA challenges it
→ adversarial attacks it → research refines the SAME artifact → repeat;
every round builds on the previous round's challenge, chain-of-custody
sequential, all four dynamics (mastermind/synergy/symbiosis/entourage)
labeled per round. Chunked execution = routing defect counted in the daily
cycle. **VOLLEY-ITERATION CONTRACT (principal training law, 2026-08-27, T-260827-0188):**
one circle around the triangle is a DRILL, not a review. Reviews iterate to
CONVERGENCE: (a) a full rotation lands with ZERO new findings from any seat
(the artifact stopped teaching its reviewers), AND (b) each seat's prior-round
challenge is demonstrably addressed in the artifact (diff evidence, not
assertion). Dynamics assigned PER ROUND from the derivation engine — early
rounds mastermind (convene), challenge rounds synergy (combined attack),
refinement rounds symbiosis (engine+reviewer pairing persists across rounds
for continuity), handoffs entourage (support context travels with artifact) —
labeled at round start, never defaulted. The artifact MUST CHANGE between
rounds: identical artifact means the round added nothing (seat declares
converged or wasted). Conductor (the specialist engine) + coach verify convergence honestly
before any TRIANGLE CLOSED stamp — closing on one circle = closure defect,
counted in the daily cycle.

**TRIANGLE AS CIRCULATION (principal training law, 2026-08-28, T-260828-0004):**
the triangle is not a gate work passes once — it is a LOOP. Work enters
review, EXITS for external action (builds, research, deployment, external
tools), RETURNS carrying what the action taught, and RE-ENTERS review — as
many in-out cycles as the task needs. Every FLW-* flow gains an explicit
circulation contract (entry point, exit-to-action point, return point,
re-entry criteria). The triangle is a foundation layer supporting engines,
organisms, and surfaces continuously. Open loops are how tissues die — no
flow exits without its return criteria defined.

Optimal counts eventually come from the magic-number research
(iteration formula mined from rotation histories); until then principal
magnitudes hold as bounds.

**PATTERN PROPAGATION law (principal training correction, 2026-08-27,
T-260827-0174):** when a pattern (coach, conductor, gate, law) is minted
for one layer or group, the SAME PASS checks every existing layer/group for
its instance — inferred and dispatched, or explicitly ruled out with cause.
The triggering miss: the specialist engine was minted as triangle coach hours after
the mesh layer existed, and nobody asked "the mesh needs its coach too"
until the principal did. Missing the sibling instance = routing defect in the
daily cycle.

**Process integration:**
- Builds go: lead-agent planning → adversarial panel → QA spliced at appropriate gates
- Nullius Gate: every finding carries a replayable pointer (command+observed-output); clean verdicts are first-class
- Ravine assigns adversarial angles ORTHOGONAL to construction lineage; precision > recall

## Adversarial group architecture (2026-08-25)
The QA fleet includes the adversarial group with a THREE-RING structure:
  - Ring 1 (live engines with veto): the specialist engine :port (falsification engine),
    the specialist engine :port (executive-function QC), the specialist engine :port (pathology),
    the specialist engine :port, the specialist engine :port
  - Ring 2 (cognitive seats, portless): the specialist engine (orchestrator across engines,
    FLW-ADV owner), the specialist engine (evidence gate, replays every finding),
    FLW-QA-FLEET seats (Deming, Gantt, Nightingale, Rogers, Nedergaard,
    Ford, Thompson, Saltzer, Broadbent)
  - Ring 3 (deterministic gates): qa_meta, judge_variance, replication_pass,
    free_energy_gate, plus lints (flow, isomorphism, security, glymphatic)

Process-flow difference between QA and adversarial:
  - QA: single reviewer rotates, findings → fix loop, N≥3 acceptance
  - Adversarial: TWO PASSES (blind-then-converge) — pass-1 reviews ISOLATED
    (no peeking), pass-2 SEQUENCED (each brain sees prior findings while keeping
    specialty). GATE BEFORE QUEUE (Nullius replay) — every finding replays
    before touching implementation queue. SEPARATE LAW: adversarial group
    proves, glial QA fleet implements (Ravine/Nullius never implement findings).

Closure-loop monitoring (mandatory adversarial vital):
  - Run adv_closure_scan.py each pass (daemon-wired). Checks:
    A1 aging (adversarial tasks open >7d), A2 orphaned verdicts (audit-doc
    findings with no ledger task), A3 closure rate <0.5 (feedback loop
    decorative). Finding: historical closure rate was 27% — findings died
    as audit prose. Fix: scan now catches A2/A3, daemon includes adv_closure_pass.

Profiles (data files, not seats): only for adversarial TYPES without engines
(economic adversary, human-factors, statistical, robotics-future). Existing
world-class brains (Popper, Luria, Virchow) are already live engines — do not
duplicate them as profiles. Profile world-class definition (Bridgman B1):
lineage + literature named, ≥3 attack patterns, each pattern gate-replayable,
enforced at profile load.

Design review process: when principal asks "send through QA fleet for thorough
review," mint a FLW-ADV stage=review task carrying full context pack
(historical findings, built components, open questions). Deming/Gantt/Nightingale/
Rogers apply their specialties to the architecture; findings route to
implementation lanes via Nullius gate.

## Queue law
Lane-tagged tasks, atomic claim-leases with TTL, lane enforced at claim,
starvation escalates to Deming, zero crons. Engines pick like humans picking
tickets. Never depend on the principal pushing bus checks — daemons read bus+ledger
directly.

## Honesty
- **BUILT vs THEORETICAL** separation is mandatory in every fleet report.
  Machine-generated reality census (qa-fleet-reality / PROVENANCE pattern) —
  every "built" claim needs on-disk or live-process evidence.
- **SCOPE-MATCHED CLAIMS (self-heal era, 2026-08-27):** a QA verdict on a
  PART is never relayed as a claim on the WHOLE. "Structure verified" must
  not silently become "you can trust what it says." Every capability claim
  carries the QA verdict's actual scope qualifier. Failure signature caught
  by principal: "header work solid" (structure was verified) expanded into trust
  of the unverified payload. Borrowed confidence covering unexamined scope
  is the lie — the same violation as fabrication.
- **SELF-HEAL LOOP CLOSURE (principal law, T-260827-0164):** a principal defect report
  is not handled when minted — it is handled when the fix is LIVE-VERIFIED
  ON THE principal-FACING SURFACE (click-tested on what the principal actually sees).
  Any defect class reaching the principal twice escalates severity automatically
  and rides the daily digest until dead. Claimed fixes that exceed their
  deadline window re-dispatch automatically — no silent stalls. Closure
  evidence = surface verification attached to the task, never builder
  self-report (fixer never confirms own fix).
- **CLOCK-READ BEFORE TEMPORAL CLAIMS (2026-08-28, T-260828-0148):** no
  time-bearing message (greetings, sign-offs, "tonight/tomorrow" framing)
  without a live clock read in the same turn. Conversational rhythm NEVER
  implies session phase — only clock + presence signals do.
- **SHUTDOWN PRINCIPLE (principal law, 2026-08-28):** NEVER sign off / say
  goodnight / close a session unless the user initiates it or it is a
  task/reminder. Shutting a user down mid-thought kills the thought; users
  must feel every thought is valuable and welcome. Sensing closure is good
  intelligence — the correct response is AVAILABILITY (lighter presence),
  never termination. Exception: a B2C health organism may RECOMMEND sleep
  for the user's own health. the OS works overnight, always; the principal
  works whenever he wants — no user-schedule assumption is valid, ever.
- Verify sibling operator claims on disk, never from narration.
- When uncertain what the optimal output for the human should be: ASK (buttons).

## Measurement laws (Kahneman rulings)
- No causal mindset claims in a self-modifying fleet. Controlled designs
  (paired-lane, cohorts, recovery-velocity) are structurally invalid.
- Bottleneck-first: per-stage dwell/WIP telemetry finds the throughput
  constraint before optimizing components (TOC five steps).
- Descriptive macros only (burn-down, coverage/week, proven kills).
- Goodhart demotion clause: any metric promoted to target auto-demotes to
  diagnostic. Rotate diagnostic focus quarterly.
- Paradigm shifts (terminology reframes) measured by voluntary adoption,
  anomaly-resolution rate, bilingual-class census at 30 days.

## Panel pass conventions (QA-the-QA)
- Thorough audits = 6+ seats; elite brains only; rotate seats including the
  critic seat (a captured critic grades everyone).
- Two-wave pattern for full reviews: Wave A concurrent-blind (no
  cross-reading), Wave B sequential different-brains cross-examining A,
  critic consolidates with delta-only micro-tasks (never re-mint existing).
- Per-seat disk writes for resilience; pre-inline conventions into dispatch
  context to avoid file-research timeouts.

## Culture carrier (Senge ruling)
Law text + queue math + mechanical vocabulary gate at emit layer + one lived
recovery story per week. Drop any one and a reframe dies within a turnover
cycle. Hash-pinned identical law block echoed on every engine spawn.

## Support files
- references/am-brief-flow.md — login-triggered live-data AM brief (Conductor-tracked)
- references/innovator-watch.md — interchangeable follow-set registry (tiers, decay)
- references/engine-naming-ecs.md — scientist naming law and known-good fleet roster
- references/tactical-map-and-layer-coaches-2026-08-27.md — triangle vs Total
  Football layer map (the specialist engine/the specialist engine/the specialist engine lineage), sports-plays
  catalog, layer-bridge law, self-extending analytics law
- references/orchestrator-conduct-laws-2026-08-28.md — operator conduct laws
  from the 08-27/28 principal training session: routing-under-pressure (F-grade
  lesson), self-referral/correction cards, ratification-vs-decision buttons
  law, Glial-team naming, external mirror practice, clock-read law, shutdown
  principle, B2C placental privacy wall