# Release Priority Scoring & Running Watchlist

## Purpose

This reference defines the calculation used to decide *which skills should be updated next* and how to maintain a persistent running list of future candidates.

The output of the calculation is a ranked queue that feeds the daily ship window:
- **Top 3 eligible items** are considered for build/patch work
- Anything unsafe is quarantined by **SENTINEL** before ranking
- Everything else remains on the **running watchlist** for later cycles

---

## 1. Inputs

Each candidate skill receives normalized scores in the range **0.0–1.0**:

- `market_momentum` — how strongly the market is moving in this direction
- `user_value` — expected benefit to actual users
- `anchor_gap` — how far the candidate closes the gap from the current stable core anchor
- `freshness_decay` — urgency created by staleness, errors, or drift
- `implementation_fit` — how easy it is to ship safely now
- `moat_gain` — how much this improves the open-core boundary or premium path

Safety inputs:
- `safety_risk`
- `privacy_risk`
- `boundary_risk`
- `uncertainty_risk`

---

## 2. Sentinel Gate Score

Before anything can enter the release ranking, SENTINEL computes a risk gate.

### Hard stop conditions
If any of the following are true, the candidate is **blocked**:
- `safety_risk >= 0.80`
- `privacy_risk >= 0.80`
- `boundary_risk >= 0.80`
- explicit policy violation
- the update would expose private calibration / moat logic

### Risk score
If the candidate is not hard-blocked, compute:

```text
risk_score =
  0.35 * safety_risk +
  0.30 * privacy_risk +
  0.20 * boundary_risk +
  0.15 * uncertainty_risk
```

### Interpretation
- `0.00–0.39` → ship-eligible
- `0.40–0.59` → review-only
- `0.60+` → SENTINEL quarantine

### Salvage rule
A blocked item is not automatically dead forever. If the failure is fixable, it stays on the watchlist with status `revise` and a concrete edit plan. Only hard-stop items are removed from active consideration.

---

## 3. Release Priority Score

For items that pass SENTINEL, calculate the benefit score:

```text
benefit_score =
  0.25 * market_momentum +
  0.20 * user_value +
  0.15 * anchor_gap +
  0.15 * freshness_decay +
  0.15 * implementation_fit +
  0.10 * moat_gain
```

Then compute the final priority:

```text
priority_score = benefit_score * (1 - risk_score)
```

Multiply by 100 for a human-friendly 0–100 scale.

### Ranking rule
Sort descending by `priority_score`, but only among candidates that are:
- not blocked
- not duplicate entries
- not already shipped in the current cycle

---

## 4. Running Watchlist

Maintain one persistent watchlist file:

```text
~/.sibling-agent/workspace/intel/skill-engine/watchlist.json
```

### Watchlist states
- `watching` — candidate is known, not yet strong enough
- `shortlisted` — candidate is rising and likely near-term
- `draft` — candidate has a draft patch ready
- `revise` — candidate failed but has a fixable issue and should be edited, then re-scored
- `blocked` — SENTINEL hard stop or missing prerequisite that cannot be safely cleared yet
- `shipped` — shipped and no longer active

### Recommended record shape

```json
{
  "skill_id": "8d-pattern-awareness",
  "family": "8D",
  "release_class": "support",
  "status": "shortlisted",
  "last_seen_at": "2026-05-31T09:00:00Z",
  "market_momentum": 0.82,
  "user_value": 0.91,
  "anchor_gap": 0.74,
  "freshness_decay": 0.66,
  "implementation_fit": 0.88,
  "moat_gain": 0.55,
  "safety_risk": 0.12,
  "privacy_risk": 0.05,
  "boundary_risk": 0.08,
  "uncertainty_risk": 0.20,
  "benefit_score": 0.83,
  "risk_score": 0.11,
  "priority_score": 0.74,
  "evidence": ["market scan", "usage drift", "freshness audit"],
  "notes": "Hot candidate if current trend holds for 2 more cycles"
}
```

---

### Daily Update Rule

At every daily cycle:

1. Add new signals to the watchlist
2. Refresh scores for existing watchlist items
3. Mark anything stale or duplicated
4. Identify near-miss items that should move into `revise`
5. Re-rank by `priority_score`
6. Select the **top 3 eligible items** for the ship window
7. Leave the rest in the watchlist with updated `last_seen_at`

This creates a stable, running memory of future updates instead of a one-off queue.

---

## 6. Practical Notes

- Use **current-anchor coherence** when calculating `anchor_gap`
- The watchlist should accumulate long-horizon opportunities, but shipping should remain daily
- If the same skill stays top-ranked for several days, promote it from `watching` → `shortlisted` → `draft`
- Never let the watchlist become a duplicate graveyard; merge near-identical items instead of stacking them
- If SENTINEL blocks an item, keep it on the list only if the blocking condition can realistically clear later; otherwise archive it as a hard stop
