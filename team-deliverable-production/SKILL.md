---
name: team-deliverable-production
description: Use when a document ships to a teammate or external.
version: 1.0.0
author: the operator agent
license: MIT
metadata:
  hermes:
    tags: [qa, deliverables, writing, gauntlet, review]
    category: operations
---

# Team Deliverable Production

Any document handed to a human teammate, the principal, or an external party is a
DELIVERABLE, not an internal note. Deliverables get three treatments internal
notes never need: rotated-brain QA, leak-scrubbing, and (increasingly) a
briefing layer for the reader's own AI agents.

## When to use
- A teammate (designer, CTO, partner) needs a grounding/briefing/resource document
- A principal-facing explainer, summary, or translation of technical work
- Any document that will be copied into another person's tools (Notion, Perplexity, Figma)

## The three layers

### 1. Rotated-brain QA gauntlet (never one pass, never one brain)
Sequential review passes by DIFFERENT specialist brains catch disjoint defect
classes; a repeated brain catches repeats. Validated 2026-08-20: four passes,
26 defects, zero fabrication shipped. Schedule + full dispatch contract:
`references/document-qa-gauntlet.md`.

Core sequence (adapt names to the org's specialist roster):
1. Falsifier: verify EVERY factual claim against named sources; returns exact
   replacement wording per defect
2. Domain expert (physics/math/etc.): accuracy at the target simplification
   level; simplification wanted, errors not
3. Meta-reviewer: independent re-verification (do NOT trust prior passes),
   readability, completeness-for-reader, cross-section consistency
4. Voice/register reviewer: speaks TO the named reader, no internal-speak, and
   the final leak hunt

Dispatch contract per pass: read-only mandate; named source files; numbered
checks; require verdict + numbered defects + exact replacement wording. Fold
all findings into one new version, then run mechanical scans (banned
punctuation/phrases; em dashes outside math notation).

### 2. Leak-scrubbing (operational metadata never ships)
principal rule (2026-08-20): internal tooling problems never appear in team-facing
deliverables; work around them silently. The deliverable reads as if
everything was always easy. Scrub before delivery: internal tooling names and
outage states, workaround narratives, census plumbing ("17/20 verified", HTTP
codes), DB IDs and finding numbers, QA-pass bookkeeping. Limits are declared
as product facts ("still to verify: X"), never as incident reports.
Run-record lives in the task ledger, not the document.

### 3. Briefing the reader's own AI agents
Teammates run agentic systems (Perplexity Projects, Figma Design Agent, Notion
custom agents) against documents you hand them. Include:
- ONE paste-ready canonical context block: what the project is in a few
  sentences, the hard rules (claims that must not be made, visual cliches,
  palette, approvals). Must be self-contained and accurate to the body.
- Per-tool setup notes: what the tool is FOR, setup steps, concrete first
  prompts, honest limits, and a one-line division of labor.
Worked example (poster-project context block + Perplexity/Figma/Notion
briefing): `references/agentic-tool-briefing.md`.

## Pitfalls
- One QA pass by the drafting brain is generalist drift; the gauntlet needs
  different brains, and pass N+1 must re-verify independently
- Reviewers must return exact replacement wording, or folding becomes
  re-writing and introduces new defects
- The most common ship-blocker is not factual error but leak residue; grep the
  final text for internal terms mechanically, do not eyeball
- Version the footer's QA history (which passes, folded when) so provenance
  travels with the document
- PDF render is explicit-request-only; deliver in chat/files until the user
  says render

## Verification
- Every checkable claim traces to a source line (falsifier pass table)
- Mechanical scans return zero hits (banned terms, em dashes, leak terms)
- Context block cross-checked against the body by the voice pass
- Ledger task closed with run-record citing each pass (delegation ID, duration)
