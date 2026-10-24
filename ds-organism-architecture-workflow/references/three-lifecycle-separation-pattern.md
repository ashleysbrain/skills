# Three-Lifecycle Separation Pattern

## When to Use

When designing interactions between symbiotic but independent biological systems (e.g., organism + fungal network + forest ecosystem), decompose into separate lifecycles FIRST, define stages for each, THEN define integration points. Never merge lifecycles from different biological kingdoms into one phase cycle.

## The Problem This Solves

Mixing fungal biology, tree/organism biology, and forest ecology into one N-phase cycle produces structural incoherence. Phases cannot map cleanly to engines. A "network growth" phase accidentally includes organism birth mechanics. An "ecosystem maturity" phase accidentally includes fungal fruiting. The root cause: treating a symbiotic relationship as a single organism.

Trees and fungi are symbiotic partners. They depend on each other. But they are NOT the same organism. They reproduce differently (seeds vs spores), grow differently, die differently. A forest is neither a tree nor a fungus. It is an emergent property of both.

## The Three Lifecycles

### Lifecycle 1: Organism Lifecycle (the specialist engine, already built)

How ONE organism is created. Birth canal stages, embryonic development, APGAR, birth. This is REPRODUCTION. the specialist engine owns this entirely. It does NOT connect organisms to anything. It births them and hands them off.

- Stages: Gametogenesis -> Specification -> DNA Injection -> Compile -> Birth (then embryonic: Zygote -> Morula -> Blastula -> Gastrula -> Organogenesis -> Fetus -> Birth operational)
- Produces: the operator agent -> B2B -> B2C -> Product (each birthed through the same canal)

### Lifecycle 2: Fungal Network Lifecycle (the specialist engine, new)

How the mycorrhizal NETWORK grows. The fungus is a SEPARATE ORGANISM from the trees. It has its own lifecycle using fungal biology, NOT plant biology.

- Stages: Spore -> Germination -> Colonization (Hartig Net) -> Expansion -> Anastomosis -> Fruiting -> Succession
- Key constraint: the specialist engine does NOT create organisms. It CONNECTS them. All cognition belongs to organisms. The network is substrate.
- Fungal lifecycle terms (spores, hyphae, mycelium, fruiting bodies) are used for this lifecycle. NOT plant terms (seed, germination for plants, fruiting for plants).

### Lifecycle 3: Forest Ecosystem Lifecycle (emergent)

What happens when Lifecycle 1 and Lifecycle 2 interact over time. No single engine owns this. It emerges.

- Stages: Pioneer -> Establishment -> Canopy Closure -> Climax -> Renewal
- Monitored from the specialist engine state (organism count) and the specialist engine state (topology density). Never commanded via API.

## Integration Point Pattern

Define 4-6 specific integration points where the lifecycles meet. Each integration point has:

1. **Trigger** — what event fires the interaction
2. **Engines involved** — which engines from each lifecycle participate
3. **What happens** — the concrete mechanism
4. **Data flow** — what crosses the boundary, in which direction
5. **Physics** — what equation or model governs the interaction

Worked example: 6 integration points between the specialist engine and the specialist engine:

1. Organism birth triggers network germination (birth event -> /simard/connect)
2. Colonization unlocks cross-organism value (ConsentGrant + receptor channel open)
3. Forest establishment enables network intelligence (critical mass -> the specialist engine cross-organism patterns)
4. Products connect only to parent (scoped topology, no lateral edges)
5. the operator agent evolution pushes flow through network (phosphorus cascades through topology)
6. Disconnect triggers succession (channel decay, coupling drift, alternative source evaluation)

## Concrete Example Format

Track all three lifecycles in parallel across timeline steps (T=0 through T=N). For each time step, state what happens in EACH lifecycle independently. Include a summary table at the end:

| Time | Organism Lifecycle | Fungal Lifecycle | Forest Lifecycle |
|------|-------------------|-----------------|-----------------|

This parallel tracking is what makes the separation concrete. The reader sees that at T=2, the specialist engine births a B2C, the specialist engine moves from Spore to Germination, and the forest is still at Pioneer. Three clocks, three processes, one timeline.

## Separation Rules Enforced

1. the specialist engine never calls `/simard/connect`. The organism calls it after birth.
2. the specialist engine never creates a DimensionalSchema. The organism declares its own.
3. the specialist engine never interprets molecule content. Routes by type, priority, consent.
4. Forest stage is never set by API call. Computed from organism count + topology density.
5. Products are scoped to parent-only topology.

## Design Separation Test

Before designing any phase or stage, ask:
- Is this about how an organism is CREATED (Lifecycle 1)?
- Is this about how the network GROWS (Lifecycle 2)?
- Is this about how the ecosystem MATURES (Lifecycle 3)?

If the answer mixes two or more, separate them first, then define the handoff points.

## Worked Example

`~/your-workspace/ds-wave-gamification-advisory-panel-private/THREE-LIFECYCLES-SEPARATED.md` (370 lines). Six sections: organism lifecycle (references existing birth canal), fungal network lifecycle (7 stages with biological/technical/physics per stage), forest ecosystem lifecycle (5 emergent stages), 6 integration points, separation rationale, and the principal concrete example tracked across 9 timeline steps with summary table.
