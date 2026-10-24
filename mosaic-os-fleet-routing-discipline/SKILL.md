---
description: Use when routing the OS tasks or minting org laws.
name: mosaic-os-fleet-routing-discipline
trigger: When assigning the OS work to teams (research/glial/scouts/QA/triangle) or writing any division-of-labor or process-flow rule
---

# the OS Fleet Routing Discipline

## The Two Failure Modes (both caught by the principal 2026-08-31)

**1. Misrouting internal work to external teams.** A telemetry/ontology survey of the organism's own surfaces was minted as `research` and sent to research agents. Research agents do EXTERNAL work (literature, markets, prior art, the outside world). Internal perception/verification belongs to the scout fleet + QA.

**2. Minting org structure from one-turn judgment.** When correcting the above, the orchestrator minted a division-of-labor law in a single turn that listed "QA" and "glial" as parallel teams — wrong: QA is a sub-fleet INSIDE the glial team, which also carries conduction and build engines. principal: "you're muddying some waters here… you're doing this from the operator agent, you're not doing this from the OS." The law had to be retracted on the record and re-routed.

**3. The orchestrator building instead of routing.** Same evening, after minting a night-watch QA engine task, the orchestrator started hand-writing the sunrise-report script and launchd timer himself — stopped mid-turn by the principal: "You don't do the work… send through the right processes. You are not the operator agent you are the OS." The scripts were deleted before going live (nothing inert masquerading as capability) and the violation was recorded inside the minted task itself so the fleet sees it. The orchestrator contributes REQUIREMENTS only; the fleet builds everything, including support tooling around a delegated task.

**4. Converting a constraint into a stop (principal catch 2026-09-02).** principal ruled 'free-tier only' (a budget constraint). The orchestrator wrote 'image generation PAUSED' into the law and halted a work lane. principal: 'I said don't pause… wtf.' A resource constraint (cost tier, entitlement, rate limit, key availability) means RE-STACK the work onto the best free substrate — never pause a lane, never wait for principal direction. The vision-incident anti-pattern (hit a wall → stop → ask) is the same defect.

**5. Self-researching instead of routing (principal catch 2026-09-02).** Mid-answering a '$50 best value' question, the orchestrator began running web searches for vendor pricing itself. principal: 'You don't do the work.' Raw data points already gathered may be handed to the research lane as STARTING DATA, but the analysis, ranking, and card belong to the group. Orchestrator output = mint + dispatch + verify consumption, nothing else.

**6. Inventing routes over registered flows (principal catch 2026-09-02).** A content-pipeline task was routed as '~10 triangle passes' when the flow registry already carries FLW-WRITING (ingest → sherman route → research → draft → brand-voice → qa gates → publish queue). principal: 'You're not doing the processes right and building within the system. You're duplicating and doing whatever you want. You're acting like the operator agent.' HARD PRECONDITION on every routing decision: check `stores/flow-registry.json` first. If a registered flow exists, the task takes that flow with zero invented layers on top. New routes only when nothing exists, and they go through the flow-minting process.

## Rules

0. **Flow-registry check precedes all routing** (2026-09-02 law): read flow-registry.json before assigning any flow; registered flow wins over any improvised route; the triangle group USES studio flows for its own outputs — it never adds its own pass-route on top of them.
0b. **Decision-card triage (2026-09-02 principal ruling):** false-alarm / already-repaired / the-system-already-knows class NEVER reaches the principal. Triage owns it. Money/value questions DO reach the principal but scoped to the whole ecosystem — never to the vendor menu the current problem happens to offer; the group ranks options with evidence before the card goes out.
1. **Routing dimension — internal vs external (checked, not judged):**
   - research agents → EXTERNAL only
   - scouts + QA → INTERNAL perception and verification
   - glial team → conduction + build (QA is a sub-fleet within it)
   - triangle → convergence, iteration until all seats agree
   - principal → ratifies laws, gates go-live and final marks
2. **No process/routing/division law from one-turn judgment.** Structure comes from ground truth: GENOME blocks, build records, a census of what actually exists. Triangle proposes from evidence; principal ratifies. The orchestrator's job is to route the census/audit, not to author the org chart.
3. **When you catch a misroute:** fix the task's kind/lane, re-dispatch, audit for the same contamination elsewhere (it clusters), annotate affected records, and debrief the failure — do not mint a compensating law in the same breath.
4. **Process flows for each station must be outlined and assignment mechanical** (niche-to-task-class routing table), never grab-based. If you cannot state HOW tasks reach stations, that absence is itself the finding — route a flow-outline task.

## Verification Before Answering Routing Questions

- Ledger mint mechanics (single-write-path submit(), GENOME grammar, bus read-back): see `references/ledger-mint-gates.md`.

- Read the people/fleet registries and GENOME blocks for the actual current structure.
- Query the task ledger for the task's `kind`/`lane` and check it matches the work's true nature.
- Never describe team structure from memory of your own past statements — memory of a wrong mint is not ground truth.
