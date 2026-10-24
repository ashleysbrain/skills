---
name: law-enforcement-gates
version: 1.0.0
author: hermes-curator
license: MIT
description: "Use when a rule must be mechanically enforced: gates."
metadata:
  hermes:
    tags: [gates, enforcement, hooks, corrections, reliability]
    related_skills: [orchestrator-delegation-custody, mosaic-law-corpus]
---

# Law-Enforcement Gates

Converting standing rules and user corrections into mechanical pre-action
blocks. Use whenever a correction lands twice, a "remember this" is explicit,
or prose reminders have already failed once — that failure is the signal
that a gate is needed.

## When to Use
- A user correction was violated again despite being recorded as prose
- The user asks how the system will stop repeating an error
- Building or extending a pre-action hook that blocks tool calls
- Auditing whether an enforcement claim is real (blocks logged, battery passed)

## Core Principle
A prose reminder ("never do X") and the live task compete for the same
attention window; under pressure the task wins — a freshly-recorded rule can
be violated minutes later. A pre-action hook that exits non-zero BLOCKS the
violating call before it exists. Prose is for humans deciding; gates are for
agents under load.

## Procedure
1. **Distill the law to a mechanically decidable shape.** Name the tool,
   the field, and the condition: "block `cronjob_manage` create when args
   carry a recurring schedule and a non-watchdog prompt". Laws needing
   human judgment stay in skills; only the deterministic subset goes in
   the gate.
2. **Write one clause per law** in a small Python hook (see
   `references/gate-recipe.md`), each returning BLOCK + reason + the
   one-step recovery command (e.g. the re-route command) so recovery is
   a single step, never a debugging session.
3. **Battery-test BOTH directions offline before wiring:** every clause
   needs a must-BLOCK case AND must-PASS cases (benign writes, reads, and
   the same blocked action when its legitimate precondition holds, e.g. an
   active specialist routing). Run via `python3 <hook> '<json payload>'`
   and assert exit codes.
4. **Wire into `hooks.pre_llm_call` in `<agent-home>/config.yaml` via a
   terminal script** — the config file is security-protected and refuses
   patch-tool edits. Validate the YAML parses after the edit.
5. **Adversarially self-probe:** re-run the full battery AND attempt
   bypasses (path variants, benign-looking names, expired routing windows,
   the serialized-blob trap). Only then report ENFORCED — with probe output
   as receipts, not a sentence.
6. **Log state for auditability:** every BLOCK (tool, reason, timestamp,
   capped ring) plus a GO counter to a state JSON. This converts "the law
   is enforced" into a checkable claim the user can audit.

## Pitfalls
- **Match the specific FIELD, never the serialized JSON blob.** A regex
  like `r"...\.py$"` silently never fires against `json.dumps(arguments)`
  — the `$` anchor cannot match inside a blob ending `"}"`. This exact bug
  shipped and survived a first battery because only must-PASS cases were
  run on that clause.
- **A gate with a silent bug is worse than no gate** — it certifies safety
  it does not provide. Re-run the must-block battery after every edit.
- **Never report "recorded/enforced" off an ambiguous write status.** Read
  the store back or report the wedge; unverified persistence claims are
  the same fabrication class as unverified results.
- **Time-window preconditions (routing expiries ~300s) will fire mid-task**
  by design; the block message must name the recovery command. Never
  widen the window to avoid re-routing.

## Self-Audit
- Did every clause pass a must-block AND must-pass case this session?
- Did I try to bypass my own gate before calling it live?
- Is BLOCK state logged and readable by an auditor?
- Is each law's recovery path one command?
