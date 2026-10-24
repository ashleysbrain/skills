#!/bin/bash
# verify-request.sh - Verify talent request processing
#
# Usage: ./verify-request.sh <request-file>
# Checks that the request file contains a DECISION section and has been moved to processed/

if [ $# -ne 1 ]; then
  echo "Usage: $0 <request-file>"
  exit 1
fi

REQUEST_FILE="$1"
PROCESSED_DIR="~/.sibling-agent/workspace/intel/agents/talent-requests/processed/"

# Check if file exists
if [ ! -f "$REQUEST_FILE" ]; then
  echo "Error: Request file not found: $REQUEST_FILE"
  exit 2
fi

# Check for DECISION section
if grep -q "^## DECISION$" "$REQUEST_FILE" || grep -q "^### DECISION$" "$REQUEST_FILE"; then
  echo "OK: DECISION section found in $REQUEST_FILE"
else
  echo "ERROR: DECISION section missing in $REQUEST_FILE"
  exit 3
fi

# Check if file is in processed directory (optional)
if [[ "$REQUEST_FILE" == */processed/* ]]; then
  echo "OK: Request file is already in processed directory."
else
  # Check if a copy exists in processed
  BASENAME=$(basename "$REQUEST_FILE")
  if [ -f "$PROCESSED_DIR/$BASENAME" ]; then
    echo "OK: Processed copy found in $PROCESSED_DIR/$BASENAME"
  else
    echo "WARNING: Request file not yet moved to processed directory."
  fi
fi