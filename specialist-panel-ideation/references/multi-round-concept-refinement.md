# Multi-Round Concept Refinement & Reviewer Overreach Corrections

## Context
After ideation produces a winning concept, the concept itself needs
iterative refinement through successive adversarial rounds. This is
distinct from Step 6 (one-shot adversarial review of N ideas). Here
the input is ONE concept, and the process is multi-round.

## The Multi-Round Pattern

### Round 1: Initial concept review
- 4 reviewers, each with a specific lens
- Expected outcome: 40-50% of features killed, core mechanic validated
- Reviewer types: falsifiability, audience realism, viral mechanic, dignity

### Round 2: Different brains, deeper layers
- NEW reviewers, not the same ones. Each round must use different
  expertise areas or it just rehashes Round 1 findings.
- Round 2 reviewer types should go DEEPER: privacy/ethics (Lanier),
  actual audience member (Seth), startup viability (Graham), UX
  friction (Norman), long-term vision (Brand), network science
  (Pentland)
- Expected outcome: structural flaws found that Round 1 missed
  (build sequence, interaction design, cold start, data bias)

### Key rule: each round finds NEW gaps
From the multi-pass adversarial principle (memory): each pass surfaces
issues the previous pass missed. Never skip a round because "we already
reviewed it." Round 2 with different brains will find things Round 1
with different brains could not see.

## Reviewer Overreach Corrections

Adversarial reviewers can overcorrect. The user is the final arbiter.
When a reviewer flags something the user disagrees with, the user's
judgment wins. Capture the correction explicitly.

### Overreach 1: Public data is NOT private data (2026-08-05)

**Reviewer claim (Lanier/Seth):** Pre-building profiles from scraped
publications is "data colonialism" and "data extraction without consent."

**User correction:** "This information is public. They are publishing
their research publicly. I'm not tapping into their personal data or
spying on them. Why is that flagged?"

**Resolution:** Publications, abstracts, poster titles, ORCID profiles
are PUBLIC. They are already indexed by Google Scholar, OpenAlex,
ResearchGate, and every university page. Scraping public publications
to pre-build a profile is not spying. It is what every academic search
engine already does.

**The correct fix:** Pre-build stays. Add a confirm-or-edit step at
claim time ("Is this correct? Edit what you want"). This solves
consent (they confirm), accuracy (they fix errors), and bias (they
add missing work) without abandoning the pre-build. The pre-built card
REDUCES friction at claim time because people edit faster than they
create from scratch.

**When the reviewer flag IS valid:** If the data were truly private
(email, phone, location, browsing behavior), the flag would be correct.
The distinction is: published academic work vs personal/private data.

### Overreach 2: Two-tier systems create inequality (general pattern)

Reviewers may flag any differentiation between user types as
"creating a caste system." Evaluate whether the differentiation is
actually harmful or just reflects natural data depth differences.

Example: presenters have publications auto-filled, non-presenters do
not. This is not inequality — it reflects different amounts of public
data available. Both get the same card FORMAT. The data depth differs
because the public footprint differs.

## Concept Evolution Example: TSC 2026 Collaboration Constellation

### Iteration 1: Method Exchange
- Concept: copy-paste your method into a tool, get a card
- User kill: "That's a lot of manual entry. Copying and pasting their
  method doesn't even make sense."
- Lesson: the data already exists publicly. Pull it, don't make users
  enter it.

### Iteration 2: Zero-Entry (pre-build all profiles)
- Concept: scrape 483 presenters, auto-build profiles, type name at
  conference to claim
- User correction: only counted 48 speakers, actually 483 presenters
  + hundreds of non-presenting attendees
- Lesson: count the ACTUAL audience before designing

### Iteration 3: Two-tier (presenters pre-built, non-presenters quick-build)
- Concept: pre-built cards for presenters, topic selector for others
- Adversarial Round 1: killed scan counter gamification, killed global
  map as primary, identified cold start problem
- Synthesis: personal proximity view, mutual confirmation, opt-in map

### Iteration 4: After Round 2 (Lanier/Seth/Graham/Norman/Brand/Pentland)
- 7 critical gaps found across all 6 reviewers
- User corrected reviewer overreach on public data
- Final concept: confirm-or-edit pre-build, presenter-authored primary
  field, physical token not QR coupon, 30-day follow-up digest as
  primary artifact, DS branding as footer only

### The trajectory
Each iteration was SHORTER and MORE FOCUSED than the last. The concept
converged from a sprawling "do everything" tool to a focused "connect
two people meaningfully" tool. This is the physics principle: the
system found its ground state through successive energy minimization
(adversarial rounds).
