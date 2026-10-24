# principal directive capture: at-receipt law, batch dedup, provenance (2026-08-28)

Session evidence for the task-ledger-hygiene patch. Pattern class: capturing
human directives from multiple concurrent surfaces without loss or duplication.

## The two-sided failure (one morning, one thread)

1. **Under-mint:** 14 audio directives landed in the desktop sister thread
   (10:19-20:51 Thursday). The directive sweep ran Tuesdays 09:00 only. Result:
   nothing minted for ~24h. principal: "you missed quite a few details from my work
   yesterday... what is happening?"
2. **Over-mint (triggered by a false absence claim):** morning audit queried
   `origin LIKE 'ceo%' AND date >= ...` — a filter that missed sister-thread +
   bridge-responder mints (different origin strings, overnight timestamps).
   Claimed "never minted." Minted 14 more. Actual state: 22 duplicate rows
   (anti-gravity x6, conductor-naming x6, ...).

## Laws minted from it

- **At-receipt law:** directives mint in the thread they land in, at receipt.
  Sweep = backstop audit. (Also pinned to the OS memory-pins.)
- **Absence claims need the widest net:** before saying "not minted," census by
  content-prefix across ALL origins/stores, no filters. Absence is a stronger
  claim than presence.
- **Batch dedup:** canonical = richest-context row (GENOME + full audio
  context); duplicates close cancelled with `dup-of <canonical>` + dedup event.
  Never delete rows.

## Surface-echo effect (operational reality)

The principal's messages echo across 6-10 parallel sessions (desktop threads + relay
sessions see the same content). Any "messages from principal" query returns N copies;
dedupe by content prefix. This is also why sibling mints happen — relay
sessions legitimately mint the same directive. The ledger, not any single
thread, is the dedup point.

## Provenance law (same session, principal directive)

Every user-facing item carries the full chain: (1) AI interpretation,
(2) RAW SOURCE — original transcription, playable audio where retained,
original text/image, (3) links to every connected component (tasks, events,
builds, bus messages, sessions). Source pointers (session_id + message_id,
audio path) are stored AT MINT TIME — provenance cannot be reconstructed later.
Drillable end-to-end: raw input -> interpretation -> mints -> builds -> outcomes.
Related: media-in-drawer law (any media renders inline in the item's drawer).

## Session trace

- Mint storm + dedup: scripts/dedup_ceo_audio_storm.py (22 closed, 14 kept)
- False-absence + verification law: audit/T-260828-0101 training entry
- Provenance graph probe: provenance-graph-data.json (217 real nodes exported
  from state.db messages + ledger + message-bus; the principal plays with his own
  system's history to decide keep/kill)
