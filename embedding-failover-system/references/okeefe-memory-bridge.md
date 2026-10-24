# O'Keefe Memory Bridge — Text-to-Hippocampus Translation

## What This Is

The translation layer between text facts and DS O'Keefe's vector-based
hippocampal memory store. Located at:
`~/your-workspace/marketing-consortium/src/okeefe_bridge.py`

## How It Works

```
Text fact → NVIDIA NIM embed (4096-dim) → truncate to 128 → O'Keefe /encode
                                                              ↓
Query text → NVIDIA NIM embed (4096-dim) → truncate to 128 → O'Keefe /retrieve
                                                              ↓
                                                    Returns text + strength + tags
```

## Usage

```python
# Store a fact
from okeefe_bridge import store, recall, health

result = store(
    "Marketing consortium v1.0.0 at marketing-consortium/ — 23 files, git committed",
    tags=["marketing", "project_state"],
    reward=0.8
)
# Returns: {"trace_id": "mem_0.000_...", "memory_count": N}

# Recall by semantic query
memories = recall("marketing project status")
# Returns: [{"text": "...", "strength": 0.50, "tags": [...]}]
```

## CLI

```bash
python3 okeefe_bridge.py health                    # Check O'Keefe
python3 okeefe_bridge.py store "text" "tag1,tag2" 0.8  # Store
python3 okeefe_bridge.py recall "query"            # Recall
python3 okeefe_bridge.py list                       # List all
python3 okeefe_bridge.py consolidate                # Run consolidation
```

## Verified Working (2026-06-29)

- Store: encoded marketing project state, received trace_id
- Recall: queried "marketing project status", got correct text back at strength 0.50
- O'Keefe v1.1.0 with ec_dim=128, text metadata field, cognitive layer

## Provider

NVIDIA NIM (nv-embed-v1, 4096-dim). NEVER Anthropic. Config in
`<agent-home>/config.yaml` under `providers.nvidia-nim`.

## Related

- O'Keefe engine: :port, DS-ECS-CEL-04.07.06-v1.1.0
- Design docs: `docs/hippocampus-engine-design/`
- State file: `<agent-home>/state/okeefe_memory.json`
- Full memory architecture: see `hermes-memory-quality-audit` skill
