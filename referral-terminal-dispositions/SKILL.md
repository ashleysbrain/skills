---
name: referral-terminal-dispositions
description: Use when referrals drop or digest. Gate + card mechanics.
version: 1.0.0
author: the operator agent Agent
provenance: agent
license: MIT
tags: [referrals, follow-strength, dispositions, digest-cards]
related_skills: []
---

# Referral terminal dispositions

## When to Use
Trigger: a referral has completed its read + pipeline stage and needs its
termination — (a) the pipeline returned panel-PASS but the follow-strength
scorer says WEAK/SKIP (drop mechanics), (b) the referral is a plain science
article URL with no comment target (digest card lane), or (c) a comment
pipeline run needs launching and babysitting (execution discipline). Also
fires on duplicate background-completion receipts for a run already
dispositioned.

Class of task: a principal referral (LinkedIn post, plain article URL) has been read
and run through the comment pipeline (or is a science article with no comment
target). This skill executes the TERMINAL disposition correctly: the fs-gate
drop when the scorer overrules a unanimous panel, the science digest card when
the referral is a plain article, and the execution discipline for multi-minute
pipeline runs.

## Referral intake mechanics (before any disposition)
- **Resolve lnkd.in shares with curl, not extractors.** `curl -sIL` the short
link and read the final `location:` header, then fetch the resolved URL and
parse `og:title` + `og:description` with a desktop UA. LinkedIn article pages
403 under keyless extraction while the og layer still returns the author, the
claim, and usually the full numeric findings. Cache the HTML to scratch before
parsing so re-parses never re-hit the network.
- **A truncated og:description (post text cut mid-sentence) means the numbers
past the cut are UNVERIFIED** — file them as explicit gaps in the mint/corpus
row; never round off or complete them from plausibility.
- **Multi-referral turns batch-resolve first.** Referral storms arrive 2-4
links at a time; run one curl loop resolving ALL links, then disposition each.
The principal expects every link of a batch metabolized in the same reply.
- **Dup-check the corpus before minting a dissection.** research_scans.db
scan_results: LIKE on title/note, url fragment is the strongest key. An
author with 10+ prior rows is a TRACKED AUTHOR — register the new post as a
seen-row cross-referencing the thread and mint nothing; the dissection task
would duplicate an existing lane.
- **Corpus inserts race live writers.** Open with busy_timeout, wrap in BEGIN
IMMEDIATE, one statement per execute() call, and verify by SELECTing the url
back — a locked db raises OperationalError that a silent retry loop can mask
as done.
- **BUILD-lane minting** goes through your-stack/gates/task_ledger.py per
skill `mosaic-ledger-mint-close` (title cap, GENOME block, flow vocabulary);
carry the corpus row id in the task detail so task and corpus cross-link.

## Law: the follow-strength scorer outranks the panel
A pipeline result of panel-PASS (even 6/6 unanimous) with fs band WEAK or SKIP
is DROPPED, never delivered and never parked at the principal seam. Unanimity does
not clear a comment; the value battery is binding (typical failure: value
18-40 with reach 85 — panel liked the argument, scorer found nothing only we
could say). The principal is never the repair loop: weak candidates iterate inside
the pipeline or drop to knowledge.

## Drop-to-knowledge mechanics (one script, in order)
1. Score independently: `follow_strength.score_follow_strength(comment, [])`
   with `writing-studio` on sys.path. Record score, band, all four batteries
   (value, engage, voice, reach).
2. Log one row in `writing-studio/linkedin_metabolism.db → follow_strength_log`
   (columns: ts, draft_id, source_author, score, band, value, engage, voice,
   reach, needs_human, delivered, outcome). PRAGMA before INSERT — there is no
   referral_id column; the draft_id is the join key. Name columns explicitly
   in the INSERT. Set outcome `dropped-to-knowledge`.
3. INSERT an ARCHIVE-REFERENCE disposition into `referral_dispositions` with
   rationale carrying fs + batteries + what knowledge was kept, organ_route
   `writing.comment`, decided_by `fs-gate-law`.
4. Unpark the draft in `writing-studio/drafts.db`: load the metadata JSON,
   remove `parked_at_delivery`, set `needs_human: false`, write back. A parked
   dropped draft holds the producer brake and silently blocks later pipeline
   runs.
5. File a KNOWLEDGE card on the comments board (`boards/boards.db → items`,
   board_id `b-comments`, seq = MAX(seq)+1 within that board, kind `card`,
   channel `knowledge`): numbered WHAT WE LEARNED points — the
   mapping/insight worth keeping, NEVER the failed comment text — plus source
   URL, draft id, attempt count, and the fs receipt. PRAGMA items first.
6. Verify with a SELECT count on the new title + curl the board route (200),
   then report receipts: fs, batteries, panel verdict, card seq. Zero items
   parked at the principal seam is the pass condition.

## Loop-stage stamp at filing (T-261015-0061, Buehler science-loop)
EVERY card minted into `b-comments` (digest lane, drop-to-knowledge, intake
holds) carries a `loop_stage` value in the INSERT: one of `knowledge /
hypothesis / simulation / experiment / validation / closed-loop` (engine:
`boards/card_loop_stage.py` — vocabulary, classifier, `stamp()`,
`distribution()`). Assign honestly at filing: `knowledge` = annotated
external result; `hypothesis` = the card minted a testable build gap/probe;
`simulation/experiment/validation` = WE ran it (the cited authors' runs are
never ours); `closed-loop` = a previously minted gap came back validated.
The classifier `classify_card(title, body)` gives a conservative default +
evidence string; override with judgment when the card's own MINT section
says more. `stamp()` fails closed on bad tokens and never touches
`updated_at` (backfill must not reshuffle the board). The comments surface
renders the chip per card + the trailing-100 Loop balance strip — the
sensor that shows which stage our metabolism starves.

## Science digest card lane (plain article URLs)
A bare article URL (news relay, journal page — no LinkedIn post, no comment
target) is a DIGEST lane, not a comment or build lane by default. Deliver a
SCIENCE DIGEST card on the comments board (same insert pattern as above, kind
`card`, channel `knowledge`) whose body carries three numbered blocks:
1. THE RESULT — method, measured numbers, honest caveats. Caveats live at the
   ends of articles; read the whole body, not the head. For news pages, regex
   `<p>...</p>` blocks and filter fragments under ~100 chars + nav/boilerplate
   (CSS dumps can leak into naive `<p>` extraction — filter lines containing
   `{` or `margin`).
2. WHY THIS IS OURS — the organism mechanism the finding maps to, NAMED (which
gate, law, specialist, store). Prefer domain-mechanism isomorphism over
   surface-topic matching (rest-period replay = context compaction with a
   predicted gist/detail trade-off; lipid postal-codes = unmapped co-firing
   layer under seat+engine maps). State where the analogy BREAKS — the principal's
   audience includes domain experts who check.
3. At least one minted BUILD GAP — the measurement the result makes possible
   that we have never run, stated as a testable probe, not a vibe.
The card is the terminal artifact the principal reads; a corpus row may follow but
never substitutes for it.

## Pipeline execution discipline
- Comment-pipeline runs (`POST /api/drafts/comment` on :port with mandatory
  `value_case` payload) take 4-15 minutes and run 6-17 internal attempts.
  They exceed the 600s foreground terminal cap: launch with background=true +
  notify_on_complete, then poll the result JSON at 4-5 minute intervals.
- Create the payload/runner script with write_file FIRST, launch SECOND. Never
  put a heredoc and a launch command in the same terminal call — a rejected
  shell wrapper (nohup/disown) aborts the entire command including the
  heredoc, so the file is never created and the retry dies with 'can't open
  file' after the full wait.
- Duplicate background-completion receipts for the same run (stale first
  attempt + real re-run) are informational only — check the result JSON/draft
  id against what was already dispositioned before acting; re-dispositioning
  a duplicate double-files cards.
- Draft-angle payloads: ground them in the organism's MEASURED state (real
  counters, real log columns, real commit facts) — the pipeline's fact gates
  cannot verify what the caller never supplied, and a fabricated receipt in
  the angle leaks into the comment.

## Reporting format
One message per referral batch, header per the report/delivery law: the post
(2-3 sentences), the pipeline verdict (panel + fs + batteries), the disposition
with receipts (card seq, draft id, DB rows), and what was kept — the numbered
learnings. No permission asks, no offers. Report unflattering states plainly
(fs SKIP with unanimous panel is a normal gate outcome, not an embarrassment
  to soften).
