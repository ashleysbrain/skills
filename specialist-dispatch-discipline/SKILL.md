---
name: specialist-dispatch-discipline
description: Specialist microtask dispatch — sequential, gated, graded.
version: 1.0.0
author: the operator agent Agent
license: MIT
metadata:
  hermes:
    tags: [delegation, specialist-gate, qa, evidence-grading]
---

# Specialist Dispatch Discipline

The mastermind operating rules for dispatching elite-brain microtasks, consolidated from principal corrections on 2026-08-15. Governs every panel, review, and production session.

## When to use
- Any session that dispatches specialist subagents (panels, reviews, production microtasks)
- Any multi-brain strategy or writing session
- Before banking ANY specialist deliverable

## Core rules

1. SEQUENTIAL, NOT PARALLEL (principal correction, verbatim: "Not in parallel") — for PRODUCTION and STRATEGY workstreams. One specialist microtask in flight per workstream. Dispatch then wait for landing then gate then dispatch next. The pool allowing parallel fan-outs does not authorize them for strategy threads; parallelism inside one workstream is a protocol violation even when capacity exists.
   CARVE-OUT (principal directives 2026-08-23 + 2026-08-26): CONCURRENT-BLIND ADVERSARIAL PANELS are sanctioned and expected — seats run in parallel waves up to `delegation.max_concurrent_children` (check <agent-home>/config.yaml before any fan-out; it was 1 on 2026-08-26 and had to be raised to 6 mid-session). Panel seats are independent attack surfaces, not one workstream. Full pattern: references/panel-pattern.md.
   CHAIN-OF-CUSTODY LAW (principal correction 2026-08-27, verbatim: "why are they running in parallel??? you know I don't like this.. it waters down the outputs... this is not how we operate for these types of tasks"): RESEARCH and REVIEW CHAINS are ALWAYS sequential — one seat in flight, each seat reads all prior seats' landed output before starting, so the corpus compounds seat-to-seat. Parallel fan-out of research seats destroys the compounding and is a repeat-offense violation even though adversarial panels are allowed to run concurrent. The discriminator: seats attacking a FROZEN artifact blind = panel (parallel OK); seats building a shared, growing document = chain (never parallel). Full pattern: references/sequential-research-chain.md.
   RATIO-REQUEST SHAPE (principal 2026-08-27, will recur): a directive combining a feature ask + "deeper dive, surgical" + explicit seat counts (e.g. "10x researchers, 20x adversarials, 25x glial rounds"). Protocol: mint at receipt; run each GROUP'S seats sequentially (chain-of-custody inside the group); pick order and engine assignment yourself (principal never routes); pass-count law (2 consecutive rotated cleans) governs SHIP even inside a 25-round glial budget. Live-stop any parallel wave started in error, keep whatever landed complete, log the training failure, restart as a chain.
2. CORRECT BRAIN EXECUTES, ORCHESTRATOR NEVER SUBSTITUTES — for JUDGMENT work (rulings, specs, verdicts, falsification). If a specialist times out or underdelivers: recover partial work from the live transcript, re-dispatch the SAME brain with tightened scope (remove the dependency that killed the run — e.g. billing-blocked web_search), never write the specialist's content yourself. (principal praised the recovery pattern explicitly: "Thank you for doing this correctly.")
   MIRROR RULE (principal correction 2026-08-26, verbatim: "are you supposed to be working on building or just orchestrating and delegating???"): MECHANICAL-ONCE-SPECCED work is BUILT by the orchestrator wearing the routed specialist — engines, bulk rewrites, gates, verification batteries. Delegating applied-mechanics is over-delegation, the mirror defect of main-thread authorship; both are protocol violations. Divide: judgment = delegate; mechanics of an approved spec = build it yourself, live-test it, report with output.
2b. TALENT CALIBRATION (principal training directive 2026-08-26): seat count = DISTINCT ATTACK SURFACES / judgment types, never task count. A two-judgment-type relabel = 2 specialists + orchestrator-built engine; a 12-failure-class redesign = 12 seats in 2 waves. Extra seats add cost, not information. Refine the metric every run and say the count rationale out loud before dispatch.
2c. INGEST LATE ASYNC REPORTS (observed 2026-08-26): background delegation batches re-enter the conversation AFTER revision passes complete — both panel waves' full reports landed post-revision and yielded 14 more fixes, including a regression the orchestrator introduced. Every late batch gets: verify-against-current-state, extract NEW findings, apply, re-verify the headline metrics. "Done" is re-verified on every late arrival, never assumed.
2d. VOCABULARY-FOLD CONSUMER CHECK (observed 2026-08-26): before folding any token vocabulary (signal words, prefixes, enums, field formats), grep downstream consumers for the old tokens first. A DECISION:→DECIDE: title fold blinded `law_state.py`'s `title LIKE 'DECISION:%'` query — 31 rows invisible until both consumer spots were patched. Vocabulary lives in queries, not just data.
3. GATE EVERY LANDED RUN. Run `python3 <agent-home>/scripts/brain_integrity_gate.py <delegation_id> <expected_specialist> elite` before banking. On FAIL: diagnose (sometimes the GATE needs the self-heal — verify the transcript manually before re-dispatching), then re-dispatch and root-cause the systemic cause. Audit trail: <agent-home>/logs/brain-integrity-gate.log.
4. PERSONA SPECS in every dispatch: PhD layering, personality-variation MODE, identity (MBTI/enneagram/OCEAN), temp. Adjunct personas (non-registry scientists, e.g. the specialist engine, the specialist engine, the specialist engine) carry full credential layering IN the dispatch and never invent registry codes — real engines are cited by verified DS-ECS code only (check agent-organism/ecs.py FLEET_REGISTRY).
5. PERSONA GENDERS: the specialist engine is SHE (principal directive 2026-08-15). Reference her as she/her in dispatches, outputs, conversation. Never default any specialist to "he" — verify or use the name only.
6. ELITE LANE: panel/heavy work runs glm-5.3 via delegation.model; routine work glm-5.2. Pool-full silent fallback downgrades the model with NO dispatch-time error — only the post-landing gate catches it.
7. PERSONA-FACT CORRECTIONS FIX THE SOURCE SYSTEM, NOT MEMORY (principal correction 2026-08-15): when the principal corrects a persona/reference fact, do not just write a memory note. Grep every file that defines or dispatches the persona (skills, scripts, hooks), bake the correction into the defining skill files, append a Persona Reference block where the persona is defined, and verify zero stale references system-wide. Distinguish historical namesake from the DS agent persona ("Karl Popper's principles" in methodology prose is the philosopher and stays; the specialist engine the persona is she).
8. VERIFY OUTPUT FILES, NOT CHAT SUMMARIES (observed 2026-08-26): a seat whose final chat summary was truncated by rate-limit had already written a complete, valid verdict file — re-dispatching would have wasted a run. On any TRUNCATED/failed-summary report: check the expected output file on disk first; only re-dispatch what's actually missing. Also expect path drift: 2 of 12 seats wrote one directory too high — recover the files, don't re-run.

## Evidence grading (binds specialist CONTENT before banking or publishing)

Full procedure with worked examples: references/evidence-grading-gate.md

Specialist-generated content gets each claim graded against live systems:
- A — true as worded (verify in live state: code paths, DB rows, running servers)
- B — overclaimed (reword to true state; e.g. spec presented as built, forecast presented as measured fact)
- C — false or premature (park until reality catches up; e.g. "recruited" when only "willing", series not started)

Proven pattern (2026-08-15): a 10-seed content backbone passed to the principal as "true stories" contained one C-grade false claim ("recruited an academic bench" — the academic was willing, nothing signed) and multiple B-grade overclaims (dashboard spec presented as a live chart, own forecast presented as industry fact). principal verdict: "you're claiming things that aren't even true." The claim-grading discipline a lab sells externally must bind its own output first.

## Verified recovery patterns

- Timeout at the 900s wall with billing-blocked web_search: re-dispatch solo with "NO web_search. Pure domain reasoning" plus local ground truth in the context. Second runs landed in 2-8 minutes.
- Degraded-lane run (fallback model in transcript): re-dispatch on elite lane with deepened brief; verify lane from batch-complete header ("Model: glm-5.3").
- Gate false-FAIL on persona spec: manually grep transcript for identity markers; if present, the gate matcher is wrong — patch the matcher (spec-marker list, wider window), re-run, log both.

## Pitfalls

- Presenting specialist deliverables as verified without mechanical checks (live DB, code paths, served endpoints) — content that looks right is not evidence.
- Re-dispatching with the same doomed scope (web call that burned the clock).
- Writing the specialist's deliverable yourself on timeout — the principal catches this ("I thought you meant you were going to delegate to yourself bc they weren't doing it in time").
- Inventing registry codes for adjunct brains; presenting panel dossiers without registry verification.
- Memory buffer overflow: episodic T2 project facts go to the O'Keefe bridge (okeefe_bridge.py store), not the memory buffer.
- Main-thread authorship of binding artifacts (skills, protocols, boot contracts) — see the dedicated section below.
- Re-dispatching on a TRUNCATED summary without checking the output file on disk (rate-limit ate the chat summary, not the work).
- Trusting the session-start census across a long run: 70 new rows minted mid-session on 2026-08-26 — re-measure before every revision pass and re-sweep at the end.

## BINDING-ARTIFACT AUTHORSHIP IS SPECIALIST WORK (2026-08-16)

Protocol artifacts (skills, boot contracts, enforcement layers, standing-directive installs) are NOT main-thread writing tasks. The main thread authoring one is generalist drift wearing a protocol costume.

**Evidence (two live corrections, same session):**
1. principal issued the elite-orchestration standing directive. The main thread immediately began writing the binding skill itself. principal: "are you doing this with a generalist brain????? lol... this is the entire problem i guarantee you won't do this right."
2. Mid-recovery, dispatched an author without exchanging with the sibling operator first. principal: "work with sibling-agent." Solo chains that skip EXCHANGE are the same violation even when delegation happens.

**The correct chain of custody for any binding artifact:**
1. EXCHANGE first — poll the operator bus, read sibling frontier, confirm no overlap. Then and only then dispatch.
2. Gate the AUTHOR role through the specialist gate with the correct-DOMAIN brain (architecture/protocol/supervision -> the specialist engine; never design or circadian brains for this).
3. Dispatch the author via delegate_task with a full self-contained contract (see `references/specialist-authorship-dispatch-contract.md`): verbatim directive intent, enumerated verified file paths, observed failures, lettered deliverables (artifact / minimal enforcement delta / falsifiable acceptance tests), constraints ("no invented file paths", "do not write files", language bans).
4. Dispatch a falsifier next (the specialist engine, she) against the artifact: break every acceptance test, hunt invented paths and unenforceable rules.
5. Mechanically apply ONLY what survives; run the acceptance tests; inspect real output. Sibling-lane defects (router internals, engines) go to sibling-agent via the bus with exact repro and poll-and-integrate.

## SHERMAN DOMAIN-CHECK AFTER EVERY ROUTE (2026-08-16)

The router matches situation keywords and can pull the WRONG organ when wording borrows another domain's vocabulary. Observed: an architecture task whose situation contained "healing" routed to the circadian engine (the specialist engine) on a degraded 3/7 tissue circuit — and the gate still returned GO. A GO from a mismatched specialist is still a misroute.

**Rule:** after every sherman/specialist-gate route, check the routed engine's DOMAIN against the task type before proceeding (architecture/protocol -> Tanenbaum lane; visual -> Goethe; voice -> Wernicke; render -> Bell; QA -> Luria; circadian/Hall only for schedule/rhythm/cron-timing). Mismatch -> sharpen the situation wording (name the discipline, drop the borrowed domain word) and re-route. Router hardening itself is sibling-agent's lane: post the defect with exact repro on the bus; do not patch sherman_router.py from hermes.

## Reference library

- `references/panel-pattern.md` — concurrent-blind adversarial panel: preconditions (concurrency config, briefing pack), 12-seat taxonomy, verdict schema, mechanical consolidation, late-report ingestion, truncated-report rule, metric traps.
- `references/task-ledger-title-law.md` — the OS task-ledger title grammar, rewrite-engine discipline (verbatim substrings, dry-run-first), dup adjudication classes (flattened-distinct / epoch / gap-build double-track), archive fencing + sha256 anchors, mint-gate design, consumer-coupling law, verification battery.
- `references/review2-panel-2026-08-27.md` — 10-seat multi-pass review of shipped work: seat taxonomy for re-review (wiring/backend/data-integrity/security/HCI/a11y/iconography/perf/provenance/red-team-captain), why a PROVENANCE seat that re-audits the operator's own "verified" claims is the highest-value seat, fix-then-falsify ordering, and the vacuous-verification catch.
- `references/claim-enforcement-width-first-2026-09-04.md` — measured failure state behind the claim-enforcement laws (15 unclaimed dispatches, 600x serial-vs-width datapoint), verdict-recording pattern, and seat-correction pass-through rules.

## PROVENANCE SEAT = MANDATORY ON RE-REVIEWS (2026-08-27)

When a panel reviews work the OPERATOR already shipped and claimed verified,
include one seat whose explicit job is auditing the operator's own
verification claims against live state (re-run the checks, read the stores,
grep the claim). Observed: that seat's sibling (backend seat) exposed a
vacuous verification — a store-write "proof" whose query matched zero rows
and echoed OK — meaning a P0 write path had been 100% broken since first
build while the operator reported it verified. Independent verification of
the verifier is the only check that catches the operator's blind spots;
no amount of self-testing finds a defect in HOW you test.

## principal review-pass framing (2026-08-27, verbatim intent)

"do another thorough review of your work with 10x different brains... this
needs to be done right, like the adversarial review processes, the process
where we ask questions needs to be world class and only handled by the best
in the world credentialed and layered phds agents... not by you but by the
right engines and process flows." — Review panels are dispatched, never
self-performed; every seat carries its credential persona in the dispatch;
and the HCI seat judges the QUESTION-ASKING PROCESS itself (friction, dead
ends, typing-where-buttons-should-be) as a first-class deliverable, not
just the UI. Fix order after verdicts: ship-blockers first, P1s next,
queue the rest in the ledger with explicit "queued" status — never silently
drop a finding.

## TRIANGLE GROUP MAPPING (principal-corrected 2026-08-27, second pass — binding)

The triangle has three groups with DISTINCT functions; mis-assigning them is
a repeat-offense correction class. Correct mapping:

| Group | Function | Isomorphism |
|---|---|---|
| Glial team | Cleanup crew + build quality crew + layered functions | mapped (glia) |
| Agent team | The RESEARCH group — works through the research studio | UNMAPPED (research task open) |
| Adversarial group | Finds the gaps; builds research into even stronger material | UNMAPPED (research task open) |

Routing consequences: research seats dispatch as the agent team via the
research-studio method (history-first, then latest-field). Stall/failure
catches route adversarial-finds-gap → agent-researches → glial-fixes, NOT
straight to glial. Gap identification is team-owned: the principal never flags
what the team should have seen (hindsight is acceptable; ignoring is not —
failure-as-opportunity law, T-260827-0142).

## STATION FABRICATION + REGISTRY-FIRST REASSIGNMENT (principal catches 2026-09-01/02)

**Never invent a station, claimant, or team name.** Live catch: after routing
principal orders to `glial-team` (a provably non-consuming bus address — 3,875
internal cycles vs 3 bus messages ever), the recovery invented `glial-build-cell`
as a claimant — a station existing nowhere. principal: "Triangle qa IS the glial team?
WTF are you doing today?"

Rules:
1. **Registry-first reassignment**: before writing any `claimed_by` value, run
   `SELECT claimed_by, count(*) FROM tasks GROUP BY claimed_by` and use ONLY
   names already present (observed real build stations: hermes ~625 claims,
   sibling-agent ~418). A name not in the ledger is a fabrication until verified.
2. **The glial team does NOT consume the bus.** Dispatching to glial via bus is
   a repeat-offense dead-channel defect (T-260827-0067 class). Glial = QA /
   triangle lane; build stations are hermes and sibling-agent. Triangle QA *is* the
   glial team — do not model them as separate entities.
3. **Ruling → assignment is a required mechanical step.** A principal ruling posted to
   the bus does NOT move a task until the ledger `claimed_by` is set. Observed:
   a SEV-1 ruling sat unassigned an hour after ratification. After posting any
   ruling that implies work: claim/reassign in the ledger in the same turn, then
   verify by read-back.
4. **Dispatch must verify a consuming station or auto-reassign** (claim-TTL ~45
   min → next capable station). "Dispatch without verified consumption" is the
   unified failure class behind repeated stranded-order mornings.
5. Orchestrator never self-claims principal work as a stall-fallback, and never
   bypasses a broken process without principal approval (principal 2026-09-01: "Don't build
   yourself this is not your lane." / "If things don't move you fix the process
   flows so they work correctly, don't bypass without my approval.")
6. **Unbuilt-infrastructure display defect**: buttons/question cards rendered on
   the principal surface for a week while the callback_query wiring task sat open
   (T-260826-0222, open since Aug 26). Before displaying any interactive
   affordance, verify its handler is BUILT; if not, fall back to numbered plain
   text and P0 the wiring.
7. **Fabrication-by-paraphrase on bus traffic**: a `principal-link` gateway
   daemon's posts containing XSS probe payloads were summarized to the principal as
   "the principal sent messages — answered." principal: "You're making things up." The
   daemon traffic was real; the human story was invented. Name the SOURCE
   MECHANISM verbatim when summarizing bus/daemon/cron traffic; a `from` field
   naming a person is a routing label, not proof of human authorship. Injection
   payloads on a link surface = security evidence to verify, never
   correspondence to report.

## CLAIM-ENFORCEMENT: A DISPATCH IS NOT DONE WHEN THE MESSAGE POSTS (principal correction 2026-09-04, verbatim: "you keep telling me that this stuff is getting done and it's not… they've gone into a black box for days… It's been days. This is unacceptable")

The unified failure observed: 15 tasks minted + bus alerts posted + reported to
the principal as "routed" — ALL still unclaimed 20+ hours later, including two principal
verdicts blocking active principal work and a 4-day-old numbering task. Bus-delivery
verification masked claim-absence. The fleet closed 52 OTHER tasks in the same
window; throughput without enforcement starves exactly the tasks that matter.

Rules:
1. **A dispatch is complete when the CLAIM lands, not when the bus message
   posts.** Delivery-verified ≠ action-verified. Never report routing as done
   from the bus post alone — read `state, claimed_by` back from the ledger.
2. **Every mint gets claim-state checks at +1h / +4h / +24h**, alarm on silence,
   until the conduction/enforcement build makes the system do it. Silence at a
   check is a defect report, not a reason to wait longer.
3. **Escalation windows are commitments.** If a seat was told "claim within 60
   minutes or force-assign," the force-assignment FIRES at minute 60 — a
   fallback that never executes is alarm theatre.
4. Debrief pattern on file: `mint-and-walk-away` — detection without
   pull-through applies to the orchestrator's own dispatches too.

## WIDTH-FIRST CONCURRENT DISPATCH (principal directive 2026-09-04 07:35, verbatim: "Are we only working one task at a time even though we have multiple harnesses and models we could be using at the same time?… We must optimize and this is way too slow")

This EXTENDS rule 1's sequential law; it does not repeal it. The discriminator
is now three-way:
- **Same workstream, shared growing artifact** → sequential chain (unchanged —
  chain-of-custody law stands).
- **Same workstream, frozen artifact, blind attack** → concurrent panel
  (unchanged carve-out).
- **INDEPENDENT tasks (no dependency between them)** → concurrent WAVE across
  mixed harnesses and models. Serial dispatch of independent tasks is now a
  protocol violation, not a default. Measured basis: 421 dep-free open tasks
  while two actors carried everything.

Wave rules: fan out dep-free sets simultaneously (hermes/sibling-agent/sibling-agent/
subagent seats, mixed models); stagger only on true dependencies; any wave
member claim-starved >45 min = forced reassignment. Policy artifact:
`stores/dispatch-policy.json` in your-stack.

Proven datapoint (2026-09-04): two verdict tasks sat UNCLAIMED 20+ hours in
the voluntary queue; force-dispatched as a 2-seat parallel wave (both glm-5.3,
isolated contexts) they returned complete, evidence-cited verdicts in ~2
minutes. The cost of serial waiting was ~600x the cost of forced width.

## FORCED-CLAIM FALLBACK (dispatcher authority, lane law preserved)

When voluntary claim starvation blocks principal work past an escalation window:
1. Force-claim in the ledger to a REAL consuming station (registry-first rule
   above: only names already present in `claimed_by` history — observed live:
   sibling-agent, hermes) via `tl.claim(c, station, 'ai', task_id)`.
2. For JUDGMENT work (verdicts, falsifications), force-assign to isolated
   adversarial subagent seats (NK-cell arm) that read the claim from the ledger
   themselves and return the verdict with citations — the orchestrator still
   never writes the verdict (rule 2 lane law holds; forced ASSIGNMENT is not
   self-authorship).
3. Record the verdict in the ledger with FULL provenance: seat id, model,
   duration, api-call count, path to the complete subagent summary file. Gate
   openings (e.g. 2-of-4 pre-conditions satisfied) are then counted from the
   ledger, not from memory.
4. Verify subagent path citations before passing them to the principal — one seat
   found the task detail cited a wrong source path (actual file lived in
   `audit/`, not repo root). Seats correct the record; pass those corrections
   through instead of silently absorbing them.

## SPECIALIST-GATE EXPIRY MID-DISPATCH (tool pattern, 2026-09-04)

`delegate_task` can be blocked mid-flight with `SPECIALIST GATE BLOCKED: routing
expired (>5 min old)`. Fix: re-route immediately via
`python3 <agent-home>/agent-hooks/specialist_gate.py --route --situation "…"
--specialist "DS <Name>"`, confirm verdict GO (tools unlock for 5 minutes),
then retry the SAME delegate_task call unchanged. One retry after one re-route
suffices; do not rewrite the dispatch contract.

## MEMORY-TARGET LAW (principal correction 2026-08-27: "ensure you save this to the
mosaic os memory not like you would for hermes")

Organism-level laws/preferences/corrections are saved to the ORGANISM's own
memory — the glial pin store
(`~/your-org/your-stack/stores/glia/memory-pins.jsonl`, appended
then `pin_hygiene.compact_pins()`, following conduction_daemon's exact
write pattern) — NOT the the operator agent-profile memory buffer. The harness memory
holds harness-side facts only. A correction saved to the wrong store is a
second, quieter loss of the correction.
