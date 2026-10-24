# PENDING SKILL.md BODY EDIT — merge into SKILL.md (curator)

Curator: insert the section below into `your-stack-operations/SKILL.md`
immediately BEFORE the "## Package map" section (single anchor:
`## Package map (detail: references/package-map.md)`). Rationale:
three durable protocol lessons from MR10/MR11 QA panels (2026-08-18).
The full session detail already lives in
`references/mr10-mr11-qa-panels-2026-08-18.md` (landed, no guard).

```markdown
## QA panel discipline (freeze, rotate, salvage)
- **FREEZE before dispatch.** Claim surgical leases
  (`SurgicalEdit().claim(path, 'hermes-<mr>-freeze')`) on every target
  surface and record shas BEFORE delegate_task of a QA panel. MR10 ran
  unfrozen: the target rewrote 3x under the probes and three brains
  burned budget re-anchoring. MR11 froze first: churn zero. Release
  leases when the panel files. Lease TTL is 300s (shorter than a panel
  run): the freeze is discipline-visible, not hard-enforced.
- **ROTATE brains per pass.** Repeat QA on the same surface wears
  brains NOT yet spent there (MR10: Popper/Luria/Lamport after Da
  Vinci/Tanenbaum; MR11: Wernicke/Osler/Sherrington). Track spent
  brains via the audit/ report series.
- **Route each brain through specialist_gate --route --specialist**
  immediately before delegate_task; Sherman routing expires after ~5
  min. Batch the routes in parallel, then dispatch at once.
- **SALVAGE timeouts, never re-dispatch blind.** A timed-out specialist
  usually finished the probes and died writing the report. Extract
  verdicts from /<workspace><deleg>/task-N.log
  (think/result lines), file the report under the auditor's name with a
  disposition note, close the ledger. Prevention: dispatch contexts say
  "write the report file as soon as probes complete, before polish".
- **Selftests NEVER read production stores** (the CI runner has none):
  fixture-based checks + an open-spy isolation proof. One red CI run
  (32181576234) taught this.
- Full protocol + reusable finding classes (declare-but-never-invoke,
  stats-vs-render divergence, INHERIT violation, prose-claims-vs-code,
  port-coupled CORS) + the localhost headless-shell DOM battery:
  references/mr10-mr11-qa-panels-2026-08-18.md
```

Also append one line to the SKILL.md References list:

```markdown
- `references/mr10-mr11-qa-panels-2026-08-18.md` — MR10/MR11 panel
  protocol, subagent-timeout salvage pattern, selftest store-isolation
  (open-spy), finding classes, DOM battery commands.
```
