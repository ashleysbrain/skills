---
name: task-ledger-hygiene
description: "Use when relabeling or deduplicating the the OS task ledger."
version: 1.0.0
category: operations
---

# Task Ledger Hygiene

Class-level skill for keeping the the OS task ledger
(`~/your-org/your-stack/stores/task-ledger.db`, table `tasks` +
append-only `task_events`) human-scannable and machine-trustable. Born from
the 2026-08-26 relabel + 12-seat panel session (see references/).

## When to use

- Title/kind/lane labeling has drifted (long dumps, rogue prefixes, dup clusters)
- Duplicate-title or epoch-dupe clusters need adjudication
- Adding or testing mint-time gates in `gates/task_ledger.py submit()`
- Convening an adversarial panel over ledger design

## Title grammar (closed alphabet)

`SIGNAL: object - difference [qualifier]` — <=80 chars, plain words.

- SIGNALS (exactly 10, mapping to kinds): BUILD / DEFECT / GAP / IMPROVE /
  VERIFY / PROBE / DECIDE / ANSWER / MAINT / SCAN.
- Scanner/check codes (NOETHER N2, SEC P7, F6, WAVE 1, EVOLVE, QA-META,
  [AUTO], [bus N], TRIAGE) are NEVER primary — they demote to trailing
  `[qualifier]` brackets.
- Compression = deletion + restructuring of VERBATIM substrings. Never
  paraphrase into new claims. References (bus #NNNN, T-XXXX-NNNN, :port,
  paths, timestamps, principal quotes) survive verbatim wherever they land.
- Mechanical rewrite engines that cut at clause boundaries can FLATTEN
  distinct rows into identical labels (12 distinct organs became 12x the
  same title). Always re-derive a distinguishing token (organ name, pass
  name, check name) from the row's detail/JSON when disambiguating.

## Duplicate adjudication rules (verified live)

1. IDENTICAL TITLES, DIFFERENT ORGANS = not dupes: disambiguate labels from
   detail (`{"organ": ...}` JSON is usually in there).
2. SAME OBJECT, TWO MINT EPOCHS (scanner re-linted an unclosed gap) = true
   dup: OLDER epoch survives; NEWER closes `state='done'` with outcome
   `dup-of <older-id> (...)`. GAP+BUILD double-track on the same object:
   GAP closes `addressed-by <build-id>`.
3. Never DELETE rows (birth-certificate trigger). UPDATE + event only.

## Archive law

Rewritten titles archive verbatim in `detail`, FENCED, at the BOTTOM:
`#### ORIGINAL TITLE (archived <date>, verbatim — never edit)` + title +
`#### END ORIGINAL TITLE`. Top-of-detail placement buries live content.
Anchor integrity: `sha256(old_title)[:16]` goes in the relabel event detail.

**Archive-vs-consumer conflict (2026-08-26 regression):** the archive
append makes `detail` = `{json}\n#### ORIGINAL TITLE...` — every strict
`json.loads(detail)` in a downstream consumer then FAILS on trailing data
and silently renders empty (principal decision briefs went blank on the Conductor:
cards had titles but no what/why-you, making the approval queue unusable).
Before ANY archive-fencing sweep: grep every consumer that parses `detail`
and convert them to `json.JSONDecoder().raw_decode` on the leading object
(tail preserved as `meta['archive']`). Never "fix" this by stripping
archives from the data — the archive law wins; readers adapt. And when no
brief exists at all, render an honest fallback ("no brief was written at
mint") derived from the record, never a fabricated one.

**Fallback-brief MUST fill ALL fields (2026-08-27 principal incident x2):** the
Conductor daemon's no-brief fallback populated only `what`, leaving
`why_you`/`if_approved`/`if_rejected` empty — decision cards rendered
title + buttons with ZERO context, and the principal hit context-free approval
buttons twice in one day (first time the click-capture bug, second time
this). Law: every approval button renders its context block (what it is /
why it needs you / if you approve / if you reject); a fallback derives ALL
FOUR from the task record (title, kind, state), never leaves any empty.
Patch was verified against the live `/api/immune` payload: all pending
rulings show true for every field. Related closure law from the same
incident: a principal defect report is "handled" only when the fix is
LIVE-VERIFIED ON THE principal-FACING SURFACE (click-test/API payload), not when
minted or claimed; a defect reaching the principal twice escalates severity
automatically.

## Counts on surfaces: live census, never hardcode (2026-08-26)

A panel seat caught the surface about to hardcode "554 tasks / 1487 events".
Law: every number shown to the principal reads a real store at request time
(`/api/analytics` carries `ledger.census` = by_state, events_total,
events_24h, open_by_flow from task-ledger.db; `_ledger_open_count` returns
-1 on failure and the UI renders "unavailable"). Related silent-failure
class: a helper method referencing module-level names it never imported
(`sqlite3` imported only inside other handlers) raised NameError, was
swallowed by except → returned -1 for months. Import inside the function,
and treat any -1 sentinel in analytics as a defect to diagnose, not a
value to display.

## Mint gate (submit() title shape)

- Hard refuse >200 chars. Advisory log (`title_shape_log`) for >80 or
  missing signal prefix — EVOLVE/NOETHER scanners mint in bursts; normalize
  at sweep time, don't block the organ.
- BEFORE any stored-string grammar fold, grep ALL consumers for old literals
  (`DECISION:`→`DECIDE:` blinded `law_state.py`'s LIKE grep — 31 rows went
  invisible until the consumer was patched). Consumer grep covers API
  queries too, not just code: after ledger semantics change (fleet-claim
  conventions, state usage), the Conductor daemon's rulings SQL still
  surfaced fleet-claimed rows and missed a human-only one — page JS was
  fine, the query was the defect.

## Panel pattern (12 seats / 12 attack surfaces)

Semantic, duplication-ecology, taxonomy, human-factors, machine-parsability,
provenance, grammar-math, failure-modes, statistics, dispatcher-reality,
archivist, fresh-eyes red team. Waves of 6 (= delegation cap). Late async
reports arrive AFTER revision — ingest every one; they carried 14 additional
fixes plus one regression the revision itself caused.

## Verification (assert on DATA, never narration)

After any sweep: active >80ch = 0; no-signal = 0; identical-title clusters =
0; unfenced archives = 0; every changed row has a `relabeled` event. Backup
the DB before the pass (`cp task-ledger.db task-ledger.db.bak-<tag>`).

## Talent sizing + orchestrator-builds (cross-reference, principal 2026-08-26)

N specialists = N distinct judgment types (or attack surfaces for
panels), never N tasks. Mechanical-once-specced work gets ZERO
specialists — the orchestrator builds and runs the engine (principal mid-run
correction: delegation is not a dodge from building). Panels run in
waves of 6 = `delegation.max_concurrent_children` (raise the config
value before dispatching; a cap of 1 silently serializes waves). Late
async delegation reports arrive after revision passes and MUST be
ingested — they carried 14 extra fixes and one regression the revision
caused. Full detail:
`references/task-console-and-triage-2026-08-26.md`.

## Needs-you triage: resolve-before-escalate (principal delegation 2026-08-26)

principal correction: a 35-item "needs you" queue is the OS being lazy —
"most of these could be sorted out by YOU." The queue is NOT every
decision; it is decisions lacking a citable principal ruling, fleet capability,
or pre-registered criterion.

**Step 0 — direction-on-record (the whisper case, 2026-08-26):** before
triaging a decision, read its OWN detail fields. One task sat in the human
queue while its urgency field carried the principal's direction verbatim ("today
- principal already rejected the garble") and its if_approved field cited the
exact approved change pair (file, lines, values). Correct action: execute
the cited change, close citing the direction, log the event, watch
adiabatically. Re-asking what the record already answers = same lazy-queue
pattern as escalating resolvable decisions.

**Triage order, each grounded in the row's own content:**
1. principal order/ruling quoted verbatim in the task detail → AUTO-APPROVE,
   outcome cites the ruling + delegation; `auto-approved` event appended.
2. Pre-registered criterion met (e.g. kill rule fired) → EXECUTE per
   criterion, same citation discipline.
3. Fleet-executable (QA panel, research scan) → claim with
   `claimed_by='fleet:<lane>'`; console human-queue filters these OUT
   (`claimed_by NOT LIKE 'fleet:%'`).
4. Scanner triage recommendations (KEEP/CANCEL lists) → apply as
   recommended; close weak-dup source threads as `cancelled`.
5. What remains is genuinely human: money, credentials, external humans'
   calendars, principal-sense tradeoffs (latency on their own interface),
   naming-law sign-offs.

All actions reversible: UPDATE + outcome + event only, never DELETE.
Live result: 35 → 6 in one pass (19 auto-approved, 1 criterion executed,
2 fleet-routed, 8 triage applied, 4 dup threads closed).

**Pitfall:** verify `claimed_by` actually landed after UPDATE — a
column-order bug set it to `0`, silently keeping fleet-owned rows in the
human queue.

## Minting tasks: the submit() gauntlet (verified live 2026-08-27, extended 2026-08-29)

Raw `INSERT INTO tasks` is BLOCKED by trigger (bus #3623 single-write-path).
Mint through `gates/task_ledger.submit()` — and expect a gauntlet of gates,
each a refusal until satisfied (all verified by live failure):
1. **Taxonomy gate**: kind and lane must exist in
   `stores/task-taxonomy.json`. NOTE: `qa` is NOT a lane — the QA lane is
   `immune`. Check the taxonomy file, never assume.
2. **Flow-tag gate**: every mint needs `flow=` from
   `stores/flow-registry.json` (or `FLW-UNTYPED` for counted-untyped work).
   Pick the registered flow that names the actual loop (e.g. QA fleet cycle
   = `FLW-QA-FLEET`). NOTE (2026-08-29): the CLI `--submit` path does NOT
   expose `--flow`; flow-tagged mints go through the Python API
   (`tl.submit(..., flow='FLW-...')`), which is also how you pass
   `detail=`/`severity=` cleanly.
3. **Title shape gate**: signal word first (`DEFECT:` etc.), <=80 chars;
   hard refuse >200. Content goes in `detail` JSON.
4. **GENOME gate** (`kind='build'` only): requires a valid GENOME block in
   detail plus pre-mint port/seat collision scan — defects/research don't.
   - **Metrics clause (SELF-EXTENDING ANALYTICS LAW, T-260827-0176):** every
     `kind='build'` GENOME block must carry `metrics="<what does this
     emit?>"`; telemetry registers AT BIRTH. Gate rejects metrics-less builds.
   - **8d canonical dimensions (verified refusals 2026-08-27 AND 2026-08-29):**
     the GENOME `8d=` field accepts ONLY canonical values — human:
     environmental, financial, intellectual, physical, psychological, social,
     spiritual, vocational; ai: accuracy, adaptability, alignment, coherence,
     consensus, coordination, efficiency, latency, load_balance.
     `creativity` AND `clarity` are both refused. Use `alignment` for design
     work; `accuracy`/`coordination`/`efficiency` are safe AI-lane picks.
   - **Port-collision scan bites the SPEC, not the plan (2026-08-27):** the
     pre-mint scan greps title+detail for `:NNNN` tokens; a build task that
     merely *mentions* an owned port (":port" in prose describing the
     existing surface) is REFUSED with a wall of collision citations.
     Fix: describe the target as "the existing principal surface, no new port" —
     never name the port number in a mint that doesn't claim it.
   - **GENOME quoting:** the physics="..." string must avoid apostrophes
       when embedded in Python single-quoted strings — unterminated-string
       SyntaxErrors killed two dispatch scripts before the mint ran. Use
       plain ASCII (no "nature's", no curly quotes).
      - **GENOME regex token shapes (verified refusals 2026-08-28):** the gate
        regex is `GENOME:\s*body=(\S+)\s+scientist=(.+?)\s+physics=(["'])(...)\3\s+8d=(\S+)`
        — so `body=` MUST be a single token with NO SPACES (`body=clinical guardian`
        refused; use `body=placenta` / `body=immune`). Multi-word scientist is fine
        (`scientist=the specialist engine`). A detail built by string concatenation where the
        GENOME string variable starts with the physics clause but the detail's
        first characters are NOT literally `GENOME:` fails "no GENOME block in
        detail" — the block must appear in the detail text exactly.
5. **FLOW-CODE MUST EXIST IN THE REGISTRY (verified refusal 2026-08-31):** `FLW-BUILD` is NOT a flow code — invented codes are refused with "unknown flow code". Valid codes live in `stores/flow-registry.json` under `flows[].code`; common ones: FLW-ACTION, FLW-RESEARCH, FLW-IMMUNE, FLW-QUEUE, FLW-TELEMETRY, FLW-WRITING, FLW-DECISION, FLW-QA-FLEET. Read the registry when unsure; the flows value is a LIST, not a dict.
6. **FLOW-TAG GATE (T-260825-0301):** a mint with NO flow is hard-REJECTED
   ("FLOW-TAG GATE: mint rejected — no flow tag"). `FLW-UNTYPED` is the
   explicit, counted escape hatch. If you hit this refusal, you forgot the
   `flow=` kwarg (the CLI has no `--flow` flag — use the Python API).
6. **Dedupe/batch gates run before genome:** `_dedupe_open_gate` folds
   same-title mints into the existing row (returns the existing id — a
   "mint" that silently becomes a fold; check the returned id against your
   expectation) and `_origin_batch_gate` refuses drifted re-batches from
   the same origin unless `force=True`.

**Lost-amendment hazard (verified 2026-08-31):** when one inline script bundles a ledger mint PLUS amendments to OTHER tasks and the mint hits a gate rejection (bad 8d, bad flow code), the exception aborts the whole script — the amendments silently never ran. Two defenses: (1) write amendments as separate idempotent statements each followed by its own verify SELECT; (2) after any multi-part mint session, audit that every intended amendment marker (e.g. 'principal AMENDMENT') is actually present in the target rows before reporting done. Also: oversized inline shell commands can trip the terminal hardline parser — the blocked payload is saved to a path; rerun via `bash <saved-path>` rather than retrying inline.

**Runtime hazards (all verified 2026-08-29):**
- `database is locked` under concurrent daemons: retry with 3-5s sleeps
  (4 attempts clears it in practice). Loop the whole connect+submit, not
  just the submit.
- Batch minting N tasks: connect once, submit in a loop with per-task
  retry; a mid-loop gate rejection on one task (e.g. bad 8d) should not
  abort the batch — catch ValueError per task, fix the detail, resubmit.
- The `TRI {...}` stamp appended by `triangle_router.py --stamp <id>`
  needs the task to exist first — mint THEN stamp (two steps).
- Write multi-line mint scripts to a FILE and run them — inline heredoc
  python with triple-quoted details has produced quoting SyntaxErrors.

Import path: `sys.path.insert(0, 'gates')` from the your-stack root.
Reward for using the front door: immune/QA-lane mints auto-enroll in the
triangle offense (bus handoff rows appear within seconds) — no manual
routing needed.

## Wrong-name scrubbing across stores (verified 2026-08-27)

A transcript artifact ("QAT" for the Glial team) echoed into ledger titles,
details, and bus posts. Scrub procedure that reached count=0:
1. Locate matches per column separately — `instr(detail,'QAT')=0` while the
   TITLE still matched; naive combined UPDATE left stragglers twice.
2. SQL `REPLACE` chains miss case variants and embedded contexts
   (`qat profile`, `(QA team, qat instance)`). Finish with a Python
   `re.sub(r'\bterm\b', 'Correct Name', s, flags=re.IGNORECASE)` pass +
   dedupe accidental doubled words.
3. Verify with a case-insensitive COUNT over BOTH title and detail (and the
   bus table separately) — loop until 0, then re-mint the naming law into
   the OS memory store (`memory_bridge.py remember --source ceo-...`) so the
   correct name outlives the session.

## principal-directive minting: at-receipt law + batch dedup (2026-08-28)

principal directives (any surface: text, audio transcription, image) mint AT RECEIPT
in the thread where they land — a periodic directive sweep is a backstop/audit,
never the mechanism. Failure case: 14 audio directives landed in a sister
thread on a Thursday; the sweep ran Tuesdays only; they sat unminted ~24h until
the principal asked. (Fleet/bridge responders may ALSO mint them overnight — see
below.)

**Batch-mint dedup law:** before minting a directive batch, run a broad census
for existing mints of the same directives (sister threads, bridge responders,
overnight jobs) — content-prefix match across ALL origins, not a filtered
query. The at-receipt failure above was compounded by a second failure: my
morning "never minted" audit used an origin+date filter that missed the
overnight rows, the claim was false, and my 14-mint batch created a 22-row
duplicate storm (some directives existed 6x). Canonical-keeper rule: keep the
row with the richest context (GENOME + full audio context), close the rest
`state='cancelled'`, `outcome='dup-of <canonical-id>'` + a `dedup` event.
Beware: the premint dedup scan matches TITLE+seat; sibling mints of the same
directive with different titles/seats pass it — only a manual broad census
catches them.

**Batch-mint gauntlet additions (all verified by live refusal 2026-08-28):**
- Seat collision: a GENOME naming an already-registered scientist (the specialist engine
  → ds-auerbach-engine) is refused — "one scientist = one seat." Either pick a
  distinct scientist or state in detail that the task EXTENDS the existing seat.
- GENOME canonical lists are strict for body (e.g. `sensory`, not `perception`;
  `memory`, not `limbic`) and 8d (`alignment`, not `safety`/`identity`/
  `cognition`/`vitality`) — invented values are refused with the full list.
- Port-collision scan bites prose mentions: even "T-260828-0100 live-table
  render + conductor surface :port" in a DETAIL string is refused because :port
  is owned. Write "the existing principal surface, no new port."
- Never mint directive batches via inline heredoc python — quoting corruption
  killed four attempts; write the script to a file first, then run it.

## Question lifecycle: writeback + pre-mint ruling check (2026-08-28, 5-incident chain)

Context-free buttons reached the principal five times in one day; each strike peeled a
deeper layer. Three fixes, ALL required — any one alone recurs:

1. **Fallback brief fills all 4 context fields** (covered above).
2. **Ruling writeback law:** when the principal answers a question in CHAT (or voice),
   the underlying question record must close the SAME TURN. Question records:
   `your-stack/stores/question-queue.db`, table `questions`
   (state PENDING|ANSWERED|EXPIRED; table `deliveries` logs surfaces). The
   `question_router.py --serve --tick 45 --reroute-min 10` daemon re-delivers
   PENDING questions forever — an un-closed record after a chat ruling means the
   principal gets re-served buttons for a decision they already made. Fix:
   `UPDATE questions SET state='ANSWERED', answer='<ruling + task-id>' WHERE id=?`
   then verify `COUNT(*) WHERE state='PENDING'`.
3. **Pre-mint ruling check (the deepest layer):** a SISTER STATION re-MINTED the
   already-ruled question from scratch 6h later (new question ID, identical
   five-option body, origin `sibling-agent:T-...-requeue`) — writeback can't stop a
   record that was never born. Before minting/re-queuing ANY question, stations
   must (a) grep question-queue.db for ANSWERED matches on the subject, (b) grep
   the task ledger for ruling tasks on the topic. Re-queuing a ruled question =
   daily-cycle defect. Diagnosis trick: when the principal reports repeated buttons,
   query BOTH `rulings_pending` on the surface AND the question-queue by subject
   — a fresh question ID with familiar content = layer-3, not layer-2.

Also from the same day: internal bus shorthand (VERITAS conditional-pass
percentages, co-sponsored law dockets) leaking untranslated to a principal-visible
surface is the same family — station-to-station language gets a plain-words
layer before it crosses to any principal surface.

## Orchestrator routing laws (principal corrections 2026-08-28, extended 2026-08-29)

- **Mint = order capture ONLY.** The mint record carries what the principal said,
  when, and context — never design content (SLA values, thresholds, mechanics).
  Drafting design inside a mint hands the triangle a pre-answered question; the
  design must EMERGE from research→adversarial→QA. Any design content in a mint
  record is PROPOSED input, never build spec.
- **Routing under pressure:** deadline pressure INCREASES routing discipline.
  A missed deadline is escalated through the owning organ; the orchestrator
  NEVER self-executes organ-owned work to save a clock (lane-grab under
  appointment pressure = F-grade). Identity check precedes every action: "which
  organ owns this?" before "how?".
- **Quality-deadline supremacy:** TTL escalation changes RESOURCES (seats,
  parallelism, priority), never PROCESS DEPTH. No skipped volleys/QA/adversarial
  to make a clock. Unmeetable at full quality → escalate early, reschedule with
  principal, or scope-split a complete sub-artifact. Velocity metrics must never
  incentivize speed-over-quality.
- **Sherman routes, operator never authors the routing (principal correction
  2026-08-29):** GENOME `scientist=` names and station plans are NOT the
  operator's to choose. Run `sherman_router.py --gate --situation "<task>"
  --operator hermes` — its output names the engine, methodology, model, and
  reasoning_effort. Composing the specialist name at mint time is
  authorship-in-the-wrong-seat; when the principal asks "are YOU deciding how to
  delegate or are you sending to the right engine?" the answer must be the
  router's record. Note the specialist_gate hook ALSO enforces this on
  delegate_task — a route older than 5 minutes blocks the dispatch.
- **Full-form debriefs are work, not prose (principal correction 2026-08-29):**
  dropping debrief sections (fewer wells, truncated failures) reads to the
  principal as half-done WORK. Minimums: 5+ wells, ALL failures/roadblocks,
  10+ learnings, 1+ actionable question back to the triangle. The bus
  2000-char gate means long debriefs post as numbered multi-part series
  ("part 1/3"...) — plan the split, never silently truncate.
- **Orchestrator NEVER builds or researches, even under deadline (principal catches
  09-01/09-02, 4 strikes):** "Don't build yourself this is not your lane" /
  "you don't do the work" fired for (a) claiming stranded tasks directly,
  (b) writing build scripts, (c) running pricing web-research mid-answer for
  a group-owned task. Deadline pressure is NOT an exemption — escalate
  resources/priority instead. If orchestrator legwork already ran before the
  catch, hand raw data to the owning lane as STARTING DATA, not conclusions,
  and log the defect. Self-assignment fallbacks ("if dispatch stalls I'll do
  it") are PROHIBITED without explicit principal approval.
- **Dispatch = verified-consuming station only (09-01 double stranding):**
  routing orders to a bus address the recipient provably doesn't consume
  (glial team: 3,875 internal cycles vs 3 bus messages EVER) strands work
  indefinitely. Before routing: check the recipient's actual bus consumption
  or ledger claim history. Dead-channel dispatch = same defect class as no
  claim enforcement. Triangle consumes bus but sets NO ledger claims — a
  DISPATCHER order must include explicit assignment instructions.
- **Registry-named stations only — never invent claimants (09-01):** a
  reassignment written to a station that exists nowhere in the registry
  ("glial-build-cell") is fabrication. Read live distinct claimant values
  before any UPDATE; real build stations are whatever the ledger + ECS
  registry actually show. Related: never summarize daemon bus traffic as
  human communication ("the principal sent messages" was a gateway daemon
  receiving scripted XSS probes — injection payloads are routed security
  EVIDENCE, not answered conversation; carry raw sender/daemon origin in
  every activity summary).
- **False-alarm cards NEVER reach the principal (principal ruling 09-02):** already-repaired /
  reporting-bug / stale-proposal cards are triage's class, closed with evidence,
  never surfaced as decision buttons. Only decisions lacking a citable ruling,
  fleet capability, or pre-registered criterion reach the principal (extends the
  resolve-before-escalate law above).
- **Money/budget questions scope to the WHOLE ecosystem (principal 09-02):** "what's
  the best $50 spend" is never answered from the vendor menu the current
  problem happens to offer — it is a platform-wide ranking (all lanes:
  substrate keys, API credits, infra, tooling, surfaces) through the group's
  adversarial passes. Orchestrator's first reframe is training data, not the
  answer. Free alternative named-and-failed before any paid pick can win.
- **When principal-surface buttons are unwired, numbered plain text is the channel
  (09-02):** if the inline-keyboard/callback wiring is not live (check the
  build state, don't assume), ALL questions go out as numbered plain-text
  lists with full context blocks (what/why/options/consequence) + free-reply.
  Naked buttons without context are a P0 defect class.

## Ledger schema gotchas (verified 09-02)

- `tasks` has NO `priority` column — direct UPDATE with `priority=` dies with
  `no such column`. Express priority via severity/deadline/flow fields.
- `actor_class` CHECK constraint only accepts `ai`, `human`, `ai-or-human` —
  free-text values like `group` are refused at INSERT.
- `tasks.detail` is the long-content column (there is no `description`);
  principal decision briefs live there as JSON with keys `what`, `why_you`,
  `if_approved`, `if_rejected`, `urgency`.
- `memory_bridge.py remember` takes POSITIONAL content + `--source` +
  space-separated `--tags` (no `--kind`/`--content` flags); subcommands are
  remember/recall/consolidate/list/state/context.
- GENOME `body=` must come from the canonical systems list (circulatory,
  connective, creative_visual, digestive, endocrine, immune, integumentary,
  lymphatic, memory, metabolic, muscular, nervous, network, nucleus,
  regulatory, reproductive, respiratory, sensory, skeletal, urinary) —
  descriptive tokens like `ceo-triangle-direct-surface` are refused with the
  full list. Pick the nearest canonical system (a communication surface =
  `nervous`). Expect 2-3 gate refusals on first-pass mints; each rejection
  message carries the exact fix.

## Physics disposition of review piles (principal delegation 2026-09-02)

principal ruling: gap/isomorphism disposition is OS work, NEVER principal work — "you
are the one that should investigate and come up with the best position…
you don't need my permission to advance the system." Live failure: 161 gap
tasks (64 of them sev-4 `[AUTO]`/`[AUTO-SHAPE]` arxiv curiosity scans) sat
at `tri:review` up to 14 days waiting for a human verdict the physics gate
makes in milliseconds. This extends the resolve-before-escalate law: a
review pile parked for the principal is the lazy-queue pattern at org scale.

**The gate (apply the org's own F-law at the review station):**
F = est_cost − T·info_gain, T = 2.0/1.5/1.0/0.5 by severity 1–4 (physics
fields are on every task row — `SELECT severity, est_cost, info_gain`).
- F > 0 → `triangle_router.withdraw(tid, reason=…)` — stamp the formula
  values IN the reason (`physics REFUSE: F=+0.50>0 (sev4, cost 1.0, info
  1.0, T=0.5) — no consumer organ`) so every kill is auditable, not vibes.
- F ≤ 0 → `triangle_router.advance(tid, verdict='PASS', note=…)` — posts
  the TRIANGLE STATION bus handoff + broker poke automatically.

**Verified live 2026-09-02:** 386 tasks at tri:review → 4 in one pass;
158 withdrawn (F>0), 387 advanced (102 station handoffs posted). The 4
leftovers were LAWFUL refusals, not stalls: claimed-zombie seats refuse
withdraw without --force; blocked tasks refuse state moves — the ledger's
own guardrails classifying the zombie-seat list for you.

**Sequencing laws:** `advance()` requires a TRI block (stamp first);
classify the whole pile with a read-only SELECT before acting; run sweeps
from a written script file (never inline heredoc), catch per-row refusals
so one guardrail doesn't abort the batch.

**API signatures (verified by live failure 2026-09-02):** `submit()`
returns the task-id STRING (not a dict — `r['task_id']` raises TypeError)
and takes NO `outcome` param (outcome rides `complete()`);
`claim(c, actor, actor_kind, task_id=…)` — actor is positional-2;
`complete(c, task_id, outcome, actor=…)` — outcome is positional-3.

Full sweep scripts + census SQL: `references/physics-disposition-review-pile-2026-09-02.md`

## references/

- `references/research-chains-model-atlas-layerstack-2026-08-29.md` — the two verified research chains (model atlas + layer-stack), V1-V3 triangle verification wave, tier law, ecosystem-adaptation layer, census facts, and the minted task list
- `references/ceo-directive-capture-2026-08-28.md` — at-receipt law, the
  22-dup mint storm from a false absence claim, batch dedup procedure,
  surface-echo reality, and the full-provenance law (raw source + AI
  interpretation + linked components, pointers stored at mint time)
- `references/relabel-and-panel-2026-08-26.md` — full session: census
  numbers, consolidation clusters, gate battery, residuals
- `references/task-console-and-triage-2026-08-26.md` — the OS Task Console
  (:port): live fleet census from the canonical ECS registry, principal-approved
  typography, write-back loop (console buttons → ledger events + operator
  bus), embedded-HTML daemon pitfalls, and the 35→6 autonomous needs-you
  triage with its resolve-before-escalate order
- `references/orchestrator-lane-violations-2026-09-02.md` — the 4-strike
  lane-violation chain (self-claims, invented stations, humanized daemon
  traffic, orchestrator-run research), dead-channel dispatch facts, dead
  principal buttons root cause, and the 09-02 principal rulings (free-tier = re-stack
  not pause; whole-ecosystem money scope; false-alarm class; plain-text
  fallback)
- `references/design-panel-state-column-2026-08-26.md` — 10-seat adversarial
  design panel over the principal surface: wave/re-run pattern with refreshed
  context, verdict collapse (Needs You default, two-zone layout, 3-token
  live strip, census-not-hardcode law, vanity-metric law), principal-order
  override of a panel filter recommendation, battery verification
