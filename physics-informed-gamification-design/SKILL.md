---
name: physics-informed-gamification-design
version: 1.0.0
description: >-
  Design gamification and engagement layers for physics-informed health/wellness products.
  Maps physics concepts (free energy, strain, critical slowing, coupling matrices, coherence)
  to game mechanics (XP, quests, achievements, narrative arcs, RPG progression). Includes
  advisory-panel-tested constraints: Red Team dignity checks, B=MAP difficulty model,
  tri-mode guardrails, coherence multiplier safety, and the invisibility principle.
trigger: >-
  When designing gamification, engagement mechanics, XP systems, quest systems, achievement
  systems, progression systems, or any game-like layer for a health/wellness product that has
  a physics-informed scoring engine underneath. Also when mapping physics concepts to game
  mechanics, designing the toggle between gamified and non-gamified modes, or producing
  gamification roadmaps for products like 8D360, the specialist engine, Divinity Health, or similar.
tags:
  - gamification
  - physics-informed
  - game-design
  - health-tech
  - engagement
  - xp-systems
  - quest-design
  - octalysis
  - behavioral-design
---

# Physics-Informed Gamification Design

## When to Use

- Designing gamification for a health/wellness product with a physics-based scoring engine
- Mapping physics concepts (free energy, strain, coupling, critical slowing, TWC) to game mechanics
- Designing XP formulas, quest systems, achievement systems, or progression mechanics
- Producing gamification roadmaps with phased rollout plans
- Designing safety guardrails for gamified health products (off modes, quiet modes, dignity checks)
- Preparing meeting talking points or briefs for gamification advisory panels
- Wearing dual specialist brains (physics engine owner + gamification framework expert)

## The Core Thesis

The gamification does not get bolted on. It **emerges** from the physics the scoring engine already computes. Every physics concept already has a game-mechanic shadow. The design work is turning the lights on — mapping each physics signal to a game-readable experience layer.

The gamification layer is a **projection** of physics state into game-readable signals. It never changes the physics. It only changes how the user *experiences* the physics.

## The Physics-to-Game-Mechanic Mapping Methodology

This is the core methodology. For each physics concept in the underlying engine, map it to a game mechanic:

### 1. Free Energy → XP Reward / Quest Energy

`F = cost - T × info_gain` (cost = priority + age; T = priority weight; info_gain = 1 on completion)

| Physics State | Game Mechanic |
|---|---|
| High F (stale, high-priority, undone) | "Boss Task" — big XP payoff when completed |
| F drops sharply on completion | The dopamine moment — visceral celebration |
| Low F (fresh, low priority) | "Quick Win" — small XP, easy completion |

**Design rule:** XP reward ∝ |ΔF| (magnitude of free energy drop). Completing a stuck task gives more XP than a fresh task. This rewards **clearing bottlenecks**, not **churning easy tasks**. This is the anti-volume differentiator: reward quality (resolving stuck energy), not volume (tasks completed).

### 2. Strain → Dimension Stress / Threat Level

`strain = stuck_free_energy + blocked_penalty + critical_slow_boost`

| Physics State | Game Mechanic |
|---|---|
| Strain < 0.35 | 🟢 "Stable" — dimension in ground state |
| Strain 0.35-0.60 | 🟡 "Under Load" — tasks accumulating |
| Strain 0.60-0.85 | 🟠 "Strained" — system suggests product, quests trigger |
| Strain > 0.85 | 🔴 "Critical" — emergency quests (EASY mode) |

**Design rule:** Strain never punishes — it **activates support**. High strain → product suggestions, easier quests, resilience XP. System says: *"We see you. Showing up right now matters more than being perfect."*

### 3. Critical Slowing Down → System Warning / Emergency Quests

`Scheffer signals: rising variance + rising AR(1) = approaching tipping point`
`Task age > 72h in a dimension = critical_slow flag`

**Design rule (B=MAP model):** When critical slowing is detected, quest difficulty drops to **trivially easy**. The user's motivation is at its lowest. B = M × A × P. Motivation (M) is low, so Ability (A) must be maximally easy (one-tap, <30 seconds) and Prompt (P) must be gentle, not alarming.

### 4. Coupling Matrix → Resonance Network / Synergy Bonuses

`COUPLE = [(sleep, psychological), (financial, psychological), ...]`
`TWC = η × μ × C × (1 + 0.5 × S) where S = synergy tensor`

| Physics State | Game Mechanic |
|---|---|
| Coupled dimensions improving together | "Resonance Bonus" |
| Strain propagating across coupled dimensions | "Cascade Warning" |
| User discovers a coupling link | "Coupling Discovery" achievement |

**Design rule:** The coupling matrix is the **competitive moat**. Every coupling discovery is a curiosity moment. The user feels like the system *understands* them, not like it's counting them.

### 5. TWC (Total Wellness Coherence) → Character Level / World State

`TWC = η × μ × C × (1 + 0.5 × S)`

| Physics State | Game Mechanic |
|---|---|
| TWC score (0-100) | "Level" — master progression stat |
| Coherence C | "Resonance" — diagnostic, NOT XP multiplier (see Safety) |
| Synergy S | "Flow State" — rare bonus state |
| TWC rising | "World is brightening" |
| TWC falling | "World needs attention" (never "you're losing") |

## The Toggle Design

Gamification operates as a projection layer with a mode switch. The physics **always** runs.

```
gamification_mode: "off"      → Pure physics. No user-facing game elements. Data flows silently.
gamification_mode: "standard" → Scoring + XP + quests + achievements (phased rollout)
gamification_mode: "full"     → RPG layer: narrative, world, character progression
```

Every layer (XP, quests, achievements, narrative) can be independently disabled. `gamification_mode: "off"` exists from day one — this is non-negotiable for health products.

## The Phased Rollout Pattern

Health gamification must start invisible and earn the right to add mechanics.

### Phase 0: Scoring Visibility (ships first)
Show cause-and-effect: *"You slept 7.5 hours. Sleep +3 points. Here's why."* No XP. No badges. No quests. Just truth, made visible. This validates the Hook loop with real data before any game math ships.

### Phase 1: Basic Scoring
Flat XP (= raw score, NO coherence multiplier), per-dimension streaks, levels. Only after Phase 0 data proves scoring visibility drives retention.

### Phase 2: Achievements
Dimension-tied milestones. Include **Resilience XP** (showing up during hard weeks) and **Recovery Badges** (dimension recovers from critical slowing) as alternatives to coherence-penalty mechanics.

### Phase 3: Emergent Quests
Triggered by physics events (dimension threshold crossings, multi-dimensional shifts, critical slowing). Ships with tri-mode guardrails or doesn't ship.

### Phase 4: Narrative Arcs
Storylines generated from actual dimension trajectories. Monthly "chapters" in second person. Pull-based, not push-based.

### Phase 5: Full RPG (12-18 months)
Skill trees, world state, companions. **Invisible gamification** — the user doesn't feel like they're playing a game.

## Safety: Non-Negotiable Guardrails

These come from advisory panel sessions and red-team vetoes. They are NOT optional.

### The Coherence Multiplier Veto
Never use coherence (consistency) as an XP multiplier in early phases. Chronically ill users, caregivers, people in financial stress have low coherence through no fault of their own. Multiplying XP by coherence punishes them for circumstances.

**Resolution:**
- Phase 1: XP = flat score. Coherence = diagnostic insight in UI only.
- Phase 2+: Coherence may go on XP **only if** real population data proves it motivates. If used, apply log-diminishing returns above 80th percentile + resilience XP for detected hard periods.
- Stress-test any XP formula at 1K/10K/50K simulated users before shipping.

### The Tri-Mode Guardrail (for emergent quests)
Users with chronic conditions will trigger multi-dimensional shift alerts constantly. Without guardrails, the system becomes surveillance of suffering.

1. **Active mode:** For users with stable baselines. Shifts trigger curiosity quests.
2. **Quiet mode:** User-flagged OR system-detected (high dimension variance → auto-default). Shifts are logged but not pushed. Weekly summary: *"Your wellness data showed some shifts. Explore when ready."*
3. **Off mode:** Scoring runs silently. Gamification completely dark.

**Auto-default logic:** If any dimension shows variance > 2σ over 14-day window → auto-quiet. Quiet mode can NEVER be overridden by the system — only by the user.

### The B=MAP Difficulty Model
During health dips (critical slowing, high strain), quest difficulty drops to trivially easy. One-tap completion. <30 seconds. Immediate celebration within 2 seconds. The user needs a WIN, not a challenge, when they're struggling.

### The Dignity Check
Every mechanic must pass: *Would a vulnerable user feel respected or controlled?* If "controlled," redesign or cut.

Test against these personas: single parent with chronic pain, bipolar user with natural mood swings, postpartum mother with destabilized dimensions, autoimmune patient during flare-ups, person in financial crisis.

### The Off Switch Principle
*"A health product that cannot be silenced is a health product that harms."* Every gamification layer has an off switch from day one. Data still flows to the scoring engine silently.

## The Hook Cycle (One Sentence)

The core engagement loop, stated in one sentence:

> *"Your score changes, you see what shifted and why, you log one behavior that refines your baseline."*

This is Trigger (score change) → Action (open app) → Variable Reward (discover cause-and-effect) → Investment (log behavior). A complete Hook cycle without a single badge.

## Meeting Talking Point Format (ADHD-friendly)

When producing meeting prep for gamification decisions, use this format:

- 5-7 bullets maximum
- Each bullet starts with an emoji + bolded headline
- One sentence of explanation per bullet
- End with the one-sentence Hook cycle for the room
- No walls of text. Glanceable. Punchy.

## Wearing Dual Specialist Brains

When the user asks you to wear two specialist brains simultaneously (e.g., "you are X and Y"):

1. Read the actual source code and documents that each specialist owns
2. Do not roleplay from general knowledge — ground every claim in real code/files
3. Synthesize the two perspectives into a single coherent deliverable, not two separate sections
4. The output should feel like two experts collaborated on one document, not two documents stapled together

## Advisory Panel Constraints Reference

For the full set of advisor-specific requirements (Yu-kai Chou, BJ Fogg, Nir Eyal, Amy Webb, Anti-Gamification Advocate), see `references/advisory-panel-gamification-constraints.md`. This includes:
- Each advisor's specific requirements and what they vetoed
- The XP formula stress test methodology and results
- The vulnerable user persona gallery
- The competitive landscape scan findings

## Habit Formation Review Framework

When reviewing gamification mechanics through a habit-formation lens (Wendy Wood: dorsal striatum transfer, context-response repetition), see `references/habit-formation-review-framework.md`. This includes:
- The three review dimensions: habit transfer, context stability, sunset condition
- Per-mechanic verdicts for all Phase 3–5 mechanics and all 5 physics-to-game mappings
- Ship-readiness assessment format (CONDITIONAL APPROVE / VETO per phase)
- The automatic graduation principle (Schultz RPE sunset: when Δ→0, gamification fades)
- The critical missing feature: gamification must sunset itself based on automaticity signals

## Related Skills

- `physics-informed-ai-health-scoring` — physics-based dimension derivation and self-healing loops (AI fleet focus)
- `8d-predictive-behavior-model-design` — trajectory prediction and regime detection for 8D scoring
- `advisor-panel-orchestration` — designing and running advisory panels with named personas
- `adversarial-strategy-stress-testing` — red-team methodology for strategy validation

## CRITICAL: Review the ACTUAL BUILT SYSTEM, Not Planning Documents

The single most expensive error in gamification review work: dispatching specialist
reviewers against a PLANNING DOCUMENT (what might be built) instead of the ACTUAL
BUILT SYSTEM (production code that already exists). This happened on 2026-07-07:
four elite scientists reviewed GAMIFICATION-ROADMAP.md (a future design doc with
"flat TWC = XP") while the ACTUAL system already had a five-multiplier XP economy,
a Goals > Quests > XP hierarchy, a Bragg crystal lattice, a Schultz RPE module,
and a resonance engine. Every verdict was invalid because the source was wrong.

**The rule:** Before dispatching ANY specialist review of a gamification system:
1. Find the ACTUAL production code (task_engine.py, bragg engine, schultz_rpe.py,
   the XP formula in the codebase, the 8D scoring engine)
2. Find the architecture documents (ARCHITECTURE.md, CASE_FILE.md, INTEGRATION.md,
   PRODUCT_THESIS)
3. Read them yourself and extract the ACTUAL system into a compact context block
4. Pass that context to each specialist. Tell them: "This is the ACTUAL BUILT
   SYSTEM, not a planning document."
5. Do NOT pass planning/roadmap documents as review source material unless the
   user explicitly says "review the roadmap"

**The actual XP formula (from CASE_FILE.md):**
`xp_reward = base_xp × coherence_multiplier × difficulty_multiplier × confidence_multiplier × pacing_multiplier`

This is NOT "flat TWC = XP." It has FIVE multipliers. The coherence multiplier
IS present in the actual system (it was only vetoed in the planning doc's Phase 1).
Reviewers must see the real formula.

**The actual experience hierarchy:**
Goals > Quests > XP. Three separate concepts. XP = single action reward.
Quest = multiple XP events grouped. Goal = multiple quests grouped.
Harada Mapping: 1 goal > 8 pillars/quests > 8 actions each.

**The actual habit loop chain:**
Bragg (select action via lattice settling) → Schultz (RPE on completion) →
Carlsson (reinforcement learning) → Dale (broadcast). Every game mechanic sits
ON TOP of this chain.

See `references/actual-built-system-architecture.md` for the complete system
extract to use as review context.

## Pitfalls

- **Do NOT review planning documents when the actual system is already built.** Read the production code first. The XP formula, quest hierarchy, and engine chain in the codebase ARE the system. The roadmap describes what MIGHT be — it is not the system. (2026-07-07: all four specialist reviews were invalid because they reviewed a roadmap instead of the built system.)
- **Do NOT use coherence as an XP multiplier without stress-testing at scale.** The gap between healthy and chronically ill users can exceed 3x. Run the simulation at 1K/10K/50K users before committing.
- **Do NOT ship emergent quests without tri-mode guardrails.** Users with chronic conditions will experience them as surveillance of suffering.
- **Do NOT make quests harder during health dips.** B=MAP model: motivation is lowest, so quests must be easiest. One-tap, <30 seconds, immediate celebration.
- **Do NOT use loss aversion mechanics (streak shame).** No "you lost your streak!" notifications. Streaks are celebrated when active, silently paused when broken.
- **Do NOT require social comparison.** All achievements private by default. Social features require explicit opt-in.
- **Do NOT skip the scoring-visibility-only phase.** Before any XP, quests, or badges ship, validate that showing cause-and-effect drives retention. The gamification IS the scoring at first.
- **Do NOT invent physics-to-game-mechanic mappings from general knowledge.** Read the actual engine code (function signatures, constants, formulas) and ground every mapping in real computation.
- **Do NOT forget the invisibility endgame.** By month 6+, gamification should fade. External triggers diminish. Habits internalize. The scoring engine becomes ambient intelligence.
- **Do NOT reward free energy resolution as user-facing XP.** Free energy quantifies surprise — the opposite of the stable, predictable context-response loop that habits require. Rewarding its resolution keeps behavior in the deliberative/prefrontal system. Use free energy as an internal diagnostic only.
- **Do NOT use TWC as a user-visible "level" during the first 66 days of any dimension.** The coherence factor C penalizes variance, which is NORMAL during habit acquisition. Punishing inconsistency during the formation period directly counteracts the repetition loop.
- **Do NOT fire quest notifications mid-streak as "keep going" prompts.** A mid-streak notification disrupts the very automaticity it celebrates by injecting novelty. Fire quests retrospectively after the pattern is confirmed.
- **Do NOT design RPG elements (skill trees, world state) for users with consolidating habits.** RPG framing makes behavior remarkable — the opposite of automaticity. Restrict to opt-in "entertainment mode" mutually exclusive with active habit-formation pathways.
- **Do NOT omit automatic graduation.** Every gamification mechanic must have a sunset condition tied to automaticity signals (Schultz RPE: when prediction error delta → 0, gamification fades). Without this, the roadmap optimizes for engagement, not habit formation.
