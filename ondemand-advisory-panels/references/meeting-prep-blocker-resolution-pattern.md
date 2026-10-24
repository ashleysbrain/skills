# Meeting Prep Blocker Resolution Pattern

## When to Use
Before any meeting where an advisory panel has flagged a standing blocker that has lingered unresolved for multiple sessions. If you can resolve the blocker with a simulation or computation BEFORE the meeting, you change the meeting from "discuss the problem" to "here is the answer, here is what we do next."

## The Pattern

### 1. Identify standing blockers from session logs
Read the panel's SESSION_LOG.md and STRATEGY_BOARD.md. Look for items flagged as UNRESOLVED, BLOCKER, or carrying a multi-session age (e.g., "still unassigned after 2 weeks"). These are the highest-value targets.

### 2. Assess: can you compute the answer?
For blockers that are mathematical, statistical, or formula-based, you can often resolve them directly:
- "Does the formula break at scale?" → Monte Carlo simulation
- "What is the actual gap?" → Compute it against real population distributions
- "Is the threshold safe?" → Test it across the parameter space
- "Does the competitive claim hold?" → Verify the underlying data

For blockers that are product-direction decisions (should we ship X?), you cannot resolve them computationally. But you CAN produce the evidence that makes the decision easier.

### 3. Build and run the resolution
Import the REAL formula from the canonical codebase (never reimplement). Run the simulation at multiple scales. Produce reproducible output (fixed seed, JSON results).

### 4. Write the meeting decision brief
The brief should have this structure:
- TL;DR: what was the blocker, what did you find
- One section per decision needed, with:
  - The question
  - The evidence (your computation + advisory panel input)
  - Your recommended position and WHY
  - Anticipated pushback and your response
- Meeting rhythm guide: how to sequence the decisions in the allotted time
- Questions you will get (with prepared answers)

### 5. Frame it as conduction, not dictation
You are not telling the user what to decide. You are pacing the meeting so decisions happen in the right order with the right evidence. The user makes the call. You ensure the evidence is in front of them when they do.

## Worked Example: Gamification XP Formula (2026-07-07)

**The blocker**: The Gamification Advisory Board flagged a "4.7x XP gap" from coherence multiplier compounding in Session 2 (2026-06-23). It stayed unresolved for two weeks. Amy Webb kept asking "who owns the simulation?" Nobody did.

**The resolution**: Built a Monte Carlo simulation (50K users, 5 population archetypes, real TWC formula). The 4.7x gap did not replicate. Actual worst case: 3.48x (coherence squared), stable across scales.

**The meeting impact**: Instead of walking into the meeting saying "we still need someone to run the simulation," the user walked in with the answer, the raw data, and a clear recommendation (scoring visibility only for v1, which makes the gap question irrelevant).

**The conduction layer**: The meeting brief sequenced three decisions in priority order, with the XP resolution first (clear the blocker, free the room) before the harder product-direction decision (v1 scope).

## Key Insight
Standing blockers accumulate social weight over multiple sessions. Each session that passes without resolution makes the blocker feel harder to solve. Running the computation yourself collapses the blocker before it gets heavier. This is the highest free-energy action available in meeting prep: the info gain is maximal, the cost is a few hours of simulation.

## Cross-References
- Monte Carlo population stress test technique: `qubit-gr-8d360-scoring-pipeline/references/xp-coherence-stress-test-2026-07-07.md`
- Worked meeting brief: `ds-wave-gamification-advisory-panel-private/MEETING-BRIEF-2026-07-07.md`
