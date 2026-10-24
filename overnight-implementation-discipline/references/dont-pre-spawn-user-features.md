# Don't Pre-Spawn User-Facing Features

## The Mistake (2026-06-11)
Built the Wave Engine V2 API with full panel endpoints (`POST /v1/panels`, `POST /v1/panels/{id}/deliberate`, `GET /v1/panels/{id}/summary`). Then **immediately spawned an "Executive Board" panel** via API calls without the user asking.

**User correction:** "I didn't tell you what type of board to spawn... I was waiting for you to get the wave engine complete so that I could spawn one myself and go through the coaching process."

## The Principle
**Build the engine. Verify it works. STOP. Let the user invoke features.**

This applies to ALL user-facing workflows:
- ❌ Panels / advisory boards
- ❌ Goals / coaching plans
- ❌ Situational threads
- ❌ Agent spawning
- ❌ Any feature the user initiates through the product

## Correct Flow
```
1. BUILD engine → all endpoints implemented
2. TEST engine → unit tests + integration smoke tests pass
3. DELIVER engine → "Server running at http://localhost:port, v2.0.0 tagged"
4. WAIT → User decides when to create session, do intake, spawn panel
5. SUPPORT → Help user through THEIR flow when they ask
```

## Anti-Patterns to Avoid
| Anti-Pattern | Why It's Wrong |
|--------------|----------------|
| "I'll create a demo panel so you can see it works" | User didn't ask. They want to practice THEIR flow. |
| "Let me set up a goal for you" | Goals are user-initiated in Mode 2. |
| "I'll spawn an agent to monitor this" | Agents are talent-gated, not builder-spawned. |
| "Here, I made you a thread for the legal case" | Threads are Mode 3, user-activated. |

## User Ownership
The coaching engine is **the user's tool**. They drive the flow:
- Mode 1: User asks question → engine responds
- Mode 2: User sets goal → engine builds plan
- Mode 3: User activates thread → engine manages
- Mode 4: User creates panel → engine orchestrates

**The engine serves. The user decides.**

## Verification Checkpoint
After engine delivery, ask: "What would you like to try first?" Not "I made you a panel."