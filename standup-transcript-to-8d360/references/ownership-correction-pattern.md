# Ownership correction pattern for mixed standup notes

When processing a mixed standup / voice-note transcript:
- Do not assume numbered items belong to the user just because they appear in the transcript.
- If the user later corrects ownership (e.g. "items 1 through 4 are not mine"), discard those items and rebuild the task list from scratch using only the confirmed user-owned items.
- Treat ownership corrections as hard boundaries, not soft hints.
- If ownership is unclear, pause and ask or leave the item unassigned instead of guessing.
- In the final task list, separate:
  - user-owned tasks
  - other-speaker tasks
  - shared/system tasks
- Never preserve an earlier misattribution in the revised list just for continuity.