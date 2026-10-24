# Evidence-Grading Gate for Specialist Content — reference

Session-proven procedure from 2026-08-15, when the principal falsified a 10-seed LinkedIn content backbone that had been presented as "true stories from banked assets."

## The failure pattern
A specialist (Andreasen) generated a content backbone from banked session assets. Every seed LOOKED grounded because each cited a real session deliverable. But the cited deliverables themselves contained unverified claims, and no one graded the seeds against live system state before presenting them as publishable truth.

## The grading procedure (run before banking or publishing any specialist content)
1. For each factual claim in the content, identify the verifiable artifact: code path, DB row, running server, signed letter, published piece.
2. Check the artifact LIVE: sqlite3 queries, curl the endpoint, ls the file, grep the code path. Never grade from memory or from another agent's summary.
3. Assign the grade:
   - A — artifact exists and matches the claim's wording. Publishes as written.
   - B — artifact partially matches. Reword to the true state ("we are building X" not "X is live"; "our forecast is p=0.65" not "65% of fleets fail").
   - C — no artifact or the artifact contradicts the claim ("recruited" vs "willing"; "series" vs "no posts yet"). Park until reality catches up.
4. Write the grade INTO the content artifact next to each claim, with the one-line evidence note.
5. Publishing rule: A publishes on schedule, B only after rewording, C is parked. No seed graduates without its grade.

## Worked examples from the 2026-08-15 falsification
- "Our AI fleet has a vital-signs chart" — GRADE B: only the OS-OS-KPI-DASHBOARD-SPEC.md exists (a spec), no built dashboard UI served live.
- "What 65% of agent fleets get wrong" — GRADE B: p=0.65 was Tetlock's calibrated forecast (our prediction), not a measured industry statistic.
- "We recruited an academic bench before a product" — GRADE C: Anantua was WILLING (nothing signed), Alterovitz a prospect. False as worded.
- "We blocked our own writing engine from citing papers it never read" — GRADE A: pipeline_api.py L292 phantom-citation blocker live; runs completed same day with complete_with_quality_issues status in pipeline_runs.db.

## Why this binds the orchestrator too
The orchestrator's summary layer can launder an unverified claim into "banked truth" — a specialist says it, the orchestrator banks it, the next dispatch cites it as ground truth. The grade must be checked against the LIVE artifact at every hop, not inherited from the previous agent's confidence.

## Adversarial multi-round QA (principal directive 2026-08-15: "do another thorough QA pass... I'm not even reading this until we go through this a couple of times")
Strategy documents and plans get a MINIMUM of two falsification rounds by different brains before the principal reads them:
1. Round 1: Popper falsifies the plan's structure — sequencing, missing microtasks, premise errors, instrument choice. Her 2026-08-15 dual-track kill: 3 fatal gaps (equity-first instrument inversion when all named doors were non-dilutive grants; shell entity with no IP conveyance/data room; zero evidence artifacts scheduled).
2. Round 2: a DIFFERENT adversarial brain (e.g. Tetlock for forecast/instrument questions, Bridgman for artifact-dependency questions) attacks what survived round 1.
3. Only after both rounds does the principal see the rebuilt plan.
Sequential rounds, never parallel. Gate each round. The plan the principal reads must already carry the fixes, not the debate.

## People-verification via Crossref/arXiv (principal pattern 2026-08-15)
When the principal names a real-world expert as a potential advisor/partner, VERIFY the person before building strategy on them:
- Crossref: `https://api.crossref.org/works?query.author=<Surname>` — scan titles, venues, dates; confirm the domain matches the claimed expertise
- arXiv: `http://export.arxiv.org/api/query?search_query=all:"<Surname>"+AND+cat:<category>` — confirm active publication line
- Record verified publications in the strategy doc (e.g. Anantua: M87* EHT charge constraints PRD 2021; Alterovitz: vcf2FHIR 2021) — this converts "principal says they're good" into "verified published, domain-matched"
- web_search may be billing-blocked; Crossref/arXiv APIs work regardless (they don't route through Firecrawl)
