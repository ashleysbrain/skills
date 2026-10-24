# Daemon-lane hardening lessons (Lamport panel, 2026-08-24)

Second adversarial panel (the specialist engine / the specialist engine / the specialist engine) over the
five-seat fleet build. Three defects fixed in-session; capture so they
never recur.

## LP4 — Sum of per-lane timeouts must respect the pass interval
autonomous_iteration grew lanes until sum(timeout=)=2820s vs INTERVAL=900s.
A slow day stacked passes. Fixes applied: rebalance timeouts (improvement_scan
300->180, ci_battery 600->300, glymphatic 300->120); daily-only lanes don't
count toward every-pass budget; passes serial+idempotent so overlap delays
rather than corrupts. Audit one-liner:

    grep -o 'timeout=[0-9]*' daemon.py | awk -F= '{s+=$2} END {print s}'

## LP6 — State files need atomic writes
`STATE.write_text()` mid-crash leaves torn JSON killing census continuity.
Fixed pattern:

    tmp = STATE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(...))
    tmp.replace(STATE)          # rename is atomic

JSONL appends are concurrency-safe ONLY as single newline-terminated
`f.write(json.dumps(rec) + "\n")` calls under O_APPEND (atomic below
PIPE_BUF on macOS). No multi-part writes; no flock needed at that shape.
flock is queued hardening only, not a defect.

## Ford-lane catch — a lane isn't live until wired into one_pass()
flow_lint.py ran green in manual invocations for hours while never wired
into the daemon's one_pass(). Manual runs prove nothing about 24/7
operation. Checklist when adding a lane:
1. write the organ script
2. write the `<x>_pass()` wrapper in the daemon
3. ADD the call + log key to one_pass()
4. kill-test the daemon (kill PID, sleep ~14s, launchctl shows new PID)
5. grep the next pass's log entry for the new lane key

## Deming D5 — instance fixes without a class fix = tampering
49 flow-lint findings (per-flow owner/sensor/verified gaps) existed; zero
tasks fixed the CLASS. The registry schema itself accepts flows without
required fields. Class-fix minted: schema must REQUIRE owner+sensor+
verified at registration (mint-time gate, genome-gate pattern). When a
scanner keeps minting instance findings, ask what upstream acceptance
gate is missing and mint THAT.

## Bridgman B5 — claimed metrics must be measured
the specialist engine's methodology names clearance rate K = Q_flow x dC as its
driving physics; K is computed nowhere. Physics stated but unmeasured =
decoration risk (same law as isomorphism falsifiability). Rule: every
methodology naming a quantity must ship the vital that measures it, or
the quantity comes out of the methodology.

## Ledger cleanup law (recurred this session)
The task ledger is append-only: DELETE forbidden ("tasks are birth
certificates"), states CHECK-constrained to
open/claimed/done/blocked/cancelled. Duplicate removal =
`UPDATE state='cancelled', outcome='...'` keeping MAX(id) per canonical
title prefix. Dedupe keys must be literal `title.startswith(key)` prefixes
matched across ALL states (open-only matching re-mints cancelled dupes).
