# Adversarial Review Example — TSC 2026 (2026-08-05)

Concrete example of Step 6 (adversarial review) applied to the TSC 2026
viral conference product brainstorm. 10 ideas reviewed by 4 specialists.

## The 4 Reviewers

### the specialist engine (Falsifiability)
Can you TEST whether each idea will go viral? What is the falsifiable
prediction? Kill ideas with no measurable viral hypothesis.

### N. Katherine Hayles (Digital Media Critic, author of "How We Think")
Would the target audience ACTUALLY use this? What assumptions are wrong?
Is it a technologist's fantasy of what researchers want?

### Ev Williams (Twitter/Blogger/Medium founder)
What is the ACTUAL viral mechanic? Where does the sharing loop break?
A utility with no loop is not a viral product.

### Bruce Sterling (Science fiction author, SXSW Interactive veteran)
Is this worthy of the conference? Does it respect the audience's
intelligence? Or is it a gimmick that will be mocked?

## Results: 50% Kill Rate

The adversarial review KILLED 5 of the 10 ideas, including some that
scored well in initial synthesis:

### KILLED (5)
1. **TSC Atlas** (scored 19/21 in synthesis!) — no viral loop (Williams),
   unfalsifiable (Popper), overbuilt (Sterling). Utility, not viral.
2. **Poster Genome** — no viral loop, no testable hypothesis
3. **Pulse** — wrong mental model for academics, engagement theater
4. **MindCard** — trivializing framing, gimmick risk
5. **TSC Decoder** — no viral loop, unfalsifiable

### SURVIVED (5, re-ranked)
1. **Camp Compass** (4/4 PASS) — clear winner, tight viral loop
2. **Theory Wars** (3.5/4) — rename to less combative framing
3. **Phi Constellation** (3/4) — needs pull mechanic
4. **Mirror** (3/4) — highest ceiling, needs rigorous prompt design
5. **Blind Match** (2.5/4) — not viral but best connection tool

## Key Lesson

The adversarial review is more trustworthy than initial synthesis.
TSC Atlas scored 19/21 initially but was killed 1/4 in adversarial
review because it had no actual viral loop. The synthesis scored
utility and beauty, but the adversarial review caught the absence
of a sharing mechanism.

ALWAYS run Step 6 before showing ideas to the user. The user expects
it and will not trust first-pass output without it.

## Execution Note

The adversarial review subagent FAILED on first dispatch because it
loaded 3 heavy skills (adversarial-elite-panel-review,
specialist-panel-ideation, ds-popper-audit) which consumed the entire
context budget. The subagent hit max_iterations before writing any
output. The review was then executed in-host successfully.

Lesson: adversarial review should be executed in-host, not delegated
to a subagent that loads reference skills.
