# Fleet-Wide Layer Propagation — Layer 5 (Philosophy) Rollout

**Session:** 2026-06-18
**Task:** Build Layer 5 (Philosophy Engine) for all 40 DS engines
**Result:** 40/40 engines live with all 5 layers, 480 philosophies total

## The 5-Layer Engine Architecture

Every DS engine has 5 layers, each mounted as API endpoints:

| Layer | Name | Purpose | Shared Library |
|-------|------|---------|----------------|
| 1 | Physics Layer 1 | Domain-specific physics (e.g., "Double-Helix Encoding") | Per-engine `_get_physics_layers()` |
| 2 | Physics Layer 2 | Second physics domain | Per-engine `_get_physics_layers()` |
| 3 | Physics Layer 3 | Third physics domain | Per-engine `_get_physics_layers()` |
| 4 | Methodology Engine | Institutions, methodologies, personalities, sub-agents, model routes | `ds-engine-shared/methodology_base.py` + `methodology_api.py` |
| 5 | Philosophy Engine | 12 philosophies (2 per source type), 8 wisdom principles | `ds-engine-shared/philosophy_base.py` + `philosophy_api.py` |

Layer 5 source types (always 2 each = 12 total):
- contemplative (Buddhist, Taoist, Zen)
- indigenous (Maori, Andean, Aboriginal, Native American)
- artistic (Wabi-sabi, Bauhaus, Surrealism)
- counter_cultural (Hacker ethos, punk, DIY, open source)
- scientific (cybernetics, systems thinking, complexity)
- academic (Aristotle, Kant, pragmatism, phenomenology)

## Fleet-Wide Layer Propagation Pattern

This is a recurring workflow: any time a new layer is added to the architecture,
it must be propagated to all engines. The pattern:

### Step 1: Build the Shared Library
Create `<layer>_base.py` (data classes + base layer) and `<layer>_api.py`
(endpoint mounter) in `ds-engine-shared/`.

### Step 2: Wire Into the Existing Layer Below
Modify the shared mount function to auto-detect the new layer. For Layer 5,
`methodology_api.py`'s `mount_methodology_endpoints()` now tries to import
`philosophy_api` and auto-mounts it. The `/v1/layers` endpoint passes the
philosophy layer to `get_layer_summary(philosophy_layer=_philosophy)`.

### Step 3: Generate Per-Engine Files
Write a generator script that reads each engine's metadata (body_system,
dimension, engine_name from its `methodology.py`) and generates a themed
`<layer>.py` file at `src/<module>/core/<layer>.py`.

### Step 4: Restart and Verify
Restart all engines, then query `/v1/layers` on every port. Build a port map
from stderr logs (look for `127.0.0.1:NNNN` or `0.0.0.0:NNNN` patterns).

### Step 5: Fix Edge Cases
Always expect engines with custom/hardcoded endpoints that bypass shared mounts.

## Pitfalls Discovered

### 1. `str(Bool).lower()` produces JavaScript-style booleans
**Bug:** Code generator used `str(phil['is_university_derived']).lower()` which
produces `false`/`true` in Python — but these are NOT Python keywords. The
generated files had `is_university_derived=false` which crashes at import.

**Fix:** Use `str(phil['is_university_derived'])` directly (Python prints `True`/`False`),
or better: write the boolean literal directly.

### 2. `import importlib.util` shadows module-level import
**Bug:** In `philosophy_api.py`, the except block did `import importlib.util`
which created a local binding that shadowed the module-level `import importlib`.
When the except block tried to use `importlib.util.spec_from_file_location()`,
it failed with `UnboundLocalError: cannot access local variable 'importlib'`.

**Fix:** Move `import importlib.util` to the top of the file alongside `import importlib`.

### 3. Engines with custom `/v1/layers` bypass shared auto-mount
**Bug:** the specialist engine had its own `get_layer_summary()` method (not inherited from
`MethodologyLayerBase`) that didn't accept the `philosophy_layer` kwarg.
the specialist engine-Coaching had a compatibility shim `server.py` → `src/server/api.py`
with a `sys.path.insert` that went 4 levels up instead of 3.

**Fix:** For each engine with a custom endpoint:
- Add `philosophy_layer=None` parameter to its `get_layer_summary()`
- Add `if philosophy_layer: result["layer_5"] = ...` to the return
- Ensure `ds-engine-shared` is on `sys.path` (count `../` carefully)

### 4. Path resolution: count `../` carefully
Multiple engines had wrong `sys.path` depth to find `ds-engine-shared`:
- Harvey: missing entirely (had `ds-engine-registry` but not `ds-engine-shared`)
- Wave-Coaching: `"..", "..", "..", ".."` (4 levels) should be 3 from `src/server/api.py`

**Verification:** The correct path from `src/api/server.py` is 3 `../` to reach
the workspace root. From `src/server/api.py` it's also 3. Always verify by
checking `os.path.exists()` on the resolved path.

### 5. Port detection confusion
Engines bind to `0.0.0.0:NNNN` or `127.0.0.1:NNNN` inconsistently. Some engines
(the specialist engine) were on a different port than expected (8121, not 8104).

**Fix:** Read stderr logs for the `Uvicorn running on http://...` line to get
the actual port. Try both `127.0.0.1` and `0.0.0.0` when curling.

## Verification Script Pattern

```python
# Scan all engines for layer presence
for engine_dir in glob.glob(f"{base}/ds-*-engine"):
    log = f"{engine_dir}/logs/launchd-stderr.log"
    if os.path.exists(log):
        content = open(log).read()
        ports = re.findall(r'(?:127\.0\.0\.1|0\.0\.0\.0)[:.](\d{4,5})', content)
        if ports:
            port = int(ports[-1])
            resp = curl(f"http://127.0.0.1:{port}/v1/layers")
            layers = json.loads(resp)
            has_5 = "layer_5" in layers
            # If not, try 0.0.0.0
```

## Domain Theme Mapping

Engines were grouped by body_system for themed philosophy content:

| Theme | Count | Example Engines |
|-------|-------|-----------------|
| creative_cognition | 12 | Bell, Creative Cortex, Design, Goethe, Lovelace |
| _default | 9 | Beaumont, Bright, Burnet, Haldane, Harvey |
| sensory | 4 | Audio Input, Environmental Monitor, Speech Synthesis |
| creation | 4 | Genesis, Maturation, Placenta, Reproductive |
| clinical | 2 | Clinical, Organism Scanner |
| emotional | 2 | Maclean, Wave Coaching |
| healing | 2 | Morphogen, Self-Healing |
| homeostasis | 1 | Allostasis |
| protection | 1 | Quartz |
| vocational | 1 | Tech Currency |

Currently most themes use the `_default` template. Future work: write domain-specific
philosophy content for each theme so each engine's philosophies are genuinely unique
to its function rather than generic.
