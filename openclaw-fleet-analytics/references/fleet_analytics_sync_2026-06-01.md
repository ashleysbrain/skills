# Fleet Analytics Sync - 2026-06-01

## Sync Output
- Synced 0 cron jobs (no new/updated)
- Status distribution: Enabled 124, Erroring 44, Disabled 268
- Total cron jobs: 436
- Errors (24h): 7 total (0 rate limit, 3 timeout, 4 other)
- Top error: "120 cron jobs failing with auth errors: 73 gemini-2.5-flash, 43 nvidia/nemotron-3-super-120b-a12b:free, 4 gemini-2.5-pro"
- Model distribution (top):
  - anthropic/claude-sonnet-4-6: 60
  - anthropic/claude-opus-4-6: 18
  - google/gemini-2.5-pro: 15
  - claude-sonnet-4-6: 14
  - claude-sonnet-4-5: 10
- Journal compliance: 99.6%
- Agent knowledge stores synced: 51
- Journal entries indexed: 1,708 from 236 agent dirs
- Fleet health snapshot saved for 2026-06-01: 257 active / 257 total

## Issues Encountered
- the operator agent sessions error: no such table: sessions (session data sync skipped)
- Deprecation warnings about datetime.utcnow() (non-critical)

## Lessons / Pitfalls
- The auth error affects a significant portion of cron jobs (27.5%). Immediate credential rotation or provider key updates required.
- Ensure the operator agent sessions database exists before attempting session sync; otherwise skip gracefully.