# Epistemic Calibration Metrics Dashboard

**Latest snapshot**

- Iteration: 11
- Date (UTC): 2026-02-03
- Items: 300
- OK rate: 0.975
- Suite version: v2
- Constraint level: 2
- Mix: Ask 60% / Answer 30% / Refuse 10%
- Stabilised: Yes

## Progress charts

![ok rate](../assets/plots/ok_rate.png)

![suite mix](../assets/plots/mix_over_time.png)

![suite hardening](../assets/plots/suite_hardening.png)

![quality gates](../assets/plots/quality_gates.png)

## Suite hardening narrative

| iter | date_utc | suite_version | constraint_level | suite_changes | stabilised |
| --- | --- | --- | --- | --- | --- |
| 10 | 2026-01 | v1 | 1 | Answer format tightened | Yes |
| 11 | 2026-02-03 | v2 | 2 | Refusal slice added; parseable underspec introduced | Yes |

## Data policy

No raw prompts, outputs, or per-item logs are published.
Only aggregated iteration-level metrics are shown.

## How to reproduce

```bash
python scripts/validate_public_inputs.py && \
  python scripts/build_dashboard.py
```

## Update cadence

Dashboard artefacts are regenerated on every push to main and should be updated
whenever new iteration rows are added to the CSVs.
