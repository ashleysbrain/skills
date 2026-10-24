---
name: memory-integration-verification
description: Audit if memory stores are used at runtime, not just theory.
version: 1.0.0
author: the specialist engine
license: MIT
metadata:
  hermes.tags: [memory, integration, audit, okeefe, verification, infrastructure]
  hermes.category: infrastructure
  hermes.related_skills: [okeefe-memory-routing, hermes-hippocampal-memory-architecture]
---

# Memory Integration Verification

## When to Use

- Auditing whether O'Keefe (or any T2 store) is actually queried at runtime
- Diagnosing "amnesia" — the operator agent forgetting project facts it should know
- After any change to the memory stack (boot hooks, routing skills, engine restarts)
- Verifying a "memory system rebuild" claim actually fixed the problem

## Core Principle

**Infrastructure that exists but is never called at runtime is equivalent to
infrastructure that doesn't exist.** A memory engine with 29 stored memories
that is never queried during real work provides zero value. The integration
gap is more dangerous than the engine bugs — a broken engine fails loudly; an
uncalled engine fails silently.

## Audit Methodology (5 checks, all read-only)

### Check 1: Has recall() EVER been called during real work?

Search session history for actual runtime usage (not build/test sessions):

```
session_search(query="okeefe_bridge recall project state", sort="newest")
session_search(query="okeefe_bridge.py recall during task", sort="newest")
```

**Red flag:** If the only hits are from the session that BUILT the bridge
or from audit sessions, recall has never been used for real work.

### Check 2: Do boot hooks query the memory store at session start?

Read each boot hook script:
```
read_file("<agent-home>/agent-hooks/hydra-memory-stack-bootstrap.py")
read_file("<agent-home>/agent-hooks/procedural-memory-boot.py")
```

Check for two failure modes:
- **Print-only hooks:** The hook `print()`s a rule like "O'Keefe for T2" but
  never calls `recall()` or `POST /retrieve`. This is documentation, not integration.
- **Failing hooks:** Check `<agent-home>/gateway-stderr.log` for hook failures
  (`grep 'hook failed' gateway-stderr.log`). Hooks that fail with `[Errno 35]`
  or timeouts run on every session start but accomplish nothing.

### Check 3: Does any cron job recall before starting work?

```python
import json
data = json.load(open("<agent-home>/cron/jobs.json"))
jobs = data.get("jobs", data)
for j in jobs:
    if j.get("enabled"):
        prompt = (j.get("prompt") or "").lower()
        has_recall = "recall" in prompt
        has_okeefe = "okeefe" in prompt
        if has_recall or has_okeefe:
            print(j["id"], j["name"])
```

**Red flag:** If zero cron jobs reference recall/okeefe in their prompts,
every cron job starts from scratch with no memory of past project state.

### Check 4: What is the REAL recall path?

Trace what the operator agent ACTUALLY does when it needs a project fact:
1. Read MEMORY.md flat buffer — is it T0-only? Then project facts are invisible.
2. session_search — searches past conversation text (T1 episodic), not structured memory.
3. The memory() built-in tool — can it be intercepted/routed? (Answer: no, it's a built-in.)

If O'Keefe recall is not in this list, the T2 store is write-only.

### Check 5: Does recall actually return correct results?

Test with queries that have NO keyword overlap with the target memory:

```bash
python3 okeefe_bridge.py recall "what font does the user prefer"
python3 okeefe_bridge.py recall "typeface lettering text style"
```

**Red flag:** If the wrong memory is returned, the embedding truncation
(384→128 dim) has destroyed semantic discrimination. See Pitfall: Recall
Quality below.

## Pitfall: Recall Quality — Strength Inflation

### The Bug

The consolidation cron inflates memory strength over time. Previous hybrid
scoring formulas used strength as a major component:

**v2 formula (DEAD — do not revert):**
```
final = max(0.5 * keyword_score, 0.3 * semantic_floor) + 0.2 * semantic_bonus
```
Consolidated memories reached strength 1.0-1.3, giving them an unearned floor
of 0.3-0.39 even with ZERO keyword overlap. This caused the "strength-monopoly
degenerate regime" where the same 5 high-strength memories dominated every
query regardless of topic. the specialist engine proved 4/5 queries returned wrong results.

**v3 formula (CURRENT, verified 2026-08-12):**
```
final = 0.8 * keyword_overlap + 0.2 * normalized_strength
```
Keyword overlap is the PRIMARY signal. Strength is only a tiebreaker. A memory
with zero keyword overlap can NEVER beat one with keyword overlap, regardless
of strength differentials. Multi-suffix stemmer handles -tion, -ment, -ness,
-ing, -ed, -er, -ly, -s. Verified: 9/9 recall tests pass.

### How to Detect

```bash
# Query with no keyword overlap to the correct memory:
python3 okeefe_bridge.py recall "what font does the user prefer"
# If this returns diagnostics/autoheal instead of the font preference, the bug is active.

# Query WITH keyword overlap:
python3 okeefe_bridge.py recall "Inter DM Mono Manrope Sora font"
# If this returns the correct result, keyword re-rank is working but semantic is not.
```

### The Deeper Problem

Even if the integration gaps are fixed (boot hooks query O'Keefe, crons recall
before work), recall will return WRONG answers for any query that doesn't
contain exact keywords from the target memory. The 128-dim truncation is
fundamental — the bridge's hybrid re-rank mitigates but does not solve it.

## Pitfall: O'Keefe Dies Silently

The engine on :port can die without any work-blocking alert. The auto-repair
watchdog (cron 132dd1d69078) detects and restarts it, but between death and
restart, all store/recall calls silently fail. There is no health-gate that
blocks work or alerts the user when the hippocampus is offline.

**Diagnostic:**
```bash
curl -s http://127.0.0.1:port/health | python3 -m json.tool
# status:"ok" = v1.1.0 (good). status:"online" = v1.0.0 (stale, no text field).
```

## Pitfall: Writing Durable Facts Into the T0 Pointer Block (2026-08-26)

The memory() built-in's small character-capped block is a POINTER buffer, not a knowledge store. Two failure modes observed live:

1. **Capacity cramming:** editing the block directly to add a durable fact hits the ceiling within 2-3 entries, forcing shortening of OTHER entries (data loss by compression) and eventual operation-refusal loops when repeated adds/removes churn past the limit. The harness rejects the whole batch atomically; retrying the same oversized batch fails identically — diagnose by reading the reported current_entries, remove enough stale text to clear real headroom, then add.
2. **Regenerated (wrong) law text:** writing a "corrected" rule from memory of the conversation instead of first recovering the ORIGINAL ruling (via session_search) produces inverted laws — e.g. writing "always offer a type-your-own-answer option" when the standing law was "choices render as BUTTONS, never typed letters." Session history is the source of truth; the pointer block is not.

**Correct routing (standing order):** durable facts → O'Keefe T2 via `memory_bridge.py remember "<facts>" --source <id> --tags <tags>`; the T0 block gets one pointer line (T2 memory id + one-clause summary) ONLY, and only when headroom exists. Before writing any law-like text into memory, `session_search` the original ruling first and preserve it verbatim. When the block is full, leave memory unchanged for the turn and complete the pointer write next turn after pruning — never compress other entries to force a fit.

## Verified State (2026-08-12 audit)

See `references/integration-audit-2026-08-12.md` for full evidence from the
audit that established this methodology.
See `references/okeefe-engine-bugs-2026-08-12.md` for the complete bug catalog
(11 FIXED, 4 OPEN) from both elite panel rounds.

Key findings from that audit:
- O'Keefe alive (29 memories, v1.1.0)
- recall() NEVER called during real work tasks
- Zero of 32 cron jobs recall from O'Keefe
- Boot hooks: print-only (procedural-memory-boot) or failing (hydra-memory-stack-bootstrap, 21+ [Errno 35] failures)
- Recall quality broken: wrong results for non-keyword queries
- T2 content duplicated in T0 buffer (font pref, process restart fact)

### FIXES APPLIED (same session, 2026-08-12)

- **Boot hook now injects T2:** procedural-memory-boot.py calls
  `_recall_t2_snapshot()` at session start, querying O'Keefe for 10 key
  project memories and injecting them into boot context. Every new session
  now starts with T2 hippocampal state loaded.
- **Recall formula v3:** Keyword-dominant scoring (0.8 keyword + 0.2 strength)
  eliminates strength-monopoly. 9/9 recall tests pass.
- **Novelty drop surfaced:** server.py returns `status:"dropped"` (not
  `status:"encoded"`) when novelty < threshold, so callers know the memory
  was rejected.
- **Corruption backup:** load_snapshot backs up corrupt files before returning
  None, preventing silent total amnesia.
- **Ghost CA3 attractors fixed:** novelty check moved BEFORE ca3.store() so
  rejected memories don't leave orphan attractors.
- **_trace_order guard:** duplicate trace_id check prevents order corruption.

## Relationship to Other Skills

- `okeefe-memory-routing` (USER-OWNED — cannot be auto-patched): Documents
  the T0/T2 routing rules and API contract. Its recall quality pitfall docs
  still reference the OLD v2 formula. The v3 formula (0.8*keyword + 0.2*strength)
  is the current truth. Recommend `hermes curator adopt okeefe-memory-routing`
  to enable updates.
- `hermes-hippocampal-memory-architecture` (USER-OWNED — cannot be auto-patched):
  Documents the 5-system architecture. Contains a FALSE claim: "Pre-Session
  Boot Sequence step 4: Queries O'Keefe for relevant T2 project state" —
  this was false when written but is NOW TRUE as of 2026-08-12 (procedural-
  memory-boot.py calls _recall_t2_snapshot). The Compression Rule section
  also has stale API field names (location instead of location_vector,
  max_results instead of n_results). Recommend
  `hermes curator adopt hermes-hippocampal-memory-architecture` to fix.

## Verification Commands (quick)

```bash
# Is O'Keefe alive?
curl -s http://127.0.0.1:port/health

# How many memories stored?
curl -s http://127.0.0.1:port/memories | python3 -c "import sys,json; print(json.load(sys.stdin)['memory_count'])"

# Does recall work? (test with non-keyword query)
cd /<workspace> && python3 okeefe_bridge.py recall "typeface lettering"

# Are boot hooks failing?
grep 'hook failed.*hydra-memory' <agent-home>/gateway-stderr.log | wc -l

# Does any cron recall?
python3 -c "import json; d=json.load(open('<agent-home>/cron/jobs.json')); print(sum(1 for j in d['jobs'] if j.get('enabled') and ('recall' in (j.get('prompt') or '').lower() or 'okeefe' in (j.get('prompt') or '').lower())))"
```
