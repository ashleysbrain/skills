# Dependency Audit Protocol for ecs.py

Validating the biological correctness of engine dependency graphs in
`agent-organism/ecs.py`. Developed during Wave 8-9 of the fleet audit
(2026-06-28).

## Three Audit Dimensions

### 1. Broken References (Version Drift)

When engines are versioned up (v1.0 → v1.1), dependency arrays that
reference them by full ECS code break silently. The registry imports fine,
but `lookup_engine(dep_code)` fails for the stale version.

**Detection:**
```python
import ecs as m
R = m.FLEET_REGISTRY
CODE = m._CODE_TO_KEY

broken = []
for slug, entry in R.items():
    for dep in (entry.get('dependencies') or []):
        if dep not in CODE:
            broken.append((slug, entry.get('ds_ecs_code',''), dep))

# Also check for category prefix errors (e.g., ORG vs APP)
for slug, src_code, dep in broken:
    parts = dep.rsplit('-v', 1)
    base = parts[0] if len(parts) == 2 else dep
    if base in code_base_to_actual:
        print(f"VERSION FIX: {dep} → {code_base_to_actual[base]}")
    else:
        print(f"ORPHAN: {dep} (no version exists)")
```

**Fix:** Global replace_all for version drift (safe because old version
strings are globally unique):
```python
src = src.replace("DS-ECS-PTH-04.01.01-v1.0.0", "DS-ECS-PTH-04.01.01-v1.1.0")
```

**Historical fix (Wave 8):** 66 broken deps from 6 version-drift sources:
- Hall v1.0→v1.1 (47 refs — the most-referenced engine)
- Harvey v1.0→v1.1 (6 refs)
- Unna v1.0→v1.1 (5 refs)
- Morphogen v1.0→v1.1 (4 refs)
- Bright v1.0→v1.1 (2 refs)
- O'Keefe v1.0→v1.1 (1 ref)
- Osler ORG→APP category prefix (1 ref)

### 2. Missing Dependencies

Entries with `dependencies: []` need biological connections added.

**Biological rules:**
- Every entry should depend on at least one other engine
- The physics gate (the specialist engine, `DS-ECS-PTH-04.01.01`) is the master clock — most engines depend on it
- Process flows and PROCs may reference multiple engines

**Fix:** Add dependencies by inserting into the existing list:
```python
# For empty lists:
old = '"dependencies": []'
new = '"dependencies": ["DS-ECS-PTH-04.01.01-v1.1.0"]'

# For non-empty lists, insert before closing bracket:
bracket_close = src.find(']', dep_pos)
src = src[:bracket_close] + f', "{dep_to_add}"' + src[bracket_close:]
```

### 3. Biological Correctness (Dependency Semantics)

Dependencies must make anatomical sense. Two rules enforced in Wave 9:

**Blood Supply Rule:** Organ system engines (digestive, respiratory,
urinary, endocrine, muscular, skeletal, integumentary) must depend on
the specialist engine (`DS-ECS-ORG-06.01.01-v1.1.0`) for cardiovascular circulation.

**Clock Root Rule:** Nervous system components (agents, intakes, cognitive
engines) must depend on the specialist engine (`DS-ECS-PTH-04.01.01-v1.1.0`) for the
physics gate / SCN timing signal.

**Audit script:**
```python
organ_systems = ['digestive','respiratory','urinary','endocrine',
                 'muscular','skeletal','integumentary']
harvey = "DS-ECS-ORG-06.01.01-v1.1.0"
hall = "DS-ECS-PTH-04.01.01-v1.1.0"

issues = []
for slug, v in R.items():
    if v.get('status') == 'DEPRECATED': continue
    bs = v.get('body_system','')
    deps = set(v.get('dependencies') or [])
    
    if bs in organ_systems and harvey not in deps:
        issues.append(('BLOOD_SUPPLY', slug))
    
    if not slug.startswith(('process-flow-','proc-')):
        if hall not in deps and slug != 'ds-nervous-system':
            if bs not in organ_systems:
                issues.append(('NERVOUS_LINK', slug))
```

## Verification Command

After any dependency change, run this one-liner to verify integrity:
```python
python3 -c "
import sys; sys.path.insert(0,'.')
import ecs as m
R = m.FLEET_REGISTRY
broken = sum(1 for k,v in R.items() for d in (v.get('dependencies') or []) if d not in m._CODE_TO_KEY)
no_dep = sum(1 for v in R.values() if not (v.get('dependencies') or []))
print(f'Broken: {broken} | No-dep: {no_dep} | Total: {len(R)}')
"
```

Target: `Broken: 0 | No-dep: 0 | Total: 91`
