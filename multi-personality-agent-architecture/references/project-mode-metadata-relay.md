# Project-mode metadata relay

Session note: when a task is dispatched through delegation, the resolved persona metadata must travel end-to-end, not just live in the prompt.

## Fields to carry
- `brain`
- `project_mode`
- `persona_layers`

## Relay rules
- Resolve top-level metadata first, then allow per-task overrides.
- Inherit missing values from the parent/active personality.
- Normalize `persona_layers` to a string list before storing or displaying.
- Include the resolved metadata in:
  - child system prompt / dispatch brief
  - progress callbacks / event payloads
  - live task-card / agent-card UI state
  - session info payloads

## Verification pattern
- Add a unit test that asserts the child callback receives the resolved metadata.
- Add a store test that persists the metadata into the task-progress model.
- Add a UI display check that renders brain + project mode on the task card subtitle.

## Practical note
Keep the base persona stable; project mode is an overlay, not a new permanent identity.