---
name: global-term-rename-sweep
description: Workspace-wide identity rename sweep, multi-pass, verified.
tags: [rename, refactor, identity, codebase, provenance]
version: 1.0.0
author: the operator agent Agent
license: MIT
provenance: agent
metadata:
  hermes:
    tags: [rename, refactor, identity, codebase, provenance]
    related_skills: []
---

# Global canonical-term rename sweep

## When to Use
- A canonical identity term (agent/organism/product name) must change across the ENTIRE live workspace — source trees, configs, and databases — not just one document
- The rename must land before a deadline (another operator going live, a launch, a public reveal) and the user expects multiple passes
- A previous rename pass left residuals (strict-decode skips, database rows, generator-emitted old terms)
- Do NOT use for a single document/package rename — that is `document-debranding-and-link-sanitization` territory (package scope, user-owned); this skill covers fleet scope.

The core situation: a name change must land everywhere live BEFORE a deadline, and the user has said it will take multiple passes, because it will.

## Procedure

1. **Discovery pass, zero writes.** Walk the roots with `os.walk`, skip volatile dirs (`.git`, `node_modules`, `__pycache__`, delegation/session caches, logs, venvs), cap file size (~2-3 MB), and count word-boundary occurrences of ALL case variants per file. Dump the hit map to a scratch JSON. Print: counts by root, top 25 files, total. This sizes the job and exposes the noise before anything is touched. Time-box the walk — a whole-home scan can exceed 120 s; scope roots explicitly.
2. **Classify live vs frozen BEFORE writing.** Frozen-history paths — `/backups/`, archives, audit snapshots, timestamped payload dirs, `*.bak*`, session dumps — are EXEMPT: rewriting them falsifies what was true at the time. Record the exemption as a receipt (file count + occurrence count) so the boundary is deliberate and auditable. Typical split: the majority of raw hits live in frozen history; the live set is the real target.
3. **Pass 1 — bulk strike, backup-first.** Create a timestamped backup dir; for every file about to be written, copy the original in FIRST (flat name with path separators encoded) and append to a manifest `{path, replaced}`. Then substitute word-boundary regex, all case variants, strict UTF-8 read/write.
4. **Pass 2 — encoding-tolerant re-sweep of the SAME set.** Strict decode silently skipped some files (that is why pass 1's count is low, not because they were clean). Re-read as bytes, decode `surrogateescape`, substitute, write back the same mode. This pass always finds stragglers — plan it, don't hope pass 1 was complete.
5. **Pass 3 — databases.** File sweeps cannot touch rows. Enumerate live `.db`/`.sqlite` files (frozen dirs excluded), scan read-only for the term, then targeted UPDATE on the specific columns that carry identity (e.g. `claimed_by`) — never a blanket replace across all tables. Row-level scans over big stores can blow a foreground timeout; spot-check the identity-bearing columns first and background the full sweep if needed.
6. **Verify after EACH pass, not only at the end.** Re-scan the live set, require residual zero, print any STILL hits WITH surrounding context so anything left is a visible decision.
7. **Sweep the surfaces files can't reach.** Harness configs, running processes (`ps aux | grep -i <term>`), ledger claim columns, symlinked trees the patch tool refuses, env files.
8. **State the re-sweep trigger in the close-out.** Templates, crons, and generators can still emit the old term into NEW files; a rename landing mid-flight needs another pass by construction. Close with the follow-ups owed, not with "done".

## Pitfalls
- Word-boundary or nothing: substring replace corrupts identifiers, file names, and unrelated words that merely contain the term.
- Never rewrite frozen history — exempt it with a receipt instead of silently ignoring it.
- A clean file sweep is NOT a clean rename until the db pass and the process/config checks have run.
- Report per-pass replacement counts; monotone decreasing counts across passes is the health signal, and a pass-2 count of zero usually means pass 2 skipped the same files, not that pass 1 was perfect.
- Single-file revertibility is the safety net — the backup manifest must map every written file to its pristine copy before you claim any replacement count.
