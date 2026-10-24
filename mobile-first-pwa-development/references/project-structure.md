# Project Structure Reference

## File List with Descriptions

### Root
- **index.html** — Entry point. PWA meta tags (apple-mobile-web-app-capable, theme-color, manifest). **DEPRECATED for serving** — use bundle.html instead (raw ES modules silently fail in browsers).
- **public/bundle.html** — Production entry point. Loads bundle.css + bundle.js (IIFE format from esbuild). This is what you serve.
- **public/bundle.js** — esbuild output (IIFE, ~68KB). All JS bundled into single file.
- **public/bundle.css** — esbuild output (~21KB). All CSS extracted into single file.
- **public/manifest.json** — PWA manifest: name, icons, display: standalone, theme_color, background_color.
- **public/sw.js** — Service worker: caches all assets on install, serves from cache, updates on activate.

### Build command (REQUIRED before serving)
```bash
npx -y esbuild src/main.js --bundle --outfile=public/bundle.js --format=iife --target=safari15
```

### src/
- **main.js** — Bootstrap. Creates app, mounts to #app, registers SW, handles beforeinstallprompt.
- **app.js** — Core orchestrator. Instantiates State, Router, all Services, all Views. Handles routing, view mounting, persistent UI (BottomNav, Modal).
- **state.js** — Reactive state management. Map-based storage with dot-notation get/set. localStorage persistence. Pub/sub via subscribe().
- **router.js** — Hash-based routing. window.onhashchange listener. Supports query params. onRouteChange callbacks.

### src/services/
- **audio-engine.js** — Web Audio API wrapper. Procedural sound generators for 6 sound types. Master volume, per-track volume, spatial panning (8D), sleep timer. Lazy context creation (requires user gesture).
- **sleep-tracker.js** — Session lifecycle: startSession(), endSession(quality, notes). Computes insights: weeklyAvg, sleepDebt, consistency, bestDay.
- **scoring-engine.js** — 8-dimension wellness scoring. Physical, Emotional, Intellectual, Social, Spiritual, Vocational, Financial, Environmental. Sleep impact calculator. Dimension metadata (icon, color, factors).
- **researchkit.js** — ResearchKit web equivalent. enroll(), setConsent(), getSurvey(morning/evening/weekly), submitSurveyResponse(), exportData().

### src/components/
- **DashboardView.js** — Score ring, quick actions, dimension bars, insights cards, recent sessions.
- **SoundMixView.js** — Master volume slider, spatial toggle, 6 track cards with play/pause + volume sliders, timer buttons (15m-2h), stop all / start sleep.
- **SleepView.js** — Pre-sleep checklist, active sleep with breathing circle + elapsed timer, wake-up quality rating (1-5 stars), notes, save session.
- **InsightsView.js** — Large overall score ring, detailed dimension cards with bars and levels, sleep summary cards.
- **ResearchView.js** — Enrollment flow (age/region), informed consent doc, survey forms (morning/evening/weekly with scale/choice questions).
- **SettingsView.js** — Sleep goal, bedtime, wake time, notification/haptic toggles, default timer, data export, clear all data.
- **OnboardingView.js** — 3-step: name, sleep goal (6-10h buttons) + bed/wake time, finish.
- **BottomNav.js** — 5-item fixed bottom nav (Home, Sounds, Sleep, Insights, Settings). Active state highlighting.
- **Modal.js** — Overlay modal with title, body, action buttons.

### src/styles/
- **main.css** — Complete dark theme. CSS custom properties for colors, spacing, radii, shadows. Mobile-first. Safe-area insets. Breathing animation. All components styled.

## Total: 22 files, ~2900 lines