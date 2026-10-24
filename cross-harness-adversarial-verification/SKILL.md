---
name: cross-harness-adversarial-verification
description: "Verify build claims with independent harness+model seats."
version: 1.0.1
category: operations
author: the operator agent Agent
license: MIT
provenance: agent
tags: [adversarial, verification, cross-harness, qa]
metadata:
  hermes:
    tags: [adversarial, verification, cross-harness, review]
    related_skills: [harness-cli-headless-diagnosis, specialist-dispatch-lifecycle]
---

# Cross-Harness Adversarial Verification

## When to Use
- Any "prove it" moment: a principal/CTO/reviewer rejects self-reported build
  claims and demands independent verification.
- Adversarial QA of a deliverable before it ships or before reporting done.
- Standing a reviewer bench or health-checking one before dispatching to it.
- NOT for routine code review inside one harness — this skill exists to
  break single-harness confirmation.

Class of task: proving that claimed work is real (to a principal, CTO, or reviewer
who does not take the builder's word for it), and adversarial QA of any
deliverable. The reviewer seat must be independent of the builder on BOTH
axes — the clearest statement of the rule is the ruling itself:

> "Adversarial = another harness and model."

## Always-on rules

1. **Different harness AND different model family per adversarial seat.**
   A subagent reviewer spawned inside the builder's own harness on the same
   model family is an echo: it inherits the builder's blind spots AND its
   failure modes (a provider rate-limit storm kills both seats at once).
   Kill an echo reviewer mid-flight; do not re-dispatch it; never let its
   output enter the verdict table as confirmation.
2. **Bench floor: 2 live harness+model reviewer combinations.** One live
   reviewer = a monoculture bench, which is itself a defect to disclose,
   not a condition to work around silently.
3. **Health-check the bench BEFORE promising verdicts.** Installed !=
   authenticated != model-creation-working; a harness can pass its own
   doctor command and still die at dispatch time. Run a one-line alive-check
   per seat (`--prompt "reply exactly: HARNESS-ALIVE"` or equivalent) and
   record dead seats with their failure mode (401 / expired OAuth /
   model-creation failure). Only a live probe returning real model output
   classifies a lane WORKING; diagnosed-but-dead is INERT with the cause
   named.
4. **Probe durable definitions, not only live runtime.** A claim about
   current state can be true at probe time and false after the next
   re-create: a runtime `docker update --memory` cap vanishes when the
   container is recreated from its start script or compose file — the cap
   must live in the run definition (env-overridable), so verification greps
   the definition files, not just `docker inspect`. Generalize: for every
   "X is now Y" claim, ask which artifact survives a restart, and probe
   THAT.
5. **Surface contradicting verdicts with the correction, never
   quiet-edit.** When an independent seat refutes a claim, report both the
   original claim and the refutation, fix the underlying defect, re-probe.
   Convergence (an independent seat re-derives a known flaw blind) is
   confirmation of the flaw, not novel damage — escalate, do not duplicate.
6. **Certify the hash in the same turn as the fix.** A certified sha256
   computed before the last edit certifies nothing — the next seat finds it
   matches nothing on disk and the closure is void. After EVERY fix batch:
   re-hash the artifact, brace-audit any regex/string replace (count `{` vs
   `}` in style/script blocks — a replace that swallows or strands a brace
   silently deletes the FOLLOWING rule, which mis-renders the headline
   element while every other check passes), then post the hash with the
   closure record. When a seat predicts a minimal-repair hash, your applied
   fix landing byte-identical to that prediction is the strongest closure
   evidence available — report it as hash-identity convergence.

## Procedure

1. **Assemble the claim bundle** from `templates/claim-bundle.md`:
   numbered claims, each carrying (a) the exact probe command(s) that
   produce raw evidence, and (b) the adversarial angle — the most likely
   way the claim is true-at-probe-time but false-in-effect (runtime-only
   state, unwired output, stale registry field, single-source number).
2. **Run your own probes first** and record the raw evidence lines. Your
   probe results are one input to reconcile against — never the verdict.
3. **Alive-check the bench**, then dispatch the bundle to each live
   harness+model seat in read-only mode (sandbox read-only; sqlite via
   `mode=ro` URIs only). Require per-claim TRUE / PARTIAL / FALSE plus the
   raw evidence line.
4. **Reconcile:** agreement across independent seats upgrades confidence;
   every PARTIAL gets its durable-definition check (rule 4) before final
   scoring.
5. **Report:** per-claim verdict table, raw evidence, dead-seat disclosure
   with failure modes, and the strongest weakness found — even when all
   claims pass, name the weakest seam.

## Pitfalls

- **Round count is never a stop condition.** A multi-round adversarial volley closes ONLY on the convergence pair — a full rotation across ALL independent seats returning zero new findings AND every prior finding closed with diff evidence (the fix visible in the artifact, not promised). Stopping at a fixed number of rounds ("two passes looked thorough") is the reviewer's convenience substituting for convergence; if round N finds real defects, fix and run round N+1.
- Do not spawn the "independent" reviewer as a same-model subagent because
  it is faster — the speed IS the echo; it returns the builder's own
  assumptions in new words.
- Verifying a number by re-reading the same source the number came from is
  not verification — probe the underlying surface (socket for a "serving"
  claim, definition file for a "durable" claim, real consumer for a
  "wired" claim).
- OAuth re-auth URLs are single-use and expire in minutes — re-arm one
  only on explicit user go-ahead, never in a loop; keep other reviewer
  lanes moving instead of serializing all verdicts behind the login.
- A reviewer that returns only prose verdicts with no raw evidence lines
  has not reviewed anything — the output contract (evidence per claim) is
  part of the dispatch prompt for this reason.
- A claim verified by one seat only, when a second seat exists but is
  dead, carries the dead-seat disclosure in the SAME reply as the verdict —
  verdict confidence is meaningless without the bench state it rode on.
- **A micro-fix seat reporting after the fix it demanded is not a new
  finding** — reconcile its verdict against the fix timestamp before
  treating it as a reopen trigger; if the defect it names is already closed
  in-file, record the closure, do not dispatch another round for it.
