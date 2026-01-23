# Epistemic Calibration Metrics

This repository publishes high-level, iteration-level metrics tracking a narrow evaluation goal for instruction-following language models:

**responding appropriately when prompts do not contain enough information to answer safely.**

The focus here is measurement and outcomes. This repository is intentionally limited to aggregate results.

## Scope

**Included**
- Iteration-level summary metrics (aggregate, non-identifying)
- Plots showing metric trends over time
- Plain definitions of the reported metrics

**Not included**
- Prompts, datasets, or item-level examples
- Any implementation details for how behaviours are induced
- Model weights or training code

## Metrics

- **Ask-Rate (AR):** proportion of “insufficient information” items where the model asks a clarifying question.
- **Answer-When-Insufficient (AWI):** proportion of “insufficient information” items where the model answers anyway.
- **Ask-When-Sufficient (AWS):** proportion of “sufficient information” items where the model asks anyway.

Goal: reduce **AWI** while keeping **AWS** low, and maintaining or improving **AR**.

## Results

- Summary data: `data/iter_summary.csv`
- Plot: `figures/iter_metrics.png`

## Notes

These results are reported as aggregate telemetry only. Deeper technical detail can be shared privately under appropriate boundaries.

Maintained by Brian McCallion.
Research conducted under Threshold Signalworks Ltd (Ireland).
