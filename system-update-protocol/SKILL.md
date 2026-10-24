---
name: system-update-protocol
description: Use when updating installed agent systems.
version: 1.0.0
---

# System Update Protocol

Standing law (principal): every installed system stays updated, EVERY time, each via its
correct per-system protocol. Updating is a standing duty, not an on-request task.

## Procedure (per session or when any system misbehaves)
1. **Survey what is installed** before updating anything:
   `for c in hermes sibling-agent claude codex gemini sibling-agent mcporter npm brew; do command -v $c && $c --version; done`
2. **Update each through its own protocol** — never one command for all:
   - hermes: `hermes update` (git install; the `Update available: N commits behind` line in `hermes --version` output shows drift — large drift means overdue). Background it; a multi-thousand-commit pull takes minutes.
   - sibling-agent: check current vs latest from its own release channel, then its upgrade path (version at `~/.local/bin/sibling-agent --version`).
   - claude / codex / gemini / sibling-agent / mcporter: each has its own updater — run `--version`, then the tool's native update command.
   - brew: `brew update && brew outdated`, then upgrade.
   - npm globals: `npm outdated -g`, then upgrade.
3. **Verify version actually moved** by re-running `--version` after each update — an update command exiting 0 is not a version bump.
4. **Restart into the new version cleanly**: updates typically need a service/session restart to take effect; preserve in-flight state first (open orders, owed deliverables) — a restart can cost conversation context.

## Model currency (adjacent but distinct)
- Model version and harness version are independent. Verify the latest model from the
  provider's LIVE `/models` endpoint before assuming a bump is needed — the catalog is
  the ground truth, not announcements.
- A model default pinned in a harness config (e.g. `~/.config/sibling-agent/sibling-agent.jsonc`)
  silently runs every build on the old model. Patch the config, then KILL live runs of that
  harness — running sessions pin the model at start and never pick up the change.

## Pitfalls
- Never apply one system's update procedure to another — git-pull vs native-upgrade
  mismatched procedures break installs.
- Do not update mid-build: an update that restarts a service kills in-flight runs. Sequence
  updates after builds verify, or explicitly hold (the principal may order holding a fix until a
  gated deliverable lands — honor the hold).
- Never claim "everything is updated" from exit codes alone — version re-reads are the receipt.
- App updates break wrapper scripts that exec into the app bundle: an update can move
  config files OUT of the paths the bundled CLI searches. Fix with a writable-dir shim
  (copy the engine + config to a layout the CLI's search paths accept, exec from there),
  never by writing into the SIP-protected `/Applications` bundle. Decode the real search
  paths from the bundle itself (`strings <engine> | grep '<error text>'`, read the adjacent
  path.join list) — the error message names the paths it tried; guessing directory
  permutations wastes runs. macOS BSD grep rejects some regexes with `maximum
  repetition exceeds 255` — when grepping a large bundle, fall back to python `re`
  over the auto-saved terminal-output file instead of re-running the command.
- Verify a fixed wrapper by EXECUTION (`--version` then a real one-shot call), not by
  the error going away — a CLI can clear its config error and still fail later at model
  creation because the shimmed CLI needs its own login that the desktop app session
  does not transfer.
- **A GUI app launched with a live quarantine xattr runs TRANSLOCATED — check the
  process path, not the install path.** `ps` showing
  `/private/var/folders/.../AppTranslocation/<UUID>/d/<App>.app/...` means every
  launch executes from a fresh randomized read-only mount: per-user state
  (~/Library/Containers, WebKit, login/activation) never accumulates, no matter
  how many times the app is relaunched or re-copied (`ditto`/`cp` preserve the
  quarantine bit). `xattr -d com.apple.quarantine` on the bundle fails under
  SIP/TCC — the working de-translocation is the Finder-originated open with its
  one-time Gatekeeper approval (`osascript -e 'tell application "Finder" to
  open POSIX file "/Applications/<App>.app"'`), then verify by `ps` that the
  binary path is `/Applications/<App>.app/Contents/MacOS/...`. Never report an
  app as installed-and-running while its process path still shows AppTranslocation.
