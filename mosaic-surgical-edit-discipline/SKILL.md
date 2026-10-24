---
name: mosaic-surgical-edit-discipline
category: software-development
description: Use when editing any file in the your-stack package.
version: 1.0.0
author: the operator agent Agent
license: MIT
metadata:
  hermes:
    tags: [mosaic, surgical, editing, discipline, self-override]
    related_skills: [surgical-code-patching, baseline-first-surgical-precision]
---

# the OS Surgical Edit Discipline (OS-enforced)

Origin: principal directive 2026-08-17 (voice note): "Make sure that the operating
system doesn't override itself. And every action needs to be done in the
surgical precision." Built as `gates/surgical_gate.py` in the the OS method
package (`~/your-org/your-stack/`), task T-260817-0015.
This skill is the operator-side habit layer; the gate is the enforcement.

## When to use

- Editing ANY file inside `your-stack/` (gates, stores, docs, configs)
- Editing any store or DB the OS owns (scheduler.db, task-ledger.db,
  registry, events log, surgical.db itself)
- Any time two actors (hermes / sibling-agent / sibling-agent / human) can touch the
  same file

## The two rules

1. **Self-override prevention.** The OS must never clobber itself: no
   concurrent writers to one file, no lost updates, no selftest touching
   production state. Enforced by expiring leases (TTL 300 s) in
   `ledger/surgical.db` — a second claimant inside the TTL is REFUSED
   with the holder named; expired leases self-free (crashed editors can't
   freeze files).
2. **Surgical precision.** Every edit: unique anchor (exact-once match or
   declared count), single contiguous region (multi-region = separate
   calls), atomic apply (same-dir temp + os.replace), verify-after
   (re-read: new present, old gone). An edit that can't prove itself is a
   refuse, logged to the hash-chained audit.

## Exact usage (working pattern)

```python
import sys; sys.path.insert(0, "gates")
from surgical_gate import SurgicalEdit

g = SurgicalEdit()  # uses ledger/surgical.db
r = g.apply(path, old, new, actor="hermes")
if not r.ok:
    print(r.refused_because)  # lease held? anchor moved? verify failed?
```

Refusal reasons are actionable, not fatal: if "anchor not found — file
changed under you", RE-READ the file and re-plan; if "lease held by X",
wait for TTL expiry or coordinate with X on the bus; if multi-match,
narrow the anchor with surrounding context lines.

## Manual / verification commands

- `python3 gates/surgical_gate.py --selftest` — 13 cases, tempdir-isolated
- `python3 gates/surgical_gate.py --chain-ok` — audit hash-chain intact
- CI runs both on every push to your-org/your-stack

## Pitfalls

- **Fuzzy-match temptation.** The gate refuses fuzzy anchors on purpose.
  Don't bypass it with manual whole-file rewrites on package files — that
  is the non-surgical anti-pattern the gate exists to block.
- **Multi-region edits.** Want to change 3 places? That's 3 surgical
  applies, each uniquely anchored. Never widen a diff to "save calls".
- **Empty anchor = whole-file rewrite.** Refused. If a rewrite is truly
  needed, it's a new-file + review operation, not a surgical edit.
- **Lease discipline.** Long edit sessions re-claim (renewal allowed for
  the same actor) and release when done: `g.claim(p, "hermes")` then
  `g.release(p, "hermes")`.
- **Selftests must never touch production stores.** The QA-PASS-10 D2
  defect class (a selftest unlinking prod scheduler.db) is structurally
  impossible here: selftest DBs are tempdir-pinned.

## Enforcement surface

- CI step "Surgical audit chain integrity" (chain-ok) on every push
- Gate battery in CI includes surgical_gate selftest
- Audit chain: every claim/apply/refuse is hash-chained; tampering breaks CI

## Related

- `PROCESS-FLOWS.md` Flow 7 (surgical edit) in the your-stack package
- skill `surgical-code-patching` (numbered patches, same philosophy)
- skill `baseline-first-surgical-precision` (deliverable-level variant)
