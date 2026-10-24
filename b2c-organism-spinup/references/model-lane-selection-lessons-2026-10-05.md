# Model-Lane Selection Lessons (B2C classification organs)

Fold-target for ledger T-261005-0071 (principal-tagged intake, closed 2026-10-06 by
DWC bus #72687 answer). These rules bind WHENEVER the consumer organism's
model-lane selection math runs (calculation + process-flow design activation,
B2C spinup). Each rule forces a decision — none are decorative.

## Lesson 1 — "Trained" does not mean "learned the taxonomy" (2026-10-05)

Source: LinkedIn post by Neeraj Sinha (lnkd.in/p/gMXJJ_EV -> HTTP 200,
verified live 2026-10-06T19:00Z; tags generativeai/slm/llm). SmolLM2-1.7B-
Instruct fine-tuned with QLoRA 4-bit NF4 on 44 support-ticket examples,
1 epoch, T4. Result: 83.33% valid JSON but 0% exact-match accuracy — the
model understood ticket intent yet invented its own labels
('investigate_duplicate_charge') instead of the predefined business taxonomy
('Request refund'). In-post metrics are auth-walled-unverified; the failure
MODE is the lesson, not the exact numbers.

BINDING RULES for B2C model-lane selection math:

1. PRIVACY/COST ENVELOPE: small local models (SLM class, ~1-2B) fit the B2C
   envelope for classification organs (on-device class work, no PHI egress).
   They are viable lanes — but only under rules 2-3.
2. EVALUATION TESTS THE BUSINESS CONTRACT, never the format. Grade against
   the human taxonomy (human_tok maps, clean_title exact-match), never JSON
   validity, never free-generation similarity. A classifier that emits 100%
   valid JSON at 0% taxonomy match is a FAILED lane, not a working one.
   Gate: exact-match against the closed label set is the acceptance metric.
3. CLOSED-LABEL TAXONOMY + TINY-DATA FINE-TUNE is the right SHAPE for B2C
   classification organs (food parsing, symptom routing): constrain decoding
   to the label set at inference; fine-tune data must map onto the exact
   business labels; verify label-adherence empirically before the lane ships
   (falsification: feed the eval set, count invented labels — must be 0).

This IS the organism's clean-data law seen from the other direction: the
model must be graded against the human taxonomy, never against its own
output plausibility.

Re-surface binding: this file rides the b2c-organism-spinup skill — loaded
at spinup activation, so the lesson resurfaces exactly when the consumer
organism's calculation and process-flow design activates. Ledger row
T-261005-0071 carries the full intake digest (alias KERN-2179, WS-4).
