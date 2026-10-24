#!/bin/bash
# check_ds_ports.sh
# Verify health of all Divinity Science AI Organism engines on canonical ports

# Define canonical port mapping (echoes references/ds-engine-port-mapping.md)
declare -A DS_PORTS=(
    [8010]="Wave Coaching"
    [8089]="Quartz (Crystal)"
    [8090]="Reproductive"
    [8091]="Allostasis"
    [8092]="Harvey"
    [8093]="Morphogen"
    [8094]="Beaumont"
    [8095]="Seed"
    [8096]="Bright"
    [8097]="Unna"
    [8099]="Clinical (Bernard)"
)

TIMEOUT=2
FAILED=0

echo "=== Divinity Science Engine Health Check ==="
echo "Checking canonical ports: ${!DS_PORTS[*]}"
echo ""

for port in "${!DS_PORTS[@]}"; do
    engine=${DS_PORTS[$port]}
    echo -n "Port $port ($engine): "
    if response=$(curl -s --max-time $TIMEOUT http://127.0.0.1:$port/health 2>/dev/null); then
        # Try to parse JSON status
        status=$(echo "$response" | python3 -c "import sys,json;print(json.load(sys.stdin).get('status','ERROR'))" 2>/dev/null || echo "PARSE_ERROR")
        if [[ "$status" == "ok" ]] || [[ "$status" == "OK" ]]; then
            echo "✓ HEALTHY ($status)"
        else
            echo "✗ UNHEALTHY ($status)"
            FAILED=$((FAILED + 1))
        fi
    else
        echo "✗ DOWN (no response)"
        FAILED=$((FAILED + 1))
    fi
done

echo ""
if [[ $FAILED -eq 0 ]]; then
    echo "All engines healthy ✓"
    exit 0
else
    echo "$FAILED engine(s) unhealthy ✗"
    exit 1
fi