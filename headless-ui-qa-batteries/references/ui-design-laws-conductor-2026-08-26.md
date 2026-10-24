# UI design laws: drawers over tabs, census-then-extend, surface marriage — 2026-08-26

Session detail for the interface-design corrections issued while building
the the OS ruling queue surface. The canonical surface is **Conductor
(:port)** — `conductor_screen.py` + `conduction_daemon.py`.

## The triggering corrections (verbatim principal intent)

1. "you laid this out all in tabs??? that is not dynamic nor interactive..
   i had you work on the drawers for a reason. I liked the lists with the
   interactive dynamics and features within the lists and drawers.. this
   tabs at the top thing is NOT elite design and you just erased our hard
   work."
2. "i also don't see how I can toggle between organisms or go through the
   calendar views... this feels like it is much more narrow than the scope
   you had built before... ensure we don't lose the features we worked on
   like the os chat and research features. you forgot that stuff."
3. "I did like the fonts of the other view but I need the functionality of
   this original view" — typography from the new surface was approved;
   scope was not.

## Law 1: drawers + interactive lists are the house style; tabs-at-top are a regression

The elite pattern (iterated across Conductor + Research Studio + gg-ops):
dense interactive LISTS whose rows open slide-out DRAWERS. Inside drawers:
linkified IDs (T-XXXX, bus #NNNN) that drill further, clickable depends_on
chains, in-drawer actions (Approve/Reject/Defer buttons, modal notes).
Scenario lenses carry live counts ON the toggle buttons. Dimming is the
visibility language (human bright, AI dimmed-but-drillable). A new surface
built as top-tabs with plain panes reads as "erased our hard work" even
when feature-equivalent — the interaction model IS the product.

## Law 2: census-then-extend — never build a parallel surface for an existing capability

Before building ANY new surface: census what already exists (ports, repos,
daemons, sibling-thread work). If a canonical surface covers the territory
(Conductor already had /api/decide, drill drawers, ruling cards with
What/Why-you/If-approved/If-rejected), EXTEND it — add the view, patch the
daemon query, restart — instead of shipping a parallel page. The parallel
tab console (:port) duplicated capability the principal had already iterated on.

## Law 3: surface marriage — port approved tokens into the canonical surface

When a throwaway/secondary surface wins praise for a specific token
(typography scale, a color, a component), do NOT keep the secondary surface
alive for it — port the token into the canonical surface. Live example:
console's 14px body / 1.45 line-height patched into Conductor's body rule
(Conductor already ran Manrope/Sora/Space Grotesk; only the scale differed).

## Daemon data-query staleness (same class as serving stale bytes)

A canonical surface is only as current as its API queries. The daemon's
rulings query (`kind='decision' AND state IN ('open','claimed')`) went
stale after ledger triage: it excluded the human-only OIDC task and
included fleet-claimed rows the OS had already taken. When the ledger's
semantics change (new claimed_by conventions, new state usage), grep EVERY
consumer query — same discipline as the DECISION:→DECIDE: consumer grep.

## Direction-on-record: execute, don't re-ask (the whisper case)

A decision task sat in the human queue while its OWN detail carried the
principal's direction verbatim (urgency field: "today - principal already rejected the
garble; every voice note in flight keeps garbling" + an approved
if_approved change pair citing exact lines). Correct action: execute the
cited change (intake_triage.py tiny→small + timeout 480→900, config.yaml
stt.local.model=small), close citing the direction, log the event, watch
adiabatically. Re-asking what the record already answers is the same lazy
queue pattern as escalating resolvable decisions.
