# Advisory Panel Gamification Constraints

Reference for the physics-informed-gamification-design skill. Captures the specific requirements, vetoes, and methodologies from the the specialist engine Advisory Panel sessions (3 sessions, June-July 2026).

---

## Advisor Requirements

### Yu-kai Chou — Gamification Design Lead (Octalysis Framework)

**Core thesis:** TWC is not just a number — it's a game state. Every change in TWC is a game event. Every dimension is a skill tree. The gamification doesn't need to be bolted on; it emerges naturally from the scoring engine.

**Requirements:**
- Emergent quests triggered when dimension scores cross baseline thresholds
- First 5 minutes = scoring reveal with "Spotify Wrapped energy" — not a tutorial, a revelation
- Diminishing returns in the XP economy to prevent insurmountable advantages for early adopters
- Coherence multiplier is a unique White Hat mechanic (Core Drive 2: Accomplishment) — rewards quality over volume
- Wellness Radar quest type: multi-dimensional shift detection triggers curiosity-driven notification
- Compete on "smarter scoring," not "more features" or "better badges"

**Octalysis Core Drive mapping for health gamification:**
- CD1 (Epic Meaning): wellness journey as part of something bigger
- CD2 (Development & Accomplishment): progress bars, level-ups, skill trees per dimension
- CD3 (Empowerment): customizable quests, visible impact of choices
- CD4 (Ownership): personal wellness profile, earned achievements
- CD5 (Social Influence): team challenges, mentorship (opt-in only)
- CD6 (Scarcity): limited-time seasonal quests (use sparingly)
- CD7 (Unpredictability & Curiosity): surprise quests, emergent challenges — THE signature drive
- CD8 (Loss & Avoidance): streak preservation (used carefully, never as shame)

**White Hat bias:** Prioritize CD1-5 (meaningful, empowering, social). Use CD6-8 sparingly and ethically.

**Intrinsic vs extrinsic progression:**
- Early game: lean on extrinsic (XP, badges, progress) to build habits
- Mid game: transition to intrinsic (identity, mastery, autonomy)
- Late game: intrinsic dominates; gamification becomes invisible

**Signature question:** "What is the one emotion you want users to feel when they see their TWC change?"

---

### BJ Fogg — Behavioral Psychology (B=MAP Model)

**Core thesis:** v1 gamification should be so simple it barely qualifies as gamification. Show the user one dimension score. Show them what behavior moved it. Celebrate the connection. That's it.

**B=MAP Model:** Behavior = Motivation + Ability + Prompt

**Requirements:**
- v1 = scoring visibility only. No XP, no badges, no quests. Show behavior-to-score cause-and-effect.
- Signal-based quests (triggered when scores drop) must be EASIER than daily quests
- During health dips: quest difficulty drops to one-tap, <30 seconds, auto-accept
- Immediate celebration within 2 seconds of completion — visceral feedback (visual, sound, animation)
- Pick the dimension with the most reliable data signal (likely Sleep or Physical) for v1
- "Make it tiny. Make it visible. Celebrate immediately."

**Key question:** "What happens on day 45 when the novelty wears off?"

**The v1 loop:** "You slept 7.5 hours last night. Your Sleep dimension went up 3 points. That's real progress." No XP, no badges, no quests. Just truth, made visible.

---

### Nir Eyal — Engagement Strategy (Hook Model)

**Hook Model:** Trigger → Action → Variable Reward → Investment

**Requirements:**
- Redesign score-change notifications to spark CURIOSITY, not deliver data
  - ✅ "Something shifted in your wellness profile"
  - ❌ "Your score changed by 3 points"
- Introduce surprise bonuses tied to coherence streaks (variable Hunt-type rewards)
- Users should move from external triggers (notifications) to internal triggers (habit) over time
- Gamification should eventually become INVISIBLE — habits internalized, no daily engagement needed
- Hook cycle in one sentence: "Your score changes, you see what shifted and why, you log one behavior that refines your baseline."

**Key question:** "When you picture the ideal user after 6 months, are they still engaging with gamification daily, or has it become invisible?"

---

### Amy Webb — Data Science & Scoring Engine

**Requirements:**
- Stress-test XP formula at extreme values (99th percentile) and model impact on diverse populations
- Build instrumentation into every gamification feature from day one — measure leading indicators of 90-day retention
- If coherence multiplier exceeds 5x gap at any scale → implement logarithmic diminishing returns above 80th percentile
- If gap is 3-5x → monitor closely, consider linear formula instead of squared
- Data pipeline documentation tracing every dimension score to input sources, confidence levels, update frequency

**Key question:** "Has the XP formula been stress-tested at extreme values? What happens at the 99th percentile?"

---

### Anti-Gamification Advocate — Red Team Skeptic

**Core principle:** "If you have to gamify it, is the underlying experience actually valuable?"

**User Dignity Test:** Does this mechanic treat the user as a person to be empowered or a behavior to be optimized?

**VEToes (non-negotiable):**

1. **Coherence multiplier on XP** — punishes chronically ill users for circumstances beyond their control. Resolution: coherence as diagnostic only, resilience XP for showing up during hard weeks.

2. **Wellness Radar without tri-mode guardrails** — users with bipolar, autoimmune, postpartum conditions trigger constant alerts. Resolution: Active/Quiet/Off modes, auto-default to Quiet for high-variance users.

3. **Any mechanic that cannot be silenced** — "A health product that cannot be silenced is a health product that harms." Resolution: `gamification_mode: "off"` from day one.

4. **Loss aversion mechanics** — no streak shame, no "you lost your streak!" notifications.

5. **Social comparison without explicit opt-in** — comparing a chronically ill user to a healthy user on a leaderboard is cruelty disguised as motivation.

**Constructive alternatives:**
- "Life context" layer: adjusts expectations based on known disruptions
- "Resilience XP": award for showing up during hard weeks
- "Quiet mode": shifts logged but not pushed, passive weekly summary
- Vulnerable user persona gallery: test every mechanic against 5 specific personas before shipping

**Key question:** "If a user tells you the gamification makes them feel worse about their health, do you change the gamification or tell them it's working as intended?"

---

## XP Formula Stress Test Methodology

### The Formula
```
TWC = η × μ × C × (1 + 0.5 × S)
C   = 1 - σ/μ  (coherence factor: penalizes high variance across dimensions)
S   = synergy tensor (rewards positive coupling)
```

### Test Setup
- Simulate 1K, 10K, 50K users across 5 population archetypes
- Archetypes: balanced_high, balanced_mid, imbalanced, chronic, struggling
- Compute XP under 6 formula variants
- Measure p99/p10 gap (worst-case user vs best-case user)
- Check archetype equity (balanced_high / struggling ratio)

### Formula Variants Tested
| Formula | Gap at 50K (p99/p10) |
|---|---|
| Flat (no coherence on XP) | 2.64x |
| Capped (coherence max 0.6) | 2.65x |
| Log diminishing returns | 2.81x |
| Linear (1+coherence) | 3.00x |
| Squared (1+coherence)^2 | 3.48x |

### Key Finding
The originally feared 4.7x gap does NOT replicate under realistic population distribution. Actual worst case: 3.48x (squared formula). The gap is STABLE across scales (does not grow at scale). The original 4.7x was likely an extreme edge case (max coherence user vs min coherence user), not the p99/p10 range.

### Archetype Equity Check
- balanced_high: mean 221 XP
- balanced_mid: mean 114 XP
- imbalanced: mean 82 XP
- struggling: mean 73 XP
- Ratio (balanced_high / struggling): 3.0x — significant but not the 4x+ requiring redesign

### Recommendation
- v1: XP = flat TWC score. Coherence shown in UI as diagnostic, NOT applied to XP. Eliminates math risk entirely.
- v2+: If coherence goes on XP, use linear (not squared) + log diminishing returns + resilience XP modifier for chronic users. Validate with real population data.

---

## Vulnerable User Persona Gallery

Before any mechanic ships, it must pass the dignity check against these personas:

| Persona | Condition | What breaks for them |
|---|---|---|
| Single Mom | Chronic pain, caregiving, inconsistent schedule | Coherence multiplier punishes her for her life |
| Bipolar User | Natural mood dimension swings | Wellness Radar pings constantly about their illness |
| Postpartum Mother | Sleep, emotional, physical all destabilized | Every dimension in critical slowing → system feels like nagging |
| Autoimmune Patient | Flare-ups crater physical + cognitive | Strain alerts during flares feel like surveillance |
| Financial Crisis | Financial dimension chronically low, cascading to psychological | Low scores across coupled dimensions feel like the algorithm judging their poverty |

**The test:** *Would this user feel respected or controlled?* If "controlled," redesign or cut.

---

## Competitive Landscape (July 2026)

- Top 10 healthcare gamification apps ALL use volume-based mechanics (steps, workouts, days streaked). Nobody rewards quality/consistency via coherence.
- Our differentiation: multi-dimensional scoring QUALITY, not another badge system.
- Noom hired Peloton's design chief — combining behavior change science with premium engagement design.
- Oura Ring 5 shipped Health Radar (proactive alerts), GLP-1 Insights, lab integration.
- Healthcare gamification market: $6.4B in 2026, growing at 12.98% CAGR.
- Wearables shifting from passive tracking to AI-driven predictive coaching.

**One-sentence pitch:** *"We're not just adding another health game to the pile. We're introducing a fundamentally different game loop: one where the player levels up by being coherent, not by being prolific."*

---

## Config Schema Reference

```yaml
gamification:
  mode: "off"              # "off" | "standard" | "full"
  scoring:
    enabled: false
    xp_formula: "flat"      # "flat" (v1) | "linear" (v2) | "log_diminishing" (v2+)
    show_coherence: true    # always diagnostic, never on XP in v1
    streak_tracking: true
  achievements:
    enabled: false
    tied_to_8d: true
  quests:
    enabled: false
    emergent_mode: "quiet"  # "active" | "quiet" | "off"
    auto_default: "quiet"
    difficulty_model: "bmap"
  narrative:
    enabled: false
  safety:
    quiet_mode_auto_trigger: true
    dignity_check: true
    resilience_xp: true
    off_ramp_always_available: true
```
