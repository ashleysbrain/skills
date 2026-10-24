# LinkedIn Newsletter + Viral Post Program (session 2026-08-16)

Post-audit edition. Everything here was live-verified or principal-corrected this session. Companion workspace docs: THREAD-4-LINKEDIN-NEWSLETTER-PLAN.md, THREAD-4-VIRAL-POST-SYSTEM.md, THREAD-4-POSTING-INTELLIGENCE-SPEC.md, THREAD-4-CONTENT-MACHINE-SCAN.md.

## Locked architecture

- Company page: newsletter home. Personal page: standalone viral post engine (2-3/week, 1-2 viral candidates + 1 connective tissue, 48h rule between candidates).
- Synergy: last-line handoffs (3 variants), first-comment open question, company reposts personal only on real lab milestones, never Field Breakers.
- Superseded: the earlier two-newsletter alternating-weeks design (personal newsletter one-pager kept for reference only; its segments/voice rules still govern personal posts).

## Platform facts (live-fetched from LinkedIn Help Center 2026-08-16)

| Fact | Article |
|---|---|
| Personal profiles: ALL members get newsletter access, no threshold | a522525, a591266 |
| Company Pages: 150+ followers + original-content history + good standing, evaluated by LinkedIn | a591266 |
| Up to 5 newsletters per profile/Page; 2-week cooldown after create/delete | a517925 |
| First edition auto-invites connections/followers to subscribe | a517925, a596833 |
| Every edition: push + in-app + email to subscribers + feed surface | a522525 |
| Logo 300x300; per-article cover 1920x1080; custom SEO title/description | a517940 |
| Cadence shown on badge (public commitment); analytics: views, new subs, impressions, demographics | a517940, a1658525 |
| Subscribe = auto-follow author; newsletter page public without login | a522525 |

Launch implication: personal page can launch today; company Page may need follower growth first. Verify Page eligibility in the admin UI, never assume.

## Topic draft metadata schema (the adjustable batch contract)

```json
{
  "batch_id": "li-batch-YYYY-MM-DD",
  "batch_name": "...",
  "dedup_key": "sha1(title)[:12]",
  "launch_mode": "solo",
  "remains_linked_to_batch": true,
  "surface": "company|personal",
  "content_type": "linkedin_newsletter|viral_post",
  "pillar": "P1..P4",
  "evidence_grade": "A|B|C",
  "source_asset": "what real thing backs this",
  "trajectory_role": {"role": "...", "phase": "early|launch|mid|parked", "rationale": "..."},
  "audit_YYYY_MM_DD": "downgrade note + graduation condition when applicable"
}
```

Write to drafts via POST /api/drafts (stage=ideation). Read via GET /api/drafts?limit=200. Token: GET /api/auth/local-token.

## Fabrication screening (the known-false list for DS content)

Never let these into any doc, brief, table, or sequence, even marked [NEEDS DATA]:
- 48-hour sleep/finance lag (from advisor-drafted NEWSLETTER-001/002 marketing copy; no data exists: daily_scorecard has 27 sparse rows, mostly NULL, July frozen placeholders)
- Environment dimension most predictive (same source, same status)
- Critical slowing down as a built detector (zero engine code refs; benchmark design vocabulary only)
- Pipeline runs displaying claim grades (runs carry evidence_level vocabulary, not A/B/C grades)
- Academic bench recruited (willing inquiries only, nothing signed)

Screen delegate outputs against this list mechanically: regex the exact phrases, check whether each hit sits inside an audit/downgrade context or is asserted as fact.

## Evidence grades after audit (2026-08-16)

- A: phantom-citation gate (code L292, 9 quality-issues runs), 1-of-7 OS assessment (real file, verdict MEETS 1/7), 8D engine (701 lines), founding essay (approved)
- B: claim-grading post (practice real; runs-display false), vital-signs chart (spec), 65% forecast (ours), skippable-work gate (built not benchmarked)
- C (parked with graduation conditions): sleep/spending story (8+ weeks continuous tracking), organism-week-breaks (same + detector), ADHD post (principal material only), what-would-change-my-mind (series installment 1)

## Session techniques

- Delegate timeout salvage: a 900s timeout killed the closing message but the child had already write_file'd the full 10.5KB spec to disk seconds earlier. On timeout, grep the live transcript for write_file calls and read the artifact before re-dispatching.
- Zero-tool re-dispatch guardrails: when the environment is degraded (terminal returns empty, web unconfigured), re-dispatch with "Do NOT call terminal/web_search/web_extract. Answer from domain knowledge in ONE pass." at the TOP of the brief. Reduced a 900s timeout to a 6-minute clean completion.
- False-empty read_file: read_file returned 0 bytes for files that existed with content (subagent summaries, plan doc). execute_code with open().read() read them fine. When read_file says empty, verify with execute_code before believing it.
- Chinese leakage in delegate output: one spec shipped two Chinese sentences in an English-only context (user has corrected Chinese TWICE before). Grep delegate outputs for CJK ranges before delivering.
- Adversarial pre-read caught: fabricated claims re-asserted in a draft brief after metadata-only downgrade (metadata patch is not enough; the CONTENT body must be rewritten), missing graduation conditions on 2 of 4 C-grade briefs.