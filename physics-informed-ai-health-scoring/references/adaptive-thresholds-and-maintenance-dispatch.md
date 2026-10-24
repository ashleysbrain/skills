# Adaptive Thresholds and Maintenance Dispatch

Session: 2026-07-06
Status: Live in `organism/adaptive_thresholds.py`

## The Problem

A static threshold of 7.5 for every dimension does not account for system state. During recovery from a disturbance, the system needs room to oscillate. During steady state, it should be held to tighter expectations. A static threshold either fires too often during normal recovery, or not often enough when the system is quietly degrading.

## Adaptive Threshold Design

`get_adaptive_threshold(dimension)` returns a per-dimension threshold bounded [4.0, 9.0].

Three adjustment signals:

| Signal | Condition | Adjustment |
|--------|-----------|------------|
| Variance | std > 1.0 (disturbed) | loosen up to -1.5 |
| Variance | std < 0.3 (stable) | tighten +0.3 |
| Trend | improving > 0.5 | tighten +0.2 |
| Trend | declining < -0.5 | loosen -0.5 |
| Recovery | intervention in last 24h | loosen -1.0 |

Base threshold is 7.5. With fewer than 3 history data points, base is returned unchanged (not enough data to adapt).

Physics basis: critical slowing down. A system near a tipping point needs a lower threshold because its recovery capacity is already strained. Forcing it to hit 7.5 during recovery causes false alarms and intervention thrashing.

## Maintenance Ticket Dispatch

`generate_maintenance_ticket(dimension, score, threshold)` creates a concrete repair ticket. Each dimension has a specific action map:

| Dimension | Physics | Symptoms | Example Steps |
|-----------|---------|----------|---------------|
| COG | Information theory | Re-entry loops, contradictions | Review logs, check context, clear stuck loops |
| PIPE | Transport phenomena | Latency, failures, stalls | Check APIs, clear stale refs, reset budgets |
| RES | Thermodynamics | Budget overrun, wrong model | Audit tier routing, enforce caps |
| KNOW | Radioactive decay | Stale sources, deprecated APIs | Refresh KB, prune old sources |
| ALIGN | Potential landscape | Low compliance, violations | Run audit, fix decorative engines |
| ADAPT | Relaxation dynamics | Slow recovery, tipping | Measure tau, run hormesis cycle |
| INTER | Synchronization | Handoff failures | Check bus, reconcile schemas |

Priority: CRITICAL (gap > 2.0), HIGH (gap > 1.0), MEDIUM (otherwise).

`post_maintenance_ticket(ticket, operator)` posts to the operator bus as a `design_request`. Both hermes and sibling-agent see pending tickets via `operator_bus.py read --to hermes --status pending`.

## Integration with Self-Healing Loop

The `detect()` function in `self_healing_loop.py` accepts `use_adaptive=True` (default). When enabled, each dimension gets its own threshold from `get_adaptive_threshold()`. The `_cron_post_alerts()` function generates and posts maintenance tickets for every dimension_drop alert.

## Linear Integration — Real Ticketing (Session 2026-07-06)

The operator bus is a message queue, not a ticket tracker. When the user asks "can we use Linear for the ticketing system", the answer is yes, and the bridge is `linear_bridge.py`.

### Bridge Architecture

`linear_bridge.py` provides four functions:
- `create_health_issue(title, description, priority, label_name)` -> Linear issue URL
- `close_health_issue(identifier)` -> marks Done (by DIV-NNN or UUID)
- `find_open_health_issues(dimension)` -> list of non-completed health tickets
- `_get_team_id()`, `_get_label_id()` -> cached lookups

Priority mapping: CRITICAL=1 (Urgent), HIGH=2, MEDIUM=3, LOW=4. Labels: all AI health dimensions map to "Bug" label (configurable per dimension in `adaptive_thresholds.py:post_maintenance_ticket()`).

### Dual-Write Pattern

`post_maintenance_ticket()` writes to BOTH Linear AND the operator bus:
- Linear: creates a real issue with formatted Markdown body (physics, symptoms, numbered steps)
- Operator bus: posts a `design_request` with a "Linear ticket created" subject and the Linear URL

If Linear is unavailable (API key missing, network down), the bus notification still fires. Graceful degradation is mandatory.

### Verification

```bash
# Test the bridge creates a real issue
python3 organism/linear_bridge.py
# Should print: SUCCESS: Created test issue at https://linear.app/...

# Find open health tickets
python3 -c "from linear_bridge import find_open_health_issues; print(find_open_health_issues('ALIGN'))"

# Close a recovered dimension's ticket
python3 -c "from linear_bridge import close_health_issue; close_health_issue('DIV-153')"
```

### Key IDs (Divinity Science workspace)

- Team: DIV (id: 177b4ef0-3432-447f-8efc-dc433f2e05b6)
- Labels: Bug, Improvement, Feature, research, infrastructure
- States: Backlog (backlog), In Review (started), Done (completed), Canceled

## The Remaining Gap

Tickets are now tracked in Linear with sprint planning, assignment, and status workflow. But no automated system executes the repair steps yet. Full autonomy (system fixes its own degradation without human intervention) is the next layer to build.

## Verification

```python
from adaptive_thresholds import get_all_thresholds, generate_maintenance_ticket
thresholds = get_all_thresholds(fleet_mode=True)
# Each threshold in [4.0, 9.0], potentially different per dimension

ticket = generate_maintenance_ticket("ALIGN", 4.0, 7.5)
# ticket has ticket_id, priority, physics, symptoms, steps
```
