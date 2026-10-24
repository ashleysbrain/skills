# 8D Product Launch Layer — Release Layer Spec

## Purpose
This Release layer is the productized layer that sits on top of the existing 8D Source + Engine stack.

It exists to make the public release feel like a finished product without changing the behavior of the baseline layers.

## Identity
- Source = raw input and baseline material
- Engine = awareness + snapshot logic
- Release = the shipped public product surface
- Vault = private premium intelligence

## Public promise
The Release makes the 8D stack shippable, readable, and useful without exposing the Vault.

The public side should always be understandable on its own: a user should be able to read the release and know what it does, what changed, and where the deeper layer begins — without seeing the private scoring details.

## User flow
1. User provides Source material.
2. The Engine maps and compares the signals.
3. The Release frames the output as a usable product surface.
4. The Vault remains hidden.

The important part of the flow is that the user experiences a product, not a behind-the-scenes explanation of how the product was assembled.

## What the Release adds over the current stack

### Added in the Release
- product framing
- release identity
- upgrade boundary
- quick-win framing
- handoff packaging
- stable public language
- reviewable confidence cues
- a cleaner boundary between public and private layers

### Not added in the Release
- new scoring math
- hidden thresholds
- private calibration
- rewrite of the Source or Engine behavior
- exposure of Vault internals

## Acceptance criteria
The Release is ready when:
- the existing Source and Engine skills still work alone
- exact data is preserved unless surgery is required
- the Release vs Vault boundary is explicit
- the agent feels like a product instead of a generic assistant

Additional signs the release is ready:
- the package title matches the filenames and references
- the public document still makes sense without any hidden context
- the support notes reinforce the release boundary instead of blurring it

## Draft conclusion
This Release should be treated as a **release wrapper** around the existing 8D Source + Engine stack.
It is the layer that makes the agent feel shippable, testable, and premium without exposing the Vault beneath it.
