# Runtime Package Audit Notes

## Learning from the the specialist engine pass
When a project has a runtime-facing wrapper plus a docs index, do not treat the wrapper's startup read list as complete on its own. Reconcile:
- the wrapper file (`AGENT.md`, `SOUL.md`, or equivalent)
- the docs index / README
- any support docs named in the index, especially aliasing and scoring rubrics

## Audit checklist
1. Read the runtime wrapper startup list.
2. Read the docs index.
3. Check whether the index names any support docs the wrapper omitted.
4. Verify the wrapper and index point to the same canonical package.
5. Patch the wrapper if startup coverage is incomplete.

## Example support docs that are easy to miss
- aliasing schema for canonical public aliases
- public scoring rubric or proxy-score contract
- state machine / handoff rules when the wrapper is only a thin shell

## Practical takeaway
A wrapper can be syntactically correct and still be operationally incomplete if it skips a support doc that the index treats as core.