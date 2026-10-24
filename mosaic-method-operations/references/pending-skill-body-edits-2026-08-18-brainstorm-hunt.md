# PENDING SKILL.md BODY EDIT — QA-pass session 2026-08-18 (brainstorm hunt)

Curator: fold into SKILL.md body at the "Related repos" area of
`references/package-map.md` (and optionally a one-liner in SKILL.md's
Package map section pointing at the new reference file). Attempted via
skill_manage patch 3x; blocked by _read_before_write guard (dedup view
does not count as a read in background sessions — known issue, see
memory note 2026-08-18).

## Edit 1 — append to "## Related repos" in references/package-map.md

After the existing your-workspace organism/ bullet, add:

- **Writing-studio RUNTIME lives in ~/your-workspace/, not this package**
  (false-"vanished" hunt 2026-08-18): `pipeline_api.py` (FastAPI, port
  8310, auth via `WRITING_STUDIO_TOKEN` in ~/your-workspace/.env, pass
  as `?token=` query param), `writing-studio.html`, `writing-studio/*.db`
  (brainstorms + brainstorm_links + angle_evidence + angle_threads tables
  all consolidated in `writing-studio/drafts.db`). Audit records inside
  your-stack reference that code by name — grep the package alone and
  you get zero hits, which reads as "feature gone". Route map:
  `/api/brainstorm`, `/api/brainstorm/save|saved|refine|batch`,
  workbench routes `/api/brainstorm/{bs_id}/links`,
  `/api/brainstorm/angle/{add,link,evidence,thread}`,
  `/api/brainstorm/{bs_id}/angle/{i}/evidence|threads`.
  Check server: `lsof -nP -iTCP:port -sTCP:LISTEN`; probe live:
  `curl "http://localhost:port/api/brainstorm/saved?token=$TOK"`.
  Full recipe: `references/feature-disappearance-investigation-2026-08-18.md`.

## Edit 2 — optional one-liner in SKILL.md Package map section

After the PROCESS-FLOWS.md bullet:

- **Cross-workspace split**: writing-studio runtime (pipeline_api.py
  port 8310, writing-studio.html, drafts.db) lives in ~/your-workspace/,
  NOT in this package. Run-record claims referencing studio code grep
  zero here — search your-workspace before concluding a feature is
  gone. Recipe: references/feature-disappearance-investigation-2026-08-18.md.
