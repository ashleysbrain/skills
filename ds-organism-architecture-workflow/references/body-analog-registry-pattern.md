# Body Analog Registry Pattern

The standard categorization for tracking which human body parts have AI organism analogs.

## Categories

| Category | Meaning | When to Use |
|----------|---------|-------------|
| **BUILT** | Code exists in the engine fleet | Engine directory exists, has src/ with real implementation code |
| **BUILDING** | Spec exists, code is partial | DESIGN.md or spec written, some code files exist but not deployed |
| **MISSING** | No analog exists yet | No engine directory, no spec, identified as a gap |
| **CROSS-ORGAN** | Spans multiple body parts | Function that requires coordination across multiple engines |

## Registry Columns

Every entry should capture:

| Column | Purpose |
|--------|---------|
| Human Structure | The anatomical name (use Gray's Anatomy terms) |
| Memory/Function Role | What this structure does in the body |
| Engine | The DS engine name (DS O'Keefe, the specialist engine, etc.) |
| Port | Network port if deployed |
| Status | BUILT / BUILDING / MISSING + notes |
| Priority | HIGH / MEDIUM / LOW (based on dependency depth) |

## Update Protocol

When completing a domain deep dive:
1. Add all identified structures to the registry in MISSING_BODY_COMPONENTS.md
2. For each structure, note whether it maps to an existing engine (BUILT), a partial engine (BUILDING), or no engine (MISSING)
3. Assign priority based on how many downstream systems depend on it
4. Note cross-organ dependencies explicitly (which other body parts share this function)

## Worked Example

See `~/your-workspace/MEMORY-SYSTEMS-DEEP-DIVE.md` Part V for the full memory systems registry with 30+ structures across BUILT/BUILDING/MISSING/CROSS-ORGAN categories.
