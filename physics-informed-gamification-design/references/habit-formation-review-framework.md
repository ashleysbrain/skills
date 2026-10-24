# Habit Formation Review Framework (Wendy Wood Lens)

Reference for the physics-informed-gamification-design skill. Captures the habit formation / dorsal striatum transfer review methodology and per-mechanic verdicts from the the specialist engine Advisory Panel session (July 2026).

---

## Core Principle

Every gamification mechanic must answer one question: **does it accelerate or block the transfer from ventral striatum (goal-directed, reward-driven) to dorsal striatum (automatic, context-cued)?**

The best mechanics seed the context-response loop and then get out of the way. The system's highest success state is a user who no longer needs it.

### The Three Review Dimensions

For each mechanic, assess:

1. **HABIT TRANSFER:** Does the mechanic keep behavior in the goal-directed system (bad) or does it help the behavior transfer to the automatic/habit system (good)? Reward salience, novelty, self-monitoring, and social performance all block transfer. Easy repetition in stable contexts accelerates it.

2. **CONTEXT STABILITY:** Does the mechanic reinforce stable context cues (good) or introduce novelty/disruption (bad)? Skill tree branching, narrative chapter boundaries, world-state changes, and frequent toggling all destabilize context cues.

3. **SUNSET CONDITION:** Every mechanic must have a defined fade-out condition tied to habit automaticity. When should the mechanic disappear? What signal triggers the fade? (Lally et al. 2010: median 66 days to automaticity plateau.)

### Key Citations

- Wood & Neal (2007), *Psychological Bulletin* 134:843 — habits form through repetition in stable contexts; extrinsic rewards undermine transfer when they remain salient.
- Lally et al. (2010) — median 66 days to automaticity; missed repetitions slow but don't stop formation; shame-based avoidance kills it entirely.
- Scheffer et al. (2009) — critical slowing down as early warning of tipping points.

---

## Per-Mechanic Habit Verdicts

### Phase 3: Emergent Quests

| Mechanic | Verdict | Key Issue |
|---|---|---|
| Momentum Quest | ✅ APPROVE | Fire retrospectively after streak confirmed; never as "keep going" prompt mid-streak |
| Wellness Radar Quest | ⚠️ MODIFY | Detection-only (observe + name emergent co-occurrence), never task assignment. Multi-dimensional coordination is prefrontal/declarative, not dorsal striatum |
| Recovery Quest | ✅ APPROVE | Shift to context-anchoring after 2–3 reps (habit stacking onto existing routine), then stop prompting |
| Coupling Quest | ✅ APPROVE | Present as recognition ("You've been doing X then Y"), never as instruction ("Try doing X then Y") |
| Tri-Mode Guardrails | ✅ APPROVE | "Off" mode must truly silence ALL tracking — no silent XP accumulation that surfaces as surprise reward later |

### Phase 4: Narrative Arcs

| Mechanic | Verdict | Key Issue |
|---|---|---|
| Monthly Chapters | ⚠️ MODIFY | Strictly retrospective — describe past behavior, never prescribe future action. Monthly resets create novelty boundaries that destabilize context cues |
| Reflective Prompts | ✅ APPROVE | Cap at monthly, decreasing over time. Sparse reflection doesn't block transfer; frequent self-monitoring does |

### Phase 5: Full RPG

| Mechanic | Verdict | Key Issue |
|---|---|---|
| Skill Trees + World State | 🚫 VETO | Textbook design for PREVENTING habituation — makes every action remarkable, opposite of automaticity. Restrict to opt-in "entertainment mode" |
| Companions | ⚠️ MODIFY | Pull-only (user-initiated); never push prompts. Social performance framing keeps behavior in goal-directed system |

### Physics-to-Game Mappings

| Mapping | Verdict | Key Issue |
|---|---|---|
| Free Energy XP | 🚫 VETO | Free energy quantifies surprise — opposite of stable context-response. Rewarding its resolution incentivizes deliberation. Internal diagnostic only |
| Strain per Dimension | ⚠️ MODIFY | Internal-only above automaticity threshold. Never display as "threat level" without actionable trivially-easy next step |
| Critical Slowing Quests | ✅ APPROVE | B=MAP difficulty drop is correct. After 2–3 emergency reps, habit-stack onto daily anchor, then stop prompting |
| Coupling → Synergy XP | ⚠️ MODIFY | Detection-only. Synergy XP bonuses vetoed or capped with decay as either coupled dimension automatizes |
| TWC Formula (as level) | ⚠️ MODIFY | Internal-only first 66 days per dimension. Coherence factor C penalizes variance, which is NORMAL during habit acquisition. Never gate XP on coherence |

---

## Ship-Readiness Assessment Format

The closing assessment for any gamification review should state ship-readiness per phase:

- **CONDITIONAL APPROVE** — safe to ship with listed modifications
- **VETO** — not safe to ship as designed; specific redesign required
- For each: list the exact required changes, not vague suggestions

---

## The Missing Feature: Automatic Graduation

The roadmap's "invisibility" endgame is correct in spirit, but the proposed RPG mechanics achieve invisibility by removing the user's *awareness* while keeping them *engaged*. True invisibility means the user has graduated from the app entirely.

**The Schultz RPE sunset** is the key operationalization: when prediction error delta approaches 0, the behavior has transferred. Gamification should fade *at that point*, not become ambient.

The roadmap must build in **automatic graduation** — a mechanism that detects when a behavior has reached automaticity and systematically sunsets the gamification layer for that behavior. Every mechanic should have a sunset, and the sunset should be triggered by automaticity signals, not by user choice alone.

---

## Cross-Cutting Verdicts

### Gamification Mode Toggle (Off / Standard / Full)
✅ APPROVE — the single most important habit-formation feature. "Off" must be truly off (no silent XP, no re-emergence). Add "recommended mode" indicator that shifts toward Off/Standard as automaticity rises. Rate-limit toggling to prevent novelty-seeking churn.

### Dignity Check
✅ APPROVE — not just ethics; it is hard behavioral science. The most common reason habit formation fails is negative affect (shame, frustration) causing context avoidance. The dignity check is functionally a retention safeguard for the repetition loop. Explicitly include anti-loss-aversion and anti-social-comparison criteria.
