---
name: harness-cli-headless-diagnosis
description: Use when an external agent CLI fails headless.
version: 1.0.0
---

# Harness CLI Headless Diagnosis

Class-level skill for external agent CLIs in the fleet (zcode, grok,
sibling-agent, sibling-agent). Two laws drive it:

1. **Verify-before-ask**: never tell the user a login/setup step is needed
   until on-disk artifacts prove it. Credentials that exist on disk with a
   healthy sibling process running on them = login DONE; a CLI failure after
   that is a CLI defect, not a user action item. Reporting a CLI symptom as a
   user ask is a false-work claim the user will correctly reject.
2. **Wrapper errors are not causes**: a printed error like "Model creation
   failed (traceId ...)" is a wrapper; the actionable message is nested in the
   CLI's structured log. Diagnose from the log, not the stdout line.

## Procedure

1. **Locate the credential store and read it for PRESENCE, never values.**
   zcode: `~/.zcode/v2/credentials.json` (values are `enc:v1:`-prefixed
   encrypted blobs — print key names, lengths, mtimes only). File mtime =
   when login state was last written; compare it against the user's claim of
   when they logged in before contradicting them.
2. **Corroborate with the sibling desktop app.** Many CLIs share credentials
   with a desktop app (zcode: `~/Library/Application Support/ZCode`, logs at
   `~/.zcode/v2/logs/<date>.log`). A desktop app alive with healthy
   heartbeats and successful RPC calls proves the shared auth works — the
   defect is then isolated to the CLI path.
3. **Parse the CLI's structured log for the nested cause.** zcode:
   `~/.zcode/cli/log/zcode-<YYYY-MM-DD>.jsonl` — load with a small JSON pass
   (not grep; nesting survives quoting only in parsed form), find the last
   `turn.failed` entry, read `error.cause.message` and `context.turnPhase`.
   `turnPhase: model_creation` means it died BEFORE touching credentials —
   an auth-independent configuration gap (observed live: "Select a model
   before continuing", CONFIGURATION_ERROR, while OAuth tokens were valid
   and the desktop app ran fine on them).
4. **Classify before proposing any fix:**
   - Auth gap (no credential file / expired / 401 from the provider with a
     known-good key) → the only class that justifies a user ask.
   - Configuration gap (no default model, stale settings) → CLI-side fix.
   - Bundled-resource path bug → check for an existing shim before writing
     one (zcode ships `~/.local/bin/zcode-fixed` for its provider-config
     path resolution; use the shim for headless work).
5. **Declare the lane state honestly at the end**: a lane is WORKING only
   after a live probe returns real model output; a diagnosed-but-unfixed CLI
   is INERT with the cause named. Record unresolved causes in the task
   ledger, not as user requests.

## Pitfalls

- Exit code 0 with zero output is NOT success — a CLI can parse, print
  nothing, and do nothing (verified: mint-style CLI invocations missing
  their action flag). Verify every claimed side effect by reading back the
  target store.
- `strings`-minifying huge bundled JS (minified .cjs) for symbol hunts is
  slow and times out on context-greedy greps; prefer the structured log and
  config files first, bundle archaeology last.
- Do not convert an unresolved CLI defect into a standing "this CLI does
  not work" belief — the defect class is configuration, and the sibling
  app usually proves the underlying service is fine.
- A desktop-app self-updater can silently break a previously-fixed CLI
  wrapper: the updater rewrites the bundled CLI path, so a wrapper that
  worked yesterday dies with a provider-config error (zcode: Chinese text
  naming `ZCode Built-in`). Re-run the version probe after ANY app update
  before dispatching work; fix = repoint the wrapper at the existing shim,
  do not write a new one.
- Probe auth freshness BEFORE queueing real work onto a CLI whose sibling
  app is signed in — the app holding live in-memory tokens proves nothing
  about the CLI's on-disk store (zcode: app auths at launch and keeps it in
  the Electron session; the CLI's credentials.json ages independently and
  surfaces as `Model creation failed`). One cheap `--prompt "reply OK"`
  probe classifies the lane in seconds.
- OAuth re-auth flows that print a URL block ~4-5 min and die if the URL
  is not tapped; each URL is single-use. Re-arm once per explicit user
  go-ahead, never on a loop — repeated unprompted links are friction. If
  the user cannot act now, record the blocker and keep other lanes moving
  rather than serializing everything behind the login.
- Env-var / keychain / cookie archaeology for the app's in-memory tokens is
  a dead end by design (checked: no keychain service items, CDN-only
  cookies, no local-storage tokens, no auth env vars on app processes).
  The CLI refresh path is OAuth; state that plainly instead of hunting.
