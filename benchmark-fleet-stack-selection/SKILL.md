---
name: benchmark-fleet-stack-selection
description: Use when choosing models/harnesses for task classes.
tags: [benchmarking, model-selection, stt, stack-selection, measurement]
version: 1.0
author: hermes
license: MIT
---

# Benchmark Fleet + Stack Selection

## When to Use

- A recurring task class (transcription, TTS, coding lane, vision, image-gen, embedding, rerank, judging) needs a model/harness chosen or changed
- A quality complaint arrives (garbling, repetition, wrong names) and the current stack is suspect
- A new capability arrives (new harness, new provider) and must earn its production slot

## Always-On Rules

1. **Measured runs only.** A layer with zero logged runs answers `UNMEASURED` — never a guess dressed as a recommendation. Log every run (wall time, quality metric, config hash) to the fleet store so `stack-for <task_class>` ranks from data.
2. **Switch production only after a back-to-back bench on the SAME input, same machine, same morning.** Cross-day or cross-machine comparisons carry load drift; the winner must beat the incumbent on both speed AND a task-specific quality metric (keyword recall for STT, loop-score for repetition-prone models).
3. **Gate quality with a scorer, not an eyeball.** For STT: n-gram loop runs, immediate-echo rate, unique-token ratio, keyword recall against known content of the note. A transcript that fails the repeat-audit fails, whatever its fluency.
4. **Load discipline is part of the measurement.** Read `uptime` before launching any decode; run candidate benches SEQUENTIALLY at `nice -n 19` under `terminal(background=true, notify=true)`. N concurrent large-model decodes saturate the cores, distort the timing being recorded, and can re-create watchdog cascades that orphan the very pipeline under test.
5. **Replay the production config exactly when isolating a defect** — same model file, same flags, same script path, read live from config (never from memory of it). Any drift invalidates the A/B.
6. **Paid keys bench through the budget guard** (check-and-reserve, hard abort at cap). A benchmark must never silently drain credit; free-lane and paid-lane runs are logged separately.
7. **A clean isolated replay + a dirty live transcript = live-path defect.** Before blaming the model, re-decode the exact cached file in isolation; if it comes back clean, investigate starvation (load) or double-processing upstream, not the engine.
8. **Selection operates on SLOTS, not bare models.** The candidate unit is (model, harness, thinking level, route); the same model at a different effort or on a different harness is a different candidate with different outputs, so log runs with all four and rank slots, not model names. Slot inventory lives in ecosystem-catalog.db, measured runs in benchmark-fleet.db; catalog upkeep and the /ecosystem + /stacks surfaces are covered by `ecosystem-catalog-operations`.
9. **Macro tasks are carrier-invariant by construction.** A multi-stage task
NEVER pins one model for the whole ride: state lives in the ledger row
(stages, leases, depends_on) with a serialized handoff packet at every stage
boundary (goal, decisions, evidence, next-stage spec). A mid-macro model swap
is a lease handover — re-entry starts from the packet, not scrollback.
Carrier dies mid-macro: lease expires, successor claims, reads the packet.
Carrier delisted: catalog sync prunes the slot, and the router re-picks per
microtask from measured rows only. Micro picks stay per-slot (rule 8);
continuity belongs to the work, not the carrier.

## Procedure (model switch for a task class)

1. Pull the incumbent config from the live system (e.g. `stt.providers.<name>.command` in config.yaml) and the recent real inputs (cached audio, real prompts).
2. Bench incumbent and candidate back-to-back on identical input, sequentially, load-checked, timed.
3. Score outputs with the task's scorer (repeat-audit for STT; domain keyword recall for naming-heavy audio).
4. If the candidate wins both axes: patch the production entrypoint (one line), then verify END-TO-END through the real path — the exact script the gateway invokes, not a manual equivalent.
5. Log the run rows to the fleet store; update the `stack-for` ranking. Record the loser's numbers too — negative results steer the next switch.
6. If the complaint persists after a verified-clean engine: chase the live path (load at decode time, duplicate passes), per references/stt-repeat-defect-diagnosis.md.

## Pitfalls

- Never bench on synthetic/ideal audio when the complaint is about real notes — accent, filler, and phone-codec compression are exactly where models diverge.
- Never trust a downloaded model file by size alone — verify with `file -b`; a wrong filename on a hub returns a tiny "Entry not found" text body with HTTP success.
- Temperature-fallback-capable decoders (whisper family) can emit looping n-grams on silence/noise; enable VAD (`--vad --vad-model <silero-ggml>`) on silence-looper models like large-v3-turbo rather than accepting the loops as speaker behavior.
- The user repeating themselves in input is NOT evidence of an engine defect, and near-fluency is NOT evidence of health — the scorer decides, both directions.
