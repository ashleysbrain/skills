# the operator agent Agent Import Troubleshooting Guide

This guide provides solutions for common import errors, circular imports, and path-related issues encountered when working with the operator agent agents (engine services).

## Common Issues and Solutions

### 1. Incorrect Path Calculations in Core Modules
When an engine's `core.py` tries to import from the shared `ds-engine-registry/ecs.py`, the path calculation is often wrong.

**Problem Pattern**:
```python
# Wrong - too few ".." to reach workspace root
_REGISTRY_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "ds-engine-registry")
)
```

**Fix**:
```python
# Correct - add appropriate number of ".." to reach workspace root
# From src/ecs_compliance/core.py: need 4 ".." to reach /<workspace>
_REGISTRY_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "ds-engine-registry")
)
```

### 2. Circular Imports in `__init__.py`
When `core/__init__.py` tries to import from `core` (itself) or creates circular dependencies.

**Problem Pattern**:
```python
# Creates circular import
from .core import *  # When core/__init__.py is in core/ directory
```

**Fix Options**:

**Option A: Import from sibling core.py**
```python
# In core/__init__.py - import from the actual core.py file
from ..core import (  # noqa: F401
    AGENT_PERSONA,
    ENGINE_CODE,
    # ... other exports
)
```

**Option B: Use importlib to load core.py directly**
```python
# In core/__init__.py - avoid relative imports entirely
import importlib.util
import os
core_py_path = os.path.join(os.path.dirname(__file__), '..', 'core.py')
spec = importlib.util.spec_from_file_location("core_module", core_py_path)
core_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core_module)

# Export what's needed
from core_module import (
    AGENT_PERSONA,
    ENGINE_CODE,
    # ... other exports
)
```

### 3. Future Import Placement in server.py
Future imports (`from __future__ import annotations`) must be at the very top of the file.

**Problem Pattern**:
```python
# Wrong - future import not at top
some_code_here()
from __future__ import annotations  # SYNTAX ERROR
```

**Fix**:
```python
# Correct - future import at absolute top
from __future__ import annotations

import os
import sys
# ... rest of imports
```

### 4. Import Order Issues
Mixing local imports with standard/library imports can cause issues.

**Recommended Order**:
```python
# 1. Future imports (must be first)
from __future__ import annotations

# 2. Standard library imports
import os
import sys
import json
# ... etc

# 3. Third-party imports
import requests
import uvicorn
# ... etc

# 4. Local application imports
# Add paths to sys.path FIRST if needed
sys.path.insert(0, '/path/to/workspace')

# Then import local modules
from ecs = FLEET_REGISTRY  # from ds-engine-registry
from .core = engine  # local to this package
```

## Verification Steps

After making fixes, verify with:

```bash
# 1. Test core module imports directly
python3 -c "
import sys
sys.path.insert(0, '/path/to/agent/src')
sys.path.insert(0, '/path/to/workspace')  # for ecs import
from ecs_compliance.core = engine, AGENT_PERSONA
print(f'✅ Import successful: {AGENT_PERSONA} on port {engine.port}')
"

# 2. Test server.py imports without starting server
python3 -c "
import sys
sys.path.insert(0, '/path/to/agent/src')
from ecs_compliance.api.server = app
print(f'✅ Server import successful: {app.title}')
"

# 3. Check for syntax errors
python3 -m py_compile /path/to/agent/src/ecs_compliance/core.py
python3 -m py_compile /path/to/agent/src/api/server.py

# 4. Verify engine instantiation works
python3 -c "
import sys
sys.path.insert(0, '/path/to/agent/src')
sys.path.insert(0, '/path/to/workspace')
from ecs_compliance.core = engine
print(f'✅ Engine created: {engine.engine_name}')
print(f'   Port: {engine.port}')
print(f'   Scientist: {engine.scientist}')
"
```

## Engine-Specific Notes

- **ECS Compliance (the specialist engine)**: Fixed by correcting path calculations (4 dots → 3 dots) and fixing future import placement
- **Reproductive Engine**: Similar path issues - often mounts methodology before app creation
- **Clinical Engine**: Similar import structure issues
- **General Pattern**: Most DS engines follow the same core.py/server.py structure

## Prevention Tips

1. **Always backup first**: `cp src/api/server.py src/api/server.py.bak`
2. **Make one change at a time**: Fix imports, test, then fix mounting, test, etc.
3. **Use existing working engines as reference**: Compare with Quartz or Allostasis engines
4. **Test imports before restarting**: Don't restart the engine service until imports work in Python
5. **Check line numbers in error messages**: Python tracebacks often point to the exact problematic line