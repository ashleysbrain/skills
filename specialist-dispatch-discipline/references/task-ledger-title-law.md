# Task-Ledger Title Law + Relabel Mechanics (proven 2026-08-26)

Governance reference for labeling/categorization work on
~/your-org/your-stack/stores/task-ledger.db (the ONLY real ledger —
0-byte decoys exist elsewhere; verify by opening and counting rows).

## Title grammar (canonical, closed)
`SIGNAL: object - difference [qualifier]` ≤80 chars.
Signals (closed 10): BUILD: DEFECT: GAP: IMPROVE: VERIFY: PROBE: DECIDE:
ANSWER: MAINT: SCAN.
Qualifiers (trailing brackets, never primary): [EVOLVE] [NOETHER N3]
[SEC P7] [bus 143] [AUTO] [TRIAGE KEEP] [F7 sev4] [WAVE 1].
References (bus #NNNN, T-XXXX-NNNN, :port, paths, principal quotes) verbatim wherever they land.

## Rewrite engine discipline
- New titles are restructured SUBSTRINGS of old ones (cut at natural boundaries:
  em-dash, colon, semicolon, period-paren) — invention impossible by construction.
- ALWAYS dry-run first: the 2026-08-26 dry-run exposed two engine bugs (detail-swallowing
  archive parser; missed mid-title qualifiers) before any commit.
- Dedupe guard: when disambiguating a flattened cluster, use the DISTINGUISHING TOKEN
  from the detail (organ name, pass name, check id) — NOT the row's trailing seq digits
  (two days can share seq 0220; that discriminator itself collided).
- Unit-test detail rework on the previous round's layout before commit.

## Duplication classes (adjudicate, don't merge blindly)
1. FLATTENED-DISTINCT: N identical titles, N different organs/passes underneath →
   relabel each with its distinguishing token. (12x isomorphism cluster was 12 organs;
   5x THINKERY was architecture/usability/motivation/falsification/creativity passes.)
2. EPOCH DUPES: same organ+check re-minted by a scanning organ days apart → close the
   NEWER epoch, state='done', outcome='dup-of <older> (epoch duplicate...)', event logged.
3. GAP/BUILD DOUBLE-TRACK: same organ open as both GAP and BUILD → close the GAP,
   outcome='addressed-by <BUILD id>' (the build carries the work).
A same-organ label pair appearing twice in the active set is the tell for classes 2/3.

## Archive law (originals are never lost)
Detail tail carries:
  #### ORIGINAL TITLE (archived <date>, verbatim — never edit)
  <original title verbatim>
  #### END ORIGINAL TITLE
Fenced both ends, at the BOTTOM of detail (top placement buried live content under
5K walls). Every relabel event stores sha256(old_title)[:16] as an integrity anchor
(events table is append-only; anchors make archive mutation detectable).

## Mint gate (gates/task_ledger.py submit())
- Hard refuse: title >200 chars ("a title is a label, not a document").
- Advisory (logged to title_shape_log, not blocked): >80 chars OR no ^[A-Z]+[:!]
  signal — automated organs mint in bursts; normalization happens at relabel passes.
- Gate battery must include the FLOW-TAG gate interaction (submit requires flow=
  in tests) and a full-schema in-memory DB (workstream/alias columns are hit).

## Consumer-coupling law
Before folding any vocabulary (DECISION:→DECIDE: etc.), grep all gates/*.py for the
old token — law_state.py queried `title LIKE 'DECISION:%'` and went blind until both
the query and the _title_stem prefix list were patched. Vocabulary lives in queries.

## Verification battery (run after every pass, assert zeros)
active count; COUNT(title>80); COUNT(title NOT GLOB '[A-Z]*:*'); duplicate-title
clusters (GROUP BY title HAVING n>1); unfenced archives (LIKE head NOT LIKE end);
double-signal rows (LIKE 'BUILD: EVOLVE:%'); gap/build overlap by organ.
Keepalive: mints continue during long sessions — re-sweep at the end.

## Residuals filed (not blocking, next sweep)
kind misfiles (doctrine/umbrella/readout/spec-study/daemon as kind=build — kind changes
scheduler physics + GENOME gate, needs taxonomy ruling); zero-info labels needing hand
rewrites; raw bookmark-row intake design; 'legal' lane used but not in taxonomy lanes.
