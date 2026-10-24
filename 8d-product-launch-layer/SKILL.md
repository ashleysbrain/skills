---
name: 8d-product-launch-layer
description: Use when launching the 8D agent as an actual ship-ready skill package with a Source / Engine / Release / Vault stack and strict baseline-preservation rules.
version: 1.1.2
author: the operator agent Agent
license: MIT
metadata:
  hermes:
    tags: [health, 8d, source, engine, release, vault, baseline, product, launch]
    related_skills: [product-immune-system, 8d-pattern-awareness, 8d-snapshot-report, open-core-skill-architecture, baseline-first-surgical-precision]
---

# 8D Product Launch Layer

## Overview

Use this skill when you are launching the 8D agent itself — not drafting a product spec about it.

This is the operational launch skill for the 8D family. It takes the existing 8D Source and Engine layers and turns them into a shippable agent package with:
- a stable Release surface
- a clearly hidden Vault
- explicit baseline-preservation rules
- a release artifact the user can actually open and use
- a working demo path when the user wants to feel the flow end-to-end (intake → awareness → snapshot → quick wins → upgrade path)

The skill is intentionally additive. It does not replace the core 8D skills. It wraps them into a product-ready launch shape while preserving exact user-provided content unless a surgical change is required for function.

## When to Use

Use this skill when the user wants to:
- launch the 8D agent as a real reusable skill
- turn the existing Source + Engine stack into a releaseable product
- define the actual launch behavior of the agent they are creating
- keep the Release layer useful while hiding the Vault
- ship a versioned skill package instead of a loose design note
- verify that the release artifact is real, current, and attached

Do **not** use this skill when the user wants only:
- a one-off health note interpretation
- a generic product strategy memo
- a purely visual mockup with no runtime behavior
- a rewrite of the baseline 8D skills themselves

## Core Promise

> Launch the 8D agent as a real skill package: keep the Release workflow useful, keep the Vault private, and preserve the baseline exactly unless a surgical change is necessary.

## What This Skill Actually Produces

The output of this skill is not a concept doc.
It is a launchable skill package that defines:
- the Source / Engine / Release / Vault map
- the public input/output contract
- the hidden Vault boundary
- the release version and identity
- the acceptance criteria for shipping
- the actual artifact the user can receive

## Source

The Source layer is the raw input and baseline material.
It includes:
- intake
- notes
- transcripts
- observations
- historical baseline content

The Source layer is useful on its own because it preserves what came in without distortion.

## Engine

The Engine layer is the core 8D logic.
It handles:
- 8D awareness mapping
- baseline-aware snapshotting
- confidence handling
- safe next-step framing
- non-diagnostic interpretation

The Engine must stay stable and readable.

## Release Surface

The Release layer is the part of the product that is safe and useful on its own.
It should do three things well:

1. **Make the result understandable**
   - explain what the user is looking at
   - state what changed
   - summarize the strongest signal(s)

2. **Make the result usable**
   - frame one or two quick wins
   - show a clean next step
   - keep the handoff compact and readable

3. **Make the result reviewable**
   - include a confidence statement
   - separate facts from interpretation
   - preserve the baseline wording when precision matters

The Release surface should handle:
- product framing
- quick-win framing
- a clear confidence statement
- concise human-readable delivery
- a stable handoff format
- an explicit boundary note when deeper logic exists

The Release surface must not expose:
- private scoring formulas
- hidden weights or thresholds
- longitudinal calibration logic
- proprietary decision rules
- internal routing details that are not needed by the user
- raw telemetry or internal debugging artifacts

If the public output cannot stand on its own without private context, the Release surface is too thin and needs another pass.

## Vault

Keep the Vault private and separate.
It may include:
- richer scoring and calibration
- deeper longitudinal memory
- personalized threshold tuning
- automation hooks
- internal release telemetry
- premium-only review or synthesis logic
- private validation notes or operator-only exceptions

The Vault is a boundary, not a section of the public deliverable.
When the user asks for the public skill, the Vault can be referenced only as a hidden layer or upgrade boundary — never described in enough detail to recreate it.

Rule of thumb:
- if the user needs it to understand or use the public release, it belongs in Release
- if the user does not need it and it would reveal how the system really works, it belongs in Vault

## Launch Contract

Every launch should satisfy this contract:

1. **Input**
   - Existing Source and Engine artifacts
   - Current user goal
   - Any release constraints
   - Any required artifact path or delivery target
   - Any exact wording that must be preserved
   - Any existing file names or references that must stay aligned

2. **Processing**
   - Preserve the baseline
   - Map the stack clearly
   - Keep Vault logic private
   - Package the release as an actual skill
   - Validate that the artifact is real
   - Prefer surgical edits over broad rewrites
   - Move dense detail into references when the main file starts to get crowded
   - Keep the release language consistent across titles, headings, and attachments
   - When the user says the product has launched, treat that as first-class evidence, and reflect it explicitly in the review, scorecard, and release language instead of describing the work as if it is still only a concept or draft

3. **Output**
   - A launch-ready skill package
   - A clear Release identity
   - A compact handoff artifact when requested
   - A verified file path or attachment the user can open
   - A readable boundary statement
   - A final artifact that matches the naming used in the file list
   - If product launch evidence is present, an explicit launch-recognition section or sentence so the milestone is impossible to miss

4. **Verification**
   - the file exists at the expected path
   - the old label is gone from current titles and references unless intentionally preserved
   - shipped product evidence is called out directly in the visible review, not implied or buried in a footnote
   4. **Launch a concept instead of a concrete artifact**
      - Fix: make the skill package itself real, readable, and attached.

   5. **Renaming a product line without preserving scope boundaries**
      - Fix: keep product-line naming confined to the intended surface; do not propagate it into fleet, ops, or archive docs unless the file is explicitly part of the product surface.

   6. **Leaving duplicate labels after a rename pass**
      - Fix: audit titles, headings, filenames, and references in the same pass so stale suffixes like `Name (Name)` are removed everywhere they appear in-scope.

   7. **Forgetting the user asked to feel the runtime flow**
      - Fix: include a compact demo run that shows the path from intake through awareness and snapshot to quick wins and upgrade path.

   ## Launch Flow

### 1. Anchor the baseline
Start from the approved Source and Engine skills.
Do not reconstruct them from memory.
Do not generalize away exact user data.
Do not widen scope unless it is required for the launch to function.
If the baseline file is unclear, re-read it before editing anything else.

### 2. Define the stack boundary
State clearly:
- what the Source is
- what the Engine does
- what the Release presents
- what the Vault hides
Write the boundary in plain language first, then tighten it into the final artifact.

### 3. Package the runtime behavior
Describe the actual launch behavior in operational terms:
- how inputs enter
- how the public review is produced
- how quick wins are framed
- how the upgrade path is positioned
- how confidence and uncertainty are shown
- what the user receives at the end
- what the release intentionally leaves out

### 4. Preserve release hygiene
Keep the package versioned and stable.
Keep references for detailed launch notes, examples, and acceptance checks.
Keep the main SKILL.md focused on the reusable launch workflow.
Keep filenames, headings, and references synchronized in the same pass.

### 5. Verify the artifact
Before handing it over:
- confirm the file exists
- confirm the content reflects the actual launch skill
- confirm the Release surface is useful on its own
- confirm the Vault is not exposed
- confirm the baseline has not been accidentally rewritten
- confirm the updated filenames are the ones referenced in SKILL.md
- confirm any renamed companion files no longer appear under old labels

### 6. Deliver the actual file
If the user asked to see the launch skill, deliver the actual artifact path or attachment.
Do not stop at a description of what the skill would be.
If there are multiple artifacts, label which one is the main skill and which are support references.

## Behavioral Rules

- Be precise.
- Be additive.
- Preserve exact wording when it matters.
- Make only surgical changes.
- Do not turn a launch pass into a redesign pass.
- Do not expose private scoring logic in the public layer.
- Do not generalize a concrete user input into a bland abstraction.
- Do not claim the artifact is ready until it has actually been written and verified.

## Output Shape

When this skill is used to create or revise a launch package, the final handoff should include:
- release identity
- public promise
- open-core boundary
- premium boundary
- actual artifact path or attachment
- verification note

## Delivery and Resend Rules

When the user asks to "update and send these again" or points to a screenshot of named attachment files:
- treat the named attachment files as the source of truth
- update the actual artifact files first
- verify the updated file contents before sending
- send the real files with `MEDIA:/absolute/path/to/file`
- if Telegram has no home channel configured, list targets first and send to an explicit target
- do not substitute a summary or pointer when the user wants the files themselves

Reference: `references/telegram-artifact-resend.md`

- a short note stating whether the package is the skill itself or a supporting release document

If the user wants the skill itself, send the skill file.
If the user wants the launch package, send the launch package.
If the user wants both, keep them separate and label them clearly.
If the user asked for a thoroughness pass, prefer a slightly richer handoff over a terse one — but keep it readable.

## Common Patterns

### Pattern A: launch wrapper
Use when the existing 8D stack already works and needs a product layer on top.
This pattern is for cases where the core intelligence is stable, but the user experience needs a cleaner public surface, stronger naming, and a clearer handoff.

### Pattern B: Source / Engine / Release / Vault packaging
Use when the user wants public usefulness without revealing the Vault.
This is the default pattern for the 8D family because it preserves the working baseline while still giving the release a real moat.

### Pattern C: baseline-preserving version bump
Use when the existing skills are approved and only the release framing should change.
Use it when the underlying logic should remain stable, but the naming, output shape, or shipping story needs to be more explicit.

### Pattern D: release-document cleanup
Use when the files are already functionally correct but the labels, filenames, or references are inconsistent.
This pattern is about coherence: one package, one naming system, no stale labels.

## Common Pitfalls

1. **Writing a product spec instead of a launchable skill**
   - Fix: define the runtime behavior, not just the vision.

2. **Replacing the baseline**
   - Fix: keep the Source and Engine skills intact.

3. **Exposing the Vault**
   - Fix: keep calibration and private scoring out of the Release surface.

4. **Generalizing exact user data**
   - Fix: preserve the user’s exact wording unless surgery is required.

5. **Missing the launch milestone language**
   - Fix: if the user says the product is launched, shipped, or live, say so explicitly and frame it as a major readiness transition, not a minor implementation detail. If the launch surface is now real, call out what became live and how that changes product status.

6. **Handing over a pointer instead of the actual artifact**
   - Fix: create the file, verify it, then attach or name the exact path.

7. **Treating a draft as a release**
   - Fix: confirm the skill package is written and reviewable before saying it is launched.

8. **Letting references drift away from the main skill**
   - Fix: keep the public contract in SKILL.md and move detail into references.

9. **Making the main file too thin**
   - Fix: if the release behavior, boundary, or verification is still ambiguous, add the missing operational detail rather than leaving it implicit.

10. **Renaming only part of the package**
    - Fix: update the file contents, filenames, references, and visible headings in the same pass.

Reference: `references/launch-milestone-callout.md`

## Verification Checklist

### Skill Package Verification
- [ ] The file describes a launchable skill, not a product spec
- [ ] The Release surface is useful on its own
- [ ] The Vault is private
- [ ] The Source and Engine skills remain intact
- [ ] Exact user data is preserved unless a surgical change is required
- [ ] The release artifact exists and is attached or pathable
- [ ] The skill can be used as the actual launch layer for the agent we are creating
- [ ] The package is readable, shippable, and versioned
- [ ] The filenames match the references in the file
- [ ] No stale V1/V2 labels remain unless intentionally preserved for historical context
- [ ] The output tells the user what changed and what stayed the same
- [ ] The package can be understood without opening the hidden Vault

### Software Product Verification (when the 8D product includes runnable code)
- [ ] `npm run build` / `cargo build` / `go build` (or equivalent) passes clean
- [ ] Test suite passes (`npm test` / `pytest` / equivalent)
- [ ] CI pipeline exists and is green on main
- [ ] Repo is under version control with a remote (GitHub)
- [ ] No secrets or credentials in the codebase or git history
- [ ] Dev server working is NOT sufficient proof of health (Vite hot-reload masks type errors; always run the production build)

If any software product check fails, the product is NOT launched regardless of how complete the skill package is. Use the `product-immune-system` skill for the full birth quality gate.

## References

- `references/stack-terminology.md` — plain-English layer names
- `references/release-layer-spec.md` — explanatory launch note
- `references/review-package-delivery.md` — delivery and boundary note
- `references/v2-demo-run.md` — sample intake → awareness → snapshot → quick wins → upgrade-path run
- `references/launch-milestone-callout.md` — launch milestone language and readiness transitions
- `references/telegram-artifact-resend.md` — Telegram artifact resend pattern
- `references/publishable-release-package.md` — publishable release package shape
- `references/launch-vs-spec.md` — launch skill vs spec distinction
- `attachments/8d-product-launch-layer-deep-spec.txt` — deep behavioral detail for the release pass
- `attachments/8d-product-launch-layer-release-package.txt` — release package attachment
- `attachments/8d-product-launch-layer-SKILL.txt` — SKILL file attachment
- `attachments/8d-product-launch-layer-review-package.txt` — review package attachment
- `attachments/8d-product-launch-layer-preview.txt` — preview attachment
- `attachments/8d-product-launch-layer-preview.md` — preview attachment (Markdown)
- `attachments/8d-product-launch-layer-review-package.md` — review package attachment (Markdown)

## Release Note

This is the operational launch skill for the 8D agent family. It is meant to ship as the agent's public-facing skill wrapper, not as a product strategy memo.

## Release Identity
- `8D Product Launch Layer — ops — v1.1.2 — 2026-06-08`
- Public role: operational launch wrapper for the 8D skill family
- Public promise: turn the existing Source + Engine stack into a versioned, shippable agent package with a clean Release surface and a hidden Vault
