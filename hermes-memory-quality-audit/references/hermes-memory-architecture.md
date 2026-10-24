# the operator agent Agent Memory Architecture (v0.16+)

Source: the operator agent Agent docs (memory.md, memory-providers.md, configuration.md), GitHub issues #346, #509, AGENTS.md, community guides.

---

## 1. Built-In Core Memory (Always Active)

### Files
| File | Path | Purpose | Char Limit | Token Est. |
|------|------|---------|------------|------------|
| `MEMORY.md` | `<agent-home>/memories/MEMORY.md` | Agent's notes: environment facts, conventions, learned procedures | 2,200 | ~800 |
| `USER.md` | `<agent-home>/memories/USER.md` | User profile: preferences, communication style, expectations | 1,375 | ~500 |

### Config (config.yaml)
```yaml
memory:
  memory_enabled: true           # Enable MEMORY.md
  user_profile_enabled: true     # Enable USER.md
  memory_char_limit: 2200        # ~800 tokens
  user_char_limit: 1375          # ~500 tokens
  write_approval: false          # false = agent writes freely; true = require approval
```

### Behavior
- **Immediate persistence**: Changes written to disk instantly during session
- **Next-session injection**: Updated content appears in system prompt on `/reset` or new session
- **No mid-session update**: Prompt caching means changes don't affect current conversation
- **Delimiter-separated**: Entries separated by `---` (flat structure, no metadata)
- **Agent-curated pruning**: When at limit, agent must consolidate/replace entries

### Profile Isolation
Each profile (`<agent-home>/profiles/<name>/`) has its own `memories/` directory with independent `MEMORY.md`/`USER.md`.

---

## 2. Session Search (Separate from Memory)

### Storage
- `<agent-home>/state.db` — SQLite + FTS5
- Per-session JSONL transcripts in `<agent-home>/sessions/`
- Optional JSON snapshots if `sessions.write_json_snapshots: true`

### Retrieval
- Tool: `session_search` (FTS5-backed)
- Slash: `/history`, `/sessions browse`
- CLI: `hermes sessions list/export/browse`
- **Not injected in system prompt** — on-demand tool only

### Key Distinction
> "Session search is not memory." — the operator agent docs
- Memory = curated, bounded, always-injected facts
- Session search = raw conversation history, unbounded, tool-retrieved

---

## 3. External Memory Providers (Pluggable, One at a Time)

### Activation
```bash
hermes memory setup          # Interactive picker
hermes config set memory.provider honcho  # Manual
```

### Providers Shipped (8)
| Provider | Package | Config Location | Notes |
|----------|---------|-----------------|-------|
| Honcho | `hermes-honcho` | `plugins.hermes-memory-store` | Dialectic user modeling, scopes |
| Mem0 | `hermes-mem0` | `plugins.hermes-memory-store` | Scoped extraction pipeline |
| Hindsight | `hermes-hindsight` | `plugins.hermes-memory-store` | Semantic recall, cloud |
| Holographic | `hermes-holographic` | `plugins.hermes-memory-store` | Graph-based |
| ByteRover | `hermes-bytterover` | `plugins.hermes-memory-store` | Hierarchical Context Tree, AKL |
| RetainDB | `hermes-retaindb` | `plugins.hermes-memory-store` | 7 memory types, hybrid search |
| OpenViking | `hermes-openviking` | `plugins.hermes-memory-store` | Simple, free |
| Supermemory | `hermes-supermemory` | `plugins.hermes-memory-store` | Free tier, hybrid |

### Provider Behavior
- **Context injection**: Provider context injected into system prompt (what provider knows)
- **Prefetch**: Relevant memories prefetched per turn
- **Tools exposed**: Provider-specific tools (e.g., `memori_recall`, `honcho_peer`)
- **Profile-scoped**: Config in `$HERMES_HOME/` so each profile has own credentials

### Honcho-Specific (Most Relevant for Preference Evolution)
```yaml
# Config via hermes memory setup honcho or config.yaml
honcho:
  observation: directional
  peer_name: ""
  contextCadence: 10        # API call frequency
  dialecticCadence: 5       # LLM dialectic frequency
  dialecticDepth: 2         # Chat passes per dialectic (1-3)
  recallMode: hybrid        # hybrid/context/tools
  tokenBudget: 4000         # Context + dialectic tokens
```

---

## 4. Current Limitations (Gap vs. Best Practices)

| Limitation | Impact | Tracking |
|------------|--------|----------|
| **Flat delimiter entries** | No metadata, no types, no provenance | Issue #346 |
| **No conflict detection** | Contradictions accumulate | Issue #509 (cognitive layer) |
| **No recency decay** | Stale entries displace current | Manual audit only |
| **No domain scoping** | All memories injected globally | Provider-dependent |
| **No confidence scoring** | All entries treated equal | Not implemented |
| **Write approval off by default** | Noise accumulation risk | Config option exists |
| **Char limits fixed** | Forces lossy compression | Configurable but hard cap |
| **Session search separate** | Conversational context not auto-curated | Manual `/compress` or skills |

---

## 5. Key Commands for Audit

```bash
# View memory files
cat <agent-home>/memories/MEMORY.md
cat <agent-home>/memories/USER.md

# Check config
hermes config check | grep -A10 "memory:"

# Provider status
hermes memory status

# Session search test
hermes chat -q "Search sessions for 'pytest-xdist'"

# Recall test
hermes chat -q "What is my preference for technical responses?"
```

---

## 6. Config Tuning Recommendations

### With No Provider (Current Default)
```yaml
memory:
  memory_enabled: true
  user_profile_enabled: true
  memory_char_limit: 1800      # Stricter curation
  user_char_limit: 1100
  write_approval: true         # Gate noise
```

### With Honcho Active
```yaml
memory:
  memory_enabled: true
  user_profile_enabled: true
  memory_char_limit: 1500      # Provider handles deep memory
  user_char_limit: 1000
  write_approval: true
  provider: honcho
```

---

## 7. References

- Docs: https://hermes-agent.nousresearch.com/docs/user-guide/features/memory/
- Providers: https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers/
- Issue #346: https://github.com/NousResearch/hermes-agent/issues/346
- Issue #509: https://github.com/NousResearch/hermes-agent/issues/509
- AGENTS.md: https://github.com/NousResearch/hermes-agent/blob/main/AGENTS.md