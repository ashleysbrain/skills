# Probe-discipline addenda — QA pass 4 (2026-08-20, Writing Studio)

Rules 6-10 extending "The five rules that catch real bugs" in SKILL.md. Born from a live data-loss incident + five probe bugs that each cost a battery run.

6. **Destructive bulk checks may only select rows they can name.** A "select all + bulk delete" verification ran against real data and the unguarded hard-delete endpoint destroyed ~25 real rows (recoverable in part only). Stage identifiable fixtures (unique prefix like `QA4-0820`), select ONLY those — populate the app's selection state directly (e.g. `_bsSelection[id] = true` + matching checkboxes) or filter cards by fixture prefix — and freeze a DB copy (`cp db /tmp/freeze.db`) BEFORE the first destructive click. Background auto-save pollers overwrite freed SQLite pages within minutes, so the freeze delay decides recoverability.
7. **`position:fixed` elements report `offsetParent === null` by spec** — visibility probes for fixed bulk-bars/toasts must use `getComputedStyle(el).display !== 'none'`. (Cost a false "bar hidden" product-bug verdict.)
8. **`networkidle` never settles under polling apps** — a 5s batch poller keeps the network busy forever; navigate with `domcontentloaded` + a fixed sleep instead. (Cost a 30s goto timeout.)
9. **`page.reload` wipes injected fetch wrappers and window state** — make the wrapper installer idempotent (`if (window.__wrapped) return;`) and reinstall after every reload, or post-reload captures read as `undefined.filter` and crash the battery. (Cost a mid-run CRASH.)
10. **Playwright `evaluate` takes max 1 extra argument** — pass `{id, tag}` objects, not positional args (throws "Too many arguments"). (Cost a mid-run CRASH.)

Related product-side lessons from the same pass live in `writing-studio-operations` → `references/qa-pass-4-deep-falsification-2026-08-20.md` (archive-by-default deletes, `status=all` filter lie, scores-guard render crash, stored XSS in angle render).
