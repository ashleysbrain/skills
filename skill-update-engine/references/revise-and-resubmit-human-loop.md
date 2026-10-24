# Revise-and-Resubmit + Human Loop

## Purpose
Keep near-miss candidates alive instead of discarding them, while ensuring humans stay in the approval loop for the release ladder.

## Core rules
- If a candidate fails for a *fixable* reason, mark it `revise` rather than `blocked`.
- Attach a concrete edit plan: what to change, why it failed, and what to rescore.
- Re-run the candidate through SCOUT and SENTINEL after the edit.
- If the item exceeds the retry limit or hits a hard stop, archive it as `blocked`.

## Human touchpoints
- **Daily:** human reviews the top 3 eligible candidates before the final ship choice.
- **Weekly:** human receives a report package covering approvals, rejects, revisions, near-misses, and watchlist drift.
- **Monthly:** human performs a mandatory audit/reset of safety boundaries, portfolio freshness, and release ladder coherence.

## What the weekly report should contain
- candidate counts by status
- top 3 ranked candidates
- items moved to `revise`
- items archived as hard stops
- shipped items
- watchlist trends over time

## Pitfall
Do not treat `revise` as a soft delete. It is an active state that should preserve the idea, the evidence, and the next edit action.