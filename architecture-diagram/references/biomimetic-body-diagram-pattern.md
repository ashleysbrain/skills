# Biomimetic Body Diagram Pattern

For the specialist engine engine fleet visualizations that map engines to human body systems on a body silhouette.

## When to Use

The standard skill scope says "look elsewhere for anatomy" but the specialist engine regularly needs body-shaped diagrams showing engines positioned at anatomical locations with flow arrows between systems. This is the pattern for those.

## Structure

1. **Body silhouette** — draw a stylized human (or female for the specialist engine's AI organism = female framing) using a single `<path>` with cubic bezier curves. Keep it abstract, not anatomically detailed. Fill with very low opacity (0.03), thin stroke (#334155).

2. **Engine nodes** — positioned at anatomical locations:
   - Brain/CNS → top center (Wave, Quartz)
   - Heart → upper chest, left of center (Harvey)
   - Immune → upper chest, right of center (Allostasis)
   - Digestive → mid-torso center (Beaumont)
   - Kidneys → lower torso, flanking center (Bright)
   - Reproductive → lower torso center (Reproductive)
   - Skin/Boundary → outer edges (Unna)
   - Skeleton/Registry → side panel (Morphogen)

3. **Future engines** — same positions but with `stroke-dasharray="5,3"` and reduced fill opacity (0.06). Label with "FUTURE" or "PLANNED".

4. **Flow arrows** — use the same arrowhead marker. Color-match to source engine. Dashed arrows for regulatory/feedback paths, solid for primary data flow.

5. **Side panels** — two boxes at bottom: left = body→engine mapping reference, right = fleet status summary.

6. **Annotations** — italic text labels on arrows ("pumps", "signals", "waste →", "→ product") to clarify the physiological metaphor.

## Color Mapping (extend the standard palette)

| Body System | Fill (rgba) | Stroke (Hex) |
|---|---|---|
| Nervous | rgba(168,85,247,0.18) | #a855f7 |
| Autonomic | rgba(245,158,11,0.15) | #f59e0b |
| Cardiovascular | rgba(239,68,68,0.15) | #ef4444 |
| Immune/Homeostasis | rgba(34,197,94,0.15) | #22c55e |
| Digestive | rgba(251,146,60,0.15) | #fb923c |
| Excretory | rgba(236,72,153,0.15) | #ec4899 |
| Reproductive | rgba(219,39,119,0.18) | #db2777 |
| Skeletal/Registry | rgba(34,211,238,0.15) | #22d3ee |
| Integumentary | rgba(148,163,184,0.12) | #94a3b8 |

## Build Pattern (avoids stream timeouts)

1. Write base HTML with `<svg>` containing only the body silhouette `<path>` and grid.
2. Patch in engine nodes (one patch call per batch of 3-4 nodes).
3. Patch in future engine nodes.
4. Patch in flow arrows + annotations + status boxes.
5. Patch in the legend.

Each call stays under the ~8K token limit. Do NOT write the entire SVG in one write_file call.

## Example

See `docs/ai-body-architecture.html` in hydra-os for a working 9-engine + 4-future example with female body silhouette.
