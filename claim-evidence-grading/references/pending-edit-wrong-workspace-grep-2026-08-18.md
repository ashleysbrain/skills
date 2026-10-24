# PENDING SKILL.md EDIT — wrong-workspace grep (2026-08-18)

Curator: extend Pitfalls (or verification op #1) in SKILL.md with the
one-liner below. Direct patch blocked by _read_before_write guard in
background session (known quirk; dedup view doesn't count).

## Suggested pitfall line

- **Right pattern, wrong workspace (2026-08-18).** A recursive grep of
  the correct term inside the repo you happen to be working in still
  returns ZERO when the claimed artifact lives in a sibling workspace
  (your-stack audit records name writing-studio code that actually
  lives in ~/your-workspace/). "No grep hits" grades to GRADE C only
  after searching every workspace the claim could live in, not just the
  current repo. Run-records are pointers, not locations.

## Context

principal asked "what happened to brainstorming??? mosaic os". Run-record
(audit/RUN-RECORD.md pass 12) claimed WORKBENCH BUILT + 8 routes + E2E
10/10 green — all TRUE, but grep of your-stack repo returned zero
because pipeline_api.py lives in ~/your-workspace/. Five turns burned;
recipe captured in your-stack-operations skill,
references/feature-disappearance-investigation-2026-08-18.md.
