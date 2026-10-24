# Compacted summaries + sibling sweeps: two verification traps (2026-08-19)

Caught during PASS-4 adversarial QA. Belongs in the numbered case list as #19/#20;
recorded here until the SKILL.md patch path reopens.

## Case 19: Compacted-summary identifiers are untrusted — grep the CONCEPT, not the name

- After context compaction, the handoff summary claimed the novelty-verdict store was
  `_NOVELTY_RECORDS`; `grep -n "_NOVELTY_RECORDS"` returned zero matches, which read
  as "the hardening was reverted by a sibling" — a false alarm nearly reported to the
  user as fact.
- **Root cause:** the compaction summary paraphrased the identifier; the real symbol
  was `_NOVELTY_SCANS`. A zero-match grep on a summarized NAME is evidence the name
  is wrong, not that the work is gone.
- **Fix:** when a grep for a summarized identifier returns zero, re-grep the CONCEPT
  (`grep -in "novelty" file`) before concluding anything. Never report "X was
  reverted/deleted" without a matched deletion in `git log -S` or a concept-level
  grep also coming back empty.
- **Also:** the same summary's "third raw INSERT at line 8026" was the gated main
  path itself. Summary line numbers and path claims are as untrusted as names —
  read the cited lines before acting on them.

## Case 20: "Commit failed: nothing staged" after a sibling sweep = work may already be committed

- `git add <files> && git commit` exited with "no changes added to commit" — yet the
  working tree had just received those fixes. First instinct (loss) was wrong.
- **Root cause:** a background guardian/sibling had already swept the modified files
  into its own commit. Verified with `git log -S "<distinctive marker>" --oneline --
  <file>` (found the changes inside the sibling's commit) and
  `git show HEAD:<file> | grep -c <marker>` (present at HEAD).
- **Fix:** on "nothing to commit" for files you KNOW you modified, run
  `git log -S '<marker from your edit>' --oneline -- <file>` and
  `git show HEAD:<file> | grep <marker>` BEFORE assuming loss or re-editing. If the
  work sits in a sibling commit, it is durable — cite that commit.
- **Corollary:** in shared repos with guardian sweeps, re-editing a file that "won't
  commit" can silently fork your changes against a moving HEAD. Verify first, edit
  second.
