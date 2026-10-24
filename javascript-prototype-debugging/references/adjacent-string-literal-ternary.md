# Adjacent string literals in ternary — one missing space kills the script block (2026-08-19)

Found while building the the OS conductor screen v2 (live dashboard served by
the conduction daemon on :port). Could not be patched into SKILL.md by the
background curator (gate refused for this subdirectory skill) — recorded here.

## The bug
```javascript
// BROKEN — kills the ENTIRE <script> block:
const dl = (k,v) => v? '<div class="dl"><b>'+esc(k)+':</b> '+esc(v)+'</div>'+'':
//                                                                            ^^^^ two adjacent literals

// FIXED — pad the ternary:
const dl = (k,v) => v? '<div class="dl"><b>'+esc(k)+':</b> '+esc(v)+'</div>' : '';
```

## Symptoms (exactly one data panel dead, rest of page fine visually)
- The panel's container renders empty (`innerHTML === ""`, zero rows).
- ALL event handlers across the page are dead (the whole block died, but CSS
  still renders so the page looks superficially intact).
- Browser automation reports `pageerror: "Unexpected string"` with NO stack,
  NO line number — useless for localization.

## Diagnosis (fastest path, confirmed twice now)
1. Extract the `<script>` block: `re.search(r'<script>(.*?)</script>', html, re.S)`
2. `node --check /tmp/extracted.js` — prints the EXACT line/column in seconds.
This outranks all browser debugging for "vague pageerror + dead page" reports.

## Why ternaries that build HTML are high-risk
The then-branch ends in a string literal and the else-branch starts with one;
concatenation makes the boundary invisible in review. Rule: when string
literals sit on both sides of `?`/`:`, always pad with spaces.

## Sibling lesson from the same session
Empty data + no error usually means a swallowed exception over a wrong schema,
not a network problem: a broker query referenced a nonexistent `updated_at`
column; `except Exception: pass` returned empty recommendations silently for
hours. `PRAGMA table_info` before writing store queries; make bare excepts
at least log.
