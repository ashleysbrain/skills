---
name: organism-native-review-cadence
description: Use when asked for regular organism review. Never cron.
---

# Organism-native review cadence

Class of task: the principal asks for a REGULAR or PERIODIC review of anything —
science corpus, backlog, seats, metrics, self-improvement. The principal's law is
explicit: "I don't set up crons because that's not the mosaic way." Reviews
fire when the SYSTEM changes, not when a clock ticks.

## Law
Cron-shaped cadences are harness drift. A review cadence is a pure function
guarded inside an existing daemon cycle (conduction daemon is the carrier),
invoked by events, silent when nothing is due.

## Procedure
1. **Census before build.** Find the existing organs that already touch the
   material (gap hunters, triage gates, metabolism reports) and EXTEND one —
   new spine for an old function is a blank-slate build, which the principal rejects.
2. **Model the triggers as cheap guards** inside the daemon's cycle function
   (two COUNT queries max):
   - CAPABILITY EVENT — something completed (bus seats done, new law minted):
     the system changed, so prior material can newly make sense.
   - CORPUS EVENT — the material pool grew past a threshold since last pass.
3. **Eligibility via a global freshness window** (row not reviewed within N
days), NEVER per-trigger exclusion — per-trigger "not in this trigger" filters
make every pass re-read the same batch while the backlog never drains.
4. **Dedup-key gate on every bus INSERT** the review organ makes — coalesced
pokes/daemons fire the same pass repeatedly and duplicate findings leak into
principal surfaces.
5. **Batch, adiabatic** — cap entries per pass; retro sweeps burn down backlog
oldest-eligible-first, never the whole pool at once.
6. **Free-energy gate inside the organ** — score candidates before fetching;
record skips, don't retry them.
7. **Failure-only logging** — healthy is zero output; review organ must never
be able to break its carrier daemon (wrap in try/except, record to
last_error).

## Verification (acceptance test)
- Run the organ twice with the same trigger — the second run must be QUIET
  (0 new reviews of already-reviewed rows). Silence is the pass condition.
- Check the bus for duplicate rows with the same dedup_key — must be exactly 1.
- Kickstart the carrier daemon to load patched code: grep `launchctl list`
  for the exact label FIRST (never kickstart from memory — labels have
  suffixes, e.g. `-daemon`), then `launchctl kickstart -k gui/$(id -u)/<label>`
  and confirm via the /health endpoint that `started_at` reset.

## Known pitfalls
- "--selftest" vs "selftest" argument conventions differ per daemon — read
  the argparse block before running.
- Hand-seeded keyword lists rot: seed lists must be born self-extending
  (grown at runtime from live bus content), or they become stale
  classifiers within weeks.
- The health endpoint only shows the new behavior fields AFTER a poke drives
  one cycle — force one cycle before declaring the hook live.
- **An audit organ that scans a git working tree becomes a perpetual-finding
  machine** when runtime churn (glia state ticks, telemetry logs, the
  audit's own append-only log) dirties the tree between commits — split
  CANONICAL surfaces (law files, gates, migrations) from RUNTIME churn
  (gitignore the churn; filter findings to canonical paths) or the audit can
  never reach zero and its nonzero state means nothing. Gitignore the
  audit's own log too: an auditor that dirties the repo it audits feeds
  itself findings forever.
- **Findings are HANDLED inside the same sweep, not queued** — commit the
  churn, disposition the bus row, verify the restart before reporting. An
  audit that only lists is a diary.
- **Measured constants only.** Time the organ (mean of ≥5 runs) for its cost
  term; count real bus events for the temperature term and CLAMP it —
  auto-repair/watchdog floods (hundreds of events/hour) are noise, not
  organism stir, and an unclamped T makes the audit's own free energy absurd
  (an impossible value like F = −689 on a one-finding sweep is the tell that
  a constant is fake; chase it, never round it away).
- **'Fires at every stir' written in a docstring with no hook wired is a lie
  by docstring.** Wire the organ into a real stir surface (boot checklist,
  gateway wake) and prove it by running that surface end-to-end and reading
  back the persisted verdict.
- **Age-filter queue findings** (pending bus rows newer than ~30 min); stale
  rows are the reaper's lane, and one zombie row pins the health radius at
  nonzero forever.
- **Same-minute dedupe on the verdict log** — identical verdicts within a
  minute write once.
- **Never report an organ 'done' off its own self-report.** Rerun the
  artifact cold (fresh process, no cached state) and read back persisted
  state; expect the first cold runs to expose defects in the organ itself —
  those runs ARE the test. A principal distrust cascade ('I don't trust this', 'I
  bet it is still not done') is the cheapest adversarial audit available;
  meet it with enumerated defects and raw state, never reassurance.
