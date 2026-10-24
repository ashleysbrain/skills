#!/bin/bash
# Verification script to check if rescore results persisted in the database
# Usage: ./verify_rescore_persistence.sh <date> <expected_twc>

DATE="$1"
EXPECTED_TWC="$2"

if [ -z "$DATE" ] || [ -z "$EXPECTED_TWC" ]; then
  echo "Usage: $0 <YYYY-MM-DD> <expected_twc>"
  exit 1
fi

# Query the actual TWC from the database
ACTUAL_TWC=$(sqlite3 /<workspace> "
  SELECT twc_score FROM daily_scorecard WHERE date = '$DATE';
")

# Check if the value exists and matches expected (within tolerance)
if [ -z "$ACTUAL_TWC" ]; then
  echo "ERROR: No TWC found for date $DATE"
  exit 1
fi

# Check if values match within 0.01 tolerance
TOLERANCE=0.01
DIFF=$(echo "$ACTUAL_TWC - $EXPECTED_TWC" | bc -l)
ABS_DIFF=$(echo "${DIFF#-}" | bc -l)  # Get absolute value

if (( $(echo "$ABS_DIFF > $TOLERANCE" | bc -l) )); then
  echo "ERROR: TWC mismatch for $DATE"
  echo "  Expected: $EXPECTED_TWC"
  echo "  Actual:   $ACTUAL_TWC"
  echo "  Diff:     $DIFF"
  exit 1
else
  echo "SUCCESS: TWC persisted correctly for $DATE"
  echo "  Value: $ACTUAL_TWC (within $TOLERANCE of expected $EXPECTED_TWC)"
  exit 0
fi