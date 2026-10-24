# the specialist engine Maintenance Procedures

## Layer 4 Methodology Fix Procedure

When DS engines return empty `{}` on `/v1/layers` endpoint due to incorrect mounting of methodology endpoints:

### Root Cause
The `mount_methodology_endpoints(app, ...)` call is placed BEFORE `app = FastAPI(...)`, causing a syntax error or premature execution before the FastAPI app is fully configured.

### Fix Pattern
Move the methodology mounting block to AFTER app creation:

```python
# BEFORE (INCORRECT):
app = FastAPI(
    from methodology_api import mount_methodology_endpoints  # SYNTAX ERROR
    mount_methodology_endpoints(app, "engine-name", "module")  # SYNTAX ERROR
    title="the specialist engine",
    version="1.0.0",
)

# AFTER (CORRECT):
app = FastAPI(
    title="the specialist engine",
    version="1.0.0",
    description="Engine description",
)

# Layer 4: Methodology API - MOVED HERE
import sys as _sys, os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(__file__), "..", "..", "..", "ds-engine-shared"))
try:
    from methodology_api import mount_methodology_endpoints
    mount_methodology_endpoints(app, "engine-name", "module")
except Exception:
    pass  # graceful degradation
```

### Verification Script
Use `fix_layer4_final.py` to automate the fix across multiple engines:
- Locates the auto-wired Layer 4 block (try/except with mount_methodology_endpoints)
- Moves it to after `app = FastAPI(...)`
- Preserves `__future__` imports at top of file
- Validates syntax after changes

### Restart Procedure
1. Kill existing process: `lsof -ti :<port> | xargs kill -9 2>/dev/null || true`
2. Start engine: `cd <engine_dir> && source venv/bin/activate && nohup python -m uvicorn src.api.server:app --host 127.0.0.1 --port <port> > /dev/null 2>&1 &`
3. Wait 3-5 seconds for startup
4. Verify: `curl -s http://127.0.0.1:<port>/v1/layers` returns populated JSON

### Engine List (22 engines requiring Layer 4 fix)
- ds-genesis-engine (genesis)
- ds-quartz-engine (quartz)
- ds-allostasis-engine (allostasis)
- ds-morphogen-engine (morphogen)
- ds-beaumont-engine (beaumont)
- ds-self-healing-engine (self_healing)
- ds-haldane-engine (haldane)
- ds-sutherland-engine (sutherland)
- ds-burnet-engine (burnet)
- ds-hill-engine (hill)
- ds-helmholtz-engine (helmholtz)
- ds-organism-scanner-engine (organism_scanner)
- ds-tech-currency-engine (tech_currency)
- ds-lovelace-engine (lovelace)
- ds-audio-input-engine (audio_input)
- ds-text-vision-input-engine (text_vision_input)
- ds-speech-synthesis-engine (speech_synthesis)
- ds-system-state-sensor-engine (system_state_sensor)
- ds-environmental-monitor-engine (environmental_monitor)
- ds-nervous-system-engine (nervous_system)
- ds-wave-engine (wave)
- ds-ecs-compliance-engine (ecs_compliance)

### Working Engines (Do NOT modify)
These 16 engines already work correctly:
- ds-reproductive-engine
- ds-harvey-engine
- ds-bright-engine
- ds-unna-engine
- ds-creative-cortex-engine
- ds-clinical-engine
- ds-da-vinci-engine
- ds-goethe-engine
- ds-bell-engine
- ds-luria-engine
- ds-sperry-engine
- ds-wernicke-engine
- ds-maclean-engine
- ds-ito-engine
- ds-gazzaniga-engine
- ds-tawara-engine

### Safety Checks
- Always backup first: `cp src/api/server.py src/api/server.py.bak`
- Verify syntax after changes: `python3 -c "compile(open('server.py').read(), 'server.py', 'exec')"`
- Confirm no regression in other layers (1,2,3) still return data
- Test in small batches (3-5 engines at a time)