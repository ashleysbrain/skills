# Cylindrical Time-Linear Crystal Geometry

**Date:** 2026-06-27 (updated with upward-flow stacking pattern)
**Source:** User directive during Task Engine redesign session
**Status:** MANDATORY for all task-engine / time-based 3D structures

## The Core Insight

The user explicitly rejected orbital/planetary metaphors for time-based data:

> "i want a column like structure that is cylindrical in structure with the crystals growing out of it in the order that tasks are handled and growing to the size of the time spent on the task. i want there to be a visual correlation between the structure and the time the human or ai spends on tasks and time is linear, as human tasks can only follow a linear timeline not an orbiting one."

**Time is linear for humans and AI agents.** Tasks follow a sequential timeline, not an orbit.

## LATEST CORRECTION: Upward-Flow Stacking (2026-06-27 #5)

User rejected the ring-scattered approach:

> "this structure isn't pieced together and flowing upward in time like i planned or want it to."

### What Was Wrong
Tasks were arranged in horizontal RINGS around a pre-built cylinder skeleton at 3 fixed levels (segments). Each ring had tasks distributed evenly around the circumference. This read as scattered particles, NOT as a growing structure.

### What Works: Sequential Upward Stacking
The column builds itself piece by piece, bottom to top:

1. **NO pre-built cylinder skeleton.** No WireframeGeometry of a CylinderGeometry. The column only exists where tasks have been placed.
2. **Each task = a unique Y position.** Tasks stack one on top of another, sorted by segment then by urgency (highest urgency = bottom = first).
3. **Each task = a crystalline prism ring** extruded vertically (not radially). The polygon cross-section (hex/tri/dodec/etc.) is extruded upward by CELL_HEIGHT (0.85 units).
4. **Helical growth spiral.** Each task ring rotates slightly (0.3 radians per unit height) from the one below it, creating a crystal-twin spiral as you look up the column.
5. **Protruding crystal facets.** A smaller gemstone facet sits on the outer wall of each ring, offset at a fixed angle from the ring rotation. This is the "stone" that shows the dimension color and catches light.
6. **Bamboo node rings** (TorusGeometry) at segment boundaries mark time transitions. Gold for Now, teal for Next, dim for Later.
7. **Segment gaps** (0.35 units) between time blocks show the column is built in pieces, not as a continuous tube.
8. **Central axis line** (thin gold, 12% opacity) runs through the entire column for spatial reference.
9. **Column is centered vertically** around the origin by offsetting the group's Y position by -totalHeight/2.

### Growth States (Material Properties)
| State | Opacity | Roughness | Metalness | Emissive | Visual |
|-------|---------|-----------|-----------|----------|--------|
| DONE | 0.85 | 0.2 | 0.4 | 0.15 (bright) | Solid, permanent, metallic |
| DO | 0.55 | 0.5 | 0.1 | 0.08 (subtle) | Semi-transparent, active |
| WATCH | 0.35 | 0.5 | 0.1 | 0.03 (faint) | Translucent, waiting |
| DEFER | 0.20 | 0.5 | 0.1 | 0.03 (faint) | Ghostly wireframe at top |

### Three.js Geometry Pattern
```javascript
function createCellGeometry(sides, radius, height) {
  const shape = new THREE.Shape();
  for (let i = 0; i <= sides; i++) {
    const a = (i / sides) * Math.PI * 2;
    shape.moveTo/lineTo(Math.cos(a) * radius, Math.sin(a) * radius);
  }
  const geo = new THREE.ExtrudeGeometry(shape, {depth:height, bevelEnabled:false});
  geo.rotateX(-Math.PI / 2); // extrude upward (Y), not into Z
  return geo;
}

// Stacking: each task builds on currentY
const helixAngle = (currentY * 0.3) + (taskIndex * 0.15);
cellMesh.position.set(0, currentY + CELL_HEIGHT/2, 0);
cellMesh.rotation.y = helixAngle;
currentY += CELL_HEIGHT;
```

## Dimension-Specific Crystalline Shapes (NO squares)

User explicitly rejected cubes/squares: "I don't like the square as a shape it is too simple."

| Dim | Shape | Sides | Gemstone | Color |
|-----|-------|-------|----------|-------|
| phy | Hexagon | 6 | Citrine | #1a5c4c (teal-deep) |
| spi | Triangle | 3 | Clear Quartz | #d96b4a (warm) |
| int | Dodecagon | 12 | Fluorite | #4ad6b4 (teal) |
| soc | Pentagon | 5 | Sapphire | #5fb0d6 (blue) |
| env | Hex variant | 6 | Celestine | #9fd8c4 (ice) |
| voc | Decagon | 10 | Tourmaline | #c9a227 (gold) |
| fin | Octagon | 8 | Topaz | #b0894a (amber) |
| psy | Octagon | 8 | Amethyst | #6b5b95 (violet) |

## Multi-World Toggle (Four Worlds)

The user's requirement: toggle switching based on task engines for personal user, monitoring personal AI, business use, and monitoring business AI.

### UI Implementation (proven working)
- 4 buttons centered at the top of the screen, in a frosted glass panel
- Each button loads a completely different task set on the same 3D structure
- Active button highlighted with gold text on subtle gold background
- Clicking rebuilds the entire column (clear colGroup, rebuild cells)

```javascript
const WORLDS = {
  personal:     { title: 'My Tasks',      tasks: [...], deps: [...] },
  'personal-ai':{ title: 'My AI Monitor', tasks: [...], deps: [...] },
  business:     { title: 'Business',      tasks: [...], deps: [...] },
  'business-ai':{ title: 'Business AI',   tasks: [...], deps: [...] }
};
```

## Phenotype Application (8D Sleep Warm Midnight)

| 8D Sleep Element | Column Crystal Equivalent |
|------------------|--------------------------|
| Breathing glow | Background radial gradient div + pulsing core PointLight |
| Mucha lines | Barely visible SVG curves at 3% opacity behind canvas |
| Grain overlay | body::after noise filter (svg turbulence, 50% opacity, overlay blend) |
| Ultra-thin typography | Inter weight 200-300, letter-spacing 0.02em, tabular numerals |
| Frosted glass panels | backdrop-filter:blur(20px) on all UI overlays |
| Progressive disclosure | Onboarding tooltip, then structure, then click-for-detail |

## Ease-of-Use Requirements

1. **Onboarding tooltip** — centered panel explaining the metaphor in plain language. "Enter" button to dismiss.
2. **Plain language** — no jargon labels. "Start/Defer/Complete" not "DO/DEFER/DONE". Priority percentage not "F=0.18".
3. **2D fallback** — "List View" toggle button for users who find 3D confusing.
4. **Timeline navigation** — vertical segment indicator on the left (Now/Next/Later). Click to focus camera on that segment.
5. **Detail panel** — slides from right on cell click. Frosted glass. Shows task title, dimension, priority, time spent. Start/Defer/Complete buttons.

## Pitfalls to Avoid

1. **NO orbits, NO planets, NO spheres** — user explicitly rejected
2. **NO stacked boxes** — rejected as "Minecraft", not crystal
3. **NO cubes/squares for dimensions** — rejected as "too simple, needs to look crystaly"
4. **NO ring-scattered layout** — rejected as not "flowing upward in time"
5. **NO pre-built cylinder skeleton** — the column only exists where tasks grow
6. **Time must be vertical** — bottom = past/done, top = future/pending
7. **Growth is additive** — column only gains facets, never loses
8. **Tasks stack sequentially** — each task gets its own Y level, building upward

## Related References
- `references/3d-crystal-hive-technique.md` — approved gemstone palette, Three.js material properties
- `references/creative-process-gap-diagnosis.md` — body-part gap analysis for 3D work
- `references/8d-sleep-phenotype-tokens.md` — phenotype DNA to apply