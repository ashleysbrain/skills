# Recovering Destroyed Python Source from .pyc Cache

When a Python source file has been overwritten, truncated, or destroyed but the
compiled `.pyc` in `__pycache__/` still exists, you can recover the module's
data (and reconstruct source) by loading the bytecode directly.

## When to Use

- Source file size dropped dramatically (e.g., 112KB → 694 bytes) with no git history
- `.pyc` in `__pycache__/` is newer or larger than the `.py` file
- No git, no backup, but `__pycache__` survived

## The Technique

```python
import sys, json
import importlib.util, importlib.machinery

# 1. Load the .pyc as a sourceless module
loader = importlib.machinery.SourcelessFileLoader(
    'module_name',
    '/path/to/__pycache__/module_name.cpython-311.pyc'
)
spec = importlib.util.spec_from_loader('module_name', loader)
mod = importlib.util.module_from_spec(spec)

# 2. CRITICAL: register in sys.modules BEFORE exec_module
#    Without this, dataclass decorators fail because they look up
#    sys.modules[cls.__module__] to resolve type annotations.
sys.modules['module_name'] = mod
loader.exec_module(mod)

# 3. Dump all module-level data structures to JSON
output = {}
for attr in dir(mod):
    if attr.startswith('_'):
        continue
    val = getattr(mod, attr)
    if isinstance(val, (dict, list, tuple, str, int, float, bool)):
        output[attr] = val  # JSON-serializable

with open('/tmp/recovered.json', 'w') as f:
    json.dump(output, f, indent=2, default=str)
```

## Key Gotcha: sys.modules Registration

The `sys.modules['module_name'] = mod` line before `loader.exec_module(mod)` is
non-obvious but critical. Without it, any module that uses `@dataclass` will fail:

```
AttributeError: 'NoneType' object has no attribute '__dict__'
```

This happens because the dataclass decorator calls `_is_type()` which does
`sys.modules.get(cls.__module__).__dict__` — if the module isn't in
`sys.modules` yet, it gets `None`.

## Reconstructing Source from JSON

Once you have the JSON dump, regenerate Python source programmatically:

```python
import json

with open('/tmp/recovered.json') as f:
    data = json.load(f)

lines = []
# For each dict/list/string in the data, emit Python source lines
# This is mechanical: iterate keys, emit "key: value," with proper
# escaping for strings, nested dicts, lists of dicts, etc.
```

The reconstruction won't recover the original function *bodies* (those are
bytecode, not data), but it will recover:
- All module-level constants, dicts, and lists
- All dataclass field definitions (via `dir()` inspection)
- String/int/bool/list/dict values

## Verifying Recovery

After writing the reconstructed source:

```bash
python3 -c "
from module_name import FLEET_REGISTRY, fleet_summary
s = fleet_summary()
print(f'Recovered: {s}')
"
```

## Limitations

- Function bodies are lost (bytecode → can decompile with `decompyle3`/`uncompyle6`
  for Python ≤3.8, but 3.11+ has no reliable decompiler)
- Comments and docstrings inside functions are gone
- Import order may need manual fixing
- The `.pyc` must match the Python version that compiled it

## Prevention

Always `git init` in directories with important Python files. A `.pyc` recovery
is a last resort — git history is the correct backup.
