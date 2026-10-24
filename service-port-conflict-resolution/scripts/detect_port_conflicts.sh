#!/bin/bash
# detect_port_conflicts.sh
# Automatically detect port conflicts in the Divinity Science AI Organism ecosystem
# Compares expected port assignments (from canonical mapping) with actual bound ports
# Reports conflicts and suggests corrective actions.

# Define canonical port mapping (should match references/ds-engine-port-mapping.md)
declare -A EXPECTED_PORTS=(
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

# Temporary file for actual bindings
ACTUAL_BINDINGS=$(mktemp)
trap "rm -f $ACTUAL_BINDINGS" EXIT

# Get all listening TCP ports and associated processes/commands
# Format: PORT PROCESS_INFO
sudo lsof -iTCP -sTCP:LISTEN -nP 2>/dev/null | awk '/LISTEN/ {print $9, $1}' | cut -d':' -f2 | sort -n > "$ACTUAL_BINDINGS"
# Alternative if lsof not available: use ss
# ss -tlnp 2>/dev/null | awk '{print $5, $7}' | cut -d':' -f2 | cut -d',' -f1 | sort -n > "$ACTUAL_BINDINGS"

echo "=== Port Conflict Detection Report ==="
echo ""
echo "Expected Ports (from canonical mapping):"
for port in "${!EXPECTED_PORTS[@]}"; do
    echo "  $port: ${EXPECTED_PORTS[$port]}"
done
echo ""

echo "Actual Listening Ports (from lsof):"
if [[ -s "$ACTUAL_BINDINGS" ]]; then
    while read -r line; do
        if [[ -n "$line" ]]; then
            port=$(echo "$line" | awk '{print $1}')
            process=$(echo "$line" | awk '{$1=""; print $0}' | sed 's/^ //')
            echo "  $port: $process"
        fi
    done < "$ACTUAL_BINDINGS"
else
    echo "  No listening ports found (or lsof failed)"
fi
echo ""

# Check for conflicts
echo "=== Conflict Analysis ==="
CONFLICT_FOUND=0

# 1. Check for expected ports bound to wrong process or free
for port in "${!EXPECTED_PORTS[@]}"; do
    expected_engine=${EXPECTED_PORTS[$port]}
    # Check if port is in actual bindings
    if grep -q "^$port[[:space:]]" "$ACTUAL_BINDINGS"; then
        # Port is bound, check by what
        bound_line=$(grep "^$port[[:space:]]" "$ACTUAL_BINDINGS")
        bound_process=$(echo "$bound_line" | awk '{$1=""; print $0}' | sed 's/^ //')
        # Simple check: if the bound process name doesn't contain the expected engine name (case-insensitive)
        # This is heuristic; adjust as needed for your environment
        if [[ ! "$bound_process" =~ (?i)${expected_engine//[^a-zA-Z0-9]/} ]]; then
            echo "⚠ CONFLICT: Port $port expected for '$expected_engine' but bound to:"
            echo "          '$bound_process'"
            echo "          Suggested action: Identify why '$bound_process' is using this port."
            echo "                              If incorrect, stop it and reconfigure '$expected_engine' to use $port."
            echo ""
            CONFLICT_FOUND=1
        else
            echo "✓ OK: Port $port correctly bound to '$expected_engine' (via '$bound_process')"
        fi
    else
        # Port is expected but not bound
        echo "⚠ ISSUE: Port $port expected for '$expected_engine' but not bound by any process."
        echo "          Suggested action: Start '$expected_engine' and ensure it's configured to bind to $port."
        echo ""
        CONFLICT_FOUND=1
    fi
done

# 2. Check for unexpected ports bound (not in expected list) - optional
echo "Checking for unexpected bound ports (not in canonical mapping)..."
while read -r line; do
    if [[ -n "$line" ]]; then
        port=$(echo "$line" | awk '{print $1}')
        process=$(echo "$line" | awk '{$1=""; print $0}' | sed 's/^ //')
        # Check if port is NOT in expected ports
        if [[ -z "${EXPECTED_PORTS[$port]:-}" ]]; then
            echo "⚠ UNEXPECTED: Port $port bound to '$process' but not in canonical mapping."
            echo "          Suggested action: Determine if this process should be using a different port."
            echo "                              If it's a DS engine, check its configuration for correct port."
            echo "                              If it's a non-DS service, consider if it needs to be stopped or relocated."
            echo ""
            CONFLICT_FOUND=1
        fi
    fi
done < "$ACTUAL_BINDINGS"

echo ""
if [[ $CONFLICT_FOUND -eq 0 ]]; then
    echo "✓ No port conflicts detected. All expected ports are correctly assigned."
else
    echo "✗ Conflicts or issues found. Please review the suggested actions above."
fi

exit $CONFLICT_FOUND