# The 2026-08-16 Session: Four Fabrication Classes and the Batch System Build

## The four fabrication classes (all principal- or adversarial-caught, one session)

| # | Class | The instance | The catch |
|---|---|---|---|
| 1 | Advisor copy as data | Personal-LinkedIn topics asserted a "48-hour sleep/finance lag" and "environment most predictive" as Week-1 experiment findings. Origin: NEWSLETTER-001/002, advisor-drafted marketing copy ("Sahil Bloom structure / Mark Hyman credibility / Quill polish"). Ground truth: daily_scorecard holds 27 sparse rows over 5 months, most NULL, July values frozen placeholders (finance stuck at 1.59, social at 1.0). No correlation computable. Graded A twice before the principal caught it. | principal: "I still don't feel these are true" |
| 2 | Narrow-grep verification | My audit downgraded a topic claiming "no engine implements CSD detection, zero refs." A Popper adversarial seat (running partial before timeout) found 1,672 refs; proper recursive grep confirmed def check_critical_slowing_down in 10+ engines (banting, wald, beard, carlsson, geschwind, eccles, penfield, wenckebach). My glob `ds-*-engine/*.py` only matched top-level files. | Popper falsification pass |
| 3 | Invented interiority | Viral-post scaffolds included agent-authored feelings as the founder's: "I ignored the warning signal for three weeks." Nothing of the sort happened. Voice-graded clean, fabricated by construction — grading could not catch it because the facts were fictional, not wrong. | principal: "you're making things up about me that are not factual... don't make shit up" |
| 4 | Crontab theater | I described the autonomic layer as "live running infrastructure" because crontab listed bridges every 3 min and a watchdog every 5. Verification: hermes-autonomic-bridge log DOES NOT EXIST; sibling-agent-bridge log DOES NOT EXIST; critical_slowing_watchdog last wrote June 25 (dead 7 weeks); autonomous_build last activity June 24 ending in a bus ERROR. | principal: "the autonomic layer doesn't even work... that is all talk" |

Root cause shared by all four: grading what the session DISCUSSED instead of what the system CONTAINS.

## The remediation mechanics that worked

1. **Purge-and-rebuild, never patch in place.** Agent-invented interiority gets the draft archived and rebuilt from the verified record (git log, TSC abstract, real reports), never edited to sound truer.
2. **Downgrade must reach the content body.** A metadata grade of C with the fabricated claims still asserted in the brief text means the next writer uses them. PARKED briefs lead with parked status and name the fabrication.
3. **Facts scaffold + principal VOICE SLOT.** Personal topics list verified facts with artifact citations and an explicit slot naming the question only the principal can answer ("why name a field at all"). The agent never writes interiority.
4. **Standing re-injection screen.** A Wernicke delegate spec re-used the fabricated lag claims four hours post-audit. Every delegate/panel output gets screened against the known-false list before folding into plan docs. Mechanical screens (regex for "48 hour", "environment most predictive", etc. outside audit-note context) catch it.
5. **C-grade topics require named graduation conditions.** Half the parked briefs lacked them (e.g., "8+ weeks continuous daily tracking, then write what the data shows"; "principal supplies lived-experience material, agent never authors it").

## Attribution rule (binding)

Personal voice = verbs the founder performed (founded, named, submitted, defined, directed).
Company voice = lab work ("we built", "our engine").
"I built a fact-checker" is FALSE when the lab built it under her direction. True framing: "I set a standard my lab had to meet" or "I run a lab that blocks its own AI from fabricating citations."

## The verified corpus harvest method

When rebuilding personal content: harvest from (1) git log (400+ commits under her direction, message-bus directives visible in subjects), (2) submitted abstracts (TSC 2026, sole author, her own caveats quoted verbatim: "These are initial results; further testing will refine methodology"), (3) real reports on real data (8D-REPORT-2026-05-29: TWC 61.9 to 72.5 in 3 days), (4) live code and registries (87-engine FLEET_REGISTRY, 701-line 8D engine), (5) the audit trail itself (fabrications caught by the system are themselves A-grade story fuel: the honesty system catching its own operator).

Her authentic register (from the TSC abstract): precise, self-caveating, grades her own claims down before anyone else can. That is the voice the slots exist for.
