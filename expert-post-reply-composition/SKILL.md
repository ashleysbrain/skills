---
name: expert-post-reply-composition
description: Use when composing public replies to experts' posts.
tags: [expert-engagement, positioning, qa, writing]
---

# Expert Post Reply Composition

Composing public replies (LinkedIn comments, article responses) to an expert's own post about their own work, on behalf of the principal. The expert is the author; the reply is read by the person who wrote the thing being discussed.

## Procedure

1. **Pull the post text FIRST** and enumerate the questions the author personally asks — usually at the end, in their own words. Those verbatim questions are the brief. The paper's abstract-level themes are NOT the brief.
   - lnkd.in links: resolve the redirect first (`curl -s -o /dev/null -w "%{redirect_url}"`), fetch the full URL with a mobile UA, and read the post from `og:description` after `html.unescape` — LinkedIn truncates that field well short of long posts, so read it in ~1500-1700 char windows; the author's closing questions and engagement count sit near the tail, past the first window.
2. **Answer each stated question directly**, in the author's order, labeled or clearly one-per-paragraph. Then positioning. Never the reverse.
3. **Position without selling**: one paragraph naming our live instance of the problem (domain-shaped claim, no internals: no engine names, no counts, no ports, no architecture terms; "compute topology" not "mesh"), what we run daily stated as falsifiable enforced invariants, "we are early, we publish our misses," and a collegial ask ("would like to compare notes").
4. **Adversarial review before delivery**: dispatch a reviewer seat to attack the draft (logic, source fidelity, overclaims, secret-sauce leak, sales-tone). Apply numbered fixes. Verify the answer-to-question mapping after the fixes.
5. **Empirical-claim check**: any claim an expert audience can refute from memory is a load-bearing failure (e.g. monotone-improvement invariants are counterexampled by inverse-scaling literature). Cite the counterexample as our own caution rather than being caught by it.
6. **Internal-claim audit (ledger is ground truth)**: every sentence saying we did, trained, measured, or learned something must verify against the task ledger (task-ledger.db) or live system files BEFORE delivery. The required "what we learned" paragraph is the top fabrication vector: the requirement itself tempts an invented learning episode. Query the ledger for the claimed work; zero rows = fabrication. Rewrite to credit the author's finding as the teacher and state the change only in terms of what verifiably exists in the live system.
7. **Absolute negatives are claims too**: "went unmeasured entirely", "we never had X" overstate the moment any internal system partially covers the claim. Check the existing internal surfaces first; if partial coverage exists, state exactly what exists and what is missing instead of claiming absence.
8. **Comments-open precheck**: verify the target post accepts comments BEFORE generating. If the author disabled them, no comment can ever be delivered — metabolize the content as intake or design input, file the card with a hold disposition naming the reason, and say so plainly.
9. **Secret-sauce rule**: proprietary methodology names stay internal. If the principal removes a reference from delivered copy, treat that removal as permanent for all public versions — do not reintroduce it in revisions.
10. **Deliver copy-paste text inline in chat** when asked; also keep a comment-length variant sized to platform caps (~1250 chars) alongside the full version.

## principal LinkedIn comment standard (canonical, from her own posted exemplar)
When the principal asks for a LinkedIn comment on science, produce it in HER structure — she posted the exemplar herself and it is now the template:
1. Opener: "For us at Divinity Science, the most significant implication concerns X." — one line, names the company even though she posts from her PERSONAL profile (never the company page).
2. 3-5 short paragraphs separated by blank lines, each 1-3 sentences. Never a wall of text.
3. One paragraph on what WE learned and how it applies to our system — general mechanisms only, no proprietary internals, no IP leak.
4. Product names ARE allowed when paired with an honest state label, e.g. "the OS OS (our intelligent operating system IN TRAINING)" — the honest label is what makes the name safe.
5. Warm close crediting the author BY NAME ("This is excellent research <Name> & Team"), ending "Thank you and keep up the excellent work!"
6. Truth law throughout: state only what is measured (audited / fixes queued / in training are three different states; only the true one may appear). Non-truth is not safe to post.
Target ~1000 chars. Gates verify it, deliver paste-ready inline.

Signature exemption when scanning: the canonical signature line ("— the operator agent" + the block after it) is principal-posted voice and carries the one sanctioned em dash. Strip the signature block, scan the BODY, PASS on zero body hits — never rewrite the signature and never fail the comment for its em dash.

## Generation law (hardest rule)

The comment text must be BORN inside a studio generation route. The studio's `/api/drafts/rewrite` and `/api/draft/revise` are EDITORS: they analyze and fix text that already exists. Feeding operator-written base text through the rewrite engine produces EDITED prose, not studio-generated prose — the principal rejects this every time she checks, and she checks. Composing a strong draft and having the studio "improve" it is the same violation wearing a cleaner mask: the lineage still starts with operator prose. Until a true generation endpoint exists (e.g. `/api/drafts/comment` taking source URL + post content + the standard) and has a verified run receipt, the honest status is "comment pipeline closed" — deliver that status rather than a studio-polished operator draft. Never substitute for the missing generator; order it from the engine lane (sibling-agent) with spec + acceptance criteria.

## No-reuse law

Two comments on different articles must never share recurring phrasing — same tone, same structure, same truth law, DIFFERENT verbiage every time. Maintain a banned-phrase list seeded from every posted comment (opener formulas, audit sentences, closing formulas all join the list after one use). When driving the studio, put the banned list INSIDE the generation/rewrite instruction text — the engine enforces what it is told, and "same structure" without an explicit no-reuse constraint yields a near-clone of the previous comment that fails only at the final check. Run the banned-phrase check as a gate before delivery; a near-duplicate of a previous comment fails it even when every other gate passes.

## Delivery format

Every comment ships WITH its link: author + title + full source URL above the comment text. A comment without its link is an incomplete delivery. Resolve lnkd.in shortlinks to their full URL first — shortlinks intermittently fail for the recipient.

Flag load-bearing anchors you cannot verify from sources or the ledger (a naming-first claim, a date, a count) inline at delivery, each with a drop-in replacement — the principal decides. Never silently keep an unverifiable claim, and never silently cut one: a quiet edit to a factual sentence is a decision taken away from the person whose name is on the post.

## Pitfalls

- **Sherman gate phrasing: task class, not science content.** Phrase the gate situation in lane vocabulary — "draft the operator agent public LinkedIn comment in Divinity Science brand voice on a neuroscience post about <topic class>" routes GO to the voice engine; a situation string loaded with the post's technical specifics (mechanisms, findings, the author's thesis) reads as a domain-science question no engine owns and returns GENERALIST_REFUSED. After a refusal, re-phrase toward the task class and re-gate — do not hand-draft the comment, which violates the generation law.
- **Positioning paragraphs must survive their own thesis.** A closing "we run this discipline daily: X instead of Y, A instead of B, C instead of D" triad list is itself a testimonial with marketing cadence — the exact failure the piece argues against. Replace with ONE falsifiable enforced invariant from the live system.
- **Do not answer the abstract instead of the author.** A reply structured around the paper's framing while ignoring the author's explicit closing questions reads as evasive to the author and draws an immediate correction.
- **The principal edits delivered text before posting, and the POSTED version is the new canonical standard.** When modified copy comes back (softened hedges, corrected org framing), the modified text is canonical; never revert their wording in later revisions. When she posts her final version publicly, capture it as the exemplar for that class of comment — her edits encode voice rules she will not re-explain.
- **"Send through the writing process" is literal.** Re-writing inline and scanning only the text skips the process the principal asked for — see `veritas-pipeline-operation` for the live pipeline run, and report honestly what stage it reached.
- **Never guess which article a comment is for.** When several referrals are in flight and the target is ambiguous, ask with clickable options before generating — a confidently written comment on the wrong article costs a full correction cycle and erodes trust in the pipeline itself.
- **Do not answer a correction by building an enforcement-looking artifact.** A gate script that sits in a directory with nothing invoking it is a note wearing code — it enforces nothing and reads as bullshit when discovered. Real enforcement means a wired route plus a verified run receipt; if the wiring does not exist, say the capability is closed.
- **Engine-building belongs to the engine lane (sibling-agent), not the operator.** When a missing endpoint is the blocker, file a build order with full spec (inputs, prompt requirements loading the standard file, gate chain, acceptance test) instead of building it yourself — even under "fix yourself" pressure, self-fixing means the operator's own lane (surfaces, wiring, orders), not drifting into the sibling's.
- **State measured claims in the generation instruction, and let the engine correct them.** Give the studio the true numbers and honest state labels (in training / queued / shipped are three different states) inside the instruction text; the engine catching a wrong figure in the operator's draft is the chain working, not a failure.
