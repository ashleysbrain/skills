---
name: external-platform-lane-decomposition
description: Use when onboarding an external agent platform.
version: 1.0.0
author: the operator agent Agent
license: MIT
provenance: agent
tags: [terraform, platform-integration, agent-platforms, architecture]
metadata:
  hermes:
    tags: [terraform, platform-integration, agent-platforms, architecture]
    related_skills: [tech-terraform]
---

# External platform lane decomposition

## When to Use

The principal orders an external platform assimilated — "terraform X", "be ready for X
on connect", "research dive to build the right architecture between X and our
stack" — where X ships a consumer agent product AND a hosted model API AND
(possibly) a coding harness AND (possibly) open weights. One seat per lane; never
one blob. Also use for any re-dive order on an existing platform dossier.

## Procedure

1. **Enumerate the surfaces from the vendor's DEVELOPER docs, not the launch post.**
   Launch posts describe value; developer docs describe surfaces. List every
   addressable surface before designing any seat. Determine each arrow
   empirically: if the docs show clients connecting to the user's own instance
   with no agent-control API, the consumer product cannot be driven — only
   supplied with endpoints and skills.
2. **Decompose into the four lanes and write the seat map (arrow, owner, gate per
   lane):**
   - HANDS (consumer agent app / sandboxed VM): entourage seat — the platform
     takes human-assigned missions and calls OUR exposed connector endpoints.
     Our deliverable is a skills-for-them pack + typed endpoints; agent platforms
     are typically native connector-writers, so day-one self-integration is real.
   - BRAIN (hosted model API): a fleet model — fallback-chain and stack-selector
     candidacy, measured like any model lane.
   - ENGINEER (vendor coding harness): sibling harness — eval-not-seat; earns a
     slot only by beating existing harnesses on OUR tasks at OUR cost.
   - CANNON (open weights): vendor-independence exit — parked until mesh hardware
     can serve it; state the parameter class honestly (many-hundred-B = datacenter-
     class, not laptop-class).
3. **Wire-protocol diligence in the BRAIN lane.** When the vendor offers both a
   Chat Completions adapter and a Responses-style adapter with encrypted reasoning
   replay, agentic loops MUST use the reasoning-preserving one (vendor docs
   themselves report cross-turn reasoning loss -> repeated/contradictory/dropped-
   context loops on the other adapter). Check base URL exactness (trailing slash
   rules) and current model ids against the docs page the day you wire it.
4. **Rate-limit math before promising burst capacity.** Read the tier table from
   the vendor pricing doc: limits are per TEAM, not per key. Compute headroom
   against OUR measured peak RPM/TPM. The cheap tier's REQUEST cap (not its token
   price) is usually the trap for bursty fleet lanes.
5. **Trust boundaries per lane.** The consumer VM lane has its own egress-approval
   agent — treat awaiting-approval as PAUSE, not FAIL — and may train on
   trajectories BY DEFAULT: flip the training opt-out before any real data flows
   (step zero, not a settings afterthought). The model-API lane carries none of
   that; it is just a metered model.
6. **Early lane activation.** A third-party router route (key-free signup) can
   seat the BRAIN lane before the vendor's own key arrives — probe it as a live
   candidate and say so.
7. **File the seat map** to the ledger and the operator bus with (arrow, owner,
   gate) per lane, then stage the trigger checklist for the human-dependent lanes.

## Pitfalls
- **Reversed integration arrow is the #1 architecture error.** Designing a
  puppet contract (we drive their consumer agent) for a platform with no
  agent-control API produces an unbuildable plan that survives reviews because
  the launch post IMPLIED the surface. Arrow direction comes from developer
  docs only.
- **Seating the platform as one blob mixes trust boundaries.** The consumer VM's
  approval pauses and training defaults do not belong on the model lane, and the
  model lane's metering does not belong on the mission lane — one gate set per
  lane.
- **Do not seat the ENGINEER lane by reputation.** Harness benchmarks are vendor-
  selected; the only valid comparison is the same real tasks through our existing
  harnesses at our cost.

## Multi-pass adversarial verification (principal-distrust re-dives)

Signal: principal orders the dive again ("do another deep dive", "with a different
best-in-the-world brain") — treat as first-class instruction, not repetition.

1. Each pass runs under a DIFFERENT specialist lens (falsifier, security
   architect, integrator). Repeating the same lens converges on the same blind
   spots; a pass that finds nothing wrong with its predecessor was the same brain.
2. Treat your own prior pass as the primary suspect: re-derive every load-bearing
   claim from the vendor's PRIMARY sources (developer docs, engineering blogs,
   newsroom) — never helpdesk-vendor blogs or coverage posts. Secondary sourcing
   is the usual defect: pricing from a helpdesk blog is right-or-wrong by accident
   until corroborated by the vendor's own docs.
3. Hunt specifically for: reversed arrows, default-on data/training switches,
   stale model ids and compressed version lineages, capability framings that name
   existing products as new ones.
4. Deliver corrections as OWED findings — name what the prior pass got wrong, in
   the principal reply and annotated to the ledger row. Owning the prior error is part
   of the artifact.
