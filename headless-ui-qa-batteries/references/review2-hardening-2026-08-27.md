# Review-2 hardening patterns — conductor surface, 2026-08-27

Session: 10-seat elite adversarial review of the principal surface (conductor :port)
plus the response limb and memory-pin hygiene gate. Seat verdicts live at
`~/your-workspace/relabel-work/verdicts/review2-seat-01..10.json`. This file
carries the reusable patterns, not the session narrative.

## 1. CSRF gate for localhost JSON daemons (seat-04, HIGH)

Python HTTP daemons that parse POST bodies with `json.loads` regardless of
Content-Type accept `text/plain` cross-site POSTs — preflight-free, so any
third-party page can drive every mutating endpoint. Gate at the top of
`do_POST`:

- Read `Origin` (fallback `Referer`). Absent header (curl, native tools) → allow.
- Present header → hostname must be in (`127.0.0.1`, `localhost`, `::1`) and
  port must match the `Host` header (or be the daemon's own port).
- Else `403 {"error": "cross-origin POST blocked"}`.

Also add to EVERY response (the `_json` writer is the single choke point):
`X-Frame-Options: DENY` + `Content-Security-Policy: frame-ancestors 'none'`
(kills clickjacking on ruling buttons).

Verify with three curls: evil Origin → 403, no Origin → 200, same-origin → 200.

## 2. Honest multi-store write responses (seat-02)

When one API action fans out to N stores (bus + ledger + jsonl + memory),
NEVER return a hardcoded `true` per leg. Pattern from `/api/respond`:

```python
ledger_ok, ledger_err, guidance_ok, pinned = False, None, False, False
# ... each write in its own try/except that sets its own flag and,
# on failure, captures f"{type(e).__name__}: {e}"[:200] into ledger_err
return self._json(200, {"status": "sent", "bus_id": bus_id,
    "ledger_event": ledger_ok, "ledger_error": ledger_err,
    "guidance": guidance_ok, "memory_pin": pinned})
```

The UI confirm line prints exactly what landed (`bus #4335 · pinned`), so a
degraded leg is visible to the user AND to every future battery.

## 3. flock + atomic rename for jsonl stores under threaded servers (seat-03 F4 / seat-08 P2)

Read-all → rewrite-all compaction with no lock loses appended rows when a
POST races a compaction (lost-update; appends vanished from BOTH working set
and archive in 4/20 trials). Fix, verified with a 7-thread race test:

```python
import fcntl, tempfile, os
lockp = STORES / "glia" / ".pin_hygiene.lock"
with open(lockp, "w") as lockf:
    fcntl.flock(lockf, fcntl.LOCK_EX)
    try:
        return _compact_pins_locked(max_pins)   # existing logic
    finally:
        fcntl.flock(lockf, fcntl.LOCK_UN)
# and inside, the rewrite:
fd, tmp = tempfile.mkstemp(dir=str(PINS.parent), suffix=".tmp")
with os.fdopen(fd, "w") as f: ...        # write full working set
os.replace(tmp, PINS)                    # atomic; crash-safe
```

Archive FIRST (append losers verbatim), then atomically replace the working
set. Also: archive dedupe losers, not just cap-overflow — variant wordings
that collapse must be recoverable (the "nothing is lost" law).

## 4. ID-format gates must be derived from the store (session root cause)

Two ID generations coexist in the ledger: canonical `T-20260826-0245`
(8-digit) and legacy `T-260817-0006` (6-digit). A validator written from
memory (`T-\d{8}-`) silently rejected 286 legacy rows — a write gate that
fails closed with zero error output. Before writing ANY ID regex:
`SELECT DISTINCT substr(id,1,12) FROM tasks` and match what exists
(`T-\d{6,8}-\d+`). Grep for the same pattern at every consumer (daemon gate,
daemon linkify, screen linkify) — they drift independently.

## 5. Count-integrity: totals must share the list's predicate (seat-10)

`rulings_total` computed with a narrower WHERE than `rulings_pending`
(4 vs 5 live) masks the overflow hint forever. Rule: any `N more hidden`
denominator must be the SAME SQL predicate as the visible list — or simply
`total = len(pending_list) + overflow_count` computed from one query.

## 6. Panel operating notes (what made the 10-seat review work)

- Dispatch in waves of ≤ `delegation.max_concurrent_children` (6): wave-1
  wiring/backend/data/security/HCI/a11y, wave-2 iconography/perf/provenance/
  red-team. Same total elapsed, no queue overflow errors.
- Every seat gets: live URLs, file paths, its credential persona, an OUTPUT
  file path, and a safety contract (READ-ONLY vs prefixed test payloads vs
  /tmp copies). Seat-03 ran 12 edge cases against /tmp COPIES with md5
  verification that live stores were untouched.
- Re-dispatch seats that die on rate-limit (429) with UPDATED context — the
  second run must see the fixes the first run's siblings already shipped.
- The highest-value seat finding was about the OPERATOR's verification
  method (vacuous check), not the product. Include a provenance/claim-audit
  seat that explicitly re-verifies the operator's own "verified" claims
  against live state.

## 7. Surface-laws reinforced this session (principal directives)

- Conductor calendar = ORGANISM WORK ONLY (AI/tech operating view):
  source whitelist (mosaic/cron/engine/pipeline/writing/publication/
  posting/bus) + `route != 'human'`. User-personal items (notion etc.)
  belong to the user's separate surface. Battery: 0 personal rows, all
  routes `ai`.
- DESIGN-stub rows on a default view are ship-blockers ("one stub tells a
  principal the whole page is a mockup") — show BUILT things, move roadmap to a
  drawer or drop it.
- Hash-state: `setView` writes `#view=<v>`, load restores it, else default.
  Refresh/Back/deep-links must not bounce the principal to the default view.
- Voice limb (Ask/Comment/Pin) belongs STRUCTURALLY on the drawer chrome
  (sibling of drawer-body), not wired per-view — a footer on the `<aside>`
  cannot be forgotten when a new drawer view is added.
