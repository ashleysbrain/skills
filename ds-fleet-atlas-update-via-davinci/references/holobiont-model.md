# The Holobiont Model — External Systems Architecture

Source: `docs/EXTERNAL-ENGINES-METAPHOR.md` (canonical definition)

## The Concept

In biology, a **holobiont** is a host organism plus all its associated
symbiotic partners, functioning as a single ecological unit. You are not
just your cells — you are ~30 trillion human cells + ~40 trillion
bacterial cells + viruses + fungi. They're not "you" but you can't live
without them.

The DS organism works the same way. The 45+ engines are the body.
Everything else is the holobiont: systems that work alongside, are
essential to function, but aren't body parts.

## The Four Rings

```
┌─────────────────────────────────────────────┐
│         RING 4: THE ECOSYSTEM               │
│   (External world: APIs, users, internet)    │
│  ┌───────────────────────────────────────┐   │
│  │      RING 3: THE MICROBIOME           │   │
│  │  (hydra-os, cron, scripts, kanban)    │   │
│  │  ┌───────────────────────────────┐    │   │
│  │  │   RING 2: THE IMMUNE MEMORY   │    │   │
│  │  │  (Advisory Panels, intel,     │    │   │
│  │  │   standups, data)             │    │   │
│  │  │  ┌───────────────────────┐    │    │   │
│  │  │  │  RING 1: THE BODY     │    │    │   │
│  │  │  │  (45+ the specialist engine)     │    │    │   │
│  │  │  │  Living tissue, DNA   │    │    │   │
│  │  │  └───────────────────────┘    │    │   │
│  │  └───────────────────────────────┘    │   │
│  └───────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

### RING 1: THE BODY (Endosymbiont)
- **Bio:** Your own cells. Your DNA. The organism itself.
- **DS:** 45+ engine directories with physics layers, health endpoints, DS-ECS codes. These ARE the organism. They have the DNA (ecs.py).
- **Rule:** Changes here change the organism. Registry required.

### RING 2: THE IMMUNE MEMORY (Adaptive Symbionts)
- **Bio:** Memory B-cells and T-cells. Learned from exposure.
- **DS:** Advisory Panels (ds-wave-*), intel/, standups/, health data.
- **Rule:** They observe and advise. They don't change the DNA directly.

### RING 3: THE MICROBIOME (Metabolic Symbionts)
- **Bio:** Gut bacteria that digest food, produce vitamins, train immunity. 40 trillion of them. Remove them and you die.
- **DS:** hydra-os (OS), cron system, scripts/, kanban/, LaunchAgents.
- **Rule:** They manage the body's metabolism. They can trigger changes but the body's DNA must accept them.

### RING 4: THE ECOSYSTEM (Environmental Interface)
- **Bio:** The world you live in. Food, air, water, temperature, social contact.
- **DS:** External APIs (weather, fitness trackers), Telegram gateway, web search, the operator agent Agent itself, OpenClaw fleet, external data sources, legal/financial systems.
- **Rule:** The organism senses and responds. It can't control the ecosystem but it adapts to it.

## The Vagus Nerve Bridge

The Nervous System engine (ds-nervous-system, :port) sits at the boundary
between Ring 1 and Ring 3. It is the **vagus nerve** of the organism:
connects the brain (consciousness/the operator agent) to the gut
(microbiome/cron/hydra-os) and to every organ.

Gut-brain axis is bidirectional:
- Brain tells gut what to do (top-down)
- Gut tells brain how it feels (bottom-up)

In DS:
- the operator agent (consciousness) drives the organism through the nervous system
- Engines report health through the nervous system
- hydra-os (microbiome) feeds status to the nervous system
- The dashboard shows the whole holobiont state

## Quick Reference Table

| the specialist engine | Ring | Bio Equivalent |
|-----------|------|----------------|
| 45+ DS engines (ds-*-engine) | Ring 1: Body | Human cells, organs |
| ds-engine-registry (ecs.py) | Ring 1: Body | DNA |
| Advisory Panels (ds-wave-*) | Ring 2: Immune Memory | Memory B/T cells |
| intel/, standups/ | Ring 2: Immune Memory | Antibody records |
| health-private, health-backups | Ring 2: Immune Memory | Immune memory |
| hydra-os | Ring 3: Microbiome | Gut microbiome |
| cron system | Ring 3: Microbiome | Circadian rhythm |
| LaunchAgents | Ring 3: Microbiome | Autonomic nervous system |
| kanban/ | Ring 3: Microbiome | Motor planning |
| scripts/ | Ring 3: Microbiome | Digestive enzymes |
| ds-nervous-system (:port) | Ring 1→3 Bridge | Vagus nerve |
| the operator agent Agent | Ring 4: Ecosystem | Consciousness/pilot |
| Telegram gateway | Ring 4: Ecosystem | Sensory organ (eyes/ears) |
| OpenClaw fleet | Ring 4: Ecosystem | Social group / colony |
| External APIs | Ring 4: Ecosystem | Environment |
| Products (8d-sleep, etc.) | Ring 1 Output | What the body produces |
| Business units | Ecosystem | The wider colony |

## Why This Matters for Fleet Atlas Charts

When documenting the organism architecture, Ring 1 organs go INSIDE the
body boundary (the skin / the specialist engine). External systems (Rings 2-4) go
OUTSIDE the boundary, shown as symbiotic rings. The von Frisch Signal
Organ sits AT the boundary (integumentary — it is the organism's
interface with the external world).
