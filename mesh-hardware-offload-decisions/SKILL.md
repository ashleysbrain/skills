---
name: mesh-hardware-offload-decisions
description: Use when deciding where organism workloads physically run.
version: 1.0.0
author: the operator agent Agent
license: MIT
metadata:
  hermes:
    tags: [mesh, hardware, offload, placement, sandbox]
    category: devops
---

# Mesh Hardware Offload Decisions

Governs the class "which machine runs which part of the organism": the principal
proposes hardware (cloud dedicated, NAS, laptops, consumer-agent VMs) to
move parts off an overloaded machine, or asks what a machine is actually
doing at night. Verdicts are placement decisions, written to the mesh organ.

## When to Use

- Evaluating any hardware candidate for offloading organism workloads.
- Asked "what is killing this machine / what runs here overnight".
- Deciding whether a part can move to an external sandboxed agent VM.
- Recording or checking a standing placement ruling (e.g. no local inference).

## Procedure

1. **Measure the resident load first — never quote footprints from memory.**
   `ps -axo rss` filtered to organism processes; container memory; per-night
   file-write census `find <workspace dirs> -newermt "<date> 23:00" !
   -newermt "<date+1> 06:00"` grouped by top dir; `pmset -g log` sleep/wake
   lines (maintenance wakes on battery = the machine never truly rests);
   DiagnosticReports for panics. Attribute load to named workloads before
   proposing any placement. When the question is CRASHES, read the machine's
   crash reports before attributing blame to any workload — the reports name
   the mechanism (GPU reset storms, display-server watchdog), and the loudest
   scheduled job is usually a contributor, not the cause. Full forensic
   hierarchy and the same-day lightening moves: see
   `references/crash-forensics-and-load-lightening.md`.
2. **Classify every workload by sovereignty before comparing candidates:**
   - Data-at-home (PHI-adjacent health lane, stores, ledger, keychain,
     operator bus): owned hardware only, never an external sandbox.
   - principal-facing limbs (gateway, Telegram, browser/Apple surfaces): stay on
     the principal's machine.
   - Compute class (builds, batch sweeps, heavy ingestion): biggest owned
     RAM, away from the principal-facing machine.
   - Sensory/muscle class (external watchers, research pulls, frontier
     scouts): safe for external sandboxes, secret-free.
3. **Compare candidates against the measured need.** Owned hardware beats
   equivalent rentals (already paid, data stays home). Remote dedicated
   enters only when burst load exceeds owned capacity. NAS-class CPUs run
   containers and batch, never inference servers. Laptops-as-servers need
   lid-close sleep disabled and a thermal burn-in check.
4. **External agent sandboxes (per-user cloud VMs): parts, never the whole.**
   No inbound ports means they can never host engines, the bus, or any
   server — move watchers, ingestion, and disposable scouts only. Cooperate
   via polling: each VM polls a work-outbox exposed on the tailnet, pulls a
   task card, posts results back; grant the egress approval once, standing.
   Provider egress sentinels subject anything that read local state to extra
   scrutiny, so keep such VMs secret-free. Several sandboxes usually means
   several accounts — that is the real limit, and it brushes provider ToS;
   paid seats are the clean version. One poisoned scout is burned and
   re-minted — that disposability is the feature.
5. **Write the verdict into the mesh placement organ**
   (`~/your-workspace/organism/mesh_placement_organ.json`), not just chat:
   role, load, why, caveats, resulting per-machine split. Record principal rulings
   as they land (a strike like "no local inference" closes that lane for
   every future proposal) so the plan never re-proposes a struck lane.
   Hardware the principal floats as an idea ("thoughts on this box?") is
   EVALUATION INPUT, not capacity: record it as a candidate with
   `available: false until ordered`, and never let a placement plan depend
   on unordered hardware. When a retraction lands: flip availability in the
   organ, stamp the ruling (who, when, scope), and notify the sibling whose
   capacity math referenced the machine — a retraction must cost one flag
   flip plus one notice, never a plan rewrite.

6. **Bootstrap a chosen remote node by rsync over the tailnet, not git
   clone** (fresh nodes carry no repo credentials), compile the scripts on
   the NODE's interpreter, and check for stale older mirrors before treating
   the node as empty. Full procedure in
   `references/crash-forensics-and-load-lightening.md`.

## Standing rulings (until the principal changes them)

- **No local inference anywhere** — all model calls stay on API providers;
  placement plans builds and batch, never model weights.
- One-machine-everything is a monoculture defect; the placement split keeps
  evolving as load changes.

## Pitfalls

- Quoting candidate specs or node membership from memory — probe the source
  (tailnet status, port, vendor page) before the verdict.
- Treating a partial move as failure — parts-not-whole is the correct shape:
  nervous system stays owned, sensory/muscle tissue can live outside.
- Recommending a local-model lane (weights on the NAS/laptop) — check the
  mesh organ's rulings first; it is struck.
- Forgetting that "always-on" loopers count as overnight load even when
  their schedule names no night hour.
- Planning against hardware the principal mentioned but never ordered — a musing
  is an evaluation request; machines get earmarked for other uses without
  notice, and a plan built on them is void the moment that lands.
