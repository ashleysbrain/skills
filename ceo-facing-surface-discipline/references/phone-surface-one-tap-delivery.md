# Phone Surface: One-Tap Delivery Recipe

Concrete implementation of SKILL.md Rules 2f-2h for principal phone surfaces served
over Tailscale. Pattern proven on the the OS boards server (:port).

## Calendar task editing (gate-mediated, ledger-preserving)

principal-facing task edit surface pattern when the board renders ledger tasks:

- `GET /task/<T-ID>` — edit page: title read-only (birth fact), deadline
  date input, reason input (required for date moves), note textarea, verbs
  Save/Claim/Mark done/Release, plus recent `task_events` rendered
  append-only.
- `POST /api/task/<T-ID>` — validates `T-\d{6}-\d{4}` shape, then shells the
gate CLI: redate pins the principal's local offset explicitly
  (`<date>T17:00:00-05:00` pattern parameterized to the principal's tz), annotate
  is append-only, claim passes `--actor-kind human --by "the principal (principal)"`.
- Reads open the ledger `mode=ro` only; writes NEVER open the ledger —
  subprocess to `gates/task_ledger.py` is the single write path.
- Every gate refusal renders inline as `Refused: <cause>` — surface never
  bypasses a gate, including mandatory reasons and terminal-row guards.

## Persistent bottom tab bar (never scrolls away)

```css
.tabbar { position: fixed; bottom: 0; left: 0; right: 0; z-index: 60;
  display: flex; background: #0d0a05; border-top: 1px solid #2a2214;
  padding-bottom: env(safe-area-inset-bottom); }
.tabbar a.tab { flex: 1; min-height: 56px; display: flex;
  flex-direction: column; align-items: center; justify-content: center;
  text-decoration: none; }
.tabbar a.tab.on { color: #f5c518; border-top: 2px solid #f5c518; }
```

Rules: exactly one tabbar per page, on EVERY screen; active tab gold; five
tabs maximum; hero buttons 64px min, ordinary buttons 52px min.

## One-tap copy button (with fallback)

```html
<button type="button" class="btn wide gold copybtn" data-copytarget="cmt41">Tap to copy comment</button>
<pre id="cmt41" class="copypre">FULL PASTE TEXT INCLUDING SOURCE LINK</pre>
```

```css
.copypre { display: none; }
```

Handler: delegated click listener on `.copybtn` (one listener per page, not
one per button); read the target `<pre>` `textContent`; try
`navigator.clipboard.writeText(t)`, fall back to a transient `textarea` +
`document.execCommand('copy')` (in-app browsers often gate the async
clipboard API); flip the button label to "Copied" for ~1.5s. The payload
carries the source/paper link appended so one paste delivers comment AND
reference.

## Deep-link pin route

`/comments?focus=<seq>`: render the list normally, then lift the matching
card to position 1, tag it `class="ccard pin"` (2px gold border + soft
glow) under a "Pinned for you" banner. The home screen's action hero button
links to the current top deliverable's focus URL — repoint when it
completes. Route handler must disambiguate filter vs focus params
(`?f=ready` vs `?focus=41`) before dispatching.

## Verification (from the phone path, not localhost)

1. `curl http://<tailscale-ip>:<port>/comments?focus=<seq>` — pinned card
   position precedes every other card; payload text within the first ~6K
   chars of the response.
2. Count buttons by `aria-label` or `href`, NOT by exact class strings —
   variant classes (`btn gold hero` vs `btn hero`) silently evade a
   `class="btn hero` grep and undercount conditional variants.
3. Both `clipboard.writeText` AND `execCommand` present in the served JS.
4. Tab count identical on every screen; `position: fixed` exactly once per
   page (the shared tab bar).
5. All routes 200 from the Tailscale IP after `launchctl kickstart -k`.

## JS-in-HTML generation (the .format brace trap)

When a Python renderer builds HTML that embeds JavaScript, never run
`.format()` over markup that contains JS object literals — `{}` braces in the
script crash `str.format` with KeyError or leak literal `{n}` into the page.
Split the template: `.format()` only the static fragment that needs values,
plain-concatenate the `<script>` block. If literal `{...}` tokens appear in
served HTML, this is the cause, not bad data.

## Internal-service exposure for principal phone use

A gateway bound to `127.0.0.1` is unreachable from the principal's phone even when
the host is on the tailnet — check the bind, not just the port. Patch the
launch/watchdog line to `--host 0.0.0.0`, restart via its supervisor, then
verify from the Tailscale IP (curl the phone-path URL, expect 200). Any
engineer-facing HTML it serves (raw JSON views, debug dashboards) stays
hidden: give the principal only the polished surface path, never the gateway root
or debug routes — an internal tool surface shown to a human gets rejected
outright.
