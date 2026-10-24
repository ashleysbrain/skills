# Release Review Lane — V1 Skill Product Surface

Use this reference when the 8D report workflow is being used to evaluate the *skill product* itself rather than a personal health snapshot.

## Scope
Review only the Divinity Health V1 skill product surface and its immediate release ecosystem:
- `SKILL.md`
- linked `references/` files that define output, baseline, formatting, and future-proofing
- immediate support files or runtime artifacts that shape the visible release behavior

Do not widen the review into unrelated health-scoring, diagnosis, or personal wellness interpretation.

## What to look for
- whether the current skill anchor is coherent with the latest stable release
- whether a candidate change is a true product improvement or just a one-off session artifact
- whether the release behavior matches the documented output contract
- whether the skill needs a support layer, template, or reference instead of a new narrow skill
- whether the current anchor should be preserved and updated incrementally rather than rewritten from scratch

## Recommended review outputs
A good product review should end with:
- the best next skill update
- any support file that should be added or refreshed
- any release candidate that is ready to promote
- any overlap or consolidation note if two skills are carrying the same load

## Retrieval rule for “show me the report” requests
If the user asks to *show* the latest report or update, retrieve the newest verified artifact first.
Do not answer from cron metadata, schedule status, or session summaries alone.

Verify by reading the actual rendered artifact or source text before presenting it.

## Class-level guidance
This lane should be used as a class-level release-review overlay, not as a one-session note.
If the same pattern repeats, add or update the umbrella skill and its references rather than creating a narrow ephemeral skill.