# Web-First Cross-Platform Strategy

Pattern for taking a scoring/physics engine from web prototype to all
platforms (iOS, Android, desktop) without rewriting the engine. Proven in
the 8D Sleep product build (June 2026).

## Why Web-First

The scoring engine is pure JavaScript. It runs identically in a browser tab,
in an iOS WKWebView, in an Android WebView, and in an Electron shell. The
physics doesn't care where it runs. Build once, ship everywhere.

| Factor | Web-First | Native-First |
|---|---|---|
| Time to first user | Deploy today, share a link | 2-4 weeks (build + App Store review) |
| Platform reach | Every phone, tablet, laptop | iOS only (or Android only) |
| Updates | Instant (push to server) | 1-7 day review |
| Scoring engine | Identical JS code | Identical (port or WebView) |
| Server cost | Near zero (static hosting) | Per-user backend |

## The Three-Phase Path

### Phase A: Web App (NOW)
- Zero-dependency vanilla JS (or Vite + React)
- `python3 -m http.server` for local testing
- Deploy to Vercel/Netlify free tier for public URL
- CSV upload for data import (Apple Health export, Sleep Cycle, etc.)
- Scoring runs entirely client-side

### Phase B: Native Wrapper (WEEKS)
- Wrap the same web app in [Capacitor](https://capacitorjs.com/)
- Add native HealthKit / Health Connect plugin bridge (~50 lines glue)
- Submit to App Store + Google Play
- Same scoring engine, same JS, same UI — just native shell

### Phase C: PWA (MONTHS)
- Add manifest.json + service worker for offline/installable
- Push notifications via web APIs
- Installable on any device without app store
- Works offline (cached scoring engine + localStorage data)

## Connecting to Existing Apps (Integration Strategy)

Position as a complementary intelligence layer, not a competitor:

### Tier 1: CSV/File Import (works immediately)
- Apple Health export → CSV upload → local scoring
- Any sleep app that exports data → upload → 8D layer on top
- Zero API needed, works in browser today

### Tier 2: Direct API Integration (weeks)
- Apple HealthKit (Capacitor native bridge)
- Google Fit / Health Connect (native bridge)
- Fitbit API (OAuth), Garmin Health API (OAuth)

### Tier 3: Unified Health Platform (months)
- Terra API — one OAuth covers 20+ wearables (Oura, Whoop, Polar, etc.)
- Validic — enterprise health data platform

## Apple Health Data Mapping

| Apple HealthKit Field | Engine Input |
|---|---|
| SleepAnalysis (asleep) | `totalSleepTime` |
| SleepAnalysis (inBed) | `timeInBed` |
| Sleep stages (deep/REM/core/awake) | `sleepStages` |
| Time in bed - time asleep | WASO |
| Heart rate during sleep | Optional: stress inference |

Web path: user exports Health data as XML/CSV from the Health app, uploads
to web app. Native path: Capacitor HealthKit plugin pulls sessions directly.

## Revenue Model (Cross-Platform)

Use RevenueCat for unified subscription management across web + iOS + Android.
- Free: full scoring, manual logging, 7-day history
- Pro ($4.99/mo): unlimited history, all integrations, CSV export
- Pro+ ($9.99/mo): coaching insights, trend analytics, sound library

## Fastest Launch Checklist

1. Deploy web app to Vercel/Netlify (1 hour)
2. Add PWA manifest (1 hour)
3. Write short privacy policy (data stays local) (2 hours)
4. Share the link

**Time to first real user: 1 day.**
