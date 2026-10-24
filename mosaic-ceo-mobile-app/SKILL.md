---
name: mosaic-ceo-mobile-app
description: "Upgrade the principal's phone app surface surgically, with proof."
version: 1.0.1
author: curator
license: MIT
metadata:
  hermes:
    tags: [mobile-app, ceo-surface, mosaic-os, surgical-edit, bounded-lists]
    category: software-development
---

# the OS principal Mobile App

## When to Use

- Any change to the principal-facing mobile app surface (renderer, server, lists,
  home, tab bar, badges).
- The principal asks "where is the link", reports the interface changed or went
  dead, or asks for app dynamism/inspiration upgrades.
- The principal reports missing controls ("old drop down buttons and
  functionality I used to have") — that is a parity regression on the
  canonical surface; treat it as sev-1 and inventory what the old surface
  had before touching anything else.
- Adding any new list to the app (bounded-portion law applies).
- Minting/closing ledger tasks for this surface (proof-gate rules apply).

The principal's canonical app: a phone-first shell (bottom tab bar Home · Calendar ·
Tasks · Comments · Body, warm dark phenotype, safe-area aware) served by the
boards stack (task calendar server + a self-contained HTML renderer module).
This skill governs how to change it without breaking the relationship the principal
has with it.

## Hard laws (every change)

1. **Canonical-surface law.** When the principal asks "where is the link" or "this
   is not the interface I had", FIND and RESTORE the existing surface. Never
   spawn a parallel surface in answer to that question — a new port reads as
   a rebuild and a loss. A dead canonical page is sev-1, not a footnote.
2. **Surgical upgrade only.** No rebuilds. The tab bar, navigation model, and
   visual identity are the interface the principal knows; upgrade pattern-by-pattern
   so the principal never opens a stranger. Keep the renderer self-contained.
3. **"Designed for a human" is the bar.** Retail-app-grade dynamism "in the
   right ways": greet by name, show live measured state, act in one tap.
   Dynamic does not mean infinite feed.
4. **Numbers on the surface are live reads, never hardcoded** — including
   uncomfortable ones (a rising swap figure on the home strip is the surface
   doing its job).
5. **Functionality conservation.** Never reduce reachable functionality in
   a design change unless the removed thing is validated dead (zero live
   uses). Collapsing content into a one-line stub, hiding a control, or
   pushing it below the fold all count as removal — re-exposing the
   capability must land in the same ship, not a follow-up.
6. **Parity conservation on migration.** When a surface becomes canonical,
   inventory every affordance of the one it replaces BEFORE shipping: grep
   the old code for `<details>`, `<select>`, `onclick`, form buttons, copy
   handlers, and port each one (or record it validated-dead). A canonical
   app that can do less than the board it replaced is a regression the principal
   finds by touch — missing buttons read as taken-away functionality even
   when the old surface still runs on its old port.
7. **Analytics on every change.** Every interactive control (copy, filter
   chip, expand, status button) posts to a server-side /track endpoint
   writing an events table, and an /analytics page summarizes counts +
   last-touch per control. Feature life or death is read from counters,
   never guessed — the ecosystem adapts on measured usage.

## Change procedure (in order)

1. Read the renderer functions you will touch (home, tasks list, comments
   frame) before editing; patch surgically, never rewrite the module.
2. Syntax-check both renderer and server files (`ast.parse`) before restart.
3. Restart: the server imports the renderer ONCE at startup — live edits are
   invisible until restart. If a launchd KeepAlive agent owns the port
   (boards stack: `com.your-org.taskcal-boards`), deploy ONLY via
   `launchctl kickstart -k gui/$(id -u)/<agent>` — a manual kill+relaunch
   races KeepAlive (ThrottleInterval ~30s) and LOSES, so the principal keeps
   seeing ghost code from an old process born before the patch. **After
   relaunch, verify the LISTENING pid's start time** (`lsof -nP -iTCP:<port>
   -sTCP:LISTEN` then `ps -o lstart= -p <pid>`) is AFTER the patch: file
   state proves nothing; only the birth time of the process actually
   serving the port does.
4. Verify on the REAL external URL with curl + grep for the expected marker
   strings (greeting text, portion counters, tab labels). A looser grep
   pattern (`marker.{0,60}`) is needed when markup sits between the text and
   its count span. Localhost 200 does not mean the principal's phone can reach
   the surface: servers that bind 127.0.0.1 by default are invisible on the
   Tailscale URL. Verify the external IP too; when a gateway must be
   phone-reachable, set the bind (0.0.0.0) in the watchdog/launch script
   that relaunches it — patching only the running process reverts on the
   next watchdog cycle.
5. Client-side truth: server-verified is not principal-verified — an open phone
   tab renders its cached page while curl returns the new one. Every page
   carries a visible version+clock stamp in its header, and reports to the
   principal end with "the header should read <stamp>" so one line back from
   them identifies exactly which version they are seeing.
6. Affordance visibility: an affordance that sits below a full portion list
   is unreachable. Any collapsed or buried section gets a jump link with
   its count in the first screen (e.g. "N journal notes — tap to jump
   down"), not only a DOM presence somewhere down the page.
7. Analytics hooks ship WITH the feature, not after (hard law 7) — every
   new control logs its taps on day one, and the mutation path is proven
   by a live round-trip: POST the route on a real card, read the DB back,
   restore the original value, then report.
8. Commit in the repo that actually owns the file (watch for symlinked
   module directories committing elsewhere).
9. Ledger: mint via submit with a registered flow code (read the flow
   registry; invented codes are refused). Close = claim (with `--by`) then
   complete, and the outcome MUST carry inline proof next to every verdict
  word (URL + exit code + output excerpt + file/lines + commit hash) — the
  proof gate refuses naked "live/verified" claims AND outcomes that quote
  exit codes with no command context anywhere (no path, flag, or tool
  named reads as a forged artifact): paste the actual command lines
  (curl URL, sqlite query, file + offset), not just their exit statuses. Strongest form: save the
   verification output itself to a receipt file (e.g. the curl'd HTML) and
   anchor its absolute path in the outcome. Mint failures on the GENOME
   line mean the format is strict — pull an existing ledger task's detail
   and copy its exact GENOME shape, and use a canonical organ-system name
   for the body field rather than free text.

## List behavior: bounded portions, never infinite scroll

The principal's standing order: lists must be dynamic differently — infinite
scroll is rejected behavior, fixed with science through the intake process.

- Initial portion 15–20 cards; explicit "Show N more (M left)" button; a
  progress line ("1–15 of 60"); an "End of list" marker; footer always
  reachable; NEVER auto-append on scroll.
- Each portion boundary is a deliberate decision point (continue or act on
  what was seen) — that is the feature, not a limitation.
- **Clamp the page parameter** to the real page count before slicing — an
  out-of-range page renders "61–60 of 60" style inverted ranges.
- The research base (portion-cue science, agency findings, mobile
  thresholds, and the isomorphism with deformations) is in
  `references/list-design-science.md`. Re-derive parameters from it when a
  new list surface is added; do not re-run the search.

## Home surface patterns (retail-app inspiration)

- Time-of-day greeting by first name, then ONE line of live context
  (measured vitals, model counts). Not a dashboard wall.
- Badges with real counts belong on the tab bar (needs-you state visible
  without navigation).
- Ship one pattern per pass, verified, committed, closed with proof —
  never a batch redesign.
- Composition controls (entity/brain toggles on the profile) are chips
  backed by a store table plus a flip endpoint (this stack serves mutations
  over GET, matching /track) that appends an event to the spine — the
  current mix AND its change history stay queryable, and the chip count
  updates live without a reload. SEE ALSO the interactive-controls contract
  in `operations/ceo-facing-surface-discipline` Rule 2g: a toggle that only
  recolors chips gets rejected — ship it only with a verified enforcement
  seam (router veto + dispatcher sink), all-on defaults, and fail-closed
  unknowns.

## List content: partition before sort

A recency sort over an UNpartitioned row set is a design defect the principal
reads as "not organized correctly". The board mixes two disjoint kinds:
action items (paste-ready comments, referrals — things needing hands) and
system journal notes (law changes, field verdicts — the machine talking to
itself). Sorting the union by timestamp buries a freshly delivered artifact
under process chatter, and the principal cannot find the thing that was announced.

- Default view renders the ACTION partition only; order action kinds
  deliberately (delivered/paste-ready first, then the rest), recency within.
- Journal/system notes render in a collapsed section below with their own
  count — never interleaved, never deleted.
- Filter chips, badges, and portion counters ("1–15 of 20") count the
  action partition only; a counter that includes journal rows overstates
  the work and breaks the bounded-portion math.
- Verify by parsing the rendered page after restart: the delivered
  artifact must be card #1, and no journal title may appear above the
  portion nav.

## Editable tasks (calendar edit page)

The principal edits tasks from the calendar, not from a desktop console — and the
edit must never bypass the ledger's write law.

- Route shape: task rows link to `/task/<T-ID>` (GET renders an edit page);
`POST /api/task/<T-ID>` applies changes by shelling the gate CLI
(`gates/task_ledger.py`) — never open task-ledger.db from the surface
process. Full contract in `operations/ceo-facing-surface-discipline`
Rule 2h.
- Editable post-mint: deadline (via `--redate`, mandatory `--reason`), notes
(via `--annotate`, append-only), claim/complete/release. NOT editable:
title/kind/lane/id (birth facts) — a title change is a new mint + successor.
- A naive date from the UI pins the principal's own clock offset explicitly
(e.g. `17:00:00-05:00`), never a guessed UTC instant — the gate's TIME LAW
refuses naive input by design.
- Gate refusals render on the page as "Refused: <cause>" — the gate saying
no IS the system working; never route around it from the surface.
- The edit page reads tasks + task_events READ-ONLY (events table columns
are `event`/`detail`, not kind/note).

## Pitfalls

- Renderer edits without restart = "the principal says nothing changed" — the
  module is cached at import.
- Server down after a kill = surface dead; restart and 200-verify before
  reporting anything.
- sqlite board inserts: use the real schema (`items` table with its actual
  columns), CHECK constraints reject invalid actor_class values.
- Keep internal store names out of principal-visible UI text.
- Never template an HTML line that carries inline JS with `.format()` —
  quotes and braces inside onclick handlers collide with placeholders and
  produce silently-broken markup; rewrite those lines by line index or
  pass the JS fragment as a named kwarg. The fix has a second edge: when
  you drop `.format()` to protect the JS, static `{placeholders}` left in
  the string render literally ("{n} brains") — substitute them by hand and
  grep the fetched page for literal braces as part of verification.
- A redesign that reorganizes content (partition, regroup, collapse) is
  the highest-risk change class on this surface: run the affordance
  inventory diff (old controls vs new controls) before AND after, because
  reorganization is where functionality quietly disappears without any
  code path being deleted.

## Related skills

- `gg-interface-architecture` (phenotype/design-language law, mobile
  breakpoints — user-owned)
- `task-ledger-hygiene` (mint/claim/complete gauntlet — user-owned)
