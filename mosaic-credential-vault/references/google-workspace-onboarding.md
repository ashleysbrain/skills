# Google Workspace Onboarding — worked example (2026-08-20)

First tenant/provider wired into the vault. Records what was VERIFIED by
execution vs what remained PENDING at session end, so the next session
resumes from truth, not hope.

## Situation

principal: "connect mosaic os to my google workspace... hook it up once and for it
to be like google is with different company systems... use your google
credentials to log in." Clarified mid-session: DS tenant
(principal.williams@divinityscience.com) drives B2B organisms (GGLive);
sovereign-user organisms get separate tenant walls.

## Credential census results (all probed live)

| Surface | State found | Meaning |
|---|---|---|
| `<agent-home>/google_token.json` | absent | the operator agent never minted Workspace token |
| `~/.config/gws/client_secret.json` | present but INVALID (missing project_id, auth_uri, token_uri, auth_provider_x509_cert_url) | gws blocked at config parse |
| `~/.sibling-agent/sibling-agent.json` auth.profiles | `google-gemini-cli:goddessdivinity888@gmail.com` — Gemini model OAuth, gmail identity | NOT Workspace; does not transfer |
| `~/.sibling-agent/credentials/` | only whatsapp files | no google |
| `gcloud auth list` | principal.williams@divinityscience.com, project sibling-agent-ds-063963 (session expired for describe) | tenant identity confirmed |
| OAuth client | `683351052141-6uapev...apps.googleusercontent.com`, Desktop type | reusable |

## What was BUILT (verified)

1. Vault at `~/.config/mosaic/credentials/tenants/your-org/google/`:
   repaired client_secret.json (canonical 7-field Desktop shape) +
   client_meta.json lineage note.
2. Symlink bindings live:
   - `<agent-home>/google_client_secret.json` → vault
   - `<agent-home>/google_token.json` → vault (dangling until mint)
   - `~/.config/gws/client_secret.json` → vault (old file backed up as
     `client_secret.json.pre-mosaic`)
3. `gws auth status` client_config_error went from missing-field errors to
   `None` — verified after each repair iteration.

## Repair iteration detail (the serde trap)

gws validates the client_secret against a full struct even though Google's
endpoints only need client_id/secret. Missing fields surfaced one at a time:
`project_id` → `auth_uri` → then canonical order. Final valid shape:

```json
{"installed": {
  "client_id": "<id>",
  "project_id": "sibling-agent-ds-063963",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_secret": "<secret>",
  "redirect_uris": ["http://localhost", "http://127.0.0.1"]
}}
```

## Mint flow (as executed)

- `python3 skills-library/productivity/google-workspace/scripts/setup.py --auth-url`
  (installed build has NO `--services`/`--format` flags despite SKILL.md)
- URL embeds PKCE challenge + state, scope set = gmail.readonly/send/modify,
  calendar, drive, contacts.readonly, spreadsheets, documents;
  `redirect_uri=http://localhost:1&access_type=offline&prompt=consent`
- PKCE verifier persisted to `<agent-home>/google_oauth_pending.json` — the
  `--auth-code` exchange works headless/later.

## PENDING at session end (resume here)

1. principal pastes `http://localhost:1/?code=...` redirect → run
   `setup.py --auth-code "<pasted URL>"` → token.json lands in vault via
   symlink.
2. Live verify: `setup.py --check` (AUTHENTICATED), `--check-live`, one real
   `gws gmail users getProfile --params '{"userId":"me"}'` call.
3. Write `~/.config/mosaic/credentials/registry.json` (walls as data).
4. Register provider in `~/your-org/your-stack/stores/connectivity.store.json`.
5. OpenClaw + sibling-agent bindings (env/registry rows, no re-consent).
6. the operator agent profile homes: decide per-profile tenant binding with principal.

## Pre-diagnosed mint failures

- `Error 403: access_denied` → client in Testing mode; add
  principal.williams@divinityscience.com at
  https://console.cloud.google.com/auth/audience
- Account picker offers gmail identity → must pick divinityscience.com
  (tenant identity).
- Code expired/used → setup.py returns `fresh_auth_url`; retry with newest.
