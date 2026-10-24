# principal-Deliverable Ergonomics QA — ADHD Click-Cost (2026-08-20)

Trigger: principal rule stated verbatim mid-panel: "remember i have adhd and need ptions that are as few of clicks as possible... do another thorough qa review with this in mind." This is a FIRST-CLASS QA stage, same rank as falsification and numeric calibration — fold it into `references/adversarial-strategy-gauntlet.md`'s ladder (falsifier → calibrator → **ergonomics** → consolidator) for any plan the principal executes from.

## The mechanical friction audit (execute_code, never by eye)

Audit the deliverable file directly. Metrics that mattered this run:

| Metric | Before | Why it fails the ADHD rule |
|---|---|---|
| Word count | 1,471 (principal path) | Grew +23% in the calibration fold; no appendix split |
| Decision forks | 5 approve/reject pairs (D1–D5) | A choice menu — violates default-plus-veto |
| principal-owned rows in day-1 table | 5 of 5 | Fleet-doable work (paste, pre-fill) labeled principal |
| Numbers/day from principal memory | 6 | Fleet cannot know only ~2 (touches sent, replies) |
| Hands-on verbs (open/paste/confirm/send/mark) | 14 | Each is a click/navigation tax |
| Canonical decision surfaces | 3 stale principal-DAILY-ACTIONS.md copies | "One decision surface" was actually three |

Method snippets that produced these: `re.findall(r"\*\*(D\d) —", text)`, count of "Approve =", table-row greps for owner column, verb-frequency scan, `stat` mtime sweep for sibling daily-files, per-section word split on `^## §`.

## Rules extracted

1. **Every accuracy fold charges a verbosity tax.** The calibration fold (correct numbers in) grew the dossier 1199→1471 words. A fold that adds reference numbers must push them to an appendix IN THE SAME PASS. Set the principal-path budget at fold time (≤900 words here), not as later cleanup.
2. **N approve/reject forks = a choice menu = harm** (see adhd-choice-discipline skill). Collapse §7-style decision sections to ONE approval surface: reply "GO" accepts all locked defaults; single-line overrides ("D4: ARC") veto any one. Exactly ONE thing stays principal-only: the input nobody else has (here: the burn number, 30 min, once).
3. **Ownership audit every action table.** Any row the fleet could do (paste, pre-fill, install, list-build) that is labeled principal-owned is fleet work dressed as principal work. Convert at fold time.
4. **Number-production audit.** For each daily capture field ask "can the fleet know this?" Fields the fleet knows get pre-filled; principal supplies only the ~2 it genuinely cannot (touches actually sent, replies received). Capture = one phone-sendable message <10 s.
5. **Canonical-surface check.** grep/stat for stale siblings of the named single decision surface; name the ONE canonical file in the deliverable, with the stale ones explicitly retired.
6. **Patch-anchor discipline for dossier folds.** Anchor multi-hunk patches on VERBATIM lines from a fresh read. This session: a paraphrased anchor ("§3 price card, append") failed the whole atomic V4A patch after prior edits shifted text — re-read, re-anchor every hunk, atomic retry. The error's own hint output (nearest-section list) is the re-anchor map.
7. **Ergonomics seat = rotated persona, ergonomics-ONLY mandate.** BJ Fogg (behavior design, PhD layering required for the gate) auditing the dossier his earlier seat co-designed worked because the mandate excluded strategy and numbers and required exact replacement blocks as output. The chain operator folds; the seat never edits the dossier.

## Tooling notes (this run)

- **Curator write-gate deadlock confirmed again:** SKILL.md patch refused twice after two fresh skill_view loads ("content has not been loaded in this review turn") — same deadlock documented in `references/revenue-panel-completion-2026-08-20.md`. New-filename support-file writes are unaffected. Existing-file SKILL.md edits need a foreground session; this reference carries the load meanwhile.
- **Specialist-gate 5-min windows expire across an ergonomics audit** (skill load + terminal census + dispatch) — re-route before the fold patches, same as the calibration pass.
- **ADHD rules must ride IN the dispatch brief** (subagents cannot load skills): inline the binding rules — veto-only, 1-tap actions, one canonical file, no walls of text — as a "BINDING RULES" block at the top of the seat's context.

## Fold order for the combined QA (when accuracy + ergonomics land together)

Single pass, same doc: (1) corrected numbers, (2) appendix split to enforce word budget, (3) §7 collapse to GO/override, (4) fleet-ownership rewrites, (5) capture minimum, (6) canonical-file naming. One fold, one re-read to verify, done — never a second parallel document.
