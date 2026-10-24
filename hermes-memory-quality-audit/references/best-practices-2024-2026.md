# LLM Agent Memory Best Practices (2024–2026)

Condensed from: Maxim.ai, ByteRover (arXiv:2604.01599), Mem0, SSGM Framework (arXiv:2603.11768), MemRL (arXiv:2601.03192), Preference-Aware Memory Update (arXiv:2510.09720), ACM Survey 2025, IAAR Awesome-AI-Memory, 2026 Memory Survey (arXiv:2602.06052), Memory Poisoning (arXiv:2603.15125), MIA (arXiv:2604.04503), Databricks Memory Scaling (Apr 2026), Mem0 State-of-Memory 2026, SGAM (slavadubrov 2026-06-20).

---

## 1. Schema Design — Explicit Memory Types

| Type | Purpose | Example |
|------|---------|---------|
| `fact` | Verifiable, time-stamped claim | "Project uses pytest-xdist v3.5 (2026-03)" |
| `preference` | User's stated/implied preference with conditions | "User prefers concise responses for technical Q&A; wants detail for strategy" |
| `procedure` | Reusable workflow or protocol | "Deploy: run `./scripts/deploy.sh --env prod`" |
| `constraint` | Hard rule or boundary | "Never hand-compute scoring math; use rescore engine" |
| `episode` | Specific event with context | "2026-04-08: the principal corrected the operator agent lane violation — health work → AISHA-MD" |

**Required metadata per entry:**
- `source_agent` — which agent created/verified it
- `timestamp` — ISO 8601
- `confidence` — 0.0–1.0 (agent's confidence at write time)
- `evidence_ref` — session ID, file path, or user message anchor
- `verification_status` — `unverified` | `user_confirmed` | `cross_checked` | `superseded`
- `domain` — `health`, `fleet`, `gd`, `research`, `config`, etc.
- `importance` — 1–10 (decay weight)

---

## 2. Retrieval Pipeline — Hybrid + Metadata

### Two-Pass Retrieval
1. **Broad recall** (k=50): dense vector + sparse BM25 + metadata pre-filter
2. **Rerank** (k=5–10): cross-encoder or CoT LLM pass scoring relevance to current query
3. **Inject** top-k with confidence-gated threshold (e.g., `confidence > 0.7`)

### Metadata-Scoped Queries
Filter by: `domain: "health"`, `project: "sibling-agent"`, `time_range: "7d"`, `importance: ">5"`, `verification_status: "user_confirmed"`

### Recency Decay (Weibull / Exponential)
```
weight = importance * exp(-λ * hours_since_last_access)
```
- λ tuned per domain (health: slower decay; config: faster)
- Last access timestamp updated on every successful recall

---

## 3. Write Path — Conflict Detection & Consolidation

### Pre-Write Checks
1. **Contradiction scan**: LLM compares new input vs. existing entries in same domain
2. **Duplicate detection**: Semantic similarity > 0.85 → merge or reject
3. **Confidence assignment**: Based on source (user direct > observed > inferred)
4. **Provenance stamping**: Auto-fill metadata fields

### Consolidation on Limit
When char limit reached:
1. Score all entries: `score = importance * confidence * recency_weight`
2. Archive bottom 20% to session search (preserve full text)
3. Keep top 80% in active memory
4. Log consolidation event with timestamp

---

## 4. Preference Evolution — Non-Stationary Users (arXiv:2510.09720)

### Problem
Users' intents, preferences, goals shift over time. Static memory becomes stale.

### Solutions
| Approach | Mechanism |
|----------|-----------|
| **Dialectic reasoning** (Honcho) | Periodic LLM passes synthesize user model from interaction history; output structured preference updates |
| **Intent-Experience-Utility triplets** (MemRL) | Track: what user *tried* (intent), what *worked* (experience), what *they valued* (utility) |
| **Drift detection** | Compare current session preferences vs. stored preferences; flag divergences for review |
| **Versioned preferences** | Keep preference history; current version active, prior versions archived with timestamps |

### Implementation Signals
- User says "I used to want X but now Y"
- Repeated corrections in same domain
- Preference entry never recalled in 60+ days but new contrary behavior observed

---

## 5. Provider Comparison (the operator agent-Compatible)

| Provider | Schema Support | Hybrid Retrieval | Dialectic/Drift | Cost | Best For |
|----------|----------------|------------------|-----------------|------|----------|
| **Honcho** | Structured (scopes) | Vector + BM25 | Yes (dialectic cadence) | Free tier | Preference evolution, user modeling |
| **Mem0** | Scopes (conv/session/user) | Hybrid + rerank | LLM extraction pipeline | Free tier | Multi-scope isolation |
| **Hindsight** | Typed nodes | Semantic + keyword | No | Paid | Deep semantic recall |
| **ByteRover** | Hierarchical Context Tree | AKL lifecycle | Adaptive importance | Free | Agent-native curation |
| **Supermemory** | Flexible | Hybrid + rerank | Free tier | General purpose |
| **RetainDB** | 7 memory types | Vector + BM25 + rerank | Delta compression | Paid | Structured enterprise |
| **Holographic** | Graph-based | Hybrid | No | Paid | Relational memory |
| **OpenViking** | Flat + tags | Vector | No | Free | Simple needs |

---

## 6. Five Memory Types Need Different Retrieval (2026 Survey arXiv:2602.06052)

The 2026 survey maps five cognitively distinct memory types. The key insight:
**each type needs different retrieval logic, and most production systems collapse
them into one store — a category error.**

| Type | What it is | Correct retrieval | Common mistake |
|------|-----------|-------------------|----------------|
| Working | Active context window | Compression/prioritization | Treating as retrieval problem |
| Episodic | What agent did and when | **Recency-first ranking** | Semantic similarity (wrong function) |
| Semantic | Facts about world/codebase | Content-similarity (RAG) | Mixing episodic logs into semantic index |
| Sensory | Raw inputs (images/audio) | Summarize on ingestion → semantic/episodic | Storing raw without summarization |
| Procedural | How to perform tasks | Skill library / templates | Storing as prose facts |

**Five operations any memory system needs:** storing, retrieval, updating,
compression, **forgetting**. Most teams build the first two and skip the rest.
Forgetting is the most underrated — stale/wrong entries accumulate quietly
and degrade every future retrieval.

## 7. Memory Poisoning & Confidence Inflation (2026)

### Conversational correction has ~100% relapse rate (arXiv:2603.15125)
A security study of memory poisoning attacks found **over 90% of tested agents
vulnerable**, with a **100% relapse rate when teams tried to fix the problem
by correcting the agent in conversation.** Telling the agent "no, the right
answer is X" does NOT fix the stored wrong memory. The wrong entry persists
and surfaces again.

**Implication for the operator agent:** the utilization bottleneck (stored prefs not
honored at runtime) is structurally unfixable by conversational correction.
The stored entry must be edited/replaced directly. Tag-prefix supersession
(`[ROUTE] old → new`) makes the correction visible at the string level, but
the OLD entry must actually be removed or it will resurface.

### Stale facts amplify wrong answers with confidence (Databricks Apr 2026)
Databricks published a concrete example: agents that retrieved notebooks from
earlier incorrect runs **reused those results with even more confidence** than
before, because memory gave the wrong answer "the appearance of established
precedent." Stale entries don't just add noise — they actively amplify errors.

**Implication:** unmarked superseded entries are actively harmful, not just
wasteful. Every supersession must explicitly mark or remove the old version.

### Compounding memory beats raw capability (MIA, arXiv:2604.04503)
A 7B model using MIA's structured memory framework outperformed a 32B baseline
by 18%, with gains holding on frontier models. Structure beats raw capability.

## 8. SGAM: Schema-Guided Agent Memory (slavadubrov 2026-06-20)

When a user changes a fact (passport deadline July 15 → June 30), vector search
retrieves BOTH. The system must record that June 30 supersedes July 15.

**SGAM pattern:** treat durable memory as typed application state with:
- tenant scope (isolation boundary)
- validity windows (valid_from / valid_until)
- supersession (which older fact did this replace?)
- provenance (who said it, source episode)
- schema versioning (migration support)

**Write gate (Schema-Guided Reasoning):** before storing, the model must:
1. Inspect evidence → identify subject + attribute
2. Check whether the fact changes existing state
3. Produce a candidate write only after comparison

**Read path:** filter by tenant, type, subject, attribute, validity window FIRST.
Add vector/graph expansion only if exact state lookup is insufficient.
Reserve vector search for fuzzy recall — read mutable facts from scoped records.

## 9. Audit Checklist (Per Session)

- [ ] All entries have required metadata (or lightweight tag-prefix)
- [ ] No `unverified` entries older than 30 days
- [ ] No duplicates (similarity > 0.85)
- [ ] No contradictions detected
- [ ] Char usage < 80% of limit
- [ ] Provider healthy (if active)
- [ ] Recall test ≥ 4/5 on known facts
- [ ] Critical preferences present (see skill Section 4)
- [ ] Stale entries archived, not deleted
- [ ] No superseded entries left unmarked (poisoning/confidence risk)
- [ ] Episodic queries use recency-first ranking, not semantic similarity