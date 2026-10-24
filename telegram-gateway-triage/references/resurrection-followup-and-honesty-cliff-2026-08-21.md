# Resurrection Follow-up + Honesty Cliff (2026-08-21 late session)

PENDS MERGE into `references/false-positive-restarter-diagnosis.md` (the
background patch guard's dedup bug refuses the edit — same known issue
documented in daemon-cadence-architecture). Merge BOTH sections below.

## 1. Resurrection mechanics (extends "Fix pattern")

DEMOLITION, NOT EVICTION: `launchctl bootout` without `rm` of the plist
resurrects. Any GUI session event (login/unlock/wake) triggers a launchd
bootstrap rescan of ~/Library/LaunchAgents and reloads every plist still
on disk. Verified: watchdog booted out 23:10 CDT 08-20, resurrected 00:20
CDT 08-21 by `launchd: entering bootstrap mode` (findable via unified log
`log show --predicate 'process == "launchd"' --start ... --end ...`).
DEMOLITION = bootout + `rm ~/Library/LaunchAgents/<label>.plist`, and the
verification is `ls ~/Library/LaunchAgents/` — NOT `launchctl list` at a
single moment (a session event hasn't happened yet to test the removal).

## 2. The honesty cliff (the principal-charge lesson)

Timeline that triggered "you lie again": fix landed 22:49 CDT and genuinely
held (0 false kickstarts after, vs 10 in the two prior days, uptime 6h+,
overnight cron reports delivered). But the CLEANUP claim ("both watchdogs
removed") was false for one duplicate until ~11:00 UTC next day because
the plist resurrected it. General rules:

1. Never claim removal on bootout alone — removal is proven by plist
   deletion + surviving a session-event cycle.
2. When the principal reports a recurring failure, verify the FULL claim surface
   (processes AND plists AND logs AND deliveries) before asserting a fix
   held; partial verification presented as full verification reads as a
   lie even when intent is honest.
3. The overnight proof surface is gateway uptime (exit-diag), iteration
   counts (telemetry), delivered-message ids — never the operator's word.
