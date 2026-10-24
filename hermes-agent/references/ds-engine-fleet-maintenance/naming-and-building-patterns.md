# the specialist engine Conventions and Building Patterns

## Naming Convention Preference
As established in session, when referring to Divinity Science (DS) engines in verbal/written communication:
- Use only the scientist names as a "tip of the hat" (e.g., the specialist engine, the specialist engine, the specialist engine)
- Do not append functional descriptions like "(Genome)", "(Placenta)", or "(Maturation)"
- The functional roles are encoded in the ECS registry and engine metadata

**Correct**: "the specialist engine is running on port 8129"
**Incorrect**: "the specialist engine (Genome) is running on port 8129"

## Building New the specialist engine: Complete Pattern

### Directory Structure
```
ds-<engine-name>-engine/
├── run_server.py
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── server.py
│   └── <engine>/  # e.g., placenta
│       ├── __init__.py
│       └── core/
│           ├── __init__.py
│           ├── engine.py
│           └── methodology.py
├── VERSION.md
├── logs/  # (created after first run)
└── ~/Library/LaunchAgents/com.divinityscience.<engine>.plist
```

### Core File Specifications

#### 1. `run_server.py`
```python
import uvicorn
from src.api.server import app

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=<PORT_NUMBER>)
```

#### 2. `requirements.txt`
```
fastapi
uvicorn
pydantic
numpy<2
```

#### 3. `src/<engine>/core/engine.py`
```python
from dataclasses import dataclass, field
import time
from typing import Dict, Any
import PHI  # golden ratio constant from shared location

@dataclass
class <EngineNamePascalCase>Engine:
    organ_name: str = "<Engine Name>"
    function: str = "<Engine function description>"
    port: int = <PORT_NUMBER>
    scientist: str = "<Scientist Name>"
    body_system: str = "<body system>"
    # ... other engine-specific fields
    
    # Engine state tracking
    _initialized_at: float = field(default_factory=time.time)
    _operations: int = 0
    
    def get_vitals(self) -> Dict[str, Any]:
        """Return engine vitals for /health and /v1/vitals."""
        import time
        uptime = time.time() - self._initialized_at
        return {
            "engine_name": self.organ_name,
            "status": "ok",
            "port": self.port,
            "body_system": self.body_system,
            "scientist": self.scientist,
            "function": self.function,
            # ... engine-specific vitals
            "uptime_seconds": round(uptime, 1),
            "operations": self._operations,
            # ... other metrics
        }
    
    # ... engine-specific methods (e.g., route_dna, record_milestone, etc.)

# Singleton instance
_engine = <EngineNamePascalCase>Engine()
```

#### 4. `src/<engine>/core/methodology.py`
```python
"""Layer 4: Methodology for <Engine Name>"""

# Institutions (8 total - examples)
INSTITUTIONS = [
    "<Institution 1>",
    "<Institution 2>",
    "<Institution 3>",
    "<Institution 4>",
    "<Institution 5>",
    "<Institution 6>",
    "<Institution 7>",
    "<Institution 8>",
]

# Methodologies (7 total)
METHODOLOGIES = [
    "<Methodology 1>",
    "<Methodology 2>", 
    "<Methodology 3>",
    "<Methodology 4>",
    "<Methodology 5>",
    "<Methodology 6>",
    "<Methodology 7>",
]

# Model Routes (8 total)
MODEL_ROUTES = {
    "primary": "llm-vendor/glm-5.2",
    "technical": "deepseek/deepseek-v3", 
    "creative": "xai/grok-4",
    # ... additional routes
}

# Personalities (10 total)
PERSONALITIES = [
    "<Personality 1>",
    "<Personality 2>",
    "<Personality 3>",
    "<Personality 4>",
    "<Personality 5>",
    "<Personality 6>",
    "<Personality 7>",
    "<Personality 8>",
    "<Personality 9>",
    "<Personality 10>",
]

def create_methodology_layer():
    """Create and return the methodology layer."""
    return {
        "institutions": INSTITUTIONS,
        "methodologies": METHODOLOGIES,
        "model_routes": MODEL_ROUTES,
        "personalities": PERSONALITIES,
    }
```

#### 5. `src/api/server.py`
```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from ..<engine>.core.engine import _engine
from ..<engine>.core.methodology import create_methodology_layer
from methodology_api import mount_methodology_endpoints

app = FastAPI(
    title="DS <Engine Name>",
    version="1.0.0",
    description="<Engine description>",
)

# Health endpoint
@app.get("/health")
async def health():
    return JSONResponse(content=_engine.get_vitals())

# Vitals endpoint
@app.get("/v1/vitals")
async def vitals():
    return JSONResponse(content=_engine.get_vitals())

# Engine-specific endpoints (examples)
# @app.post("/v1/route-dna")
# async def route_dna(request: Request):
#     # ... implementation
#     return JSONResponse(content={"status": "success"})

# Mount methodology endpoints (MUST come AFTER app creation)
mount_methodology_endpoints(app, "<engine-key>", "<engine>")
```

#### 6. `VERSION.md`
```
# DS <Engine Name> Engine

## Version 1.0.0

Initial release of the DS <Engine Name> engine.
```

#### 7. Launchd Plist: `~/Library/LaunchAgents/com.divinityscience.<engine>.plist`
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.divinityscience.<engine></string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>/<workspace><engine>-engine/run_server.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>WorkingDirectory</key>
    <string>/<workspace><engine>-engine</string>
    <key>StandardOutPath</key>
    <string>/<workspace><engine>-engine/logs/out.log</string>
    <key>StandardErrorPath</key>
    <string>/<workspace><engine>-engine/logs/err.log</string>
</dict>
</plist>
```

## ECS Registry Fix: Critical Import Pattern

When adding a new engine to `ds-engine-registry/ecs.py`, you MUST update BOTH the `_C` dict AND the `FLEET_REGISTRY`:

### Step 1: Add to `_C` dict (PREVENTS KeyError on import)
```python
# At the top of ecs.py, in the _C dict:
_C = {
    # ... existing entries
    "<engine-key>": _code(2, 10, <sequence-number>),  # e.g., "genome": _code(2, 10, 1)
    # ... other entries
}
```

### Step 2: Add to `FLEET_REGISTRY` (defines the engine)
```python
# In the FLEET_REGISTRY dict:
FLEET_REGISTRY = {
    # ... existing entries
    "ds-<engine>-engine": _entry(
        key="<engine-key>",
        directory="ds-<engine>-engine",
        name="DS <Engine Name>",
        port=<PORT_NUMBER>,
        scientist="<Scientist Full Name>",
        body_system="<body system>",
        cognitive_layer=<true/false>,
        description="<Engine description>",
        dependencies=_deps("<dependency1>", "<dependency2>", ...),
        extra={"role": "<engine-role>", "subsystem_label": "<label>"}
    ),
    # ... other entries
}
```

### Verification
After making both changes, verify clean import:
```bash
python3 -c "
import sys
sys.path.insert(0, '/<workspace>')
from ecs import FLEET_REGISTRY
active_engines = {k:v for k,v in FLEET_REGISTRY.items() if not v.get('renamed_to')}
print(f'Total active engines: {len(active_engines)}')
# Check your engine is present
engine = active_engines.get('ds-<engine>-engine')
if engine:
    print(f'✅ {engine[\"engine_name\"]} found on port {engine[\"port\"]}')
else:
    print('❌ Engine not found in registry')
"
```

## Troubleshooting Common Issues

### Symptom: `KeyError: '<engine-key>'` when importing ecs
**Cause**: Engine key added to `FLEET_REGISTRY` but not to `_C` dict
**Fix**: Add the engine key to `_C` dict using `_code(2, 10, <sequence>)`

### Symptom: Engine fails to start or returns empty `{}` on `/v1/layers`
**Cause**: `mount_methodology_endpoints` called before `app = FastAPI()`
**Fix**: Move the mount call to AFTER app creation in `src/api/server.py`

### Symptom: Voice note transcription slow or timing out
**Cause**: Using default Whisper model (large) on CPU
**Fix**: Use `--model tiny` for faster transcription:
```bash
whisper --model tiny --language en --output_format txt --output_dir /tmp/whisper_out /path/to/audio.ogg
```