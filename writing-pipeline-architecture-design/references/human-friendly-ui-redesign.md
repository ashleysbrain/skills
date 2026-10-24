# Human-Friendly UI Redesign: Academic Frameworks Behind Plain Language (Aug 2026)

## The Problem

The Writing Studio's "Argument Skeleton" view was built by a specialist who
understood Toulmin argumentation theory. The result was technically correct
but hostile to the actual user (a writer, not an argumentation theorist).

**What the user saw:**
- "Construct the Toulmin argument architecture before any prose"
- "Drag evidence from the pool into claim components"
- "Missing warrants block progression"
- "Three candidate skeletons per §GAP S13"
- "Central Claim · C0" with qualifier text
- "Grounds", "Warrant", "Backing", "Rebuttals" as component labels
- "Walton scheme" dropdown per claim
- Tabs: "Skeleton A (Strong) / Skeleton B (Qualified) / Skeleton C (Contrarian)"
- "Commit Skeleton → Stage 4"

**What the user said:**
> "i don't understand the skeleton system thing in v2. this doesn't feel human friendly"

## The Fix

Redesign the UI to hide academic terminology behind plain language. The
underlying pipeline still uses Toulmin skeletons, Walton schemes, and warrant
checks — the user just never sees those words.

### Translation Table

| Internal (pipeline/code) | User-facing (UI) |
|---|---|
| Toulmin skeleton builder | "Build Your Argument" |
| Central claim / C0 | "Your main argument (thesis)" — textarea |
| Sub-claim | "Key Point" |
| Grounds | "Evidence" — collapsible panel |
| Warrant | "Connection to your main argument" |
| Walton scheme classification | Hidden (dropdown removed from UI) |
| Skeleton A/B/C (Strong/Qualified/Contrarian) | Three cards: Direct / Nuanced / Counter-argument |
| "Missing warrants block progression" | "X points need a connection before you can start writing" |
| "Commit Skeleton → Stage 4" | "Lock Argument → Start Writing" |
| skSupported / skUnderSupported / skUnsupported / skBlocking | "well-supported / need more evidence / missing connections" |
| Evidence Pool (permanent left rail) | Collapsible `<details>` panel |

### Design Principles

1. **Power is invisible.** The system still checks warrants, classifies Walton
   schemes, and enforces Toulmin structure. The user experiences a thesis box,
   key points, and evidence sources.

2. **Plain language for all actions.** "Lock Argument" not "Commit Skeleton."
   "Start Writing" not "→ Stage 4." The user never sees stage numbers.

3. **Approach tabs use descriptions, not labels.** Instead of
   "Strong/Qualified/Contrarian" (academic), use "Direct: Argue your thesis
   head-on" / "Nuanced: Acknowledge limits, argue with caveats" /
   "Counter-argument: Steelman the opposing view first."

4. **Evidence is secondary, not primary.** The old UI had a permanent 280px
   left rail dominating the screen with evidence items. The new UI puts
   evidence in a collapsible `<details>` panel — available when needed, not
   always visible.

5. **Confidence slider uses percentages.** "70%" not "0.70". Humans think
   in percentages, not decimals.

### CSS Changes

Replace `.toulmin-layout` (grid with evidence rail) with a single-column flow.
Replace `.toulmin-tabs` (tablist with Strong/Qualified/Contrarian) with
`.arg-approach-tabs` (card buttons with descriptions). Remove `.evidence-pool`
(permanent sidebar) in favor of `.arg-evidence-panel` (collapsible details).

### JS Changes

- `addClaim()` → `addPoint()` (claim IDs become "Point 1" not "C1")
- `commitSkeleton()` error message: "points need a connection" not "claims missing warrants"
- `_wireSkeletonTabs()` → `switchApproach()` with plain-language approach names
- Nav label: "Build Argument" not "Argument Skeleton"

### Generalizable Pattern

This applies to ANY DS product that uses academic frameworks:

1. **Physics gate** → don't show "physics_gate verdict: REDESIGN" to users.
   Show "This approach may have issues. Here's why..."
2. **Bastani gate** → don't show "Bastani boundary violation". Show
   "The system did the thinking for you here. Can you explain this in
   your own words?"
3. **Sommers revision levels** → don't show "discourse/paragraph/sentence
   revision". Show "Big picture → Section structure → Sentence polish"
4. **Doshi-Hauser homogenization** → don't show "TTR below threshold".
   Show "Your writing is starting to sound similar across sections."

The framework names belong in the code comments and architecture docs, not
in the user's browser.
