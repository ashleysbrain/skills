# the operator agent public-comment lane (LinkedIn, paste-ready delivery)

Depth for referral-intake sessions that end in a public the operator agent comment the principal
posts manually. Read when a COMMENT-CLASS referral passes the value filter.

## Why this lane exists
No OAuth posting lane is live; every public comment is delivered as
paste-ready text in the principal's chat plus a board card with a Tap-to-copy
button. The principal's manual post is the canonical artifact — what she posted is
the voice precedent, including the signature block.

## Delivery surface checklist
1. Draft lives in `writing-studio/drafts.db` (drafts table, stage review,
   pipeline gg-comment, author the operator agent).
2. A board card must exist on the comments board (`boards.db → items`,
   board_id b-comments, kind comment) carrying the FULL body in its body
   column — drafts without cards are invisible to the principal interface, and the
   recurring complaint "I can't see my comments" is this gap, not a UI bug.
   PRAGMA the items table before INSERT (board_id, not board; no actor_class
   column) — one schema read prevents the silent failed insert.
3. Card status ready + a copy affordance renders only for ready cards with
   non-empty body; body-less ready cards show no copy button.
4. After the principal posts, flip the card to posted and log the receipt in the
   metabolism store (gg_comment_candidates state → delivered).

## The QA gates (in order, before paste-ready text reaches the principal)
1. **Telltale scan** via `scan_ai_tells.py` with the `— the operator agent` signature line
   stripped (canonical signature; see the SKILL.md pitfall). Body must scan
   0 telltales.
2. **First-person provenance audit**: every we/our/"at Divinity Science"
   sentence checked against the task ledger and stores for corresponding
   done work. No rows = rewrite to personal-learning framing.
3. **Attribution audit** for historical claims (already in SKILL.md): mirror
   the post's own phrasing where facts are shaky.
4. **Architecture encryption**: no biological isomorphism fingerprints;
   technology analogs only.
5. Log the review in `linkedin_metabolism.db → qa_tracking` (create the table
   with the canonical schema if missing) with revision_number.

## Card hygiene
- Sync the board card body when a newer panel draft supersedes it (highest
  updated_at wins); stale card bodies deliver outdated text to Tap-to-copy.
- Comments-off posts never get drafts: verify the affordance before drafting,
  file HOLD with the reason, absorb as design input if the content maps to a
  build lane.
- Same-author multiple posts: value-filter each independently; a comments-off
  post does not block a comments-open sibling post's comment.

## Reading-card renders
When the principal asks to read the referred post/article itself, render it as a
static dark-theme HTML card under `boards/renders/<slug>.html` (served via the
boards app /renders/ route) instead of pasting raw text into chat — one link,
  phone-readable, quote-pull styling for the load-bearing lines. The render is
  for reading only; the comment draft is a separate artifact.
