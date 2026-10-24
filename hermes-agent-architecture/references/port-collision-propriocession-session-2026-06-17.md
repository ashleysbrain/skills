# Port Collision Proprioception — 2026-06-17 Session

## Problem

User noticed "the registry is wrong that it's reading from. Something is off."
Investigation found 4 invisible/mismatched engines hiding in the fleet.

## Discovery Method

### Step 1: Physical disk scan
```bash
for d in /<workspace>*/; do
    name=$(basename "$d")
    if [ -f "$d/run_server.py" ] || [ -f "$d/src/api/server.py" ]; then
        echo "$name"
    fi
done
```

### Step 2: Registry scan
```python
import sys; sys.path.insert(0, 'ds-engine-registry')
from ecs import FLEET_REGISTRY
reg = {v.get('directory','') for v in FLEET_REGISTRY.values() if not v.get('renamed_to')}
```

### Step 3: Port collision scan (CRITICAL)
```python
import re, os
port_map = {}
# From disk run_server.py files
for d in os.listdir('.'):
    if not d.startswith('ds-'): continue
    path = f'{d}/run_server.py'
    if not os.path.exists(path): continue
    content = open(path).read()
    ports = re.findall(r'port[=,\s]+(\d{4,5})', content)
    for p in ports:
        port_map.setdefault(int(p), []).append(f'{d} (disk)')
# From registry
for k, e in FLEET_REGISTRY.items():
    p = e.get('port')
    if p:
        port_map.setdefault(p, []).append(f'{k} (registry)')
# Find collisions
for p in sorted(port_map):
    if len(port_map[p]) > 1:
        print(f'COLLISION :{p}: {port_map[p]}')
```

## Findings

| Engine | Port | Issue | Fix |
|--------|------|-------|-----|
| ds-design-engine | 8094 | Collided with Beaumont. Beaumont won every boot, Design died silently. | Reassigned to :port, registered as DS-ECS-02.09.01 |
| ds-seed-engine | 8095 | Renamed to Reproductive months ago but old dir+server still existed, colliding with Self-Healing | Archived to `_archived/`, LaunchAgent removed |
| ds-system-state-sensor | 8104 | Registry said `ds-system-state-sensor` (no `-engine`), actual dir is `ds-system-state-sensor-engine` | Fixed registry key to match directory |
| ds-nervous-system | 8000 | Not registered at all. Organism dashboard/spine. | Registered as DS-ECS-02.00.00 |

## Proprioception Check Fix

The body-map diff was only matching directories ending in `-engine` or `-agent`.
Fixed to also detect directories with actual server code:

```python
disk_engines = set()
for d in os.listdir(WORKSPACE):
    if d.startswith("ds-"):
        full_path = os.path.join(WORKSPACE, d)
        has_server = os.path.exists(os.path.join(full_path, "run_server.py")) or \
                     os.path.exists(os.path.join(full_path, "src", "api", "server.py"))
        if has_server or d.endswith("-engine") or d.endswith("-agent"):
            disk_engines.add(d)
```

## Result

Before: 27 UP / 0 DOWN (but 4 engines invisible or colliding)
After: 29 UP / 0 DOWN / 0 PLANNED / 29 TOTAL, proprioception SYNCED
