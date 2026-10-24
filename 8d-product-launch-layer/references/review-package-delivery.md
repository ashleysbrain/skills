# Release Package Delivery Note

## What this layer adds that the Source + Engine did not
The Source + Engine gave the agent the ability to read signals and report them responsibly.
The Release adds the ability to package that same capability as a product surface.

That means the release is not a new intelligence layer; it is the polished public wrapper that makes the existing intelligence easy to hand off, review, and reuse.

## Why this matters
The user explicitly does not want the existing work generalized away.
This layer respects that by treating the Source + Engine as the baseline and the Release as an additive wrapper.

The practical consequence is that the public doc should stay faithful to the original behavior while making the shipping story cleaner and more useful.

## What the Release does
- keeps the core behavior intact
- presents the stack as a ship-ready product
- gives the user a clear public surface
- keeps the Vault hidden
- makes the handoff easy to inspect
- keeps the public language stable and readable

## What the Release does not do
- it does not replace the Source
- it does not replace the Engine
- it does not expose the Vault
- it does not invent new scoring math
- it does not turn the package into a spec memo
- it does not require the user to infer the release boundary from hidden context

## Delivery rule
When the user asks for the actual skill, deliver the actual SKILL.md or the actual release package file — not just a summary or pointer.

If multiple support files exist, label the main artifact first and then list the references so the handoff stays obvious.

## Verification
The handoff is complete only when the artifact is real, readable, and attached or pathable.

The final check is simple: can someone open the file and understand what the release is, what it adds, and what it intentionally keeps private?
