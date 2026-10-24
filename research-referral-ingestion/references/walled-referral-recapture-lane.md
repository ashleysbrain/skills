# Walled-referral re-capture lane

Depth for referrals that arrive auth-walled. Use when a LinkedIn referral
capture returns a signup/consent wall or title-only tags.

## Capture ladder (cheapest first, one attempt per rung)

1. `curl -sIL <short> | grep -i '^location'` — resolve the canonical URL.
2. `curl -sL -A 'facebookexternalhit/1.1' <full-url>` — crawler UA often
   renders full og:title/og:description for ugc posts.
3. Reader proxy (`r.jina.ai/<url>`) — recovers reshare layers and bodies
   the og tags truncate.
4. Web search on distinctive title fragments + author name — some posts
   are indexed elsewhere (Pulse long-forms often are; ugc posts usually
   are not). A zero-hit result is evidence, not failure.
5. STOP. Anything beyond this (UA cycling, proxy rotation, cookie jars
   from other profiles, keychain decryption attempts) burns an afternoon
   per post — measured outcome: the wall stands for all headless routes.

## Filing rules

- Mint a re-capture row with capture state in the title (WALLED, Nth this
  week) and every thing the slug/og tags DID yield — a title-only row with
  the author handle and ugcPost ID is recoverable later; an empty row is
  not.
- Track the wall rate (walled / total principal LinkedIn referrals that week) —
  it is the measured number that justifies an authenticated-capture lane,
  and repeat-walled authors are follow-lane candidates, not five sieges.
- Corpus row with note = capture state + recovery path.

## The two recovery routes that exist

1. principal paste — immediate, always available; ask once with the specific
   post list, not per-referral.
2. An authenticated-browser agent seat (external agent with a persistent,
   credentialed, human-supervisable VM browser). This is the structural
   fix; local automation Chrome with the real profile still gets served
   the signup wall, and OS keychain decryption is GUI-locked headless.

## Signals

- `og:description == og:title` → title-only capture; further fetches of
  the same URL return identical tags.
- Pulse long-form (`/pulse/` slug) → consent interstitial, not a UA gate.
- `lnkd.in/e...` shortener → 200 with no Location header; resolve from
  page body or web search.
