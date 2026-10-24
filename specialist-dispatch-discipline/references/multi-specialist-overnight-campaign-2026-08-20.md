# Multi-Specialist Overnight Campaign Pattern (2026-08-20)

**Trigger:** User commissions overnight work with "do a deep qa review of all of our telemetry and all of our ontology... iterate until done correctly. at least 10 iterations from qa and same for build. this can happen throughout the night but don't default to crons"

**Outcome:** 7 elite specialists running in parallel (B1, B2r, B3, B4, B6, B8, B7p), 1 done (B5), no file collisions, bus lease active.

## Pattern: File-Ownership No-Overwrite Enforcement

**Problem:** Parallel specialists editing the same file = data loss or conflict.

**Solution:** Decompose tasks by file ownership and enforce via context contract.

```python
# B1 contract (the specialist engine)
context = "You own ONLY these files: /<workspace> and sense_collector.py. DO NOT touch any other file."

# B2 contract (the specialist engine)
context = "You own ONLY: /<workspace> and tests/. DO NOT touch real_sensors.py, sense_collector.py, or anomaly monitor."

# B3 contract (the specialist engine)
context = "You own: telemetry_anomaly_monitor.py, qa_tick.py, and any NEW module you create. DO NOT touch real_sensors.py, sense_collector.py, homeostatic_supervisor.py."
```

**Steering for intentional overlap:** When two specialists MUST touch the same file (B1 and B4 both editing real_sensors.py), steer one to sequence behind:

```python
delegate_task(action='steer', subagent_id=sa-0-8122fa8e,
    message="SEQUENCE CORRECTION: the specialist engine is actively editing real_sensors.py RIGHT NOW. Do T8 cron work FIRST — zero conflict. Only after T8 is verified, re-read real_sensors.py fresh: if sense_task_log already returns None-on-fail, your remaining job is purely the WIRED-vs-RETIRED decision. Make any real_sensors.py edit surgical (sense_task_log function body only), re-reading immediately before the patch. If B1's edit is still mid-flight when you get there, sleep 90s and re-read rather than racing.")
```

## Pattern: Bus Lease Announcement

Announce ownership on the operator bus before starting work:

```python
python3 /<workspace> post \
  --from hermes --to all --type status \
  --subject "OVERNIGHT LEASE: telemetry stack + ontology artifacts" \
  --content "HERMES takes lease NOW on: organism/real_sensors.py, homeostatic_supervisor.py, telemetry/, qa_tick.py, ONTOLOGY.md. OPENCODE retains ENGINE_REGISTRY.yaml/ecs.py lane pending ACK or flag collision by 00:30Z. No-overwrite law active: read sibling state before any write."
```

Result: bus 2743, visible to sibling-agent and all hermes sessions.

## Pattern: Campaign Index + Run-Record Chain

Maintain master index in `your-stack/audit/OVERNIGHT-CAMPAIGN-INDEX-YYYY-MM-DD.md`:

```markdown
| ID | Specialist | Scope | Status | Run-record |
|----|-----------|-------|--------|------------|
| B1 | the specialist engine | T3 NULL-law fabrication kill | RUNNING | RUN-B1-null-law-2026-08-20.md |
| B2 | the specialist engine | T1+T2 supervisor revival | RUNNING | RUN-B2-supervisor-2026-08-20.md |
```

Each specialist writes its own run-record (`RUN-B{ID}-{YYYY-MM-DD}.md`) with:
- Changes (file:line)
- Verification output (pytest pass count, sqlite3 query results)
- Live evidence (cron diff, port probe, grep delta)
- Limits (what was NOT done, why)

## Pattern: Subagent Timeout → Tighter Contract, Relaunch Immediately

**Problem:** B2 timed out at 427s "API call failed after 3 retries: Non-streaming API call timed out after 90s". Died in READ phase, never wrote anything.

**Solution:** Relaunch with tighter contract — edit-first, budget reads:

```python
delegate_task(context="""
A previous attempt timed out in the READ phase — go EDIT-FIRST, budget your reads (the file is only 334 lines: read it ONCE in full, then edit). DO NOT touch real_sensors.py, sense_collector.py, anomaly monitor, triggers, executor.
...
""", goal="B2 RELAUNCH — HOMEOSTATIC SUPERVISOR REVIVAL", role="leaf")
```

Rule: Never ask the user. Relaunch immediately with the learned constraint.

## Pattern: Gate Expiry Mid-Campaign → Re-Route Before Each Dispatch

**Problem:** Specialist gate expires after 5 minutes. Multi-hour campaign, gate expires mid-way.

**Symptom:** `SPECIALIST GATE BLOCKED: delegate_task. Sherman routing expired (>5 min old).`

**Solution:** Re-route before every new delegate_task:

```python
python3 <agent-home>/agent-hooks/specialist_gate.py \
  --route --situation "B6 dead-organ pruning..." \
  --specialist "the specialist engine"

# Then immediately dispatch
delegate_task(...)
```

## Pattern: Read-Only Prep Before Write Lane Falls Through

**Problem:** Write task B7 (registry consolidation) depends on sibling-agent ACK by 00:30Z. If sibling-agent doesn't claim, hermes must take it — but needs the plan ready instantly.

**Solution:** Dispatch read-only prep task NOW that builds the consolidation plan, mapping, and rollback path:

```python
delegate_task(context="""
STRICTLY READ-ONLY: you write ONLY run-record.md. NO edits to ENGINE_REGISTRY.yaml, ecs.py, ORGANS.json.
MISSION: (1) Parse each ENGINE_REGISTRY.yaml: count engines, list name+code+port per fork.
(2) Parse each ecs.py: what does each define, md5 them, show which diverge.
(3) Reconcile registry-vs-live: for the 81-ref fork the heartbeat collector reads, which refs point at ports NOT listening.
(4) CONSOLIDATION PROPOSAL (deliverable): which single file becomes canonical, where it lives, which copies become symlinks, migration steps ordered adiabatically.
""", goal="B7-PREP — REGISTRY FORK CENSUS + CONSOLIDATION PLAN", role="leaf")
```

The write execution happens when the lane clears — the prep makes the surgery instant.

## Pattern: Falsify Sibling Claims, Never Trust Self-Reports

**Problem:** B5 reported ":port double-booking resolved (the specialist engine sole tenant)" and "the specialist engine's registry code is GEN-00.01.08" — these CONTRADICT the original audit (O3 said Cannon AND Allostasis both attributed :port; git commit d4a095c says SUB-04.04.08).

**Solution:** Dispatch falsifier with explicit re-verify contract:

```python
delegate_task(context="""
TWO CLAIMS FROM B5 YOU MUST FALSIFY FIRST (never trust a sibling self-report):
(1) B5 claims ':port double-booking is resolved in-body (the specialist engine sole tenant)' — this CONTRADICTS the audit's O3 (Cannon AND Allostasis both attributed :port). Resolve with live probes: `lsof -iTCP:port -sTCP:LISTEN -P -n`, curl localhost:port/health, and grep every binding doc for 8091 attributions.
(2) B5 claims the specialist engine's registry code is GEN-00.01.08 and SUB-04.04.08 exists nowhere — verify: grep -rn 'SUB-04.04.08' and 'GEN-00.01.08' across ~/your-org and ~/your-workspace.
""", goal="B6 — DEAD-ORGAN PRUNING + LIVENESS CANONICALIZATION", role="leaf")
```

Never carry sibling assertions downstream without re-probing.

## Pattern: Todo List as Campaign Manifest

Build the full 20+ item list at campaign start:

```python
todo(todos=[
  {"id": "b1", "content": "B1 [the specialist engine]: T3 kill neutral-default fabrication in real_sensors.py", "status": "pending"},
  {"id": "b2", "content": "B2 [the specialist engine]: T1+T2 homeostatic_supervisor revival", "status": "pending"},
  ...
])
```

Update status as specialists finish (merge=true). This makes campaign state queryable without re-scanning the index.

## Anti-Pattern: Parallel Dispatch on Same Workstream

**What I did correctly (2026-08-20):** dispatched B1, B2, B3, B4, B5, B6, B7p, B8 in parallel with zero file overlap — each specialist owns a disjoint file set.

**What to avoid:** parallel specialists editing overlapping files without sequencing. This creates merge conflicts and data loss that only surface at CTO review.

## Reference

- Campaign index: `/<workspace>`
- Run-records: `your-stack/audit/RUN-B{ID}-2026-08-20.md` for each completed specialist
- Lease post: bus 2743