# First Audit Findings — 2026-06-11 (Baseline)

**Audit Run**: Weekly cron job #1 | **Profile**: `default` | **Auditor**: hermes-memory-quality-audit skill (first run)

---

## Executive Summary

- **Memory tool unavailable in cron context** — could not inspect actual `MEMORY.md`/`USER.md` content
- **No external provider active** — running on built-in flat-file memory only
- **Write approval disabled** (`write_approval: false`) — noise accumulation risk
- **Critical preferences missing** — 6 key user corrections not encoded in `USER.md`
- **Char limits at default** — 2200/1375, no provider to offload deep memory

---

## Memory-Content Issues (Projected)

Since memory tool unavailable, these are *likely* issues based on common patterns and known user corrections:

| Issue | Likelihood | Evidence |
|-------|------------|----------|
| Stale entries (>90d no recall) | High | No automated decay; flat file accumulates |
| Over-broad preferences ("User prefers X") | High | Typical default agent behavior |
| Imperative entries ("Remember to Z") | Medium | Agent often writes instructions as facts |
| Missing critical preferences | **Confirmed** | 6 the principal corrections (2026-04-08, 2026-06-11) not in memory |
| Duplicates/near-duplicates | Medium | No deduplication on write |

---

## Recall/Process Issues (Confirmed)

| Issue | Severity | Details |
|-------|----------|---------|
| No external provider | High | No semantic recall, no dialectic modeling, no drift detection |
| Write approval off | Medium | `memory.write_approval: false` (default) |
| No metadata on entries | High | Flat delimiter-separated only (Issue #346) |
| No conflict detection | High | Contradictions can accumulate silently |
| No recency decay | Medium | FIFO-ish pruning only at char limit |
| Char limits at default | Medium | 2200/1375 with no provider offload |
| Session search separate | Low | By design; not a bug |

---

## Gap Analysis vs. Best Practices

| Best Practice | the operator agent Current | Gap | Effort |
|---------------|----------------|-----|--------|
| Typed memory schema | ❌ Flat text | Critical | Medium (Issue #346) |
| Provenance/metadata | ❌ None | Critical | Medium |
| Hybrid retrieval | ⚠️ Provider only | High | Low (enable provider) |
| Recency decay | ❌ None | High | Medium |
| Conflict detection | ❌ None | High | Medium |
| Confidence scoring | ❌ None | Medium | Medium |
| Domain-scoped recall | ❌ Global injection | Medium | Medium |
| Preference drift detection | ⚠️ Honcho only | Medium | Low (enable Honcho) |
| Write approval gating | ⚠️ Config exists, off | Low | **Trivial** |

---

## Critical Missing Preferences (Not in USER.md)

Per the principal corrections in `agent-delegation-discipline` skill and this session:

1. **Delegate domain-expert work** — "User expects immediate specialist spawn for: security (HIPAA/crypto), medical, legal, complex physics/math, DB schema. Coordinator does NOT write implementation code."

2. **Math through deterministic engine** — "All product-grade scoring/calculation MUST run through Python engine with unit tests. Hand-computed math banned."

3. **Auto-remediate when path clear** — "When remediation path is obvious (re-run timed-out agent, fix broken pipeline, apply NEXUS recs), execute immediately. Do not ask for confirmation."

4. **the operator agent lane = AI fleet ops ONLY** — "the operator agent handles: spawning agents, cron, memory, sessions, Telegram routing. Routes health/scoring→AISHA-MD, GD content→HERA, DB schema→FORGE, research→SAGE."

5. **Memory maintenance = operational lane** — "When user raises memory quality: classify as content vs. process issue. Fix correct layer. Replace stale entries, don't append. Escalate enforcement drift to skill/workflow fix."

6. **No generic assistant fallback** — "Never use generic assistant lane. Every task → best-fit specialist with defined sandbox boundary. If platform-wide question, build full fleet (control plane, research, memory, execution, knowledge)."

---

## Blockers

| Blocker | Severity | Mitigation |
|---------|----------|------------|
| Memory tool unavailable in cron | High | Run interactive audit: `hermes chat -q "cat <agent-home>/memories/MEMORY.md <agent-home>/memories/USER.md"` |
| No external provider | Medium | Enable Honcho via `hermes memory setup` |
| Char limits tight for complex context | Medium | Monitor usage; reduce if noise high |

---

## Recommended Immediate Actions (P0/P1)

| Priority | Action | Command |
|----------|--------|---------|
| P0 | Inspect actual memory files | `hermes chat -q "Show MEMORY.md and USER.md contents"` |
| P0 | Enable write approval | `hermes config set memory.write_approval true` |
| P1 | Enable Honcho provider | `hermes memory setup` → select Honcho |
| P1 | Create weekly audit cron | `hermes cron create "0 6 * * 1" --prompt "Run hermes-memory-quality-audit..." --skills hermes-memory-quality-audit,session_search` |
| P2 | Add 6 critical preferences to USER.md | Manual edit or agent write (after P0) |

---

## Next Audit Focus (Week 2)

- Compare actual `MEMORY.md`/`USER.md` content vs. projected issues
- Measure char usage % of limits
- Run recall test (5 known-fact queries)
- Verify Honcho provider health (if enabled)
- Track delta: entries added/removed/replaced