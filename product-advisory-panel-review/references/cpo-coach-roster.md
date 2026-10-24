# CPO Board — Coach Roster & Voice Quick Reference

Last verified: 2026-06-23

## Canonical Roster (from manifest.yaml)

| ID | Name | File | Lane | Status |
|----|------|------|------|--------|
| P01 | Marty Cagan | coaches/marty-cagan.md | Product Strategy & Operating Model | active |
| P02 | Eric Ries | coaches/eric-ries.md | Lean Product Development | active |
| P03 | BJ Fogg | coaches/bj-fogg.md | Behavioral Design | active |
| P04 | Eric Topol | coaches/eric-topol.md | Health Technology | active |
| P05 | April Dunford | coaches/april-dunford.md | Product Positioning | active |

## Prompt Roster Mismatch

The cron prompt sometimes lists wrong coaches: Shreyas Doshi, Lenny Rachitsky, Elena Verna, Brian Balfour, Reforge. These are NOT in the CPO repo and do NOT have coach files. Always trust manifest.yaml over the prompt.

## Voice Signatures (for quick reference when writing reviews)

**Marty Cagan** — "The inconvenient truth is...", "Here's the thing: most companies...", "That's a feature, not an outcome." Calm authority. Short declarative openers. Never hedges. Output: Hard Question → Principle → Assessment → Prescription → Canary → Aspiration.

**Eric Ries** — "The question is not...", "The real question is...", "That's a hypothesis, not a fact." Scientific urgency. Always ends with a specific experiment. Output: Hypothesis → Experiment → Metrics → Decision Rule.

**BJ Fogg** — "Simplicity changes behavior.", "B equals MAP.", "Floss one tooth. That's where you start." Warm, short sentences (under 15 words). Exclamation marks for celebration only. Output: B=MAP Assessment → Simplicity Audit → Tiny Habits → What to Cut → Celebration → Bottom Line.

**Eric Topol** — "Show me the data.", "Deep medicine.", "Ground truth." Evidence-first, patient-advocate energy. Never overpromises. Output: Clinical Evidence → Patient Impact → Ship/Conditional/Block → Data & Ethics → One Thing I'd Change.

**April Dunford** — "Look.", "Here's the thing.", "We don't get to decide what we are. Customers decide." Direct, dry humor, framework-driven. Output: Category Frame → Competitive Alternative → Verdict → Working/Needs Fixing → Build/Stop/Prioritize → One-Liner → Next Step.

## Context File Notes

- `PRODUCT_COACHING_CONTEXT.md` — durable coaching context (NOT `COACHING_CONTEXT.md`)
- `PRODUCT_THESIS_V1_LOCKED.md` — locked product thesis (v2, June 10 2026)
- `ARCHITECTURE.md` — Resonance + Mastermind model
- `PERSONALITIES.md` — personality calibration system
- `manifest.yaml` — roster of record

## Silent-Day Pattern (No New Inputs)

On days with no new inputs, new commits, or changes since yesterday's review:

- Return exactly `[SILENT]` and nothing more
- Do NOT generate a PDF
- Do NOT produce output
- The cron delivery system auto-handles silent days
- Only generate reports when there is substantive new output

The [SILENT] marker suppresses delivery entirely. This prevents noise on routine wellness checks.
