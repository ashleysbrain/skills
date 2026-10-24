# Fleet target vs active roster note

## Session lesson
In OpenClaw fleet-health rebuilds, the visible active roster can be much smaller than the systems-health fleet the user actually wants.

### Durable rule
- If the user says the fleet is "almost 80", "way more than 22", or similar, check the source dashboard summary first.
- Distinguish:
  - **Active roster**: the currently surfaced command-layer agents
  - **Target-tier fleet**: the larger systems-health group, often the one the user means when asking for the full fleet
- Use the fleet summary counts from the source file as the source of truth for scale.
- Do not silently shrink a rebuild to only the active roster if the user is clearly asking for the broader fleet.

### Rebuild pattern
- Preserve the active roster as a highlighted subset when useful.
- Build the larger fleet artifact separately if the user asks for the almost-80 or systems-health cohort.
- Call out the cohort size explicitly in the artifact header and summary.

### Verification
- Confirm the source count you are using before generating the PDF/HTML.
- Confirm the final artifact title and summary match the intended cohort, not just the visibly active agents.
- If there are multiple relevant cohorts, label them both instead of merging them into one ambiguous roster.