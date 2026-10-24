# Live DOM verification battery (localhost QA, 2026-08-18)

Proven recipe for verifying a localhost web UI without eyeballs, developed
on the sovereign-user Connection Hub QA (MR10-MR12). The battery caught 8+
defects code review missed, including two self-inflicted regressions
(0-card render from const hoisting, duplicate script tag SyntaxError).

## Setup

```
SHELL_BIN=$(find ~/Library/Caches/ms-playwright/chromium_headless_shell-* \
  -name "chrome-headless-shell" -type f | head -1)
```

## Console errors + crash detection

```
"$SHELL_BIN" --headless --disable-gpu --enable-logging=stderr \
  --dump-dom --virtual-time-budget=8000 http://127.0.0.1:port/index.html \
  2>/tmp/err.log | grep -c Uncaught
```

The console log is where silent-fail contracts surface: an empty catch
looked like a neutral label until the log showed the fetch failing. Make
degraded states VISIBLE in the DOM (bad color + reason) so the battery can
assert them.

## Assertion battery (single dump, node post-process)

Pipe dump-dom into node and emit one JSON line:

```
... | node -e "
let d='';process.stdin.on('data',c=>d+=c).on('end',()=>{
  console.log(JSON.stringify({
    cards:(d.match(/class=\"card /g)||[]).length,
    live:(d.match(/class=\"status live\"/g)||[]).length,
    emDash:d.includes('\u2014'), ellipsis:d.includes('\u2026')
  }));
})"
```

Assert on: element counts (cards), badge counts per status, forbidden
characters (em dash, ellipsis), presence of expected strings (service
line, registry age), absence of error markers.

## Traps that cost real time

- A grep hit on a card NAME can be a note-text mention, not a card.
  Count `<h3>` elements when proving a card renders.
- Merge logic can be sound while a SECOND render path still reads the old
  array. Assert the final DOM, never the intermediate structure.
- Registry/generated-file drift: assert the page shows a generated_at stamp
  or age line; silent staleness is how generated registries rot.
- Keep --virtual-time-budget generous (8000) for pages with fetch calls in
  the render path; too-low budgets pass with stale state.
- Mid-word truncation produces ellipsis chars in user-visible notes; clip
  at word boundaries and end with a period, never U+2026.

## Falsification pattern (Popper-standard proof)

To prove a code path executes (not just renders): temporarily instrument
the page to write the path's result into document.title, dump, read the
title, then de-instrument and re-run the battery clean. Used to prove a
merge produced 33 entries while the DOM showed 32 (separate render bug).

## Related

- qa-pass-freeze-and-claims-laws.md (same skill) for the panel discipline
  that surrounds this battery.
