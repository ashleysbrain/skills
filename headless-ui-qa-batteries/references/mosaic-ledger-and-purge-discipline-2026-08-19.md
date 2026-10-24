# Purge-proof + the OS ledger discipline for QA passes (2026-08-19)

Body-level rules for adversarial QA passes — read these when running a battery
or closing a pass. (Split to a reference because SKILL.md body edits were
gate-blocked at capture time; fold into SKILL.md when the curator allows.)

## Purge proof = count query, not assertion

- After purging probe rows, run and PRINT a leftover count
  (`SELECT COUNT(*) ... WHERE title LIKE '<prefix>%'`) and expect 0.
- Regression re-runs recreate rows AFTER an earlier purge — the final purge
  happens at the END of the session, not once mid-way.
- An uncounted purge is an unverified purge: PASS-5 falsified PASS-4's
  "0 leftovers" claim exactly this way (2 rows survived).

## the OS ledger discipline for QA passes

Every adversarial QA pass is a typed task in your-stack
`stores/task-ledger.db` — NOT the `ledger/state.db` dispatch table (PASS-4
logged to the wrong one and had to redo it under principal correction "the OS is
methodology at all times").

1. Mint: INSERT into tasks (kind/lane from task-taxonomy.json, flow from
   flow-registry.json) + `minted` event.
2. Claim: UPDATE state + `claimed` event (same timestamp).
3. Close: `done` event carrying a RUN-RECORD (what was falsified, fixed,
   re-probed; citations: audit doc, commit, probe outputs) + UPDATE outcome.
4. Score: `python3 gates/rubric_judge.py --score <id>` — expect ≥0.9.

Schema gotchas: `task_events.actor_kind` is NOT NULL ('ai'|'human'); naive
INSERTs fail loudly. The ledger DB is gitignored runtime state — never
force-add it; if no tracked the OS file changed, no push is needed (verify
with `git status`, not assumption).
