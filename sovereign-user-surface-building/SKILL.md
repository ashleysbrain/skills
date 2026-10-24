---
name: sovereign-user-surface-building
description: Build user personal-data surfaces outside org organisms.
version: 1.0.0
---

# Sovereign User Surface Building

## What This Is

The procedure for building user-facing personal-data surfaces (butterfly-style launchers, personal worlds, user dashboards, personal health/analytics/conversations views) where the user's data world is served from the SOVEREIGN-USER organism, separate from org organisms. The organisms are separate; they connect only at the entry point (a button/link). The org NEVER gets a data path to personal data.

Load `ds-genome-transcription` + BRAND-DNA.md and route the task through Sherman (then triangle: research → adversarial → QA) BEFORE any user-facing design work.

## Always-On Rules (binding)

1. **Census before build.** Enumerate the real organs FIRST and wire every view to one: flow registry (FLW-*), the deterministic 8D rescore engine (canonical weights), coaching/studio/research stores, session store. A view with no real organ behind it is fabrication, not a placeholder, and is P0 when discovered.
2. **Data honesty.** Show canonical dimensions, weights, and freshness dates. State when a pipeline is stale. Never render invented or proxy scores in place of the user's real scoring system.
3. **Structure-enforced scope.** The boundary is a separate server + store inside the sovereign organism's directory, not access control layered on an org route. Verify with a NEGATIVE TEST (org-scope path on the sovereign server must 404) before reporting done. For personal MEDICAL data the wall is stricter — see the four-probe checklist below; the org lineage gets no path by default, and the only thing that ever opens one is an explicit typed connection row the user instructed.
4. **Drawer-native UX.** User worlds pop out as dynamic drawers (slide-in, crumbs, chips, drill stack) per the host surface's drawer contract; never a full-screen redirect takeover. Keep the launcher logo animated while closed. Every empty view states WHY it is empty and names the endpoint it wanted.
5. **Seat every server.** launchd plist with RunAtLoad + KeepAlive at birth. Raw nohup spawns die on reboot; fire-and-forget periodic spawns stack into process floods under load. Seat-minting order (violating it makes healthy seats look broken): (a) extract the MEASURED run command from the live process (`ps -o command= -p PID` + `lsof -nP -iTCP:PORT` for port→PID→cwd/interpreter) — never from a registry or doc, which accumulate stale paths; (b) grep existing plists for the engine first — a duplicate seat crash-loops both fighting for the port, so keep the incumbent; (c) kill the raw holder and CONFIRM the PID is gone BEFORE `launchctl bootstrap` — a KeepAlive spawn onto an occupied port exits with a clean-looking log ("shutdown complete", no bind error) and retries into launchd throttle backoff; (d) SIGTERM is often trapped by uvicorn holders — verify death, escalate only if still alive; (e) an already-throttled seat needs `launchctl kickstart -k gui/$(id -u)/<label>` to break the backoff; (f) verify with plain sequential curls on separate lines — `set -- $var` inside a `for spec in` loop clobbers the loop variable and the sweep reports every engine down while each is fine, and engines without a `/health` route answer 000 on `/health` while root serves.
6. **Port identity verification.** A listening port is not proof of service identity: resolve the PID to its command line before claiming a service lives there. Verify port free with `lsof` AND grep the ECS registry before minting.
7. **QA in a real browser.** Puppeteer `evaluate` on the live DOM; naive static-HTML grep assertions fail on dynamically-built DOM and pass on broken builds. Close the ledger task only with proof evidence adjacent to every verdict word (exit codes, output excerpts, file anchors within ±300 chars).

## Medical-data wall (four probes, all by execution)

When the data class is personal health, the wall must be measured, not
asserted: (1) bind 127.0.0.1 and curl the machine's external IP on the
port — REFUSED proves the bind; (2) grep the engine source for
`requests|urllib|http.client|curl` — zero outbound calls, ever (naming
org ports in a docstring is fine; calling them is the breach); (3) own
stores 0600 inside the sovereign zone + a typed connection ACL file that
ships with `"connections": []` (default DENY; a row = permit quote +
exact scope + revocable by row removal, surfaced live on a
localhost-only summary endpoint); (4) recursive grep for the port across
org workspaces and registries — zero references, so nothing can wire to
the surface by accident later. Gate serving behind an in-process birth
score (compile → init own stores → score → refuse-to-serve below threshold) so the organism
cannot run degraded — score AFTER bootstrap or store-existence checks read 0 and a healthy organism wedges at its own gate. Reuse the sovereign substrate (HMAC health webhook,
connection hub, records tunnel) — never rebuild collectors.

## Build Order

1. Census organs (per rule 1). Check `PRAGMA table_info` before writing SQL against unfamiliar stores — column names differ from assumptions.
2. Run `sherman_router.py --gate --situation ... --operator hermes`; carry its routed engine + methodology into the minted GENOME block verbatim (unquoted `scientist=the specialist engine`; quoted values fail the format gate).
3. Mint the ledger task with a mandatory flow tag (`flow='FLW-...'` or deliberate `FLW-UNTYPED`). Describe servers by role in prose — port literals trigger the collision scan.
4. Build the boundary server inside the sovereign organism's directory: stdlib `ThreadingHTTPServer`, read-only sqlite (`file:...?mode=ro`), localhost bind, `/health` returning organism identity, per-domain endpoints, 404 JSON naming the organism for everything else.
5. Seat it (rule 5), bootstrap, verify `/health` 200.
6. Negative-test the boundary (rule 3); record the 404 output as the receipt.
7. Build the frontend per rule 4.
8. Browser QA (rule 7), then close the ledger with inline proof.

## Pitfalls

- Do not wire a user Health view to a near-empty org endpoint and render partial data as the full system — the census step exists to make this impossible.
- Do not embed personal-data endpoints in the org daemon because it is the surface already in hand — move the data path into the sovereign organism instead.
- Do not describe tasks with port literals unless the port is verified free and yours — the mint gate scans live binds.
- Do not run engines as raw spawns that later matter — unseated means silently dead after reboot.
- Do not build a monitor organ that detects without acting — a watchdog with no revival path (kickstart when a seat exists, bus alert when not, never a raw spawn) is the recurring root failure class: outages stay down while monitors watch them. Wire detection→action in the same organ, or route the action lane explicitly in the task detail.
- Do not claim an engine is "self-healing" from its name or docs — grep its source for restart actions (kickstart/launchctl/restart/Popen). Monitors wearing repair-organ names are the most dangerous class because the census reads them as coverage.
- Do not ship generic AI copy ("your world", symmetric card grids, gradient buttons) — it fails the genome gate and reads as AI-generated to the principal.

- Do not describe tasks with port literals unless the port is verified free and yours — the mint gate scans live binds, and it counts BOTH your own engine's live bind (pause the engine before mint; restart after the seed row lands) AND any substrate port you merely cite as a dependency (name reused services by role — "health webhook", "hub registry" — never `:NNNN`).
- To mint with an explicit T-* id, reserve it first with `tid = tl.mint(c)` and pass the return value as `task_id=` — submitting an unminted explicit id is refused. `flow=` must be a registered code (read stores/flow-registry.json; plausible codes like FLW-BUILD do not exist).
- launchd bootstrap is blocked from inside a supervised gateway shell — the birth procedure still completes: write the plist, hold the engine as a background process, and hand the user the one outside-shell `launchctl bootstrap gui/$(id -u) <plist>` command as a disclosed follow-up rather than reporting the seat as seated.

## Ledger gate quick reference

- `submit(c, title, kind, lane, origin, created_by, flow=..., detail=...)`
- `claim(c, actor, actor_kind, task_id=...)` — actor first, `'ai'|'human'` second.
- `complete(c, task_id, outcome_text, actor)` — proof gate wants evidence adjacent to every verdict word.
- Title is a label — hard refuse above 200 chars; the document lives in `detail=`.
- GENOME block vocabulary is CLOSED: `body=` must be a canonical body system (nervous, circulatory, immune, sensory, …), `8d=` a canonical dimension (human: physical/psychological/… or AI: accuracy/coherence/…), `scientist=DS <LastName>` unquoted — free-form values fail with a vocab error naming the canonical set, so read the sets from the gate module before composing the block.
- `force=True` does NOT bypass the premint port scan; the only lawful fix is a genuinely clean scan (engine paused, substrate deps named by role).

## B2C organism scoping (standing principal law)

- The user's B2C organism is 8-dimension-complete by design; medical/physical health is the FIRST ORGAN, not the organism's identity. Name organs by dimension; never scope, title, or describe the organism itself as medical-only.
- A personal health interface is an ORGAN of the sovereign organism, built through the full methodology (census → deep research → panels → build inside the sovereign zone) — never a bolt-on attachment to an org-facing surface. A design that reads as an attachment means the census step was skipped.
- A birth through the L3 canal completes with a live engine held as a background process and the launchd seat as a disclosed outside-shell follow-up (see pitfalls); the organism is BORN at APGAR-pass + seed row, not at first organ maturity — grow organs as separate minted tasks through the same canal.

## Related Skills

- `agent-organism-interface-building` — org-side interface rules (read; user-owned, not editable here)
- `mosaic-os-architecture` — organism layering and terminology (read; user-owned)
- `ds-genome-transcription` — brand DNA loading before any creative output
