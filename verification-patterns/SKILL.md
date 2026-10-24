---
name: verification-patterns
description: Verify live surface first. Check API then UI, not code.
---

# Verification Patterns — Live Surface First, Assumptions Second

## Trigger
Use when you receive a user report like "I see no updates," "not working," "broken," or similar complaint about the live surface.

## Core Principle

**Verify what the user actually sees before concluding something is broken or not implemented.**

The user's report is **what they see on their device**, not the system state. There are many reasons for a mismatch:

- Browser cache (stale HTML/CSS/JS)
- Stale view (user viewing old tab)
- Local state differences (hard-refresh needed)
- Network issues
- User-specific context

## The Failed Pattern (What NOT to Do)

```
User: "I see no updates to the health"

❌ WRONG: Assume "not implemented" → start building new endpoints → waste time

Result: You discover the endpoint exists and works, but user had cached view
```

## The Effective Pattern (What TO Do)

### Step 1: Check Backend API First
```bash
curl http://127.0.0.1:port/api/health/state_signal
```
If API returns data → backend is working → proceed to step 2

### Step 2: Check Live Surface (not code, not logs)
```python
open_preview(url="http://127.0.0.1:port/#view=health")
read_preview()
```
Read what the surface actually renders, not what you think it renders

### Step 3: Identify the Gap

| Backend | UI | Diagnosis |
|---------|----|----------|
| ✅ Works | ✅ Shows correct data | User has cache/stale view → recommend hard-refresh |
| ✅ Works | ❌ Shows wrong/no data | UI bug (not rendering correctly) |
| ❌ Error/404 | — | Backend endpoint missing/broken |

### Step 4: Take Correct Action Based on Diagnosis

**If gap = cache/stale view:**
- Tell user: "hard-refresh (Cmd+Shift+R)"
- Verify: ask user to refresh, confirm data appears

**If gap = UI bug:**
- Fix UI rendering (not backend)
- Test: refresh UI, verify data appears

**If gap = backend missing:**
- Build backend endpoint
- Test: curl returns data

## Session Evidence

### Session: 2026-08-27 — the OS OS Surgical Edits

**User report:** "I see no updates to the health"

**My wrong assumption:** Health state signals not implemented

**Verification (correct):**
1. Checked backend API: `/api/health/state_signal` returned valid data ✅
2. Checked live surface: UI showed correct data ✅
3. **Diagnosis:** User had cached view, not implementation gap
4. **Action:** Recommending hard-refresh, not building new endpoints

**Evidence:**
```bash
$ curl -s http://127.0.0.1:port/api/health/state_signal
{
  "state": "live",
  "signals": {
    "cognitive_load": "NORMAL",
    "energy_level": "RESERVED",
    "focus_span": "SHORT",
    "stress_signal": "WATCH"
  }
}

$ # Live surface read_preview() showed:
# "OPERATOR STATE SIGNALS\nCognitive Load NORMAL\nEnergy Level RESERVED\nFocus Span SHORT\nStress Signal WATCH"
```

**Result:** The feature was already working. I wasted time assuming "not implemented" when it was actually "cache issue."

## Related Patterns

- **Triangle-offense** (see T-260827-0037): Multi-pass verification with rotated profiles
- **Nullius evidence**: Every finding must have command/selector/observed proof
- **Live surface testing**: Always verify what user sees, not what code says

## BUILT ≠ WIRED ≠ RUNNING — absence claims and delivery claims (2026-08-28)

Two verification failures from one session, both principal-caught:

### 1. Absence claims require a BROAD query first
Claimed "the audio directives were never minted" after a query that filtered
out overnight rows (`origin` + date filter missed sister-thread mints). The
directives existed — minted 6x each by bridge responders. The claim was made
on incomplete evidence and triggered a duplicate mint storm (22 dups).

**Rule:** before reporting "X doesn't exist / never happened," re-query with
the WIDEST net (drop filters, search by content prefix across all origins,
check sibling-thread stores). Absence is a stronger claim than presence and
needs stronger evidence.

### 2. Delivery claims must be probed against the LIVE system, not the artifact
A done task's outcome said "hermes #4436 carries delivery limb" — the job
didn't exist (previous cron system, numeric IDs, never migrated). A built
daemon no-op'd silently for 8 hours because its key-fetch couldn't see the
env (see daemon-cadence-architecture). Retroactive audit found 26 done-builds
citing dead delivery mechanisms.

**Rule:** any outcome claiming "X carries/delivers/fires Y" must be verified
by EXECUTING the check (launchctl print, curl :port/health, cron/schedule
registry grep, ps for the process) — proof-shaped TEXT (regex-visible exit
codes, offsets near verdict words) is not proof. States are distinct: BUILT
vs WIRED vs RUNNING; "done" requires RUNNING or an explicit BUILT-INERT
label with owner + activation ticket. Liveness is COMPUTED from event logs,
never self-reported (adversarial S10 law).

## Support files
- `references/mint-storm-and-approval-drain-2026-08-28.md` — the 22-dup mint
  storm (filtered-query absence claim), the dedup pattern, and the
  approval-drain loop directive.

## Pitfalls to Avoid

1. **"User report = system state"** — User report is what they see, not what the system does
2. **"Not working = not implemented"** — Could be cache, UI bug, network, user error
3. **Assume without verification** — Check API, check live surface, then diagnose
4. **Fix the wrong thing** — Building backend when UI is broken, or vice versa
5. **Temporal claims from memory or mental math** — Session (2026-08-28): the operator agent claimed "sibling-agent dead 3+ days" and "appointment in 40 mins" without system verification. Both were FALSE. The user corrected: "your timezone and clock is off... my appointment is NOT in 40 mins" and "you failed this training." Temporal facts require ACTUAL system verification, not recall or mental computation. Use `date` (terminal) for current time, compute distances programmatically (`python3 -c "from datetime import datetime; t1=datetime.fromisoformat('2026-08-28T12:45'); t2=datetime.now(); print(f'{(t2-t1).total_seconds()/60:.1f}')"`), verify timestamps from logs (e.g., `grep` for BOOT timestamps in sibling-agent-autonomic.log). NEVER claim temporal fact without log verification.

## Templates

### Diagnostic Checklist
```markdown
1. Backend API check:
   - [ ] API endpoint returns data (curl test)
   - [ ] Data is correct (not error/404)

2. Live surface check:
   - [ ] Open live surface (open_preview)
   - [ ] Read actual rendered content (read_preview)
   - [ ] Compare backend data vs UI rendering

3. Gap diagnosis:
   - [ ] Backend working + UI working → cache/stale view
   - [ ] Backend working + UI broken → UI bug
   - [ ] Backend broken → backend issue

4. Action:
   - [ ] Cache: recommend hard-refresh
   - [ ] UI bug: fix UI rendering
   - [ ] Backend: build/fix endpoint
```

## Neuroplasticity

This pattern emerges from principal correction: "do another pass... find your gaps and improve on them long term."

Effective patterns (verify first) should be wired as skills for reuse. Failed patterns (assume without verification) should be documented for avoidance.

Neurons that fire together wire together — verify first, then act.