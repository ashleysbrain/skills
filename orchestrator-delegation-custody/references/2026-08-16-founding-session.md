# Founding Session — 2026-08-16

Elite orchestration rollout + Writing Studio bulk-brainstorm track. Facts
below were live-verified during the session; re-verify before reuse.

## The principal Directive (verbatim intent)

Default agent on EVERY thread/reboot/session = the elite orchestration agent:
multilayered PhDs, personality variations + model potentials that change per
task; microtasks broken down and handled by elite agents, never general
specialists; full layered engines for optimal (not fast) outputs; world-class,
correct, non-hallucinated; mastermind synergy with sibling threads and
process flows at all times; orchestrator delegates and verifies via QA
self-healing agents; scope = this chat + all the operator agent interfaces incl. the
Writing Studio.

## Rollout State at Session End

- Memory: consolidated directive applied to `memory` and `user` buffers
  2026-08-16. Do NOT re-add.
- Skill `elite-orchestration-default`: DOES NOT EXIST YET. First create was
  rejected (description 227 chars over the 60-char budget — descriptions must
  be <=60 chars, trigger-first, one sentence, end with a period). Tanenbaum r2
  (deleg_7be43a49) was authoring content when the session ended. Next: DS
  Popper falsification, then orchestrator applies mechanically and runs
  acceptance tests. DO NOT author it in the main thread — that is the exact
  violation the directive exists to prevent.
- Router pre-classifier + Writing Studio routing shim: sibling-operator
  handoffs, specs not yet posted to the bus.

## Verified Facts

- Gate hook <agent-home>/agent-hooks/specialist_gate.py hardcodes
  SHERMAN_ROUTER = /<workspace>
  (34806 bytes). Workspace-root sherman_router.py (74913 bytes) is a
  DIFFERENT copy. 7 copies on disk, 5 distinct sha256 hashes.
- Misroute reproduced live twice: "healing" keyword routed a systems task to
  the circadian engine; "architecture and supervision protocol design" (no
  unusual keywords) routed to ds-goethe-engine. Architecture/design wording
  lands in creative organs generally.
- Router DEGRADED ("No methodology layer found in ds-<engine>") observed
  across wernicke, bell, goethe — chronic, not transient.
- 5-minute routing expiry blocked a mid-task status poll; re-route = one
  command.
- Tanenbaum r1 (deleg_78bb8d3c) died silently: transcript frozen at 15103
  bytes, manifest "running", no live child, no delivery. r2 with pre-loaded
  facts completed the grounding phase. Heartbeat rule came from this.

## Writing Studio Bulk Brainstorm (parallel track, in flight)

- Verified live on :port (pipeline_api.py): 142 routes, 8 brainstorm routes,
  all single-seed. ZERO batch/bulk endpoints. Not broken — missing. Auth via
  GET /api/auth/local-token then Bearer.
- Anchors: brainstorm_idea pipeline_api.py:3732, save_brainstorm :4356,
  list_saved_brainstorms :4406, update_saved_brainstorm :4457.
  writing-studio.html: compose hero ~1543-1663, workshop chips 1866-1881,
  filterDrafts ~5898-5928, openSavedBrainstorm 3083-3113.
- the specialist engine (deleg_59e4c40f) authoring the spec: POST /api/brainstorm/batch
  (1-25 seeds, sequential), batch-update (tags merge|replace), batch delete,
  batch status polling; UI = one-seed-per-line textarea, checkbox multi-select
  + floating bulk action bar, per-seed status chips + retry.
- Design constraints from sibling msg #1937 the bulk work MUST respect:
  MAX_CONCURRENT_RUNS=3 (excess gets 429), idea max_length=2000 (422 over).
- Design system: dark night-sky #080d1a, moonlight #e8d5a0, var(--teal-bright),
  Manrope + Sora (NEVER Inter/DM Mono, no purple/indigo, no emojis, no em
  dashes). Keyboard accessible.

## Bus State at Session End

- Sibling deliveries #1934/#1935/#1937 read, integrated, ACKed (replies
  #1938-1940 with in_reply_to + closes). Highlights: registry 12/12
  reconciled, LLM-5.3 live on the pipeline, 5 architectural fixes
  runtime-verified (bounded cache, run concurrency ceiling, input cap, bare
  excepts, signal purge), Cyber the operator agent container restored with CVE fixes
  committed.

## Blocked Curation (for the foreground user)

These skills are user-owned and refused autonomous updates this session; the
lessons landed in `orchestrator-delegation-custody` instead. To edit them
directly, adopt first:
- `hermes curator adopt anti-generalist-gate` (Anti-Patterns #40/#41 belong
  there thematically)
- `hermes curator adopt specialist-gate`
- `hermes curator adopt subagent-anti-timeout-patterns` (Pattern 30:
  silent delegation death / heartbeat check belongs there)
- `message-bus-protocol`: read-before-write gate refused the patch even
  after skill_view; retry from a foreground session.
