#!/usr/bin/env bash
# create-body-system-profiles.sh
# Creates 7 engine profiles + 1 patient interface profile for the the specialist engine organism.
# Each profile maps to a body system with its own model, skills, and memory.
# Run from any directory with hermes CLI available.

set -euo pipefail

HERMES_CMD="${HERMES_CMD:-hermes}"

echo "=== Creating the operator agent Body System Profiles (7 engines + 1 interface) ==="
echo ""

# Engine profiles (one per FastAPI engine service)
declare -A MODELS=(
  ["wave"]="openrouter/nvidia/nemotron-3-ultra:free"
  ["quartz"]="openrouter/google/gemini-2.5-flash"
  ["seed"]="openrouter/deepseek/deepseek-r1:free"
  ["allostasis"]="openrouter/z-ai/glm-4.5-air:free"
  ["harvey"]="openrouter/z-ai/glm-4.5-air:free"
  ["morphogen"]="openrouter/nvidia/nemotron-3-ultra:free"
  ["bernard"]="openrouter/nvidia/nemotron-3-ultra:free"
)

for p in wave quartz seed allostasis harvey morphogen bernard; do
  echo "Creating profile: $p..."
  $HERMES_CMD profile create "$p" --clone
  $HERMES_CMD -p "$p" config set model.default "${MODELS[$p]}"
  $HERMES_CMD -p "$p" config set agent.max_turns 60
  $HERMES_CMD -p "$p" skills install hermes-agent kanban-worker
  echo "  $p profile created (${MODELS[$p]})"
done

# Specialized skills per body system
echo ""
echo "Installing specialized skills..."
$HERMES_CMD -p wave skills install kanban-orchestrator 2>/dev/null || echo "  (ds-wave-coaching: install if available)"
$HERMES_CMD -p allostasis skills install sentinel-compliance-audit 2>/dev/null || true
$HERMES_CMD -p bernard skills install aisha-md-health-orchestration sentinel-compliance-audit 2>/dev/null || true

# Patient Interface profile
echo ""
echo "Creating patient interface profile (principal-interface)..."
$HERMES_CMD profile create principal-interface --clone
$HERMES_CMD -p principal-interface config set model.default "openrouter/nvidia/nemotron-3-ultra:free"
$HERMES_CMD -p principal-interface skills install aisha-md-health-orchestration hermes-agent
echo "  principal-interface profile created"

# Route Telegram to patient interface
echo ""
echo "Configuring Telegram routing to principal-interface..."
$HERMES_CMD config set gateway.platforms.telegram.default_profile "principal-interface" 2>/dev/null || echo "  (set manually in config.yaml if needed)"

echo ""
echo "=== Profile Creation Complete ==="
echo ""
$HERMES_CMD profile list
echo ""
echo "Next steps:"
echo "1. Start all engines: bash scripts/start-all-engines.sh"
echo "2. Verify Morphogen registry: curl $MORPHOGEN_URL/organism/map"
echo "3. Test Telegram routing to principal-interface"
echo "4. Set up per-profile cron rhythms (see references/cron-rhythms.md)"
