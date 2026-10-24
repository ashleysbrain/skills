# Integration Patterns Reference

## Integration Architecture Overview
```
                    ┌─────────────────────────┐
                    │    USER (Voice/Text)     │
                    └────────────┬────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │   Divinity Health UI     │
                    │   (Frontend Platform)    │
                    └────┬──────────────┬──────┘
                         │              │
              ┌──────────┴──┐    ┌──────┴──────────┐
              │  Coaching   │    │   Task Engine    │
              │  Engine     │◄──►│   (DS ALFRED)    │
              │  (the specialist engine)  │    │                  │
              └──────┬──────┘    └──────┬───────────┘
                     │                  │
              ┌──────┴──────────────────┴───────────┐
              │          8D Scoring Engine            │
              │          (PIML Pipeline)              │
              └──────────────────┬───────────────────┘
                                 │
              ┌──────────────────┴───────────────────┐
              │          Data Sources                  │
              │  EHR │ Wearables │ Labs │ User Input   │
              └──────────────────┬───────────────────┘
                                 │
              ┌──────────────────┴───────────────────┐
              │          Gamification Engine           │
              └───────────────────────────────────────┘
```

## 1. DS ALFRED Task Engine Integration
**Relationship**: Coaching decides WHAT to do. Task engine ensures FOLLOW-THROUGH.

**Outbound: Coaching → Tasks**
```json
{
  "source": "coaching-engine",
  "type": "action_item",
  "payload": {
    "user_id": "uuid",
    "session_id": "uuid",
    "coaching_mode": "goal-oriented",
    "action": {
      "title": "Complete 2-week sleep protocol",
      "description": "Follow the sleep hygiene plan discussed in today's session",
      "due_date": "2026-06-24",
      "priority": "high",
      "dimension_tags": ["physical", "psychological"],
      "coaching_context": "Sleep identified as primary drag on all dimensions"
    }
  }
}
```

**Inbound: Tasks → Coaching**
```json
{
  "source": "task-engine",
  "type": "completion_signal",
  "payload": {
    "user_id": "uuid",
    "action_id": "uuid",
    "status": "completed|overdue|skipped",
    "completion_date": "2026-06-20",
    "capacity_signal": {
      "overload": false,
      "current_load": 3,
      "max_recommended": 5
    }
  }
}
```

**Sync Rules**:
- Coaching engine NEVER creates tasks directly — it sends recommendations
- Task engine decides HOW to present and track the task
- Task engine's personality system adapts task language independently
- If task engine flags capacity overload, coaching engine reduces pace
- Coaching milestones sync bidirectionally with task deadlines

## 2. 8D Scoring Engine Integration
**Relationship**: Consumer relationship — coaching engine reads scores. It does NOT compute them.

**Inbound: Scores → Coaching**
```json
{
  "source": "scoring-engine",
  "type": "dimension_update",
  "payload": {
    "user_id": "uuid",
    "timestamp": "2026-06-10T14:30:00Z",
    "dimensions": {
      "psychological": {"score": 62, "trend": "declining", "confidence": 0.85},
      "physical": {"score": 45, "trend": "stable", "confidence": 0.90},
      "intellectual": {"score": 71, "trend": "improving", "confidence": 0.78},
      "social": {"score": 55, "trend": "stable", "confidence": 0.82},
      "spiritual": {"score": 48, "trend": "improving", "confidence": 0.70},
      "vocational": {"score": 68, "trend": "stable", "confidence": 0.88},
      "financial": {"score": 42, "trend": "declining", "confidence": 0.75},
      "environmental": {"score": 58, "trend": "stable", "confidence": 0.80}
    },
    "twc": 54.9,
    "coupling_highlights": [
      {"pair": ["physical", "financial"], "strength": 0.72, "direction": "mutual_decline"},
      {"pair": ["psychological", "physical"], "strength": 0.68, "direction": "physical_dragging"}
    ],
    "cascade_warning": {
      "active": true,
      "source": "financial",
      "at_risk": ["psychological", "vocational"],
      "predicted_window": "5-7 days"
    }
  }
}
```

**Outbound: Coaching → Scoring**
```json
{
  "source": "coaching-engine",
  "type": "behavioral_observation",
  "payload": {
    "user_id": "uuid",
    "session_id": "uuid",
    "observations": {
      "engagement_level": "high",
      "topic_area": "financial_planning",
      "emotional_valence": "motivated",
      "action_commitment": "strong",
      "dimension_signals": {
        "financial": "user_proactive",
        "psychological": "showing_resilience"
      }
    }
  }
}
```

## 3. Gamification Engine Integration
**Relationship**: One-way — coaching produces outcomes. Gamification converts them to engagement.

**Coaching Events → Gamification**
- Goal milestone completed → Achievement unlocked
- 7-day coaching streak → Streak badge
- First session completed → Onboarding achievement
- Dimension improvement detected → Progress celebration
- Action item completed (via task engine) → XP/grind reward
- Advisory panel review completed → Review streak

**Rules**:
- Coaching engine does NOT gamify directly
- Coaching engine emits events; gamification engine consumes them
- Gamification never interferes with coaching quality
- No vanity metrics — only outcome-based achievements

## 4. Health Data Platform Integration
**Relationship**: Indirect — coaching engine does NOT connect directly to health data platform.

**Inbound: Health Data → Scoring → Coaching**
1. Health Data Platform → 8D Scoring Engine (raw data)
2. 8D Scoring Engine → Coaching Engine (processed scores)

**Outbound: Coaching → Health Data Platform**
The coaching engine can request specific data through the scoring engine:
- "What's this user's sleep pattern this week?"
- "Show stress biomarker trends"
- "What's the latest heart rate variability data?"
These requests go through the scoring engine, which serves as the data access layer.

## 5. External System Integration

### LLM Backends
- Multiple model backends supported
- No Anthropic models (company policy)
- Model selection based on coaching mode and complexity
- Fallback chain for reliability

### Notification System
- Push notifications for scheduled check-ins
- In-app notifications for coaching reminders
- Email digest (opt-in) for weekly progress summaries
- NO notifications for marketing or engagement baiting

### Calendar Integration
- Coaching sessions can be scheduled via calendar
- Advisory panel reviews appear as calendar events
- Task deadlines sync with external calendars

### Voice Integration
- Voice input for coaching sessions
- Voice output for hands-free coaching
- Speech-to-text and text-to-speech pipelines
- Voice tone analysis for emotional state detection

## 6. Data Privacy & Security Integration

### Data Flow Rules
1. Health data NEVER leaves the scoring pipeline unencrypted
2. Coaching sessions are encrypted at rest
3. User data is NEVER used for model training
4. User data is NEVER sold
5. Each user's data is isolated (no cross-user contamination)
6. Deletion requests are honored completely and promptly

### Compliance
- HIPAA-compliant architecture
- SOC 2 Type II (target)
- GDPR-compliant for international users
- State-specific health data regulations

## 7. API Contract Summary

### Coaching Engine Endpoints (exposed to platform)
```
POST   /v1/session/start          # Start a coaching session
POST   /v1/session/message        # Send message in active session
GET    /v1/session/{id}           # Get session state
POST   /v1/session/{id}/end       # End a session
GET    /v1/goals                  # List user's goals
POST   /v1/goals                  # Create a new goal
GET    /v1/goals/{id}/progress    # Get goal progress
GET    /v1/threads                # List situational threads
POST   /v1/threads                # Create a new thread
GET    /v1/panels                 # List advisory panels
POST   /v1/panels                 # Create a new panel
GET    /v1/personality            # Get current personality settings
PUT    /v1/personality            # Update personality settings
```

### Inbound Webhooks (consumed by coaching engine)
```
POST   /webhook/score-update      # From scoring engine
POST   /webhook/task-completion   # From task engine
POST   /webhook/health-data       # From health data platform (via scoring)
POST   /webhook/gamification-event # From gamification engine
```

## 8. Integration Versioning
All integration contracts are versioned. Breaking changes require:
1. New API version endpoint (e.g., `/v2/`)
2. 30-day deprecation notice
3. Backward compatibility maintained during transition
4. Migration guide published