# Catalog-Lag Probe: verify a model ID before pinning it

## Principle

A provider's `/models` catalog is a cached advertisement, not a routing
table. It lags the endpoint: new models get served before the catalog lists
them, and catalog entries can outlive the hardware. The only proof a model ID
works is a minimal chat completion with that exact ID.

## Recipe (Python, stdlib only)

```python
import os, json, urllib.request

key = None
with open(os.path.expanduser("<agent-home>/.env")) as f:
    for ln in f:
        if ln.strip().startswith("GLM_API_KEY="):
            key = ln.strip().split("=", 1)[1].strip().strip('"').strip("'")

BASE = "https://api.z.ai/api/coding/paas/v4"

# 1) Catalog check (cheap, first pass)
req = urllib.request.Request(f"{BASE}/models",
    headers={"Authorization": f"Bearer {key}"})
with urllib.request.urlopen(req, timeout=30) as resp:
    ids = [m.get("id") for m in json.loads(resp.read().decode())["data"]]
print("catalog:", ids)

# 2) Chat probe (authoritative — run regardless of catalog result)
def probe(model):
    body = json.dumps({"model": model,
        "messages": [{"role": "user", "content": "reply with exactly: OK"}],
        "max_tokens": 10}).encode()
    req = urllib.request.Request(f"{BASE}/chat/completions", data=body,
        headers={"Authorization": f"Bearer {key}",
                 "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            d = json.loads(resp.read().decode())
            return f"served, echoed model: {d.get('model')}"
    except urllib.error.HTTPError as e:
        return f"HTTP {e.code}: {e.read().decode()[:200]}"

print(probe("glm-5.3"))
```

## Worked example (2026-08-14, llm-vendor coding endpoint)

- `/models` returned: glm-4.5, glm-4.5-air, glm-4.6, glm-4.7, glm-5,
  glm-5-turbo, glm-5.1, glm-5.2 — **no glm-5.3**
- Chat probe `glm-5.3`: 200 OK, response `model` field echoed `glm-5.3`
- Chat probe `glm-5.2`: 200 OK, but the response `model` field echoed
  **`glm-5.3`** — the provider was already routing 5.2 traffic to 5.3-class
  hardware. Catalog said one thing, routing said another.

Decision: pin `glm-5.3` as a real served ID; trust the probe over the list.

## Cross-provider check for fallback entries

Before bumping a `fallback_providers[]` entry, query THAT provider's own
catalog with THAT provider's key. Same model family, different namespaces:

| Provider | Catalog (2026-08-14) | Notes |
|----------|---------------------|-------|
| llm-vendor direct (`api.z.ai/api/coding/paas/v4`) | serves glm-5.3 (probe-verified) | catalog omits it |
| nvidia-nim (`integrate.api.nvidia.com/v1`) | `z-ai/glm-5.2` only | do NOT bump to 5.3 — breaks fallback |
| OpenRouter (`openrouter.ai/api/v1`) | up to `z-ai/glm-5.2` (+ `:batch`) | lags llm-vendor by one release |

Bumping a fallback to an ID its provider doesn't serve makes the fallback
dead weight that only surfaces during a real outage — the worst time to
discover it.
