# CFP writing-mission referrals through the Writing Studio

Applies when the principal sends a call-for-papers, edited-volume, showcase, or
collection link framed as writing intent ("we are going to write for this",
"send through the studio for ideas and revisions"). Class of task: turn a
referred call into a gated, studio-produced submission package with principal
sign-off.

## Procedure
1. **Pull the FULL call text from the source page.** Use a real browser tab
(`new_tab(url)` → wait ~3-4s → `document.body.innerText`) — an anchor URL
like `#submit` still renders the whole page, and web_extract summaries drop
submission mechanics. Extract and record: deadline, word limit, required
extras (keywords, bio note), submission inbox (often plain email, not a
portal), editors, notification and publication dates, and the call's own
framing of what qualifies.
2. **Enumerate ALL open calls on the page before drafting.** A single center
site can host SEVERAL distinct calls with different deadlines, formats, and
inboxes (e.g. an abstract volume due one date AND a tools/showcase call due
another). Bind each deliverable to its own deadline and inbox; never assume
one CFP per domain. If the principal names a second call by title, locate it on the
same page or its true source before searching the open web.
3. **Seed one studio draft PER CALL with its own thesis angle.** Two calls from
one center get two drafts and two Veritas runs; record both run ids in the principal
report so neither mission goes quiet. The strongest angle is usually where our
daily operating material IS the phenomenon under study — not decorating a
generic topic with our vocabulary.
3. **Seed a studio draft**: `PUT /api/drafts/<uuid>` on the studio API (port
8310, `Authorization: Bearer $WRITING_STUDIO_TOKEN` from `<agent-home>/.env` —
the variable is WRITING_STUDIO_TOKEN, not STUDIO_TOKEN) with title + content
carrying the thesis brief mapped against the call's own framing: what the
venue asks for, not what we want to say. A 401 means wrong token variable.
4. **Launch a Veritas run**: `POST /api/veritas/runs` with the draft id and
idea; poll `/api/veritas/status/<run_id>`. Record the run id for the principal
report.
5. **Diagnose failures from the state file before re-running.** The newest
`/tmp/Veritas_process_state_*.json` carries `stage_results` with per-stage
verdicts and error fields. A stage failing on generator output (e.g.
argument-architecture skeletons whose every variant has a JSON parse error)
re-fails identically on a blind re-run — the defect is in the stage's output
handling, not the draft text. Root-fix the stage, then re-run the same idea.
6. **Deliver the gated abstract/proposal for principal sign-off** — full text plus
the venue checklist (deadline, limit, extras, inbox). Submission itself is
principal-triggered: never auto-send to a call's inbox.

## Pitfalls
- **Drafting from search summaries.** Search-result snippets of a call omit
the word limit and inbox; always read the live page.
- **One page, many calls.** Missing the second call on a multi-call site means
a missed deadline class of failure; enumerate at intake.
- **Treating a pipeline stage FAIL as a verdict on the idea.** Error keys in
stage_results mean broken engine, not rejection — inspect state before
concluding anything about the draft.
- **Reporting a gated deliverable from a broken ladder.** When one mission's
run FAILs on a pipeline defect, the other mission's still-running draft does
not inherit success: re-run the failed one post-fix and say plainly which
artifacts are pending. Never present either deliverable as final until its own
run completes the ladder.
- **Auto-submission.** The principal writes for these venues under their own name;
sign-off precedes any send, always.
