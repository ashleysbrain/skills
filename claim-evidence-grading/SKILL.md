---
name: claim-evidence-grading
description: Grade claims A/B/C against live state before publishing.
version: 1.0.0
author: the operator agent Agent
license: MIT
metadata:
  hermes:
    tags: [qa, content, evidence, claims, publishing]
---

# Claim-Evidence Grading

Origin: 2026-08-15 principal falsification catch. A 10-seed LinkedIn idea backbone was presented as "true stories from banked assets"; the principal's response: "those true stories aren't even true... you're claiming things that aren't even true in the things you're saying you're doing." Mechanical re-audit: 4 of 10 seeds overclaimed or false as worded. Root cause: claims were graded against what the session DISCUSSED, not against what the system CONTAINS.

## When to use
- Before publishing any article, post, thread, or newsletter seeded from internal work
- Before presenting a capability statement, roadmap claim, or partnership claim
- Before any content whose thesis is honesty, calibration, or claim-grading itself (double standard = fatal)
- When building an editorial backbone or idea backlog from project assets

## The grading standard (mechanical, not vibes)

Every claim gets exactly one grade, verified against live state:

- **GRADE A — true as worded.** A runnable operation exists (code live on disk and serving), the event actually happened (logs/DB prove it), or the artifact is real (file exists with the claimed content). Publishes as written.
- **GRADE B — real substrate, wrong tense or scope.** The thing exists but the claim overreaches: a spec presented as a build, a forecast presented as a measured fact, an unbenchmarked mechanism presented with implied results. Publishes ONLY reworded to the true state ("we built the gate" not "it saves 40%"; "our forecast: 0.65" not "65% of fleets").
- **GRADE C — false or premature.** Reality hasn't caught up to the claim: willing-but-unsigned partnerships, unstarted series, personal claims with no data. PARKED until reality catches up. No publishing.

## Verification operations (how you actually check)

1. **Code claims**: file exists + imports + live endpoint (curl the port; check the log ran today). WARNING: grep RECURSIVELY. The 2026-08-16 Popper catch: an audit claimed "zero CSD refs in engine code" using a top-level glob (ds-*-engine/*.py) and missed 1,672 references inside src/ subdirectories across 10+ engines. A claim graded against a narrow grep is a claim graded against nothing. Minimum: grep -rn --include=*.py <term> <workspace-root>, exclude .venv/node_modules, then classify hits (def/class = implementation; comments = vocabulary only).
2. **Event claims**: query the DB/log for the actual run (e.g. pipeline_runs data blobs for status values)
3. **Spec-vs-build**: is there a built artifact, or only a SPEC document? A spec file titled "dashboard" is not a dashboard. COROLLARY (2026-08-16 principal catch, the crontab-theater class): a SCHEDULED JOB is not a WORKING SYSTEM. A crontab entry proves intent, not function. Verification for any "our system does X continuously" claim requires: the job's log file EXISTS, was written RECENTLY (within its scheduling interval x small factor), and contains non-error output. The autonomic-layer catch: three cron jobs, two with no log file at all, one dead for 7 weeks, one ending in an ERROR. All were described as "live running infrastructure" because the crontab listed them. Schedule is not function.
4. **Forecast-vs-fact**: whose number is it? If the org produced it via a prediction process, it's a forecast; frame it as ours
5. **Partnership claims**: artifact test — is there a co-signed letter, agreement, or co-authored output? Willing + nothing signed = GRADE C "forming", never "recruited"
6. **Series/habit claims**: has installment #1 actually shipped? If not, the series doesn't exist yet
7. **Advisor-drafted copy**: any document with external-advisor attribution (marketing drafts, positioning docs) is NOT a data source. Its "findings" are narrative devices until independently verified against a real dataset. This is the 2026-08-16 fabricated-lag origin: NEWSLETTER-001/002 carried a "48-hour sleep/finance lag" written by advisor attribution, and it survived two grading passes before the principal caught it.

## Publishing rule
A publishes on schedule. B publishes only after rewording to the verified true state. C is parked with its graduation condition named (what reality must produce). No seed graduates without its grade, and grades are recorded in the backlog artifact next to each seed.

## Pitfalls
- **Verb-tense fabrication (2026-08-27, principal catch x2).** Narrating a minted task or inert code in present tense ("every utterance gets tagged") is Grade C behavior even when every noun is real. Standing law: capability statements carry a state marker — BUILT-RUNNING (live process checked same turn) / BUILT-INERT (file exists, nothing runs it) / DESIGNED (spec only) / ORDERED-ONLY (task minted, nothing else). See `references/verb-tense-state-markers-2026-08-27.md`.
- **UI-captured human intent is a claim, not a fact (2026-08-27).** A console logged "principal approved" from a click on the text-entry bar — false-input capture. Any human ruling recorded by a UI surface is Grade B until corroborated (explicit submit action, no click-through capture). When a user disowns a logged ruling, revert first, audit same-signature rulings second.
- **Grading against the plan, not the system.** Discussion in a session is not evidence. The disk, DB, and logs are.
- **The plausibility trap.** Well-written deliverables feel true. The catch list (spec-as-build, forecast-as-fact, willing-as-recruited) all read naturally and shipped confidently.
- **Marketing copy is not data (2026-08-16).** A vivid "experiment finding" traced to advisor-drafted campaign copy, not to any dataset. In-house marketing docs get the same live-state verification as everything else. Advisor-persona drafts are voice targets, never evidence.
- **Downgrade is not purge (2026-08-16).** Changing metadata grade to C while leaving the fabricated claims asserted in the draft's content body means the next writer still uses them. A downgrade rewrites the body: PARKED briefs lead with parked status and name the fabrication. A [NEEDS DATA] footer does not neutralize a table row that asserts the claim as fact.
- **Delegate re-injection (2026-08-16).** A specialist spec re-used already-caught fabricated claims hours after the audit caught them. Screen every panel/delegate output against the known-false list before folding it into plan docs.
- **Missing graduation conditions.** A C-grade without a named graduation condition (what reality must produce) is an unowned promise. Audit found half the parked briefs lacked theirs.
- **Confusing internal honesty language with external verification.** Saying "built/in-validation/theoretical" in your framework while shipping unverified seeds underneath it is the exact failure the principal flagged — the meta-claim of honesty makes the ungraded claim MORE damaging when caught.
- **Agent-written personal claims.** First-person founder claims (health, habits, history) are GRADE C unless the human supplied the material directly.

## The parroting pitfall (2026-09-05, "four asks" catch — FIRST-CLASS)

**A number the user supplies is a hypothesis, never a measurement.** principal said "I've
brought this up at least four times"; the response quoted "four asks" back as if it
were a measured count. principal: "you're only telling me four asks because I gave you
that number. I don't even think you're accurate." The record (queried, not recalled)
showed **8 distinct asks over 19 days across 4+ threads** — the parroted number was
an undercount AND an unverified claim wearing the user's authority.

Same anatomy as every fabrication class above: a true kernel (the user did ask
repeatedly) + a number the speaker never verified + borrowed confidence from the
source's authority. Parroting feels SAFE ("I'm just agreeing with them") which is
why it survives every honesty gate that catches invented facts — it's not invented,
it's unverified.

**Mechanical rules:**
1. When the user states a count, duration, frequency, or quantity, and your reply
   will RE-STATE that number, the number is now YOUR claim — grade it.
2. Count/verify from records in the same turn, before the sentence containing the
   number. For cross-session counts: query `<agent-home>/state.db` table `messages`
   (`role='user'`, FTS via `messages_fts`); `sessions/*.jsonl` is a legacy mirror
   (ends 2026-05-29) and the other `.db` files are empty shells — see
   `references/session-history-store-2026-09-05.md`.
3. If records disagree with the user's number, report the measured count with the
   evidence — never silently adopt theirs, never argue the number, show the query.
4. Deduplicate repeated deliveries: one voice message delivered to six sessions is
   ONE ask in six envelopes; count intent, not message rows.

## The scope-borrowing pitfall (2026-08-27, "header work was solid" catch)

**A QA verdict on PART of a thing is not a claim about the WHOLE.** The recurring
fabrication signature this week: a real, verified fragment gets narrated with
borrowed confidence covering unverified scope. Concretely: a header-law build
passed QA on *structure* (one header, zero harness-name occurrences — machine
verified), and the orchestrator relayed it as "the header work is solid." The
dynamics *payload* inside that header was never computed or verified — prose in
an emitter. The QA verdict itself said "machine-checkable shipped claims"; the
scope qualifier was dropped in relay.

**Mechanical rules:**

1. **Relay the verdict's scope verbatim.** If QA said "structure verified,"
    the principal-facing sentence is "structure verified, payload unverified" — never
    "solid."
2. **Before saying "X is done/solid," enumerate X's parts** and ask which
    parts the verification actually touched. Any untouched part = say so or
    say nothing.
3. **Audit-then-census before any "is it real?" answer:** grep for the
    computing code, not the naming. "Dynamics law marked DONE + zero modules
    deriving dynamics at dispatch time" = decor, caught in one grep. A law on
    paper is DESIGNED, not BUILT.
4. Same class: "gates are solid" (enforcement real, evolution unbuilt),
    "firewalls stream appropriately" (skeleton files exist, nothing runs).
    Every one had a true kernel + an overreaching verb.

See `references/scope-borrowing-qa-verdicts-2026-08-27.md`.

## Known overlap
This skill covers factual-state grading of claims. The `external-content-qa-pipeline` skill covers the broader external QA pipeline (AI telltales, voice, cross-doc consistency) and already carries a "no fake metrics" pitfall; this skill sharpens that into the A/B/C mechanical standard. Curator should eventually fold this into that pipeline's factual-accuracy section, or keep this as the dedicated pre-publish grading gate.

## References
- `references/2026-08-15-linkedin-seed-catch.md` — the worked example: the full 10-seed re-audit table, the verification commands used, and why a well-written audit still shipped bad seeds.
- `references/verb-tense-state-markers-2026-08-27.md` — state-marker vocabulary (BUILT-RUNNING / BUILT-INERT / DESIGNED / ORDERED-ONLY) and the pre-send process check; origin: the firewall fabrication catch.
- `references/time-perception-presence-vs-testimony-2026-08-27.md` — three escalating time-claim failures (UTC-as-local, gap-as-morning, invented 2h downtime); the four mechanical rules that prevent the fourth.
- `references/scope-borrowing-qa-verdicts-2026-08-27.md` — QA verdict on PART ≠ claim on WHOLE: the "header work was solid" catch, the true-kernel-plus-expanded-verb anatomy, and the pre-relay scope check.
- `references/session-history-store-2026-09-05.md` — where cross-session history actually lives (`<agent-home>/state.db` messages table), the verified dead ends, and the working SQL pattern for cross-thread counts (the "four asks" recount).
- `references/2026-08-16-reinjection-catch.md` — the second-day recurrence: marketing copy graded as data, downgrade-without-purge, delegate re-injection four hours post-audit, and the standing-screen doctrine with the exact mechanical regex screens that worked.
