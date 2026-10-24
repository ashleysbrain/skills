#!/usr/bin/env bash
# generate-pdf.sh
# Helper script to convert markdown to PDF using weasyprint.
# Expects to be run from the skill's directory or with proper paths.

set -euo pipefail

# Usage: ./generate-pdf.sh input.md output.pdf
if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <input-markdown-file> <output-pdf-file>"
  exit 1
fi

INPUT="$1"
OUTPUT="$2"

# Create a temporary virtual environment for weasyprint to avoid system conflicts
TMPVENV=$(mktemp -d)
python3 -m venv "$TMPVENV"
source "$TMPVENV/bin/activate"
pip install --quiet weasyprint

# Run conversion
weasyprint "$INPUT" "$OUTPUT"

# Cleanup
deactivate
rm -rf "$TMPVENV"

echo "PDF generated: $OUTPUT"