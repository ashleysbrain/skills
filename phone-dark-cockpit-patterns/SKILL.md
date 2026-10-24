---
name: phone-dark-cockpit-patterns
description: Build phone-first dark dashboards.
version: 1.0
author: the specialist engine
license: MIT
metadata:
  hermes:
    tags: [design, mobile, dark-ui, mosaic-os]
    related_skills: []
---

# Phone Dark Cockpit Patterns

## When to Use

Use when building or refining phone-first dark operator dashboards (the OS app_shell_v3 and successors).

Canonical spec: `/<workspace>` (15 ranked patterns, each with exact px/ms/opacity/easing and an apply-target). Built 2026-10-04 from 12 primary sources.

## Core rules (memorable subset)

1. One hero number owns the screen (Flighty: 32-40px bold tabular; everything else demoted).
2. Status = tinted fill chips (13px w700 uppercase on 14-20% tint of own color, pill radius), never uniform outlines.
3. Press physics on every tappable: scale(0.98) + one-step surface lift, 120ms ease-out-expo; nothing over 250ms (Linear: over-250ms feels broken). Ease-out-expo = cubic-bezier(0.16,1,0.3,1).
4. Aliveness = 3-4% visibility motion gated by real state (breathing glow only when work pending; stillness when clear). Heavy 45%+ box-shadows read as bugs, not life.
5. Lists are hairline rows (1px at 7% accent), not grids of identical boxed cards. Boxes only for containers.
6. Month grids: 4px event dots (sage=1-2 items, gold=3+, pulse=overdue) + today ring 1.5px, not flat borders.
7. Type scale: max 5 sizes with committed jumps (e.g. 13/15/22/40). Light-on-dark: +0.05 line-height, +0.01em tracking, weight floor 500 under 14px.
8. Stagger lists on render: 30ms/item capped at 12 items, rise 8px + fade, 240ms ease-out-expo. Always honor prefers-reduced-motion.
9. Exactly one filled-accent element per screen; asymmetric hero stack (1 tall + 2 short). Uniform card grids are the AI-look tell.
10. Empty states: symbol + title + guidance + CTA, inward shadow; never a dashed gray box.

## Sources

awesome-ios-design-md DESIGN.md specs (Linear #08090A canvas, 44pt rows, 90-240ms motion; Flighty #0B0B0F, tabular data, status chips on 15% tints; Things 3 checkbox ritual 500ms, ring progress), Apple HIG (44x44pt targets, tab bar blur/capsule, empty-state structure), Notion Calendar (5.3:1 type ratio, 9%-opacity grid lines), Amie (0.3s entries, 0.05s staggers), Meridian terminal patterns (market breathing 3-4%, empty-state gravity).
