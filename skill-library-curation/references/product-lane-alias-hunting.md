# Product-Lane Alias Hunting

## Lesson
When a user corrects a named engine, repo, or lane, do not assume the exact label exists in the workspace.

Search in this order:
1. exact acronym / proper name variants
2. neighboring product-family names and aliases
3. cron/job names that may reference the operational lane
4. closest canonical working spec if no dedicated artifact exists

## Durable rule
If the exact named artifact is missing, treat the closest matching spec as the working source of truth *only after* verifying the alias trail. This avoids getting stuck on a label that was never the canonical repository name.

## Good signals
- The user says "that's the wrong engine"
- The user gives a remembered name that may be a nickname, codename, or mispronunciation
- The repo contains multiple adjacent product families with similar wording
- Cron jobs or docs reference a different canonical label than the user's spoken label

## Verification
Before concluding the target is missing, confirm:
- the exact-name search returned empty or only irrelevant hits
- at least one adjacent alias family was checked
- the fallback spec or repo is the closest operational match
- the final response names both the user's label and the canonical artifact name so the mismatch is explicit
