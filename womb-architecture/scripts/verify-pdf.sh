#!/usr/bin/env bash
# verify-pdf.sh
# Simple verification that a PDF file exists and is not empty.

set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <pdf-file>"
  exit 1
fi

PDF="$1"

if [[ ! -f "$PDF" ]]; then
  echo "Error: File '$PDF' does not exist."
  exit 1
fi

SIZE=$(stat -f%z "$PDF" 2>/dev/null || stat -c%s "$PDF")
if [[ "$SIZE" -eq 0 ]]; then
  echo "Error: PDF '$PDF' is empty (0 bytes)."
  exit 1
fi

echo "PDF '$PDF' exists and has size ${SIZE} bytes."

# Optional: try to get page count if pdfinfo is available
if command -v pdfinfo >/dev/null 2>&1; then
  PAGES=$(pdfinfo "$PDF" 2>/dev/null | grep Pages | awk '{print $2}' || echo "unknown")
  echo "Page count: $PAGES"
else
  echo "pdfinfo not found; skipping page count check."
fi

exit 0