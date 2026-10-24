# Private overlay repo pattern

Use this pattern when the user wants a *private* repo for a derived or user-specific variant, but there is also a shared/original repo that must remain untouched.

## Goals
- Keep the shared/original repo stable.
- Put user-specific work in a separate private repository.
- Make the repo easy to extend without confusion.
- Ensure future edits happen in the overlay repo only unless explicitly requested.

## Recommended layout
- `README.md` — human entry point and scope statement
- `manifest.yaml` — machine-readable roster / ordering / stable IDs
- `items/` or `coaches/` — one file per entity

## Practical conventions
- Use stable IDs in the manifest (`coach_id`, `item_id`, etc.).
- Keep one concept per file to preserve clean diffs.
- Avoid merging the overlay back into the shared repo.
- State the repo scope clearly in the README.
- If the shared repo also has a similar concept, keep naming distinct (e.g. `private`, `overlay`, `principal-only`).

## Verification checklist
1. Confirm the target repo with `git status --short --branch`.
2. Confirm remotes with `git remote -v`.
3. Confirm the overlay repo URL after creation.
4. Push only the overlay repo branch.
5. Re-check `git status` to verify tracking is clean.

## Example manifest shape
```yaml
policy:
  overlay_only: true
  do_not_modify_shared_repo: true
  one_file_per_item: true
items:
  - item_id: example-1
    name: Example Item
    status: active
    file: items/example-1.md
```
