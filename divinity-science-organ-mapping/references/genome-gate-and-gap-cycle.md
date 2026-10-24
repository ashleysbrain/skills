# GENOME Gate + Gap Cycle — wiring, battery, and pitfalls (session 2026-08-20, QA Passes 8-9B)

Class-level reference for two the OS OS organs built under the principal directive
"8d and physiomorphic foundations at allllll times": FLW-GAP-CYCLE (Flow 17)
and FLW-GENOME-GATE (Flow 18). Full narrative lives in
your-org/your-stack/audit/RUN-RECORD.md (Passes 8, 8B, 9, 9B) and
PROCESS-FLOWS.md (Flows 17, 18).

## The GENOME block (build-task DNA)

    GENOME: body=<system> scientist=DS <Name> physics="<principle>" 8d=<dimension>

Enforced in gates/task_ledger.py submit(): kind=build without a valid block
raises ValueError. Organ: organism/genome_gate.py. Census command shows build
coverage by body/8d/scientist:

    python3 /<workspace> --census

### Canonical vocabularies (single source: organism/organism_config.py)
- body: BODY_SYSTEM_ENGINES keys ∪ Gray's 11. immune ↔ lymphatic are the same
  system — immune aliases to lymphatic in canonical output. Engine-map keys
  add: connective, creative_visual, memory, metabolic, network, nucleus,
  regulatory, sensory (20 total).
- 8d: HUMAN_DIMENSIONS (physical, psychological, intellectual, social,
  spiritual, vocational, financial, environmental) ∪ AI_DIMENSIONS (latency,
  accuracy, coherence, alignment, efficiency, adaptability, coordination,
  consensus, load_balance).
- scientist: "DS <LastName>" — two-word names valid ("the specialist engine").

## Validation battery (8 cases — re-run after any gate change)

1. Valid genome accepted (body=immune → lymphatic canonicalization).
2. Genome-less build rejected at the write path.
3. Non-canonical body rejected (body=cyber).
4. Non-canonical 8d rejected (8d=happiness).
5. Non-build kind without genome passes (advisory only).
6. Scientist without "DS " prefix rejected (scientist=Burnet).
7. Gray's-only system + human dim accepted (body=urinary, 8d=spiritual).
8. Alias: parse_genome('...body=immune...')['body'] == 'lymphatic'.

## Pitfalls found the hard way (each cost a live failure)

- **Regex with one-word scientist capture**: `scientist=([^\s]+)` fails on
  "the specialist engine" / "DS Ramón y Cajal". Use a lazy non-space-free capture:
  `scientist=(.+?)\s+physics=`. The physics value is quoted; the scientist
  field is not — capture up to the physics keyword.
- **AST extraction misses AnnAssign**: organism_config.py uses annotated
  assignments (`BODY_SYSTEM_ENGINES: Dict[str, List[str]] = {...}`). A plain
  `ast.Assign` walk extracts NOTHING (empty dict) — half the body-system
  vocab silently missing. Handle `ast.AnnAssign` with non-None .value too.
- **Never exec() organism_config as a module**: standalone import raises
  NameError (WORKSPACE is defined only under its env guard). AST-literal
  extraction is side-effect-free and immune to module-level code.
- **Gate × organ collision**: an organ that mints kind=build without a genome
  will raise ValueError mid-tick once the gate is live. Pattern: mint with a
  default genome (connective/the specialist engine/interstitial wiring/adaptability) and
  catch ValueError per-item, log to stderr, never let the tick die.
- **Cap-before-dedup starvation**: `[:MAX]` slice applied before the
  already-minted check starves tail gaps forever (top-ranked items were
  already minted but still consumed cap slots). Fill-to-cap: cap counts
  MINTS, not items considered.
- **Soft-hyphen corruption (U+00AD)**: long-context sessions injected an
  invisible soft hyphen into an f-string, producing SyntaxError on run.
  If a freshly-patched file fails with "invalid non-printable character",
  strip U+00AD (`src.replace('\u00ad','')`) before deeper debugging.
- **SQLite .connect() silently creates**: probing a wrong DB path creates a
  0-byte phantom. Verify the parent dir + file exists BEFORE connect when
  the path was derived (symlinks + WORKSPACE.parent patterns lie).

## Gap cycle composition recipe (no-new-cron rule)

1. Organ writes its own state file (organism/gap_cycle_state.json) — census
   counts, minted list, verdict. Single source of truth for its sensor.
2. Autonomic bridge tick (hermes-autonomic-bridge.py main()) spawns the organ
   via subprocess.Popen fire-and-forget — never blocks the 60s cardiac tick.
3. Sensor (real_sensors.py sense_gaps) reads the state file: serves stale
   data this tick, kicks refresh if age > 900s, neutral defaults when absent.
4. Scoring: new dimension added to self_healing_loop.score() as a SATELLITE
   (outside principal-settled DIMS_CORE — 6D TWC composite must not be touched).
5. Alerting: detect() satellite_drop class covers scored dims outside the
   composite (GAPS, MCP both alert now; previously both were blind).
6. Hepatic filter excretes the alert when remediation is already minted —
   closing the loop without spamming the bus.

## Ledger interface facts (gates/task_ledger.py)

- submit() validates: kind, lane, flow code, stage vocabulary, assignee,
  genome (kind=build). Unknown anything → ValueError with remediation text.
- complete() only transitions rows WHERE state='claimed' — ALWAYS claim
  first (tl.claim(actor=..., actor_kind='ai', task_id=...)), else silent
  no-op. A close that "worked" may have done nothing.
- flow-registry.json is {"flows": [...]} — a dict, not a bare list. Reading
  it as a list raises TypeError: string indices must be integers.
- Append-only law is physical: triggers forbid UPDATE/DELETE on task_events
  and DELETE on tasks. Close with outcome, never delete.
- Every submit() with severity=1 (non-self-healing origin) fires a principal alert;
  submit() pokes conduction automatically (ledger-submit:<tid>).
