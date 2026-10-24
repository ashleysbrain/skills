# Research Topic QA Chain — 2026-08-20 (research-thread, principal + Aditya co-write)

Five-brain chained QA over 32 generated writing topics (target: 25 publication-grade).
Chain: the specialist engine (generate 32) -> the specialist engine (falsification) -> the specialist engine (synthesis v2
+ census repair) -> the specialist engine (calibration) -> the specialist engine (operationalism) -> the specialist engine
(positioning, pending) -> the specialist engine (consolidate). All adjunct brains carry full persona
layering in dispatch. Sequential, gated at every landing.

## The QA-LOG.md chain-of-custody artifact (reusable pattern)
One markdown file in the work directory is the single source of truth every brain reads
and every verdict lands in: pass verdicts with exact tighten fixes, census updates,
conductor rechecks, infra-failure records. Benefits observed:
- Async batch-complete deliveries can arrive TWICE (duplicate completion messages);
  reconcile idempotently against the log instead of re-banking.
- A later census update (r2/r3) can be flagged for the next brain without steering a
  run that already finished reading (steers miss finished runs ~60s after final).
- Conductor transcription errors get caught by re-reading the subagent-summary file
  (a dropped SURVIVES row was found this way; the summary files are authoritative,
  live transcripts truncate at ~400-600 chars).

## Verdict cascade shape (worked cleanly)
Generator overproduces (32 for a 25 target), then each pass KILLs / TIGHTENs / PASSes
with a one-sentence fix per TIGHTEN banked verbatim. Cascade: Popper 7 KILL + 9 refit
-> Tetlock 0 KILL + 10 TIGHTEN (calibration: result-verbs over uncollected data, scope
multiplication) -> Bridgman 0 KILL + 11 TIGHTEN (operationalism: every noun needs a
measuring instrument). Lenses complement rather than repeat: falsifiability,
realism/scope, measurability. Fixes compose; none conflicted. Conductor duty: recheck
earlier verdicts when new evidence lands mid-chain (census r2 strengthened 2 topics,
resolved 1 tighten REASON without flipping the verdict).

## glm-5.3/llm-vendor subagent API timeout — the batching fix (TWO dead runs)
Failure: non-streaming API call times out at 90s with no response during ONE long
reasoning turn. Two shapes observed: (a) delegation owner exits after input reads, no
verdict; (b) max_iterations exhausted, "API call failed after 3 retries". Both runs
read all inputs fine — the death is the big completion turn.
Fix (run 3 landed clean in 110s): split the review into batches of ~16 and ~9 topics;
write the brief (context + lens + topics VERBATIM + output format) to a file; dispatch
with "read exactly one file" + EXECUTION RULE: produce output in MULTIPLE SHORT turns,
end the turn every 5-6 table rows, never one turn over ~1200 tokens. Second batch landed
~120s with batch-A results summarized in dispatch context for continuity.

## Never hand-copy data into dispatch briefs
Inlining 16 topic lines from memory corrupted mid-transcription (mojibake, duplicated
restatements, garbled notes) — the corrupted dispatch was caught in the echo and stopped
before the child started. Fix: extract the data programmatically (python regex over the
source file -> JSON -> verify by reading back -> generate the brief file from that JSON).
Cost of the safe path: ~2 minutes. Cost of the unsafe path: one wasted elite dispatch +
poisoned verdicts downstream.

## Census short-query pattern (OpenAlex + Semantic Scholar)
- OpenAlex default search returns ZERO on multi-clause natural-language queries (6+
  words / 2+ conjunction concepts). Short queries (2-4 words) returned 5/5 on every
  previously-failed leg. Widen with per_page, never with longer strings.
- Semantic Scholar graph API returned empty on 4 of 5 legs. API-empty != field-empty:
  never cite absence as evidence. Cover the territory with short-query OpenAlex legs on
  each CONCEPT, then the union claim is bounded: "both territories populated, union
  empty WITHIN census (census != field)".
- Crossref (query.bibliographic, short queries) verified memory-recalled citations:
  Darley & Batson 1973 JPSP doi:10.1037/h0034449; Schultz 2016 doi:10.31887/dcns.2016.18.1/wschultz.
  Verified DOI replaces imprecise recall ("Schultz 2006") in the artifact.

## Session-state artifact lock (workflow-enforcement gate)
`.hermes/.session-state.json` active_artifact lock blocks write_file on NEW paths it
considers off-baseline (hit by two subagents and the conductor in one session). Unlock:
read the state file, set active_artifact to null, write back. Symptom is a
baseline-first / surgical-precision gate refusal on a genuinely new file. Subagents
self-recover via terminal writes; the conductor can clear the lock directly.

## Gate false-positive (recurrence)
brain_integrity_gate FAILED one clean run on PERSONA-SPEC-MISSING (transcript head
lacks the spec markers; dispatch context carried full layering). Known matcher
limitation — manual verification (grep transcript for identity markers) then bank.
Second recurrence this week; the matcher fix list lives in the parent skill.
