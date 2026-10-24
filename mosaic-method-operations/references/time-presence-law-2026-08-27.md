# Time & Presence Law — principal 2026-08-27 (machine-enforced)

Three violations in three days forced structural (not discipline-based)
enforcement. Any time/duration claim in a principal-facing message must be
verified programmatically in the same turn.

## The three cases

1. **"3 AM busiest hour" (08-26)** — read UTC bus timestamps as local.
   Actual busiest overnight hour was ~midnight-1 AM principal local. Fix:
   always convert UTC→America/Chicago before reporting.
2. **"2 hours of downtime" (08-26 evening)** — 01:32 UTC read as local;
   that's 8:32 PM CDT, EIGHT minutes before the principal's next message.
   Continuous traffic was relabeled "downtime." The bus bucket query was
   even in hand showing steady traffic — the contradiction went unnoticed.
3. **"Morning report" + 10-hour sleep window (08-27)** — principal said "I just
   wanted to make sure you were not broken... if it isn't morning don't
   send morning briefs." Local time was 8:39 PM. Presence was anchored to
   ONE Telegram thread's silence; principal was active on other interfaces
   until ~4 AM per their testimony. User testimony beats inferred windows.

## The law (as minted)

- User testimony WINS over sensor inference, always.
- Presence = ALL interfaces. Thread silence ≠ sleep.
- Bus/ledger timestamps are UTC — convert programmatically before any
  time/duration claim.
- Never infer time-of-day state ("morning", "overnight") from a message
  gap: run `date` and cross-interface presence check in the same turn.
- Wake-digest triggers only on a VERIFIED sleep gap (no activity across
  ALL interfaces for a defined overnight window, then resumption) — never
  on any message after a quiet stretch.
- Testimony/sensor conflict → surface the conflict, never silently pick.

## Why discipline alone failed

Each violation came after a same-day promise to be careful. The fix is
machinery: pre-send check on any message containing a time/duration claim
(timestamps converted + verified against the bus record by code), wired
into the wake-digest build and orchestrator dispatch flow.
