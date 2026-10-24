# 8D360 Competitive Landscape Research — Session Reference

Date: 2026-06-06
Context: the principal requested competitive landscape research across the 8 dimensions of wellness (8D360) plus a holistic cross-dimensional category, for the Qubit GR / Divinity Health product.

## Scope
9 research categories, each delegated to a specialist agent:
1. Physical — Sleep (2 agents: sleep trackers + sleep science)
2. Physical — Nutrition (calorie trackers, meal loggers)
3. Physical — Fitness (workout apps, training platforms)
4. Physical — Wearables (fitness bands, smart rings, health monitors)
5. Psychological (therapy platforms, mental health apps)
6. Environmental (ambient wellness, air/light quality — merged into adjacent)
7. Social (community, connection, relationship wellness)
8. Intellectual (learning, cognitive training, brain health)
9. Financial (budgeting, financial wellness, money mindfulness)
10. Spiritual (meditation, mindfulness, purpose-finding)
11. Holistic (cross-dimensional platforms, integrated wellness)

## Agent execution
- 14 markdown files produced (01a through 09)
- Sequential execution, one agent at a time
- Skeleton-first write enforced
- Each agent covered 2–3 products in depth
- Total output: ~328 KB, 4,744 lines

## Products researched (partial list)
Sleep: Sleep Cycle, Rise Science, Calm (blocked by bot detection)
Nutrition: MyFitnessPal, Cronometer, Noom
Fitness: Strava, Peloton
Wearables: Apple Health, Oura Ring, Fitbit, WHOOP, Garmin
Psychological: BetterHelp, Talkspace, Headspace
Intellectual: Duolingo, Coursera
Financial: YNAB, Monarch Money
Holistic: Welltory, Happify, OpenEvidence, K Health, Ada Health, Glass Health, Hippocratic AI

## Screenshot collection
- 26 screenshots total, captured via browser_navigate + browser_vision pattern
- Stored in `assets/` directory under the research folder
- Sites that blocked automated access: Calm.com (bot detection)
- MyFitnessPal screenshot captured a cookie banner (93KB) — not the homepage
- Browser screenshots cached at `<agent-home>/browser_screenshots/` and copied to assets

## Inline screenshot embedding
Initially screenshots were in a "Visual Survey" appendix at the end. User corrected twice:
1. First pass: moved 4 apps inline, kept appendix for the rest
2. Final pass: moved ALL 26 inline, deleted appendix entirely

Python script (`embed_screenshots_inline.py`) handled the bulk repositioning by finding each product's heading and inserting the image reference directly below.

## PDF rendering pipeline
```bash
# Master markdown → HTML → PDF
pandoc master.md -f markdown -t html5 -o master.html
python3 -c "
from weasyprint import HTML
HTML('master.html').write_pdf('report.pdf')
"
```

Custom CSS for margins and images:
```css
@page { margin: 2.5cm; }
img { max-width: 100%; height: auto; }
```

Final PDF: 210 pages, 1.2 MB.

## Key files
- Master report: `8D360-Competitive-Landscape-Report-2026-06-06.md` (4,987 lines)
- Assets: `assets/` directory — 38 image files (26 PNG, 5 JPG, plus extras)
- Individual dimension files: `01a-sleep-trackers.md` through `09-holistic.md`

## Lessons
1. Split Physical into sub-dimensions (sleep, nutrition, fitness, wearables) — too broad for one agent.
2. Calm.com blocks bots — note this for future screenshot passes.
3. LLM-5V-Turbo vision API returns 429 rate-limit errors under load — screenshots still capture but vision analysis fails.
4. User wants inline screenshots, never appendix. This is a repeated, non-negotiable preference.
5. Margins at 2.5cm are the minimum comfortable width for mobile PDF review.
6. 210-page PDF is deliverable via Telegram MEDIA path (1.2 MB fits within limits).
