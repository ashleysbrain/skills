#!/usr/bin/env bash
# Bind (or re-bind) a the OS organ surface to a tenant Google Workspace vault.
# Idempotent: safe to re-run; existing symlinks are refreshed, old real files
# are backed up with .pre-mosaic suffix before being replaced.
#
# Usage:
#   bind_google_workspace_tenant.sh [tenant]      # default tenant: your-org
#   bind_google_workspace_tenant.sh my-other-tenant
set -euo pipefail

TENANT="${1:-your-org}"
VAULT="$HOME/.config/mosaic/credentials/tenants/$TENANT/google"

if [ ! -f "$VAULT/client_secret.json" ]; then
  echo "ERROR: no vault at $VAULT — onboard the provider first (see SKILL.md recipe)." >&2
  exit 1
fi

# bind <target-path> <vault-file>
bind() {
  local target="$1" source="$2"
  if [ -e "$target" ] && [ ! -L "$target" ]; then
    cp "$target" "$target.pre-mosaic" 2>/dev/null || true
    echo "backed up real file: $target -> $target.pre-mosaic"
  fi
  ln -sfn "$source" "$target"
  echo "bound: $target -> $source"
}

# the operator agent default home
bind "$HOME/.hermes/google_client_secret.json" "$VAULT/client_secret.json"
bind "$HOME/.hermes/google_token.json" "$VAULT/token.json"

# gws CLI config
bind "$HOME/.config/gws/client_secret.json" "$VAULT/client_secret.json"

# Optional additional the operator agent profile homes: pass names as extra args
shift || true
for profile in "$@"; do
  bind "$HOME/.hermes/profiles/$profile/google_client_secret.json" "$VAULT/client_secret.json"
  bind "$HOME/.hermes/profiles/$profile/google_token.json" "$VAULT/token.json"
done

echo
echo "Vault token present: $([ -f "$VAULT/token.json" ] && echo yes || echo 'NO — mint not done yet')"
echo "Direct CLI env (add to organ launch env):"
echo "  export GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=\"$VAULT/token.json\""
