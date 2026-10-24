# Backlog census: auditing past referrals for unactioned science

Periodic (and on-principal-demand) pass proving the ingest-and-act loop actually
acted. Trigger: principal says work is missing, or as a standing monthly surface.

## Census procedure
1. Pull every principal referral from `<agent-home>/state.db` (messages table,
   role='user'): match `http`, `lnkd`, `arxiv`, `nature.com`, `science.org`.
   `timestamp` is a unix float — format with `datetime.fromtimestamp`. Exclude
   system rows (CONTEXT COMPACTION, ASYNC DELEGATION, gateway JSON).
2. Bind each referral to an outcome, in this order of evidence:
   (a) corpus row: scan_results note carrying a principal-order marker + run_at
   within minutes of the message timestamp (notes like `principal order`/
   `principal batch` are the binding); (b) deliverables file; (c) bus/ledger
   build request citing it; (d) NONE = unaccounted.
3. Assistant-side verification is weak evidence (assistant messages can
   narrate without acting) — only corpus rows, file mtimes, and bus msg ids
   count as action proof. A `SELECT` read-back outranks any self-report.
4. Classify every referral into exactly three buckets: ACTED (mechanism or
   artifact exists), FILED-ONLY (corpus row, nothing built — the waste
   bucket), UNACCOUNTED. Report the three counts raw.

## Closing the gaps found
- FILED-ONLY: rank by organism value (what mechanism the science implies),
  mint build specs from the corpus notes themselves (the notes carry enough
  detail to write the brief), dispatch via the build path in
  references/dispatching-builds.md. Do not re-research what is already filed.
- UNACCOUNTED: fetch each URL; bind to an existing corpus row or file fresh
  with a full note; login-walled links get an explicit blocked-record with
  the cause — never silently dropped.
- The census result (three counts + gap list) doubles as the principal report;
  deliver numbers and dispatch ids, not intentions.

## Pitfall
- Do not claim a referral was handled because nearby assistant activity
  exists — bind by timestamp-proximate corpus/bus/deliverable artifacts only;
  assistant message volume in a window is not action evidence.
