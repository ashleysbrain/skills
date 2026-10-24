---
name: research-referral-ingestion
description: Use when principal sends links, screenshots, papers, or science for the corpus or for system-building. Ingest AND act.
version: 1.1.0
author: hermes
provenance: agent
tags: [research-corpus, ocr, dedupe, ingestion]
---

# Research referral ingestion

Class of task: the principal sends a URL, a DOI, or phone screenshots of posts/articles
to be added to the research corpus ("add this to research", "research non duplicate
items", bare image batches with no text). The job: read the source, verify it is
NOT a duplicate, insert with provenance, and offer the follow-on digest.

## Procedure
1. **Read the source.** For URLs, extract in chunks (long essays run ~35k chars;
  read all of it — the key numbers and honest-caveat language live at the ends).
  For images run `tesseract <img> stdout 2>/dev/null | grep -v '^\s*$'`; batch
  multi-image runs in one loop, ~18 lines head per image, then read the remainder
  of anything ambiguous rather than deciding on the head alone.
  For LinkedIn short links (`lnkd.in/...`) the extraction API 500s — cheapest
  first: (0) `curl -sL -A 'facebookexternalhit/1.1' <short>` — the crawler UA
  follows to the full `linkedin.com/posts/...` URL and renders complete
  og:title/og:description in one call; a plain/desktop UA on the same shortlink
  can 404 or bounce to the signup wall, so switch UA before concluding the post
  is unreachable. (a) `curl -sI <short> | grep -i '^location'`
  gives the canonical post URL, then `curl -sL -A '<desktop UA>' <full-url>` and
  pull `og:description`; (b) when og:description is truncated or the post is a
  reshare (content lives in the original author's layer og-tags cannot reach),
  fetch the reader proxy: `curl -s -m 30 "https://r.jina.ai/<full-url>"` and
  cut the body between `Report this post` and `Like` — this recovers BOTH the
  reshare text and the embedded original post including paper numbers; (c) a
  real browser tab returns post text PLUS the comment thread — use the browser
  only when comments matter (mining discourse, checking who said what), because
  LinkedIn pages stall the automation CDP (Runtime.evaluate timeout) and each
  stall costs a daemon reset. Default to (a)+(b): curl paths never wedge.
  Reader-proxy output carries markdown link residue (`site.com]`, stray
  brackets) — strip `[...](url)` patterns before quoting post text anywhere.
  When the FULL post URL itself 404s for the recipient, deliver the canonical
  `linkedin.com/posts/...` URL resolved from the shortlink, not the lnkd.in
  redirect.
  **Login-wall ladder:** when the redirect lands on
  `linkedin.com/signup/cold-join?session_redirect=...`, the real post URN
  (`urn:li:ugcPost:NNN`) is embedded in that redirect URL — build the direct
  `/feed/update/urn:li:ugcPost:NNN/` URL and retry it with the crawler UA; if
  still walled, file a HOLD row carrying the shortlink + URN and ask the principal
  for the author name or a reshare — never drop the referral silently and
  never file it with guessed content.
  **Primary-source resolution for linkless paper claims:** when a post cites a
  paper without linking it, resolve it via
  `api.crossref.org/works?query.bibliographic=<distinctive title words>&rows=3`
  (returns DOI, journal, publication date — verify journal and year match the
  post's claim), then pull the abstract from the publisher page (`dc.description`
  meta). A post's summary of its own paper is a claim, not a source; grade the
  evidence from the paper.
  Before inserting, verify resolvable artifacts resolve live: a DOI should
  answer a HEAD request at the publisher (`curl -sIL` → 200) — a mis-OCR'd
  identifier must never enter the corpus as real.
2. **Dedupe BEFORE insert.** Search the corpus by DOI, exact title, distinctive
title fragment, author surname, topic slug, AND the raw source URL/shortlink
itself — the principal's link bursts re-send the same shortlink within minutes, and
the correct response to a re-send is reporting the already-filed disposition,
not a second row. Any hit means verify the match
is the SAME work, not a fragment coincidence.
3. **Insert with provenance**: one row per distinct work, in the research corpus's
topic + results tables — source URL/DOI, author, why it is relevant to our
physics (which gate/law it overlaps), scan cadence (~30 days for active topics).
Readback the row id after insert; report the corpus count before → after.
4. **Classify honestly.** Research claims get active topics. Pure visuals (math
art, design references, shares already actioned elsewhere) get recorded in a
reference topic for provenance — never mint research topics for non-claims, and
mark conjectural claims (unpublished derivations, unverified numbers) as
conjectural in the entry rather than parroting the referring post's framing.
5. **Offer the triangle digest** for the strongest 1-2 items; do not auto-run it
unless ordered.
6. **Act on the science — never stop at filing.** The referral feed exists to
drive system change: an AI that reads and does nothing is a filing cabinet.
When the principal frames the item as input for the organism ("for our self-healing
system", "dive into this extensively", any systems-evolution framing), run the
science-deep-dive lane after ingestion: (a) research seat on primary sources
with graded evidence, (b) mapping seat converting findings into organism
mechanisms labeled BUILT-RUNNING vs DESIGNED with free-energy ranking, then
(c) IMMEDIATELY dispatch the top-ranked mechanisms as build requests — never
offer them ("ready when you want them" is the primary laziness violation and
burns principal trust). For the dispatch mechanics and gates, see
references/dispatching-builds.md. Periodically audit that past referrals
actually got acted on — the census recipe is references/backlog-census.md.
If the item only clears a comment/answer
lane, the delivered text is the terminal artifact: run the full the operator agent
public-comment lane (gates, board card, paste-ready delivery) per
references/the operator agent-public-comment-lane.md.
  When the principal sends a call-for-papers/collection/showcase link as a writing
mission ("we are going to write for this"), it is a WRITING-MISSION referral,
not corpus material: route it per references/cfp-writing-studio-route.md
(pull the full call, seed a studio draft, launch a Veritas run, gate, principal
sign-off — never auto-submit). A bare post link with no writing framing is
NOT a writing mission: classify it explicitly as COMMENT-CLASS (respond to
  the author) or FILE-CLASS (corpus entry + disposition) in the reply, and for
  physics content state where the analogy or claim breaks — the principal's audience
  includes domain experts who check, and the honest-break note is what makes
  the corpus entry reusable in public writing later.
  COMMENT-CLASS must pass a value filter before any comment is generated: (a)
  does the organism already carry this content natively (foundational
  material, own operating laws, tech already dissected from primary sources)?
  (b) is the author a genuine SOURCE (originator, practitioner with measured
  data) or a learner summarizing others' work? Either answer failing the item
  means FILE-CLASS: register the row, note the filter verdict, deliver a
  one-line disposition — no comment. Not every referral earns a public
  comment; a comment on material the organism already knows outperforms
  silence in cost but underperforms it in credibility.
7. **Verify inserted counts read-back** and report raw numbers (corpus before →
after, rows promoted) — never parrot a seat's self-reported counts without a
SELECT. When the store backs a live rendered surface (board/page/API), also
grep the RENDERED output for the new title after insert — a committed row is
invisible to the UI when the insert targets the wrong partition (board_id or
similar per-board filter), and row-count SELECTs alone will not reveal it.
Pre-existing duplicate seq numbers in a board may be intentional (raw referral
rows and derived comment rows sharing a seq) — inspect the row kinds before
deleting anything that looks like a duplicate.

## Pitfalls
- **Filing without digesting is waste.** Inserting a corpus row is not learning: the loop closes only when every entry gets a disposition (PROMOTE with a substantive distilled note + evidence link, DISCARD with reason, or DEFER to an existing open lane) via the triage pass (organism/research_triage.py; standing metrics in writing-studio/metabolism_report.py — corpus size, % triaged/promoted/discarded, scanner health). Never report corpus growth as metabolism: measured state was 2,170 entries with 1.5% ever read — accumulation tokens, not learning.
- **Scanner liveness is diagnosed from scan_runs, not newest rows.** The scanner mostly re-sees existing rows (updates last_seen_at/seen_count), so a weeks-old newest scan_results row does NOT mean the scanner died — check the scan_runs table (last run_at, status, rows touched, error count) before claiming scanner death. Claiming a live daemon dead burns principal trust as fast as claiming a dead one live.
- **Generic title fragments make false-positive skips.** A duplicate check on a
single common word ("Physics") matches unrelated rows and silently skips a real
insert — list the matched rows before trusting any skip, and re-insert with a
correcting note when the match was coincidental.
- **First INSERT into a topic table can exit 1** (id sequence not auto-assigned) —
retry with an explicit id one past the current max.
- **Screenshots arrive in pairs** (post + companion screenshot); dedupe the batch
  itself before counting — N images is usually fewer than N works.
- **Rearchitecting an entry is an UPDATE, not a new topic.** When the principal
  reframes an item after filing (a visual reference becomes an architecture
  directive), rewrite the existing topic row and note in place — never insert a
  second topic for the same underlying referral; the topic table is the record
  of the referral, and duplicates there are invisible to the dup-check.
- **Geometry/topology counts as physics** for classification — a geometry
  directive maps to gates, lattices, and state spaces, so route it to the
  physics/architecture lane, not "visual reference", once the principal says it is
  about handling data or decisions.
- **Historical-reference recovery from conversation state.** When the principal names something from a past conversation ("the site you said was closest to us"), query the session store directly: `<agent-home>/state.db`, table `messages`, text column `content` (NOT `message` — a LIKE on the wrong column silently returns empty and looks like "not found"), filter `role IN ('user','assistant')`. Try session_search for discovery first; fall back to direct FTS/LIKE with several distinct phrasings. If several well-formed searches fail, STOP and ask the principal to re-drop the reference — inventing a plausible source to fill the gap is a fabrication, and an honest miss costs one message.
- **Public comments on referred posts carry attribution traps.** Before a
  comment ships, adversarially verify every historical/personal claim the post
  itself made (dates, affiliations, which work an anecdote belongs to) — the
  post can be wrong and mirroring its error in our voice is worse than the
  error staying in theirs. Where the fact is shaky, mirror the post's own
  phrasing verbatim instead of asserting more than the source did.
- **A reshare is not the original.** When the referred post amplifies someone
  else's content, credit and link BOTH layers in the filing (resharer +
  original author/paper) — the corpus note and any comment must attribute the
  work to the people who did it, not the account that amplified it.
- **Corpus and bus schemas must be PRAGMA-read before the first INSERT, every
  script.** The scan_results table uses string ids with a fixed column set
  (id/topic_id/run_at/title/url/source/year/cited_by/note/last_seen_at/seen_count
  — no `authors`, no `abstract`, no `created_at`), and the operator bus
  messages table uses timestamp/from_op/to_op/msg_type/subject/content/status.
  Guessing column names fails the insert SILENTLY-or-loudly after the fetch
  work is already done; one `PRAGMA table_info(<table>)` line at the top of
  every filer script makes first-try landings the norm.
- **Amending a ledger/bus row is APPEND, never overwrite.** An UPDATE that
  replaces a detail/content column destroys prior context (recoverable only
  from session history); concatenate the new text onto the existing value and
  write the event row in the same transaction, verifying with a length
  before/after — length shrinking means you clobbered.
- **Two consecutive same-shape arrivals = a pattern thread; three = graduate
  it.** When multiple same-day referrals share a mechanism (e.g. fragmented
  search spaces solved by decentralized curation; aggregate signal over
  discrete events), file one cross-linked re-read thread instead of N isolated
  insights — note the converging arrivals in each corpus entry so the thread
  survives context loss, and say the convergence count in the reply. Independent
  arrival is the strongest signal the mechanism is real.
- **Opencode dispatch: run `sibling-agent run` in BACKGROUND with notify, never
  foreground.** A foreground `sibling-agent run` call can burn the entire 420s
  terminal timeout and die silently; background + notify_on_complete keeps the
  dispatch observable. If a dispatch dies at launch (`Session not found`),
  redispatch once with the full order inline (bus id + read command + spec
  summary) rather than concluding the sibling refused.
- **Report honest lane state on comment-capable referrals.** When the comment
  pipeline is closed (no generation route live), say so once in the reply and
  stop repeating it every referral — the principal knows the state; repeating the
  closure reads as process narration instead of metabolism. When the pipeline
  is OPEN, stop saying "pipeline closed" and start delivering.
- **A first live run of any newly shipped engine is an acceptance test, not a
  delivery.** When a sibling ships a new route, run a real payload through it
  and report the raw result (gates passed/refused, artifact ids) — but a
  gated-PASS output still gets the full verification battery (claim-check,
  tell-scan, banned list) before the principal sees it, and the first clean output
  belongs to whichever article the principal actually named, never to the test
  payload's article.
- **When multiple un-commented referrals are live, confirm the target article
  before generating — and prefer buttons over free-text asks.** A clarify call
  with the candidate articles as choices outperforms a prose question; if it
  times out, do NOT pick the most likely one and generate (wrong-article
  comments are pure rework and each wrong guess erodes trust). Say you're
  holding until the principal names it, and metabolize the rest of the referral
  stream meanwhile.
- **If the principal rejects a delivered comment as untrue, withdraw it explicitly
  and file the defect the same turn.** Name the false claims back (which
  sentences asserted things that never happened), mark the draft withdrawn in
  the reply, and order the missing gate — do not defend, do not soften, and do
  not regenerate immediately without the fix in place, or the same fabrication
  ships again with new wording.
- **First-person organizational claims in comment text are fabrications until
  proven against the ledger.** "When we trained reward models…" in a
  what-we-learned paragraph sounds crediting but asserts work that may never
  have happened; a comment under the principal's account asserting un-done work is a
  public misstatement. Before ANY paste-ready text ships: grep the task ledger
  (done-state rows) and project stores for the claimed work's artifacts. Zero
  rows = rewrite the paragraph to credit the author's finding as the teacher
  and state what changed in OUR reasoning (personal-learning framing), never
  what we built. This check applies to every draft previously marked ready:
  "we/our" sentences added at draft time ride through untouched because the
  panel reviews argument, not provenance.
- **Verify the comment medium before drafting: authors disable comments on
  specific posts.** Check the post page for the comment affordance (og metadata
  or page HTML showing comments-off) BEFORE generating text; a comments-off
  post routes to FILE-CLASS with the content absorbed as corpus/design input,
  never a draft. When the same author has a second comments-open post, the
  audience overlap still makes the drafted comment deliverable there — surface
  that option to the principal rather than discarding the work.
- **Model-currency checks apply to the sibling too.** Before an sibling-agent
  dispatch that will run a model, check `~/.config/sibling-agent/sibling-agent.jsonc`
  default matches the provider's latest (verify from the live `/models`
  endpoint); stale pins make every build silently run an old model, and
  bumping the config does NOT affect already-running sessions — kill and
  redispatch them.
- **The em dash on the the operator agent signature line is canonical, not a tell.** When
  scanning the operator agent public comments, `— the operator agent` on its own line is the principal-approved
  signature block (precedent: comments the principal posted verbatim). Scan the body
  with the signature line stripped or normalized to `the operator agent`; counting the
  signature em dash as a telltale fails a clean comment and invites removing
  the brand mark. Every OTHER em dash in the body remains a hard fail.
