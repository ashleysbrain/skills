# Client-Side Urgency Computation (Fallback Pattern)

When task-level physics engines (Quartz/the specialist engine) are unavailable, the
calendar Lattice view computes urgency client-side. This is NOT the same
as the 4 physics primitives — it is a simpler heuristic that provides
actionable ranking without requiring a backend physics engine.

## When to Use This Pattern

- The Quartz/Hall task lattice endpoints (`/v1/tasks`, `/v1/lattice/state`)
  are dead or unreachable
- You need task ranking for a UI surface (Lattice view, dashboard)
- You have access to item metadata: priority, status, scheduled_start, route
- You do NOT have computed free_energy values from a physics engine

## The Formula

```javascript
// urgency = priority_weight * 0.40 + status_contribution + deadline_proximity + route_boost
// Range: [0, 1] — clamped

var PRIORITY_WEIGHTS = { critical: 1.0, high: 0.75, expedite: 0.8, standard: 0.45, low: 0.2 };

function computeUrgency(item) {
  var p = PRIORITY_WEIGHTS[item.priority] || 0.45;
  var s = 0, d = 0;

  // Status contribution
  if (item.status === 'blocked' || item.status === 'needs_input') s = 0.3;
  else if (item.status === 'awaiting_review') s = 0.25;
  else if (item.status === 'in_progress') s = 0.15;
  else if (item.status === 'completed' || item.status === 'cancelled') s = -0.5;

  // Deadline proximity
  var sched = item.scheduled_start || '';
  if (sched) {
    var hoursAway = (new Date(sched) - new Date()) / 3600000;
    if (hoursAway < 0) d = 0.35;        // overdue
    else if (hoursAway < 24) d = 0.30;   // today
    else if (hoursAway < 72) d = 0.20;   // 1-3 days
    else if (hoursAway < 168) d = 0.10;  // this week
  }

  // Human-route boost (requires human decision = more urgent)
  var r = item.route === 'human' ? 0.10 : 0;

  return Math.max(0, Math.min(1, p * 0.40 + s + d + r));
}
```

## Verdict Thresholds

```javascript
function computeVerdict(item) {
  if (item.status === 'completed' || item.status === 'cancelled') return 'DONE';
  var u = computeUrgency(item);
  if (item.status === 'blocked' || item.status === 'needs_input') return 'HUMAN';
  if (u >= 0.55) return 'DO';
  if (u >= 0.30) return 'DEFER';
  return 'DELEGATE';
}
```

## Critical Distinction: Urgency vs Free Energy

- **Free energy** (F = E - TS): requires a physics engine computing internal
  energy (sum of task energies), entropy (status distribution), and
  temperature (deadline pressure). NOT computable from item metadata alone.
- **Urgency** (this formula): a heuristic ranking score. Computable from
  priority + status + deadline + route. Does NOT model entropy or
  critical path.

**Rule:** Label this "urgency" in ALL UI text. Never call it "free energy"
or "F=" — that implies the full physics model which we do not have. The
Lattice mockup (`opendesign/mockups/task-engine-lattice/index.html`) uses
"F=" labels, but those were aspirational. The live system uses "urgency".

## Degradation-Graceful Upgrade Path

When a physics engine becomes available again:

1. Probe `_engine_alive(url)` for the task physics endpoint
2. If alive, consume real free_energy values from `/v1/lattice/state`
3. Fall back to this client-side formula when the probe fails
4. The calendar_items.free_energy DB field exists for this purpose but
   is currently never populated by any adapter

Source: organism-calendar-harness Lattice view, built 2026-08-09.
Confirmed via sibling-agent bus exchange (msg 1624-1626).
