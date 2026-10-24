# Audit Findings — 2026-07-23 (Cycle 8, Weekly)

**Session:** `cron_*` weekly memory-improvement audit
**Cadence:** Continuing from `audit-findings-2026-07-16.md` (Cycle 7).

## Step 0: Stall check

- Memory backend still disabled in cron (`memory(add)` + `memory(target=memory)` both return "Memory is not available"). **8th consecutive cycle.**
- No evidence any interactive session applied the pre-authorized batch from Cycles 5-7.
- The structural blocker is unchanged.

## What is NEW this cycle (information gain)

### 1. Web tool regression
Cycle 7 had working web search/extract (the first cron cycle able to ground findings against current literature). Cycle 8 has BOTH blocked:
- `web_search` → Firecrawl `BILLING_ERROR: insufficient_funds` (402)
- `web_extract` → same Firecrawl billing block on all 3 URLs tested

This means the research grounding achieved in Cycle 7 cannot be extended or refreshed this cycle. The best-practices reference (`references/best-practices-2024-2026.md`) remains the most recent compilation — it is still current (updated 7 days ago with 2026 sources).

### 2. No new user corrections surfaced
Session search for memory-batch application signatures and recent "memory drifting / don't remember / recall" user voice returned no new interactive-session activity applying the batch or raising fresh memory complaints in the last 7 days.

## Diagnosis (unchanged — verified across 8 cycles)

The two problem classes identified in Cycles 6-7 persist:

**Memory-content** (pre-authorized batch ready, unverifiable from cron): overbroad routing note, missing verbatim-corrections pref, missing memory-maintenance expectation, missing non-Anthropic policy note, buffer near capacity.

**Recall/process** (PRIMARY, structurally dominant): utilization bottleneck (conversational correction ~100% relapse per arxiv 2603.15125), no supersession mechanism (stale facts amplify wrong answers per Databricks 2026), single flat retrieval function for all 5 memory types, no active forgetting, audit cron lacks memory access.

## Recommended action (unchanged — still Option C)

The single highest-leverage fix: **grant memory read+write to this cron job, or convert it to an interactive-session trigger.** The `memory` tool is present in the cron tool surface; the block is a runtime config decision (`skip_memory=True` default for cron sessions). Flipping that single flag closes the loop and lets the audit self-execute the pre-authorized batch that has now been ready for 3+ cycles.

The pre-authorized batch (Cycles 5-7) is correct and complete. No changes needed.

## Blockers

1. Memory backend disabled in cron — 8th cycle, structural.
2. Web tools now blocked too (Firecrawl billing) — new regression this cycle.
3. Loop has produced identical findings for 8 weeks with zero execution.
