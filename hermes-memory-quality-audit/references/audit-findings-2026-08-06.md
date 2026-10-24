# Audit Findings — 2026-08-06 (Cycle 9, Weekly)

**Session:** `cron_*` weekly memory-improvement audit
**Cadence:** Continuing from `audit-findings-2026-07-23.md` (Cycle 8).

## Step 0: Stall check — STALL BROKEN

**Cycle 9 is the first cycle with memory write access.** Prior 8 cycles (June 4 - July 23) all reported "Memory is not available" in cron context. Cycle 9 confirms:
- `memory(add)` triggers the integrity gate (requires `[source:]` markers) but the backend IS writable
- Buffer was at 97% (4,849/5,000 chars) — near capacity
- The pre-authorized batches from Cycles 5-8 were PARTIALLY applied in interactive sessions: the `[PREF]` tag-prefix convention was adopted, the verbatim-corrections preference exists
- Two research-backed entries from Cycle 7 were never added until this cycle

## What was executed this cycle (information gain > 0)

### 1. Loop closed — 5 batch operations applied

| Op | Action | Content | Chars saved/gained |
|----|--------|---------|-------------------|
| 1 | replace | Compressed the principal image-editing entry (removed model path + verbose provider notes) | -88 chars |
| 2 | replace | Compressed VERITAS+CRUCIBLE entry (removed run command, endpoint count — belongs in skill) | -104 chars |
| 3 | replace | Compressed CONSCIOUSNESS TRAPS entry (tightened phrasing) | -81 chars |
| 4 | add | `[POLICY]` direct-edit-on-correction entry (arxiv 2603.15125) | +170 chars |
| 5 | add | `[CONSTRAINT]` supersession marking entry (Databricks 2026) | +149 chars |

**Net result:** Buffer went from 4,849/5,000 (97%) to 4,768/5,000 (95%). Made room while adding two new high-priority entries.

### 2. Web research regression (unchanged from Cycle 8)

`web_search` still blocked by Firecrawl `BILLING_ERROR: insufficient_funds` (402). Cannot refresh best-practices compilation this cycle. The `best-practices-2024-2026.md` reference (updated Cycle 7) remains the most recent compilation and is still current.

### 3. No new user corrections surfaced

Session search for "memory drifting / forgot / recall quality" complaints in July-August returned no new interactive-session activity raising fresh memory complaints. This suggests the partial application of prior cycle recommendations (tag-prefixes, verbatim corrections) has been sufficient to prevent visible regressions.

## Diagnosis update

**Memory-content issues (now largely addressed):**
- ✅ Blended routing note — was split in prior cycles
- ✅ Missing exact-corrections preference — added as `[PREF]` in prior cycles
- ✅ Memory-maintenance expectation — exists in `agent-delegation-discipline` skill
- ✅ Non-Anthropic model-policy note — exists in USER profile
- ✅ Buffer capacity — freed from 97% to 95% this cycle
- ✅ Direct-edit-on-correction policy — ADDED this cycle (Cycle 7 recommendation)
- ✅ Supersession marking constraint — ADDED this cycle (Cycle 7 recommendation)

**Recall/process issues (structural, still open):**
- Utilization bottleneck remains the dominant failure mode. The `[POLICY]` entry added this cycle attacks it directly: stored prefs must be edited, not re-told. But enforcement is still behavioral, not mechanical.
- No typed memory / single retrieval function. the operator agent uses one flat store + FTS5 for all 5 cognitive memory types. This is an architecture-level issue, not a content issue.
- No active forgetting / consolidation levers (importance scoring, merge, decay, eviction). All absent.
- FTS5 skill-injection noise in session_search persists (noted Cycle 6).

## Recommended action for next cycle

**Priority shift.** With the content backlog cleared, the next cycle should focus on:
1. **Verify the two new entries fire at runtime.** Next interactive session: does the agent actually edit memory directly when corrected, instead of re-telling? If not, escalate from memory entry to skill-level enforcement.
2. **Assess whether the buffer capacity (95%) is sustainable** or whether further consolidation/T2 offloading is needed.
3. **If web search is restored**, refresh the best-practices compilation with any new 2026 Q3 research.

## Blockers

1. Web tools still blocked (Firecrawl billing, 2nd consecutive cycle).
2. The utilization bottleneck is structurally unfixable without either (a) a mechanical enforcement layer that blocks wrong-lane routing when a stored routing note exists, or (b) active consolidation levers in the memory backend.
3. The flat-store architecture (all 5 memory types in one buffer) is a design constraint, not a content fix.
