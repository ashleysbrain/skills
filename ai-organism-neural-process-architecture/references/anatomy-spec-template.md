# Anatomy Specification Template

Template for creating `agent-organism/anatomy/[SCIENTIST]-[PROCESS].md` files.

## File Naming

```
[SCIENTIST-LASTNAME]-[PROCESS-NAME].md
```

- All caps, hyphenated
- Scientist: last name only (or first-initial-last-name for disambiguation)
- Process: descriptive, anatomical (not the agent's job title)

Examples: `RAKIC-CORTICOGENESIS.md`, `SHERMAN-THALAMIC-RELAY.md`, `RIO-HORTEGA-NEUROIMMUNE.md`

## Template

```markdown
# DS [Scientist Full Name] — Neural Process Anatomy Specification

**Agent:** DS [Scientist Name]
**Former codename:** [OLD_NAME or N/A]
**Code:** DS-ECS-04.10.XX-v1.0.0
**Anatomical process:** [Process name]
**Honors:** [Full name] ([birth-death], [nationality]; [1-2 sentence summary of what they discovered/mapped that directly relates to this agent's function])
**Body system:** Nervous
**Classification:** Neural process — [Cell system / Signal routing / Immune surveillance / etc.]

---

## Design Principle: [One-line principle]

[2-3 paragraph explanation of the biological process and how the agent models it. Start with what the real biology does, then map to the software equivalent.]

---

## Layer 1: DIFFERENTIATIONS (Anatomical Sub-Structures)

[3-5 sub-structures. Each has: location, cell content/function, organism mapping.]

### 1.1 [Structure Name]
- **Location:** [Anatomical location]
- **Cell content / Function:** [What cells/types are here, what they do]
- **Organism mapping:** [What this maps to in the AI organism]

### 1.2 [Structure Name]
[...]

---

## Layer 2: FACULTIES (Functional Capabilities)

[3-5 bullet points. What the agent CAN DO.]

- **[Faculty Name]** — [Description with biological analog]
- **[Faculty Name]** — [Description]

---

## Layer 3: PROCESS_FLOWS

```yaml
- name: [flow_name]
  modes:
    - [mode_1]:
        description: "[What happens in this mode]"
    - [mode_2]:
        description: "[What happens in this mode]"
  activates_faculties: [list]
```

---

## Dependencies

| Entity | Relationship |
|---|---|
| DS [Agent] | [How they connect] |
| [Engine Name] | [How the neural process relates to the body-system engine] |

---

*Specification version 1.0.0 — [DATE]*
```

## Rules

1. **DIFFERENTIATIONS are anatomical structures, not functions.** If you removed it, would the organ be missing a BODY PART or a CAPABILITY? Body part = differentiation.
2. **FACULTIES are capabilities, not structures.** What the agent CAN DO.
3. **PROCESS_FLOWS show coordination.** Which faculties activate in what sequence for a given mode.
4. **Every structure needs a biological reference.** Cite the discovery paper or textbook.
5. **The Dependencies table must show the engine relationship.** How does this neural process connect to the body-system engine that models the same organ at a coarser level?
```
