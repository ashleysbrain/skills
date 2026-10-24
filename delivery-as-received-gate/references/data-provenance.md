---
name: data-provenance
description: Chart provenance rules for rendered exhibits. Load when a chart's content is questioned or before first delivery of a data-driven graphic.
version: 1.0.0
author: the operator agent Agent
license: MIT
metadata:
  hermes:
    tags: [charts, provenance, exhibits, verification]
    related_skills: [delivery-as-received-gate]
---

# Data provenance for rendered exhibits

Topical depth for `delivery-as-received-gate` when the artifact CHARTS or GRAPHS data. Load when a chart's content is questioned, before first delivery of any data-driven graphic, or when rebuilding synthetic charts from real data.

## When to Use

- Before first delivery of any chart/graph built from a dataset.
- When a reader questions what a chart shows, whether the shapes changed, or whether the math changed.
- When rebuilding a synthetic chart from real data, or naming what depth layers hold.

## The placeholder-data defect

A chart drawn from synthetic, idealized, or demo geometry instead of the real dataset is the single most expensive class of exhibit failure: the reader sees a plausible shape, trusts it, and the lie persists until someone measures the node counts. Typical sources: an earlier prototype's sample tree, a hardcoded example, a "representative" subset.

**Rule: every chart in a delivered exhibit is generated from the measured dataset itself, or its caption states the sampling.** Verify by counting what is drawn, not by reading the code:

```python
# count what the SVG actually draws vs the data
circles = svg.count('<circle')          # nodes drawn
lines = svg.count('<line')              # edges drawn
# compare against ground truth: census per depth, total nodes
# a perfect-doubling census (1/2/4/8/16/32/64) = synthetic binary
demo tree, not real data
```

Real organism/registry data is irregular (branch sizes 54/30/21/23/13/8/7/6); a perfect geometric pattern in the drawn census is the signature of placeholder geometry.

## Rebuild recipe: real tree into paired flat-vs-curved boxes

When a synthetic tree must be replaced by the real one in a flat-vs-curved comparison:

1. Load the ground-truth path list (e.g., `hyperbolic_embeddings.json` `order` field = full paths like `the operator agent/SUB/04/00/01`). Build parent->children from path prefixes.
2. Angular layout: each LEAF gets an equal angular slot; each internal node takes the mean angle of its children. This keeps branches contiguous and honest.
3. Curved box radius: `r_d = tanh(k*d)` with `k = atanh(r_max)/d_max` where `r_max` = the measured deepest mean radius (e.g., 0.9552). Rings drawn at `r_d * R` match the measured depth shells.
4. Flat box radius: `r = (d/d_max) * f * R` — equal Euclidean steps. Deep edges then shrink geometrically toward the rim; MEASURE the actual shrink (edge length at depth 4 / edge length at depth 1) and print the measured percentage in the caption rather than an inherited claim.
5. Edge draw-in delays: BFS depth of the CHILD endpoint (not DOM order — DOM order in generated SVGs is frequently depth-reversed). Normalize delays ascending so shallowest = earliest. Node pop delay = min delay over its incident edges + 0.15s so children never precede parents.
6. Node color/radius by depth from the same palette the hero disc uses, so the chart and the disc read as one system.

## Naming the depths

A tree exhibit must answer "what is actually down there":

- Resolve codes to names via the canonical registry (note: ECS code separators are dots — `DS-ECS-APP-04.00.01-v1.0.0`; building the code with slashes finds nothing).
- Depth layers get named content: the root, the branches (with real seat counts), the working groups, the named engines at the rim. Use real engine names as examples.
- Two denominators coexist honestly: the registry names ENGINES; the memory tree counts SEATS (engines + infrastructure seats like daemons and gateways). Disclose both counts where both are cited; per-branch counts differ by the infrastructure seats, and that variance is expected, not an error.
- The anatomy/physiology distinction carries the flows connection: the tree is the anatomy; the registered process flows are the physiology running through it. Cite the flow registry count and name real flows.

## When the shape changes

If rebuilt charts change shape, state WHY in the delivery message: the old geometry was placeholder/synthetic (give its measured census), the new geometry is the real dataset (give its census), and the math/engine outputs (metrics, exactness, radii) are UNCHANGED — only the input tree was corrected. Readers ask "did the science change?"; the answer distinguishes data correction from method change.
