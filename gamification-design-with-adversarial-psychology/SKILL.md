---
name: gamification-design-with-adversarial-psychology
description: Gamification design for health products requiring scientific evidence, adversarial psychology review, and neurobiological rationale. Three-stage pipeline producing branded PDFs.
version: 1.0.0
---

# Gamification Design with Adversarial Psychology Review

## Purpose
Design gamification systems for health products where every mechanic is
scientifically justified, adversarially stress-tested for healthy behavior,
and documented with neurobiological rationale. The user requires that all
gamification techniques drive positive behavioral outcomes with citations,
not manipulation.

## When to Use
- Designing gamification for any DS product (task engine, health app, coaching platform)
- Adding scoring, streaks, levels, achievements, or RPG elements to an existing system
- User asks for "gamification" on ANY product
- Preparing meeting materials about gamification strategy

## The Three-Stage Pipeline

### Stage 1: Design Specialist (Gamification + Domain)
Produce the roadmap wearing the correct specialist brains:
- Yu-kai Chou (Octalysis Framework) for game mechanic design
- the specialist engine (:port, task lattice physics) for the physics-to-mechanic mapping
- Map existing physics concepts (free energy, strain, coupling, critical slowing) to game mechanics
- Design a progression roadmap (Phase 1 basic scoring through Phase 5 full RPG)
- Include a toggle design: gamification_mode as an ON/OFF switch

### Stage 2: Adversarial Psychology Review (MANDATORY)
Spin up psychology specialists with clinical credentials to scrutinize every
mechanic from Stage 1. This is NON-OPTIONAL. The user's binding requirement:
every technique must be healthy, evidence-backed, and neurobiologically
explainable.

Review panel must include:
- A behavioral psychologist (BJ Fogg B=MAP model perspective)
- A dopamine/addiction neuroscience specialist
- A clinical psychologist focused on vulnerable populations
- A red-team anti-gamification advocate

Each mechanic must pass:
1. Does it create intrinsic motivation or extrinsic dependency?
2. What happens to dopamine circuits with prolonged use?
3. Does it punish users for circumstances beyond their control?
4. Is there cited scientific evidence that this drives healthy behavior?
5. What is the neurobiological rationale (explainable to a non-scientist)?

Veto power: the red-team advocate can VETO any mechanic. If vetoed, the
design specialist must redesign or provide overwhelming evidence.

### Stage 3: Branded PDF Output
Final roadmap goes through the creative production spine:
Goethe then Wernicke then Geschwind then Broca then Bell then Luria.

## Physics-to-Game-Mechanic Mapping

The DS task engine already has physics concepts that map to game mechanics:

- Free energy F = cost - T*info_gain: XP gained on task completion (high-priority tasks = more XP). Basis: information-foraging theory (Pirolli and Card, 1999).
- Strain (per dimension): Challenge meter or difficulty indicator. Basis: cognitive load theory (Sweller, 1988).
- Critical slowing down: Warning system for dimensions approaching tipping points. Basis: Scheffer et al., 2009.
- 8D coupling matrix: Cascade effects (improving sleep cascades to psychology). Basis: network theory and coupled oscillator models.
- TWC (Total Wellness Coherence): Overall game state score. Basis: phase coherence in complex systems.

## Critical Constraints from Advisory Panel

### Anti-Gamification Advocate (Red Team) VETO
The coherence multiplier in the XP formula risks punishing users whose health
situations make consistency impossible (chronic illness, caregiving, financial
stress). Mandatory design: Life Context layer. If the system detects a tough
week, pause the coherence penalty and award resilience XP for showing up.

### BJ Fogg (Behavioral Design) Requirements
- Quests during health dips MUST be easier than daily quests (B=MAP model)
- One-tap completion for micro quests under 30 seconds
- Immediate celebration within 2 seconds of completion
- Design for day 45 when novelty wears off, not day 1

### Nir Eyal (Hook Model) Requirements
- Users should move from external triggers to internal triggers over time
- Gamification should eventually become INVISIBLE (habits internalized)
- Notifications spark curiosity, not deliver data
- Variable rewards tied to coherence streaks

### Yu-kai Chou (Octalysis) Requirements
- Emergent quests triggered when dimension scores cross thresholds
- Diminishing returns in XP economy
- Coherence multiplier as a White Hat mechanic (Core Drive 2: Accomplishment)

### Amy Webb (Data Science) Requirements
- Stress-test XP formula at 99th percentile
- Model impact on diverse user populations
- Instrument every feature for 90-day retention
- Quantify any rich-get-richer dynamic

## The Toggle Design

gamification.mode: off | basic | full
- off: pure task engine, no game elements
- basic: scoring + streaks + levels (Phase 1-2)
- full: emergent quests + narrative + RPG (Phase 3-5)

XP formula includes priority multiplier, coherence multiplier (capped at 1.5
with diminishing returns), and life_context_protection flag.

Streak system includes grace_period_days (3) and resilience_xp flag.

Notifications use curiosity style, not data delivery, with
external_to_internal_transition at 60 days.

## Progression Roadmap (5 Phases)

### Phase 1: Basic Scoring (ships first)
Points for task completion, streaks with grace period, levels with non-linear
XP curve. No coherence multiplier yet.

### Phase 2: Achievement System
8D-tied milestones (one tree per dimension), progress visualization, TWC as
coherence display (framed as alignment not score).

### Phase 3: Emergent Quest System
Quests triggered by dimension changes, signal-based quests (easier during
dips), variable rewards, life context layer active.

### Phase 4: Narrative Arcs
Storylines from actual wellness journey (no fictional overlay), narrative
engine reads 8D patterns and frames as story beats.

### Phase 5: Full RPG
Character progression (wellness profile IS character sheet), world state
reflects 8D coherence, story choices equal health decisions, game is invisible.

## Meeting Prep Checklist
1. Run Stage 1 (design specialist) first
2. Run Stage 2 (adversarial psychology) on Stage 1 output
3. Incorporate psychology review feedback
4. Run Stage 3 (branded PDF through production spine)
5. Include 5-7 ADHD-friendly talking points
6. Include advisory panel constraints section

## Pre-Review Staging: Mechanics Extract

Before running any named-scientist review, strip the roadmap to a flat list of
mechanic names grouped by phase and write it as `MECHANICS-EXTRACT.md` in the
panel repo. This prevents the scientist from reviewing phase descriptions,
rationales, or design intent — they review the MECHANIC, not the justification.
A scientist who reads the full roadmap inherits the design team's framing and
is less likely to independently challenge it.

## Per-Scientist Review Output Format

Each named-scientist review follows the standardized output contract documented
in `advisor-panel-orchestration/references/named-scientist-review-output-format.md`.
Read that file before producing a review. The format: ~5-line theory primer →
per-mechanic numbered field analysis (3 core fields: VERDICT / REQUIRED CHANGES
/ CITATION, plus theory-specific fields that vary by scientist — e.g., Wood v3
uses 6 fields: HABIT TRANSFER IMPACT / CONTEXT STABILITY / SUNSET CONDITION /
VERDICT / REQUIRED CHANGES / CITATION) → summary tally table with guiding
principle. Target ~120 lines for a Phases 0-2 review (11 mechanics).

## Pitfalls
- **VERIFY MATH AGAINST SOURCE CODE, NOT MEMORY.** When documenting gamification systems for the team, always read the actual engine source files (task_engine.py, schultz_rpe.py, bragg engine.py, twc_coupling_physics.py) and extract the real formulas. Do not paraphrase from memory. The team needs to see actual code-verified math, not approximations.
- **INCLUDE ENGINE NAMES WITH DS-ECS CODES.** Team-facing gamification docs must name the engines behind each component (the specialist engine DS-ECS-SUB-04.11.01, the specialist engine DS-ECS-NPR-13.01.07, the specialist engine DS-ECS-SUB-04.09.01, the specialist engine DS-ECS-NPR-13.01.01) so the team knows what we are pulling from.
- **TEAM-FACING DOCS: DESCRIBE IDEAS, NOT AGENT WORK.** When producing team documents, describe the system ideas and the science behind them, attributed to real researchers at real institutions (Baumeister at Queensland, Wood at USC, Berridge at Michigan, Schultz at Cambridge). Do not mention AI agent names, engine internals, or review processes.
- Proposing gamification WITHOUT adversarial psychology review (binding requirement)
- Using coherence multiplier without life context protection layer (red team VETO)
- Making quests harder during health dips (BJ Fogg B=MAP violation)
- Designing for day 1 instead of day 45+ habit formation
- Delivering data in notifications instead of sparking curiosity
- Creating fictional narrative separate from actual wellness journey
- Shipping Phase 1 without grace period in streaks
- Proposing ECS codes without querying live registry
