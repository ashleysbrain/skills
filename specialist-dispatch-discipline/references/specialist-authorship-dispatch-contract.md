# Specialist Authorship Dispatch Contract (template)

Used 2026-08-16 to dispatch the specialist engine (delegation deleg_78bb8d3c, elite
lane) to author the elite-orchestration-default binding skill, after the
main thread was caught authoring it itself. Reusable for ANY binding-artifact
authorship dispatch (skills, protocols, enforcement layers, boot contracts).

## Structure (delegate_task call)

**goal:**
- Role line: `You are DS <Scientist> (<code>) — <specialty>. Elite lane.`
- Adjunct brains (not in FLEET_REGISTRY) carry full credential layering IN
  the dispatch and never invent registry codes; real engines cited by
  verified DS-ECS code only.
- Scope line: `You AUTHOR <artifact>. You do NOT apply changes; you produce
  the design artifact.` (Keeps authorship separate from application so a
  falsifier can review before anything lands.)

**context:**
- Lane split of the two-operator mastermind (who owns what; which defects
  belong to the sibling — e.g. sherman_router.py internals = sibling-agent lane).
- Brain-tag format every user-facing message must carry.
- Physics-PM concepts binding on the design (superposition, entanglement,
  free energy, critical slowing, adiabatic).
- Model lanes (5.2 default / 5.3 elite via delegation).

**In goal or context, include:**
- VERBATIM principal directive intent — never paraphrase corrections.
- ENUMERATED existing enforcement layers with REAL verified paths. The author
  must extend what exists, not invent. List every path verified this session.
- The session's observed failures, stated plainly with quotes.

**DELIVER spec — lettered sections:**
- A: the artifact's full content (e.g. complete SKILL.md with frontmatter;
  description <= 60 chars, trigger-first, one sentence).
- B: minimal enforcement delta, ordered, each with file/path + what changes +
  why it catches drift mechanically + blast radius. Minimality: no new
  daemons, no new ports, extend existing files.
- C: risks + falsifiable acceptance tests with exact commands and expected
  outputs.

**Constraints (always include):**
- Language bans per principal prefs (English only; no em dashes in user-facing text).
- "No invented file paths — every path you reference must be from the
  verified list or a standard the operator agent path." (Kills the classic subagent
  failure of inventing plausible paths.)
- "Do not write files. Return the artifact as your final message." (Lets the
  orchestrator gate the write through the specialist gate and keeps the
  falsifier step possible.)

## Post-authorship chain (mandatory)

1. the specialist engine falsifies the artifact: attack every acceptance test,
   hunt invented paths, unenforceable rules, and lane violations.
2. Orchestrator mechanically applies ONLY surviving content, then actually
   runs the acceptance tests and inspects real output.
3. Sibling-lane defects (router internals, engines) go to sibling-agent via the
   bus with exact repro — with poll-and-integrate, never fire-and-forget.

## Observed failure that produced this contract

Main thread began writing the binding skill for the elite-orchestration
standing directive immediately after receiving it (2026-08-16). principal: "are you
doing this with a generalist brain????? lol... this is the entire problem i
guarantee you won't do this right." Second correction when the recovery
dispatch skipped the sibling exchange: "work with sibling-agent."