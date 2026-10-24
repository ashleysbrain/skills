---
name: skill-library-curation
description: Maintain and evolve the the operator agent skill library into class-level umbrellas with support files; convert session learnings into durable SKILL.md updates and references.
---

# Skill Library Curation

Use this skill when deciding whether a session should change the skill library, and when shaping that change.

## Core principle

Prefer *durable, class-level knowledge* over one-off session artifacts. A good skill should make the next similar session start already smarter.

## When to update the library

Update a skill when any of these appear:
- the user corrects tone, format, verbosity, or legibility
- the user corrects workflow, sequence, or decision logic
- a non-trivial workaround, fix, or debugging path emerges
- a skill in play was incomplete, misleading, or outdated
- the session reveals a reusable authoring convention or tool pattern
- the user establishes a canonical product name, product-line boundary, or aliasing rule; capture it in the governing umbrella skill and keep the distinction visible across docs and artifacts
- the user corrects the owning repo or says a repo/repo-lane is wrong; do not trust the first exact-match hit, run an alias hunt across adjacent product families, and verify the runtime wrapper, docs index, and canonical spec bundle together before treating the repo boundary as settled
- the user expresses frustration about being "stuck", a channel not working, or the assistant missing the real ask; treat that as a signal to capture the underlying workflow lesson, not just the symptom
- the user asks for repo docs to keep a branded voice distinct from a generic workflow layer; capture that as a durable umbrella-skill update and mirror the distinction in the governing docs
- the user explicitly asks to review the conversation and update the skill library, or says to "be ACTIVE"; treat that as a curation audit and save at least one reusable lesson when any durable signal exists
- the user asks to expand, re-rank, or repurpose an agent roster; inspect active *and* inactive/archived pools (including adjacent canonical rosters such as OpenClaw when the operator agent is only part of the picture), preserve existing agent lineage when the user says not to recreate agents, and revise identities/skillsets in place when possible
- when the user says the roster is larger than the visible live list, treat that as a prompt to verify the inactive/archive surface before sizing the work; do not assume the visible roster is complete
- the user asks for credential evolution or persona layering; prefer a role-by-role credential matrix over a single generic degree path, and encode the lesson in the umbrella skill that governs the roster or persona pack
- the user explicitly asks to review the conversation and update the skill library, or says to "be ACTIVE"; treat that as a curation audit and save at least one reusable lesson when any durable signal exists
- the user expects full advisor profiles in panel output; update the governing coaching-engine umbrella and its panel-format reference so recommendations do not collapse to name-only lists
- the user asks for the process "from start to finish" or says steps are missing; preserve every established step and sub-step instead of compressing the flow

If there is no durable learning, do not invent one. When a real signal appears, prefer *some* durable update over no update at all, even if the change is small.

When the user explicitly asks you to review "everything in our chat" or to make sure nothing was missed, treat that as a scope-expansion signal: audit the whole thread for additional corrections, workflow lessons, and style constraints before deciding what to save.

If the user explicitly asks to update the skill library, treat the request as a curation audit, not a status report: look for at least one durable class-level improvement when any correction, frustration signal, or reusable workaround appears, even if the change is small. Do not default to "Nothing to save." if the thread contains a usable lesson.

If the user explicitly asks for a skill-library review or says to "be ACTIVE," treat that as a mandate to make one real durable update when any reusable lesson exists. Prefer a small, correct umbrella patch over no-op output.

When the user asks for a conversation review after a confusing or "stuck" exchange, compare the latest user turn with the assistant's immediately prior reply before choosing what to save. The durable lesson is usually the workflow mismatch, not the transport symptom.

If the user reports the conversation or channel is "stuck," "not working correctly," or responding to the wrong thing, inspect the latest user message against the assistant's last turn before deciding what skill to update. The durable lesson is usually the workflow mismatch, not the transport symptom.

When a response appears to answer a different task than the latest user message, treat that as drift: compare the immediate user turn and the assistant's last turn first, then save the lesson in the governing umbrella skill and a short reference note.

When the user corrects a named engine or lane, do not trust the first exact-match search result; run an alias hunt across adjacent product families, cron jobs, and canonical specs before choosing the fallback artifact.

- For repository-owned agent packages, audit the runtime wrapper, docs index, and canonical docs as one bundle; do not assume a pass over README alone is enough.
- When the user corrects the owning repo or product-line boundary, audit the canonical repo first, roll back stray edits in the wrong repo, and normalize the README, docs index, and core spec headers together.

If the wrapper exposes advisor categories or public scoring, include the aliasing/schema and public-score docs in the startup-read verification set so the runtime and docs stay aligned.

## Preferred shape

1. **Patch an existing umbrella skill first** if it already governs the task class.
2. If no fit exists, **create a class-level umbrella skill** rather than a narrow one-off.
3. Keep the library shaped as class-level umbrellas; when a session reveals a reusable lesson, extend the governing umbrella and add a concise reference note instead of minting a one-off skill.
4. Put session-specific detail in `references/`, not in the main skill body.
5. Use `templates/` for scaffolds and `scripts/` for deterministic repeatable actions.

## What belongs in SKILL.md

Include:
- trigger conditions
- the recommended workflow
- pitfalls and failure modes
- verification steps
- notes on overlaps or adjacent skills
- pointers to any support files

Keep the body usable as an operating manual, not a diary.

## Skill rubrics (living rubric field)

Every umbrella skill carries a RUBRIC: measurable criteria that make the skill an evaluation asset, not just instructions. A well-written skill is three things at once — a reusable capability, an evaluation asset, and a behavioral contract (Skill2Env finding, T-261004-0075 seq 8: skills compiled from practitioner text carry enough structure to become tests).

A rubric has three parts, kept in the skill body or a `references/rubric-*.md` file linked from SKILL.md:
1. **MUST** — 2-5 checkable criteria for correct execution (each falsifiable by pointing at output or its absence; prefer machine-checkable forms: exit codes, counts, schema fields, rendered artifacts).
2. **MUST-NOT** — the failure modes the skill exists to prevent (each maps to a pitfall already documented).
3. **GOOD-LOOKS-LIKE** — what excellent output looks like, concrete enough that a reviewer can score it pass/fail.

Rubrics are LIVING: when a skill misfires in a session (wrong output class, missed gate, user correction), update its rubric in the same curation pass — the rubric is where "evolve by use" lands. A skill whose rubric no longer matches its body is drift; fix one or the other in the same change.

Seeding is incremental (adiabatic): populate rubrics when a skill is next touched for any reason; do not mass-edit the library just to raise rubric coverage. Track coverage as a census metric (skills-with-rubrics %), not a mandate.

This skill's own rubric (exemplar): MUST — (1) every curation pass names the governing umbrella skill it patched; (2) durable lessons land in the skill body or a linked reference, never only in memory; (3) the change is class-level (an umbrella gains the lesson, not a one-off skill). MUST-NOT — no no-op review passes when the user asked for active curation; no narrow one-off skills for single sessions; no invented lessons when no durable signal exists. GOOD-LOOKS-LIKE — a later session facing the same class of problem starts already smarter because the lesson is findable in the library itself.

## What belongs in references/

Put in `references/`:
- compact session notes that may be useful later
- concise evidence, examples, or extracted guidance
- reproduction notes and tool quirks that are useful but not core policy

Do not turn references into a full transcript mirror.

## What not to capture

Do not encode:
- environment-dependent failures
- transient setup problems
- one-off project narratives
- negative claims about tools that may change later

If a setup issue is durable, capture the fix in a relevant setup/troubleshooting skill instead.

## Pitfalls

- Creating too many narrow skills for single sessions
- Storing workflow lessons only in memory instead of the skill body
- Failing to add a support file when the detail would clutter SKILL.md
- Forgetting to mention overlapping skills when curation touches multiple umbrellas
- Capturing a user-corrected formatting, tone, or scoring rule only in memory instead of the governing skill; update the class-level skill and add a reference note when the lesson should persist for future rebuilds
- Treating a repo-boundary correction as a simple path fix; if the user says the repo is wrong, verify the canonical bundle and adjacent aliases before making or summarizing edits
- Compressing or generalizing a process when the user explicitly asked for the full start-to-finish flow; preserve every established step and sub-step in the governing skill instead of inventing a shorter version
- Reporting a side effect as complete before verifying it with tool output; if a file, doc, or skill change is mentioned, confirm it directly before telling the user it happened
- Treat a "stuck" or channel-confused report as a literal tooling failure; first inspect the latest user message and the surrounding conversation for the real workflow lesson
- When the user says the Telegram/channel session is "not working correctly," do not jump straight to gateway or transport fixes; audit the last user turn and last assistant turn for the actual mismatch before deciding what to save
- Compressing a user-corrected full process into a simplified outline instead of preserving the established start-to-finish steps
- Blending distinct advisor categories together when the workflow has already established a three-way taxonomy
- Downgrading narrow specialist advisors just because the lane is narrow; keep them highly credentialed and elite within their focus
- When the user asks for a more psychologically attuned coach voice, patch the governing coaching-engine umbrella so tone, question examples, response rules, and process flow stay aligned; do not update only the sample prompts
- Assuming that write_file and terminal tools are always available; in restricted environments, first check tool availability and consider alternative approaches such as storing content in memory for direct output or deferring actions to a session with full tool access.

## Report rebuild curation note
When a deck/report rebuild surfaces a durable formatting or scale correction (for example, a rejected `1–10` mapping), update the report-rebuild umbrella skill's pitfalls/verification section and link a concise reference note. Keep the rendered artifact as the verification target, not just the source file.

## Verification

Before finishing a skill update:
- confirm the skill name is class-level
- confirm the body includes a clear trigger and workflow
- confirm support files are linked from SKILL.md
- confirm the change is durable and not session-noise

## Support files

- `references/skill-rubric-field-spec.md` — rubric field spec (MUST / MUST-NOT / GOOD-LOOKS-LIKE), living-rubric evolution rule, Skill2Env external validation (T-261004-0075 seq 8).
- `references/skill-library-curation-notes.md` — compact session lessons and examples for deciding what to save.
- `references/report-rebuild-format-guardrails.md` — durable notes from report/deck rebuilds where the user corrected formatting, scale labels, or verification expectations.
- `references/channel-context-and-latest-message-rule.md` — notes on treating channel confusion, stale summaries, and "stuck" reports as a cue to inspect the latest user message and capture the underlying workflow lesson.
- `references/full-chat-audit-before-skill-update.md` — reminder to audit the full thread before saving a skill update when the user says the assistant missed part of the ask.
- `references/full-process-preservation-and-dedup-notes.md` — notes on preserving full start-to-finish flows, explicit sub-steps, and advisor category distinctions instead of compressing them.
- `references/advisor-taxonomy-and-credential-standards.md` — notes on the three-way advisor taxonomy, best-in-field/best-in-niche positioning, and what "highly credentialed" should mean in practice.
- `references/runtime-package-consistency-audit.md` — bundle-consistency notes for agent/package maintenance where runtime wrappers, docs indexes, and canonical docs must stay aligned.
- `references/versioned-engine-family-registry-pattern.md` — shared registry pattern for Qubit-style versioning across a related engine family.
- `references/start-here-launch-surface.md` — pattern for adding a dedicated launch page when a runtime package needs a shortest explicit entry path.
- `references/telegram-channel-stuck-session-note.md` — concise lesson on treating "stuck" or wrong-turn Telegram sessions as drift checks against the latest user message and assistant reply.
- `references/launchd-telegram-route-verification.md` — layered verification notes for launchd-backed services, direct health checks, gateway status, and routing-mode inspection.
- `references/product-lane-alias-hunting.md` — alias-hunt workflow for correcting named engine/lane mismatches and choosing the right fallback artifact.
- `references/product-naming-canon.md` — canonical naming notes for product lines and the rule to keep distinct names visible across artifacts.
- `references/repo-boundary-and-doc-label-normalization.md` — notes on auditing the owning repo, rolling back stray edits in the wrong repo, and normalizing repo labels across the docs bundle.
- `references/repo-disambiguation-lesson.md` — this session's repo-boundary correction: wrong-repo detection, adjacent-alias search, and bundle verification before settling on the canonical lane.
- `references/chat-review-memory-skill-capture.md` — curation notes for review-the-chat requests that should produce durable memory + skill updates.
- `references/voice-workflow-layer-separation.md` — notes on preserving a branded public voice separately from a generic workflow layer in repo-owned specs and docs.
- `references/active-update-and-umbrella-shape.md` — notes on the active-update mandate and the class-level umbrella shape expected for new or revised skills.
- `references/active-skill-update-session-note.md` — this session's note on treating explicit skill-library review requests as a mandate to capture at least one reusable lesson when available.
- `references/pipeline-upgrade-micro-task-discipline.md` — lesson: apply fixes as micro tasks one at a time, never claim "all done" without verifying each. Plus: never guess personality types, tech pipelines need scientific grounding, and both dual-process-research-pipeline + execution-over-documentation are user-owned (recommend `hermes curator adopt`).
- `references/adaptive-credential-matrix-and-roster-reuse.md` — session note on inactive-pool inspection, in-place roster reuse, and role-by-role credential matrices for agent expansion.
- `references/inactive-roster-skillset-reuse.md` — compact lesson from the voice-message roster correction: inspect inactive pools too, preserve lineage, and add skillsets in place instead of recreating agents.
- `references/roster-lineage-and-inactive-pool.md` — notes on checking inactive/archived rosters, including adjacent canonical pools, and revising existing agents instead of recreating them.
- `references/skill-update-no-op-avoidance.md` — concise note on avoiding no-op skill-library review passes when the user has explicitly asked for active curation.
- `references/class-level-umbrella-skill-shape-session-note.md` — this session's note on the class-level umbrella shape and roster reuse lesson.

## Added workflow note
When a repo-owned agent package needs a clean launch surface, create a dedicated `START-HERE.md` and wire the runtime wrapper + launch guide to it in the same change. Verify the read order across those files agrees before finishing.

## Note: protected skills and the inline-Python-heredoc workaround (Aug 2026)
The single-step inline Python heredoc — `python3 << 'PYEOF' ... pathlib.Path(...).write_text(content) ... PYEOF` run via `terminal` — is a cleaner variant of the baseline-first gate's Workaround B (one call, no temp `.py` file, safe when `write_file` is blocked for all paths, and immune to the terminal backgrounding detector that misfires on bash heredocs containing `&&`/`2>&1`). Its proper home is `baseline-first-surgical-precision`, which is currently **user-owned** (`created_by=None`) and therefore off-limits to autonomous curation. Recommend `hermes curator adopt baseline-first-surgical-precision` so the workaround family can be extended in place.

## Architecture validation note
When proposing a classification taxonomy, evidence hierarchy, or content categorization system, test it against real data (50+ items from the target corpus) BEFORE committing to the build. Regex patterns that sound correct in theory may classify only 34% of real entries. See `references/architecture-validation-against-real-data.md` for the case study where a "universal study design hierarchy" turned out to apply to only 4% of actual library content.