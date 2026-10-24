# Architecture Validation Against Real Data (2026-08-11)

## The Lesson

When proposing a classification taxonomy or architecture for a knowledge system,
TEST IT AGAINST REAL DATA before committing to the build. Regex patterns that
sound right in theory may classify only 34% of real entries.

## Case Study: Research Hub Classification Architecture

### Initial Proposal (WRONG)
Proposed a "universal study design hierarchy" as the classification system
for all research entries. RCT > cohort > case-control > etc. Sounded correct
because evidence-based medicine uses this hierarchy.

### What Happened When Tested
Ran the study design detector against all 364 findings in the Research Library.

Result: **66% had NO detectable study design.** They were not studies at all.
The library contained:
- 34% scientific facts (textbook knowledge)
- 17% design principles (curated rules)
- 9% historical findings
- 9% critical analyses
- 8% behavioral phenomena
- Only 4% actual empirical findings

The study design hierarchy was universal for 4% of the content. The other
96% needed different authority models entirely.

### Corrected Architecture
Entry type classifier runs FIRST. It determines whether the entry is an
empirical finding (study design hierarchy applies), a benchmark result
(reproducibility ladder), a scientific fact (authority weight), etc.

11 entry types, 3 evidence quality systems, 97% classification rate.

## Generalizable Pattern

Before building ANY classification or taxonomy system:
1. Pull the real data it will operate on
2. Run the proposed classification against a sample (50+ items)
3. Measure the classification rate
4. Examine what falls through — those reveal the missing categories
5. Only commit to the build once the taxonomy covers 90%+ of real data

This applies to: evidence systems, content categorization, user type
classification, agent role taxonomy, any domain where you are tempted to
impose a clean hierarchy on messy real-world content.

## Related
- `references/pipeline-upgrade-micro-task-discipline.md` — same session, reinforces the "test before claiming done" pattern
- The entry type classifier code lives at `/<workspace>`
