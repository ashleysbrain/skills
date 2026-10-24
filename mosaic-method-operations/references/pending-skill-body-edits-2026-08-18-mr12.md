# Pending SKILL.md body edits — MR12 session (2026-08-18, hermes)

Curator: apply these to software-development/your-stack-operations/SKILL.md.
(The _read_before_write guard refused direct patches from this background
review turn; new-file writes work, hence this parking file. Pattern matches
existing pending-skill-body-edits-* files.)

## Edit 1 — law range (intro paragraph)
OLD: "laws as data (CONTRACT.md + mosaic.manifest.json, L1-L9),"
NEW: "laws as data (CONTRACT.md + mosaic.manifest.json, L1-L11),"

## Edit 2 — new laws under "Standing principal directives encoded in the package"
Append after the L9 bullet:
- **L10 qa_freeze**: during an active QA pass, target surfaces hold
  surgical leases (`claim(path, '<pass>-freeze')` + shas pinned in the
  dispatch context); remediation lanes must not edit frozen targets until
  the pass files. Surface any time: `surgical_gate.py --leases`.
  (Three-witness MR10/MR11 finding: mid-audit churn invalidated probe
  baselines 3x and timed out one 1800s subagent before this law.)
- **L11 claims_honesty**: no doc/table/card/note may claim an enforcement
  that code does not run (encryption, PHI handling, consent);
  declared-but-unused functions are findings, not features. Enforced by
  `gates/claims_gate.py --check <dir>` (selftest 6/6; CI-wired).
  Honest escape hatch: mark claims "pending".

## Edit 3 — CI discipline paragraph, extend segfault rule
OLD: "close every sqlite connection before interpreter exit — four CI
runs died to segfaults before this rule existed."
NEW: append "A gc-sweep of connections is NOT sufficient (C-level state
survives); the reliable fix for teardown segfaults (rc=-11, selftest
prints PASS then dies) is flush stdout/stderr then `os._exit(0)`. See
references/qa-panel-laws-l10-l11-2026-08-18.md."

## Edit 4 — References section, add pointers
- `references/qa-panel-laws-l10-l11-2026-08-18.md` — QA panel freeze
  protocol, L10/L11 law rationales, runner-only segfault diagnosis chain,
  census merge law (INHERIT/verdict mapping/phantom-count), live DOM battery.
- `scripts/hub-dom-battery.sh` — re-runnable live DOM verification for a
  local hub page (cards>0, no em dash, no ellipsis, no Uncaught console
  errors; prints measured facts as JSON).

## New support files already written (live now)
- references/qa-panel-laws-l10-l11-2026-08-18.md
- scripts/hub-dom-battery.sh
