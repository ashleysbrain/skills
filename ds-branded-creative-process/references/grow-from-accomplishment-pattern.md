# Grow-From-Accomplishment Pattern

## Origin
User correction via sibling-agent (operator bus msg 838, 2026-06-27): "this feels very overwhelming. I want them to take tasks and build the structure by accomplishing tasks but this feels overwhelming."

## The Problem
Pre-existing complex 3D structures (microtubule cylinders, concentric stacks, orbiting nodes) impose cognitive load that exceeds what a task interface should demand. The user shouldn't have to LEARN a structure.

## The Pattern

### 1. LIST IS THE DEFAULT VIEW
The user lands on a clean, calm task list (Things 3 aesthetic). This is where the user WORKS. Simple, fast, familiar.

- Ordered by AI priority, then 8D balance
- Dimension color dots inline
- Verdict badges (DO / DEFER / WATCH)
- Capture bar at bottom
- Next-best-action hero at top

### 2. THE 3D STRUCTURE DOES NOT PRE-EXIST
It GROWS FROM ACCOMPLISHMENT:
- Start: a list + a single empty hexagonal cell
- Task completed → a cell FILLS with the task's 8D dimension color
- More tasks completed → cells CONNECT, patterns EMERGE, the structure GROWS
- The structure IS the user's progress made visible — like a crystal forming, a honeycomb being built, a coral reef growing

### 3. THE STRUCTURE IS A REWARD, NOT A TOOL
- Like a Tamagotchi for productivity — feed it tasks (complete them) and it grows
- Like a zen garden — it grows as you tend it
- The user never needs to understand the biology (hexagonal/microtubule/DNA). They just see their structure growing
- The shape naturally reflects 8D balance (lopsided = one dimension dominating; balanced = fuller)

### 4. AI TASKS = COMPANION GROWTH
- AI tasks are visually distinguishable (slightly different texture/pattern, not competing color)
- The user sees "I built 12 cells, my AI grew 8 alongside me"
- Partnership, not competition

### 5. TOGGLE BETWEEN VIEWS
- List = work mode (get things done)
- Crystal = reflection mode (see what you've built)
- Vitals = health mode (8D dimension bars)
- Toggle is instant (Taskade pattern), no page reload

### 6. GROWTH IS MONOTONIC (ADIABATIC)
- Never shrinks, never punishes
- Add a "tend" mechanic: revisiting a task, checking in on an in-progress item, or logging a small reflection ALSO feeds the structure (smaller cell, partial fill)
- This prevents the "streak anxiety" problem that kills Habitica adoption
- Growth is slow and steady (adiabatic principle)

## Science Remains the Inspiration (Not the Interface)

- Hexagonal cells = the growth unit (from microtubule/grid-cell research)
- Dynamic instability = cells grow/pause/collapse (SIMPLIFIED: complete = solid, in-progress = transparent, abandoned = gone)
- DNA packing = natural zoom (day → week → sprint → year — but ONLY if the user zooms; not default)
- The user SEES simple beauty. The SCIENCE powers it underneath.

## Implementation Notes

- Completed task = cell appears (grows in over 0.5s ease-out animation)
- Cells cluster by 8D dimension (8 regions of the structure)
- Color fill = completion. Wireframe = open. Filled solid = done.
- Balance score = how evenly distributed across 8D (variance calculation)
- MeshBasicMaterial (not Lambert — see MeshLambertMaterial invisibility pitfall)
- Demo data fallback for file:// protocol (see Static HTML pitfall)

## What NOT to Do

- Do NOT pre-build a complex cylinder/sphere/orbit structure and fill it
- Do NOT make the 3D view the default
- Do NOT add ambient rotation or motor-protein animation
- Do NOT punish the user for missing days (no collapse, no shrinkage)
- Do NOT require the user to understand the biology
