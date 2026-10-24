#!/usr/bin/env bash
# start-all-engines.sh
# Start all 7 the specialist engine engine FastAPI services, register in Morphogen, verify health.
# Usage: bash scripts/start-all-engines.sh
#
# Engines: wave(8000) quartz(8089) seed(8090) allostasis(8091) harvey(8092) morphogen(8093) bernard(8094)

set -euo pipefail

WORKSPACE="${DS_WORKSPACE:-/<workspace>}"
MORPHOGEN_URL="http://127.0.0.1:port"

declare -A ENGINES=(
  ["wave"]="ds-wave-coaching-engine:port"
  ["quartz"]="ds-quartz-engine:port"
  ["seed"]="ds-seed-engine:port"
  ["allostasis"]="ds-allostasis-engine:port"
  ["harvey"]="ds-harvey-engine:port"
  ["morphogen"]="ds-morphogen-engine:port"
  ["bernard"]="ds-clinical-engine:port"
)

declare -A GENOTYPES=(
  ["wave"]='{"engine_id":"wave","name":"Wave Engine","version":"1.0.0","body_system":"brain_cns","scientist":"Kuramoto","port":port,"capabilities":[{"name":"coaching","version":"1.0"},{"name":"mastermind","version":"1.0"},{"name":"resonance","version":"1.0"}]}'
  ["quartz"]='{"engine_id":"quartz","name":"Quartz Engine","version":"2.0.0","body_system":"autonomic_ns","scientist":"Diviq","port":port,"capabilities":[{"name":"lattice","version":"1.0"},{"name":"tasks","version":"1.0"},{"name":"pid_control","version":"1.0"}]}'
  ["seed"]='{"engine_id":"seed","name":"Seed Engine","version":"2.0.0","body_system":"endocrine_growth","scientist":"Waddington","port":port,"capabilities":[{"name":"avrami_jmak","version":"1.0"},{"name":"landau_phase","version":"1.0"},{"name":"soc","version":"1.0"},{"name":"cpm","version":"1.0"}]}'
  ["allostasis"]='{"engine_id":"allostasis","name":"Allostasis Engine","version":"1.0.0","body_system":"immune_homeostatic","scientist":"Sterling","port":port,"capabilities":[{"name":"surveillance","version":"1.0"},{"name":"diagnosis","version":"1.0"},{"name":"intervention","version":"1.0"}]}'
  ["harvey"]='{"engine_id":"harvey","name":"Harvey Engine","version":"1.0.0","body_system":"circulatory","scientist":"William_Harvey","port":port,"capabilities":[{"name":"fabric","version":"1.0"},{"name":"registry","version":"1.0"},{"name":"transport","version":"1.0"}]}'
  ["morphogen"]='{"engine_id":"morphogen","name":"Morphogen Engine","version":"1.0.0","body_system":"skeletal_registry","scientist":"Paxton","port":port,"capabilities":[{"name":"genotype_registry","version":"1.0"},{"name":"bmp_gradient","version":"1.0"},{"name":"morphogen_field","version":"1.0"}]}'
  ["bernard"]='{"engine_id":"bernard","name":"Bernard Engine (Clinical Diagnostic)","version":"1.0.0","body_system":"clinical_diagnostic","scientist":"Claude_Bernard","port":port,"capabilities":[{"name":"clinical_diagnosis","version":"1.0"},{"name":"rounds","version":"1.0"},{"name":"differential_diagnosis","version":"1.0"},{"name":"vitals_monitoring","version":"1.0"},{"name":"soap_notes","version":"1.0"},{"name":"credential_management","version":"1.0"}],"metadata":{"agent_name":"the specialist engine","description":"AI Organism Attending AI Physician"}}'
)

echo "=== the specialist engine Fleet Startup ==="
echo ""

# Step 1: Start Morphogen first (it's the registry hub)
echo "Starting Morphogen Engine (registry hub, port 8093)..."
cd "$WORKSPACE/ds-morphogen-engine"
python run_server.py &
sleep 3
if curl -sf "$MORPHOGEN_URL/health" >/dev/null 2>&1; then
  echo "  Morphogen: UP"
else
  echo "  Morphogen: FAILED TO START"
  exit 1
fi

# Step 2: Start all other engines
for engine_id in wave quartz seed allostasis harvey bernard; do
  IFS=':' read -r dir port <<< "${ENGINES[$engine_id]}"
  echo "Starting $engine_id (port $port)..."
  cd "$WORKSPACE/$dir"
  python run_server.py &
  sleep 2
  if curl -sf "http://127.0.0.1:$port/health" >/dev/null 2>&1; then
    echo "  $engine_id: UP"
  else
    echo "  $engine_id: FAILED (may need more time, continuing...)"
  fi
done

echo ""
echo "Waiting for all engines to stabilize..."
sleep 5

# Step 3: Register all engines in Morphogen
echo ""
echo "=== Registering genotypes in Morphogen ==="
for engine_id in wave quartz seed allostasis harvey morphogen bernard; do
  result=$(curl -sf -X POST "$MORPHOGEN_URL/genotypes/register" \
    -H "Content-Type: application/json" \
    -d "${GENOTYPES[$engine_id]}" 2>/dev/null || echo '{"registered":"error"}')
  echo "  $engine_id: $(echo "$result" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("registered","error"))' 2>/dev/null || echo 'registered')"
done

# Step 4: Verify all engines
echo ""
echo "=== Health Verification ==="
healthy=0
total=0
for engine_id in wave quartz seed allostasis harvey morphogen bernard; do
  IFS=':' read -r dir port <<< "${ENGINES[$engine_id]}"
  total=$((total + 1))
  status=$(curl -sf "http://127.0.0.1:$port/health" 2>/dev/null | python3 -c "import json,sys; print(json.load(sys.stdin).get('status','unknown'))" 2>/dev/null || echo "DOWN")
  if [ "$status" = "ok" ]; then
    healthy=$((healthy + 1))
    echo "  Port $port ($engine_id): OK"
  else
    echo "  Port $port ($engine_id): $status"
  fi
done

echo ""
echo "=== Organism Map ==="
curl -sf "$MORPHOGEN_URL/organism/map" 2>/dev/null | python3 -c "
import json, sys
d = json.load(sys.stdin)
print(f'{d[\"total_engines\"]} engines registered, {d[\"systems_covered\"]} systems covered')
for eid, info in d.get('engines', {}).items():
    print(f'  {eid}: {info[\"status\"]} ({info[\"body_system\"]})')
" 2>/dev/null || echo "  Could not fetch organism map"

echo ""
echo "=== Result: $healthy/$total engines healthy ==="

if [ "$healthy" -eq "$total" ]; then
  echo "ALL ENGINES OPERATIONAL"
  
  # Run clinical rounds as final verification
  echo ""
  echo "=== Clinical Rounds (Bernard) ==="
  curl -sf -X POST "http://127.0.0.1:port/rounds" 2>/dev/null | python3 -c "
import json, sys
d = json.load(sys.stdin)
print(f'Severity: {d[\"severity\"]}')
print(f'Physician: {d.get(\"physician\", \"unknown\")}')
print(f'Objective: {d[\"objective\"]}')
" 2>/dev/null || echo "  Clinical rounds failed"
else
  echo "WARNING: Some engines are down. Check logs."
  exit 1
fi
