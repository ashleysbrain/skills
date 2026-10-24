# 3D Microtubule Honeycomb Technique

Reference for building tightly-packed hexagonal honeycomb cylinders on a
Three.js surface. Distinct from `3d-crystal-hive-technique.md` (faceted
gemstone growth) and `cylindrical-time-linear-geometry.md` (crystal arms
on vertical axis). This is the MICROSTRUCTURE pattern: many small cells
 tessellating a cylinder skin, one cell per task, fill = completion.

## When to Use

- Task grids / kanban data that is dense (16+ items) and categorical.
- The user says "honeycomb", "microtubule", "tessellation", "hex pattern".
- When you need to show many items at a glance WITH dimension color coding
  AND completion state simultaneously.

## Three Binding Rules (learned 2026-06-27)

### 1. Single layer first. Concentric complexity comes ONLY on user approval.

v1 shipped 3 concentric cylinders (User / Business / AI) plus 6 orbiting
motor proteins. User feedback: "one layer deep as this is too confusing."
Default to ONE cylinder. If the concept calls for multi-stakeholder views,
implement them as a TOGGLE (show one at a time), not simultaneous concentric
rendering. Add concentric layers only after the single-layer version is
approved.

### 2. Default STATIC. Ambient motion destroys legibility.

v1 had: (a) each cylinder auto-rotating at its own speed, (b) 6 motor-protein
nodes orbiting the AI cylinder at 3x speed with fading trails. User feedback:
"this is too much for the human to understand with the movement." The 3D
data viz must be STATIC by default. The only motion should be the user's
manual orbit/zoom (OrbitControls with `autoRotate = false`). Add ambient
animation ONLY when the user explicitly asks for it, and even then prefer
a single subtle motion over multiple simultaneous motion systems.

### 3. Cells must almost touch. Compute hex size from the cylinder geometry.

v1 placed hex cells at `lane_angle = (lane / LANE_COUNT) * 2pi` with a
hardcoded `hexR = 0.42`. The result was loose, gappy, and did not read as
a honeycomb surface. User feedback: "these shapes need to be almost touching."

The correct formula derives hex radius FROM the cylinder so cells tessellate
the surface tightly:

```javascript
const R = 3.5;                          // cylinder radius
const COLS = 8;                          // angular columns (one per 8D dim)
const ANG_STEP = (Math.PI * 2) / COLS;   // radians per column
const ARC = R * ANG_STEP;                // arc length per column on surface

// Flat-to-flat width of a pointy-top hex = r * sqrt(3).
// Set that equal to ARC, solve for r. Multiply by 0.92 for a hairline gap
// so cells stay distinguishable but read as a continuous honeycomb.
const HEX_R = ARC / Math.sqrt(3) * 0.92;

// Row vertical spacing for true honeycomb tessellation = 1.5 * r.
const ROW_SPACING = 1.5 * HEX_R;

// Alternate rows offset by half an angular step so cells interlock.
const offset = (row % 2) * (ANG_STEP / 2);
```

This makes the honeycomb density a FUNCTION of the cylinder, not a guess.

## Completion Fill Encoding (3 discrete states)

Map completion to visual opacity in three bands, not continuous interpolation:

| State        | Completion | Fill opacity | Edge opacity |
|--------------|-----------|--------------|--------------|
| Captured     | < 0.2     | 0.10         | 0.35         |
| In progress  | 0.2 - 0.8 | 0.10 + c*0.90| 0.35 + c*0.65|
| Complete     | > 0.8     | 1.0          | 1.0          |

Use `MeshLambertMaterial` (not MeshBasicMaterial) with ONE DirectionalLight
+ AmbientLight. This gives subtle material variation across the faceted hex
surface that flat MeshBasicMaterial cannot produce — a key anti-AI-telltale
fix (see `references/ai-telltale-design-audit.md` telltale #5). Avoid
MeshStandardMaterial with multiple PointLights (breaks the no-glow rule).
Depth perception comes from the wireframe edges + Lambert shading, not from
expensive lighting setups.

## Extrusion Depth = Time/Effort

Flat hexagons read as "just captured." Taller prisms read as "work has
accumulated." Map extrusion depth to completion + time allotted:

```javascript
const depth = 0.06 + task.completion * 0.32 + (task.timeAllotted / 255) * 0.12;
const geo = new THREE.ExtrudeGeometry(HEX_SHAPE, { depth, bevelEnabled: false });
```

Keep the depth modest. The cells are on a CURVED surface (cylinder); deep
extrusions collide with neighbors. 0.06 to ~0.5 is the usable range.

## Orientation Trick

To make a flat hexagon sit ON the cylinder skin facing outward:

```javascript
mesh.position.set(x, yPos, z);       // x,z on circle of radius R
mesh.lookAt(0, yPos, 0);             // face the central axis
mesh.rotateY(Math.PI);               // then flip to face OUTWARD
```

Apply the SAME position + rotation to the wireframe `LineSegments` so edges
overlay exactly.

## File Location

Working reference implementation:
`opendesign/mockups/task-engine-microtubule/index.html`

Self-contained Three.js, CDN-only, Fleet Atlas phenotype, single cylinder,
tight honeycomb, zero ambient motion.

## Anti-Patterns (do NOT ship)

- 3+ concentric cylinders rendered simultaneously without a toggle.
- Auto-rotating cylinders + orbiting nodes in the same scene.
- Hardcoded hex radius that ignores cylinder circumference.
- `MeshStandardMaterial` with PointLights (breaks the no-glow rule).
- Continuous opacity interpolation across all states (muddy visually;
  the 3 discrete bands read more cleanly).
