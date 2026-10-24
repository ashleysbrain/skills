#!/usr/bin/env zsh
# Live DOM battery for a local hub page (MR10-MR12 pattern).
# Usage: hub-dom-battery.sh <url> ; exit 0 = all assertions pass.
# Asserts: card count > 0, no em dash (U+2014), no ellipsis (U+2026),
#          no Uncaught console errors. Prints the measured facts as JSON.
set -u
URL="${1:-http://127.0.0.1:port/index.html}"
SHELL_BIN=$(find ~/Library/Caches/ms-playwright -name "chrome-headless-shell" -type f 2>/dev/null | head -1)
[ -z "$SHELL_BIN" ] && { echo "chrome-headless-shell not found"; exit 2; }
ERRLOG=$(mktemp)
"$SHELL_BIN" --headless --disable-gpu --enable-logging=stderr \
  --dump-dom --virtual-time-budget=8000 "$URL" 2>"$ERRLOG" | node -e '
let d="";process.stdin.on("data",c=>d+=c).on("end",()=>{
  const facts={cards:(d.match(/class=\\"card /g)||[]).length,
    live:(d.match(/class=\\"status live\\"/g)||[]).length,
    emDash:d.includes("\u2014"), ellipsis:d.includes("\u2026")};
  console.log(JSON.stringify(facts));
  process.exit(facts.cards>0 && !facts.emDash && !facts.ellipsis ? 0 : 1);
});'
rc=$?
UNCAUGHT=$(grep -c "Uncaught" "$ERRLOG" 2>/dev/null || echo 0)
rm -f "$ERRLOG"
[ "$UNCAUGHT" -gt 0 ] && { echo "UNCAUGHT console errors: $UNCAUGHT"; exit 1; }
exit $rc
