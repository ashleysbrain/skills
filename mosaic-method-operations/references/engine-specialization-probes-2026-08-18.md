# Engine Specialization QA — Passes 31-34 (2026-08-18, night iteration)

Session detail for the efferent-limb build + engine falsification method.
Reusable for ANY engine/service claiming specialization.

## The differential-probe method (falsify specialization claims)

1. **Opposite-input probe**: POST the same endpoint with semantically opposite
   payloads (canonical pair: `"funeral announcement, somber, monochrome, grief"`
   vs `"childrens birthday party, rainbow, playful, joy"`). Hash both outputs
   (sha256 over sorted JSON). Identical hash = **DECORATIVE** (canned output).
   Live proof: Goethe `/process` returned identical palettes for both
   (sha prefix 53a74256e4ecbefa), theme locked to `da_vinci`.
2. **Determinism probe**: same input twice. Stable output = deterministic.
   If outputs differ per call with no seed change, the "differentiation" is
   randomness, not input-awareness (false positive for #1).
3. **Echo-dependency check**: distinctive input tokens (len>3, stopwords
   stripped) must appear in output (>= 1/3). Implementation:
   `validate_output_dependency()` in `organism/engine_dispatch.py`.
4. **Liveness probes must hit `/health`, never `/openapi.json`**: Farr :port
   returns HTTP 500 on openapi but `/health` is fine. openapi error != dead
   engine. (Census bug, corrected.)
5. **Never trust engine self-reports.** Verified pathology: Geschwind
   `/integrate` → `text:""` with coherence=1.0 ACCEPT; Broca `/plan` →
   word_count=0 with fluency=1.0 ACCEPT; language_pathway reported
   "completed, 3 hops, 0 failed" while carrying `transport_verified:false`
   in its own payload. Green self-reports on empty signal = conduction
   aphasia in silicon.

## Verified fleet state (2026-08-18)

- CANNED: Goethe /process, Luria /v1/review (100.0 on anything), Wernicke
  /process, Bichat :port /process, Bragg :port /process.
- REAL: `/v1/methodology/select` on all 5 creative engines — deterministic
  per situation AND different across situations (Goethe GOE-M01, Wernicke
  BRAND-VOICE-ARCH, Luria LUR-M01, Tawara BERK-RHYTHM, Bell BELL-M01).
  **The shared persona layer works; per-engine /process handlers ignore it.**
- REAL: Harvey fabric :port (publish/subscribe/replay roundtrip 13.98ms),
  Andreasen /v1/ideate (topic-derived combinatorial ideas + novelty scores).
- Mountcastle `/direction` is literal CW/CCW rotation — role-name collision,
  not an orchestrator intake.
- Fix pattern shipped: `persona_preflight()` — per dispatch, fetch the
  engine's own methodology/select for the task, inject as `persona_context`
  in the work-call body. Engines that consume it become specialists.

## Built (patterns to reuse)

- `organism/engine_dispatch.py` — the efferent limb: ledger task →
  routing_gate panel (first specialist WITH a port) → engines.json port →
  contract map `stores/engine-contracts.json` (data, per-engine body
  templates `{task_text}` + `{var|default}`) → POST → ledger outcome +
  task_event + bus post. DECORATIVE probe verdicts auto-quarantine;
  re-probe after fix auto-clears. Quarantined/refused attempts are recorded
  with reasons (never silent).
- `gates/engine_liveness_sentinel.py` — the patrolling immune cell:
  probe all ports → OK/FAIL events to `telemetry/events.jsonl` →
  telemetry_gate physics quarantines on critical slowing → routing_gate
  honors health-overrides. Reflex arc: sentinel (afferent) → telemetry_gate
  (analysis) → overrides (memory) → routing (avoidance). Before this,
  the system had antibodies but no patrol: Farr dead-but-declared-healthy
  for weeks, health-overrides empty since the events stream had no engine
  events.

## Task-ledger API gotchas (new this session)

- Lanes are a CLOSED list in `stores/task-taxonomy.json`: scheduler,
  registry, interop, stores, bus, deck, report, gg, fleet, security, legal,
  connectivity. `organism`/`engines` raise ValueError (error names the file).
- Python API signatures: `claim(c, actor, actor_kind, task_id=...)` but
  `complete(c, task_id, outcome, actor=...)` — complete takes NO actor_kind.
- CLI supports only `--submit/--list/--selftest`; claim/complete are
  Python-only.
- routing_gate.route() output: `{"decision", "specialists": [{name, port,
  ...}]}`. Persona-only specialists carry `port: null` — the efferent limb
  must pick the first specialist that HAS a port.

## All-night iteration protocol (principal standing directive)

- Rotate a DIFFERENT elite specialist per phase; record the rotation in the
  report header (L9 dogfood — the variation column is still manual until
  T-0173 class fixes land).
- End EVERY pass by writing NEXT PASS GOALS into `audit/RUN-RECORD.md` so
  the next brain starts warm.
- Mint defects to the ledger; bus engine-side fixes to sibling-agent WITH the
  live evidence; verify sibling closures by falsification, never accept
  self-reports (independently verified QA-27 closures honest: 0 dup ECS
  codes, no twin personas).

Related: `references/qa-pass-30-fresh-brain-rotation-2026-08-18.md`,
`references/persona-variation-qa-pass-27-2026-08-18.md`.
