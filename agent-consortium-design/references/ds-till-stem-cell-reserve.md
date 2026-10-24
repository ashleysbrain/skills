# the specialist engine Cell Reserve + Twin Organism Architecture

## the specialist engine Cell Reserve

Named after James Till (1922-2020) and Ernest McCulloch (1926-2011), who proved
in 1963 that a single stem cell can regenerate the entire blood system.

Registered in FLEET_REGISTRY at :port as Bone Marrow (Hematopoietic Stem Cell Niche).

### What It Does

When ANY engine goes down, the specialist engine differentiates a replacement from a stored
template in ~3 seconds. The replacement grafts into production while sibling-agent
diagnoses and fixes the original.

### Implementation

- Location: `~/your-workspace/stem-cell-reserve/`
- Activator: `activate.py` (300 lines)
- 9 of 10 critical engine templates harvested (the specialist engine missing — code in organism/ scripts)
- Differentiation tested: the specialist engine spawned on :9120 from template in 3 seconds, fully alive

### How to Use

```bash
# Check status
python3 ~/your-workspace/stem-cell-reserve/activate.py status

# Harvest/re-harvest templates (run after engine code changes)
python3 ~/your-workspace/stem-cell-reserve/activate.py harvest

# Differentiate a replacement for a failed engine
python3 ~/your-workspace/stem-cell-reserve/activate.py repair ds-goethe-engine
```

### the operator agent vs Opencode Roles

- HERMES does the bandaid: detect failure, differentiate spare, graft in, log repair
- OPENCODE does the deep fix: diagnose root cause, fix code, verify, remove graft
- Every hermes repair logged in `stem-cell-reserve/repair-log/` for sibling-agent review

## Twin Organism Architecture

### Problem
A 24/7 company needs the organism always operational. But the organism must sleep
(consolidate, clean, integrate) or it degrades.

### Solution: Identical Twins with Replicated Data

NOT conjoined twins (shared brainstem = single point of failure). NOT organism-level
failover. IDENTICAL TWINS where each is fully independent.

### Key Principle: Surgical Graft, Not Organism Failover

User correction (2026-06-30): "I don't want the twin to take over. I want that
element that's broken in the operator agent to have a backup in the twin that it can surgically
put in there."

When the specialist engine (:port) breaks in Production the operator agent, the Twin's the specialist engine-T grafts
into Production the operator agent's process flow. The rest of the operator agent keeps running. Only the broken
part is replaced.

### Architecture

- Production the operator agent: ports 8xxx
- Twin the operator agent: ports 10xxx (offset +2000)
- Shared DATA (not shared engines): memory DB, genome file, task queue
- Each organism has COMPLETE set of engines — fully self-sufficient
- No single point of failure

### Sleep Cycle (24/7 operation)

Three layers running simultaneously:
1. CORE (never sleeps): the specialist engine heartbeat, the specialist engine homeostasis, the specialist engine autonomic
2. CORTEX (mode switches): AWAKE = task execution, SLEEP = consolidation
3. GLIA (inverse schedule): MORE active during sleep — the specialist engine glymphatic cleansing

Sleep mode activates: DS O'Keefe full consolidation, the specialist engine glymphatic cleanse,
the specialist engine connection repair, selection engine weight renormalization, the specialist engine
immune memory integration.

Emergency wake: critical task arrives during sleep, the sleeping engine wakes instantly
(like a mother waking to a baby's cry).

### Build Order

1. the specialist engine stem cell reserve (DONE — hermes built, sibling-agent integrates)
2. the specialist engine service mesh (detects failures, performs grafts)
3. Twin organism instances (once graft protocol works)
4. Sleep architecture (circadian mode switching, local sleep)

### Bus Messages

- 952: the specialist engine service mesh + sleep architecture design spec
- 957: the specialist engine stem cell reserve build request
- 958: Twin organism architecture
- 960: the specialist engine proven working status
