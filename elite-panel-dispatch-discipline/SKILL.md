---
name: elite-panel-dispatch-discipline
description: Dispatch elite panels with approval gates and lane checks.
version: 1.0.0
author: the operator agent Agent
license: MIT
metadata:
  hermes:
    tags: [panels, delegation, dispatch, specialist-integrity, orchestration]
---

# Elite Panel Dispatch Discipline

## When to Use
- Composing any multi-brain specialist panel, advisory board, or expert review for a strategic decision
- Dispatching any single elite specialist micro-task where brain identity, model lane, or persona spec matters
- The user asks to see who is being spun up, asks for panel credentials/bios, or corrects how a panel was dispatched
- Verifying external human partners named by the user before building them into strategy

Dispatch-side rules for elite specialist panels and micro-tasks. Post-task verification lives in `brain-integrity-self-healing-gate` (gate every completed run). This skill governs what happens BEFORE and DURING dispatch.

## 1. Show the panel before firing (approval gate)
Present full seat dossiers — brain, personality-variation mode, credential stack (15+ PhDs), identity (MBTI/OCEAN), model lane — and WAIT for explicit user approval before any dispatch. User correction 2026-08-15: "show me who you're spinning up before you begin the work, and then I'll tell you to move forward."

## 2. Adjunct personas: never fabricate registry codes
Real-person seats not in the ECS registry (Tanenbaum, Tetlock, Kuhn, Amodei, Musk, etc.) dispatch as adjunct personas with credential layering inline. NEVER invent DS-ECS codes for them — fabricated codes were caught in QA (2026-08-15). Verify every code against `agent-organism/ecs.py` FLEET_REGISTRY before presenting. Registry engines cite their real code; adjuncts cite credentials only.

## 3. Lane integrity on dispatch
Elite tasks must run glm-5.3 via delegation config. The silent failure: pool-full (max_concurrent_children) triggers synchronous fallback to a non-elite model with NO dispatch-time error. Raise `delegation.max_concurrent_children` when batching (3 to 6 on 2026-08-15), and gate every completed run post-hoc.

## 4. Web-blocked subagent trap
When web_search is billing-blocked, subagents burn their entire clock retrying it (same_tool_failure_warning x5, 900s timeout). Remedies: (a) dispatch states "web_search is UNAVAILABLE. Do NOT call it. Pure domain reasoning." (b) point at working alternatives: arXiv API via curl, Crossref API, HN Algolia. A timed-out run that already gathered ground truth redispatches cheaply with web calls stripped.

## 5. Sequential after correction
After the user corrects parallel dispatch ("Not in parallel"), run ALL subsequent micro-tasks strictly one-at-a-time: dispatch, wait for landing, gate, next. Do not revert to parallel batching later in the session even for independent tasks.

## 6. QA-review the panel itself
When a panel's output feeds a funding/strategy decision, falsify the PANEL COMPOSITION with a dedicated reviewer brain before convening it (2026-08-15: Popper found 5 unanswerable questions, 2 redundant seats, 1 framing collision in a 9-seat panel). Grade the org's actual assets REAL/THEORETICAL/ASPIRATIONAL (Bridgman operationalism: real = a funder could run the verifying operation themselves) so the panel debates what exists, not what's claimed. Lead funding identity with the asset a funder can independently reproduce; the impressive-sounding but operationally hollow asset is the diligence trap (the OS OS: present as roadmap, never headline).

## 7. User-named external humans: verify live, then deploy
When the user names real academic partners, verify via Crossref/arXiv APIs before building them into strategy — verified publications plus domain match convert "missing academic credibility" gaps into "deployment sequence" plans (2026-08-15: Anantua = EHT black-hole physicist matching the Hamiltonian/Fisher-info scoring math; Alterovitz = Harvard FHIR/Bayesian informatics matching the validation-cohort gap). Store verified profiles in O'Keefe.

## Pitfalls
- Compressing one seat's dossier while others get full depth ("lazy on Andreasen" — user caught it; every seat gets the same depth).
- Parallel dispatch of deliverables the user wants sequential control over.
- Losing a timed-out specialist's gathered ground truth — recover from the live transcript before redispatching.
- QA gates failing compliant runs: when a gate FAILS, manually verify the dispatch spec was present (grep kickoff for identity/temp/PhDs); if it was, patch the gate's matcher, not the workflow.

## Related skills
- `brain-integrity-self-healing-gate` (post-task gate + self-heal loop)
- `agent-delegation-discipline` (general delegation doctrine; user-owned, not editable here)
- `specialist-gate` (pre-action routing enforcement)
