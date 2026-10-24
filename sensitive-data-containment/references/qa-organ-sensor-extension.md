# QA-Organ Sensor Extension Protocol (executed 2026-08-17, genome v3 → v4)

How to add a sensor to the self-evolving QA organ
(`<agent-home>/scripts/qa_tick.py` + `<agent-home>/qa/qa-manifest.json`) so it
actually runs. Grew out of adding the phi-surface sensor; generalizes to any
new surface.

## Genome shape (get this wrong and nothing runs)

The manifest's `surfaces` field is a **LIST of dicts**, each:

```json
{"name": "phi-surface", "cadence_h": 1,
 "next_due": "2026-08-17T09:00:00-0500",
 "checks": ["health-private dir 0700, all files 0600",
            "git ls-files health-private == 0 (retrack)",
            ".gitignore has health-private/ and vaults/"]}
```

Failure modes observed when the shape was wrong:
- Appending a bare string (`'phi-surface'`) → tick crashes at
  `s["next_due"]` with `TypeError: string indices must be integers`.
- Adding a top-level manifest key instead of a list entry → silent no-op:
  the checker never runs, the tick stays silent, defects go undetected, and
  nothing errors. The silent variant is the dangerous one.

## Code side

1. Write `def check_<surface>(actions)` returning a list of defect strings
   (empty = healthy) in `qa_tick.py`.
2. Register it in the `CHECKERS` dict at module level.
3. Import guard: the phi checker uses `subprocess` for the git call —
   whatever the checker needs, confirm the module already imports it.

## Verification protocol (the part everyone skips)

Monitor Mode means stdout is a state key: silence = healthy. A naive
healthy-run-then-negative-test is MASKED — the healthy run advances
`next_due` past now, so the planted defect never gets sampled (the
cadence-gating trade-off biting the tester instead of the system).

```
1. python3 scripts/qa_tick.py          → expect [] (silence)
2. FORCE due: rewrite next_due to now for the new surface in the manifest
3. plant the defect (e.g. chmod 755 the guarded dir)
4. python3 scripts/qa_tick.py          → expect EXACTLY one DEFECT line
5. restore the defect
6. python3 scripts/qa_tick.py          → expect silence
7. python3 -c "json.load(open manifest)" → valid JSON
```

The sensor exists only when step 4 actually fired. On 2026-08-17 the naive
negative test (skip step 2) read as silent-failure twice before forcing due
exposed the masking.

## First sensor: phi-surface

Checks health-private perms 0700/0600, git retrack (ls-files count), gitignore
rules. Cadence 1h. Defect classes: phi-perm-drift, phi-retrack. Pairs with
the containment work in this skill's scrub runbook — containment without a
sensor decays.
