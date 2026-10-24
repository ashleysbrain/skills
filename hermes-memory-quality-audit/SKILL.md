---
name: hermes-memory-quality-audit
description: "Run a structured quality audit of the operator agent Agent's persistent memory (MEMORY.md, USER.md) and recall pipeline. Produces a standardized report with findings, gap analysis vs. best practices, and prioritized remediation."
version: 1.0.0
author: the operator agent Agent (cron job)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, memory, audit, quality, recall, cron, maintenance]
    related_skills: [hermes-agent, memory-maintenance-cadence, memory-recall-audit, honcho-memory-infrastructure]
    trigger: "Weekly cron job or on-demand when memory quality concerns raised"
---

# the operator agent Memory Quality Audit

A repeatable, standardized audit procedure for evaluating the quality of the operator agent Agent's built-in persistent memory (`MEMORY.md`, `USER.md`) and the recall pipeline (session search, external providers). Designed to run as a weekly cron job or on-demand when the user raises memory quality concerns.

## When to Use

- **Scheduled**: Weekly cron (e.g., `0 6 * * 1` — Monday 6 AM)
- **On-demand**: User says "memory is drifting", "recall is shallow", "you forgot X", or "audit memory"
- **Post-incident**: After a notable memory failure (missed critical preference, stale entry caused error)

## Critical Process Pitfall: The Stalled Audit Loop

**Symptom (observed Jun 4 → Jun 11 → Jun 18 → Jun 25, 2026):** Four consecutive weekly audits produced near-identical findings (blended routing note, missing exact-corrections preference, missing memory-maintenance expectation, etc.) with **zero execution between runs**. The audit produced correct recommendations but no follow-through.

**Root cause:** A recommend-only audit process is structurally broken. If the audit cannot execute its own verified recommendations, it will loop indefinitely. Three structural conditions trigger this:

1. **Audit runs in a context with no memory write access** (cron sessions skip memory injection by design). The auditor can read prior findings via `session_search` but cannot apply fixes.
2. **No owner is assigned to execute the recommendations** between audit runs.
3. **Recommendations are framed as discussion prompts** ("consider adding X") rather than pre-authorized, copy-paste-ready batch operations.

**Physics-informed read (critical slowing down):** When a system's recovery attempts show no convergence across multiple cycles, that is a critical-slowing-down signal — the system is near a tipping point. The correct response is to STOP pushing the same intervention and redesign the loop, not to generate the recommendation a 5th time.

**Fix — close the loop in one of three ways (in priority order):**

| Option | When to use | Implementation |
|--------|-------------|----------------|
| **A. Grant the audit write access** | Audit is the right owner of the fix | Configure the cron to run in a context with memory write capability, OR convert to an interactive-session trigger |
| **B. Pre-authorize execution** | Recommendations are verified across ≥2 prior audits | Frame recommendations as a copy-paste batch with `old_text`/`new_text` pairs ready to apply. The next interactive session runs the batch as a pre-authorized action list, not a discussion prompt |
| **C. Stop auditing, escalate** | After 3+ stalled cycles | Convert the audit into an escalation: surface the loop stall as the primary finding and stop generating per-finding recommendations until the loop is structurally fixed |

**Step 0 of EVERY audit (run before methodology Steps 1-5):** Query `session_search` for the prior audit's recommendations. Check whether they were executed (look for memory writes, skill patches, or config changes referencing the prior findings between the two audit timestamps). If `prior_findings == current_findings` AND no fix was applied between runs, treat the stall as the PRIMARY finding and apply Option A, B, or C. Do NOT generate the same per-finding recommendations a 4th time — that has near-zero information gain.

See `references/stalled-loop-pattern.md` for the full case study and generalization to any recommend-only review process.

---

## Audit Methodology

### 1. Inspect Current State
```bash
# Check memory tool availability
hermes chat -q "Show MEMORY.md and USER.md contents"

# Check config
hermes config check | grep -A5 "memory:"

# Check provider status
hermes memory status
```

### 2. Classify Each Entry
For every entry in `MEMORY.md` and `USER.md`, tag as:
| Tag | Meaning | Action |
|-----|---------|--------|
| `current` | Accurate, recently recalled, high value | Keep |
| `stale` | >90 days since last recall, or superseded by new info | Archive to session search, remove from memory |
| `overbroad` | "User prefers X" without context/conditions | Replace with contextualized version |
| `imperative` | "Remember to Z" reads as instruction not fact | Rewrite as declarative fact with timestamp |
| `duplicate` | Near-duplicate of another entry | Consolidate, keep best version with multiple evidence refs |
| `canonical` | Content duplicated from canonical source (e.g., BRAND-DNA.md) | Replace with pointer/ref to source |
| `missing` | Critical preference known from corrections but not in memory | Add (see Section 4) |
| `skill-locked` | Preference/constraint exists in 1+ skills but not in memory. Only loads when that skill is invoked, so sessions that don't load the skill never see it. Inverse of `canonical`. | Promote to memory if it must fire in ALL sessions (esp. cron/fleet contexts). Leave in skill if genuinely task-scoped. |\n
### 2.5 Episode Memory Audit (Honcho Observations)

When Honcho is the active memory provider, raw observations accumulate in its store between deriver cycles. Check for two failure modes:

| Pattern | What to Look For | Action |
|---------|-----------------|--------|
| **Completed-work logs** | Observations like "restarted X", "verified Y", "fixed Z" — resolved infrastructure work that has no future value | These violate the no-completed-work-logs rule. They should have been filtered by the deriver. If they persist, the deriver may be down (see `honcho-memory-infrastructure` skill). |
| **Procedures rotting as episodes** | A multi-entry block of observations that describe a reusable scoring rubric, decision framework, or step-by-step procedure (e.g., a credential scoring system captured as 25 separate observations) | Extract into a skill reference file (`references/<topic>.md`) under the appropriate umbrella skill. The procedure moves to the durable skill layer; the episode observations become redundant. |

**How to check:** Call `honcho_search` with broad queries like "rubric", "scoring", "procedure", "checklist", "framework" and scan for multi-observation clusters that read like a procedure manual rather than episodic facts. Each cluster found = a candidate for skill promotion.

**Promotion procedure:**
1. Identify the procedure cluster in Honcho observations
2. Determine which existing skill umbrella covers this domain
3. Write a condensed reference file via `skill_manage(action='write_file', file_path='references/<topic>.md')`
4. Add a one-line pointer to the skill's SKILL.md support files section
5. The procedure now lives in the durable skill layer; the episode observations become redundant

### 2.6 Identity Fact Verification

Cross-check every identity claim in `USER.md` (name, role, company, location,
pronouns, credentials) against **environmental evidence** — not just memory
consistency. Identity facts are the highest-trust entries in the buffer; a
wrong name poisons every downstream interaction.

| Evidence Source | What to Check |
|----------------|---------------|
| Workspace paths | `~/<name>-workspace`, project dirs, `.sibling-agent/` workspace names |
| Agent/health system names | Agents named after the user (e.g., `AISHA-MD` → user is Aisha) |
| Session history corrections | Search for `"my name is not"` / `"stop calling me"` / `"it's not"` — any correction means a wrong identity entry persisted |
| Git/email credentials | These are **NOT** identity evidence. Admin accounts, service accounts, and gcloud credentials use whatever email was configured — they do not reveal the user's name. |

**Credential inference poisoning** (observed 2026-03-24 through 2026-07-10):
A past session saw `principal.williams@divinityscience.com` in a gcloud credential
path and wrote "the principal Wilson" into `USER.md` as the user's name. The real name
is **Aisha** (evidenced by `~/your-workspace/`, `AISHA-MD` health agent, and
multiple explicit corrections across sessions). The wrong name persisted for
**months** because no audit step cross-checked identity claims against
environmental evidence.

**Rule:** Infrastructure credentials (email accounts, git author config, API
keys, gcloud accounts) are NEVER a source of personal identity facts. They
reflect whoever set up the infrastructure, not who the user is.

If an identity mismatch is found, fix `USER.md` immediately and search session
history for the user's explicit corrections to confirm the right value.

### 3. Evaluate Recall Pipeline
| Dimension | Check | Pass Criteria |
|-----------|-------|---------------|
| **Provider active** | `hermes memory status` shows provider | Honcho/Mem0/Hindsight/ByteRover/Supermemory active |
| **Write approval** | `memory.write_approval: true` | Enabled (prevents noise) |
| **Char limits** | `memory_char_limit`, `user_char_limit` | Appropriate for provider (lower if provider active) |
| **Semantic recall** | Test 5 known-fact queries | ≥4/5 correct with context |
| **Domain scoping** | Query with context filter | Returns scoped results (provider-dependent) |
| **Utilization** | Stored preference is retrieved but not acted on at runtime (e.g., wrong-lane routing despite a stored routing note) | Diagnose via `session_search` for cases where a routing/preference note was retrieved but the action diverged. **Utilization bottlenecks dominate retrieval bottlenecks** (arxiv 2603.02473 diagnostic framework). Fix by making entries action-triggering, not descriptive — see tag-prefix convention below. **Structural root cause (arxiv 2603.15125, verified Cycle 7):** conversational correction has ~100% relapse rate. Telling the agent the right answer does NOT fix stored wrong memory — the wrong entry persists and resurfaces. The stored entry must be edited/replaced directly. |
| **FTS5 skill-injection noise** | `session_search` returns 100KB-630KB payloads where the highlighted FTS5 snippets are dominated by repeated SKILL.md boilerplate text (because skills are injected as raw text into the user-message slot of cron sessions). | Run a sample `session_search(query="...")` and inspect payload size + snippet quality. If snippets are dominated by skill-injection text rather than genuine user voice, **signal-to-noise is degraded**. No runtime workaround in the auditor (cannot change FTS5 ranking). Mitigation: (a) quote exact user phrases in queries to bias toward user messages, (b) filter `role_filter=user` to restrict to user-originated text, (c) flag as engineering issue for the hermes-agent codebase (down-weight skill-injected message segments in discovery ranking). Observed 2026-07-06: every window landed on the skill-injection message, blocking access to the actual audit report tail. |

### 4. Apply Critical Missing Preferences
If not present in `USER.md`, add these (per Aisha's corrections 2026-04-08, 2026-06-11):
- **Delegate domain-expert work**: "User expects immediate specialist spawn for: security (HIPAA/crypto), medical, legal, complex physics/math, DB schema. Coordinator does NOT write implementation code."
- **Math through deterministic engine**: "All product-grade scoring/calculation MUST run through Python engine with unit tests. Hand-computed math banned."
- **Auto-remediate when path clear**: "When remediation path is obvious (re-run timed-out agent, fix broken pipeline, apply NEXUS recs), execute immediately. Do not ask for confirmation."
- **the operator agent lane = AI fleet ops ONLY**: "the operator agent handles: spawning agents, cron, memory, sessions, Telegram routing. Routes health/scoring→AISHA-MD, GD content→HERA, DB schema→FORGE, research→SAGE."
- **Memory maintenance = operational lane**: "When user raises memory quality: classify as content vs. process issue. Fix correct layer. Replace stale entries, don't append. Escalate enforcement drift to skill/workflow fix."
- **No generic assistant fallback**: "Never use generic assistant lane. Every task → best-fit specialist with defined sandbox boundary. If platform-wide question, build full fleet (control plane, research, memory, execution, knowledge)."

### 5. Produce Standardized Report
Use the template in `templates/audit-report.md`. Include:
- Executive summary (2-3 lines)
- Memory-content issues (stale, overbroad, missing)
- Recall/process issues (provider, config, pipeline)
- Gap analysis vs. best practices (table)
- Prioritized action plan (P0/P1/P2/P3)
- Blockers & risks

## Best Practices Reference (Condensed)

### Memory Schema (Target State)
- **Typed entries**: `fact`, `preference`, `procedure`, `constraint`, `episode`
- **Metadata per entry**: `source_agent`, `timestamp`, `confidence`, `evidence_ref`, `verification_status`, `domain`, `importance`
- **Hybrid retrieval**: Dense (semantic) + sparse (BM25) + metadata filters
- **Adaptive lifecycle**: Importance scoring → maturity tiers → recency decay (Weibull)
- **Conflict detection**: LLM pre-write check for contradictions
- **Tag-prefix convention (lightweight typed metadata)**: When the host memory tool has no native schema, prefix entries with `[ROUTE]`, `[PREF]`, `[POLICY]`, `[CONSTRAINT]`, `[PROJECT]` at the string level. Improves retrieval precision, makes supersession visible, and surfaces the entry type to the model at recall time. Example: `[ROUTE] Always dispatch the operator agent/OpenClaw issues to engineer-architect lane, not generic pool.` outperforms `Prefers elite specialists`.
- **Action-triggering phrasing**: Every preference/route entry must be phrased as a directive the model can directly execute, not a description of the user. Bad: "User likes concise responses." Good: "[PREF] Default to ≤3 sentences unless depth is explicitly requested." This directly attacks the utilization bottleneck (model retrieves the right memory but doesn't act on it).
- **Four consolidation levers** (Hindsight framework, May 2026): importance scoring, merge (similarity >0.85 → averaged vectors + LLM conflict resolution), decay (recency-weighted relevance), eviction (>0.9 dedup). Mem0 reports this cuts storage 60% and raises precision 22%. the operator agent currently runs pure append + manual compression — none of these levers are active.\n### Canonical Sourcing Principle\n- **Memory should point, not duplicate**: Rather than copying content from canonical sources (e.g., BRAND-DNA.md, PIML documents, engine registries), memory should contain pointers, references, or summaries with clear attribution to the source.\n- **What stays in memory**: Cross-cutting constraints that must fire in every session (including fleet/cron/contexts where creative-tagged skills don't load), user-specific routing rules, operational constraints, and pointers to canonical sources.\n- **What belongs in canonical sources**: Identity, voice, visual DNA, philosophy, product protocol, domain-specific facts, reference data, and detailed methodologies.\n- **Verification**: During audit, flag entries that duplicate content available in canonical sources as `canonical` tag and replace with appropriate reference.\n\n### Preference Evolution (arXiv:2510.09720)\n- Users are non-stationary — preferences drift\n- Honcho dialectic: periodic LLM synthesis of user model from interaction history\n- Track Intent-Experience-Utility triplets (what tried, what worked, what valued)\n
## Cron Integration

```bash
# Create weekly audit job
hermes cron create "0 6 * * 1" \
  --prompt "Run hermes-memory-quality-audit skill: inspect MEMORY.md/USER.md, classify entries, evaluate recall pipeline, apply critical missing preferences, produce report. Save report to session." \
  --skills hermes-memory-quality-audit,session_search \
  --channel last
```

## Destructive Deletion Pitfall (2026-06-29)

**CRITICAL: Never delete important memories to make room for new ones.**

When the the operator agent buffer hits its char limit, the WRONG response is to remove an
existing entry (especially time-sensitive or important facts) to cram in new
content. This was caught by the user: "You probably just deleted something
important, and you've done that before."

**Root cause:** The 2,200 char buffer tries to serve as both working memory
(identity, rules, current priority) AND long-term storage (project state,
domain knowledge). These are different memory systems in the brain and should
be different systems in the organism.

**Correct behavior when buffer is full:**

1. Check whether the new content belongs in T0 at all. Project state, domain
   knowledge, and session-specific facts do NOT belong in the the operator agent buffer.
   They belong in T2 (DS O'Keefe) or in files/git/operator bus.
2. If the new content IS a T0 fact (identity, rules, current priority),
   consolidate existing entries to make room rather than deleting. Merge
   overlapping entries into shorter combined versions.
3. If consolidation is insufficient, escalate the capacity problem as a
   system design issue (memory architecture), not a content triage issue.
   Do NOT silently destroy data.

**The tiered memory architecture:**

| Tier | Function | Storage | What Belongs |
|------|----------|---------|-------------|
| T0 Active | Working memory | the operator agent 2,200 char buffer | User identity, communication style, standing rules, CURRENT priority only |
| T1 Episodic | Session history | Session search (FTS5) | What happened in past conversations |
| T2 Semantic | Curated durable facts | DS O'Keefe (:port) | Project state, domain knowledge, decisions, environment facts |
| T3 Procedural | How to do things | Skills library | Workflows, procedures, step-by-step instructions |

**DS O'Keefe endpoint status (verified 2026-08-12, POST-FIX):**
- Versioning diagnostic: health `status:"online"` = stale v1.0.0, `status:"ok"` = current v1.1.0
- `POST /encode` — v1.1.0 fields: `{content: [float], location_vector: [float], tags: [str], reward: float, text: str}`. NOTE: `location_vector` NOT `location`.
- `POST /retrieve` — v1.1.0 fields: `{cue: [float], n_results: int}`. NOTE: `n_results` NOT `max_results`.
- `POST /consolidate` — `{dt: float}`.
- `GET /health` — `{status: "ok", engine_name: "DS O'Keefe", memory_count, ec_dim}`.
- `GET /memories` — Returns traces WITH text field.
- Bridge: `/<workspace>` — `store`, `recall`, `health` CLI.
- Persist: `<agent-home>/state/okeefe_memory.json` — server.py reads `OKEEFE_PERSIST_PATH` env var.
- Auto-repair: registered in FLEET_REGISTRY, watchdog restarts within 2 min if dead.
- See `references/okeefe-endpoint-status.md` for full API details and field-name migration table.

**Advanced memory physics (design phase, not yet built):**
- Free energy memory selection (Friston: keep memories that minimize surprise)
- Criticality tuning (Beggs/Plenz: stay near phase transition for optimal capacity)
- Ebbinghaus adaptive forgetting (R = e^(-t/S), old low-valence memories decay)
- STDP co-occurrence strengthening (facts that co-occur reinforce each other)
- Attractor dynamics for pattern completion (Hopfield networks in CA3 analog)

Bus messages 911 + 912 posted to sibling-agent with full design spec for advancement.

## Verification Checklist

- [ ] `MEMORY.md` / `USER.md` char usage < 80% of limit
- [ ] No entries tagged `stale`, `overbroad`, or `canonical` remain
- [ ] No procedures rotting in Honcho episode memory (checked via `honcho_search` for rubric/procedure/framework clusters)
- [ ] All 6 critical preferences present in `USER.md`
- [ ] External provider active and healthy
- [ ] Recall test ≥4/5
- [ ] Report saved to session and delivered
- [ ] No destructive deletions performed — if buffer was full, content was routed to T2 or consolidated, not deleted
- [ ] **Identity facts verified** — name/role/company in USER.md cross-checked against workspace paths, agent names, and session corrections (Step 2.6). No identity entry sourced from infrastructure credentials alone.

## References

- `references/best-practices-2024-2026.md` — Condensed research on LLM memory schema, retrieval, preference evolution
- `references/hermes-memory-architecture.md` — the operator agent-specific architecture details (limits, providers, config)
- `references/audit-findings-2026-06-11.md` — First audit run findings (baseline)
- `references/audit-findings-2026-06-25.md` — Fourth-cycle findings; confirmed 4-week stall + structural root cause (cron lacks memory write access)
- `references/audit-findings-2026-07-02.md` — Fifth-cycle delta; memory backend EMPIRICALLY confirmed disabled in cron (tested); Option C escalation active; exact pre-authorized batch for next interactive session
- `references/audit-findings-2026-07-06.md` — Sixth-cycle delta; new `skill-locked` finding type; FTS5 skill-injection noise blocker; cycle-6 pre-authorized memory entries
- `references/stalled-loop-pattern.md` — Generalizable pattern for any recommend-only review process that cannot execute its own fixes; case study + 3 fix options
- `references/credential-inference-poisoning.md` — How infrastructure credentials (email/git/gcloud) poisoned USER.md with a wrong name for 4 months; prevention rules for identity fact verification
- `templates/audit-report.md` — Standardized report template