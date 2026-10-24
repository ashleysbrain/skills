# Open-Core Boundary Map

Use this when packaging a domain workflow as a public skill with a premium upgrade path.

## Public / open-source layer
Keep the public skill focused on:
- intake and normalization
- structured summaries
- safe next-step suggestions
- explainable state or trend framing
- templates and checklists
- escalation / triage rules where safety matters
- user-visible workflow steps that create trust

## Premium / hosted layer
Keep these out of the public skill:
- personalized calibration and private weights
- longitudinal memory and cross-session synthesis
- proprietary thresholds, scoring formulas, or interaction rules
- advanced automation and reminders
- richer dashboards and custom reporting
- secret heuristics or moat logic

## Packaging rules
- The main SKILL.md should describe the reusable workflow class.
- Session-specific details, examples, or launch notes belong in `references/`.
- Copy-paste boilerplate belongs in `templates/`.
- Deterministic validation belongs in `scripts/`.
- If a feature feels too specific to one release, do not put it in the umbrella skill body.

## Good test for leakage
If a competitor could reproduce the premium system by reading the public skill alone, the boundary is too thin. The public skill should be useful and credible, but not enough to recreate the moat.
