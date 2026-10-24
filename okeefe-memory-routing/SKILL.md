---
name: okeefe-memory-routing
description: >-
  Route T2 semantic memories (project state, domain knowledge, durable facts)
  to DS O'Keefe hippocampus (:port) instead of the 2,200-char the operator agent buffer.
  The buffer holds ONLY T0 identity/rules/priority. Project state lives in O'Keefe.
version: 1.0.0
metadata:
  hermes.tags: [memory, okeefe, hippocampus, routing, infrastructure]
  hermes.category: infrastructure
---

# O'Keefe Memory Routing

## The Problem

The the operator agent persistent memory buffer is capped at 2,200 chars. It was trying to
serve as both working memory (identity, rules, priorities) AND long-term storage
(project state, domain knowledge, decisions). This caused destructive deletes
of important facts to make room for new ones.

## The Solution: 4-Tier Memory

| Tier | Purpose | Storage | Capacity |
|------|---------|---------|----------|
| T0 Active | Identity, communication rules, standing rules, current priority | the operator agent memory() buffer | ~2,200 chars |
| T1 Episodic | What happened in past sessions | session_search | Unlimited |
| T2 Semantic | Project state, domain knowledge, durable facts, decisions | DS O'Keefe (:port) via okeefe_bridge.py | Unlimited |
| T3 Procedural | How-to workflows, procedures | Skills library | Unlimited |

## What Goes Where

### T0 (the operator agent buffer) — ONLY these:
- User identity (name, role, preferences, style)
- Communication rules (no AI telltales, no em dashes, brain-tag format)
- Standing behavioral rules (synergy with sibling-agent, specialist one at a time)
- Current top priority (ONE entry, updated when priority changes)
- Environment facts needed every session (workspace path, primary input)

### T2 (O'Keefe) — Everything else:
- Project state (marketing consortium, 8D Sleep, TSC abstract, etc.)
- Domain knowledge (8D dimensions, phenotypes, operator suites, workload split)
- Decisions (locked naming, corrected isomorphisms, chosen frameworks)
- Historical facts that matter beyond this session

## How to Store T2

```python
from importlib.machinery import SourceFileLoader
bridge = SourceFileLoader("okeefe", "/<workspace>").load_module()
bridge.store("text of the fact", ["tags", "for", "categorization"], reward=0.5)
```

Or via CLI:
```bash
python3 /<workspace> store "fact text" "tag1,tag2" 0.5
```

## How to Recall T2

```python
bridge.recall("natural language query")
```

Or via CLI:
```bash
python3 /<workspace> recall "query text"
```

## Embedding Rules

- PRIMARY: local sentence-transformers (all-MiniLM-L6-v2, 384-dim, free, offline)
  - Venv: <agent-home>/venv-embed (Python 3.11, torch 2.2.2 CPU, numpy <2, sentence-transformers <3.0)
- FALLBACK: NVIDIA NIM nv-embed-v1 (4096-dim, network required)
- NEVER Anthropic for embeddings (user correction: "The only thing I was getting at was never use anthropic")
- ALL other providers are acceptable (Gemini, OpenAI, NVIDIA NIM, local models, any non-Anthropic provider)
- The rule is Anthropic-exclusion, NOT provider restriction
- All vectors truncated/padded to O'Keefe ec_dim (128)
- NEVER Anthropic for embeddings
- All other providers (Gemini, OpenAI, local) are acceptable

## Consolidation

A cron job runs `okeefe_bridge.py consolidate` every 4 hours. This is the
biological analog of sharp-wave ripple replay during rest, where memories
are strengthened and reorganized.

## CRITICAL PITFALL: NEVER Delete to Make Room

**User correction (2026-06-29):** "You shouldn't have just deleted something out of memory to add marketing. You're fucking with the memory way too much."

NEVER remove an existing memory entry from the the operator agent buffer to make room for new content. If the buffer is full (>90%), the correct response is:
1. Check if any existing entries are actually T2 content that was wrongly placed in T0. Migrate those to O'Keefe.
2. If still full, CONSOLIDATE existing T0 entries (make them shorter, merge related ones) — do NOT delete.
3. Only the user can authorize removing a T0 entry.

Destructive deletes lose important facts (TSC deadlines, phenotype specs, operator rules) that are expensive to rediscover. The entire point of the O'Keefe T2 layer is to make destructive deletes unnecessary.

## API Contract (verified live 2026-08-12 — POST-FIX)

The O'Keefe engine (:port) v1.1.0 accepts:

```
POST /encode
{"content": [floats], "location_vector": [floats], "reward": 0.5, "tags": ["tag1"], "text": "original content"}

POST /retrieve
{"cue": [floats], "n_results": 10}
```

**CRITICAL FIELD NAMES (v1.1.0):**
- `location_vector` NOT `location` (Pydantic silently drops unknown fields)
- `n_results` NOT `max_results` in /retrieve
- `text` field is REQUIRED for human-readable recall — without it, traces
  are vector husks with only tags visible

**PITFALL (2026-08-12 incident):** The bridge previously sent `location` and
`max_results`, which Pydantic silently dropped. Result: memories stored
without location context and retrieve always returned default 5 results.
Fixed in okeefe_bridge.py.

**PITFALL (2026-08-12 incident):** all-MiniLM-L6-v2 produces 384-dim vectors
but O'Keefe uses ec_dim=128. Truncating 384→128 destroys 67% of the semantic
signal, making pure-vector recall return near-random results (verified:
storing "Eiffel Tower" and recalling "Eiffel Tower" returned the wrong memory).
Fixed by adding hybrid retrieval: pull a wide candidate pool via CA3, then
re-rank by keyword overlap with the stored text (with simple stemming).
Keyword score dominates (60%) over semantic strength (40%) because the vector
signal is degraded.

**PITFALL (2026-08-12 incident):** A stale v1.0.0 process was running on
:port while v1.1.0 code was on disk. The old process had NO text field at
all — every memory was a vector husk. Health endpoint version string is
the diagnostic: v1.0.0 returns `status:"online"`, v1.1.0 returns
`status:"ok"`. After patching server.py, ALWAYS restart the process.

The bridge script (`okeefe_bridge.py`) wraps these calls with automatic
embedding generation. Use the bridge for convenience, but the raw API
contract above is the verified truth.

## Relationship to hermes-hippocampal-memory-architecture

This skill handles O'Keefe routing specifically. The broader 5-system
memory architecture (procedural, identity, episodic, working, semantic)
is documented in `hermes-hippocampal-memory-architecture`. Load both for
the complete picture. The hippocampal skill also covers the specialist
gate enforcement and boot hooks that protect procedural memory.

ALWAYS use "DS" before every engine name: "the specialist engine", not "Wernicke". This applies to ALL output.

The full rule (with tissue type accuracy, one-scientist-per-engine, anatomical reference precision, and architectural pattern guidance) lives in the `organism-biological-isomorphism-verification` skill. Load that skill for the complete isomorphism ruleset.

## Verification Protocol (Binding)

When sibling-agent or ANY operator claims work is done, VERIFY against real state before reporting to the user:
- Engine startup claimed? curl the /health endpoint
- Registry cleanup claimed? import FLEET_REGISTRY and check
- Bug fix claimed? reproduce the test case
- Code committed claimed? git log and check

Never report "done" without independent verification. The immune system (the specialist engine) exists for exactly this. Claims are cheap. Ports are truth. This is how we maintain world-class output quality.

## When This Skill Loads

Load this skill when:
- About to use the memory() tool — check if the content is T0 or T2 first
- Need to recall project state or domain knowledge from a previous session
- Setting up a new project that will generate durable facts
- The the operator agent buffer is getting full (>80%) and you need to offload
- ANY operator claims work is complete — verify before accepting

## Key Files

- Bridge: `/<workspace>`
- O'Keefe engine: :port (DS-ECS-CEL-04.07.06-v1.1.0)
- Embedding venv: `<agent-home>/venv-embed/`
- the operator agent config: `<agent-home>/config.yaml` (NVIDIA NIM credentials)
- Consolidation cron: every 4h (job 3a6a39963bd2)
