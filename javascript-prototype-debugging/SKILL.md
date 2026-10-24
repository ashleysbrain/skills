---
name: javascript-prototype-debugging
description: Debug and fix JavaScript web prototypes to ensure full interactivity
version: 1.0.0
---

# JavaScript Prototype Debugging

## When to Use This Skill
Use this skill when debugging JavaScript web prototypes where UI elements are not responding as expected, buttons don't work, or interactive features are broken due to JavaScript errors or incomplete implementations.

## Key Principles
1. **Always check the browser console first** - JavaScript errors will prevent interactivity
2. **Verify all referenced variables and functions exist** - Undefined references are common in prototypes
3. **Complete incomplete functions** - Look for TODO comments, empty functions, or stub implementations
4. **Ensure proper event handling** - Check that event listeners are correctly attached
5. **Test thoroughly** - Verify each interactive element works after fixes

## Step-by-Step Process

### 1. Initial Assessment
- Open browser developer tools (F12 or Cmd+Option+I)
- Go to Console tab to identify JavaScript errors
- Note which interactive elements are not working
- Reload the page and attempt to use broken features while watching for new errors

### 2. Common Issues to Check
**Undefined Variables/Functions**
- Search for references to variables/functions that may not be defined
- Common patterns: `audioPlayer`, `someUndefinedFunction`, `missingObject.property`
- Fix by either defining the missing reference or correcting to the proper name

**State Variable Never Updated (silent no-op)**
- A click handler reads `btn.dataset.metric` but never assigns it to the variable the render function checks. Buttons highlight but nothing changes.
- Always trace: click handler → state variable → render function that reads it. If the assignment is missing, the toggle is cosmetic only.

**Incomplete Functions**
- Look for functions with empty bodies or just `return;` statements
- Check for TODO comments or FIXME notes
- Complete the implementation based on the intended functionality

**Duplicate Function Definitions**
- If the same function name is defined twice in the same file, the LAST definition wins silently, overriding any fixes in the earlier one.
- This is extremely common in files that grew incrementally (someone adds a "fixed" version at the bottom but the old one is still there).
- Fix: `grep -n 'function <name>' file.html` — if you see 2+ hits, delete the stale one.
- **Nested function shadowing (2026-07-14):** A function defined INSIDE another function (indented, scoped to the parent) is invisible to `onclick` handlers. `grep -n 'function name'` shows 2 hits but only the inner one runs. Remove the inner definition so the global one is reachable.

**Functions Defined Inside `<script src="external.js">` Blocks (2026-07-14)**
- When you inject inline JS between `<script src="external.js">` and `</script>`, the browser loads the EXTERNAL file and completely ignores the inline content. No error, no warning — the functions simply don't exist.
- **Detection:** Function text is in the file but `typeof myFunction` returns `"undefined"`.
- **Fix:** Use two separate tags: `<script src="external.js"></script>` then `<script>/* inline */</script>`.

**Brace Balance Corruption in Large Single-File HTML (2026-07-14)**
- In 10000+ line HTML files with inline JS, incremental string replacements can introduce extra or missing braces. This silently breaks the ENTIRE script block — ALL functions become undefined, not just the one near the edit.
- **Detection:** Run brace balance check per script block:
  ```python
  import re
  scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
  for i, code in enumerate(scripts):
      print(f'Block {i}: {code.count("{") - code.count("}")}')
  ```
  Any non-zero result = syntax error in that block.
- **Fix:** Find the negative-balance line, add or remove the offending brace.

**`const` Redeclaration Crashes ENTIRE Script Block (2026-07-14)**
- A `const` or `let` declared in one location (e.g., line 2395: `var MED_API = ...`) that gets redeclared elsewhere (e.g., line 10294: `const MED_API = ...`) is a **SyntaxError** that kills the ENTIRE `<script>` block — all 553K chars of it. Not just the local scope. Every function, every variable, every init call in that block is dead.
- **Symptom:** `typeof TELEMETRY_URL === 'undefined'`, `typeof ORGANISM_DATA === 'undefined'`, nothing interactive works, but the page renders HTML fine (CSS runs independently). Console shows empty `exception` errors with no message.
- **Detection:** Run `new Function(code)` per script block in the console:
  ```javascript
  (function(){
    var scripts = document.querySelectorAll('script:not([src])');
    var errors = [];
    for (var i=0; i<scripts.length; i++) {
      try { new Function(scripts[i].textContent); }
      catch(e) { errors.push(i + ':' + e.message.substring(0,80)); }
    }
    return errors.length ? errors.join(' | ') : 'ALL_OK';
  })()
  ```
  `Identifier 'MED_API' has already been declared` = redeclaration crash.
- **Fix:** Remove the duplicate declaration. Keep the one that was there first (usually the one wired to config like `ORG_CFG`). Delete the hardcoded one that was added later.
- **Key insight:** This is NOT caught by brace balance checks. The braces are balanced. The syntax error is semantic (duplicate binding), not structural.

**Missing Closing Brace Traps All Subsequent const/let in Function Scope (2026-07-14)**
- A function like `switchOrganism()` is missing its closing `}` (e.g., at line 2710). Every `const GATEWAY_STAGES`, `const ENGINE_VARIANTS`, `const ROUTE_RULES`, `var PIPELINES` declared AFTER it (lines 3652+) is now scoped INSIDE `switchOrganism` instead of at global scope. They exist in the file but `typeof PIPELINES === 'undefined'` globally.
- **Symptom:** `typeof ORGANISMS === 'object'` (declared BEFORE the unclosed function) but `typeof GATEWAY_STAGES === 'undefined'` (declared AFTER). The cutoff between "defined" and "undefined" globals pinpoints the unclosed function.
- **Detection:** Check `typeof` for each top-level `const`/`var` in declaration order. The first one that's `undefined` tells you the unclosed function is between the last-defined and first-undefined variable. Look for a function between those two line numbers that's missing its closing `}`.
- **Fix:** Add the missing `}`. Then re-check brace balance (diff will go to -1 if there was already a compensating extra brace elsewhere). Find and remove the compensating brace.
- **Key insight:** This is NOT a SyntaxError — `new Function(code)` passes because nested functions are legal JS. It's a SCOPE error: the declarations are valid but trapped in the wrong scope. The page renders fine (HTML/CSS) but all interactive JS after the unclosed function is invisible globally.
- **How it differs from TDZ:** TDZ means the variable exists but accessing it before assignment throws. Scope-trapping means the variable does NOT exist in global scope at all. `typeof` returns `'undefined'` for scope-trapped, throws `ReferenceError` for TDZ.

**PREMATURE Closing Brace — Orphaned Code at Top Level (2026-07-14)**
- The INVERSE of the missing-brace problem: a `}` placed TOO EARLY inside a function (e.g. at line 2646 instead of 2710) closes the function mid-body. The remaining 50+ lines of code that were SUPPOSED to be inside the function now execute at TOP LEVEL during script parsing.
- These orphaned lines reference function-local variables (`org`, `canInput`, `orgId`, `dispatchBar`), throwing `ReferenceError` at runtime. This HALTS the entire `<script>` block, preventing all downstream `const`/`let` declarations from executing.
- **Symptom:** Identical to scope-trapping: `typeof` shows globals declared before the orphaned section are defined, globals after are undefined. But the mechanism is different: it's not that the downstream consts are trapped in the wrong scope — it's that a runtime ReferenceError in the orphaned code killed the script before reaching them.
- **How to distinguish from scope-trapping:** In scope-trapping, the function body is intact but too long (no premature `}`). In premature-closure, the function body is split — the `}` appears mid-function, and code that should be inside now runs at global scope.
- **Detection:** Use the Binary Search Sentinel Technique (below). When you find the crash zone, read the code: if you see top-level statements (not inside a function) that reference variables like `org` or `canInput`, those are orphaned lines from a prematurely-closed function.
- **Fix:** Move the closing `}` to after all function body code. Verify the function spans correctly: `switchOrganism` starts at line X, should end at line Y where Y > X + all body code.

**DOM-Rendered window.onerror — When Console Errors Show as Empty Strings (2026-07-15)**
- In some browser automation contexts, `browser_console` returns `js_errors` with `"message": ""` and `"source": "exception"` — the error is detected but the message text is empty. You CANNOT see what crashed. Console messages (console.log) also don't appear, making sentinel probes invisible.
- **Fix:** Inject a `window.onerror` handler as a SEPARATE `<script>` block BEFORE the main script. This handler renders the error directly to a DOM element, bypassing the console entirely:
  ```html
  <script>
  window.onerror = function(msg, src, line, col, err) {
    var d = document.createElement('div');
    d.style.cssText = 'position:fixed;top:0;left:0;right:0;background:red;color:white;font-size:12px;padding:5px;z-index:999999;font-family:monospace';
    d.textContent = 'JS ERROR L' + line + ': ' + msg + (err ? ' | ' + err.message : '');
    document.body.appendChild(d);
    return false;
  };
  </script>
  ```
- The error appears as a visible red bar at the top of the page and shows up in the accessibility tree snapshot as StaticText. Example: `"JS ERROR L2498: Uncaught ReferenceError: org is not defined | org is not defined"` — instantly pinpoints the crash line.
- **When to use:** When `browser_console` shows exceptions with empty messages. When sentinel `console.log` probes don't appear in console output. When you need the EXACT line number of a runtime crash that kills a 500K+ script block.
- **Clean up:** Always remove the error handler script block before committing.
- **Key advantage over sentinel technique:** Sentinels require multiple reload cycles (binary search). The error handler fires on the FIRST load and immediately shows the crash line + message. Use this FIRST, then sentinels only if the error handler doesn't catch it (e.g., SyntaxErrors that prevent `window.onerror` from being registered).

**Binary Search Sentinel Technique for Finding Where Execution Halts (2026-07-14)**
- When top-level script execution silently stops partway through a 10K+ line script block (no SyntaxError, but `typeof` shows variables declared after a certain line are undefined), use sentinel markers to binary search:
  1. Insert `var __TEST_MID = "marker"` at the midpoint of the suspect range
  2. Reload, check `typeof __TEST_MID` — if `undefined`, crash is BEFORE the marker; if `string`, crash is AFTER
  3. Narrow the range by halves until you find the exact line
- **Pattern:**
  ```python
  lines = content.split('\n')
  # Insert at line N (0-indexed)
  content = '\n'.join(lines[:N]) + '\nvar __TEST_N = "marker";\n' + '\n'.join(lines[N:])
  ```
- **Clean up:** Always remove ALL sentinel markers before committing (`content.replace('\nvar __TEST_N = "marker";\n', '\n')`)
- **When to use:** Faster than reading 1000+ lines of code looking for the error. The binary search converges in ~5 iterations for a 1000-line range. Especially useful when the crash is a runtime error (not SyntaxError) that doesn't appear in the console because it happens during top-level execution, not inside a called function.

**`const`/`let` Temporal Dead Zone (TDZ) Crashes init() at Runtime (2026-07-14)**
- A `const PIPELINES = {...}` at line 3963 is accessed by `Object.entries(PIPELINES)` in a function called from `init()` at line 12438. The code is **syntactically valid** (`new Function()` passes), but at RUNTIME, if anything causes `init()` to fire before the assignment at 3963 executes (or if a runtime error between script start and line 3963 halts top-level execution), `PIPELINES` is in the TDZ — accessing it throws `TypeError` or `ReferenceError`.
- **Symptom:** `typeof PIPELINES === 'undefined'` even though the `var PIPELINES = {...}` line is in the file. `init()` throws `TypeError: Cannot convert undefined or null to object` at `Object.entries(PIPELINES)`.
- **Detection:** Call `init()` manually in console to get the exact error + stack:
  ```javascript
  (function(){ try { init(); } catch(e) {
    return e.stack ? e.stack.substring(0,400) : e.message;
  }})()
  ```
- **Fix:** Change `const` → `var` for any top-level constant that is (a) referenced in functions and (b) declared more than ~500 lines into a large script block. `var` hoisting means the variable exists (as `undefined`) from the start, avoiding TDZ crashes. The tradeoff (mutable vs immutable) is acceptable for config objects.
- **Key insight:** Runtime errors between script start and a `var`/`const` assignment line will prevent the assignment from ever executing. This means even after fixing the SyntaxError that caused the crash, you may need to find the NEXT runtime error that was masked by the first one. Debug iteratively: fix SyntaxError → reload → fix TDZ → reload → find next masked error.

**Systematic const→var Conversion for Large Single-File HTML Apps (2026-07-15)**
- In a 10K+ line single-file HTML app where the main `<script>` block is 500K+ chars, `let`/`const` declarations at the top level create temporal dead zones. Any runtime error (even one) between the script start and a `const`/`let` assignment line will prevent that assignment from ever executing, causing cascading failures where variables appear `undefined` despite being in the file.
- **The conversion rule:** Convert ALL top-level `let`/`const` declarations to `var` for any variable that is:
  (a) Referenced by functions called during `init()` or by event handlers
  (b) Declared more than ~500 lines into the script block
  (c) A configuration constant (ROUTE_RULES, PIPELINES, ORGANISMS, etc.)
- **Why `var` is safe here:** `var` hoists the declaration (variable exists as `undefined` from the start), avoiding both ReferenceError AND TypeError-on-undefined in most cases. The tradeoff (mutable vs immutable) is irrelevant for prototype-grade code. The critical property is that `var` declarations survive runtime errors earlier in the script block — the variable EXISTS even if the assignment hasn't run yet, so `typeof` returns `'undefined'` instead of throwing.
- **Arrow functions in const:** `const q = (id) => document.getElementById(id);` should become `var q = function(id) { return document.getElementById(id); };` — arrow functions in `const` declarations are doubly vulnerable (TDZ + arrow syntax issues in older parsers).
- **Batch conversion pattern:**
  ```python
  import re
  # Find all top-level let/const declarations
  for i, line in enumerate(lines):
      stripped = line.strip()
      if re.match(r'^(?:let|const)\s+\w+\s*=', stripped):
          print(f"L{i+1}: {stripped[:80]}")
  ```
  Then convert each one to `var` via patch tool. Do NOT convert `let`/`const` INSIDE function bodies — those are correctly scoped.
- **Key insight:** This is a defensive measure for large prototype files. In production code with proper module boundaries, `let`/`const` is correct. But in a single-file HTML app where one runtime error can silently kill 500K characters of JavaScript, `var` is the safer choice for top-level declarations.

**Node.js Syntax Extraction for Large Inline Scripts (2026-07-15)**
When dealing with a 500K+ char inline `<script>` block in HTML, browser console errors are often empty (`"message": ""`, `"source": "exception"`). Extract the script and check syntax with Node.js instead:
```python
import re, subprocess

# Extract the big inline script from HTML
with open('app.html', 'r') as f:
    html = f.read()
scripts = re.findall(r'<script(?:\s[^>]*)?>(.*?)</script>', html, re.DOTALL)
# Find the big one (usually index 5, 500K+ chars)
main_script = max(scripts, key=len)
with open('/tmp/main_script.js', 'w') as f:
    f.write(main_script)

# Check syntax
result = subprocess.run(['node', '--check', '/tmp/main_script.js'], capture_output=True, text=True)
# returncode 0 = valid. Nonzero = exact error with line number.
```
**Why this beats browser debugging:** `node --check` gives you the EXACT line and column of syntax errors in seconds, without reloading the browser or fighting cache. For "Unexpected end of input" errors (missing brace), use the Brace Count Triangulation below.

**Brace Count Triangulation (2026-07-15)**
When `node --check` reports "Unexpected end of input" (missing closing brace), find how many are missing:
```python
stubs = 'var window = {}; var document = { getElementById: function(){return {};} };'
for n_braces in [0, 1, 2, 3, 4]:
    test = stubs + main_script + ('\n' + '}' * n_braces)
    with open(f'/tmp/test_b{n}.js', 'w') as f:
        f.write(test)
    result = subprocess.run(['node', '--check', f'/tmp/test_b{n}.js'], capture_output=True, text=True)
    if result.returncode == 0:
        print(f'{n_braces} closing braces needed')
        break
```
Once you know the count, track brace depth in the HTML file (accounting for template literals and string literals) to find which function is missing its closing brace. The function with depth never returning to 0 is the culprit.

**Function-Swallowing from Missing Closing Brace (2026-07-15)**
When `switchOrganism()` is missing its closing `}`, it doesn't just trap variables — it swallows ALL subsequent function definitions into its body. Functions like `crystalPopOut()` that appear top-level are actually nested inside `switchOrganism()`. Symptoms: `typeof ROUTE_RULES === 'undefined'` AND `typeof crystalPopOut === 'undefined'` — the first global defined BEFORE the unclosed function works, the first global defined AFTER it doesn't. The cutoff between defined/undefined pinpoints the exact unclosed function.

**Systematic Diagnosis Chain for "Entire Platform Not Working" (2026-07-14)**
When NOTHING works (no telemetry data, no interactive elements, console shows empty exceptions), follow this chain IN ORDER:
-1. **Node.js syntax extraction** (see above) — extract the script block, run `node --check`. This catches ALL syntax issues (missing braces, redeclarations, malformed code) in seconds without browser cache issues. START HERE for any 500K+ script block.
0. **Check the server response** — `curl -s http://localhost:PORT/ | head -3` or check `document.querySelectorAll('script').length` in console. If 0 script tags or raw JSON response → port hijacking (see "Background Process Port Hijacking" above). The HTML file is fine; the browser never received it. This is a 5-second check that saves 30 minutes of JS debugging.
0.5. **Inject DOM-rendered window.onerror** — if step 0 confirms the HTML is loading but JS is broken, inject the error handler (see technique above). This will immediately show the crash line+message as a visible red bar, bypassing empty console errors. Faster than sentinels for runtime crashes.
1. `typeof TELEMETRY_URL` (or any known global) → if `undefined`, the main script block is dead
2. Run `new Function()` per script block → finds SyntaxErrors (redeclaration, malformed code)
3. Check `typeof` for EACH top-level `const`/`var` in declaration order → if some are defined and others aren't, suspect a missing closing brace (scope-trap). The cutoff line pinpoints the unclosed function.
4. Call `init()` manually → finds RuntimeErrors (TDZ, undefined references) with exact line numbers
5. If steps 2-4 don't reveal the issue, use the **Binary Search Sentinel Technique**: insert `var __TEST_N = "marker"` at line N, reload, check `typeof __TEST_N`. Narrow by halves.
6. Fix errors one at a time, reload, re-check — errors mask each other. A SyntaxError masks RuntimeErrors; a TDZ masks scope-traps; a scope-trap masks everything downstream.
7. Once `init()` runs clean, verify data flows: check `ORGANISM_DATA`, `ecgBuffers`, etc.
This is faster than guessing. The stack trace from step 4 points directly at the problem.

**Restore-and-Reapply Protocol for Accumulated Breakage (2026-07-14)**
- When you've made 3+ edit passes on the same large HTML file and things keep getting worse: STOP editing. Restore from the last known-good git commit, then re-apply ALL changes in ONE clean Python script pass.
- This is faster and safer than trying to surgically fix layered breakages (orphaned code, duplicate definitions, extra braces, broken layout all at once).

**Dead/Orphaned Code From Prior Refactors (entire FILE is stale)**
- A `.js` file is still loaded via `<script>` but references globals that were NEVER defined in any loaded file. This happens when a refactor moved definitions to a new file but left the old file loading. The old file's functions silently never execute (or crash when called), but the page still loads because the references are inside function bodies that may not be called on load.
- **Diagnostic pattern:** Pick a symbol the file references (e.g., `DIM_KEYS`, `SleepDimension`). Grep across ALL loaded JS files:
  ```bash
  grep -rn "DIM_KEYS\s*=" js/*.js   # look for the DEFINITION, not usage
  ```
  If the definition appears in ZERO files, the referencing file is dead code from a prior version.
- **Fix:** Either replace the file's contents with working code, or delete it and remove the `<script>` tag from HTML. Do NOT leave dead code loading — it wastes parse time and creates confusion for the next debugger.
- **Key difference from "Undefined References":** Undefined references is about a single missing function call. Dead/orphaned code is about an entire FILE that's stale. The symptom is subtler: the page loads fine, but specific features silently don't work because the functions that would have provided them reference ghosts.

**Layered Syntax Errors — Fixing One Reveals the Next (2026-07-17)**
- In large inline JS blocks with multiple pre-existing syntax errors, the FIRST error (by parse order) silently kills the ENTIRE block. All functions become undefined. Fixing that first error makes the parser advance further — and hit the SECOND error that was previously masked.
- **Observed pattern:** `l'Étude` (unescaped French apostrophe in a single-quoted string) was the first parse error. Fixing it with `\u2019` exposed a second error: a `'the specialist engine': {...}` entry spliced into the wrong data structure (object syntax injected into an array context), producing `Unexpected token ':'`. Both errors killed the same ~17,000-line script block, making `renderStemCells`, `navTo`, `switchMedTab`, and dozens of other functions undefined.
- **Detection:** After each fix, re-run `node --check` on the extracted script block. Do NOT assume the first fix resolves everything. If `node --check` still fails, read the NEW error line — it's the next layered error.
- **Fix protocol for large inline scripts:**
  1. Extract each `<script>` block to a temp file.
  2. Run `node --check` on each. Any non-zero exit = parse error in that block.
  3. Fix errors one at a time, re-running `node --check` after each fix.
  4. When all blocks pass, verify in browser: `typeof renderStemCells === 'function'` (or whatever was missing).
- **Key insight:** When a user reports "you deleted feature X," the cause is often NOT deletion — it's a syntax error that silently killed the script block containing the function. Always check `node --check` before assuming code was lost.

**Unescaped Non-ASCII Characters in JS Single-Quoted Strings (2026-07-17)**
- Biographical text about European scientists frequently contains foreign contractions: `l'Étude`, `d'Alembert`, `Ramón y Cajal`. Inside single-quoted JS strings, the bare apostrophe `'` terminates the string prematurely. Everything after it becomes a syntax error.
- **Detection:** `grep -n "[a-z]'[ÉÀÂÊÎÔÛÜÖÄéàâêîôûüöä]" file.html` — any match is a potential parse-killer.
- **Fix:** Replace bare `'` with `\u2019` (right single quotation mark). Renders identically in browser output, doesn't break JS parser.
- **Cross-file propagation risk:** One parallel file (e.g., the operator agent Live) may use `\u2019` while the other (e.g., GG3) has the literal character. When porting features, scan the target file for this pattern before assuming it's clean.

**Cross-Structure Data Splicing — Object Entry Injected Into Array Context (2026-07-17)**
- When two large data objects coexist in the same script block with different syntax patterns:
  - `ENGINE_KB = { 'the specialist engine': {scientist:'...',...} }` — object syntax (key:value)
  - `ENGINE_CATALOG = { 'nervous': { engines: [{id:'...',name:'...',...}] } }` — array of objects inside system objects
- A paste or merge can inject a `ENGINE_KB`-style entry (`'the specialist engine': {scientist:...}`) into the middle of an `ENGINE_CATALOG` engines array. Result: `SyntaxError: Unexpected token ':'` because the parser expected `{id:...}` array item syntax, not `'Key': {props}` object syntax.
- **Detection:** `node --check` on the extracted script gives the exact line number. Read the surrounding context — if you see `'the specialist engine': {...}` between `{id:'...',name:'...'}` entries, it's a cross-structure splice.
- **Fix:** Remove the misplaced entry (it likely has a correct home in the other data structure). Verify the array/object structure is clean after removal.

**Function-Diff Technique for Detecting Clobber Risk Before Block Replacement (2026-07-17)**
- When porting a feature between parallel files that have diverged, BEFORE doing any block replacement, run a function-name diff to identify what's at risk:
  ```bash
  comm -23 \
    <(grep '^function ' file_TARGET | sed 's/function \([a-zA-Z0-9_]*\).*/\1/' | sort -u) \
    <(grep '^function ' file_SOURCE | sed 's/function \([a-zA-Z0-9_]*\).*/\1/' | sort -u)
  ```
- Output = functions in TARGET that don't exist in SOURCE. If your replacement block's boundaries overlap any of those, abort the block swap and use individual function-level patches.
- **After ALL patches**, re-run the diff to confirm zero functions were lost.
- Functions that use the implicit global `event` variable (e.g., `event.target.closest(...)`) work fine when triggered by real DOM clicks but **crash with TypeError** when called programmatically (via `element.click()` from console, or `dispatchEvent`).
- **Cause:** The global `event` is only populated by the browser during a real user-initiated event handler. In programmatic calls, `event` is `undefined`.
- **Fix:** Guard the reference:
  ```javascript
  if (typeof event !== 'undefined' && event && event.target) {
    const el = event.target.closest('.cal-day');
    if (el) el.classList.add('selected');
  }
  ```
- **Better pattern:** Pass the event explicitly as a function parameter (`onclick="handler(event)"`) rather than relying on the global.

**Canvas-Specific Bugs (critical for chart/visualization prototypes)**
See `references/canvas-rendering-pitfalls.md` for details. Quick checklist:
- **CSS variables in canvas context**: `ctx.fillStyle = 'var(--text)'` does NOT work. Canvas fillStyle/strokeStyle accept hex (`#e2e8f0`), rgb, rgba — never CSS custom properties. Text rendered with a CSS var becomes invisible or black-on-dark.
- **Hardcoded hex values survive CSS variable replacement**: When rebranding a prototype's colors, updating `:root` CSS variables is NOT enough. Canvas code (`ctx.fillStyle = '#10b981'`, `grad.addColorStop(0, '#047857')`) and inline `style="color:#10b981"` attributes use raw hex values that bypass CSS variables entirely. You MUST bulk-replace hardcoded hex values via `sed` across the entire file, then grep-verify zero old colors remain. Pattern: `sed -i '' 's/#oldhex/#newhex/g' file.html` then `grep -c '#oldhex' file.html` must return 0.
- **Math.random() inside draw functions**: redraws (resize, data change) produce different random values each time, making charts flicker and look unstable. Use deterministic values.
- **Canvas default sizing**: `<canvas>` defaults to 300x150 internal resolution regardless of CSS width/height. Must explicitly set `canvas.width = canvas.offsetWidth; canvas.height = canvas.offsetHeight;` before drawing, or everything renders tiny/blurred.
- **Excessive shadowBlur**: values above ~10px create an unreadable neon glow effect. Keep shadowBlur at 6-10 for subtle aesthetics.

**Three.js MeshLambertMaterial on Dark Background = Invisible Geometry (critical for Crystal Hive / dark-theme 3D)**
- `MeshLambertMaterial` and `MeshStandardMaterial` require sufficient directional light to produce visible pixel colors. On a dark background (e.g., `#080d1a`), with typical dim lighting (ambient ~0.5, directional ~0.4), a colored cell (#d4a547 Citrine) renders as approximately RGB(24,15,11) — indistinguishable from the background. The 3D scene appears blank even though the geometry, materials, and camera are all correct.
- **Diagnostic:** Use `renderer.getContext()` then `gl.readPixels()` to sample actual rendered pixels. If all pixels match the background color within a small tolerance, the materials are too dark for the lighting setup.
- **Fix options (in order of preference):**
  1. Switch to `MeshBasicMaterial` — shows true vertex/face color regardless of lighting. Best for Crystal Hive phenotype where depth comes from fog + opacity layering, not dynamic lighting.
  2. If lighting-based shading is required (for depth perception), boost lighting: `ambient 0.8+` and `directional 1.2+` with white light color. Add a fill light from the opposite side.
  3. Use `renderer.setClearColor(bgColor, 1)` and remove `alpha: true` from the renderer config so the WebGL canvas has an opaque dark fill rather than being transparent over the body.
- **Also check fog density:** `FogExp2` at density 0.035 on a camera at distance 14+ units washes out geometry entirely. Reduce to 0.015 or remove fog for closer camera positions.
- **This is NOT the same as "WebGL doesn't work."** The WebGL context exists, meshes are in the scene graph, raycaster hits them, but the rendered pixels are too dark to perceive. Don't waste time debugging context creation or geometry — check the pixel output.

**file:// Protocol Breaks fetch() in Static HTML Prototypes**
- When a prototype uses `fetch('/api/state')` (or any absolute-path API call) and the user opens the file directly via `open index.html` (file:// protocol) instead of through a running dev server, the fetch fails with a CORS or path resolution error. The catch block returns empty data, and `buildScene([])` renders nothing. The user sees a blank page with zero console errors about rendering.
- **Diagnostic:** Check `window.location.protocol` — if it returns `'file:'`, all fetch calls to server endpoints will fail.
- **Fix:** Add a demo data fallback in the catch block:
  ```javascript
  async function state() {
    try { const r = await fetch('/api/state'); return r.json(); }
    catch(e) { return DEMO_DATA; }
  }
  ```
  The DEMO_DATA object should contain 10-18 sample items across all categories so the visual structure renders for design review even without the backend running. This enables designers to preview visuals without starting servers.

**Programmatic QA (when screenshots/vision unavailable)**
See `references/programmatic-qa-methodology.md` for the full 7-phase verification suite. Use browser_console JavaScript expressions to verify interactivity without visual inspection — essential for large prototypes (1000+ lines) or when the vision model is rate-limited. Covers: function existence audit, toggle behavior testing, canvas pixel sampling, click handler dispatchEvent testing, audio engine state verification, and chat flow testing.

**Orphaned JavaScript After `</html>` — Renders as Visible Text (2026-07-14)**
- A function block placed AFTER `</body></html>` with a closing `</script>` but NO opening `<script>` tag is treated by the browser as page content. The JS code renders as **visible text on the page** (you can see raw `function renderEngineHeatmap() { ... }` as StaticText in the accessibility tree). The lone `</script>` also interferes with the real script block's execution, preventing event listener attachment (left-rail nav clicks stop working).
- **Symptom:** Raw JavaScript code appears as visible text at the bottom of the page. Left-rail navigation links stop working. No console SyntaxError (the browser parses it as text, not as a script).
- **How it happens:** An edit appends a function + `</script>` at the very end of the file, after the document already closed with `</body></html>`. The function exists in the file but outside any `<script>` block.
- **Detection:** `grep -n '</html>' file.html` — if ANY code appears after `</html>`, it's orphaned. Also check the browser snapshot for StaticText containing `function` keyword.
- **Fix:** Delete the orphaned code block. If the function is needed, move it INSIDE the last `<script>` block before `</script>`, before `</body>`.
- **Key insight:** This is distinct from all other script killers. The code is syntactically valid JS. The browser doesn't throw an error. It just renders the code as text because there's no `<script>` context around it. The lone `</script>` acts as a rogue closing tag that can unbalance the real script blocks.

**Background Process Port Hijacking — Page Renders as JSON or Raw Data (2026-07-15)**
- A background process (e.g., `gg3_metrics.py --serve`, a Flask/FastAPI server, a metrics collector) silently takes over the HTTP port that was serving your static HTML. The browser loads the page URL and gets raw JSON/text instead of the HTML file. The page appears blank or shows raw data, and `document.querySelectorAll('*').length` returns < 10 instead of hundreds.
- **Symptom:** Page title is empty, `element_count` is 1-7, `document.body.children.length` is 1-2, and `document.body.innerHTML` starts with `<pre>{` or raw data instead of `<div>`. Zero JavaScript runs (no script tags exist in the response).
- **Detection:** `curl -s http://localhost:PORT/ | head -5` — if you see JSON instead of `<!DOCTYPE html>`, a different process is serving that port. Then `lsof -i :PORT` to find the PID and `ps -p PID -o command` to identify what took over.
- **Fix:** Kill the hijacking process (`kill PID`), then restart the static file server (`python3 -m http.server PORT`). If the hijacking process is managed by launchd with KeepAlive, you must unload the plist first.
- **Key insight:** This mimics a JavaScript crash (blank page) but is actually a server-level issue. The HTML file is intact — the browser never received it. Always check `curl` output before debugging JS when the page is blank. The fastest diagnostic: `document.querySelectorAll('script').length === 0` in browser_console means you're not even loading the HTML file.

**`var` Hoisting Without Assignment — Guard Against `undefined` (2026-07-15)**
- `var diagChatHistory = []` on line 7369 is hoisted to the top of the script, so `typeof diagChatHistory` is NOT `undefined` — BUT the value IS `undefined` until line 7369 executes. If `init()` (called at line 12407) triggers `navTo('diagnostics')` which calls `diagChatInit()` before the parser reaches line 7369, the array access `diagChatHistory.length` throws `TypeError: Cannot read properties of undefined (reading 'length')`.
- **Wait — how is this possible?** In a synchronous script block, ALL `var` declarations execute top-to-bottom before `init()` at the bottom. The real trigger: `init()` is called via `archScript.onload` callback (asynchronous), and during that delay, a user click on a nav item fires `navTo('diagnostics')` → `diagChatInit()` while the script is still parsing (large file, slow parse). OR a runtime error EARLIER in the script halted top-level execution before line 7369, so the assignment never happened — but `init()` still ran (it was in a callback registered before the crash).
- **Symptom:** `typeof diagChatHistory` returns `'undefined'` (not `'object'`), even though `var diagChatHistory = []` is in the file. `typeof diagChatInit` returns `'function'`. The error is `Cannot read properties of undefined (reading 'length')` — NOT a ReferenceError.
- **Fix:** Add a null guard at the top of any function that accesses a hoisted `var`:
  ```javascript
  function diagChatInit() {
    var msgs = document.getElementById('diagChatMsgs');
    if (!msgs) return;
    if (!diagChatHistory) diagChatHistory = [];  // ← guard against hoisted-but-unassigned
    if (diagChatHistory.length === 0) { /* ... */ }
  }
  ```
- **Deeper fix:** Find the EARLIER runtime error that halted script execution before the `var` assignment. Use `typeof` checks on globals in declaration order to find the cutoff (same technique as the scope-trap diagnosis). Once the earlier error is fixed, the `var` assignment runs and the guard becomes unnecessary — but keep it as defensive code.
- **Key insight:** `var` hoisting prevents ReferenceError but NOT TypeError on undefined. The variable EXISTS (hoisted) but its VALUE is `undefined` until the assignment line executes. This is the gap between `var` (hoisted, value=undefined) and `let`/`const` (TDZ, access throws ReferenceError).

**Infinite Redirect Loop from Conditional Navigation (2026-07-14)**
- A function like `switchOrganism('gg3')` unconditionally navigates to the organism's expected URL (e.g. `window.location.href = 'http://localhost:port/...'`). When the page is ALREADY being served on that port, the navigation target equals the current URL. The page reloads, `init()` fires again, detects the organism from the port, calls `switchOrganism()` again — infinite loop. The page visibly **flashes/flickers** as it reloads endlessly.
- **Symptom:** Page flickers between states. No console error. The URL doesn't change. Network tab would show repeated full page loads. This is NOT a JS error — it's a control-flow bug (navigation to self).
- **Root cause:** `switchOrganism()` was written to ALWAYS redirect (for cross-port navigation), but `init()` calls it unconditionally on every page load to set the default organism from the serving port. The redirect-to-same-page creates the loop.
- **Detection:** Search for `window.location.href` assignments inside any function that `init()` also calls. If the function navigates unconditionally and `init()` calls it unconditionally, you have a loop.
- **Fix:** Compare the target port against the current serving port. Only redirect when they differ:
  ```javascript
  function switchOrganism(orgId) {
    var _expectedPort = _orgPortMap[orgId];
    if (_expectedPort && SERVING_PORT !== _expectedPort) {
      window.location.href = 'http://localhost:' + _expectedPort + '/...';
      return;  // different port -> navigate
    }
    // same port -> update UI in place, no reload
    TELEMETRY_URL = org.telemetryUrl;
    // ... update labels, title, etc.
  }
  ```
- **Key insight:** This is the **navigation analog** of the premature-closing-brace bug. The brace bug orphaned code at global scope; this bug orphans an entire page lifecycle. Both produce "entire platform broken" symptoms but through different mechanisms (script halt vs reload loop).
- **How it differs from a broken href:** A single broken `window.location.href` fails silently (page doesn't change). A redirect LOOP fails loudly (page flickers). If the user reports flickering/flashing, suspect a redirect loop, not a broken link.

**Cross-System Navigation: Always Open New Tabs (2026-07-14)**
- When multiple independent systems share the same HTML file (e.g., the operator agent Live at :port and GG3 at :9300 both serve `gg-ops-platform.html`), the org switcher must use `window.open(url, '_blank')`, NEVER `window.location.href`. Same-tab navigation between systems causes:
  - **Flashing** even after fixing redirect loops (the page navigates away, init() re-fires, detects wrong system)
  - **Context loss** (user was doing work on the operator agent Live, now loses their place)
  - **System confusion** (no visible URL change in some browsers when ports are similar)
- **Pattern for multi-system switchers:**
  ```javascript
  function switchOrganism(orgId) {
    var _expectedPort = _orgPortMap[orgId];
    // Different port = different system = NEW TAB
    if (_expectedPort && SERVING_PORT !== _expectedPort) {
      window.open('http://localhost:' + _expectedPort + '/gg-ops-platform.html', '_blank');
      // Revert currentOrganism since we didn't actually switch
      currentOrganism = Object.keys(ORGANISMS).find(function(k) {
        return _orgPortMap[k] === SERVING_PORT;
      }) || 'gg-live';
      return;
    }
    // Same port = same system = update UI in place
    TELEMETRY_URL = org.telemetryUrl;
    // ... update labels, title, etc.
  }
  ```
- **Key rule:** `window.location.href` is for navigating WITHIN one system (same port). `window.open('_blank')` is for navigating BETWEEN systems (different ports). Mixing them up is the #1 cause of multi-system flashing.
- **launchd KeepAlive respawn:** If a process is managed by launchd with `KeepAlive=true`, `kill <pid>` respawns it immediately. You MUST update the launch script (e.g. `gg3_launch.py`) to change the port or binary, then `launchctl unload` + `launchctl load` the plist. Killing alone is futile — launchd brings it back within seconds.

**HTML Div Nesting Imbalance — Browser Reparenting Causes Layout Collapse (2026-07-17)**
- In large single-file HTML apps with deeply nested flex layouts, extra or missing closing `</div>` tags cause the browser parser to **reparent** elements to unexpected locations in the DOM. The source HTML looks correct (indentation suggests correct nesting), but the browser's error-correction parser silently relocates misplaced elements.
- **How it manifests:** A left sidebar (`.rail` inside `.app`) collapses to `height: 0` because a sub-tab panel that should be inside a `.workspace` gets reparented to `.app-shell` (a direct child, sibling to `.app`). When the panel renders at full page width outside the flex container, the `.app` container (holding the rail) has no content and collapses.
- **Detection — DOM parent vs source position mismatch:**
  ```javascript
  // Check where each panel ACTUALLY lives in the parsed DOM
  ['birthTab-studio', 'birthTab-requests', 'birthTab-organisms', 'birthTab-analytics'].forEach(function(id) {
    var el = document.getElementById(id);
    console.log(id + ' parent: ' + (el ? (el.parentElement.id || el.parentElement.className) : 'MISSING'));
  });
  // If any panel's parent is 'app-shell' instead of 'ws-birthing', the browser reparented it
  ```
- **Root cause — premature container close:** A sub-tab panel (e.g., `studioProductMode`) was placed AFTER 3 closing `</div>` tags that closed its parent containers (`studioCanvas`, flex-container, `birthTab-studio`). The browser parser then treated the panel and all subsequent siblings as children of `.app-shell` rather than children of `ws-birthing`. The 3 extra closing divs that appeared later (intended to close those containers) instead closed `.app`, `.main`, etc., cascading the breakage upward.
- **Fix — div depth tracing:** Trace open/close div depth from a known container start to find where depth goes to 0 (premature close) or negative (extra closes):
  ```python
  import re
  depth = 0
  for i in range(start_line, end_line):
      line = lines[i]
      opens = len(re.findall(r'<div[\s>]', line))
      closes = len(re.findall(r'</div>', line))
      depth += opens - closes
      if depth <= 0:
          print(f"L{i+1}: depth={depth} | {line.strip()[:60]}")
  ```
  The fix: ensure each container's closing `</div>` appears AFTER all its children, not before. Move misplaced closing divs to the correct position.
- **Key insight:** This is the HTML structural analog of the JS brace-balance bugs. JS braces kill script blocks; HTML div imbalance kills layout. Both are invisible in code review (indentation looks plausible) and only surface via DOM inspection or visual testing. The symptom (sidebar disappears on sub-tab switch) is the layout analog of "all functions become undefined" — one structural error cascades to break the entire layout tree.
- **Cascading depth shift after removing premature closes (2026-07-17):** Removing misplaced closing `</div>` tags shifts the entire nesting chain downstream. Containers that were previously "correct" (because the extra divs were compensating for the misplacement) may now close at the wrong point. For example, removing 3 premature `</div>` tags inside `birthTab-studio` caused `.main` (which wraps ALL workspaces) to close before `ws-marrow` and `ws-connections`, orphaning those workspaces outside the flex layout. **Always re-trace div depth from the fixed location all the way to the outermost container after any div removal.** The fix at one point in the file can break something at a completely different point because the browser parser consumes close tags differently with the adjusted depth.
- **Verification:** After fixing, check that all panels report the correct parent (`ws-birthing` not `app-shell`), AND verify the rail stays visible across all sub-tabs:
  ```javascript
  ['studio', 'requests', 'organisms', 'analytics'].forEach(function(tab) {
    switchBirthTab(tab);
    var rail = document.querySelector('.rail');
    console.log(tab + ': rail height=' + rail.getBoundingClientRect().height);
  });
  // All should show height > 100 (e.g., 557px). If any shows 0, nesting is still broken.
  ```

**Double-`style` HTML Attributes — Second One Silently Dropped (2026-07-16)**
- When a string-built HTML element has TWO `style="..."` attributes (e.g., `'<td style="padding:4px" class="mono" style="font-size:9px">'`), the browser applies ONLY the first and silently discards the second. No error, no warning. The CSS from the second attribute (font-size, color, etc.) is lost.
- **How it happens:** Incremental string concatenation in JS template-building functions. A developer adds `style="font-size:9px"` to an existing `<td>` that already has `style="padding:4px 10px"` without merging them. Common in `.map(r => '<tr>...<td style="A" ... style="B">...')` patterns.
- **Detection:** Regex scan the entire file:
  ```python
  import re
  double_styles = re.findall(r'style="[^"]*"\s+class="[^"]*"\s+style="[^"]*"', html)
  # Also catch without class between them:
  double_styles2 = re.findall(r'style="[^"]*"\s+style="[^"]*"', html)
  ```
- **Fix:** Merge both styles into a single attribute: `style="padding:4px 10px;font-size:9px"`. Keep `class` separate.
- **Key insight:** This is invisible in code review because the HTML looks plausible. Only a regex scan or visual inspection (missing font-size, missing color) reveals it. Always scan for this pattern after editing string-built table rows.

**Orphaned Function Referencing Non-Existent DOM IDs (Silent No-Op) (2026-07-16)**
- A function like `loadMedSpawns()` calls `document.getElementById('medSpawnBody')` but no element with that ID exists anywhere in the static HTML or in any dynamically-generated template. The function is dead code: it fetches data, the getElementById returns null, the `if (!body) return` guard exits silently. No error, no user-visible effect.
- **How it happens:** A feature was prototyped (spawn request form in Medical Bay) but the HTML panel was never added to the page. The JS functions (`loadMedSpawns`, `medSubmitSpawn`, `medSelectSpawnType`) remain in the file but reference DOM elements that were superseded by a parallel implementation (the Birthing Center's `loadBirthSpawns`). The tab switcher (`switchMedTab`) never calls the orphaned function.
- **Detection — trace the call chain:**
  1. Find the function: `grep -n 'function loadMedSpawns' file.html`
  2. Find call sites: `grep -n 'loadMedSpawns()' file.html` — if only called from within itself or a sibling orphan, it's dead
  3. Check if the tab switcher calls it: `grep -n 'loadMedSpawns' inside switchMedTab function body`
  4. Check if the DOM element exists: `grep -n 'id="medSpawnBody"' file.html` — if zero hits, the function can never execute its body
- **Fix:** Either add the missing HTML panel + wire the tab switcher to call it, OR delete the orphaned functions to reduce confusion. Patching orphaned functions (adding buttons, fixing styles) is wasted effort — the code never runs.
- **Key difference from "Dead/Orphaned Code From Prior Refactors":** That pitfall is about an entire FILE being stale. This is about individual FUNCTIONS within a live file that reference ghosts. The file is loaded and running, but these specific functions are unreachable.

**Cross-Script-Block Function Availability — Function Defined in LATER Block Undefined in EARLIER Block (2026-07-16)**
- In multi-`<script>` block HTML files, `<script>` tags execute sequentially in document order. If Block 5 calls `fetchTelemetryCached()` but that function is defined in Block 8, the function is `undefined` when the call executes. The `typeof` guard (`if (typeof fn === 'function')`) correctly returns `false`, and the call is silently skipped.
- **Symptom:** `typeof fetchTelemetryCached` returns `'undefined'` in the console, even though `grep 'function fetchTelemetryCached' file.html` finds the definition. `ORGANISM_DATA` stays `null`. UI shows "Connecting to organism telemetry..." forever. No error in console.
- **Detection:** Run `typeof` for the suspect function AND a function known to be in the same script block. If the suspect is `undefined` but the known one is `function`, the suspect is in a different `<script>` block. Then find which block each function is in:
  ```python
  import re
  scripts = re.findall(r'<script(?:\s[^>]*)?>(.*?)</script>', html, re.DOTALL)
  for i, code in enumerate(scripts):
      if 'function fetchTelemetryCached' in code: print(f"Defined in Block {i}")
      if 'fetchTelemetryCached()' in code: print(f"Called in Block {i}")
  ```
- **Fix options (in order of preference):**
  1. Move the function definition into the same block as its caller (inline scripts only)
  2. Move the init call into a `DOMContentLoaded` handler in the same block as the definition
  3. Declare a global stub at the top of the calling block: `var fetchTelemetryCached;` then assign in the defining block
- **Key insight:** This is NOT TDZ, NOT scope-trapping, NOT a syntax error. The function literally doesn't exist yet when the earlier block executes. Brace balance checks pass. `node --check` passes. Only runtime `typeof` reveals the issue. This is the multi-block analog of "Functions Defined Inside `<script src="external.js">` Blocks" — the earlier block can't see what hasn't loaded yet.

**Proxy Routing Glob Prefix Misroute — `/api/spawn*` Catches `/api/spawn-requests` (2026-07-16)**
- A reverse proxy with prefix-based routing can accidentally catch unrelated endpoints. Pattern: `/api/spawn` as a gateway routing prefix matches BOTH `/api/spawn-requests` (medical server) AND any other `/api/spawn*` path. The spawn-requests endpoint gets silently routed to the wrong backend and returns 404.
- **Symptom:** Direct backend call works (`curl http://localhost:port/api/spawn-requests` returns JSON) but proxy call fails (`curl http://localhost:9300/api/spawn-requests` returns `{"error": "HTTP Error 404"}`). Browser fetch fails silently with no visible error.
- **Detection:** Always test both direct backend AND through-proxy. If direct works but proxy fails, audit ALL prefix patterns in the proxy's routing logic for glob collisions.
- **Fix:** Remove the overly broad prefix. Use more specific prefixes or move the endpoint to the catch-all route.

**Systematic Regex Audit for Large HTML Files (2026-07-16)**
- In a 1MB+ single-file HTML app, bug patterns repeat across dozens of string-built functions. Fixing one instance without scanning for ALL instances guarantees recurrence. After fixing any pattern, run a batch audit.
- **Audit script template** (run via Python in terminal):
  ```python
  import re
  with open('app.html') as f: html = f.read()
  
  # 1. Double-API URL bugs (base ends in /api/, path starts with api/)
  bad_urls = [c for c in re.findall(r"fetch\([\'\"]([^\'\"]+)", html) if c.count('api/') > 1]
  
  # 2. Double-style attributes
  double_styles = re.findall(r'style="[^"]*"\s+style="[^"]*"', html)
  
  # 3. Unnormalized status fields (checking one shape when API returns another)
  # e.g., code checks e.alive (boolean) but API returns status: "alive" (string)
  
  # 4. Buttons with 'undefined' text
  undefined_btns = re.findall(r'<button[^>]*>undefined</button>', html)
  
  # 5. onclick handlers referencing undefined functions
  onclicks = set(re.findall(r"onclick=\"[^\"]*?(\w+)\(", html))
  all_fns = set(re.findall(r'function\s+(\w+)\s*\(', html))
  missing = {f for f in onclicks - all_fns if f not in ['event','open','close','clear']}
  
  print(f"bad_urls={len(bad_urls)} double_styles={len(double_styles)} missing_fns={missing}")
  ```
- **When to run:** After any fix that touches a repeating pattern (URL construction, style attributes, status normalization). One fix should trigger a scan for ALL sibling instances. The user catches when you fix one of six and miss the other five.
- **Automated scan:** Run `python3 scripts/html-audit-scan.py <file.html>` to check for all patterns above in one pass. Returns exit code 1 if errors found.

**Double-Firing onclick Handlers (nested elements)**
- A card div has `onclick="importCSV()"` AND an inner button has `onclick="importCSV(event)"`. Clicking the button fires BOTH handlers due to event bubbling. The file picker opens, closes, or opens twice.
- **Cause:** Event bubbles from the button up to the card. Both onclick attributes fire.
- **Fix:** Remove the redundant inner handler (keep only one), OR call `event.stopPropagation()` in the inner handler. The cleanest fix is to have only the container-level handler.
- **Diagnostic:** If users report "the file picker opens twice" or "I click and nothing happens" (the second handler cancels the first), check for nested onclick attributes.

**stopPropagation Pattern for Inline Delete/Action Buttons on List Items (2026-07-17)**
- When a clickable list item (e.g., session sidebar entry with `onclick="openSession(id)"`) contains a nested action button (e.g., delete trash icon with `onclick="deleteSession(id)"`), clicking the inner button fires BOTH handlers — the delete fires, then the parent's open fires, opening the session you just deleted.
- **Fix:** ALWAYS pass `event` to the inner handler and call `e.stopPropagation()` as the first line:
  ```javascript
  function deleteSessionFromList(e, id, title) {
    e.stopPropagation();  // CRITICAL — prevents parent onclick from firing
    // ... actual delete logic
  }
  // In the rendered HTML:
  '<div class="session-delete" onclick="deleteSessionFromList(event,\'' + s.id + '\')">'
  ```
- **CSS pattern for hover-reveal action buttons:**
  ```css
  .session-delete { opacity: 0; transition: opacity 0.15s; }
  .session-item:hover .session-delete { opacity: 0.5; }
  .session-delete:hover { opacity: 1 !important; color: var(--red); }
  ```
- **General rule:** ANY nested interactive element inside a clickable container needs `stopPropagation` in its handler. Without it, the parent handler always fires after the child handler.

**Honest API Documentation (no phantom endpoints)**
- Prototypes sometimes advertise API endpoints that don't exist (e.g., a "Web API" section showing `POST /api/score` when there's no server). This misleads users and developers.
- **Fix:** Replace phantom API docs with the ACTUAL interface the code exposes. If the scoring engine is a JavaScript class, show how to import/instantiate it directly. If there's a real API, verify it with `curl` before documenting it.
- Verify event listeners are attached to the correct elements
- Check that element IDs match between HTML and JavaScript
- Ensure event listeners are added after DOM elements exist (use DOMContentLoaded or place scripts at end of body)

**Scope and Timing Issues**
- Check if code runs before DOM elements are loaded
- Verify variable scopes (especially in loops or callbacks)
- Look for race conditions in asynchronous code

### 3. Specific Fix Patterns

**Fixing Undefined References**
```javascript
// BEFORE (causing error)
audioPlayer.stopAll();

// AFTER (correct reference)
AudioEngine.stopAll();

// OR if the variable should exist but doesn't:
const audioPlayer = {
  stopAll: function() { /* implementation */ }
};
```

**Completing Stub Functions**
```javascript
// BEFORE (incomplete — reads metric but never assigns to state variable)
function setupMetricToggle() {
  document.getElementById('metricToggles').addEventListener('click', e => {
    // Missing implementation
  });
}

// AFTER (complete — note the critical `currentMetric = metric` line)
let currentMetric = 'score'; // state variable the render function reads

function setupMetricToggle() {
  const container = document.getElementById('metricToggles');
  if (!container) return;
  
  container.querySelectorAll('.metric-toggle').forEach(btn => {
    btn.addEventListener('click', () => {
      const metric = btn.dataset.metric;
      currentMetric = metric;  // ← THIS LINE IS CRITICAL. Without it, buttons highlight but chart never changes.
      
      // Update active state
      container.querySelectorAll('.metric-toggle').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      
      // Redraw chart with selected metric
      drawTrend(document.getElementById('trendCanvas'));
      
      // Save preference
      localStorage.setItem('8dsleepMetricPreference', metric);
    });
  });
  
  // Load saved preference
  const saved = localStorage.getItem('8dsleepMetricPreference');
  if (saved) {
    currentMetric = saved;  // ← Also set state on load, not just on click
    const btn = container.querySelector(`.metric-toggle[data-metric="${saved}"]`);
    if (btn) {
      btn.click();
    }
  }
}
```

**Ensuring Proper Event Attachment**
```javascript
// BEFORE (may not work if element not yet in DOM)
document.getElementById('gaugeCanvas').addEventListener('click', showScoreBreakdown);

// AFTER (safe - waits for DOM)
function setupGaugeClick() {
  const gauge = document.getElementById('gaugeCanvas');
  if (!gauge) return;
  
  gauge.style.cursor = 'pointer';
  gauge.title = 'Click to see what contributes to your sleep score';
  
  gauge.addEventListener('click', showScoreBreakdown);
  
  // Add hover effect
  gauge.addEventListener('mouseenter', () => {
    gauge.style.opacity = '0.9';
  });
  
  gauge.addEventListener('mouseleave', () => {
    gauge.style.opacity = '1';
  });
}
```

### 4. Verification Steps
After each fix:
1. Clear browser console (click the clear button)
2. Hard refresh the page (Cmd+Shift+R / Ctrl+F5) — browser caching will show old JS otherwise
3. **Actually click the element you fixed** — do not claim it works based on code review alone. Use `browser_click` on the ref, then check the result.
4. Verify no new errors appear in console
5. Test related elements to ensure you didn't break anything
6. Try edge cases (rapid clicking, changing states, etc.)
7. **Take a screenshot** if visual elements (charts, canvases, layouts) were changed. Visual bugs (overlapping text, neon glow, misaligned elements) are invisible in code but obvious in a screenshot. Do not claim visual fixes are done without looking at the rendered output.
8. **For domain-specific prototypes** (like 8D Sleep): Verify that the interactive elements correctly represent the intended framework (e.g., in 8D Sleep, sleep should be treated as a sub-dimension, not a primary dimension)

### 4a. Programmatic Verification via browser_console (when screenshots/vision unavailable)
When the vision model is rate-limited, the prototype is too large for a single screenshot, or you need to verify many interactive elements quickly, use `browser_console` with JavaScript expressions to programmatically confirm interactivity WITHOUT visual inspection. This is often faster and more thorough than clicking each element manually.

**Step 1: Batch-check all handler functions exist:**
```javascript
JSON.stringify({
  toggleCard: typeof window.toggleCard,
  sendMessage: typeof window.sendMessage,
  playSound: typeof window.playSound,
  loadPreset: typeof window.loadPreset
})
```
Any `undefined` result = UI element pointing to a missing function. This catches the common "HTML shell exists but JS never written" failure instantly.

**Step 2: Test toggle behavior (before/after class check):**
```javascript
(() => {
  const card = document.getElementById('card-0');
  const before = card.classList.contains('expanded');
  window.toggleCard(0);
  const after = card.classList.contains('expanded');
  return `before=${before} after=${after}`;
})()
```

**Step 3: Verify canvas rendering (sample FULL canvas, not just corner):**
```javascript
(() => {
  const canvas = document.getElementById('myCanvas');
  const ctx = canvas.getContext('2d');
  const imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
  let nonEmpty = 0;
  for (let i = 3; i < imgData.data.length; i += 4) {
    if (imgData.data[i] > 0) nonEmpty++;
  }
  return `total=${canvas.width*canvas.height} drawn=${nonEmpty} pct=${(nonEmpty/(canvas.width*canvas.height)*100).toFixed(1)}%`;
})()
```
**Pitfall**: Sampling only the top-left corner (e.g., `getImageData(0,0,100,100)`) gives false negatives — the canvas may be rendered in the center/bottom. Always scan the full canvas or sample at known node positions.

**Step 4: Sample specific pixel colors to verify correct rendering:**
```javascript
(() => {
  const ctx = document.getElementById('myCanvas').getContext('2d');
  const cx = canvas.width / 2, cy = canvas.height / 2;
  const center = ctx.getImageData(cx, cy, 1, 1).data;
  return `centerRGBA=[${center[0]},${center[1]},${center[2]},${center[3]}]`;
})()
```
Compare RGBA values against expected hex colors (e.g., `[251,191,36,255]` = `#fbbf24` gold).

**Step 5: Test click handlers programmatically:**
```javascript
(() => {
  const canvas = document.getElementById('myCanvas');
  const rect = canvas.getBoundingClientRect();
  canvas.dispatchEvent(new MouseEvent('click', {
    clientX: rect.left + 100,
    clientY: rect.top + 100,
    bubbles: true
  }));
  const modal = document.getElementById('modalOverlay');
  return `modalVisible=${modal && modal.style.display !== 'none'}`;
})()
```

**Step 6: Verify audio engine state:**
```javascript
JSON.stringify({
  ctxExists: !!AudioEngine.ctx,
  ctxState: AudioEngine.ctx ? AudioEngine.ctx.state : 'null',
  activeSounds: Object.keys(AudioEngine.active || {})
})
```
`ctxState === 'running'` confirms audio is actually playing, not just initialized.

See `references/programmatic-qa-methodology.md` for the full verification suite pattern.

### 5. Pitfalls to Avoid
- **Assuming elements exist** - Always check if `getElementById` returns null before using the element
- **Claiming a fix works without clicking it** - The #1 trust-killer. If you say "fixed" but didn't actually click the button / open the modal / see the chart change, the user will catch it and lose trust. ALWAYS verify through real interaction before reporting success.
- **Not screenshotting visual changes** - Canvas rendering bugs, overlapping text, and layout issues are invisible in code. If you changed anything visual, take a screenshot and look at it before claiming the fix is done.
- **Forgetting hard refresh** - Browser caches JS aggressively. After editing, a normal refresh may load the old file. Use Cmd+Shift+R (Mac) / Ctrl+F5 (Windows) or append `?v=N` to the URL.
- **Overwriting existing functionality** - When overriding methods, preserve the original if needed
- **Memory leaks** - Remove event listeners when appropriate (though less critical in prototypes)
- **Blocking the main thread** - Avoid long-running loops or heavy computations in event handlers
- **Not preserving state** - When fixing slider/data sync, ensure all related UI updates correctly
- **Domain confusion** - In health/wellness prototypes like 8D Sleep, understand the domain model correctly (e.g., sleep is a sub-dimension of wellness, not a primary dimension unto itself)
- **Ignoring medical coding context** - For health applications, respect relevant medical coding references and ensure simulated data is clearly marked as mock/prototype

### 6. Testing Checklist
- [ ] Buttons respond to clicks with visual feedback
- [ ] Sliders update related values in real-time
- [ ] Toggles change state and persist preferences
- [ ] Modals open and close correctly
- [ ] Tooltips appear on hover/interaction
- [ ] Audio plays/stops with proper controls
- [ ] Timers count down correctly and expire
- [ ] Charts update when data changes
- [ ] No JavaScript errors in console during normal use
- [ ] Responsive behavior works on different screen sizes

## Medical Coding Context (for 8D Sleep)
When working on 8D Sleep prototypes specifically:
- All scoring must run locally (no API calls in JavaScript) - respects medical coding DS-ECS-04.01.01 (Physical dimension, sleep subsystem)
- Respect medical coding references like DS-ECS-04.01.01 (Physical/Sleep/Scoring)
- Ensure any simulated data clearly marked as mock/prototype
- Validate that the interactive elements correctly represent the intended 8D Sleep framework where sleep is a sub-dimension, not a primary dimension
- Remember that in the 8D framework, sleep optimization serves the 8 dimensions, rather than being a dimension itself

**Function Hoisting vs Var Initialization — Functions Live, Variables Die (2026-07-17)**
- Function declarations (`function wizardOpen() {...}`) are **hoisted** to the top of the script block during parse. They exist and are callable from the very first moment, regardless of where execution currently is.
- Variable declarations (`var wizardState = {...}`) are **hoisted as undefined** but their **assignments** execute in-order during the execution phase. If a runtime error occurs anywhere between the script start and the assignment line, the assignment never runs — the variable stays `undefined`.
- **Critical pattern:** You can have `typeof wizardOpen === 'function'` (hoisted, alive) while `typeof wizardState === 'undefined'` (assignment never ran). This is NOT the same as scope-trapping (where the var exists but in the wrong scope). The var genuinely never got assigned.
- **Detection:** Check `typeof` for both the function AND the variable. If function is `'function'` but the variable it depends on is `'undefined'`, a runtime error killed execution before the assignment. Use the Binary Search Sentinel Technique to find where execution stopped.
- **Common cause:** An override or assignment line like `var _origStudioTemplate = studioTemplate;` placed AFTER the variable declarations but BEFORE the end of the script. If `studioTemplate` is somehow unavailable at that point (timing, scope, or it was never defined in this block), it throws and kills everything above it that hasn't been assigned yet. Wait — that's backwards. The assignment lines BELOW the error don't run, but the ones ABOVE do. Functions defined ANYWHERE in the block are hoisted.
- **Actually, the precise mechanism:** In a single `<script>` block:
  1. Parse phase: ALL `function` declarations are hoisted (they work immediately).
  2. Execution phase: `var` assignments run top-to-bottom. If line N throws a runtime error, lines N+1 through EOF never execute. But functions defined at ANY line were already hoisted in step 1.
  3. Result: `typeof anyFunction === 'function'` but `typeof anyVarDeclaredAfterLineN === 'undefined'`.
- **The fix for large injected code blocks:** When injecting a large block of JS (wizard, new feature) into an existing script block, place ALL `var` declarations at the TOP of the injected block, before any executable statements or function overrides. This ensures the variables are assigned before any runtime code can throw. If an override like `_origStudioTemplate = studioTemplate` must run, put it in a try-catch or at the very end after all critical initializations.
- **Even better fix:** Put injected code in its OWN `<script>` block at the end of the HTML file. This isolates it from runtime errors in the main script block. Functions are global across script blocks, so `wizardOpen()` called from the main block still works.

**Mid-Script Injection — Code Splits Across Scope Boundaries (2026-07-17)**
- When you inject a block of JS between two existing functions in a large single-file HTML app (e.g., between `toggleSpawnHarness()` and `submitSpawnFromScreen()`), the injected code is in the SAME `<script>` block as the surrounding code. This means:
  - A runtime error in the injected code kills ALL downstream variable assignments in the entire block.
  - A runtime error BEFORE the injection point (in the existing code) prevents the injected `var` assignments from ever running.
  - The injected functions are hoisted and callable, but the injected variables may not be initialized.
- **Detection pattern for injected blocks:** After injection, verify BOTH functions and variables:
  ```javascript
  // Functions should be hoisted and available
  typeof wizardOpen        // 'function' ✓
  typeof wizardRender      // 'function' ✓
  // Variables may NOT be initialized if a runtime error occurred
  typeof wizardState       // 'undefined' ✗ = execution halted before this line
  typeof WIZARD_ENGINES    // 'undefined' ✗ = same
  ```
  If functions are alive but variables are dead, the injection point has a runtime error between the last working variable and the first dead one.
- **Fix:** Move the injected code to a separate `<script>` block at the end of the file. Cross-block function references work fine. Within the new block, the variables initialize without interference from the main block's runtime errors.

**Over-Escaped Single Quotes in String-Built onclick HTML (2026-08-12)**
- When building HTML strings in JS that include `onclick="fn('\'' + id + '\'')"`, incorrect escape depth produces `\\\\'` (4 backslashes) instead of `\\'` (2 backslashes). The browser parser sees the extra backslash as escaping the wrong character, producing a `SyntaxError: Unexpected string` that kills the ENTIRE `<script>` block.
- **How it happens:** Incremental edits to string-built onclick handlers where someone "fixes" the escaping by adding more backslashes, not realizing they've gone too deep. Common in publications/drafts views where onclick handlers pass IDs and string literals like `viewRunResult('id', 'veritas')`.
- **Detection:** `node --check` on the extracted script block gives the exact line number. The error is `SyntaxError: Unexpected string` at the line with the over-escaped quotes.
- **Fix:** Match the escape depth used by WORKING onclick handlers in the same file. If line A uses `\\'` (2 backslashes) and line B uses `\\\\'` (4 backslashes), normalize B to match A.
- **Key insight:** This is NOT just a broken onclick — it kills the ENTIRE script block. ALL functions become `undefined`. The page renders HTML fine (CSS works) but nothing is interactive. `typeof switchView === 'undefined'`, `typeof loadDashboard === 'undefined'`, etc. This is the same class of failure as `const` redeclaration and missing braces, but caused by string-escaping errors rather than structural JS errors.

**CSS Grid Column Alignment QA — getBoundingClientRect vs offsetLeft (2026-08-12)**
- When building a database-style grid view (sortable columns, aligned header + rows), you MUST verify header and row columns share the EXACT same `grid-template-columns`. A mismatch as small as 20px in the `1fr` column causes visible misalignment.
- **The offsetLeft trap:** `element.offsetLeft` returns position relative to `offsetParent`. If the header's offsetParent differs from the row's offsetParent (common when one has `position:sticky`), the values are in different coordinate systems and CANNOT be compared. You'll see a 285px "mismatch" that doesn't exist.
- **Correct measurement:** Always use `getBoundingClientRect()` which is viewport-relative regardless of offset parent:
  ```javascript
  var header = document.querySelector('.draft-grid-header');
  var row = document.querySelector('.draft-row');
  var hSpans = header.querySelectorAll('span');
  var rCells = row.querySelectorAll('.draft-cell');
  var problems = [];
  for (var i = 0; i < hSpans.length; i++) {
    var hr = hSpans[i].getBoundingClientRect();
    var rr = rCells[i].getBoundingClientRect();
    if (Math.abs(hr.left - rr.left) > 1 || Math.abs(hr.right - rr.right) > 1) {
      problems.push('Col ' + i + ': header=' + Math.round(hr.left) + '-' + Math.round(hr.right) +
                    ' row=' + Math.round(rr.left) + '-' + Math.round(rr.right));
    }
  }
  // problems.length === 0 means perfect alignment
  ```
- **The flex-vs-grid trap:** If the header uses `display:grid` with `grid-template-columns` but rows use `display:flex` with individual `flex` properties, they will NEVER align. Convert both to the same CSS Grid template string. Write it ONCE and apply to both `.draft-grid-header` and `.draft-row` — they must have identical `grid-template-columns`.
- **textContent concatenation artifact:** When a cell contains multiple spans (e.g., `<span class="doctype">PDF</span><span class="title">Paper Title</span>`), `cell.textContent` returns `"PDFPaper Title"` with no separator. This is a measurement artifact, NOT a rendering bug. To verify visual separation, measure the gap between the spans: `titleSpan.getBoundingClientRect().left - doctypeSpan.getBoundingClientRect().right`. A gap of 8-14px means they're visually separated.

**Using Puppeteer MCP for JS Verification (2026-08-12)**
- When debugging Writing Studio or other localhost-served HTML apps, the Puppeteer MCP tools provide faster iteration than manual browser inspection:
  1. `mcp__puppeteer__puppeteer_navigate` to load the page
  2. `mcp__puppeteer__puppeteer_evaluate` with `typeof functionName` to check if functions are alive
  3. If ALL functions are `undefined`, the script block has a fatal parse error — extract with Python regex and run `node --check` to find it
  4. After fixing, re-navigate and verify `typeof functionName === 'function'`
  5. Use evaluate to test click behavior: `document.querySelector('[data-draft-id]').click()` then check if the editor view became visible
- **Advantage over browser_console:** Evaluate runs synchronously in the page context, returns structured JSON, and doesn't require screenshots (useful when vision model is unavailable). Can chain multiple checks in one expression via `JSON.stringify({...})`.
- **Pattern for verifying multiuser scoping:** Set identity via `setUserIdentity('Name')`, wait for async reload, then count cards: `document.getElementById('dashRecent').querySelectorAll('[data-draft-id]').length`

**Multiuser Draft Scoping in Single-File HTML Apps (2026-08-12)**
- When a writing platform serves multiple authors (the principal Williams, the principal Gilchrist), the identity selector should support BOTH org-level ("see all drafts") and personal-level ("see only my drafts") views.
- **Implementation pattern:**
  - Store current scope in `localStorage` (`ds_current_author`)
  - Default to org view ("Divinity Science") so new users see everything
  - Add "Divinity Science (Org)" as the first `<option>` in the identity selector
  - Create `isOrgView()` and `filterDraftsByScope(drafts)` helper functions
  - Call `_loadRecentActivity()` and `loadDrafts()` on identity change to re-filter
  - Show author badges on cards ONLY in org view (redundant in personal view)
  - When creating new drafts in org view, default author to a real person (not "Divinity Science")
- **Pitfall:** The dashboard Recent Activity panel and the full Drafts list must use the SAME data source and the SAME filter. If they fetch from different endpoints or apply different filters, users see discrepancies. Both should call `/api/drafts?stage=all` and both should pass through `filterDraftsByScope()`.

**Silent Auto-Save for Ephemeral Results (2026-08-13)**
- When a feature generates results (brainstorm angles, analysis output, search snapshots) that the user expects to find later, a manual "Save" button with prompt() dialogs is effectively NO save. Users never click it. The results vanish on page refresh.
- **Symptom:** User says "I don't see the brainstorms saved" or "where did my results go." Investigation reveals the save endpoint exists, the save button exists, but zero records in the database because the save UX required 3 manual steps (click tiny button, answer prompt 1, answer prompt 2).
- **Fix:** Auto-save silently on completion. Fire and forget. No prompts, no alerts, no user interaction required:
  ```javascript
  async function _autoSaveBrainstorm(d) {
    if (!d || !d.angles || !d.angles.length) return;
    try {
      await fetch(API + '/api/brainstorm/save', {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ seed: d.seed, angles: d.angles, /* ... */ })
      });
    } catch(e) { /* silent fail */ }
  }
  // Call immediately after results render:
  renderBrainstormResults(d);
  _autoSaveBrainstorm(d);  // no await, no blocking
  ```
- **Key principle:** If the user expects results to persist, they should persist automatically. Manual save is an anti-pattern for generated content. The only thing that should require manual action is DELETION or EDITING of saved content.

**Consolidating Separate Views via Filter Chips (2026-08-13)**
- When two related content types (brainstorms + drafts) live in separate sections of the app, users can't find them. The fix: merge them into ONE list view with a filter chip bar.
- **Pattern:**
  1. Add a filter chip (e.g., `<button class="filter-chip" data-draft-filter="brainstorm">Brainstorms</button>`) to the existing list's filter bar
  2. Wrap the original render function: if filter === 'brainstorm', fetch from the brainstorm API and render cards in the same container; otherwise call the original function
  3. Rename the section from the narrow term ("Drafts") to a broader umbrella ("Workshop") to signal the consolidation
- **Why this works better than a separate page:** users navigate to one place, see a filter chip for what they want, click it. No hidden sections. The mental model is "Workshop has everything I'm working on, I filter to narrow down."
- **Pitfall:** When wrapping a render function (`_renderDraftGrid`), rename the original to `_renderDraftGridOriginal` and create a dispatcher that checks the filter. Don't duplicate the original function body.