# Lattice-Based Task Engine Design Pattern

**Origin:** the specialist engine overnight build (2026-06-10)
**Class:** Physics-informed task management engine with autonomous operation

---

## Core Concept

A crystal lattice = repeating 3D structure of atoms in stable, organized arrangement. Every atom has its position. The structure holds because each position is optimized for stability.

Applied to task management:
- Each task = an atom with a lattice position
- Positions have: stability_score, energy_match, deadline_pressure, priority_weight, coupling, dimension_tags
- Lattice continuously rebalances (every 60s), self-heals on completions, reacts to new inputs, relaxes on energy drops, reinforces flow states

---

## Autonomous Operation Modes

### Mode A: Full Integration (Coaching Engine Active)
- User talks to coach → Coach identifies action → Quartz captures automatically
- User has a goal → Coach breaks into steps → Quartz slots into lattice
- User completes something → Coach notes it → Quartz marks done, lattice reshapes
- User's energy drops → 8D scoring detects → Quartz reorganizes lattice
- **User never opens task app. Coaching conversation IS the task interface.**

### Mode B: Standalone (No Coaching Engine)
- Auto-capture from voice/text/calendar
- Auto-clarification (NLP, skip human review if >85% confidence)
- Auto-organize into lattice positions
- Auto-energy matching from wearable/self-report
- Auto-reflection and lattice reformation
- **User's only job: do the one thing. Say "done." Next appears.**

---

## Five Continuous Lattice Operations

1. **Rebalance** — recalculate all position stability scores every 60s
2. **Reform** — close gaps when tasks complete, shift neighbors
3. **React** — find optimal position for new input or create new position
4. **Relax** — when energy drops, shift high-energy out, bring low-energy forward
5. **Reinforce** — when in flow, protect current position, suppress interruptions

---

## Coaching Engine Interface (Bidirectional)

**Inbound (from coaching):**
```json
{
  "source": "ds-wave",
  "type": "action_item | goal_breakdown | schedule_change | energy_alert",
  "payload": {
    "action": "Complete 2-week sleep protocol",
    "mode": "goal-oriented",
    "steps": [
      {"action": "Set alarm 30 min earlier", "day": 1, "energy": "low", "time_min": 2}
    ],
    "coaching_context": "Sleep identified as primary drag on Physical",
    "8d_context": {"physical": 4.2, "primary_drag": true}
  }
}
```

**Outbound (to coaching):**
```json
{
  "source": "ds-quartz",
  "type": "completion | stall | capacity | pattern",
  "payload": {
    "action_id": "uuid",
    "status": "completed",
    "stall_count": 0,
    "capacity_signal": {"current_load": 3, "max_recommended": 5}
  }
}
```

---

## Personality Engine

5 built-in personalities, runtime switching:
- 🎩 **Alfred** — Warm, proper, British butler
- 🎯 **Drill Sergeant** — Aggressive, loving, no-bullshit
- 💪 **Big Sister** — Accountable, protective, real talk
- 📱 **Nagging Best Friend** — Casual, direct, funny
- 🌸 **Gentle Coach** — Soft, patient, low-pressure

All output adapted: task language, reminder style, celebration, stuckness intervention, reflection tone.

---

## Key Implementation Requirements

- Python/FastAPI backend, PostgreSQL + JSONB, Redis queue
- Custom lattice scheduler (physics-informed optimization)
- WebSocket for real-time lattice updates
- NEVER Anthropic models — NVIDIA Nemotron only
- Graceful degradation: coaching down → standalone; 8D down → self-reported energy
- Per-user lattice isolation (each user has their own crystal)

---

## Verification Gates (Overnight Build)

- [ ] Lattice engine rebalances correctly under load
- [ ] Capture → position flow works (auto-clarify >85% confidence)
- [ ] Coaching interface accepts/receives messages bidirectionally
- [ ] Personality engine switches at runtime
- [ ] Reflection engine produces morning/midday/evening/weekly reviews
- [ ] Engagement engine presents exactly one task
- [ ] Server starts, WebSocket connects, all tests pass (pytest 0 failures)
- [ ] Integration test: coaching→quartz→lattice→engage full flow