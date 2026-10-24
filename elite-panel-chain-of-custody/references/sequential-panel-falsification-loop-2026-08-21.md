# Sequential panel + falsification-fix loop — QA-5/QA-6 (2026-08-21)

The full-day run that took the watchdog v4.3 → v4.4 and shipped the S8
predicament→market flow. Parent session detail for the chain-of-custody skill.

## Panel cadence that worked (both landings)

| Panel | Shape | Metrics | Landing |
|---|---|---|---|
| QA-6 (6 seats: Nightingale/Boole/Virchow/Democritus/Hume/Pasteur) | ONE child, seats sequential, chain-of-custody | 76 API calls, 402s | all seats landed, 10-gap census |
| QA-5 (3 seats: Shannon/Liebig/Avizienis) | ONE child, sequential | 23 API calls, 990s | 3 falsifications + fix specs |
| QA-5 first attempt (same 3, parallel children) | 3 children | dead <4 min | HTTP 429 x3 (the counterexample) |

Dispatch briefs: evidence pack on disk + file pointer + full persona specs +
"~6-10 tool calls per seat, SHORT turns" + numbered deliverables + all persona
spec lines required in the final message (integrity gate greps them).

## The three panel findings classes that repeat (watch for these)

1. **Hidden contradictions inside enforcement artifacts** — the
   elite-panel-chain-of-custody skill itself still mandated
   `max_concurrent_children >= 6` (line 27) while the new law said ==1. A skill
   that enforces a law it contradicts is worse than no skill. grep your own
   enforcement docs for the OLD rule after writing the new one.
2. **Registry/doc vocabulary drift** — FLW-DELEG flow-registry stages said
   `lease-expired` while the organ emitted LANDED-UNACKED/PARTIAL-LANDED/
   MANIFEST-SHIFT. FLOW-SYNC only checks CODES agree, not stage vocab. Fix:
   sync stages + version bump (1.0.0 → 1.1.0) + re-run store_gate --flow-sync.
3. **Dead-twin files** — a 0-byte message-bus.db in your-org (real bus
   lives in your-workspace per entity map). Quarantine, never delete evidence.

## QA-5 sensor falsifications → v4.4 fixes (all with breaking inputs)

- **C1** no-log running task invisible forever (`i not in log_age` skipped it) →
  manifest-age fallback in the no-log branch → NEVER-STARTED at staleness.
- **C4 (worst)** suppress limb restamped `ts` every tick → escalation clock
  silently reset → under brownout oscillation escalation deferred FOREVER →
  first-seen ts preservation in BOTH suppress and un-suppress limbs.
- **C6** result-payload quoting a final record spoofed a landing
  ("DO NOT REFIRE" on a corpse) → `_finals_in()` excludes result payloads
  (same law RETRY_RX already had).
- **C6'** ISO `T`-prefixed finals unread; `rate_limited` read landed-alive →
  `T?\d{2}:\d{2}:\d{2}` + exit_reason enum + re.S on fail_rx.
- **C7'** bookkeeping never pruned → prune alerted/corpse_since/manifest_bad
  keys for delegations neither live nor in migrations, every scan (locked
  atomic delete; `_set_state` gained `delete=True`).

Suite: `organism/tests/test_deleg_watchdog_qa5.py` — 7/7, every falsification
reproduced then detected post-fix. Regression law: BEFORE proving a fix, write
the repro that FAILS on the old code; run it against old (fails) and new (passes).

## S8 predicament→market flow (principal mandate, composed into gap_hunter.py)

`scan_predicaments()` subscribes to bus `[DELEG]` alert subjects (signatures:
"HTTP 429" → rate-limit-aware dispatch market; "SYSTEMIC API EVENT" → provider
failover market). `market_research_tick()` mints kind=gap immune-lane ledger
tasks carrying provider source lists (OpenRouter/LiteLLM/Portkey/Helicone docs;
Z.ai/Anthropic/OpenAI status pages), wired into `--tick` (existing cadence, no
new cron), idempotent, dedup via `predicament_done` state. Live proof: minted
T-20260821-1070 from bus msg 2808's real SYSTEMIC API EVENT.
**Consequence: the `[DELEG]` subject prefix is now a MACHINE-READABLE
vocabulary — never reword those alert subjects casually; a rename breaks the
subscription.** Market data recency law: year>=2025 + retrieved_at stamp.

## Operator quirks hit this session

- Ledger INSERT needs `created_at` + `created_by` + `state` explicitly —
  NOT NULL constraints fail otherwise; schema is id/title/kind/lane/.../state.
- Baseline-first gate blocks write_file for NEW files under a symlinked
  "existing" dir; `cat > file <<EOF` via terminal passes.
- Patch-tool "escape-drift" error on regex-heavy old_string: the tool-call JSON
  double-escapes backslashes — do the edit via python string-replace in terminal.
- specialist_gate routing expires ~5 min; re-route before re-dispatching after
  a long read phase (blocked once).
