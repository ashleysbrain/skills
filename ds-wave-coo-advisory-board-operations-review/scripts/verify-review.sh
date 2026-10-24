#!/bin/bash
# verify-review.sh
# Script to verify the completeness of a COO Advisory Board operations review

REPORT_FILE="$1"

if [ -z "$REPORT_FILE" ]; then
  echo "Usage: $0 <report-file>"
  exit 1
fi

if [ ! -f "$REPORT_FILE" ]; then
  echo "Error: Report file '$REPORT_FILE' not found"
  exit 1
fi

echo "Verifying COO Advisory Board report: $REPORT_FILE"
echo "=================================================="

# Check for required sections
REQUIRED_SECTIONS=(
  "## COO Advisory Board — Operations Review"
  "📅"
  "**Operational State**:"
  "👥 **Advisor Notes:**"
  "🚀 Gwynne Shotwell:"
  "🍎 Tim Cook:"
  "💰 Ruth Porat:"
  "💬 Sheryl Sandberg:"
  "✨ Angela Ahrendts:"
  "🎯 **Today's Operational Priorities:**"
  "⚠️ **Cross-Board Handoffs Needed:**"
  "🔄 **Communication Gaps:**"
  "## ⚡ ACTION ITEMS"
  "---"
  "⚡ Quick reply:"
)

MISSING_SECTIONS=0
for section in "${REQUIRED_SECTIONS[@]}"; do
  if grep -q "$section" "$REPORT_FILE"; then
    echo "✓ Found: $section"
  else
    echo "✗ MISSING: $section"
    ((MISSING_SECTIONS++))
  fi
done

echo ""
echo "=================================================="
if [ $MISSING_SECTIONS -eq 0 ]; then
  echo "All required sections found!"
  
  # Additional checks
  echo ""
  echo "Additional validation:"
  
  # Check date format (YYYY-MM-DD)
  if grep -q "📅 [0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}" "$REPORT_FILE"; then
    echo "✓ Date format appears correct (YYYY-MM-DD)"
  else
    echo "⚠ Date format may be incorrect - expected YYYY-MM-DD"
  fi
  
  # Check for advisor emojis
  ADVISOR_EMOJIS=("🚀" "🍎" "💰" "💬" "✨")
  for emoji in "${ADVISOR_EMOJIS[@]}"; do
    if grep -q "$emoji" "$REPORT_FILE"; then
      echo "✓ Found advisor emoji: $emoji"
    else
      echo "✗ Missing advisor emoji: $emoji"
    fi
  done
  
  # Check for action item format
  if grep -q "^\*\*1\." "$REPORT_FILE"; then
    echo "✓ Action items numbered correctly"
  else
    echo "⚠ Action items may not be formatted correctly"
  fi
  
  # Check for reply format
  if grep -q "→ Reply:" "$REPORT_FILE"; then
    echo "✓ Reply format found"
  else
    echo "✗ Reply format missing"
  fi
  
  exit 0
else
  echo "Found $MISSING_SECTIONS missing sections. Please review the report."
  exit 1
fi