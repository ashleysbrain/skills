# Team Backlog Census + Ledger Schema Map (2026-08-18)

(Also relevant to the bundled `notion` skill, which curator writes cannot touch.)

## Census method (separate demo data from real input)
- Pull all objects via `/v1/search` (paginate), group by `created_at`.
- An exact-timestamp cluster = Notion template seed data (observed: 23 objects all stamped 2026-08-14T19:49:00, sample PRDs, "Lumi Labs" refs). NOT team input — leave untouched, never mint.
- Real input = distinct recent timestamps, named owners, priorities (observed: 4 real rows — Qubit MVP, Spiritual Wellness, Computational Psychiatry blueprint, BI tools project).

## Notion DB → the OS ledger field map (team converged on this unprompted)
- AI-DLC Stage / Pillar / Stage (Triage-Ship) → `kind` / `lane`
- Priority P0-P3 → `severity` (1-4)
- Teams, Confidence → `caps` / notes
- Is-Blocking / Blocked-By → `depends_on` (comma-separated task ids)
Adopt as the canonical intake-mirror shape.

## Intake posture (review-first)
- Read-only until principal releases: GET-only against Notion; mirror JSON to disk; dissect via gated panel; mint to `~/your-org/your-stack/stores/task-ledger.db` only after explicit go.
- Never write or delete team content in Notion. a teammate's (Nanditha Murthy's) rows are immutable — additive mirrors only.
- ntn CLI: search needs explicit `-X POST` (bare path = 400 invalid_request_url).

## Where the loop design lives
`software-development/mosaic-os-architecture/references/notion-intake-loop-2026-08-18.md` — Notion-as-application placement, 6-step intake loop, BUILT vs TO BUILD split.
