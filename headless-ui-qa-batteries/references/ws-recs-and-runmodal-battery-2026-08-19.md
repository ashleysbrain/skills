# Writing Studio recommended-topics + run-modal battery (pass 2, 2026-08-19)

Session record for the adversarial QA pass on Research Studio :port. Battery:
`/tmp/ws_qa_pass2.cjs` (8/8 PASS). Full defect table lives in the repo at
`organism/WRITING-STUDIO-QA-LEDGER.md` — this file captures the transferable
mechanics.

## Defects this pass proved (patterns worth re-checking anywhere)

1. **Status-mapping gap**: a pipeline wrapper enumerated completion statuses
   (`complete`, `complete_with_errors`, ...) but NOT `complete_with_quality_issues`,
   so finished runs polled as "running" forever (memory + DB). Rule: whenever a
   wrapper maps an enum from a subsystem, diff the wrapper's cases against every
   status string the subsystem can actually emit (grep the producer, don't trust
   the consumer).
2. **Shape lie in monitoring**: a monitor read `len(draft_content)` and reported
   "5 chars" — the field was a dict with 5 keys. Rule: assert the TYPE
   (`isinstance(x, str)`) before asserting length; a tiny number on a big field
   usually means you're measuring container metadata.
3. **Kind starvation in ranked feeds**: pure score-sort filled the default top-N
   with one category (cross-pollination scored 5-8; emerging threads ~3-5; system
   gaps 3.5 never surfaced). Fix: per-kind quota guarantee before final sort.
   Applies to any "deterministic recommendation" surface.
4. **try/catch swallowing render crashes**: `const content` + `content +=` threw
   "Assignment to constant variable" on EVERY run-detail view; the catch printed
   "Error loading results: <msg>" and the console stayed clean. Batteries must
   assert rendered text (search for "Error loading" and "[object Object]"), never
   trust console-clean as pass.
5. **String coercion in rendered values**: `resultBox(label, value)` and
   `v.join(', ')` on arrays-of-objects produced "[object Object]" rows. Fix:
   stringify objects/elements, truncate long strings.
6. **Quoted-material exemption in cleanup sweeps**: a banned-word/em-dash
   rewriter ran over full drafts INCLUDING the References block — real title
   "Network Robustness and Fragility" became "Network strong and fragility",
   en-dash page ranges "5468–5471" became ", ". Fix pattern: split at the
   `## References` heading (`_split_refs`); body gets cleanup + voice gates,
   references stay verbatim; replacements case-preserving (Robust→Strong). Any
   deterministic text-rewrite pass needs a quoted-material boundary.

## Battery mechanics learned (probe bugs, not product bugs)

- `page.evaluate` returns SERIALIZED JSON. `const el = await page.evaluate(...)` then
  `el.click()` throws `(intermediate value).click is not a function`. Do the click
  inside the evaluate, or use `page.click(selector)` for real hit-testing.
- Duplicate IDs across legacy/active views: resolve the visible instance inside
  evaluate via `offsetParent !== null`; select among duplicates with
  `[...document.querySelectorAll('#id')].find(e => e.offsetParent !== null)`.
- Async-rendered lists need `page.waitForSelector('#list [data-rec-write]', {timeout: 8000})`,
  not a fixed 1300ms sleep — cards painted after a fetch missed the window.
- Classify cards by text on the `.card` ancestor (CROSS-POLLINATION / EMERGING
  THREAD / SYSTEM PROBLEM) — don't assume a `data-kind` attribute exists.
- Runs/results live in the Activity view behind `viewRunResult('<run_id>','veritas')`;
  the modal id is `#runResultModal`. Compose title field is `#wsNewTitle`, filled
  ~120ms after the panel opens — wait before probing.
- Workshop Start button has no id: find by text `/start writing/i` inside `#view-drafts`.
- Intercept `window.fetch` for `/api/veritas/run` inside evaluate to prove the
  click path WITHOUT spending a 12-minute LLM run.

##chrome-headless-shell discovery (fixes stale setup)

Old pinned path (mac-131.0.6778.204, wrong dir casing) failed with "executable
doesn't exist". Working invocation on this host (x86_64):

```bash
CHS=$(ls -d ~/.cache/puppeteer/chrome-headless-shell/mac-*/chrome-headless-shell-mac-x64/chrome-headless-shell | sort -V | tail -1)
node battery.cjs   # with executablePath: process.env.CHS
```

(mac-149.0.7827.22 was current at pass time; discovery beats pinning.)

## Editing-discipline note (model hazard)

Large `patch` new_strings produced corrupted tokens (e.g. `"realm": "amber"`,
`_re.escape(apply)`, `\u2014` escaping into a string literal) — the known
glm-5.3 long-context tail failure. Lint caught every one. Rules that saved the
session: (a) run the linter/py_compile after EVERY patch, not at the end;
(b) read the exact current text before writing old_string; (c) fix corruption
tokens one-by-one with narrow patches rather than re-issuing the big block.
