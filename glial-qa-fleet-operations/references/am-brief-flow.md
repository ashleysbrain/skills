# AM Brief Flow (Conductor-tracked, login-triggered) — principal rulings 2026-08-24 PM

## Laws
1. **Never pre-written.** The brief is generated LIVE at the moment the principal
   logs on / begins working. A night-written brief is stale by morning (same
   defect class as pre/post baseline snapshots: locks a frozen world against
   a living one).
2. **Live data at trigger time**: ledger state (overnight mints/claims/dones),
   bus traffic, Glia self-review cycle log, research-watch catches, telemetry
   deltas, B2C/exit scoreboard. Include everything that happened overnight.
3. **Structure** (organized, prioritized, per-user customized):
   - 60-second recap
   - Overnight opportunities (what changed)
   - Needs-human items: BUTTONS, minimal, prioritized by opportunity_weight x relevance
   - Standing decisions (no re-litigation)
   - Patterns noticed
4. **Trigger = first principal activity on any substrate** (Telegram first message,
   Mac unlock via local-activity feeds). Event-driven, NO timers, NO crons.
5. **Conductor-tracked**: each brief = calendar event; needs-human items become
   conductor tasks (deadlines when time-bound). Every delivery logs timestamp
   + trigger signal to analytics DB.
6. **Analytics flywheel**: wake-time series -> rolling median + drift detection
   (circadian lineage) -> predicted start window -> pre-stage data gather in
   window (still never pre-write). Which sections principal acts on first = relevance
   learning for personalization.
7. **Identity**: this is a the OS surface; hermes is only the delivery
   harness. Same flow delivers on any substrate where the morning starts.

## Pitfalls
- Do not ask the principal open questions in the brief; sign-offs and choices are
  buttons, not prose questions.
- Do not include internal tooling/outage language (team-facing rule).
- Keep a TOMORROW-PICKUP pinned-items file so "don't let me forget X" requests
  surface reliably in the next live brief.
