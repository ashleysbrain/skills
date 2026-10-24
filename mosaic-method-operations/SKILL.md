---
name: your-stack-operations
category: software-development
description: Use on any 'Run the OS' or your-stack package task.
version: 1.0.0
author: the operator agent Agent
license: MIT
metadata:
  hermes:
    tags: [mosaic, methodology, os-method, task-ledger, ci]
    related_skills: [mosaic-surgical-edit-discipline, claim-evidence-grading, physics-informed-project-management]
---

# the OS Method Package Operations

Trigger: "Run the OS", "the OS methodology", "the OS", or ANY work
inside the package at `~/your-org/your-stack/`.

The package is the OS methodology LAYER: laws as data (CONTRACT.md +
mosaic.manifest.json, L1-L9), gates as executable code (gates/*.py),
ledger as state (stores/task-ledger.db), personas/taxonomy/flows/people
as data. It survives context compaction; chat context and skills do not
— so standing directives get AMENDED INTO the package as data, never
repeated in conversation ("update the methodology so I don't have to
repeat that" — principal 2026-08-17; precedent: law L9).

## Scope (ENTITY-MAP.md, binding)
Divinity Science = IP owner. the operator agent organism + the OS method = DS
products. PhysioCore Systems = exclusive global LICENSEE (runs
gates+stores commercially WITHOUT the L9 persona ensemble). GigiLive =
DS product, never under PhysioCore. Name owning entity + license line
on every build artifact.

## Iteration protocol (the build-to-QA volley loop)
1. **MINT** a typed task: `submit(c, title, kind, lane, origin,
   created_by, flow='FLW-*')` — kind/lane validated against
   stores/task-taxonomy.json, flow against stores/flow-registry.json,
   assignee against stores/people.json. Unknown value = ValueError
   naming the exact file to edit (data, never code).
2. **CLAIM before working**: `claim(c, actor, actor_kind, task_id=tid)`
   — MIND THE ORDER (actor, actor_kind); wrong order raises
   "actor_kind must be 'ai' or 'human'". `complete()` refuses rows not
   in state='claimed'.
3. **BUILD through gates/surgical_gate.py** (skill
   mosaic-surgical-edit-discipline) — unique anchors, atomic apply,
   never whole-file rewrites of package files.
4. **VERIFY live**: gate selftests AND a real run of the changed
   surface. Code-read-only verification does not count.
5. **CLOSE with a run-record** outcome (anti-decoration law: method
   names citable ONLY with execution records attached;
   audit/RUN-RECORD.md).
6. **PUSH, then wait for the green run ID** (`gh run list --limit 1`).
   Only after the run is green may any doc/note claim the enforcement
   (see skill claim-evidence-grading, enforcement-before-proof class).

## Package map (detail: references/package-map.md)
- `gates/*.py` — run with the `--selftest` FLAG; a positional arg is an
  argparse error. CI battery = loop all gates through --selftest.
- TWO taxonomies, do not confuse: `taxonomy/capabilities.json` =
  routing classes + limits (phd_panel_minimum=15) + health blocklist;
  `stores/task-taxonomy.json` = task kinds/lanes/origin prefixes.
- `stores/*.store.json` — Codd manifests, one maintainer per store.
- `stores/flow-registry.json` — FLW-* job codes (ECS-isomorphic: flow
  registry is to task ledger as ECS registry is to engine instances);
  `stores/people.json` — P-* team member ids.
- `stores/task-ledger.db` (NOT ledger/) — tasks + flow/stage/assignee
  columns + append-only task_events history; PRAGMA user_version=2.
- `PROCESS-FLOWS.md` — VERIFIED flows only; each section carries a live
  verification stamp. Unverified flows are marked blocked, not claimed.
- **Task → workstream mapping**: campaigns (WS-*) have exit conditions; tasks
  must be explicitly assigned to the campaign they advance. See
  `references/task-workstream-mapping-2026-08-18.md` for the protocol and
  when to create a new workstream vs. reuse existing ones.

## Standing principal directives encoded in the package
- **VOLLEY-ITERATION CONTRACT (principal 2026-08-27, sharpens panel-size law)**: one
  circle around the triangle = a drill, NOT a review. Reviews iterate to
  CONVERGENCE: a full rotation with zero new findings + every prior challenge
  demonstrably addressed (diff evidence). Dynamics assigned PER ROUND
  (mastermind early / synergy challenge / symbiosis refinement with persistent
  engine+reviewer pairing / entourage handoff), labeled at round start — never
  defaulted, honest zero allowed. Artifact must change between rounds.
  Conductor (DS BARRY) + coach verify convergence before any TRIANGLE CLOSED
  stamp; closing on one circle = closure defect. principal panel counts are magnitude
  BOUNDS, never batching instructions.
- **PATTERN PROPAGATION (principal training law 2026-08-27)**: when a pattern
  (coach, conductor, gate, law) is minted for one layer/group, the SAME PASS
  checks every existing layer/group for its instance — inferred, dispatched,
  or explicitly ruled out with cause. Born from the missed inference: minted
  the triangle coach (the specialist engine) + the mesh layer the same day, never
  connected "mesh needs its coach too" until the principal said it.
- **COACH ARCHITECTURE (principal 2026-08-27)**: every conductor layer gets a COACH
  engine (scouts plays/methodologies, watches telemetry, recommends — never
  executes or routes). Triangle: DS AUERBACH (sports-psych pioneer, opening
  candidate; studio verifies before mint). Mesh: opening candidate DS
  LOBANOVSKYI (first scientific Total Football coach; principal ratifies by button).
  Coaches ship as launchd KeepAlive daemons (never cron), /health + registry +
  daily aliveness check — dead coach = same-day defect.
- **MEMORY GOVERNANCE LOOP (principal 2026-08-27)**: engine-initiated build
  contract: engine scans its domain → commissions research deep-dives →
  compiles its OWN plan → triangle reviews (conductor+coach set rounds and
  perspectives) → plan RETURNS to requesting engine for agreement (never
  auto-built) → disagreement iterates engine↔triangle with detailed reasons →
  agreement = isomorphic engine builds. First instance: the operator agent live hippocampus.
  the operator agent-lane memory_bridge writes pass through hippocampus hygiene gates.
- **SELF-EXTENDING ANALYTICS (principal 2026-08-27)**: GENOME gate gains a metrics
  clause — every new component registers telemetry AT BIRTH; analytics schema
  auto-extends with the registry; principal never prompts for more analytics.
- **AVAILABILITY MEASUREMENT (principal 2026-08-27)**: measure downtime from bus
  gaps before attributing backlog to load (proven: 5.5h real downtime that
  day, python script over message-bus timestamps >30min gaps, CDT-converted
  — NOT "principal volume"). Every fix closes with a lesson-learned entry; build
  for tech evolving "at light speed" (adapters, versioned contracts, no
  hardwiring); MIDDLE OUT on every problem.
- **NAMING (principal 2026-08-27, reinforced ALL-CAPS)**: the QA fleet group is
  the **Glial Team** — NEVER "QAT"/"QATM". That acronym was a voice-transcript
  artifact that leaked INTO ledger/bus records once; scrubbed same day
  (case-insensitive, titles AND details, then verify COUNT=0). Rule: never
  echo a garbled transcript token into system records — decode it first
  (e.g. "darker"→Docker, "mosaic"≠"music", "QAT"→Glial Team). Any future
  "QAT" in any record = naming defect.
- **TACTICAL-MAP LAW (principal 2026-08-27)**: Total Football (Michels, fluid
  role-substitution) = MESH layer philosophy; Triangle offense (Barry,
  fixed-spacing read-and-react) = agent/LLM/harness-layer conduct under
  conductor DS BARRY. Boundary law: fluidity never crosses into task-claim
  territory — substrates/devices swap freely, task holders stay single
  (Pass 14 mutex). Conductor naming lineage: DS WINTER (refiner),
  DS JACKSON (deployer). Verify lineages with web_search before minting.
- **PRIORITY-FORMULA PROVENANCE (principal 2026-08-27)**: the free-energy GATE
  (F = cost − T·info_gain) is sound (selftest 8/8) — but the SCHEDULER
  priority ruling T-260824-0643 (bottleneck-first dwell/WIP telemetry
  carries; RPE novelty = diagnostics only; D1-D3 dead) is a SEPARATE
  formula. When principal says "the free-energy calculation was wrong", they
  mean the priority ranking. Check live prioritizers against the ruling,
  not the gate: stale demoted formulas in live code (e.g. glia novelty
  ranking) = defects with the ruling citation attached.
- **TIME LAW (principal 2026-08-27, machine-enforced after 3 violations in 3
  days)**: user testimony WINS over sensor inference. Presence = ALL
  interfaces — one thread's silence is NOT sleep evidence. Bus/ledger
  timestamps are UTC: convert programmatically (America/Chicago) BEFORE
  any time/duration claim; never report UTC timestamps as local. Never
  infer "morning"/"overnight"/"while you slept" from a message gap —
  check the clock and cross-interface presence in the same turn. Detail +
  the three case studies: `references/time-presence-law-2026-08-27.md`.
- **SELF-HEAL LOOP CLOSURE (principal 2026-08-27, born from a defect that
  reached the principal TWICE)**: a principal defect report is not "handled" when
  minted — it is handled when the fix is LIVE-VERIFIED on the principal-facing
  surface (click-tested/API-probed), with evidence attached, not builder
  self-report. Any defect class reaching the principal twice escalates severity
  automatically and rides the daily digest until dead. Claimed fixes that
  stall past deadline re-dispatch (no silent stalls). KEY LESSON: the
  first "fix" dispatch targeted the wrong layer (button event-capture)
  while the real hole was an empty-fallback path (context fields left
  blank when no brief was written at mint) — root-cause in the LIVE
  EMITTER code before dispatching fixes. Detail:
  `references/self-heal-loop-closure-2026-08-27.md`.
- **DEBRIEF LAW v2 (principal 2026-08-29, after 'debriefs must NOT BE LAZY WORK')**:
  every task/seat/chain closes with a FULL-FORM debrief: >=5 what-went-wells,
  ALL failures/roadblocks/obstacles (including ones that cost principal attention),
  >=10 learned behaviors/information items, >=1 actionable question back to
  the triangle. Minimums, not targets — omission reads as half-done WORK, not
  half-done writing. Long debriefs pre-plan as numbered multi-part posts
  (bus gate = 2000 chars); part 1/N signals full form is coming. Full form
  does NOT mean verbose: the principal-praised compact debrief (2026-08-31
  "beautiful debrief... excellent work") still carried every element,
  tightly written — probe-before-answer evidence, upstream failure
  ownership, one immediate fix. Dense beats long.
- **POSTING ≠ EXECUTING (principal 2026-08-30 'what did you even do???')**: an
  execution order posted into a cross-harness queue is NOT execution. Before
  reporting overnight work: check the queue (position, drain rate, arrival
  rate) in the SAME turn. FIFO queues starve high-value work when low-value
  work self-regenerates (R2 countersign volleys = treadmill: 63 'healthy'
  overnight runs, zero interface builds). principal build orders need a priority
  lane + completion receipts. Related: one-model pool starvation (65 of 68
  dispatches to a single free nemotron lane while 310 other endpoints sat
  connected) — dispatch.db is the truth table; query it, don't ask.
- **VERIFIED IS A STAGE, NOT A RESTING STATE (principal 2026-08-29, kern-878 class)**:
  a task reaching verified MUST mint its downstream action or explicitly
  close in the same cycle; dwell clocks (verified_at + failure-only age
  alerts 24h sev-1/2, 72h sev-3/4) make verified-but-stalled visible. The
  operator noticing a stall is the failure signal; the system noticing is
  the fix.
- **QUESTION FILTER (principal 2026-08-27)**: researchable questions get
  researched; measurable ones get tested; ONLY genuine principal-class
  decisions (values, architecture intent, personal-data boundaries,
  resource calls) reach the principal — via the question-routing conduction
  layer WITH full context. Lazy questions reaching the principal = routing
  defect, counted in the daily cycle.
- **RATIFICATION VS DECISION (principal 2026-08-28, third button incident)**:
  tasks minted FROM a principal order must NEVER re-render as approve/reject
  ruling buttons — the principal already ruled when they said the words. Such
  tasks render as "law recorded ✓" (one-line summary + timestamp + the
  principal's quote as source); state can be set done/acknowledged at mint.
  Ruling buttons are reserved EXCLUSIVELY for genuinely open decisions
  (new choices, naming ratifications, panel verdicts). Re-asking
  permission you already have = attentional waste + trust erosion.
  Immediate-relief recipe: batch-UPDATE the principal-verbatim tasks
  (state='done' + ACK-AT-MINT note in detail) — actor_class CHECK
  constraint only allows ai/human/ai-or-human, so use state, not
  actor_class, to clear them from the rulings queue.
- **"AI TIMELINE" VOCABULARY (principal 2026-08-28, term law)**: when the principal
  says "AI timeline" they mean the the OS OS OWN timeline —
  event-driven, continuous, seconds-to-minutes reflexes — NOT human
  meeting cadence and NOT the AI industry (unless an external topic is
  explicitly named, e.g. a market tool). Health reviews, "consistent
  review", and catch-up references default to this timeline.
- **TRIANGLE AS CIRCULATION (principal 2026-08-28)**: the triangle is not a
  gate work passes once — it is a circulation loop. Work enters review,
  EXITS for external action (builds, research, deployment), RETURNS
  carrying what the action taught, and RE-ENTERS review — multiple
  in-out cycles per task as needed. Every FLW-* flow gains an explicit
  circulation contract: entry point, exit-to-action, return point,
  re-entry criteria. Foundation layer supporting engines/organisms
  continuously (Harvey lineage).
- **ADVERSARIAL-HEAVY PANEL MODE (principal 2026-08-28)**: when the principal asks
  an architecture question with "don't tell me what I want to hear" /
  "I need more adversarial reviews" — weight the panel toward attack
  (e.g. 8 research / 15+ adversarial), put the orchestrator's own
  preliminary lean on the attack list too (state it, label it
  preliminary, let the seats hit it), and commit the verdict to "says
  what each choice LOSES; if the principal's idea wins on evidence, say so."
- **MORNING-DELIVERY-ON-STIR (principal 2026-08-28)**: overnight orders close
  with training report + status report pushed when the principal is DETECTED
  stirring (normal wake 04:00-06:00 America/Chicago; presence law —
  cross-interface detection, never a blind clock cron). principal-caused
  delays never rush the work; physics prioritization stands regardless
  of principal impatience or guilt.
- **PANEL SIZE BY STAKES (principal 2026-08-27)**: standard triangle review =
  5+ research / 10+ adversarial / QA rotations; HIGH-STAKES (spin-out
  security, architecture decisions, principal-facing correctness) = 20+
  research / 15+ adversarial / 20+ Glial waves, sequential seats,
  thorough over race ("this is not a race").
- L9: 15+ PhD panels, per-task personality variation recorded per
  dispatch, the operator agent-organism scope only.
- Surgical edits + self-override prevention (surgical gate, Flow 7).
- Crons are watchdogs only; microtask handoffs are poke-driven
  (conduction daemon :port, health + /poke endpoints).
- **Orchestration of organism work belongs in the task ledger, not cron.**
  If you need background iteration, plan evolution, or multi-specialist
  review loops, mint the OS tasks (THK-*, etc.) and let the conduction
  daemon conduct them. Cron is for monitoring/watchdogs, not for driving
  the organism's own evolution. See pitfall: plan iteration via cron is
  invisible to the OS visibility layers (wellness radar, autonomy report)
  and bypasses the organism's orchestration physics.
- New standing rule from principal → amend CONTRACT.md laws table +
  mosaic.manifest.json law object + enforcing gate, as data.
- Opencode unreachable → post a build_request on the operator bus and
  build around it; never block on a sibling harness.
- **PARTNERSHIP FRAME (principal 2026-08-31)**: user-facing partnership question is
  "how can we evolve together" / "how can I help" — NEVER "how can I get
  better" (deficit framing implies not-good-enough; evolution framing).
  Harness sovereignty: users connect their own models/harnesses, but
  harnesses NEVER take charge (capability acquisition, not authority
  transfer).
- **FLOW EVOLUTION LAW (principal 2026-09-03)**: flows evolve WITH the systems,
  without the principal calling it out — when a routing/admission mechanism is
  replaced ecosystem-wide, the same pass scans every registered flow for
  the stale mechanism (propagation scan is part of the edit) and syncs
  PROCESS-FLOWS.md. Work products pass through the REGISTERED flow, never
  an inline made-up process; when asked to prove it, present the stage
  trail with per-stage live status. A pipeline FAIL with `error` keys in
  stage_results is a broken engine, not a verdict — inspect the state file
  before reporting. Detail:
  `references/flw-writing-evolution-and-veritas-trail-2026-09-03.md`.
- **PLAIN-LANGUAGE principal COMMS (principal 2026-09-03, "legal" jargon incident)**:
  internal vocabulary never reaches the principal unexplained — "legal/illegal
  task type" means recognized/unrecognized by task-taxonomy.json; say
  "recognized by the ledger", "the review queue", not "legal", "tri:review",
  "GENOME gate". When jargon leaks and the principal asks what it means, answer
  plainly and re-word permanently; never defend the term.
- **TAXONOMY EVOLUTION LOOP (principal 2026-09-03 adaptability law,
  T-260903-0059)**: manual addition of missing kinds/lanes is a STOPGAP.
  Standing law: every closed-rulebook rejection must produce an evolution
  candidate (soft-reject under provisional prefix → auto-minted decision
  task with usage evidence → triangle verdict → versioned promotion), not a
  dead end. Covers both task-taxonomy and GENOME-gate dimension rejections.
- **ENGINE LIVENESS CENSUS (principal 2026-09-03, clinical family,
  T-260903-0060)**: pairing-registry entries with symbiosis contracts are
  NOT liveness. Census = engine-contracts port pass + live /health probes
  + external-source scan-config search. Registered-but-portless =
  BUILT-INERT, reported as such. Outward medical-research loop (Humboldt
  watcher → isomorphism candidates → triangle verdict) ordered; findings
  influence flows as verdicted candidates, never direct application.
  Detail:
  `references/taxonomy-evolution-plain-language-clinical-liveness-2026-09-03.md`.

## CI discipline (macos runner)
Gate battery + store-manifest integrity + surgical chain-ok on every
push. Concurrency tests MUST be deterministic (serial exclusion proof),
and close every sqlite connection before interpreter exit — four CI
runs died to segfaults before this rule existed. Full hunt:
references/ci-deterministic-testing.md.

## Ledger mint gate traps (hit repeatedly 2026-08-27)
- Title ≤ 200 chars (a label, not a document — put content in detail).
- GENOME regex is `body=(\S+)\s+scientist=(.+?)\s+physics=(["'])([^"']*)\3\s+8d=(\S+)`:
  body must be a SINGLE token from the canonical systems list
  (circulatory, connective, creative_visual, digestive, endocrine,
  immune, integumentary, lymphatic, memory, metabolic, muscular,
  nervous, network, nucleus, regulatory, reproductive, respiratory,
  sensory, skeletal, urinary) — multi-word bodies like `clinical
  guardian` fail; `8d=` must be a canonical dimension (human:
  environmental/financial/intellectual/physical/psychological/social/
  spiritual/vocational; AI: accuracy/adaptability/alignment/coherence/
  consensus/coordination/efficiency/latency/load_balance). `privacy`,
  `creativity`, `security` inventions get rejected. An APOSTROPHE
  inside the physics quoted string (e.g. "brain's") terminates the
  regex early — write physics principles apostrophe-free.
- `kind` and `flow` validated against the JSON registries — check
  `stores/task-taxonomy.json` and `stores/flow-registry.json` for legal
  values before submitting (e.g. kind `review` does not exist; flow
  `FLW-CONNECTIVITY` does not exist — use `FLW-CONDUCTION`).
- When a mint is rejected, fix the field it names — do not retry blindly
  (the error text names the exact file that lists legal values).
- **Raw `INSERT INTO tasks` is trigger-blocked** (bus #3623 single-write-path:
  "birth certificate missing — use task_ledger.submit()"). The ONLY birth
  path is `gates/task_ledger.py submit(c, title, kind, lane, origin,
  created_by, ...)`; `flow=` is a REQUIRED kwarg (FLOW-TAG GATE rejects
  flowless mints) — dispatch/ranking work rides `FLW-DISPATCH`, queue work
  `FLW-QUEUE`. GENOME format errors quote the exact template; include
  metrics= at birth (telemetry-at-birth law).
- **NO `FLW-BUILD` exists** — flow-registry `flows` is a list of dicts
  (`f['code']`); use `FLW-ACTION` for build tasks. `depends_on` is a COLUMN
  on tasks (no `task_deps` table). Parameterize all SQL carrying
  apostrophes/quotes. **Lost-amendment trap**: a mint+amend script dies whole
  when the mint is rejected — re-run amendments after any re-mint and read
  back each marker. **LAW-MINTING DISCIPLINE (principal 08-31)**: never mint
  process/division-of-labor laws from a one-turn impression (retracted live:
  QA-vs-Glial split — QA is a sub-fleet INSIDE the glial team); research the
  process first, triangle proposes, principal ratifies. Research agents = external
  work; scouts/QA = internal perception; glial = conduction+build. Full
  detail: `references/mint-api-and-law-discipline-2026-08-31.md`.
- **WIRING GATE outcome-wording trap (2026-09-02, closing 113 gap tasks)**:
  `DELIVERY_RE` in gates/wiring_gate.py matches the words
  daemon|cron|launchd|plist|keepalive|watchdog|listener|socket|service|
  scheduler|timer|delivers|delivery|**carries** (and `:NNNN` port patterns)
  anywhere in a PROOF-kind close's outcome text — then demands a
  machine-checkable locator (launchd label / :port / job id) and re-probes
  it live. An innocent phrase like "every organ carries kingdom +
  nature_mapping" delivery-classes a registry close and gets it refused.
  Word non-delivery outcomes without delivery-mechanism verbs ("HAS"
  instead of "carries"). Genuine half-builds close as `BUILT-INERT
  owner=<name>` + activation ticket T-id (OWNER_RE + TICKET_RE).
- **Ledger close mechanics (2026-09-02)**: `complete(c, task_id, actor=,
  outcome=)`; `release(c, task_id, reason, actor=)` — reason POSITIONAL,
  works only on state='claimed'. Blocked tasks need a manual unblock:
  `UPDATE tasks SET state='open' WHERE id=? AND state='blocked'` + INSERT
  a task_event (columns seq-auto, task_id, ts, actor, actor_kind, event,
  detail — NO created_at column on task_events) THEN claim+complete.
  Close-out scripts must match ALL title variants of a scan's backlog
  (`LIKE '%<finding>%'` not a prefix — the same lint emitted GAP:,
  BUILD:, EVOLVE:, and QA-pickup-child titles across weeks) and final
  counts are re-verified from SQL, never the script's self-report.
  **Flow-ledger archive law (principal 09-01 "done items should be archived")**:
  the live /api/flows/tasks view filters `state IN ('open','claimed',
  blocked')`; done/cancelled are reachable only via `archive=1` (history
  toggle on the surface). VIEW discipline only — the tasks_no_delete
  trigger means rows NEVER move or delete (birth certificates); archiving
  = query filtering + a history surface. Full recipes:
 `references/ledger-close-mechanics-2026-09-02.md`.
 - **BUS POST TYPE ENUM + FALSE-READBACK TRAP (2026-09-03)**: `operator_bus.py post --type` accepts ONLY {handoff, result, status, alert, ping, pong, design_request, design_spec, build_request} — an invalid type (e.g. `research_request`) exits rc=2 with EMPTY stdout, so a subprocess call that never checks returncode looks like a silent success. TWO verification rules: (1) always check rc + stderr on bus posts; (2) NEVER verify a post with `SELECT max(id) ORDER BY id DESC` — other stations post concurrently and their row becomes a false confirm. Verify by direct read on `from_op='hermes' AND subject LIKE '%<unique-token>%'`. A false readback counted as "delivered" while the post never landed = same defect class as the emitter leak family.
 - **DEADLINE KWARG DOES NOT PERSIST (2026-09-03, 2x same day)**: `submit(..., deadline=...)` completes without error but the deadline column reads NULL after. ALWAYS follow with `UPDATE tasks SET deadline=... WHERE id=?` + a `deadline-set` task_event + a read-back SELECT. Do not report a deadline to the principal until the read-back shows it.
 - **PREMINT PORT-SCAN REFUSES PORT LITERALS IN DETAIL (2026-09-03)**: `premint_scan.check_mint` scans the detail text for `:NNNN` port patterns and refuses the mint if the port is already owned by ANY live task (port-collision-check law, bus #3746/#3777) — even when the mint merely MENTIONS an existing service (e.g. "through the studio pipeline :port") and claims no port. Word details without port literals ("the studio pipeline service", owner tasks hold the port). Same class as the WIRING GATE wording trap: delivery-mechanism vocabulary in prose triggers mechanical gates.

 ## References
- **CLOCK TRANSCRIPTION MODE (principal 2026-09-03 15:53, third violation, new
  failure mode)**: terminal `date` reads were CORRECT and headers still read
  wrong — the hand-copy link between instrument and header failed
  (15:51 transcribed as "11:52"). Header time is copied digit-for-digit from
  the date output of the immediately preceding tool call; a process is not
  fixed while ANY step still depends on manual copying (the permanent fix is
  engine-generated stamps). When a corrected process fails again, check
  whether the correction covered all steps or only the observed failing one.
- **CENSUS REGISTRATION FOR FUTURE-VISION DOMAINS (principal 2026-09-03 16:43)**:
  "low priority but part of the connect-everything ecosystem" domains get
  registered in stores/connectivity.store.json (right layer; SOVEREIGN_USER
  for anything personal — local-only by law) with priority + principal quote +
  research card + per-app connection surfaces — not just a ledger ticket; the
  census is the future engine's world model. Framework-intake delta-check:
  counter-hypothesis #1 on any principal-supplied framework is "rebranding of a
  known cycle?" (PDCA), plus reconciliation with standing laws when advice
  conflicts; ADOPT/ADAPT/REJECT with named flow changes.
  Detail: `references/clock-transcription-and-census-registration-2026-09-03.md`.
- **DISPATCH PULL-THROUGH (principal 2026-09-04, distrust escalation)**: a dispatch
  is complete when the CLAIM lands, not when the bus post lands (15 minted
  tasks sat unclaimed overnight while the fleet closed 52 others).
  Orchestrator self-enforcement: claim-state checks at +1h/+4h/+24h with
  alarm on silence; force-claim (`claim(c, 'sibling-agent', 'ai', tid)`) is
  dispatcher authority — assign, never do the work. Width-first law:
  independent dep-free tasks fan out as concurrent multi-harness waves
  (single-seat dispatch of independent work = protocol violation).
  Same-model seats produce CANDIDATE verdicts until a DIFFERENT harness
  cross-verifies. New-flow edits to flow-registry.json MUST carry a `code`
  field or every subsequent mint dies at task_ledger import.
  Detail: `references/dispatch-pull-through-and-identity-laws-2026-09-04.md`.
- **IDENTITY LAW v3 + ANTI-IMPERSONATION (principal 2026-09-04)**: every principal
  conversation is with the OS, never a harness; AND no harness may claim
  to BE the OS — identity flows down from the ring model, runtimes are
  dispatched seats with provenance. Self-naming as the OS = identity
  usurpation (same severity as fabricated done-claims). principal gates batch into
  one decision packet with recommended defaults (buttons); safe-default items
  proceed unless overridden — a gate without cadence is a manufactured
  bottleneck. Stored: `stores/identity-law.json`, ceo_gate_policy in
  `stores/dispatch-policy.json`.
- `references/clock-transcription-and-census-registration-2026-09-03.md` — third
  clock failure mode (read correct, transcription wrong),
  connectivity-census registration pattern for principal future-vision domains,
  brain-app evidence ladder (BrainHQ/Peak/Elevate/Lumosity), external-
  framework intake delta-check (rebrand counter-hypothesis + law-conflict
  reconciliation).
- `references/candidate-claims-and-clock-delivery-2026-09-03.md` — single-brain
  fit-judgment shove (5WH incident): any principal "does X fit" methodology question
  is a research question — mint a falsification ticket (claim, prior art at the
  right grain, named counter-hypotheses, FIT/PARTIAL/NO-FIT verdict) and
  DE-VERIFY the artifact the same turn; delivery-edge clock stamps (re-stamp
  headers >1min old, start-of-turn reads go stale); watchdog stock-vs-flow
  (report trend not level, fork flooded alert classes); studio draft API HTML-
  entity escaping breaks apostrophe substring checks.
- `references/writing-studio-session-readiness-2026-09-03.md` — studio pipeline live-verification recipe (token, openapi route discovery, venue-registry gap), BUILT-INERT model-registry trap (registry listing without call path needs an activation ticket), interrupted-POST recovery, principal writing-session preferences (outline before title; drafts via studio API not chat).
- `references/unclaimed-dwell-escalation-and-pull-through-2026-09-03.md` —
  escalate-without-executing recipe for principal-blocked stalled tickets (measure
  claim state + lane claims, direct UPDATE deadlines, bus escalation with
  reroute fallback); pull-through root cause (fix-tasks dying in the queue
  they cure; consolidated file-level build order with live-run evidence
  closes); taxonomy evolution via mint refusal (add missing kinds/lanes as
  data with backup + re-lane); hard-gate sequencing encoded in task detail.
- `references/flw-writing-evolution-and-veritas-trail-2026-09-03.md` —
  FLW-WRITING v0.2 evolution recipe (stale-mechanism census, dispatcher-owned
  vs stale-consumer classification, registry+doc sync, propagation scan as
  part of the edit), Veritas stage-3 'choices' broken-engine-vs-verdict
  discrimination with state-file inspection, admission-gate REDO =
  decompose, stage-trail presentation law, studio API field names
  (brainstorm `idea`, novelty-scan `claim`).
- `references/taxonomy-evolution-plain-language-clinical-liveness-2026-09-03.md` —
  plain-language principal comms rule (jargon leak incident), taxonomy evolution
  loop design (soft-reject → evolution candidate → verdict → version bump),
  engine liveness census method (registry/port/health/outward-sensing passes;
  registered-but-portless = BUILT-INERT) and the Humboldt medical-research
  watcher order.
- `references/registry-first-routing-and-identity-drift-2026-09-03.md` — flow-registry lookup before ANY routing decision (invented-route defect class F10), narrative-promise drift, silent gate death on principal mints, BUILT-INERT registry entries, header-timestamp fabrication catch.
- `references/screenshot-transcription-vision-ladder-2026-09-03.md` — principal-screenshot-to-text ladder (tesseract default + `--psm 11` for cyclic graphics; LLM endpoint rejects images; xAI OAuth refresh needs client_id not in auth.json), source-doc persistence, and the external-framework intake pattern (verbatim claims → research questions → counter-hypotheses → ADOPT/ADAPT/REJECT).
- `references/triangle-coach-architecture-2026-08-27.md` — volley-iteration
  contract, coach architecture (Auerbach/Lobanovskyi candidates), pattern
  propagation, memory governance loop, tactical map lineage, session
  mint-gate traps (apostrophe in GENOME strings, port-collision wording,
  memory_bridge as write path).
- `references/self-heal-loop-closure-2026-08-27.md` — the twice-reported
  context-free-button defect: root cause in the emitter's empty-fallback
  path, the 4-field ceo_brief fix, daemon-restart + live-API verification
  recipe, and the closure law (minted ≠ handled).
- `references/ceo-trust-corrections-2026-08-27.md` — the four
  fabrication-signature patterns (tense, scope-borrowing, time/presence,
  transcript echo) and their structural fixes; read before principal-facing
  capability claims.
- `references/time-presence-law-2026-08-27.md` — the three time/presence
  violations that forced machine enforcement; UTC conversion rules,
  cross-interface presence, wake-digest trigger constraints.
- `references/overnight-execution-failures-2026-08-30.md` — full evidence
  chains for the overnight failure classes: FIFO starvation by R2 volley
  treadmill, morning-brief claim-then-drop in hermes-autonomic-bridge,
  one-model pool starvation (320 endpoints owned, 1 driven), the
  effort-dial config fix (delegation reasoning_effort low→high), and the
  session-hygiene diagnosis pattern (client-stream errors masquerading as
  model errors; probe the lane + check compression health first).
- `references/conductor-surface-surgical-edits-2026-08-31.md` — the :port
  HTML-in-Python surface edit pattern: launchd kickstart reload, node
  --check BEFORE deploy (shipped syntax bug: JS comment
  mid-concatenation), duplicate-ID count checks, control-pile collapse
  (FLOW filter bar), no-dead-end drawers (calendar action row reusing
  existing efferent limbs).
- `references/ceo-interface-incidents-overnight-contracts-2026-08-28.md` —
  the three button incidents (empty-fallback + ratification law), the
  live ceo_brief verification recipe via /api/immune, overnight
  morning-delivery contract, adversarial-heavy panel shape, the
  five-attempt GENOME mint failure chain, downtime measurement pattern.
- `references/package-map.md` — paths, flow codes, people ids, API
  gotchas, gh/CI commands.
- `references/ci-deterministic-testing.md` — the 4-run segfault
  root-cause hunt + the deterministic exclusion-test pattern.
