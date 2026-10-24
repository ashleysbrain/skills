# Comments kit delivery (drafts → cards → paste-ready)

When the principal asks for "next comments and links" or cannot reach the interface, assemble the kit from the stores and deliver it in chat AND on the board.

## Sources

- Candidates + state: `writing-studio/linkedin_metabolism.db` → `gg_comment_candidates` (columns: id, referral_id, title, paper_url, author_post_url, author_name, note, state, queued_at, drafted_draft_id; states: pending/drafted/delivered).
- Draft bodies: `writing-studio/drafts.db` → `drafts` (id, title, stage, content). High-stakes drafts sit at stage `review`; the newest per author wins (order by updated_at DESC).
- Board cards: `boards/boards.db` → `items` (board_id='b-comments', kind='comment').

## Card mint (schema-verified)

```sql
INSERT INTO items(id, board_id, seq, title, url, status, body, reasoning, updated_at, kind)
VALUES(?,?,?,?,?,?,?,?,?,?);
```
- seq = MAX(seq)+1 for board_id='b-comments'.
- status 'ready' + body → renders with Tap-to-copy on the Ready tab.
- status 'new' (intake, no draft yet) → visible only via the all-action query, NOT the default Ready view.
- Knowledge/science-digest cards (no public comment intended) also live on b-comments with channel='knowledge', kind='card', status='ready' — same seq discipline. The knowledge card is the principal-visible receipt when a referral disposition is drop-to-knowledge or BUILD-only: body carries THE RESULT (the finding's numbers verbatim), the numbered organism mapping, and the comment-lane verdict. A drop with no card deletes the learning. Set receipt='ceo-referral-<HHMM>' so the later backlog audit (which referrals produced cards) is a single SELECT.

## Kit format in chat

Numbered entries: author + one-line why, then the post URL, then the full body verbatim (with the operator agent signature block). No process narration. Deliver the interface link once at top as the durable home.

## Sync rule

- If a newer studio draft exists for a card already on the board (older/shorter body), UPDATE the card body to the newest draft — stale bodies on the board are a silent quality regression.

## Backlog audit (past science, asked or scheduled)

When the principal asks what past science is unactioned, ground the answer in joins, never chat memory: b-comments knowledge cards ↔ task-ledger tasks on mechanism keywords. Stale open research-digest tasks close in three lawful ways — VOID (auto-scan tunnel duplicates that never extracted a mechanism; record the noise cause), CONSUMED (mechanism already covered by open builds; write the wiring spec citing every converging source and attach, mint nothing), or MERGE into an existing mechanism task. After closing, re-count from the DB and report the remaining unactioned count from the query itself — the number is the deliverable. When the drain minted new builds, the report carries them by task id; when the drain closed 11 stale items, say so with the disposition split.

## Canonical text + alignment audit (before any paste batch)

- **Print paste text from the store, never retype it.** The canonical body is the boards.db `items.body`; deliver by SELECTing it and printing byte-identical. Retyping from panel-output memory silently mutates tokens (a split word, a changed digit) and the principal pastes the mutant — she reports it as "didn't go through correctly". When she does: diff the delivered message against the stored body, check the card status (non-ready statuses hide from the Ready view), confirm the studio draft intact, then re-deliver the stored body verbatim.
- **Audit each card against its OWN source HTML.** Programmatic, not memory: for each card, locate the source fetched for the card's `url` value and check that the poster's name, every co-author named in the comment, and the topic phrases appear in THAT source. Never audit against the most recently fetched /tmp html — multi-referral sessions leave several cached files that look interchangeable, and card.url is the only source of truth (auditing the wrong file raises a false alarm on a correct card). og:title can be hashtags-only, so grep name fragments (`>Rahul Y.<`, `Name's Post` patterns) rather than trusting og: meta alone.
