---
name: mosaic-credential-vault
description: "Use when wiring the OS organs to tenant-walled OAuth vaults."
version: 1.0.0
category: infrastructure
---

# the OS Credential Vault — one mint, many binds

One OAuth consent per provider per tenant. Every organ (the operator agent, OpenClaw,
sibling-agent, gws CLI, future organisms) BINDS to the tenant vault — none mints
its own. Vault lives OUTSIDE any single harness so no harness owns it.

Routing: credential-membrane architecture routes to the specialist engine (connective
tissue). OS-level design questions go to the specialist engine / the specialist engine, never
creative organs.

## The tenant-wall law (principal directive 2026-08-20, preserve verbatim intent)

> "mosaic os is being built using [tenant A] BUT for each individual
> organism, depending on the type of organism, it will be different
> credentials and different vaults and information... which will require
> specific walls between data... GGLive is a B2B organism so it is driven
> specifically from the divinity science credentials... remember we are
> building for others so we have to think this through."

- B2B organisms (GGLive) bind to the `your-org` tenant vault.
- Sovereign-user organisms (personal data) get their OWN tenant class,
  local-only, never upstream — see sovereignty law v2 in
  `~/your-org/your-stack/stores/connectivity.store.json`.
- Tenants never share tokens. Walls are DATA (registry rows), not code.

## Vault layout (built + verified 2026-08-20)

```
~/.config/mosaic/credentials/
  ├── registry.json                      # tenant -> organs -> provider grants (as data)
  └── tenants/
      └── your-org/google/       # first tenant/provider
          ├── client_secret.json         # canonical OAuth client
          ├── token.json                 # minted user token (refreshes write through)
          └── client_meta.json           # lineage notes
```

## Binding recipe (per organ — no re-consent, ever)

Symlinks, never copies: refresh flows write THROUGH symlinks back to the
vault, so every organ sees the freshest token.

```bash
ln -sf ~/.config/mosaic/credentials/tenants/<tenant>/<provider>/client_secret.json <agent-home>/google_client_secret.json
ln -sf ~/.config/mosaic/credentials/tenants/<tenant>/<provider>/token.json        <agent-home>/google_token.json
ln -sf ~/.config/mosaic/credentials/tenants/<tenant>/<provider>/client_secret.json ~/.config/gws/client_secret.json
```

- the operator agent per-profile homes (`<agent-home>/profiles/<name>/`) need the same
  symlinks repeated — decide with principal which profiles bind to which tenant.
- Direct gws/sibling-agent/sibling-agent use: `GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE`
  pointing at the vault token (the operator agent' google-workspace bridge sets this
  itself when driving gws).
- Script: `scripts/bind_google_workspace_tenant.sh` (idempotent).

## Provider onboarding recipe (generic)

1. DIGEST: sweep ALL harnesses for existing credentials before minting —
   `<agent-home>/`, `~/.sibling-agent/` (`auth.profiles` in sibling-agent.json),
   `~/.config/gws/`, `~/.config/gcloud/application_default_credentials.json`,
   `gcloud auth list`. Reuse what exists.
2. Repair/complete the OAuth client secret into the vault (see pitfalls).
3. Mint ONCE via the the operator agent skill flow (`setup.py --auth-url` → user approves
   in browser → paste redirect URL back → `--auth-code`). Browser dead-ends at
   `http://localhost:1/?code=...` — expected; the code is in the URL.
   `Error 403: access_denied` → add the account as OAuth test user at
   console.cloud.google.com/auth/audience.
4. Bind every organ (recipe above) + registry row + register in
   `~/your-org/your-stack/stores/connectivity.store.json`.
5. VERIFY by execution: `setup.py --check` → AUTHENTICATED, `gws auth status`
   → no config error, and one LIVE API call per bound surface.

Worked example (Google Workspace, incl. what was verified vs pending):
`references/google-workspace-onboarding.md`.

## Pitfalls (observed live 2026-08-20)

1. **OpenClaw's "google" auth may be `google-gemini-cli` OAuth** — Gemini
   MODEL access on a gmail.com identity, NOT Workspace scopes. A prior
   "hookup" does not transfer. Read `auth.profiles` keys before assuming.
2. **gws serde requires fields Google ignores**: a Desktop-app
   client_secret.json with only client_id/secret/redirect_uris fails
   `gws auth status` with "Invalid client_secret.json format: missing field
   `project_id`" (then `auth_uri`, `token_uri`,
   `auth_provider_x509_cert_url`). Fill the standard constants:
   `auth_uri=https://accounts.google.com/o/oauth2/auth`,
   `token_uri=https://oauth2.googleapis.com/token`,
   `auth_provider_x509_cert_url=https://www.googleapis.com/oauth2/v1/certs`,
   `project_id=<best-known>` (endpoints do not validate it).
3. **the operator agent google-workspace SKILL.md documents `--services` / `--format`
   flags the installed setup.py may lack** — run `setup.py --help` before
   promising flags. Doc drift between skill text and script version is real.
4. **gcloud reauth expiry does NOT block minting** — it only blocks project
   introspection (`gcloud projects describe`). Proceed with the OAuth flow.
5. **Never copy tokens between organs** — copies fork refresh state; only
   symlinks/env bindings keep one source of truth.
6. **Honest encryption state**: sovereignty law G2 (tokens encrypted at
   rest) is NOT BUILT — vault files are 0600 plain JSON. Say so; never claim
   G2 compliance.

## Verification gate

A binding is DONE only when proven live: symlink resolves, `--check`
AUTHENTICATED, and a real API call returns data on EACH bound surface.
Report BUILT vs PENDING separately, never blended.
