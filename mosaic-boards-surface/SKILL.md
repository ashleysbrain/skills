---
name: mosaic-boards-surface
version: 1.0.0
author: the operator agent Agent
license: MIT
description: Use when editing the taskcal boards app or comments cards.
metadata:
  hermes:
    tags: [boards, ui, mosaic, comments, toggles]
    related_skills: [ceo-referral-intake-route, gg-ops-platform-ui]
---

# the OS Boards Surface

## When to Use

- Editing anything in `/<workspace>` (server, shell renderers, boards.db cards).
- Minting or repairing comments/referral cards, syncing studio drafts onto the board (see `references/comments-kit-delivery.md`).
- Adding any principal-facing control (toggle, chip, filter) to the surface.
- Deploying/restarting the boards app or verifying it live.

The principal-facing boards app: task calendar, comments queue, joint profile, dynamics band, brain mixer. This is a product surface with a design bar, not an admin tool.

## Architecture + deploy loop

- App: `/<workspace>` — `task_calendar_boards.py` (HTTP server, do_GET/do_POST), `app_shell_v3.py` (render fns), `boards.db` (items, brain_toggles, design_changes, events).
- Deploy: `launchctl kickstart -k gui/$(id -u)/com.your-org.taskcal-boards`, then `curl -s -m 10 http://100.107.113.11:port/<path>` and parse the HTML programmatically (count `class="ccard"`, check for literal `{`/`}` leaks). Crash log: `boards/taskcal-boards.err`.
- Always restart + live-curl after any edit; a syntax-clean file with a crashing handler renders 000/blank and looks like "the feature disappeared".
- A kickstart can leave the OLD PID serving: launchd reports the label healthy, old pages 200, but every NEW route 404s — disk and memory disagree. After kickstart, verify the server PID actually changed (`ps` start time) before curling; if stale, `kill <PID>` and let keepalive respawn, then re-curl. A new-route 404 right after a successful kickstart means stale process, not bad route wiring.

## Always-on laws

1. **Core-flow primacy.** New functionality folds into existing core flows (FLW-TELEMETRY, FLW-INTAKE, flow-registry.json) — telemetry events, rollups, ledger. Side tables and side endpoints get rejected as "building on top of the system, not into it".
2. **Design cadence + notice.** Iterate design multiple times/day freely, but a MAJOR feature/function change ships only after notice. Log every visible change in `design_changes` at ship time (rendered in /changes tab).
3. **Controls are enforcement points.** A toggle/dropdown/chip that only changes display gets rejected. Every principal-facing control must bind to the layer that enforces it (see Brain Mixer chain below): flipping it changes routing, dispatch, or security posture, measurably.
4. **Paste-ready cards.** Every ready comment card carries the FULL body plus a Tap-to-copy button, plus status and register-level chips parsed from a JSON block in the `reasoning` field (rows without the block render chip-less — never crash on old rows). Text living only in drafts.db or the studio is invisible to the principal; mint the board card with the body.
5. **Phenotype.** Warm charcoal + gold tokens, Manrope/Sora, numbers never mono-styled as body text. Hand-drawn SVG icons (thin strokes) for tabs — letter-glyph icons read as sloppy art. No raw JSON/HTML engine surfaces ever shown to the principal; route them to a designed page or do not expose.
6. **Never delete features in a sweep.** Art or platform "revamp" sweeps restyle what exists; a feature is removed only when the principal explicitly names it. A sweep that trims controls, tabs, or data "to clean things up" is a defect shipped as a deliverable — additive revamps only.

## Brain Mixer → Brain Gate chain (controls-are-enforcement, canonical)

- `brain_toggles` table in boards.db is the single writer target; the surface's `/api/brains?key=<k>` endpoint is the only writer.
- `organism/brain_gate.py` is the read side: `active_set()`, `routable(key)`, `require(key)`. Fails CLOSED for unknown/off specialists, OPEN for the two identity entities (principal, the operator agent).
- `sherman_router.py` `find_engine_for_situation`: both routing passes (static TASK_ROUTING + registry lookup) zero the score of off-brains.
- `organism/action_broker.py` `_brain_gate_row`: candidate rows naming an off-brain ("DS <Name>") get score 99 (unclaimable) + a physics note.
- Defaults: ALL seats ON; toggling off is the deliberate act.
- Source the toggle registry from the LIVE engine roster (ports/health census), not a static agents.yaml list — the live fleet is larger than any snapshot.
- Prove the binding behaviorally each side: OFF → task reroutes/refused; ON → routes normally; broker gated-count drops to ~0 when all on.

## Adding a new board + tab (whole-surface pattern)

1. `INSERT OR IGNORE INTO boards (id) VALUES ('b-<name>')` — the boards table is the registry; then mint items with explicit `id` + `seq` (slug-id law: implicit ids land NULL and never render).
2. Renderer in `app_shell_v3.py` returning `_page(tab, title, sub, body)` — there is NO `_frame`/active-arg helper; copy the `render_comments_frame` card shape (`ccard`, chip, `clean_title`, `_e` double-escape) so the surface stays one design.
3. Tab registration is TWO edits in `app_shell_v3.py`: an entry in `_TABS` (key, label, href) and a hand-drawn SVG in `_TAB_ICONS` (24x24 viewBox, stroke 1.6, same family as the others — letter-glyph icons read as sloppy).
4. Route in `task_calendar_boards.py` `do_GET` — add the `if p == "/<name>"` branch beside `/comments`.
5. Log the visible change: `design_changes` is a VIEW, not a table — INSERT into `events` with `kind='design-major'` and body shaped `'<what> | why: <why>'`; the view derives ts/cls/status from it.
6. Boards that carry living brand assets (art program, program docs) may inline the SVG from `brand/mosaic-os/iterations/` directly into the card HTML — SMIL animations run inline; reference the program doc by `file://` URL on the card.

## Adding a new surface: build WITHIN, never bolt on (principal catch, twice)

When adding any new capability to the boards app, the instinctive first cut
is a standalone page with its own `<!doctype html>` chrome — that is a
rejected side structure. The lawful shape on the FIRST cut:

1. Renderer returns through `_page(tab, title, sub, body)` — the shell owns
   ALL chrome (head, CSS, fonts, tab bar, copy JS). An engine module should
   expose a BODY-only renderer; the shell composes. Retro-deleting standalone
   chrome after shipping is rework a review pass should never have to catch.
2. Entry point lives INSIDE the surface it belongs to (a drawing instrument
   links from the Art tab), never a bare floating route. Do NOT add a tab to
   `_TABS` — the tab set is principal-sized (8→5 by her order); new capabilities
   enter through an existing tab's body.
3. Offline-test the body renderer, restart, then live-curl the route AND the
   host tab (both 200, the tab links the new route) and confirm the page
   carries `tabbar` + the shell fonts.
4. When the first cut ALREADY shipped as a standalone page (engine module
   rendering its own PAGE constant with doctype chrome), the refactor is:
   split the engine into a body-only renderer (cut everything above the
   instrument markup), add a `render_<name>(q)` in app_shell_v3.py that calls
   `_page("<host-tab>", ...)`, and re-point the route in
   task_calendar_boards.py from the engine's page renderer to the shell
   renderer. An entry link on the host tab's body (`<a class="btn"
   href="/<route>">`) makes the capability discoverable without a new tab.
   Commit the fold separately from the original build so the principal catch and
   its repair are both auditable.

## Live-render routes (no board, no cache) — the `/roster` shape

Some surfaces are PURE live renders with no db board behind them: `/roster` (organism icons, principal order "always live versions") imports the deterministic engines in-process (`importlib.util.spec_from_file_location` on `brand/mosaic-os/src/*.py`) and re-renders every icon per request. Pattern:

1. Skip the `boards` INSERT — there is no `b-roster` board and no items; the roster list (org id, label, genome, receipt line) lives in the renderer. Do NOT "fix" this by minting cards with cached SVGs; liveness is the requirement.
2. Tab + route + CSS as usual (rostergrid/rslot classes exist). Genome `living` renders the operator agent from her measured ledger state; `day1` renders any other organism from the spin-up engine.
3. Engine `render()` returns a PATH — write to a scratch file, read the SVG back, unlink, THEN embed (a page that 200s can still be serving literal `/dev/null` as icon text).
4. Verify by fetching twice and slicing each `rslot` from the HTML: both slots contain `<svg`, the living slot's state label (receipts count, spine laws, date) reflects today's live counts, zero pixels/refs of a retired color gene inside the grid.

## Art Division hero — one LIVE butterfly, toggled

The Art tab's stage-0 hero renders the organism butterflies under principal layout
law; this section is binding for any edit that touches it:

1. **Toggles first, then ONE large live butterfly** (320px) that switches with
   the toggle. A static film/lineage SVG file NEVER occupies the hero — lineage
   assets belong in the Lineage section below the cards.
2. **Every render is live from the same engine as the grove**
   (`_organism_butterfly_svg(name, joined, now)` called at request time) — "the
   art IS this organism". A toggle that swaps between three pre-baked pictures
   is not live: if the toggle is ever reported "not live", first prove the
   renders DIFFER (SVG content hash + branch count per aview), then look for
   the missing CHANGE-visibility, which is usually the absence of per-organism
   history, not stale rendering.
3. **Each organism carries its OWN five-stage life timeline under its big
   render** (birth species form → today on the gold track, stages at
   0/.25/.5/.75/1.0 of tenure, `today · day N` labels distinct per organism).
   Toggle-switching must show visibly different growth stories — that visible
   change is the liveness the principal audits.
4. **The toggle is the interim control by principal order** — a better alternative
   (grove-as-hero: all butterflies visible in one living row, tap-to-expand
   with timeline, no mode switch) is the parked candidate; do not swap the
   interaction model without an explicit principal order.
5. **Verify live, not offline-only**: curl `/art`, assert the toggle chips
   appear BEFORE the first `<svg>`, `class="aview"` count == organism count,
   each aview contains its own timeline strip, and the day labels are DISTINCT
   per organism. Then commit and ledger (FLW-QA-PASS flow, ui lane).

## Exposing an internal service to the principal's phone

Check the bind address first (127.0.0.1 = unreachable from Tailscale; relaunch with `--host 0.0.0.0` through its watchdog script so it survives restarts), then verify from the Tailscale IP with curl. But hand the principal a DESIGNED surface link, never the raw gateway endpoint.

## Pitfalls

- Never `.format()` a string containing JavaScript — braces are treated as fields and the JS leaks literal `{n}` into the page (chip count 0, dead buttons). Concatenate or escape. The deeper failure mode: `.format()` RAISES on any unescaped brace, so the builder falls through a `try/except Exception: pass` to an empty embed and the page serves WITHOUT its scripts — HTTP 200, tens of KB smaller than expected, static fallback stays. Splice JS with `str.replace('__TOKEN__', js)` only; flip the builder's except to `raise` while authoring; grep the SERVED bytes for a marker from the new JS before browser testing. Escaping braces (`{{ }}`) for `.format` breaks the JS itself, and a later partial collapse of those escapes shifts brace balance into the uninvoked-IIFE class below.
- **A `}}`-collapse or brace-shift can leave a script that PARSES but NEVER RUNS** (uninvoked IIFE): one function short a closing `}` shifts every trailing scope, so the tail `})();` closes an inner function instead of invoking the IIFE and all top-level calls (`tick(); setInterval(...)`) end up inside a body nothing calls. `node --check` passes; signature is script-in-DOM + manual `eval` of its text works + zero console/fetches from it while other page scripts run + static fallback persists. Diagnose with a cumulative per-line brace-balance scan (depth must be 1 at top-level statement lines inside an IIFE, last non-empty line exactly `})();`), and prevent with an execution probe — assert a first-line `console.log` marker or `typeof <fn>` in the same playwright pass that checks the UI. A parse gate alone proves nothing about execution.
- **The patch tool DOUBLES backslashes inside escaped-quote JS strings it inserts** — a patch whose new_string contains `\'` (JS onclick with Python-escaped quotes) lands in the file as `\\'`, which is a SyntaxError ("unexpected character after line continuation character") on first import. After ANY patch that carries escaped quotes, run `python3 -c "import ast; ast.parse(open('<file>').read())"` immediately; on failure, repair with a scripted `src.replace(bad_block, bad_block.replace(chr(92)+chr(92)+chr(39), chr(92)+chr(39)))` slice edit rather than another patch round (which re-doubles).
- `PRAGMA table_info(items)` before any INSERT — the column is `board_id`, not `board`; failed inserts surface later as "card missing".
- Comments view filter set is ready/hold/all only; anything else coerces to `ready`. Cards in other statuses (new/posted/revise) are invisible on the default view — check status before concluding a card vanished. A card stuck in `revise` from a parity test silently hides from Ready.
- A card's `reasoning` field can go stale while its panel record advanced (final unanimous pass after earlier attempts): the status flip to `ready` and the reasoning update are separate writes — reconcile BOTH in the turn the final panel lands, or a later warrant audit reports a defect that no longer exists.
- sqlite3.Row has no `.get()`. A helper that calls `r.get(k)` on Row objects raises AttributeError inside its try/except and silently gates nothing — the call site reports "gate ran" while zero rows were affected. Subscript with a per-key try/except, and prove the helper BOTH standalone on a synthetic dict AND through the live caller's row type.
- Importing a sibling module by bare `import name` when the file lives in another directory: the ImportError lands in the surrounding except and silently selects the fallback (gate = None, routing unchanged). Use importlib.util with a path built from `__file__`, joining relative to the module's OWN directory — a module already inside `organism/` joins `dirname(__file__), "brain_gate.py"`, not `dirname, "organism", "brain_gate.py"`. An off/on behavioral test through the real entrypoint catches both failure shapes.
- Trailing a pipeline segment with `| tail -1` hides the real exit code of the failing command (the pipeline returns tail's). Re-run the failing command unpiped to see the true status.
- `b-posts` renders read-only at `/posts` (archive frame: badges + body, no edit/status buttons); ACTION-class post cards (the operator agent posts needing tap-to-copy or status changes) still file on `b-comments` because the edit/status API and the action-button stack bind to the comments renderer — `kind='post'` + `status='ready'` on b-comments renders with tap-to-copy exactly like a comment card. The gg_posts bank (`writing-studio/linkedin_metabolism.db`) stays the system of record for posts: register the post there (status `pending_review`) AND file the b-comments card — the card is the delivery surface, not the record, and posting state is tracked in the bank.
- `/track` is a GET handler; POST 404s.
- Render-fn constants drift (BOARDS vs BOARDSDB path) — grep the constant at the query site.
- **Ledger CLI from the boards workspace: `--submit` is a FLAG with required `--title --kind --lane --flow`; `--flow` takes FLW-* codes only (grep flow-registry.json `"code"` keys — a bare word like `ui` raises unknown-flow); `--claim` and `--complete` both require `--by <operator>`; and a `--complete` on an unclaimed id fails ("not claimed?") — the lawful sequence is submit → claim --by → complete --by --outcome, capturing the printed task id at submit." The gates script lives at `your-org/your-stack/gates/task_ledger.py` (NOT under your-workspace).
- sqlite3 rows have no `.get()`; helpers fed Row objects must subscript with try/except, and a silent except around a helper makes a gate "run" while gating nothing. Test standalone AND through the live caller.
- **A multi-point scripted splice that corrupts a large render file is repaired from git, not layered.** Symptom: ast.parse fails at a def far from the edit site, or a helper is referenced before its definition — the splice landed mid-function and left a dangling half. Fix: `git checkout <last-good-commit> -- <file>`, re-apply the whole change as ONE insertion at a verified def boundary (helpers above their first call site), then ast.parse + grep for duplicate `def` names + offline render battery BEFORE kickstart. Repair edits stacked on the chimera inherit its damage and cost more than the restore.
- **Stage multi-card inserts as a JSON payload file, never inline heredoc.** Triple-quoted card bodies inside a Python list inside a shell heredoc collide on quotes and abort the script with a SyntaxError AFTER sibling steps (mint, bus, commit) already ran — a partially-filed wave across systems. Write the card bodies to a scratch JSON file first, INSERT from it, verify the max-seq/readback, and only then run mint/bus/commit.
- **A row filed under a wrong board id saves silently and never renders.** boards.db accepts any `board_id` string; every view filters one exact id (`b-comments` for comments). After filing a card, grep the LIVE route for its id — a saved-but-invisible card is a board-id typo, not a rendering bug.
- **Card kind must match the surface's action list, or the card is invisible with zero errors.** The comments action-list renderer draws from `kind='referral'` rows; filing a digest card as `kind='card'` commits cleanly and renders nowhere on the principal's list. Before inserting, read back one recent canonical row (SELECT the latest by seq) and copy its `kind`, `channel`, receipt-shape, title pattern (`SCIENCE DIGEST [+ BUILD REVIEW] - name (source)`), body section order, and empty-string-vs-NULL conventions verbatim; format drift on a live principal board is a visible defect the principal catches, not a cosmetic one.
- **Default pagination can bury new work behind old rows.** If the surface paginates oldest-first with a small page size, newest cards land on the last page and read as "missing"; either bump the ordering rule (fresh knowledge digests lead for a window) or verify the new card's page explicitly before reporting it live.
- **Key DOM ids on a unique column, never on seq.** boards.db carries duplicate seq values on b-comments (0, 3, 7, 8, 9, 76, 998, 999 each appear twice); card ids `c{seq}`/`cmt{seq}` collided so Copy grabbed the first match and anchors broke. Suffix ids with the unique item id (`c{seq}-{iid}`) and keep focus-pin matching a substring test so `cmt{f}` still pins `cmt{f}-{iid}`. Pass condition: fetch every page of the listing and count duplicate id attributes across all of them — zero duplicates.
- **Re-measure reported surface defects on the LIVE port before fixing.** An audit finding measured against a dead legacy surface (old :port) can describe a defect the current surface already fixed — pagination flagged "dead, pages byte-identical" was live-correct on :port (md5-diff page=1..3 distinct proves the param reaches the renderer). Confirm which port the principal actually loads, reproduce there, and fix only what still reproduces.
- **Write `updated_at` in one UTC house format.** Views sort timestamps as raw strings; a naive local `2026-10-13 10:12:00` sorts against UTC-aware `2026-10-13T15:12:00Z` values bytewise and newest cards land mid-list or below older ones. UTC-with-offset on every write, hand-fixes included.
- **A broad `except` around a new renderer branch hides a missing module import.** A NameError (e.g. `json` used but not imported at module level) raised inside `try/except` renders the feature silently absent — no error, no chips. When a renderer branch gains a new stdlib use, grep the module-level imports, then offline-verify by importing the file via importlib and asserting the NEW marker string appears in the rendered HTML; the degrade-to-no-chip fallback for old rows is why the except exists, so only the marker test catches the swallowed failure.

## Verification checklist

- [ ] Restart via launchctl, curl the changed path (Tailscale IP), parse HTML for the expected markers?
- [ ] Card counts + copy buttons present; no literal brace leaks?
- [ ] If a control was added: proven binding both states (off/on) at the enforcement layer?
- [ ] Visible change logged in design_changes (major flagged + pre-noticed)?
- [ ] New data paths folded into an existing flow, not a side structure?
- [ ] New capability renders through `_page` shell chrome + enters via an existing tab (no standalone page, no new tab)?
