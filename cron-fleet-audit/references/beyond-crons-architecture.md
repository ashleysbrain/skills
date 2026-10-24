# Beyond-Crons Architecture — Three-Layer Composition (2026-08-20)

Companion to SKILL.md "Beyond-Crons: Three-Layer Composition". Repo copy of the research memo: `your-stack/audit/BEYOND-CRONS-INFRA-MEMO.md`.

## principal ruling (verbatim intent, 2026-08-20)

"these process flows need to remove crons. We need to have as few a crons as possible. This whole crons throughout the day, cadence is ridiculous. And if they go, they have to go in the background. They cannot be crons that need human intervention because it's way too much for a human. So the crons, this cannot be crons driven primarily. We have to think beyond the crons for these process flows. So do not set up a bunch of crons for these process flows."

Follow-up directive same day: "Do thorough qa research on how to build the new level of infrastructure way from crons… is it the daemons or a combination of things? Add to the qa."

## Research verdict: a combination of three layers — NOT daemons alone

### Layer 1 — Event-reactive (the nervous system) → immediacy
Bus messages, webhooks, broker pulls fire the moment state changes. No schedule at all.
- Primary source: **arXiv 2606.20058** "Autonomous Event-Driven Multi-Agent Orchestration for Enterprise AI at Scale" (2026-06-18). Continuous event monitoring with priority inference + related-event merging + preemption beats request-response at enterprise scale. Key finding: **scale, not task complexity, dominates orchestration performance** — which is exactly why scattered per-flow crons rot as the fleet grows.
- the OS instance: conductor broker :port (Flow 16 salience gating, S = sev + 0.5*age + 0.6*type + 0.4*source + 0.8*novelty), bus atomic claim (Lamport mutex), poke daemon.

### Layer 2 — Durable reconciliation (the metabolism) → correctness
Supervised daemons (launchd KeepAlive) run observe → diff → act passes on intervals. Level-triggered, NOT edge-triggered: each pass reconciles observed vs desired state, so a missed tick or crashed pass self-corrects on the next pass — no catch-up schedules, no human intervention.
- Primary sources: Kubernetes controller reconciliation pattern (industry standard); **arXiv 2605.14968** "GraphFlow" (2026-05-14) — workflow-as-executable-spec with durable execution gives crash-resume semantics, the daemon equivalent of a cron catch-up minus the cron.
- the OS instance: autonomous_iteration daemon (15-min interval under launchd KeepAlive, INTERVAL env-tunable; runs improvement_scan battery S1-S8 + qa_meta).

### Layer 3 — Supervision (the immune system) → survivability
Let-it-crash + restart; watchdogs alert ONLY on failure (exit code ≠ 0, heartbeat silence, stall detection). THE ONLY PLACE CRONS SURVIVE — demoted from driver to alarm.
- Primary sources: Erlang/OTP supervision trees; **arXiv 2608.07627** "From Single Chatbots to Governed Agent Ecosystems" (2026-08-07) — the supervisor/orchestrator split for governed agent ecosystems; **arXiv 2607.11960** "Self-Healing Coordination in Cognitive Swarm Agents" (2026-07-12).
- the OS instance: daemon-supervision-v2 stack (launchd liveness → loop cadence+timeout → heartbeat freshness → meta-check cron as the second examiner from a different failure domain).

### Why not daemons alone
A pure event bus has no recovery for "event never fired" (bus lag, dropped webhook) and no drift detection for slow rot. The reconciliation layer makes the system self-correcting rather than merely reactive. 2606.20058 shows event-driven alone degrades at scale without a task-manager/priority-inference component. Events = immediacy, reconciliation = correctness, supervision = survivability; any one alone fails a different way.

## Cron-elimination law (audit signature)

1. Flows are event-driven: bus messages, webhooks, broker pulls, daemon passes.
2. Daemons are level-triggered reconcilers: observe → diff vs desired → act; a missed pass costs nothing.
3. **A cron that does WORK is a defect** (cron-as-driver signature). Crons exist ONLY as failure-only alarms.
4. Zero human intervention: supervision restarts, reconciliation converges, alerts page only on true failure.

Audit procedure add-on: for every process flow, classify each trigger as layer 1/2/3. Any cron doing work (ingest, digest, seeding, computation, healing) = flag as TECH-DEBT to retire into a daemon pass or an event. Document honestly as tech-debt, never as the design.

## Standing research lane

4 standing arXiv queries live in `your-stack/stores/qa-frontier-queries.json` + `research_scans.db.scan_topics` (created_by='qa-frontier'): "event-driven multi-agent orchestration", "durable execution workflow agents", "reconciliation loop controller self-healing", "supervision tree fault tolerance agents". The scan engine keeps this literature under watch permanently.

## the OS conversion table (2026-08-20 state)

| Layer | Exists today (verified) | Converts next |
|---|---|---|
| Event-reactive | broker :port pull; bus atomic claim; poke daemon | writing-pipeline webhook ingest triggers run immediately (replaces poll cadence) |
| Durable reconciliation | autonomous_iteration daemon (15m, S1-S8 + qa_meta) | research digest + coursework seeder fold into daemon passes (retire their crons) |
| Supervision | launchd KeepAlive; failure-only alert crons; daemon-fleet-meta-check | heartbeat-watchdog demoted to alert-only; remaining cadence crons audited into layers 1-2 |
