# Pending SKILL.md body edits (2026-08-18, session: QA-17 + thinkery plan)

Apply at next foreground curator pass (the _read_before_write guard
blocks background body patches; reference-file writes succeeded).

## Edit 1 — add to SKILL.md "## References" list

```
- `references/sibling-writers-scheduler-liveness-2026-08-18.md` —
  multi-writer ledger defects (counter desync, raw-INSERT closes,
  repo self-override), scheduler-liveness canary pattern, QA sweep
  order, manifest-probe hardening.
```

## Edit 2 — extend "## Iteration protocol" with a step 7 (sibling safety)

```
7. **SHARED-MACHINE DISCIPLINE**: the ledger has multiple live writers
   (desktop hermes, terminal hermes, sibling-agent). Before committing on a
   shared branch: `git pull` first, and re-verify your edit survived
   the push (grep the pushed tree, not the working tree). Never assume
   sole-writer on task-ledger.db or the repo.
```

(Rationale: three sibling-writer defect classes hit on 2026-08-18 —
counter desync fixed by collision-convergent mint(), raw-INSERT closes
scored FAIL by the judge, and a sibling push overwrote a CI fix.
Full detail in the sibling-writers reference, which IS live.)
