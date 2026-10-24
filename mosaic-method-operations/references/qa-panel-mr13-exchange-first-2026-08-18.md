# MR13: exchange-first QA on process flows (2026-08-18)

User asked for "another thorough qa pass on process flows". Digest found
sibling lane QA-PASS-30 had ALREADY audited that surface (5 macro + 6
micro defects) with zero remediation commits since. A duplicate audit
would re-measure known state: F > 0, SKIP. Correct move: remediate all
defects, then dispatch a fresh-brain verification panel on the
REMEDIATED state.

## Remediation ledger (all live-verified before the panel ran)
- M1 one flow vocabulary: 15 registry codes; doc headings carry FLW-*;
  `store_gate.py --flow-sync` (in ci_battery) fails both directions.
- M2 stage state machine: set_stage() API; legacy off-vocab warns loud.
- M3 daemon last_error cleared on success; hard-restart off stale PID
  (bootout had silently failed — ps is the truth, not launchctl list).
- M3b plist repointed to canonical path (bridge symlink = latent risk).
- M4 sev-1 principal alert wired in submit(); live-proven bus 2324. NOTE: this
  wiring introduced the Case-2 hermeticity defect below — new write paths
  need their selftest story in the SAME commit.
- M5 severity = priority; incident-class alerting = Flow 3b. Split documented.
- m4 aging: ledger_whois --aging N (oldest open; surfaced stuck decision).
- m6 hourly telemetry rollup launchd (Minute=5).

## Panel results
- the specialist engine (ops readiness): A, 5/5 probes. Referrals to flow owner:
  bus dispatches 2313/2315 parked (missing mosaic-step keyword); daemon
  --selftest not fully isolated.
- the specialist engine (falsification): B, 6 findings — ALL fixed in-window:
  F1 selftest principal-bus pollution (sev-2), F2 rubric close-hook stage
  bypass (sev-2), F3 set_stage fail-open on unregistered flows, F4
  case-sensitive self-healing guard, F5 flow-sync accepted prose codes +
  dup collapse, F6 dead default-stage code (computed, never inserted;
  132 tasks stage-less).
- Re-falsified: F1 subprocess selftest -> prod alerts 1->1 clean; F2
  complete() keeps stage in-vocab, verdict rides outcome.
- Backfills: 51 off-vocab stages -> 0; 132 stage-less -> 0.

## Laws/structures that emerged
- CONTRACT.md L0 standing law ("the OS OS always", principal 16x): methodology
  is permanent OS, no mode-off, switch-brain changes specialist not OS.
- Heading-level flow-sync: codes must live in ## headings (prose
  mentions excluded); subflow headings say "stage of FLW-X" (skipped by
  the gate's regex); one heading owns one code.
- Aging surfaces stuck decisions automatically: oldest open task was a
  pending principal ruling nobody had looked at in a day.

## Formal-delivery lesson
The async batch's TRUNCATED summary hid finding F6; only the full
delivered text surfaced it. When a panel reports N findings and the
consolidated message shows fewer, read the saved full summary file
before declaring the pass closed.
