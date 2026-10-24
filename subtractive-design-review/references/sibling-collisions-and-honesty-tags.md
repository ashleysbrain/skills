# Session Detail: Sibling Collisions + Guardian Auto-Restore (2026-08-18/19)

Backing detail for Pitfalls 6-7 in the parent SKILL.md. Passes 15-18 on
writing-studio.html.

## The two collision classes, disambiguated by git archaeology

When a later pass finds a cut element back in the live page:

```
git log --oneline --all -S 'data-view="skeleton"' -- writing-studio.html
```

- Class A — auto-restore: the commit that re-adds the element is YOUR tooling
  (guardian/watchdog "repairing" the file from a known-good backup after a JS
  validation failure). Response: re-apply cuts, then run the guardian's
  `validate` + `backup` so the known-good snapshot contains the NEW state.
  Without the backup refresh you enter a restore loop (observed: pass-15 cuts
  silently reverted between commits b73495e and 76c1918).

- Class B — sibling restore: the commit is another agent's deliberate design
  decision, often with fresh wiring. Response: stand down, audit their wiring,
  fix defects additively. Observed: pass 16 cut 4 nav views as dead shells
  (verified: zero JS writers on every stat element); sibling pass 19 (dedd7dd,
  T-260818-0134) restored all 4 AND wired real lazy-render chains
  (switchView → renderSkeletonView/renderPanelView/renderRevisionView/
  renderAuthorshipView → painters, all called). Re-amputating would have been
  a flip-flop war.

## Wiring-audit probes for a restored view (mechanical, no browser needed)

1. Stat elements in the section: `re.findall(r'id="([^"]+)"', section_html)`
2. Writers: count `getElementById('<id>')` occurrences OUTSIDE the id definition;
   >1 reference means a writer exists.
3. Writer called?: for each `function _renderX`, count call sites
   `(?<!function )_renderX\(` — defined-but-never-called = still dead.
4. Call chain: entry points like `renderSkeletonView()` should appear in the
   view-switch dispatcher (`if (name === 'skeleton' && !_skeletonRendered)`).
5. Data source: fetch calls in the view block vs. local seed arrays
   (`const _panelSeats = [...]`). No fetch = demo data → needs honesty tag.

## Honesty-tag pattern (additive, sibling-respecting)

```html
<span style="font-size:10px;letter-spacing:0.08em;text-transform:uppercase;
  color:var(--clay,#b89544);border:1px solid rgba(184,149,68,0.35);
  border-radius:3px;padding:1px 6px;margin-left:10px;vertical-align:middle"
  title="Interactive preview with sample content — not your live research data">Sample data</span>
```

Appended inside the view's section-heading div. Verify with
`src.count('>Sample data</span>')`, node --check on extracted JS,
guardian validate + backup, and served==disk byte comparison.

## Concurrent-sibling hazards observed in the same window

- A sibling session re-pushed a superseded CI workflow version mid-fix
  (your-stack 83b8670) — pull fresh before editing shared files.
- patch tool warns when a sibling modified the target file — never proceed
  without re-reading the current exact content.
- Commit-message claims can be overstated (sibling claimed a 4-group sidebar
  IA rebuild; one group shipped). Record for their QA; don't rewrite their
  commits from your lane.

## Run records

- audit/QA-PASS-17-2026-08-18.md (Popper/Knuth seats, collision reconciliation)
- audit/QA-PASS-18-2026-08-19.md (Norman/Feynman/Dijkstra, honesty markers,
  10/10 session claims live-verified)
