# QA pass laws and rotation ledger (MR10-MR13, 2026-08-18)

Session-born laws now binding in CONTRACT.md + mosaic.manifest.json. Read
before running any QA panel or remediating panel findings.

## L10 qa_freeze (how to actually run it)

1. Before dispatching a panel, claim surgical leases on every target file
   with ONE actor string (e.g. `hermes-mr11-freeze`) via SurgicalEdit.claim.
2. CRITICAL GOTCHA: the `actor` string passed to every later `g.apply()` on
   those files must EQUAL the lease actor. MR13 lost 15 heading edits to the
   self-override guard because the lease said `hermes-mr13-freeze` and the
   applies said `hermes`. Either release-then-apply as the same actor in one
   process, or claim leases under the exact actor you will apply with.
3. Lease TTL is 300s, shorter than audit windows. Renew or rely on
   `--leases` (purges expired rows) to inspect. Stale rows no longer outlive
   TTL (Sherrington F7 fix).
4. Remediation lanes MUST NOT edit frozen targets until the pass files. This
   was a three-witness finding (Popper, Lamport, Luria each burned budget
   re-anchoring to shas that moved mid-audit).
5. Surface active freezes to sibling operators: `python3 gates/surgical_gate.py --leases`.

## L11 claims_honesty

- `gates/claims_gate.py --check <dir>` mechanically rejects: encryption
  claims with zero crypto API call sites, PHI-class claims with zero
  enforcement markers, declared-but-unused functions.
- Honest alternative to removing a claim: mark it pending ("encryption
  pending") until the code exists and is verified live.
- Declared-but-unused is a FINDING class, not a feature. Wire the function
  into a real path or cut it. MR12: consent getConsent/setConsent sat
  declared-but-unused until wired into the liveness fetch + a header toggle.

## Exchange-first QA (free-energy rule for panels)

Before dispatching any panel on a surface, grep `audit/` for existing
QA-PASS / QA-MICRO-REVIEW files on that surface from sibling lanes (same
day especially). If one exists with unremediated findings, REMEDIATE THOSE
FIRST, then dispatch fresh brains to verify the remediated state. Re-measuring
known open defects is F > 0. MR13: QA-PASS-30 (process flows) existed with
5 macro + 6 micro defects and zero remediation commits; the right pass was
remediation + verification, not a duplicate audit.

## Rotation ledger (brains already spent on this organism)

Do not reuse within the same review lineage; record rotation in the report
header (principal directive: different brains every process).

- Build/render quality: the specialist engine, the specialist engine
- Claims/falsification: the specialist engine
- Systems/topology: the specialist engine
- State/ordering: the specialist engine
- Brand voice: the specialist engine
- Clinical 8D semantics: the specialist engine (sibling-agent seat, invoke only)
- Interoception/liveness: the specialist engine (sibling-agent seat, invoke only)
- Sibling lane used: the specialist engine, the specialist engine, the specialist engine, the specialist engine
- Grade C verdicts (Osler, Sherrington both hit C on 2026-08-18) demand
  same-pass remediation: C means prose-only claims or silent failures.

## Flow vocabulary (QA-PASS-30 remediation)

- One vocabulary: `stores/flow-registry.json` codes (15) must equal FLW-*
  mentions in PROCESS-FLOWS.md headings. `gates/store_gate.py --flow-sync`
  enforces both directions and runs in the CI battery.
- Stage writes go through `task_ledger.set_stage()` which enforces the
  flow's registered stages; legacy off-vocab stages warn loudly, never silent.
- Severity column = priority (1 highest). Incident-class alerting (data
  loss / fabrication / security) = Flow 3b: severity-1 mint with non
  self-healing origin posts a principal bus alert from submit (live-proven bus 2324).
- Backlog aging: `gates/ledger_whois.py --aging N` emits oldest-open tasks.

## launchd gotchas (MR13)

- `launchctl bootout` can silently fail; the old PID keeps running the old
  path. After any repoint: `ps aux | grep <label>`, kill the stale PID,
  reload, re-verify via `ps -p <pid> -o command=`.
- After directory relocations, grep ALL `~/Library/LaunchAgents/*.plist`
  for stale bridge paths; symlink resolution masks the drift until the
  bridge dies.

## Pending SKILL.md pointers (parked: guard refuses edits to existing SKILL.md)

- Point the QA-pass section of SKILL.md at this file.
