# the operator agent Archetype MBTI + OCEAN Combination System

Session: 2026-07-15. Built from `PERSONALITY-PROFILES.md` research (Big Five/OCEAN format) integrated into the 12 Jungian base x 3 tier archetype system in `archetype-variants.js`.

## Structure

36 archetypes total. Each gets a unique `ARCHETYPE_PERSONALITY` entry:

```js
{
  mbti: 'ENFJ',              // 4-letter Myers-Briggs type
  mbtiLabel: 'The Protagonist', // common name
  ocean: { O:80, C:75, E:90, A:60, N:35 },  // 0-100 per trait
  combo: 'Charismatic urgency leader. High extraversion drives collective action.'
}
```

## Design Principle: Same Jungian Family, Different MBTI Per Tier

The 12 Jungian families x 3 tiers (alpha=tactical, beta=strategic, gamma=transcendent) produce 36 unique combos. Same family shares a "personality resemblance" but the tier shifts the MBTI expression.

| Jungian Family | Alpha (tactical) | Beta (strategic) | Gamma (transcendent) |
|---|---|---|---|
| Hero | ENFJ (Tubman) | ENTJ (Spartacus) | INFJ (Joan) |
| Magician | INTP (Tesla) | INTJ (Faraday) | ENFP (Paracelsus) |
| Sage (signal) | ISTJ (Curie) | INTJ (Bacon) | INFJ (Hypatia) |
| Caregiver | ISFJ (Nightingale) | ESTJ (Barton) | INFP (Schweitzer) |
| Explorer | ISTP (Darwin) | INTP (Wallace) | ENTP (Bateson) |
| Rebel | INTP (Galois) | INFJ (Cantor) | ISTJ (Noether) |
| Sage (homeostasis) | ISFJ (Hippocrates) | INTJ (Aretaeus) | INFJ (Weisheipl) |
| Reformer | ENTJ (Virchow) | INTJ (Snow) | INFP (Goldberger) |
| Everyman | ISFP (Fleming) | ESTP (Bradford) | ENFP (Mackenzie) |
| Analyst | ISTJ (Sechenov) | INTJ (Pavlov) | INFJ (Bernhard) |
| Creator | INTJ (Lovelace) | INTP (Turing) | ENTJ (Babbage) |
| Alchemist | INFP (Hahnemann) | ENTJ (Avicenna) | ISTP (Rhazes) |

**14 of 16 MBTI types** appear across the 36 archetypes. Missing: ESFP, ESFJ.

## OCEAN Trait Tier Shift Examples

- Curie alpha: C:98 (measurement-obsessed) -> Curie gamma: O:92 (transcendent pattern-seeing)
- Galois alpha: N:55 (turbulent rebel) -> Galois gamma: N:25 (calm conservation law)
- Fleming alpha: C:60 (humble discoverer) -> Fleming beta: C:72 (opportunity architect)

## Integration Points (All Must Be Verified)

Personality data must propagate to ALL of these, not just the Psych tab:

1. `ARCHETYPE_PERSONALITY` object (data source - 36 entries)
2. `getArchetypePersonality()` helper function
3. `getArchetypesForContext()` returns mbti/ocean/combo per archetype
4. `getArchetypeVariant()` returns mbti/ocean/combo for single lookup
5. `BRIDGE_ARCHETYPES` derived array carries personality fields
6. `__activePersonality` runtime state object (both init instances)
7. Psych tab card grid (MBTI badge per card)
8. Psych tab deep dive (Combination Personality panel with OCEAN bars)
9. Birth/Edit/Spawn dropdowns list all 36 with MBTI badges
10. Chat greeting shows MBTI inline
11. Bridge selector dropdown shows MBTI per archetype
12. `applyArchetypeTrajectory()` stores personality in `__orgTrajectory`
13. Dead links to `gg-archetypes.html` redirected to Psych tab

## Audit Script

Run after any personality integration change to verify completeness:

```js
// Browser console verification
(() => {
  const results = {};
  results.personality_loaded = typeof getArchetypePersonality === 'function';
  results.archetypes_36_count = typeof ARCHETYPES_36 !== 'undefined' ? ARCHETYPES_36.length : 0;
  results.personality_count = typeof ARCHETYPE_PERSONALITY !== 'undefined' ? Object.keys(ARCHETYPE_PERSONALITY).length : 0;
  
  const ctxList = getArchetypesForContext('gg');
  results.context_has_mbti = ctxList.length > 0 && !!ctxList[0].mbti;
  
  const variant = getArchetypeVariant('curie', 'gg');
  results.variant_has_mbti = variant ? !!variant.mbti : false;
  
  results.bridge_has_mbti = BRIDGE_ARCHETYPES[0]?.mbti !== undefined;
  results.bridge_count = BRIDGE_ARCHETYPES.length;
  
  selectArchBridge('tubman');
  results.active_personality_has_mbti = !!(window.__activePersonality?.mbti);
  results.active_personality_mbti = window.__activePersonality?.mbti;
  results.active_personality_ocean = window.__activePersonality?.ocean;
  
  selectArchBridge('curie');
  results.curie_active_mbti = window.__activePersonality?.mbti;
  
  results.traj_has_personality = !!(window.__orgTrajectory?.personality?.mbti);
  results.traj_personality_mbti = window.__orgTrajectory?.personality?.mbti;
  
  return JSON.stringify(results, null, 2);
})()
```

All values should be truthy/expected. Any null or false = integration gap.

## Key Files

- `/<workspace>` — `ARCHETYPE_PERSONALITY` object + `getArchetypePersonality()` helper
- `/<workspace>` — All UI integration (Psych tab, dropdowns, chat, bridge selector)
- `/<workspace>` — Original research data (Big Five + DISC + Enneagram)
