# Competitive Design Research — 3D/Spatial Task Apps

## When This File Was Created
2026-06-27. The user asked: "we need to find other 3d design dashboards out there. what else is out there that we can gather inspiration from?"

## The 8 Apps Audited

### Category 1: Spatial Canvas (closest to what DS needs)

**Taskade** (taskade.com) — AI workspace with mind map, kanban, org chart, and action views that you toggle between. Not fully 3D but multi-view switching done well. Clean, not gamified.
- *Steal:* the seamless view toggle without page reload.

**Neural Flow 3D** (iOS) — 3D mind-mapping app. Nodes float in 3D space, you rotate through your idea graph.
- *Steal:* the "ideas float in space you can orbit through" feeling.

**Obsidian Graph View + 3D Graph Plugin** — Force-directed node graph of notes. Click a node = highlight connections + open note. The 3D plugin makes it fully navigable. Closest existing thing to "structure grows as you work."
- *Steal:* bidirectional graph-node interaction, the way structure emerges organically from content.

**IVGraph for Notion** — 3D graph view of Notion workspaces.

### Category 2: Growth / Reward (the grow-from-accomplishment model)

**Finch** (self-care app) — A bird grows as you complete self-care tasks. Color-coded rainbow system ensures dimensional balance. The visual growth IS the motivation. Highly successful.
- *Steal:* the rainbow/balance color system maps directly to 8D. Growth IS the reward, not a side effect.

**Forest** (forestapp) — Plant a virtual tree when you start a task. Tree grows while you work. Over time you build a forest.
- *Steal:* the "accumulate over time" visual. Our version: honeycomb grows, never dies.

**Habitica** — RPG gamification of habits/tasks. Avatar, gear, quests.
- *Anti-pattern:* too gamey, loses professional users. Don't go full RPG. Keep it abstract-beautiful, not character-based.

**Duolingo** — The skill tree. Completed lessons light up.
- *Steal:* the branching path visual where completed sections glow.

### Category 3: Real 3D Data Dashboards (pro tools)

**deck.gl / Kepler.gl** (Uber open-source) — Large-scale 3D geospatial visualization. Hexagonal aggregation layer. Used in production.
- *Steal:* the hexagonal aggregation layer. This is the "real product" version of what we're prototyping.

**Mapbox Studio** — 3D map data layers. Three-column layout (layers | canvas | properties).
- *Steal:* the three-column pro-tool layout.

**Holographic Media Dashboard** (GitHub: Morlock52) — Three.js real-time 3D server monitoring. Shows Three.js CAN look professional.

### Category 4: Calm Task Management (the anti-AI-design reference)

**Things 3** — The gold standard for calm, beautiful task design. No decoration. Functional typography and whitespace.
- *Steal:* the calm. The restraint. Our 3D should feel this calm, not busy.

**Linear** — Extreme density, keyboard-first. Color is the only visual encoding.
- *Steal:* density without clutter. Color does the work.

**Lunatask** — Privacy-focused, energy-aware scheduling. ADHD-popular.
- *Steal:* energy-awareness dimension. Tasks reorder based on energy level.

## What Makes Things Look AI-Generated (AVOID)

1. Saturated neon colors on dark backgrounds with glow effects
2. Too many elements visible at once (cognitive overload)
3. Uniform geometry (every cell identical — real data is messy)
4. Decorative elements that don't encode information
5. Dark mode with neon accents (the universal AI mockup look)
6. Inter font (the Helvetica of AI slop)
7. Frosted glass panels with backdrop-filter blur
8. Rounded corners everywhere (border-radius: 4-16px)
9. Breathing/glow animations on static content
10. Hint text floating in the corner ("drag = orbit")

## What Makes Things Look Human-Designed (EMULATE)

1. **Things 3 / Linear:** Calm, restrained, functional typography
2. **Finch:** Warm, playful but not childish, color encodes balance
3. **deck.gl:** Professional density, real geometry, no decoration
4. **Obsidian:** Structure emerges from content, not imposed on it

## Design Principles Extracted (embed in all future DS product design)

1. The 3D/spatial element is always OPTIONAL and SECONDARY. The primary interface is a fast, clean list.
2. The visual structure is a "reflection view" you visit occasionally.
3. Growth should be monotonic (never punishes, never shrinks).
4. Color should encode information (dimension), not decoration.
5. Warm tones over cool tones. Garden at dusk, not sci-fi terminal.
6. System fonts (Helvetica Neue / system-ui), NOT Google Fonts CDN.
7. Sharp edges (0-2px radius), not rounded. Lines, not cards.
8. Dense data, not sparse demo. Real products have 50-200 items visible.
9. One light source in 3D, not ambient fill.
10. Post-processing grain, not noise-free renders.
