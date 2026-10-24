# Coaching Score Adapter

This reference captures the coaching-engine-specific scoring convention.

## Core rule

When the conversation is about the coaching engine, and the user says "scores," the default meaning is the *public-information-only coaching score* derived from TWC unless a narrower metric is explicitly named.

The public coaching score is a proxy: it must be built from public, observable, or openly stated information only. It is not the same thing as any private/internal TWC score.

## Relationship between scores

- **TWC score**: the underlying proprietary/internal score
- **Coaching score**: the public-information-only working score used for ongoing coaching decisions
- **Health state**: the lightweight status derived from the coaching score

## Operational use

Use the coaching score when the engine needs a day-to-day health signal for:
- persistent coach mode
- ongoing advisor maintenance
- deciding whether an advisor needs attention
- keeping coaching advice current without overreacting to raw score volatility

## Maintenance rule

The coaching score should be reviewed and refreshed regularly so the advisor set stays healthy over time.

## Writing rule

In coaching-engine docs and responses, avoid saying "score" without qualification when the distinction matters. Prefer:
- public TWC score
- coaching score
- health state

