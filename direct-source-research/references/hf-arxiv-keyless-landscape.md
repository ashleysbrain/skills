# Keyless ML-landscape APIs: HuggingFace + arXiv (verified 2026-08-16)

When the managed web tools are billing-blocked and the question is "what open models exist right now in X," two keyless APIs give a live, citable landscape in minutes. Used to map the world-model/VLA landscape for the the OS OS gap analysis.

## 1. HuggingFace models API — the open-model census

```bash
curl -s "https://huggingface.co/api/models?search=<query>&sort=downloads&direction=-1&limit=8"
```

- `sort=downloads` = adoption evidence. `sort=lastModified` = freshness radar.
- Fields that matter: `id`, `downloads` (monthly), `likes`, `lastModified`.
- **Signal floor: downloads >= 500.** Below that it is a personal fine-tune, not an ecosystem entrant. The "world model" search term returns mostly noise (GGUF re-uploads, unrelated "Genie" projects); KNOWN-PLAYER searches (openvla, pi0, smolvla, GR00T, Cosmos) return the real census. Search by team/project name, not by concept.
- Namespaces are authoritative: `lerobot/*`, `nvidia/*`, `openvla/*` are first-party; everything else is community.
- No API key needed for read. Set a User-Agent header.

## 2. arXiv API — the research pulse

```bash
curl -s "http://export.arxiv.org/api/query?search_query=all:%22world%20model%22%20AND%20cat:cs.RO&sortBy=submittedDate&sortOrder=descending&max_results=8"
```

- Returns ATOM **XML, not JSON** — parse with regex on `<title>` / `<published>`, or feed through an XML parser. A json.loads() attempt fails with "Expecting value."
- `cat:cs.RO` constrains to robotics; drop it for cross-listed work.
- `sortBy=submittedDate` gives the week's pulse: on 2026-08-13 alone there were 8 new world-model-for-robotics papers.
- Rate limit: ~1 request / 3 seconds, be polite.

## 3. The landscape-snapshot pattern (what to save)

Pull the census ONCE per strategic pivot and persist the dated snapshot to O'Keefe/memory — model landscapes go stale in weeks, and a dated snapshot is what makes later gap analyses auditable ("as of 2026-08-16, Cosmos-Predict2 had 233K downloads"). Reference file for the 2026-08-16 world-model snapshot: see the the OS OS gap analysis in the workspace.

## 4. The standing-radar pattern (cron)

"Find new models as they release nearly daily" = a diff cron, not manual scanning:

- Script pulls HF (`sort=lastModified`, download floor) + arXiv (submission date floor, category) each tick.
- State file (JSON) holds `seen` IDs/titles (capped ~500). Diff = new entrants.
- **Silent unless a hit lands in a DEFINED white-space keyword set** (e.g., the missing OS layers: scheduler/arbitration, IPC/latent-bus, fault-isolation, health-telemetry, safety-envelope). Generic new-model noise stays silent.
- Alert goes through an agent-judged digest (3 lines max: what landed, which layer, does it change the gap map).
- Proven first run: caught ContactGuard in the safety-envelope layer correctly, zero false positives.

Live instance: `<agent-home>/scripts/world_model_radar.py`, the operator agent cron `world-model-radar`, every 2 days.

## Pitfalls

- Concept-term searches on HF ("world model", "VLA") return polluted results — fan-tunes and unrelated projects rank high on partial-string matches. Anchor on known players and team namespaces; let the radar catch new names by velocity rather than by search.
- HF `downloads` is a rolling window (30-day), so a brand-new hot model can show LOW downloads with a very recent `lastModified` — that is exactly the radar's `lastModified >= today-2 AND dl >= 1000` velocity heuristic.
- arXiv abstracts are marketing-grade for preprints; treat titles+dates as the census and only pull abstracts for the 2-3 papers that matter.
