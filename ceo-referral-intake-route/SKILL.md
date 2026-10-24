---
name: ceo-referral-intake-route
description: Use when principal sends any link or post to process. Gated route.
---

# principal Referral Intake Route

## Law
principal sends -> routed, gated, delivered. Artifact lands in the FIRST reply, in-channel (chat text, paste-ready), never only as a file or process narration. Verify the ACTUAL question in the source (read the post's own closing questions, not just its abstract) BEFORE writing.

## Route (fixed order)
1. **Fetch + verify source** (web_extract/browser). Extract the author's literal questions and claims. Dup-check the research corpus (writing-studio/research_scans.db, scan_topics/scan_results).
2. **Draft answer** answering the author's literal questions in their order. Plain register per audience. No internal jargon (no 'AI organism', 'routing claim', 'receipts' outside the org).
3. **Gate: ai-tell-removal-gate** — scan_ai_tells.py on the text BEFORE delivery. PASS required (0 telltales).
4. **Gate: adversarial review** — specialist_gate.py --route --specialist "the specialist engine" -> delegate_task one reviewer seat with the draft verbatim + the source's literal questions. Apply ALL fixes (CRITICAL/MAJOR always; MINOR unless principal said otherwise).
5. **Register**: writing-studio draft (PUT /api/drafts/<id>, token from <agent-home>/.env WRITING_STUDIO_TOKEN), dialectic record (POST /api/drafts/<id>/dialectic with objection_text carrying the review verdict — 422 on empty is CORRECT behavior since 2026-09-20 patch).
6. **Deliver to the comments process flow, not chat** (principal 09-28: "I don't know why you're giving me comments in here in text when this is in our process flow"). Full text goes to the social/comments queue row (claim FIFO) with the short ~1,200-char LinkedIn version attached; chat gets only a one-line "queued for your review" pointer, never the full comment body. File to deliverables-MMDD/ as backup.
7. **File corpus entry**: dup-check then insert (scan_topics + scan_results rows).

## Engine health (KeepAlive since 2026-09-20)
com.ds.wernicke:port, com.ds.tawara:port, com.ds.popper:port, com.ds.studio-api:port all launchd KeepAlive. If a Veritas run pauses on 'engine health gate failed': curl each port; a down engine relaunches itself within 10s (ThrottleInterval) — wait, don't hand-start (hand-started instances block the managed one with Errno 48).

## Known-fixed defects (do not re-trip)
- Resume 400 'No checkpoint state found': fixed 2026-09-20 (state_path hoist + fallback).
- Resume TypeError 'missing idea': fixed (VeritasPipeline(state.idea)).
- Empty dialectic records: fixed (422 on empty; position/content map to objection_text).
- Run record must be 'paused'/'awaiting_human_review' to resume; a 'failed' record needs a fresh run.

## Quality bar
First-time quality = correct gates run BEFORE delivery. If a gate is skipped the text is UNGATED — principal counts it as made-up output. Nothing ships without: source-question verification, tell-scan PASS, adversarial seat verdict + applied fixes.