# Audit Findings — 2026-07-16 (Cycle 7, Weekly)

**Session:** `cron_*` weekly memory-improvement audit
**Cadence:** Continuing from `audit-findings-2026-07-06.md` (Cycle 6).

## Step 0: Stall check

- Memory backend still disabled in cron context (tested: `memory(add)` returns "Memory is not available" even with valid `[source:]` markers). New integrity gate intercepted marker-less probe, but backend itself remains off.
- No evidence that any interactive session applied the pre-authorized batch from Cycles 5-6 (session_search for batch signatures returns only prior audit sessions).
- **Stall persists into 7th consecutive cycle.** Option C remains correct for the structural issue.

## What is NEW this cycle (information gain > 0)

### 1. Web search now available in cron

Cycles 1-6 could not do web research. Cycle 7 can. This is the first audit with live best-practices grounding against the current literature.

### 2. New research findings (not in prior condensed reference)

Key sources added to `best-practices-2024-2026.md`:

- **Memory poisoning attacks (arxiv 2603.15125):** 90% of tested agents vulnerable to memory poisoning, with **100% relapse rate when teams tried to fix by correcting the agent in conversation**. Conversational correction does NOT fix stored wrong memory — this is the structural reason the utilization bottleneck persists. Fixing requires editing the memory store directly, not telling the agent again.
- **Databricks (April 2026):** Agents that retrieved results from earlier incorrect runs **reused them with MORE confidence** — "memory had given the wrong answer the appearance of established precedent." Stale/canonical entries don't just add noise; they amplify wrong answers.
- **MIA (arxiv 2604.04503):** Compounding memory architecture — 7B model with structured memory outperformed 32B baseline by 18%. Structure beats raw capability.
- **Five cognitive memory types (survey arxiv 2602.06052):** Working / episodic / semantic / sensory / procedural — each needs DIFFERENT retrieval logic. the operator agent's flat 2,200-char buffer collapses all five into one store = category error.
- **Recency as first-class episodic signal:** Semantic similarity is the WRONG ranking function for "what did we decide about X two weeks ago." A session mentioning the topic in passing last week outranks the decision session from two weeks ago.
- **Forgetting is the most underrated operation:** Without active forgetting, stale/wrong entries accumulate quietly and degrade every future retrieval.

### 3. Updated diagnosis: two distinct problem classes

The observed failures map cleanly to the research:

**Memory-content issues (unchanged since Cycle 1, still unfixable from cron):**
- Blended routing note bundles 3 concerns in one sentence
- Missing exact-corrections preference (preserve corrections verbatim)
- Missing memory-maintenance expectation
- Missing non-Anthropic model-policy note
- Buffer at ~99% capacity
- `skill-locked` preferences (discovered Cycle 6): orchestrator-cognition rule, delegation hygiene rules live in skills, not memory

**Recall/process issues (PRIMARY, with new research grounding):**
- **Utilization bottleneck (dominant):** The agent retrieves stored preferences but doesn't act on them at runtime. The memory-poisoning paper explains WHY: conversational correction has a 100% relapse rate. The stored entry must be edited directly, not re-told. This is structurally unfixable while memory is disabled in cron.
- **No supersession mechanism:** When a fact changes, both old and new coexist. Databricks research shows this causes confidence inflation on wrong answers. The tag-prefix convention (`[ROUTE]`, `[PREF]`, `[POLICY]`) is the lightweight fix — it makes supersession visible at the string level.
- **No typed memory / single retrieval function:** The five-type survey shows each type needs different retrieval. the operator agent uses one flat store + FTS5. Episodic queries get wrong ranking (semantic instead of recency).
- **No active forgetting:** Stale entries accumulate. The four consolidation levers (importance, merge, decay, eviction) from Hindsight/Mem0 are all absent.

## Recommended action plan (unchanged structurally — still Option C)

The ONE structural fix remains: **grant memory read+write to the audit cron, or convert it to an interactive-session trigger.** No content fix matters until the loop can close.

The pre-authorized batch from Cycles 5-6 remains the correct next action for the next interactive session with memory write access. No changes to the batch this cycle — the content findings are unchanged and verified across 7 audits.

## Cycle 7 specific additions for next interactive session

Two new entries to add alongside the Cycle 5-6 batch (once memory access is available):

1. `[POLICY] Stored memory corrections require direct memory edits, not conversational re-telling. Conversational correction has ~100% relapse rate (arxiv 2603.15125). When user corrects a fact, edit the memory entry directly.`
2. `[CONSTRAINT] Stale/superseded entries must be explicitly marked or removed. Unmarked stale facts cause confidence inflation on wrong answers (Databricks 2026). Tag-prefix convention: [ROUTE], [PREF], [POLICY], [CONSTRAINT] make supersession visible.`

## Blockers

1. Memory backend disabled in cron — cannot inspect or execute (7th cycle confirmed).
2. FTS5 skill-injection noise in session_search persists (noted Cycle 6, not re-tested).
3. The stall is now structural — 7 cycles of identical findings with zero execution.
