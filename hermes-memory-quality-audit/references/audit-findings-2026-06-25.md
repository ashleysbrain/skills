# Memory/Recall Audit Findings — June 25, 2026 (4th weekly cycle)

Baseline continuation from `audit-findings-2026-06-11.md`. This file captures
the distinguishing findings of the June 25 run; content-side findings unchanged
from prior weeks are referenced, not duplicated.

## Headline finding

**4th consecutive weekly audit with the same content-side findings and zero
execution between runs.** The June 25 audit's primary finding shifted from
per-item content issues to the structural loop failure. See
`stalled-loop-pattern.md` for the generalizable pattern.

## Findings — process/enforcement (PRIMARY this cycle)

| # | Issue | Severity | Type |
|---|-------|----------|------|
| 1 | Audit→action loop broken (4 weeks running). Recommendations verified across 3 audits, none executed. | CRITICAL | Process |
| 2 | Utilization bottleneck dominates retrieval. Assistant retrieves stored preferences but doesn't act on them at runtime. | HIGH | Process |
| 3 | Audit cron lacks memory read/write capability (cron sessions skip memory injection by design). Structurally guarantees the loop stays open. Root cause. | HIGH | Process |
| 4 | No typed metadata/lifecycle on memory entries. | MEDIUM | Process |
| 5 | No supersession mechanism — corrections produce near-duplicates. | MEDIUM | Process |

## Findings — memory-content (SECONDARY, unchanged since June 4)

| # | Issue | Severity |
|---|-------|----------|
| 6 | Blended specialist-routing note bundles 3 concerns in one sentence | HIGH |
| 7 | Missing exact-corrections preference | HIGH |
| 8 | Missing memory-maintenance expectation | MEDIUM |
| 9 | Missing model-policy note (non-Anthropic for agent/profile work) | MEDIUM |
| 10 | Stale Honcho provider state (localhost:port unreachable, no Docker) | MEDIUM |
| 11 | Memory at ~99% capacity (2,198/2,200 chars per June 11 snapshot) | HIGH |

## Recommended memory fixes (verified across 3 audits, pre-authorized)

Single atomic batch (handles capacity prerequisite via concurrent removal):

```
REPLACE old: <blended routing note>
   WITH: "[ROUTE] Always dispatch the operator agent/OpenClaw/memory/skill issues to engineer-architect lane, not generic pool."
ADD:    "[ROUTE] Elite scope-specific specialists preferred over generic handling for any non-trivial work."
ADD:    "[PREF] When user corrects wording/scope, preserve the correction verbatim. Do not paraphrase away the meaning."
ADD:    "[PREF] Memory drift is an operational maintenance issue. User expects active audit + correction, not acknowledgment."
ADD:    "[POLICY] Non-Anthropic models preferred for agent/profile/schema work (Gemini, Qwen, DeepSeek)."
```

Tag prefixes (`[ROUTE]`, `[PREF]`, `[POLICY]`) implement the lightweight typed-
metadata convention added to the skill this cycle.

## Research grounding (2026 consensus)

- **Write-manage-read loop** is the operational standard (arxiv 2603.07670,
  2604.16548). the operator agent runs pure write+read; the manage phase (consolidation,
  decay, eviction) is absent.
- **Utilization > retrieval as dominant bottleneck** (arxiv 2603.02473).
  Matches observed failure: stored routing preferences not honored at runtime.
- **Four consolidation levers** (Hindsight, May 2026): importance, merge
  (>0.85 similarity → averaged vectors + LLM conflict resolution), decay,
  eviction (>0.9 dedup). Mem0 reports -60% storage, +22% precision.
- **Schema-guided typed memory** (slavadubrov 2026-06-20; PersonaTree arxiv
  2606.04780): temporal validity, provenance, structured conflict handling.
  Tag prefixes are the lightweight string-level version.
- **Hardest open problems** (Mem0 state-of-memory 2026): cross-session
  identity, temporal abstraction at scale, memory staleness. All present here.

## Blockers

1. Cannot verify current memory state from cron (memory injection skipped).
   Recommendations based on June 11 snapshot. Interactive session may have
   partially applied fixes — the batch will fail safe if `old_text` no longer
   matches.
2. Honcho backend unreachable (localhost:port refused, no Docker).
3. Memory at capacity — no additive fix possible without concurrent removal.

## What's new this cycle vs. prior audits

- **New finding #3 (structural root cause):** the audit cron's lack of memory
  access is the root cause of the 4-week stall. Now the explicit primary
  recommendation.
- **Physics-informed read:** 4 weeks of recovery attempts with no convergence
  = critical slowing down. System near tipping point. Stop generating
  recommendations; change the structure.
- All content-side findings (#6-11) unchanged because nothing was executed.

## Recommended single highest-leverage action

Stop running this audit as a recommend-only cron. Either (a) grant it memory
read+write so it can execute its own verified recommendations, or (b) trigger
an interactive session that runs the batch above. Without this structural
change, the next audit will produce this same report.
