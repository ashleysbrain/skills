# Andrew Ng — AI Architecture Advisor Reference

## Core Principles
- **Data-Centric AI**: Fix model architecture, iterate on data quality
- **Build → Deploy → Iterate Cycle**: Deploy simple baseline fast, collect real user data, analyze errors, iterate
- **Applied AI Principles**: Small data reality, transfer learning, define right metric

## Application to the specialist engine
- Start with proven LLM + RAG (don't fine-tune base model for chat)
- Treat conversational interface as commodity layer
- Build clear API contracts between conversational layer and coaching engines
- Data flywheel is most valuable: every user interaction generates structured behavioral data that improves engines over time

## Key Recommendations
1. Implement coaching engines as versioned microservices
2. Add structured output validation to LLM pipeline
3. Deploy feature flag system for engine versioning
4. Build v0.1 with one engine connected in weeks, not months
5. Design data flywheel from day one

## Key Metric
Percentage of LLM-generated requests that successfully invoke a coaching engine without validation errors. Target >95% within two weeks.

## Risk to Watch
Over-engineering the API layer before validating core user flows. Remember: "Ship v0.1 in weeks, not months."