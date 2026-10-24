---
name: veritas-pipeline-operation
description: Use when running or recovering Veritas pipeline runs.
tags: [veritas, writing-studio, pipeline, engine-health, qa]
---

# Veritas Pipeline Operation

Operating the Writing Studio pipeline (:port) programmatically when the user asks for content to "go through the writing process" or "through the studio". This skill is the operator manual; the architecture/build manual lives in `research-writing-studio-interface` (user-owned; not editable here).

## Auth

- Token: `/<workspace>` under `WRITING_STUDIO_TOKEN` (not `STUDIO_TOKEN`). Bearer header on every call to `http://127.0.0.1:port`.

## Procedure

1. **Register the draft**: `POST /api/drafts {"title", "content"}` → `{id}`. Update later via `PUT /api/drafts/{id} {"content"}`. There is NO stage-advance endpoint on drafts (`/stage`, `/advance`, `/review` all 404) — do not hunt for one; the pipeline runs through the veritas endpoints.
2. **Launch the run**: `POST /api/veritas/run {"idea", "author", "output_formats"}`. `idea` is capped at 2000 chars — distill the thesis and key moves, not the full text. Returns `{run_id}`.
3. **Poll**: `GET /api/veritas/status/{run_id}` every 20-25s. States: queued → running → completed | paused | failed.
4. **On pause**: read `error`, then diagnose from the state file (below). Fix, harvest, decide.
5. **Deliver inline when asked for copy-paste**: a file attachment does not satisfy "send in text format here" — paste the final text in chat.

## Engine health gate pauses (most common failure)

Several stages health-check named engines and pause the run when any is down.

1. `status.result.state_path` points at `/tmp/Veritas_process_state_<ts>.json`.
2. In that file, `health_snapshots` maps stage → `[{engine, scientist, port, alive}]`. Entries with `alive: false` are the engines to revive. Read the snapshot; never guess the port map.
3. Revive: `cd /<workspace><name>-engine && python3 run_server.py` as a background process; verify `curl 127.0.0.1:<port>/health` before proceeding.
4. Engines observed as gate dependencies: Wernicke :port, Tawara :port, Popper :port. Drift happens — the snapshot is authoritative.

## Convergence law (stage 6, binding on every run)

Papers ship only after >=10 review events AND 3 consecutive clean panels on the FINAL stored draft bytes; any defect resets the clean streak; exhausting the round budget fails CLOSED to human review. Env knobs: `VERITAS_REVIEW_FLOOR` (10), `VERITAS_CONSECUTIVE_CLEAN` (3), `VERITAS_MAX_REVISION_ROUNDS` (12).

**Fail-closed must be fail-closed END-TO-END (the clobber bug class):** a run-loop variable recording `convergence_unmet_fail_closed` is worthless if the outer stage machine never READS it — a later stage can overwrite the marker to `complete` and ship the body the convergence loop just refused. When hardening any pipeline state machine: (a) write the marker, (b) grep every downstream writer of that same status field, (c) make the run() loop abort on the marker, not merely record it. Prove the fix with BOTH proofs, never one: a clean run that converges AND a dirty run that aborts end-to-end (downstream counters frozen at zero, resume refused) — the proof of safety is in the failure path, not the success path. Patch discipline: backup the engine file first (`<name>.bak-<tag>`), patch, assert the fixed line is present (a quote-escape in the assert still proves the escape exists but proves nothing about the fix — grep for the FIX, not the artifact), then re-prove both paths.

**Unbounded retry loops around gated convergence:** when revision counters increment ONLY inside the revise path, a draft that never triggers REVISE never advances toward the budget — the loop can spin indefinitely at high event cost while never converging and never failing closed. Any budgeted retry loop must count EVERY round (clean or not) against the budget and expose an exit for non-converging-but-non-failing states.

**Classifier completeness:** a panel-verdict classifier with branches only for fail/revise cannot ever return PASS — real runs hit the unparseable branch and route to REVISE forever. When a gate classifies external input, enumerate ALL outcomes (PASS/REVISE/FAIL + unparseable default) before trusting any green run.

Run state `convergence_unmet_fail_closed` means the body is parked for human review - it did NOT ship and must NOT ship; downstream stages (6.5/7/7.5) are blocked after a fail-close. Report such runs as parked-with-ledger, never as a completed draft. Loop semantics, the mocked-engine verification recipe, and the defect classes to never reintroduce: `references/stage6-convergence-loop.md`.

## Known defect: resume cannot find /tmp checkpoints

`POST /api/veritas/resume/{run_id}` returns `400 "No checkpoint state found"` even when the state file exists at the /tmp path — the run writes checkpoints to /tmp while resume looks in its own state dir. Do not burn time retrying resume. Instead: harvest output, revive the dead engine, start a fresh run (with engines healthy the new run passes the gate that paused the old one and proceeds further). File the defect; do not silently re-derive the workaround each session.

## Harvesting output from a paused run

The state file carries all completed work: `current_stage`, `stages_completed`, `current_draft` (generated text), `citations`. A late-stage pause often holds a complete draft in `current_draft` — read it BEFORE re-running anything; it may already be deliverable after the tell-scan. Note `final_output` may be None while `current_draft` holds the text — check both keys.

## Delivering the result

- Run the AI-tell scanner (`ai-tell-removal-gate/scripts/scan_ai_tells.py`) on the harvested/generated text before delivery; fix and re-scan to PASS.
- Report pipeline state honestly: which stages completed, what paused, what was recovered. A paused run with harvested output is a partial success, not a completed process — say so.
