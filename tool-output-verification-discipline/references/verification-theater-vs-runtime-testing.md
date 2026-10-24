# Verification Theater vs Runtime Testing

## The 2026-08-08 Writing Studio Failure

### What happened

Built a 33-check audit script for the Writing Studio. Reported "33/33 checks pass."
The user opened the app and found AI telltales still in the output.

### What the audit checked (code existence)
- `checkAIStyle` function exists in HTML → PASS
- `loadCalendar` function exists in HTML → PASS
- 11 API endpoints return HTTP 200 → PASS
- `div` balance: 812/812 → PASS
- 28 banned phrases present in detector source → PASS
- Pipeline has `_get_draft_text()` → PASS

### What the audit NEVER checked (runtime behavior)
- Pull actual draft content from DB → run through detector → does it catch the 14 em-dashes? (Would have FAILED)
- Open calendar in browser → does the grid render with real data? (Untested)
- Run a pipeline → does the output pass the AI tell gate? (FAILED: 8 em-dashes + "robust")
- Load a draft in the editor → does the research panel suggest relevant items? (Untested)

### The corrected approach

Every audit must have TWO tiers:

**Tier 1: Code existence (setup, not verification)**
- Function exists in source
- API endpoint returns 200
- Div balance is 0
- Python syntax valid

**Tier 2: Runtime behavior (actual verification)**
- Pull real draft from DB → scan for AI telltales → report findings
- Run pipeline → check output word count and telltale count
- Load page in browser → verify visual rendering
- Call endpoint → inspect actual response body content

If your audit is all Tier 1 with zero Tier 2, you are doing verification theater.

### The detection signal

If someone reading your audit results cannot tell you what the ACTUAL OUTPUT
contains (word counts, telltale counts, rendered content), only that the CODE
EXISTS, then your audit failed. The user does not care that `checkAIStyle()`
exists. They care that their draft doesn't have em-dashes.
