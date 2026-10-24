---
name: public-skills-publishing
description: "Use when publishing a private skill corpus publicly."
version: 1.0.0
author: the operator agent Agent
license: MIT
metadata:
  hermes:
    tags: [skills, publishing, open-source, sanitization, github, leak-scan]
    category: software-development
---

# Public Skills Publishing

Class: turning a private agent-skill library into a public repo people install
and share (the pstack / mattpocock-skills format) without leaking names,
paths, ports, or secrets.

## When to Use
- Publishing any private skill corpus or excerpt to a public repo
- Sanitizing agent-generated content before public release (the three-law
  gate generalizes beyond skills)
- Building an installable public skill package (npx skills / marketplace form)

## Format leaders (research before building)
- Lauren Tan (poteto) pstack: a real engineer's working agent setup
  open-sourced; viral because it was real, not a tutorial.
- mattpocock/skills: "straight from my .agents directory"; 30-second install
  via `npx skills@latest add <repo> -a <agent>`; versioned releases.
- anthropics/skills + the skills.sh ecosystem (skills donated to the
  Agentic AI Foundation): keep the repo compatible with `npx skills add`.

## Procedure
1. Census the corpus: count SKILL.md dirs; report the REAL total.
2. Score every skill for publishability: regex-count internal refs (personal
   names, home paths, port patterns, org terms, chat ids). Buckets:
   near-clean (<=2 hits), sanitize-able (3-25), org-bound (exclude).
3. Curate via a list file (one dir per line) — the list is the versionable
   review surface.
4. Sanitizer with three mechanical laws: personal names -> role nouns;
   internal paths/ports/org terms -> placeholders; secret patterns (sk-,
   ghp_, gho_, github_pat_, xoxb-, AIza, Bearer) -> hard abort on any
   survivor. Run the text pass twice (pass 2 catches terms pass 1 created).
5. Dry-run, then build. Sanitize references/ and scripts/ subdirs too;
   binary files copy raw.
6. Post-hoc leak scan on the BUILT tree, all file types: secrets, home
   paths, personal names, chat ids. Purge `__pycache__`/`*.pyc` FIRST —
   bytecode caches embed absolute home paths and both leak and false-positive.
7. README: crown-jewels table first (the differentiated skills nobody else
   publishes), craft tier as a compact list, install snippet, a
   sanitizer-included section (publishing the gate is itself a draw), MIT,
   and a provenance paragraph selling "real 24/7 organism; each rule encodes
   a real failure that happened."
8. Ship: git init/commit, `gh repo create <account>/skills --public
   --source=. --push`, then LIVE-VERIFY via `gh api repos/<owner>/<repo>` +
   contents listing. Push success is not repo correctness.

## Pitfalls
- Partial-corpus ships read as half-done: the principal asked for "her skill
  files," saw 32 of 80+ directories, and flagged it as half-ass work. Either
  publish every publishable skill (near-clean + sanitize-able) or state the
  count math and inclusion criteria BEFORE the repo link, with the expansion
  explicitly committed. A "v1 starter set" framing must be sized against the
  full corpus out loud.
- Bytecode leaks: `__pycache__/*.pyc` copied from the source corpus carry
  absolute paths; exclude them from public trees and grep them anyway.
- Never hand-edit sanitized output for style — fix the sanitizer map and
  rebuild, or the public tree diverges from the gate that verified it.
- Check the build log for SKIP lines: renamed/missing curated dirs are
  skipped silently; the published count must match the curated list.

## Verification
- leak scan returns zero hits on the built tree
- published dir count == curated list count (no silent SKIPs)
- live repo check via API: visibility public, default branch, contents match
- README claims match the tree (every named skill exists as a dir)

## Related
- skill-library-curation (private library shape)
- sensitive-data-containment (scrubbing leaked data after the fact)
