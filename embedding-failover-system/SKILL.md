---
name: Embedding Failover System
description: Local + OpenRouter embedding support with automatic failover, Intel Mac compatible
tags: [embeddings, local-ml, openrouter, failover, cpu]
tools: [terminal, file]
---

## Rules

- **NEVER use Anthropic for embeddings.** Gemini, OpenAI, NVIDIA NIM, local models
  are all fine. The exclusion is Anthropic-specific (user clarification 2026-06-29).
  The original "Gemini or OpenAI only" rule was TOO RESTRICTIVE — the actual rule
  is "never Anthropic, everything else is acceptable."
- **NVIDIA NIM (nv-embed-v1)** is a reliable embedding provider when local
  sentence-transformers is broken. Available via nvidia-nim config in
  `<agent-home>/config.yaml`. 4096-dim vectors. Tested and working 2026-06-29.
- **DS O'Keefe (:port)** is the organism's hippocampal memory engine. It stores
  traces as numeric vectors. To store TEXT facts: embed the text first, then
  POST /encode with the embedding vector as `content`. The translation layer is
  text -> embedding -> O'Keefe vector trace.
- Local venv may break (PyTorch/NumPy version conflicts). Always have a remote
  fallback configured (NVIDIA NIM, OpenRouter, or Gemini).

## Architecture

**Primary: Local sentence-transformers** — free forever, no API
- Venv: `<agent-home>/venv-embed` (dedicated Python env, doesn't interfere with system)
- Model: `all-MiniLM-L6-v2` (80MB, auto-downloaded on first use)
- Performance: ~10ms per embedding on Intel i7-9750H (CPU only)
- Works on both Intel and Apple Silicon Macs

**Fallback: OpenRouter free embedding** — unlimited quality backup
- Model: `nomic-ai/nomic-embed-text-v1.5:free` (768-dim, 8192 context)
- Uses existing OPENROUTER_API_KEY
- Always available as long as OpenRouter is up

**Also available: NVIDIA NIM** (tested working 2026-06-29)
- Model: `nvidia/nv-embed-v1` (4096-dim)
- Uses nvidia-nim provider config (base_url + api_key)
- POST to {base_url}/embeddings with input_type "query"

**CRITICAL RULE: NEVER use Anthropic for embeddings.** This is the ONLY hard
provider exclusion. Gemini, OpenAI, NVIDIA NIM, local models, ZAI, and any
other non-Anthropic provider are ALL fine.
User correction (2026-06-29): "The only thing I was getting at was to never
use Anthropic."

## Setup

### 1. Create dedicated venv
```bash
python3.11 -m venv <agent-home>/venv-embed
```

### 2. Install CPU-only torch (Intel Mac)
```bash
<agent-home>/venv-embed/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu
```
For Apple Silicon: just `pip install torch` (gets MPS acceleration)

### 3. Install sentence-transformers
```bash
<agent-home>/venv-embed/bin/pip install sentence-transformers
```

### 4. Verify
```bash
<agent-home>/venv-embed/bin/python -c "from sentence_transformers import SentenceTransformer; m = SentenceTransformer('all-MiniLM-L6-v2')"
```

## Usage

```python
from importlib.machinery import SourceFileLoader
ef = SourceFileLoader("embed", "/<workspace>").load_module()

# Single text
vector = ef.embed_single("text to embed")  # Returns list[float]

# Multiple texts
result = ef.embed(["text1", "text2"])  # Returns dict with _source field
```

## Files

- `<agent-home>/embedding-failover.py` — Failover orchestration
- `<agent-home>/venv-embed/` — Dedicated embedding environment

## Troubleshooting

**torch install fails with 'externally managed':**
→ Use dedicated venv, don't use --system flag

**Import timeout on first run:**
→ Normal — torch is large and first import is slow. Subsequent imports are fast.

**Model download stuck:**
→ sentence-transformers auto-downloads on first use. May need internet access.

## Key facts
- Intel Mac: CPU only, ~10ms per embedding
- venv-embed is separate from the operator agent agent environment to avoid dependency conflicts
- Local never costs anything, never rate limits, never 403s
- Fallback to OpenRouter is automatic — no manual intervention needed
- FIXED (2026-06-29): local venv PyTorch/NumPy conflict resolved by pinning
  `numpy<2` (1.26.4) and `sentence-transformers<3.0` (2.7.0). torch 2.2.2
  stays (torch>=2.4 not available for this Python/platform on CPU index).
  Local embeddings confirmed working: 384-dim all-MiniLM-L6-v2.
  Fix command: `<agent-home>/venv-embed/bin/pip install "numpy<2" "sentence-transformers<3.0"`
- O'Keefe hippocampus (:port) uses vectors via /encode endpoint. The embedding
  translation layer (text -> vector -> O'Keefe) is the bridge for the 4-tier
  memory architecture. Tested working with NVIDIA NIM vectors.