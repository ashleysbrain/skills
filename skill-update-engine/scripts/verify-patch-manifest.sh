#!/usr/bin/env bash
# Post-patch manifest verification for the skill-update-engine.
# Confirms that a manifest/body-citation fix is complete:
#   1. No dead manifest entries (manifest-listed files all exist on disk)
#   2. No dead inline references (body-cited paths all exist on disk)
#   3. Version field is present in frontmatter
#
# Usage: verify-patch-manifest.sh /path/to/skill-dir
set -euo pipefail

SKILL_DIR="${1:?Usage: $0 <skill-dir>}"
SKILL="$SKILL_DIR/SKILL.md"
PASS=0; FAIL=0
check() { if eval "$2"; then echo "PASS: $1"; PASS=$((PASS+1)); else echo "FAIL: $1"; FAIL=$((FAIL+1)); fi; }

# 1. Version field exists
check "version field present" "grep -qE '^version: [0-9]' '$SKILL'"

# 2. Zero dead manifest entries — every manifest bullet resolves to a file
MANIFEST_DEAD=0
while IFS= read -r entry; do
  clean=$(echo "$entry" | sed 's/^- `//;s/`$//')
  if [ -n "$clean" ] && [ ! -f "$SKILL_DIR/$clean" ]; then
    echo "  DEAD MANIFEST ENTRY: $clean"
    MANIFEST_DEAD=$((MANIFEST_DEAD+1))
  fi
done < <(grep -E '^- `(references|templates|scripts|attachments)/' "$SKILL")
check "zero dead manifest entries" "[ $MANIFEST_DEAD -eq 0 ]"

# 3. Zero dead inline references — every backtick path resolves to a file
INLINE_DEAD=0
while IFS= read -r ref; do
  ref=$(echo "$ref" | tr -d '`')
  if [ ! -f "$SKILL_DIR/$ref" ]; then
    echo "  DEAD INLINE REF: $ref"
    INLINE_DEAD=$((INLINE_DEAD+1))
  fi
done < <(grep -oE '`(references|templates|scripts|attachments)/[^`]+`' "$SKILL" || true)
check "zero dead inline references" "[ $INLINE_DEAD -eq 0 ]"

echo "---"
echo "RESULT: $PASS passed, $FAIL failed"
[ $FAIL -eq 0 ]
