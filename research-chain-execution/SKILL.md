---
name: research-chain-execution
description: Use when running multi-seat research chains for the OS.
version: "1.0.0"
last_updated: "2026-08-29"
category: operations
---

# Research Chain Execution (the OS)

## Trigger
Use when a task requires a multi-seat deep dive: model/provider research, layer-stack integration, adversarial verification waves, or any chain of delegate_task seats feeding a build lane. Class-level workflow distilled from the 2026-08-29 atlas (R1-R5 + V1-V3) and layer-stack (L1-L3) chains.

## The Chain Shape

```
census/measure (operator, live) → mint ledger task (single write path)
→ TRI stamp (triangle_router) → sequential research seats (R1→R2→…)
→ verification wave (V1 adversarial → V2 QA → V3 synthesis)
→ build-lane handoff (minted tasks, dependency-ordered)
```

## Hard Rules (each learned from a real failure)

1. **CENSUS BEFORE SCOPE.** Measure the live source (provider cache, ledger, registry) before writing the chain scope. A 2026-08-29 session scoped a model deep-dive from one config file; the real map was 10 providers / 320 models. The operator's view is substrate-narrow by default.
2. **MINT THROUGH THE SINGLE WRITE PATH.** `gates/task_ledger.py` submit() enforces birth certificate, flow tag (FLW-*), taxonomy kind/lane, GENOME gate for builds (canonical 8d dimensions only — accuracy/coordination/efficiency/latency for AI, never invented ones), title shape (signal word first, under 80 chars). Hand-invented T-* ids are refused. `database is locked` → retry with backoff, do not bypass.
3. **ROUTING IS NOT AUTHORSHIP.** The operator writes the SPEC; the specialist engine routes it (`sherman_router.py --gate --situation ... --operator <op>`). Never hand-author a specialist assignment the router should derive. If the principal asks "are YOU deciding how to delegate?" — the answer must be the router's record, cited.
4. **SEQUENTIAL SEATS, WRITE-FIRST SHAPE.** Bandwidth is single-model: one seat at a time, no children. Each seat's FIRST tool call is the append/write of its section skeleton — seats that explore-then-compose die at composition (harness max_iterations bug, 2026-08-28). Inline all needed facts in the dispatch context; salvage of a dead seat = re-append, not re-research.
5. **VERIFY ON DISK BEFORE ADVANCING.** After each seat: check file size grew, section header present, handoff line present, UNVERIFIED markers preserved. Then dispatch the next seat immediately — the chain advances on events, no idle gaps.
6. **DEBRIEF LAW v2 (binding).** Every seat AND the operator close with at least 5 what-went-wells, ALL failures/roadblocks/obstacles, at least 10 learned behaviors or information items, and at least 1 actionable question to the triangle. Debriefs are datapoints for process evolution, not ceremony.
7. **VERIFICATION WAVE BEFORE BUILD.** A research chain is not done when its last research seat lands. V1 (adversarial/Popper — citation-rot sampling, arithmetic recompute, live re-checks, real-gaps-only), V2 (QA/Luria — ratify-or-refute, apply patches, rule open questions), V3 (synthesis/Deming — final verdict + condition register). Budget about 8 minutes total; cost concentrates in V1. The 2026-08-29 wave yielded 2 doc errors fixed, 1 real guard gap closed, 1 systemic field (DEPLOYMENT-STATE) born.
8. **REAL GAPS ONLY.** In verification seats, every finding carries evidence (file:line, failed command, reproduced math). A survived attack is a deliverable; an invented gap is worse than a missed one. principal law: find gaps if and only if they exist — do not invent them.
9. **DEPLOYMENT-STATE FIELD.** Every chain handoff states DEPLOYMENT-STATE: spec | partial | shipped, with artifacts. Approval and deployment are different axes; the 2026-08-29 chains were VERIFIED-as-spec with zero enforcement shipped, and the field makes that visible in one grep.
10. **VERIFIED IS A STAGE, NOT A RESTING STATE.** A task reaching verified must mint its downstream action or explicitly close in the same cycle; dwell alerts fire at 24h (sev-1/2) or 72h (sev-3/4) idle (T-260829-0048).

## Mechanics Reference

- **Mint:** import the API (`sys.path.insert(0, 'gates'); from task_ledger import submit`) — the args-based CLI lacks a --flow flag. Required: title, kind, lane, origin, created_by, severity, detail (with GENOME for builds), flow.
- **Stamp:** `python3 /<workspace> --stamp <T-id>` → stage tri:review, group TRI-L1.
- **Dispatch:** delegate_task background mode; context carries census facts, prior-seat section pointers, and the laws (debrief, write-first, bandwidth); goal carries the deliverable spec.
- **Bus posts:** 2000-char cap (intake gate refuses longer) — split debriefs into parts. No `question` type exists; use handoff or alert.
- **Verify CLI before use:** bridges may take positional args (`memory_bridge.py remember <content>`) where you would expect flags.
- **the OS memory:** methodology and pinned facts go through `organism/memory_bridge.py` (DS O'Keefe :port), NEVER the the operator agent memory tool. Verify writes with recall (expect 0.7+ similarity).

## Pitfalls

- Reading one config file and calling it a census (substrate-narrow scope).
- Letting a seat verify its own work — verification is a separate station with different attack vectors.
- Carrying stale figures across seats ("23 flows" persisted until an audit found 59) — each seat inherits by citation to the file, not to prior summaries.
- Marking a chain done without the verification wave because the research seats all self-reported success.
- Open questions accumulating across seats — request ONE consolidated triangle ruling session rather than piecemeal.

## Session References

- `references/exemplar-2026-08-29.md` — gate-rejection shapes, bus caps, census numbers, wave yields, two-factor liveness proof (quick lookup)
- `/<workspace>` — exemplar chain output (R1-R5)
- `/<workspace>` — layer-stack exemplar (L1-L3)
- `/<workspace>` — exemplar verification wave (V1-V3)
- Related: `temporal-verification`, `verification-patterns`, `message-bus-protocol`, `agent-delegation-discipline`