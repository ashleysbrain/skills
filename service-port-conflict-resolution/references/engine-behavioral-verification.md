# Engine Behavioral Verification — Live Probe Methodology

Verified 2026-08-19 (hermes night passes 31-40, DS organism creative spine).
Depth checks verify code EXISTS; they say nothing about whether an engine
BEHAVES. Three failure modes repeatedly made healthy engines look dead (and
dead engines look healthy):

## Failure mode 1: Contract field mismatch (healthy engine condemned as canned)

the specialist engine was falsely verdicted "canned copy" because the dispatch contract
sent `title` while the handler reads `spec.idea` — the text never reached the
engine, which then correctly processed an empty string. Same class: the specialist engine's
engine returns key `violations` but its API layer read `feedback`/`issues`, so
feedback was always empty.

RULE: before declaring an engine DECORATIVE/canned:
1. Read the engine's actual `/process` handler source (`src/api/server.py`)
2. Note the EXACT request fields it reads (`spec.get("idea")`, `input_data.previous_output`, ...)
3. Note the EXACT response keys the core engine returns vs what the API layer reads back
4. Probe with the engine's real contract, not the fleet-standard envelope

The canonical engine envelope is `{"content_spec": {...}, "input_data": {...}}`
with the brief in `content_spec.idea` — NOT a top-level `title`/`task` field.

## Failure mode 2: Verdict-mapping substring bug

the specialist engine: `verdict = "ACCEPT" if "GO" in raw_verdict` — but `"GO" in "NO-GO"`
is True, so every NO-GO mapped to ACCEPT. The gate rubber-stamped everything.

RULE: verdict/status mapping must exact-match a vocabulary tuple:
`verdict = "ACCEPT" if raw_verdict in ("GO", "ACCEPT", "PASS", "APPROVED") else "REDO"`

## Failure mode 3: Port squatting (wrong engine serving a port)

Registry said :port = the specialist engine; a launchd-parented restart had launched Luria
with `--port 8121`. Port listened, /health returned 200 — health sweeps passed
while every "Bell" dispatch was secretly answered by Luria.

RULE: identity-check, not liveness-check. `curl :<port>/health` must return the
registered engine_name. See the port-audit loop in the parent SKILL.md.

## Probe methodology

**Differential probe** (generative organs): two opposite inputs (funeral vs
birthday). Outputs must differ. Identical = suspect canned.

**Polarity probe** (GATE organs): two clean topics correctly BOTH return
ACCEPT — a differential probe false-negatives a healthy gate as DECORATIVE.
Gates get pass-case + fail-case instead:
- pass: "Revenue grew 12 percent. The team shipped the port conflict resolver."
- fail: "This will delve into synergy. Game-changer! Furthermore! Let us
  leverage cutting-edge solutions." (stock AI tells)
Healthy gate = ACCEPT on pass, REDO + named violations on fail.

**Determinism check**: same input 2-4x → identical md5. Different input →
different output. Task-id must NOT drive output (seed-driven; verify by
changing only the id and confirming identical output).

**Template completeness**: probes must substitute EVERY template var
(`{task_id}`, `{task_short}` included). Unrendered vars false-negative real
engines (Bragg select_action returned identical "" ids for both probes).

## Serving-copy divergence

The fleet may serve from a DIFFERENT directory than the canonical source
(agent-organism/<engine> vs your-workspace/<engine> are separate copies).
Patching canonical does nothing to the running service. To deploy an engine
fix: `lsof -ti :<port> -sTCP:LISTEN | head -1 | xargs -I{} lsof -p {} | grep cwd`
→ patch THAT dir → kill the PID → the fleet-autonomic pacemaker
(StartInterval=30s) resurrects it from patched source within ~30s → verify the
new PID serves the patched behavior. Waiting <35s beats fighting the pacemaker
for the port (your own bind attempt loses or doubles the engine).

## Verdict vocabulary (efferent limb, engine_dispatch.py)

- DISPATCHED: engine called + output echo-verified (task tokens present in output)
- CANNED_OUTPUT: HTTP ok but output independent of input
- ENGINE_ERROR: HTTP failure/timeout
- NO_VIABLE_ENGINE: routed panel fully quarantined (routing fact, not engine fault — telemetry records DEFERRED, not FAIL)
- DECORATIVE/SPECIALIZED: probe verdicts (differential or polarity)

## Reference verdicts (2026-08-19 night, live-probed)

| Engine | Port | Verdict | Probe evidence |
|--------|------|---------|----------------|
| the specialist engine | 8108 | REAL | topic-derived ideas, novelty 0.7071, echo 12/12 |
| the specialist engine | 8120 | REAL | funeral #ff8600 vs birthday #ff001b, id-independent, 4x deterministic |
| the specialist engine | 8122 | REAL (after 2 API-layer bug fixes) | AI-tell → REDO + violations; clean → ACCEPT 100 |
| the specialist engine | 8124 | REAL (was false-negative) | topic-driven headlines, md5-stable |
| the specialist engine | 8121 | REAL (restored from port squat) | 6KB branded HTML + 45KB PDF to disk |
| the specialist engine | 8150 | REAL | /select_action free-energy pick, deterministic |
| the specialist engine | 8089 | REAL | sleep/wake transitions, lagged-write consolidation |
| the specialist engine | 8092 | REAL | pub/sub roundtrip 14ms |
| the specialist engine | 8137 | BOOKKEEPING ONLY | traverse increments counters, hops always [], no delivery |
| the specialist engine | 8261 | ACCEPTS-AND-IGNORES | translate() echoes empty dimensions, match_rate 0.0 |
| the specialist engine | 8116 | NO WORK ENDPOINTS | persona surface only |
| the specialist engine, the specialist engine | 8001/8128 | CANNED | identical output for opposite inputs |
