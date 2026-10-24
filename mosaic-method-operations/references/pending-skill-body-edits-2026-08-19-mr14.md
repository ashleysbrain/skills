# Pending SKILL.md body edits — MR14 session (2026-08-19, hermes)

Background curator refused the direct SKILL.md patch (read-before-write
loop); parking the intended body edit here for foreground application.

## Intended edit (References section of your-stack-operations/SKILL.md)

Append after the ci-deterministic-testing.md bullet:

- `references/conductor-reach-census-mr14-2026-08-19.md` — "flows
  through ALL engines" wiring census method + five recurring conductor
  error classes (keyword-filter parking, selftest prod pollution,
  healthy-vs-dead silence, protocol bypass, off-vocab major-path
  writes); panel ops incl. re-falsification gates and transcript
  salvage.

## Optional second edit (Iteration protocol step 4 enrichment)

After "VERIFY live: gate selftests AND a real run", consider adding:
re-falsification = re-run the original prober's exact probe in
subprocess form (as CI runs it; heredoc-stdin breaks multiprocessing
spawn on py3.14) before declaring a finding closed.

Reference file itself is already written and live at
references/conductor-reach-census-mr14-2026-08-19.md.
