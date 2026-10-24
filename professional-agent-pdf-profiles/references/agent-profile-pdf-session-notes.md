# Agent Profile PDF Session Notes

This reference captures lessons learned while delivering a complete agent-profile PDF.

## Durable lessons
- Full profile PDFs should include explicit professional and educational credential sections.
- If the user says agents should not run on Anthropic models, update the profile source *and* the DB-backed model fields before rendering.
- When credentials are not real external degrees, label them as internal / role-relevant / auditable rather than inventing institutions.
- Verify the final PDF text layer contains the model line, credential sections, and the completed variation registry.

## Verification checklist
- Profile markdown has no Anthropic model references when non-Anthropic policy is requested.
- Professional credentials section is present.
- Educational credentials section is present.
- PDF renders with sensible page count and non-trivial size.
- The final file is the one delivered to the user.
