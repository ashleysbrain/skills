# Task → Workstream Mapping: First-Class Campaigns, Not Default Assignments

## The Problem (2026-08-18 session)

Minted 5 thinkery plan iteration tasks (T-0161..0165) with clear THK-* intent, but they were misassigned:
- 4 went to WS-4 the OS-KERNEL (KERN-087, KERN-088, KERN-089, KERN-090)
- 1 went to WS-2 the OS-CONDUCTOR (COND-008)

None went to a dedicated thinkery workstream. Why: `submit()` has a `lane` param but no explicit `workstream` param in this session's signature — the auto-classifier guessed based on title keywords ("architecture" → KERNEL, "motivation" → CONDUCTOR), and there was no WS-6 THINKERY yet defined.

## The Rule

**Every task must belong to the workstream that owns the CAMPAIGN it advances.** Workstreams are campaigns with exit conditions, not loose categories. If a new initiative requires multiple coordinated tasks, create a dedicated workstream first.

## Workstream Creation Protocol

1. **Add to WORKSTREAMS.md** with:
   - Mission (what the campaign achieves)
   - Exit condition (when it's DONE, not "feels done")
   - Open tasks (T-IDs)
   - Heart (the core loop)

2. **Add to stores/workstreams.json** (if your session uses a JSON registry) with:
   - id (WS-N)
   - name
   - description
   - arc_ids (which arcs this serves)
   - status (active/parked/completed)

3. **Explicitly assign tasks** when minting:
   ```python
   tl.submit(c, title, kind='build', lane='gg', origin='...',
            workstream='WS-6 THINKERY')  # ← explicit, never rely on auto-classify
   ```

## When to Create a New Workstream

- The initiative has >3 related tasks
- It has a clear finish line (exit condition)
- It serves a strategic arc (ARC-1..ARC-5)
- It will run for weeks, not hours

## When to NOT Create One

- Single one-off tasks (use existing WS by lane: WS-1 for research, WS-2 for conductor, WS-4 for kernel)
- Temporary coordination (use the todo list, not a workstream)
- Things that finish in <2 hours

## Verification

After minting a batch of tasks, verify assignment:
```python
c.execute("SELECT workstream, count(*) FROM tasks WHERE id IN (...) GROUP BY workstream")
```

If tasks are scattered across wrong workstreams, use the surgical gate to correct (or re-mint with explicit assignment — re-assigning task IDs breaks birth-certificate guarantees).
