---
name: engine-credential-layering
category: software-development
description: Use when seating PhD credential layers on DS engines.
tags: [engines, credentials, methodology, citations, count-not-names, ds-organism]
version: 1.0.0
author: the operator agent Agent
license: MIT
provenance: agent
metadata:
  hermes:
    tags: [engines, credentials, methodology, citations, count-not-names, ds-organism]
    related_skills: [ds-organism-seat-and-register, ds-agent-creation-protocol, thalamocortical-specialist-architecture, mosaic-ledger-mint-close]
---

# Engine Credential Layering

Governs how a DS engine or flagship agent gets its credential stack and methodology layer — the PhD-council / doctorates / certifications layer of a build. The single most common defect: conflating the engine's own credentials with the humans whose methodologies it borrows.

## When to Use
- Building or extending an engine's L1 council, credential stack, or methodology layer
- A principal order references PhD counts ("at least 15 PhDs like the others")
- Auditing an engine's pedigree before a review or fleet sweep
- Serving a `/pedigree` endpoint or writing pedigree contract tests

## The two halves (never conflated)

1. **Engine-own credentials.** The ENGINE holds its own doctorates (DSc/PhD) and certifications, each conferred by the organism on demonstrated shipped work, with the conferral basis written inline at the credential. Serve the stack live on a `/pedigree` endpoint so it is inspectable without reading source.
2. **Methodology donors.** Famous humans donate methodology ONLY — zero prestige transfer. A council of named humans with no engine-own credential stack is the exact defect shape: it measures the engine against other humans instead of against credentials. The contract battery must include a borrowed-human test that FAILS the battery when a human name appears inside the engine's own credential stack.

## The 15-PhD standard, operationalized

"15+ PhDs" counts DISTINCT PERSONS, not citation pairs: at least 15 distinct scientists, each attached to at least one real citation in the form `Author (Year). Title. Journal/Publisher.`, each grounding a methodology the engine ACTUALLY RUNS. The fleet reference layer itself carries 15 scientist-paper pairs across fewer distinct persons (repeat authors with multiple papers) — pairs are the floor the measurement finds, distinct persons is the bar that ships; never report a 15-pair/9-person stack as compliant. It does not mean 15 names pasted into a council list, and not uncited methodology (uncited = template filler).

- Reference pattern: the fleet's best existing methodology layer — cited scientist-paper pairs grouped by institution, each institution with key_papers, built on the shared methodology_base (Institution / MethodologyProfile / FunctionalMode / ModelRoute).
- Addendum pattern for flagships that already exist: `src/methodology_papers.py` exporting `SCIENTIST_PAPERS` (list of citation strings) + `summary()` — additive, imports nothing from existing layers, touches no existing test.

## Procedure
1. **MEASURE the fleet reference first.** "Like the others" orders mean: find the fleet's best existing implementation of the thing being ordered, programmatically count what makes it the standard, and mirror that pattern exactly. Never guess the bar — it is the fleet's own best pattern, and it moves.
2. **Map every methodology the engine runs to its scientist + paper.** A methodology that cannot name its source is either grounded or cut — no orphan methodology, no citation decoration for physics the engine does not execute.
3. **Write credentials (engine-own) and papers (donor methodology) as additive modules.** Stack not attack: do not edit existing layers, pins, or tests — additive means additive; rewriting an existing layer silently breaks sibling contract suites that were left green on purpose.
4. **Verify programmatically:** assert pair count and distinct-scientist count are each at the standard; regex every entry for `(YYYY).` plus a journal/publisher token; run the engine's full contract battery AND the sibling engine's — both must stay green.
5. **Restart the server if credentials are served live**; curl `/pedigree` and `/health` to confirm.
6. **Close with ledger proof:** file anchors, command output excerpts, and exit codes inline in the outcome.

## Pitfalls
- Uncited methodology is template filler — reviewers count pairs, not adjectives.
- A hand-counted "looks like 15" is how a 9-entry layer ships as compliant — verify with code.
- One-file sketch engines get rejected at review; build the full layer set (identity seed / council / modulation / objective core / adaptive shell / dispatch log) with per-layer contract tests the first time. Full depth only — no half-built flagships.
- Ledger titles must not carry port digits — the port-collision gate scans titles too and rejects the mint.
- Every engine, agent, and action runs on the OS-selected elite stack — standing fleet law; never a single-vendor default and never a downgrade beyond minute-tier work.

## Overlap notes
- `ds-organism-engine-creation`, `ds-agent-creation-protocol`, and `thalamocortical-specialist-architecture` cover adjacent territory (engine architecture, agent creation, the 5-layer blueprint) but this class — credential/methodology layering to the citation standard — lives here.
- `mosaic-ledger-mint-close` governs the ledger close that follows a credential build (proof classes, port-collision gate).
