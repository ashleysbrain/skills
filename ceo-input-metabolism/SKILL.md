---
name: ceo-input-metabolism
description: Use when the principal sends links or rulings to metabolize.
category: operations
version: 1.0.0
author: the operator agent Agent
license: MIT
metadata:
  hermes:
    tags: [ceo-intake, referrals, linkedin, task-ledger, rulings]
    related_skills: [ceo-referral-intake-route, referral-terminal-dispositions]
---

# principal Input Metabolism

## When to Use
The principal sends a research link (usually lnkd.in), a verdict/correction/ruling, an image with no caption, or a burst of several inputs at once, and expects them metabolized into the organism (corpus rows, ledger tasks, memory laws) in the first reply. Also use when a ruling must be locked into the law-block, not just harness memory.

The principal fires inputs rapid-fire from mobile: bare links, verdicts, rulings, images, sometimes several in one burst. Each is metabolized the same way: capture without guessing, check what the system already holds, dock it in the ledger, lock rulings into BOTH memory stores, and report with real numbers in the first reply. Never ask what to do with an input — the standing route decides.

## Triage (in order)
1. Read the clock. Bare research links in build windows run the BUILD lane; comment requests and comment-window links run the comment flow. Rulings (verdicts, corrections, law-language) run the Ruling lane regardless of clock.
2. Treat a burst of links as one intake batch: capture all, then mint together.
3. Images with no caption: work from the delivered description; if a vision probe is needed, one attempt only — if the backend is text-only, proceed from the description and say so. Never invent caption intent.

## LinkedIn capture (the standard research-referral source)
- Resolve `lnkd.in/p/<id>` with `curl -sIL` and read the `location:` header; fetch the final URL with a desktop-browser User-Agent; parse og:title + og:description from the HTML. og:description carries the full post text for normal posts — key numbers, embedded paper links, author credits.
- web_extract/Firecrawl 403s on linkedin.com — do not burn turns on it.
- LinkedIn GROUP posts (resolve target contains `groupPost`) serve NO og metadata to anonymous fetches — capture needs an authenticated browser session or the principal's paste. Mint a re-capture task, log the surface as an afferent gap, and never fill the gap with guessed content.
- When og text truncates mid-sentence, record the truncation point as a gap in the task detail rather than paraphrasing the missing part.
- Auth-walled posts (og:title/og:description = "Sign Up | LinkedIn") and unindexed posts (search returns zero) are WALLS, not captures: mint a re-capture task with the slug fragment you hold, and add a row to the canonical walled-links list (`organism/muse/seats/meta/WALLED-LINKS.md`) IN THE SAME TURN as the mint — ref, ledger row, target post ID, wall type, what is held, unlock path, status. Rows close only on captured evidence. Keep the failed-routes log in that file current so no dead route is retried without new capability. Track the wall rate (walled/total principal LinkedIn referrals) — it is the measured ingestion-loss number the principal acts on.
- A follow-up post by an already-minted author (same topic line) is an ANNOTATION on the existing row, never a duplicate mint — run the author/topic dup-check first, then `--annotate <existing-id>` with the new measured numbers and links.
- A paper link inside a captured post (lnkd.in/e...) that fails to resolve anonymously goes into the task detail as a resolve-at-build gap, not a guessed URL.

## BUILD lane (fixed order)
1. Capture the source. Record author, venue, verbatim key numbers, embedded links.
2. Dup-check the corpus BEFORE minting (`writing-studio/research_scans.db`, table scan_results: url match, keyword match on title/note, AND author match). Repeat authors have tracked threads — a continuation post gets a registered row with a cross-reference, not a new mint.
3. Prior-science scan: query the corpus for the topic keywords and write the receipt (query + hit count) into the task detail. Zero hits = genuinely new science; say so explicitly.
4. Mint: `cd /your-org/your-stack && python3 gates/task_ledger.py --submit --kind build --lane research --origin 'ceo:telegram' --by hermes --flow FLW-CONDUCTION --title ... --detail ...`
   Hard constraints that REJECT: title over 200 chars (title is a label; content goes in detail); kind=build without a GENOME block in detail; GENOME body outside the canonical systems (circulatory, connective, creative_visual, digestive, endocrine, immune, integumentary, lymphatic, memory, metabolic, muscular, nervous, network, nucleus, regulatory, reproductive, respiratory, sensory, skeletal, urinary); flow code not in stores/flow-registry.json (FLW-CONDUCTION is the safe referral default). GENOME needs: scientist=DS <Name>, physics="<principle>", 8d=<one of the 8 canonical dimensions>, metrics="<what it emits>".
5. Register the corpus row: INSERT into scan_results with topic_id='ceo-referral-<yymmdd>'. The studio holds write locks for seconds at a time — BEGIN IMMEDIATE + busy_timeout + bounded retries, then read the row back.
6. Report in the FIRST reply: task IDs, one-paragraph dissection per source, new-vs-tracked verdict, ledger + corpus counts, any uncapturable source flagged. Every number from a real query.

## Ruling lane (principal verdicts and law-language)
1. Harness memory: compact principal-law entry written at ruling time (batch with stale-entry removal if near the char budget).
2. Ledger docket: task_ledger.py --submit, kind methodology, origin 'ceo:telegram', carrying the ruling verbatim + the enforcement point + a GENOME block.
3. Law-block amendment is sibling-agent surgery in ONE change: PROCESS-FLOWS.md source section (format precedent: any existing `## <NAME> LAW` section) + SEGMENTS heading in gates/law_block_gate.py + fixture extension + `--reanchor --actor sibling-agent` + carrier sweep. Writing directly into stores/law-block.md is the prohibited path. A ruling in harness memory alone is incomplete — always dispatch the law-block change.
4. Dispatch via operator bus handoff to sibling-agent; require the completion handoff to carry the new law count and pin sha.
5. Verify after surgery: law_block_gate.py --verify exit 0, --sweep --check exit 0, recount `grep -c '^## ' stores/law-block.md` before citing totals.

## Standing laws that govern this intake
- BUILD first, COMMENT second (referral routing).
- SCIENCE-FIRST: all builds/updates scan prior accumulated, strategically categorized science before building; state the receipt.
- AFFERENT-PARITY: Telegram is one interface; instructions and learning come from every direction — flag any surface the system cannot sense.
- Duplication is waste: dup-check before every mint; continuation threads get cross-references, not new tasks.

## Pitfalls
- A mint rejection is a constraint message, not a failure: read which constraint fired (title length, GENOME shape, flow code) and re-mint corrected. Do not re-mint blindly.
- Do not guess paper links the og capture did not include — record their absence as a task gap.
- Corpus INSERT can hit 'database is locked' under studio writers: retry with BEGIN IMMEDIATE, never INSERT without a transaction, and verify the row landed before reporting counts.
- scan_results columns differ from the INSERT template's assumptions: the table is (id, topic_id, run_at, title, url, source, year, cited_by, note, last_seen_at, seen_count) — supply values positionally or by name, count the placeholders against the column list (PRAGMA table_info) before running; a mismatched binding count is a schema drift signal, not a retry signal.
- Mint batches backgrounded mid-burst (user steers while a batch runs) still land: verify by readback of the task-id range before re-minting anything — an interrupted turn's mints are usually present.
- Report clock discipline: one consolidated report per burst, header per report law; never re-narrate process as delivery.