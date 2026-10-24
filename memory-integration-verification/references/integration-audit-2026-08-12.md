# Integration Audit: O'Keefe Memory — 2026-08-12

Auditor: the specialist engine (synapses/integration). Read-only investigation.

## Executive Summary

O'Keefe is **theoretical infrastructure**. The engine runs (29 memories, v1.1.0),
the bridge exists, consolidation crons are active — but the READ path is **never
exercised at runtime**. When the operator agent needs a project fact mid-conversation, it
reads the T0-only flat buffer or uses session_search. O'Keefe recall has only
been called during the June 29 build/test session and audit sessions.

## Evidence by Check

### Check 1: Runtime recall usage — NEVER USED

session_search for "okeefe_bridge recall" and variants returned only:
- June 29 session (`20260629_085440_a0745193`): the BUILD session — store+recall test
- Same session lineage (`20260630_095343_4363c1`): continuation, same test

No hits for recall during real work tasks. Queries like
"okeefe_bridge.py recall during task" returned zero results.

### Check 2: Boot hooks — PRINT-ONLY or FAILING

**procedural-memory-boot.py** (`<agent-home>/agent-hooks/`):
- Lines 28-34 PRINT the rule "Episodic/T2: O'Keefe (:port) via POST /encode"
- NEVER calls recall() or POST /retrieve
- This is documentation injected into boot context, not integration
- The hook itself runs successfully (0 failures in gateway-stderr.log)

**hydra-memory-stack-bootstrap.py** (`<agent-home>/agent-hooks/`):
- Renders static MEMORY.md files from hydra-os memory-stack.json manifest
- Does NOT query O'Keefe
- FAILS with `[Errno 35] Resource temporarily unavailable` on 21+ session starts
  (grep count from gateway-stderr.log)
- Every session start triggers this hook, every failure is logged, nothing is fixed

### Check 3: Cron recall — ZERO OF 32 JOBS

Checked all 32 enabled cron jobs in `<agent-home>/cron/jobs.json`:
- None reference "recall" or "okeefe" in their prompts
- Every cron job starts from scratch with no memory of past project state
- The two O'Keefe crons (74b0b0d6db93, 3a6a39963bd2) only CONSOLIDATE, never recall

### Check 4: Real recall path — O'KEEFE NOT IN IT

When the operator agent needs a project fact:
1. Read MEMORY.md (T0 only — identity, rules, preferences)
2. session_search (T1 episodic — past conversation text)
3. Guess or ask user

The memory() built-in tool cannot be intercepted/routed. No wrapper or plugin
redirects memory reads to O'Keefe. The okeefe-memory-routing skill says "load
this skill when you need project state" but skills load REACTIVELY — there is
no trigger mechanism that fires when the operator agent encounters a gap.

### Check 5: Recall quality — BROKEN (strength inflation)

**Test 1 — Non-keyword query:**
```
Query: "what font does the user prefer"
Expected: font preference memory (trace 3646d91f8baf7b62, strength=0.65)
Actual: diagnostics/autoheal memory (trace 73e3d8747deec992, strength=1.30)
Result: WRONG
```

**Test 2 — Pure semantic query (no keyword overlap):**
```
Query: "typeface lettering text style"
Expected: font preference memory
Actual: diagnostics/autoheal memory (strength=1.30)
Result: WRONG — font memory not in top 5
```

**Test 3 — Keyword-rich query:**
```
Query: "Inter DM Mono Manrope Sora font typography"
Expected: font preference memory
Actual: font preference memory (strength=0.65) — correctly returned
Result: CORRECT, but only because of exact keyword overlap
```

**Root cause:** Consolidated memories inflate to strength 1.0-1.3. The hybrid
scoring formula's semantic_floor (0.3 × normalized_strength) gives them an
unearned floor of 0.3-0.39 even with zero keyword match. This drowns out
correct but lower-strength matches (0.5-0.7 strength, 0.3-0.5 keyword score).

## T2 Content Still in T0 Buffer

Three entries in MEMORY.md that violate the T0-only rule:

1. **Line 22** — "PROCESS RESTART: pipeline_api.py and gg3_gateway.py code
   changes require process restart..." — T2 (project-specific technical fact).
   Also stored in O'Keefe (trace with process/restart/deploy/gg3 tags).
   DUPLICATION across both stores.

2. **Line 20** — "[PREF] Writing Studio HTML edits: ALWAYS run `node --check`..."
   — Borderline T2. Contains project-specific detail (Writing Studio,
   viewRunResult line). Functions as a preference but references project-specific
   architecture.

3. **Line 3** — Font preference (Manrope/Sora, no Inter/DM Mono) — T0 preference
   but DUPLICATED in O'Keefe (trace 3646d91f8baf7b62). Should exist in one store.

## O'Keefe Engine State (verified live)

```
Health: {"status":"ok", "engine":"DS O'Keefe Engine v1.1.0", "port":port, ...}
Memory count: 29
ec_dim: 128
```

Engine was detected DEAD and restarted by auto-repair watchdog on 2026-08-12
(cron 132dd1d69078 output: "DS O'Keefe (:port) — detected DEAD, restarted
successfully, new PID 6658").

## Consolidation Cron State

Two crons run consolidation:
- **74b0b0d6db93** — "Hippocampal Memory Consolidation (SWR Replay)" — every 30m,
  runs `hippocampal-consolidation.sh` which calls `consolidation_daemon.py --once`.
  2195 completed runs. Last status: ok.
- **3a6a39963bd2** — "O'Keefe Memory Consolidation" — every 240m (4h), runs
  `okeefe_bridge.py consolidate` via agent prompt. 241 completed runs.
  Last ran: 2026-08-12T06:56:22. Last status: ok.

Both consolidate successfully. Neither recalls before starting work.

## False Claim in hermes-hippocampal-memory-architecture

The skill states under "Pre-Session Boot Sequence":
> "4. Queries O'Keefe for relevant T2 project state (Episodic Memory)"

This does NOT happen. The boot hooks never query O'Keefe. This claim gives a
false sense that the integration is working when it is not.
