# Private overlay repo pattern

Use this pattern when the user wants a private repo that mirrors or extends a shared/original repo without overwriting it.

## Core rules
- Create a *separate private repo* for the overlay.
- Keep the shared/original repo untouched unless explicitly asked.
- Store each logical item in its own file so changes stay diffable.
- Maintain a machine-readable manifest that points to the item files.
- Add a README that explains the repo is private/overlay-only.
- Add a short process doc when the workflow itself matters.

## Recommended structure
- `README.md` — purpose and guardrails
- `manifest.yaml` — stable IDs, ordering, file paths, status
- `items/*.md` or `coaches/*.md` — one item per file
- `PROCESS.md` — how to extend safely

## Creation flow
1. Verify the target checkout and current remote.
2. Write files in the private overlay repo only.
3. Commit locally.
4. Create or attach a private GitHub repo.
5. Push to the private remote.
6. Verify `git status` is clean and the remote repo is private.

## Pitfalls
- Do not reuse the shared repo as the overlay container.
- Do not bury multiple logical items in one file if they will be edited independently.
- Keep stable IDs in the manifest so later additions do not renumber or confuse existing entries.
