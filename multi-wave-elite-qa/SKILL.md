---
name: multi-wave-elite-qa
description: Use when bulk-batch quality is questioned. Multi-brain QA.
version: 1.0.0
author: the operator agent Agent
license: MIT
metadata:
  hermes:
    tags: [qa, panels, delegation]
    related_skills: [adversarial-elite-panel-review, sequential-multi-agent-audit-execution, specialist-dispatch-discipline]
---

# Multi-wave elite-brain QA

## When to Use

The principal (or user) questions the quality of a large batch after the fact, or
orders thorough QA with multiple iterations from different brains per task.
Never run this as a self-review and never as a single panel pass.

## Standing rules

- **Per task: at least 3 iterations, each from a DIFFERENT named specialist.**
  Rotate lenses so iterations are independent, not three copies of a
  correctness check. Lens menu: quality gate (fidelity to source, format
  law, value-filter compliance), falsification (what measurement would
  refute each claim; citation alignment; physics-identity overreach), voice
  (AI tells, absolutism, buyer-vs-jargon), mechanical read-back (every
  claimed fix verified against the live DB/render), mapping depth
  (original synthesis vs boilerplate; unmined convergences), circulation
  (does the output actually reach its consumer).
- **Never reuse a brain across waves on the same corpus** — a verifying brain
  that built a fix will rubber-stamp it.
- **Apply ALL fixes between waves, then re-export the corpus** so the next
  wave reviews the post-fix state, not the state already condemned.
- **Verify live surfaces after applying**: restart the service, curl the
  page, grep the rendered HTML for the fixed strings — a fix that landed in
  the DB but not in the render is not a fix.
- **Report per wave**: verdict counts (PASS/REVISE/FAIL), named-brain
  attribution, every fix applied with its receipt, and what the next wave
  checks. Fixes applied silently between reports read as hidden rework.
- **Stop rule**: continue waves until a full wave returns zero FAILs and the
  remaining REVISEs are judgment calls, not defects.

## Procedure

1. **Build the review corpus first.** Export every artifact of the batch
   (cards, ledger tasks, documents) into one JSON snapshot under /tmp,
   queried directly from the source DBs — the panel reviews the snapshot,
   not chat memory; a wave briefed from memory re-reviews what was already
   condemned.
2. **Scope = every domain the batch touched, enumerated from the session
   log** — deliverables AND their dispatches, art builds, system repairs,
   ledger reservations. A corpus built from the newest workstream alone
   under-scopes the order: when the principal questions the quality of a big
   queue, the QA covers the WINDOW, not the artifact. Keep an explicit
   un-QAed-domains list while waves run and extend over the remainder
   before reporting done.
2. **Route the specialist gate, then dispatch wave 1** — one delegated
   subagent per lens (3 parallel), each returning a compact JSON verdict:
   pass/revise/fail counts, named weakest items, exact fixes. Do not poll
   transcripts; results re-enter on completion.
3. **Apply every named fix**
  in the source store (cards via UPDATE on the boards DB, task details via
  UPDATE on the ledger DB, artifacts via file edit), committed where
  git-tracked. Probe-verify each fix landed in-DB before the next dispatch.
  Operational remediations (disable the cron, kill the pid, close the bus
  row) are part of the fix set: execute the command AND read back the
  target's own state store (enabled flag, lsof, row status) in the same
  turn — a remediation decided and relayed in a report but never run is a
  fabricated close, and the fired job later falsifies it twice.
4. **Restart + live-verify the render**, then re-export the corpus as v2.
5. **Dispatch wave 2 with 3 fresh brains and different lenses** — the
   mechanical-read-back lens verifies wave-1 fixes; depth and circulation
   lenses find what correctness checks cannot.
6. **Report per wave and iterate** until the stop rule.

## Defect classes to seed the lens briefs with

- **Open-state perfective metrics**: open tasks whose metrics say
  "delivered" / "9/9 covered" — designed work labeled built. State open-work
  metrics as TARGETs; past tense only when the receipt exists.
- **Placeholder gate scores**: identical unscored F/T/est/info values on
  every row while citing a selection law — selection never computed. Score
  per item with the reasoning inline, or the law is decoration.
- **Analogy-as-identity**: "our gate IS an ELBO" where no latent structure
  exists — relabel ANALOGY, reconcile with the sibling artifact holding the
  weaker position, scope "ENTIRE thesis"-class claims.
- **Causal explanations without baselines**: "explains our results" with no
  pre-registered baseline cannot fail — label HYPOTHESIS and snapshot the
  numeric baseline before any behavior change rides on it.
- **Done-state receipt fabrication**: "verdict recorded" when none exists —
  done-states close only on real receipts.
- **Citation misalignment**: the famous theorem cited to the companion
  paper — verify against the actual abstract and split the citations.
- **Delivery-count metrics on unwired artifacts**: counts of things
  delivered to consumers that were never dispatched — count the dispatch
  rows, not the claims.

## Pitfalls

- Route the specialist gate immediately before EACH subagent wave — the
  route expires after ~5 minutes and a multi-wave sequence hits the expiry
  mid-run.
- Keep each wave within the concurrent-children limit; split into two
  delegate calls rather than exceeding it.
- An output_schema with a placeholder or malformed type string aborts the
  whole dispatch before any child starts — validate the schema shape before
  dispatch.
- Compressor damage runs in BOTH directions. Incoming: a delegated
  reviewer's verdict can arrive mangled — validate its JSON parses before
  applying its fixes; a mangled verdict is a re-dispatch, not a guess.
  Outgoing: after your own context has been compacted, long inline dispatch
  payloads you compose can carry omitted-chunk markers — check the
  delegate_task ECHO for compression artifacts before letting the wave
  run; if present, the child ran on a truncated brief. Compose wave briefs
  from the on-disk corpus export (path pointer + short facts), never by
  reproducing long text from compacted memory.
- Subagent file writes can be blocked by write gates on target paths; a
  terminal-heredoc fallback inside the child loses nothing if the child is
  told to expect it.
- Fidelity drift inflates source specifics ("50-page contract" for a source
  that said "document") — the falsification lens checks the artifact's
  numbers against the fetched source text, not against the digest that
  quoted it.
- A wave verdict asserting LIVE system state (a cron stalled, a daemon
  dead, a row unclaimed) can itself be wrong: the panel read a stale export
  or a partial log and issued an operational verdict with confidence.
  Before executing any verdict-driven restart/kill/disable, spot-check the
  strongest operational claims against the live store (cron list,
  launchctl print, port /health, the bus table) — a measurement that
  REFUTES a panel's verdict saves churning healthy daemons, and the
  refutation belongs in the wave report as a finding, not as noise.
