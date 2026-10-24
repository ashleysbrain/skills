# Surgical Patcher Pattern for ecs.py Bulk Edits

When you need to add or modify neuroanatomy layers (differentiations,
faculties, process_flows) across many entries in `agent-organism/ecs.py`, use
a single Python patcher script with anchored string insertion — not
hand-editing, not regex, not parallel subagents (they race on the same file).

## When to Use

- Adding faculties + process_flows to 10+ engine entries in one pass
- Any bulk edit where each entry needs unique, scientifically grounded content
- Post-edit verification that the module still imports and schema is intact

## The Pattern (5 steps)

### Step 1: DIGEST — query live state

Import ecs.py (with sys.modules pre-registration) and list what needs filling:
```python
import sys, importlib.util
spec = importlib.util.spec_from_file_location('ecs', 'agent-organism/ecs.py')
m = importlib.util.module_from_spec(spec)
sys.modules['ecs'] = m
spec.loader.exec_module(m)
R = m.FLEET_REGISTRY
for slug, n in R.items():
    D = len(n.get('differentiations') or [])
    F = len(n.get('faculties') or [])
    P = len(n.get('process_flows') or [])
    if D > 0 and F == 0:  # partial stubs needing F+P
        print(f'{slug}: D={D} F={F} P={P}')
```

### Step 2: Extract exact anchors

For each target entry, get the LAST `biological_reference` string from the
existing differentiations list. This becomes your unique insertion anchor:
```python
last_bio = n['differentiations'][-1]['biological_reference']
# Build anchor: the bio_ref line + the closing brackets
```

### Step 3: Author the patcher script

Write a Python script to `/tmp/` (throwaway, not an artifact) that:

1. Reads ecs.py as plain text (`Path.read_text()`)
2. For each engine, defines a unique anchor string and an insertion block
3. Uses `str.count(anchor) == 1` assertion to guarantee uniqueness
4. Inserts the block AFTER the anchor via `str.replace(anchor, anchor + block, 1)`
5. Writes the file back

```python
ECS = Path("/<workspace>")
src = ECS.read_text()

def insert_after(anchor, block, label):
    global src
    count = src.count(anchor)
    assert count == 1, f"[{label}] anchor found {count}x (need 1)"
    src = src.replace(anchor, anchor + block, 1)
```

### Step 4: CRITICAL ANCHOR PITFALL

The anchor MUST end at the `differentiations` list close (`        ],\n`)
— NOT at the entry close (`    },`). If the anchor includes the entry close,
the insertion lands OUTSIDE the entry dict (as a sibling key in
`FLEET_REGISTRY`), and the data won't appear in the processed registry.

**WRONG** (insertion outside the dict):
```python
anchor = '...biological_reference..."\n            },\n        ],\n    },'
#                                                              ^^^^ THIS
```

**RIGHT** (insertion inside the dict):
```python
anchor = '...biological_reference..."\n            },\n        ],\n'
# No trailing entry-close — insertion lands inside the entry
```

For intake modules that end with a `gate` field (no differentiations), the
anchor is just the gate line:
```python
anchor = '        "gate": "VERITAS (mandatory...)",\n'
```

### Step 5: Verify — import + schema check

The patcher script MUST end with a verification step that imports the
patched file and checks each target's D/F/P counts match expectations:

```python
sys.path.insert(0, str(ECS.parent))
import ecs as ecs_mod
R = ecs_mod.FLEET_REGISTRY
targets = {'ds-beaumont-engine': (3, 4, 1), ...}
for slug, (exp_d, exp_f, exp_p) in targets.items():
    n = R[slug]
    actual = (len(n.get('differentiations') or []),
              len(n.get('faculties') or []),
              len(n.get('process_flows') or []))
    assert actual == (exp_d, exp_f, exp_p), f"{slug}: {actual} != expected"
```

If verification fails, `git checkout ecs.py` and fix the anchors.

## Why Not Parallel Subagents?

Multiple subagents editing the same Python file concurrently will race.
The file changes line numbers between edits, and concurrent writes clobber
each other. The inline patcher is both faster (one script, one run) and
safer (unique-anchor assertions catch collisions before they write).

## Content Standards

Every neuroanatomy layer entry must have:
- `name` — descriptive, specific (e.g., "Glomerular filtration", not "Filtration")
- `primary_structures` (faculties only) — real anatomical structures
- `description` — what the faculty does, grounded in the scientist's work
- `biological_reference` — cited real science (author + year, or named structures)
- `flow` + `modes` (process_flows only) — neurochemical profiles with 2 modes

All content must be REAL biology — no placeholder, no junk, no invented
references. If you don't know the neuroscience for an engine, research it
before writing the patcher block.

## Track Record

| Wave | Engines | Technique | Result |
|------|---------|-----------|--------|
| Wave 1 | 5 | Parallel subagents | 2/3 crashed, recovered work manually |
| Wave 2 | 17 | Parallel subagents | Crashed on completion, stale notification |
| Wave 3 | 10 | Inline patcher | First-run anchor bug (trailing `\n    },`), fixed, clean |
| Wave 4 | 12 | Inline patcher | Clean first run |
| Wave 5 | 12 | Inline patcher | Clean first run |
| Wave 6 | 3+20+1 | Inline patcher (triage-driven) | 3 F+P fills, 20 analog_notes, 1 deprecation. Clean |
| Wave 7 | 14 | Inline patcher (replace_field) | 26 replacements (scientist + body_part pairs). Clean |
| Wave 8 | 90 | Hybrid (inline + 3 subagents) | Subagents added 58 tech_analogs but created duplicate keys. Inline patcher added 34 more cleanly. Reconciliation commit removed 33 dupes. One subagent caught a wrong analog (compliance-verification). |
| Wave 9 | 47+29 | Inline patcher | 47 body_parts (engine_name anchor strategy), 29 dependency fixes. Clean |
| Wave 10 | 90+17 | Inline patcher (version bumps + name fixes) | 90 version bumps via global replace_all (465 text replacements), 17 engine_name fixes via slug-anchored replace. Version bump cascade broke 0 deps. Clean |
| Wave 11 | 2+21 | Inline patcher (prefix + domain fixes) | 2 prefix corrections (Morphogen ORG→PTH, Arnheim PTH→NPR) via global replace, 21 body_system fixes to match DD codes. 0 broken deps. Clean |
| Wave 12 | 35 | Inline patcher (line-based port insertion) | 35 port assignments. Entries without `"port"` field at all needed line-number-based insertion (find slug key, scan forward, insert after nearest field). 0 entries without port. Clean |
| Wave 13 | 3 new | Write-file script + manual struct fix | 3 new organs registered (Houssay/pituitary, Moruzzi/brainstem, Banting/pancreas). Anchor-based insertion into FLEET_REGISTRY closing brace hit a structural bug: the insertion consumed the previous entry's closing `},` and orphaned `"physics_gate": "required",`. Required 2 follow-up patches to fix the struct. Lesson: when inserting before `}\n`, verify the anchor doesn't span across entry boundaries. Use `rfind` for the last occurrence. Clean after fix. 94 entities, 74 DEVELOPED. |
| Wave 14 | 4 new | Write-file script + manual struct fix | 4 new organs (Rappaport/liver, Galen/spleen, Till/bone marrow, Kocher/thyroid). Same structural bug as Wave 13: the anchor `'...Banting entry closing...\\n}\\n\\n_CODE_TO_KEY'` consumed Banting's `],\\n    },` closing. Required 2 follow-up patches. Lesson REINFORCED: for new entry insertion, do NOT use multi-line anchors that span entry boundaries. Instead, build the new entries string with its own self-contained `},` closures and insert at the rfind position of the dict's closing `}`. Clean after fix. 98 entities, 78 DEVELOPED. |

The inline patcher pattern proved strictly superior: faster, safer, and
self-verifying. Use it for all future waves.

## Registering New Organs (Wave 13 Pattern)

When adding entirely new engine entries (not just editing existing ones),
three insertions are needed:

1. **Entry dict** in FLEET_REGISTRY — insert before the closing `}\n`
2. **Code mapping** in `_CODE_TO_KEY` — add `"DS-ECS-...": "slug",`
3. **Dependencies** in other engines that should reference the new organ

**Pitfall:** The FLEET_REGISTRY closing `}` is preceded by the last entry's
closing `},`. An anchor like `'"physics_gate": "required",\n    },\n}\n'`
spans across the boundary. Safer approach: use `rfind` (last occurrence)
to find the anchor from the actual last entry, then insert after its `},`:

```python
anchor = '"physics_gate": "required",\n    },'
pos = src.rfind(anchor)  # rfind = last occurrence = the actual last entry
src = src[:pos + len(anchor)] + '\n' + new_entry + src[pos + len(anchor):]
```

**New organ checklist:**
- Full ECS code (DS-ECS-<PREFIX>-<DD>.<SS>.<NN>-v1.0.0)
- Scientist name (the discoverer, Nobel laureate preferred)
- scientist_note (who they were, what they discovered)
- Port assigned (next available integer)
- body_system matching DD domain number
- body_part (specific anatomical structure, NOT the engine name)
- tech_analog (real-world technology mapping)
- D/F/P layers (minimum 3 differentiations, 3 faculties, 1 process_flow)
- Dependencies wired to Hall (clock) + Harvey (blood supply) + domain organs
- Entry added to `_CODE_TO_KEY`
- Verification: entity count increased, `broken == 0`

## Version Bump Pattern (Wave 10)

When bumping versions across the fleet, use global `str.replace()` with
the FULL old ECS code string. This catches all occurrences: the entry's
own `ds_ecs_code` field, dependency arrays, `extra` dicts, and the
`_CODE_TO_KEY` lookup table. One `replace()` call per version change:

```python
# Bump all references to the specialist engine from v1.0.0 to v1.1.0
src = src.replace("DS-ECS-SUB-04.02.01-v1.0.0", "DS-ECS-SUB-04.02.01-v1.1.0")
# Touches: own code field + all dependency arrays referencing it + extra dicts
```

For engine_name fixes, use the slug key as the anchor to scope the
replacement to the correct entry (global replace would hit other entries
that share common words):

```python
slug_anchor = f'"{slug}": {{'
pos = src.find(slug_anchor)
ename_pos = src.find(f'"engine_name": "{old_name}"', pos)
src = src[:ename_pos] + f'"engine_name": "{new_name}"' + src[ename_pos + len(old_str):]
```

**CRITICAL:** After any version bump, verify `_CODE_TO_KEY` integrity:
```python
broken = sum(1 for k,v in R.items() for d in (v.get('dependencies') or []) if d not in _CODE_TO_KEY)
assert broken == 0, f"{broken} broken dependencies after version bump"
```

## Lessons from Waves 6-9

### Triage before filling (Wave 6)

Not all entries need the same treatment. Before bulk-filling:
1. Check for `status: DEPRECATED` entries — skip them entirely
2. Process-flow channels need `analog_note` (process-level biology), NOT D/F/P layers
3. PROC definitions need `body_part` + `analog_note`, NOT D/F/P layers
4. Only scientist-named engines with ports get full D/F/P layer fills

User directive: "don't work on what you should not work on."

### Scientist names for process flows (Wave 7)

Process-flow entries had empty scientist fields and body_parts that
restated the engine name. The fix: assign the DISCOVERER of each
biological system (e.g., Dale for neuromodulatory, Kandel for plasticity,
Bernard for homeostasis). The `replace_field` technique works cleanly:

```python
def replace_field(anchor, replacement, label):
    count = src.count(anchor)
    assert count == 1
    src = src.replace(anchor, replacement, 1)
```

### Global replace_all for version drift (Wave 8)

When engines are versioned up (v1.0 → v1.1), dependency arrays across
the fleet still reference the old version. Fix with global replace:

```python
src = src.replace("DS-ECS-PTH-04.01.01-v1.0.0", "DS-ECS-PTH-04.01.01-v1.1.0")
# 47 replacements in one call
```

Then verify: `broken = sum(1 for d in deps if d not in _CODE_TO_KEY)` → must be 0.

### Engine_name anchor strategy (Wave 8-9)

For adding new fields (tech_analog, body_part) to many entries, use the
engine_name as a unique anchor, then search forward for the nearest
body_system/body_part/scientist_note line:

```python
name_anchor = f'"engine_name": "{ename}",'
pos = src.find(name_anchor)
search_start = pos + len(name_anchor)
bs_pos = src.find('"body_system"', search_start)
bp_pos = src.find('"body_part"', search_start)
# Pick nearest, insert after that line
insert_pos = min(p for p in [bs_pos, bp_pos] if p != -1)
line_end = src.find('\n', insert_pos)
src = src[:line_end] + f'\n        "tech_analog": "{val}",' + src[line_end:]
```

This is more robust than hardcoding full anchor strings because it
adapts to which fields already exist in each entry.

### Parallel subagents for simple field adds (Wave 8 caveat)

Parallel subagents CAN add simple single-line fields (like tech_analog)
to the same file without catastrophic corruption — but they create
duplicate keys that require a reconciliation pass. One subagent also
caught a data error (wrong analog value) that the others missed.

**Verdict:** Use inline patcher for complex multi-line blocks (D/F/P
layers). Subagents are acceptable for simple single-field additions if
you plan a reconciliation commit afterward.

### Prefix/domain verification (Wave 11)

After any registry change, verify ECS prefix correctness and DD-to-body_system
consistency. Each prefix must match biological granularity:

- SYS = system-level organ (the 5 non-nervous system organs)
- ORG = specific organ (heart, kidney, gonad)
- SUB = specialized sub-unit (cortical region, sensory)
- CEL = cell-level (macrophage, glial, T-cell)
- NPR = process route (agent, flow, procedure)
- PTH = fundamental pathway (action potential, clock, muscle contraction)
- APP = application/tool
- GEN = genome

Domain number (DD) must match body_system. Run both checks post-edit:

```python
# DD ↔ body_system consistency
domain_map = {'01':'integumentary','02':'skeletal','03':'muscular',
    '04':'nervous','05':'endocrine','06':'cardiovascular','07':'lymphatic',
    '08':'respiratory','09':'digestive','10':'urinary','11':'reproductive',
    '12':'diagnostic','13':'organism_processes'}
for k, v in R.items():
    code = v.get('ds_ecs_code','')
    dd = code.split('-')[3].split('.')[0] if '-' in code else ''
    bs = v.get('body_system','')
    expected = domain_map.get(dd,'')
    if expected and bs != expected:
        print(f"MISMATCH: {k} DD={dd} bs='{bs}' expected='{expected}'")
```

Prefix corrections use the same global replace pattern as version bumps.
Body_system fixes use the slug-anchored replace pattern from Wave 8-9.

### Port assignment for every entry (Wave 12)

Every entry MUST have a real integer port. Entries with `port: None` or
`port: 0` (or no port field at all) must be assigned one. The technique:

1. Find highest port in use: `max(v.get('port',0) for v in R.values())`
2. Assign sequential ports starting from next number
3. For entries with `"port": None` or `"port": 0`: use slug-anchored
   replace to swap the value
4. For entries with NO port field (some PROCs/agents): use line-number-based
   insertion — split the file into lines, find the slug key line, scan
   forward 30 lines for the nearest field, insert a new port line after it

```python
lines = ECS.read_text().split('\n')
for slug, port in port_assignments.items():
    # Find slug key line
    for i, line in enumerate(lines):
        if f'"{slug}":' in line:
            start = i
            break
    # Scan forward for nearest "port" field
    for j in range(start, min(start + 30, len(lines))):
        if '"port"' in lines[j]:
            lines[j] = f'        "port": {port},'
            break
    else:
        # No port field — insert after ds_ecs_code or engine_name
        for j in range(start, min(start + 30, len(lines))):
            if '"ds_ecs_code"' in lines[j] or '"engine_name"' in lines[j]:
                lines.insert(j + 1, f'        "port": {port},')
                break
ECS.write_text('\n'.join(lines))
```

Verify: `no_port = sum(1 for v in R.values() if not v.get('port') or v.get('port') == 0)`
must be 0.
