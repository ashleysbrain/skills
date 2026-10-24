---
name: ds-ecs-coding-system
description: DS-ECS code format with category prefixes for organism anatomy. Mandatory for all new engines and agents.
tags: [ds-ecs, ecs, ecm, coding-system, anatomy, registry, organism, versioning]
version: 1.0
---

# DS-ECS Coding System Skill

Use when creating, modifying, or referencing any DS organism engine or agent code. Every new engine, agent, or anatomical part MUST get a DS-ECS code following this format.

## When to Use

- Creating a new engine or agent in the DS organism
- Adding a body part, neural process, or cell system
- Modifying `agent-organism/ecs.py` or `agent-organism/REGISTRY.yaml`
- Creating anatomy specification files in `agent-organism/anatomy/`
- Referencing engines in documentation, cron jobs, or cross-session work

## Code Format (v4.0+)

```
DS-ECS-<CAT>-<DOMAIN>.<SUBSYSTEM>.<SPECIFIC>-v<MAJOR>.<MINOR>.<PATCH>
```

### Category Prefixes (3-letter, mandatory)

| Prefix | Category | Definition | Examples |
|--------|----------|------------|---------|
| **SYS** | Organ System | Complete body system spanning the organism | Unna (skin), Burnet (lymphatic), Sutherland (endocrine) |
| **ORG** | Organ | Discrete macroscopic anatomical organ | Harvey (heart), Haldane (lungs), Beaumont (GI) |
| **SUB** | Substructure | Named region within an organ | Luria (PFC), O'Keefe (hippocampus), Mountcastle (thalamus) |
| **CEL** | Cell System | Population of cells with shared function | Metchnikoff (phagocytes), Golgi (glial cells), Rio Hortega (microglia) |
| **NPR** | Neural Process | Functional mechanism across cell populations | Rakic (corticogenesis), Sherman (thalamic relay), Nedergaard (glymphatic) |
| **PTH** | Pathway | Signal or mechanical route through tissue | Hodgkin (white matter), Tawara (cardiac conduction), Quartz (task lattice) |
| **APP** | Apparatus | Composite functional unit (not a single organ) | Bernard (diagnostics), Semmelweis (barrier), Self-Healing (repair) |
| **GEN** | Genetic | DNA/genome/chromatin level entity | Franklin (genome) |

### Domain Map

| Domain | Body System |
|--------|-------------|
| 01 | Integumentary |
| 02 | Skeletal |
| 03 | Muscular |
| 04 | Nervous |
| 05 | Endocrine |
| 06 | Cardiovascular |
| 07 | Lymphatic / Immune |
| 08 | Respiratory |
| 09 | Digestive |
| 10 | Urinary |
| 11 | Reproductive / Genetic |
| 12 | Diagnostic Infrastructure |

### Versioning Rules

**Entity version** (in the `-vX.Y.Z` suffix):
- MAJOR: Breaking architectural change (replaces core physics model)
- MINOR: New differentiations, faculties, or process flows added (backward-compatible)
- PATCH: Bug fix, documentation correction, reference update

**Critical rule: NEVER reset an entity's version when reformatting its code.** If an entity is at v1.1.0, v2.0.0, or v3.0.0, keep that version. Only the entity's own architectural changes should bump its version.

**Module version** (`__version__` in ecs.py): tracks the ECS module itself, separate from entity versions.

## How to Assign a New Code

1. **Determine the category** — is this a whole organ? A substructure? A cell population? A process?
2. **Find the domain** — which body system does it belong to?
3. **Find or create the subsystem** — what anatomical division within that domain?
4. **Find the next available specific number** — check existing codes in that subsystem for the highest number used
5. **Assign version v1.0.0** for new entities (unless this is an evolution of an existing entity, in which case keep moving the version forward)
6. **Check for collisions** — verify the full code is unique across ALL entries

## Registry Files (source of truth)

| File | Purpose |
|------|---------|
| `agent-organism/ecs.py` | Python source of truth. `FLEET_REGISTRY` dict imported by every engine. |
| `agent-organism/REGISTRY.yaml` | YAML version, generated from ecs.py. Human-readable. |
| `ds-engine-registry/ecs.py` | Synced copy. Must match agent-organism/ecs.py. |
| `agent-organism/anatomy/<SCIENTIST>-<STRUCTURE>.md` | Three-layer anatomy spec for each entity. |
| `DS-ECS-SPEC.md` | Human-readable documentation of the coding system. |

## Adding a New Entry

1. Add to `FLEET_REGISTRY` in `agent-organism/ecs.py` with all required fields
2. Add to `agent-organism/REGISTRY.yaml` in the same format
3. Create anatomy spec at `agent-organism/anatomy/<SCIENTIST>-<STRUCTURE>.md`
4. Sync `ds-engine-registry/ecs.py`
5. Verify: `python3 -c "from ecs import FLEET_REGISTRY; print(len(FLEET_REGISTRY))"`

## Verification Commands

```bash
# Check all codes have prefixes
cd ~/your-workspace/agent-organism && python3 -c "
from ecs import FLEET_REGISTRY
import re
prefix_re = re.compile(r'^DS-ECS-[A-Z]{3}-')
bad = [(k, e.get('ds_ecs_code','')) for k, e in FLEET_REGISTRY.items() if not prefix_re.match(e.get('ds_ecs_code',''))]
print(f'Unprefixed: {len(bad)}')
for k, c in bad: print(f'  {k}: {c}')
"

# Check for code collisions
python3 -c "
from ecs import FLEET_REGISTRY
from collections import Counter
codes = [e.get('ds_ecs_code','') for e in FLEET_REGISTRY.values()]
dupes = [c for c, n in Counter(codes).items() if n > 1]
print(f'Duplicates: {len(dupes)}')
for d in dupes: print(f'  {d}')
"
```

## Pitfalls

1. **Never reset entity versions.** If Luria is at v1.1.0, adding a prefix keeps v1.1.0.
2. **Always check for collisions.** Two entries with the same code will break lookups.
3. **Sync both ecs.py files.** The agent-organism and ds-engine-registry copies must match.
4. **No duplicate scientist names.** Check the full fleet (69 scientists) before naming. Use first initial + last name if needed (e.g., DS S Dehaene, DS A Craig, DS J Eccles).
5. **Category determines the prefix.** A neural process (NPR) is different from a substructure (SUB) even if both are in the nervous system.
6. **ENGINE NAMES = SCIENTIST/INVENTOR SURNAMES ONLY** (2026-07-16, BINDING). NEVER use system names (the specialist engine, the specialist engine, the specialist engine), concept names (VERITAS), or port numbers (':port') as engine display names. The user has corrected this across multiple sessions. Every engine MUST be `DS <Surname>`. When renaming, the scientist field in the registry MUST match the engine's actual namesake (the specialist engine = Claude Bernard, NOT William Osler). See agent-organism-interface-building/references/engine-naming-compliance-audit.md for the full rename log.
7. **INVALID CATEGORY PREFIXES — DO NOT USE:** REP, ALS, HRV, MRG, BEA, BRI, UNN, or any ad-hoc 3-letter codes. These are NOT valid ECS v4.0 prefixes. Only these 8 prefixes are valid: SYS, ORG, SUB, CEL, NPR, PTH, APP, GEN. When you see invalid prefixes in messages, handoffs, or docs, IMMEDIATELY correct to registry-aligned names (see reference/ecs-prefix-corrections.md). Two real-world examples found in the live fleet (audited 2026-06-28): **`DEV`** was used as a category prefix for the developmental organizer (correct: the organizer is a morphogen-gradient **pathway**, so `PTH`); and **`NP`** (2-letter) was used as an `entity_category` value on 11 neural-process agents whose own ECS codes already used the correct 3-letter `NPR` (the hand-typed field drifted from the code). Always cross-check `entity_category` values against the actual `-<CAT>-` segment of the entity's `ds_ecs_code` — they MUST match. A valid 3-letter prefix in the code with a 2-letter or ad-hoc string in `entity_category` is a bug.
