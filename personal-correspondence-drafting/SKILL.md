---
name: personal-correspondence-drafting
description: Use when writing a letter in the user's own voice.
---

# Personal correspondence drafting

Class of task: the user asks for a letter, explainer, or message written in THEIR
voice to a real person in their life (partner, family member, friend), usually
to explain a health or relationship situation. The output is handed over as if
the user wrote it, so fact discipline matters more than polish.

## Procedure
1. **Collect the user's own words first.** Their verbatim phrases are the
   skeleton: quoted sentences from the request belong in the letter nearly
   intact. When an illness or fog context is the subject, the letter explains
   rather than apologizes.
2. **Use ONLY facts the user supplied this session.** No invented names,
   timelines, histories, or third-party details. If a person is referenced
   without a name, either omit names entirely or leave a placeholder for the
   user to fill. An invented detail in a personal letter reads as fabrication to
   the one reader who knows the truth, and costs the letter all credibility.
3. **Register-match the recipient.** Scientist readers get mechanism-first with
   citations; non-scientist readers get the same content as plain-language
   metaphors with zero jargon. On rewrite requests, PRESERVE scope: "rewrite"
   changes register, never content coverage.
4. **Carry the user's honest self-assessments without endorsing total verdicts.**
   When the user states a fault ("I didn't do it right at first"), the letter
   keeps it. When a claim is illness-shaped ("everyone is better off without
   me", "it's all my fault"), acknowledge the thought exists while declining to
   assert it as fact: name it as the documented symptom of the state, and do
   not argue it at length.
5. **Ground in real sources when science is cited.** Live-fetch the studies;
   list them at the end; keep an honest-limits section (group statistics,
   adjacent-evidence caveats, no diagnosis). Include real crisis resources when
   dark thoughts are part of the subject matter.
6. **Gate before delivery.** Run the AI-tell scanner on the final file; PASS
   required, on the whole file. Read back what was written.

## Pitfalls
- Personal-voice register is NOT an exemption from the telltale gate: intimate
  first-person documents still get scanned, and readers catch tells fastest in
  letters meant to pass as the user's own words.
- **Hand-writing a letter in the user's voice is itself a protocol violation
  when a studio generation route exists — a self-run regex scan is not the
  gate.** The tells a homemade scan misses ("I want to be straightforward",
  five-item rhythm lists, mirror endings) are exactly the ones the panel seats
  catch. Route through the studio document/comment route and let the gates run;
  if you must post-process, re-run the binding gate on the final text.
- **When the letter is the user's alone (they did the hiring/built the
  relationship), strip every system/brand/organism identity from it.** A
  persona may draft WITH the user's facts, but the letter carries no mention of
  the organism, AI systems, or pipelines unless the user named them — their
  voice, their signature, first person singular.
- **Transcription artifacts in dictated facts must be flagged, not silently
  "fixed" or carried.** If a dictated fact reads as a slip (e.g. an accidental
  adjective that changes the meaning of a sentence about people), surface it to
  the user with your reading and let them confirm before it appears in a letter
  a third party will scrutinize.
- **Sensitive-fact clusters (visa status + unpaid + retention) read as legal
  exposure to a domain-expert reader and their IRB.** Carry the user's facts
  verbatim but flag the sentence to the user before sending: their fact to
  stand behind, but they decide the framing.
- **When the user adds facts AFTER a studio draft exists, regenerate with the
  full fact set rather than splicing the new sentences in by hand** — the new
  facts change the letter's center of gravity (a market-anomaly framing pulls
  the whole close), and a splice reads as two voices. Ask for all pending
  additions once, then run one revision.
- **A studio document route that keeps returning outline-skeleton text is a
  pipeline clamp failure, not a writing problem — diagnose the compose
  engine before iterating on prompts.** Check `generation_mode` in the route's
  custody JSON; `degraded_deterministic` means the LLM call died (60s
  single-attempt clamp on letter-sized prompts). The compliant bypass: drive
  the same voice engine directly with a letter-appropriate system prompt,
  run the same panel seats, and deliver with the failure stated — never
  hand-write the letter as a fallback.
- **The panel's design seat is fail-closed for document-kind artifacts and
  probes for rendered-report features (SVG figures, phi column layouts,
  clickable citations) — on a plain-text personal letter it ALWAYS returns
  REVISE on genre grounds.** Render through the render engine anyway so the
  seat has its artifact, but judge a plain-text letter by the five
  substantive seats (fact, truth, voice, no-reuse, ai-tells); a design-seat
  REVISE citing missing figures is a genre mismatch, not a letter defect,
  and five substantive PASSes clear the letter for delivery.
- Never re-litigate settled conversations. If the user says the recipient
  already knows something, reference it in one line and move on; re-explaining
  reads as not listening.
- Revision requests are deltas, not rewrites: apply the corrections listed and
  leave everything else intact unless told otherwise. "Don't delete important
  info, just rewrite" means scope-preserving register change.
- If the user's own material references self-harm or dark thoughts, answer the
  safety need FIRST (crisis resources, direct question about plan and means)
  before producing the letter; then carry the symptom-framing into the document
  itself.
