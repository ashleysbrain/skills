# Scoring Methodology Verification (Mean vs Sum)

The most important audit step that is easy to skip. When a user asks
"is that even accurate scoring?" the answer requires going back to the
PRIMARY SOURCE and verifying the scoring method itself, not just the
keying direction.

## The Trap

You verified the +/- keying. You verified the item text. You verified the
facet/domain aggregation. But did you verify whether the source says to
SUM or AVERAGE the item scores?

## IPIP Official Scoring Instruction

Source: ipip.ori.org/newScoringInstructions.htm

> "For + keyed items, the response Very Inaccurate is assigned a value
> of 1, Moderately Inaccurate a value of 2, Neither Inaccurate nor
> Accurate a 3, Moderately Accurate a 4, and Very Accurate a value of
> 5. For - keyed items, the response Very Inaccurate is assigned a value
> of 5, Moderately Inaccurate a value of 4, Neither Inaccurate nor
> Accurate a 3, Moderately Accurate a 2, and Very Accurate a value of
> 1. Once numbers are assigned for all of the items in the scale, just
> sum all the values to obtain a total scale score."

The official instruction says **SUM**.

## Why IPIP-NEO-120 Uses Mean Instead

Johnson (2014) selected 4 items per facet from the original 10-item pools.
His published norms (mean=3.0, sd=0.8) are on a 1-5 MEAN scale, not a sum
scale. Percentile estimation against those norms requires mean scoring.

This means:
- **SUM** (4-20 range) = official raw IPIP scale score
- **MEAN** (1-5 range) = Johnson's IPIP-NEO-120 scale, needed for percentiles

Both represent the same personality measurement. They are linear transforms
of each other. The choice depends on what norms you compare against.

## The IPIP Norms Warning (Critical)

Source: ipip.ori.org/newNorms.htm

The IPIP website EXPLICITLY warns against using canned percentile norms:

> "No norms are available on the IPIP website... One should be very wary of
> using canned 'norms' because it isn't obvious that one could ever find a
> population of which one's present sample is a representative subset. Most
> 'norms' are misleading, and therefore they should not be used. Far more
> defensible are local norms, which one develops oneself."

And from ipip.ori.org/InterpretingIndividualIPIPScaleScores.htm:

> "To interpret individuals' scores, one might calculate the mean and
> standard deviation (SD) for a sample of persons, usually of the same sex
> and a particular age range, and interpret scores within one-half SD of
> the mean as 'average.' Scores outside that range can be interpreted as
> 'low' or 'high.'"

This means:
1. Any percentile you show is an ESTIMATE, not a validated norm
2. Every percentile must carry a disclaimer
3. The IPIP-recommended interpretation is categorical (low/average/high)
   based on 0.5 SD bands, not precise percentile numbers
4. For real interpretation, the user should build LOCAL norms from their
   own sample

The `interpret_score()` function should return quintile labels:
- score >= mean + 1.5*SD = "very high"
- score >= mean + 0.5*SD = "high"
- score <= mean - 1.5*SD = "very low"
- score <= mean - 0.5*SD = "low"
- otherwise = "average"

## What Must Be in the Explanation Endpoint

The `/explanation` endpoint (calculation transparency) MUST include:

1. The official scoring instruction text, verbatim, with source URL
2. BOTH sum and mean for every facet (never just one)
3. Explicit documentation of which method is used for percentile conversion
4. A percentile disclaimer: normal CDF is an approximation. Johnson's actual
   percentiles use the full empirical distribution from N=619,150, not a
   normal curve fit. Actual placement may vary 5-10 percentile points.
5. All three sources cited:
   - Johnson (2014). JRP, 51, 78-89.
   - ipip.ori.org/newScoringInstructions.htm
   - ipip.ori.org/newNEO_FacetsTable.htm

## The Verification Question to Ask Yourself

Before declaring scoring "done", ask:

> "If a psychometrics professor looked at my scoring code and my
> explanation output, would they find the method defensible?"

If you cannot show the official instruction alongside your implementation
choice, the answer is no.

## Session Origin

2026-08-06. User asked "is that even accurate scoring? isnt scoring
explained in the site?" This exposed that the explanation endpoint
documented the forward/reverse keying but NOT the sum-vs-mean decision.
The fix: fetch ipip.ori.org/newScoringInstructions.htm, quote it
verbatim, and report both scoring methods.
