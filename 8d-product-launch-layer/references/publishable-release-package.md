# Publishable Release Package Shape

This reference defines the shape of the publishable release package for the 8D product stack.

## What belongs in the shipped package
- release identity
- version label
- scope of the release
- what ships
- public surface summary
- private Vault boundary summary
- runtime behavior summary
- what the Release adds
- what the Release does not change
- acceptance criteria
- included artifacts

## What must be excluded from the shipped package
- task instructions to the agent
- internal authoring notes
- prompts about what to do next
- meta commentary about how the package was created
- links/pointers in place of the real artifact
- private scoring logic
- operational instructions that belong only in the authoring skill

## Rule
The published document should read like a package that can be handed off, not like an instruction memo.

## Layer clarification
- Source: intake and baseline material
- Engine: awareness + snapshot behavior
- Release: packaging, release identity, boundary definition, handoff format
- Vault: private premium logic
- The package must preserve the Source + Engine core and describe the Release as the wrapper above it
