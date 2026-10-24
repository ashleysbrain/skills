#!/bin/bash
# Script to verify that the manifest list in SKILL.md matches the actual files in support directories.
# Support directories: references, templates, scripts, attachments (if present)

SKILL_FILE="SKILL.md"
SUPPORT_DIRS=("references" "templates" "scripts" "attachments")

echo "Verifying manifest for $SKILL_FILE"

# Extract all inline backtick paths from SKILL.md that point to support directories
# Pattern: `references/...`, `templates/...`, etc.
# We'll capture the path inside the backticks.
MANIFEST_FILES=$(grep -o '`[^`]*`' "$SKILL_FILE" | sed 's/^`//;s/`$//' | grep -E '^(references|templates|scripts|attachments)/' | grep -v '/$' | sort -u)

echo "Files listed in SKILL.md manifest:"
echo "$MANIFEST_FILES"

# For each support directory, list actual files
ACTUAL_FILES=""
for dir in "${SUPPORT_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        # List all files in the directory, relative to skill root
        find "$dir" -type f | sort | while read file; do
            echo "$file"
        done
    fi
done > /tmp/actual_files.txt

ACTUAL_FILES=$(cat /tmp/actual_files.txt | sort)

echo "Actual files in support directories:"
echo "$ACTUAL_FILES"

# Compare
echo "Files in manifest but not on disk:"
comm -23 <(echo "$MANIFEST_FILES") <(echo "$ACTUAL_FILES") | while read file; do
    echo "  $file (dead link)"
done

echo "Files on disk but not in manifest:"
comm -13 <(echo "$MANIFEST_FILES") <(echo "$ACTUAL_FILES") | while read file; do
    echo "  $file (unlisted)"
done

# Exit with 0 if no discrepancies, 1 if there are discrepancies
if [ -z "$(comm -23 <(echo "$MANIFEST_FILES") <(echo "$ACTUAL_FILES"))" ] && [ -z "$(comm -13 <(echo "$MANIFEST_FILES") <(echo "$ACTUAL_FILES"))" ]; then
    echo "Manifest verification PASSED"
    exit 0
else
    echo "Manifest verification FAILED"
    exit 1
fi