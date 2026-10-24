# Discovery Workflow — Operational Guide

**Created:** 2026-07-06 (after first successful manual discovery run)

This is the step-by-step for the Corpus Weekly Discovery agent. The cron job
fires every Sunday 2 AM CT. A fixer agent may re-run it when the watchdog
escalates `RERUN_DISCOVERY`.

## Pre-flight checks

```bash
cd /<workspace>

# 1. Check pending count — SKIP if 30+ pending (let absorber catch up)
python3 canon_queue.py stats

# 2. Get ALL existing URLs for dedup (must use canon.db, NOT canon_queue.db)
python3 -c "
import sqlite3
conn = sqlite3.connect('canon.db')
for r in conn.execute('SELECT url FROM absorption_queue').fetchall():
    print(r[0])
"
```

## Catalog URLs by institution

### MIT OCW — browse by department

MIT OCW supports department-filtered search. The URL pattern is:
```
https://ocw.mit.edu/search/?d=<Department%20Name>
```

Key departments and their URLs:

| Department | URL |
|---|---|
| Architecture | `https://ocw.mit.edu/search/?d=Architecture` |
| Music and Theater Arts | `https://ocw.mit.edu/search/?d=Music%20and%20Theater%20Arts` |
| Media Arts and Sciences | `https://ocw.mit.edu/search/?d=Media%20Arts%20and%20Sciences` |
| Comparative Media Studies | `https://ocw.mit.edu/search/?d=Comparative%20Media%20Studies%2FWriting` |
| Brain and Cognitive Sciences | `https://ocw.mit.edu/search/?d=Brain%20and%20Cognitive%20Sciences` |
| Sloan School of Management | `https://ocw.mit.edu/search/?d=Sloan%20School%20of%20Management` |
| Engineering Systems Division | `https://ocw.mit.edu/search/?d=Engineering%20Systems%20Division` |
| Health Sciences and Technology | `https://ocw.mit.edu/search/?d=Health%20Sciences%20and%20Technology` |
| Linguistics and Philosophy | `https://ocw.mit.edu/search/?d=Linguistics%20and%20Philosophy` |
| Science, Technology, and Society | `https://ocw.mit.edu/search/?d=Science%2C%20Technology%2C%20and%20Society` |

### Yale Open Yale Courses

```
https://oyc.yale.edu/courses
```

Renders a clean HTML `<table>` with columns: department, course number, title,
professor, date. Scrapes perfectly in one JS query (see below).

### Stanford — use SEE, NOT online.stanford.edu

```
# ✅ CORRECT — Stanford Engineering Everywhere
https://see.stanford.edu/Course

# ❌ WRONG — returns 403 Forbidden
https://online.stanford.edu/free-courses
```

SEE has a limited catalog (~9 courses). Course links follow the pattern:
`https://see.stanford.edu/Course/<CODE>` (e.g. CS106A, EE261).

## Browser extraction — critical technique

### The snapshot problem

MIT OCW search result pages render courses in a React-based table that **does
NOT appear in the accessibility-tree snapshot**. The `browser_snapshot` output
shows only:
- Department filter checkboxes (Electrical Engineering, Mathematics, etc.)
- A result count ("192 results")
- Sort dropdown

The actual course cards are invisible to the snapshot. You MUST use
`browser_console` with JS to extract them.

### MIT OCW extraction JS

After navigating to a department search page, run this in `browser_console`:

```javascript
// Dedup-safe extraction — gets all course links + surrounding card text
(() => {
  const courses = {};
  document.querySelectorAll('a[href*="/courses/"]').forEach(a => {
    const href = a.href;
    if (href.includes('/search/') || courses[href]) return;
    let card = a;
    for (let i = 0; i < 5; i++) {
      card = card.parentElement;
      if (!card) break;
      const text = card.textContent;
      if (text && text.length > 20 && text.length < 400) {
        courses[href] = text.trim().replace(/\s+/g, ' ');
        return;
      }
    }
    courses[href] = a.textContent?.trim()?.substring(0, 200) || '';
  });
  return JSON.stringify(Object.entries(courses).map(([link, text]) => ({link, text})));
})()
```

**Important:** Use an IIFE `(() => { ... })()` wrapper, NOT a bare `const`
declaration. Bare `const` at the top level persists in the console scope and
causes `SyntaxError: Identifier 'X' has already been declared` on re-runs.

To get more results, scroll down before re-running:
```javascript
window.scrollTo(0, document.body.scrollHeight);
```

### Yale OYC extraction JS

Yale's table is much simpler:

```javascript
(() => {
  const rows = document.querySelectorAll('table tr');
  const courses = [];
  rows.forEach(row => {
    const cells = row.querySelectorAll('td');
    if (cells.length >= 5) {
      const link = cells[2]?.querySelector('a')?.href;
      courses.push({
        dept: cells[0]?.textContent?.trim(),
        code: cells[1]?.textContent?.trim(),
        title: cells[2]?.textContent?.trim(),
        link: link
      });
    }
  });
  return JSON.stringify(courses);
})()
```

### Stanford SEE extraction JS

```javascript
(() => {
  return JSON.stringify(
    [...new Set(
      Array.from(document.querySelectorAll('a'))
        .filter(a => a.href?.includes('see.stanford.edu/Course/'))
        .map(a => ({ title: a.textContent.trim(), link: a.href }))
    )].map(s => s)
  );
})()
```

## Domain mapping reference

| Department/Topic | Domain |
|---|---|
| Architecture, Art, Design, Music, Theater, Media Arts | `arts-design` |
| Brain and Cognitive Sciences, Neuroscience | `neuroscience-cognition` |
| Psychology, Behavioral Economics | `behavioral-science` |
| Health Sciences, Biology, Biomedical | `health-science` |
| Computer Science, AI, ML | `data-science-ml` |
| Engineering, Systems, Fourier/Signal | `systems-architecture` |
| Management, Strategy, Leadership | `product-methodology` |
| Philosophy, Ethics, Political Philosophy | `brand-philosophy` |
| Perception, Vision Science, Graphics | `human-perception` |

## Domain diversity strategy

Before selecting courses, check the stats output. Target domains with 0-2
existing entries for maximum diversity. A good run touches at least 3-4
different domains, ideally 5+.

Typical domain gaps to fill (check current stats):
- `systems-architecture` — often 0 (MIT ESD, Stanford EE courses)
- `product-methodology` — often 0 (MIT Sloan courses)
- `human-perception` — usually underrepresented
- `brand-philosophy` — Yale Philosophy/Political Science courses

## Adding courses

```bash
cd /<workspace>

python3 canon_queue.py add \
  --url "https://ocw.mit.edu/courses/21m-011-introduction-to-western-music-spring-2006/" \
  --title "Introduction to Western Music" \
  --institution mit \
  --domain arts-design \
  --course-code "21M.011" \
  --priority 3

# Priority guide:
#   3 = core creative/health topics (music composition, visual arts, health)
#   5 = default for everything else
```

## Post-run report checklist

- Count new courses by institution (MIT / Yale / Stanford)
- Count new courses by domain
- List domain gaps filled
- Run `python3 canon_queue.py stats` for final state
- Verify pending count is under 30 (if 30+, note that absorber needs to catch up)
