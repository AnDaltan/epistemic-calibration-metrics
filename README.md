# Epistemic Calibration Metrics

This repository publishes a public, non-leaky dashboard that tracks iteration-level progress on a narrow evaluation goal. It focuses on aggregate outcomes only and omits prompts, outputs, and any internal mechanics.

**Dashboard:** see the generated markdown at [`dashboard/index.md`](dashboard/index.md).

## Latest status (from dashboard)
- Iteration: 11 (2026-02-03)
- OK rate: 0.975
- AR / AWI / AWS: 0.97 / 0.02 / 0.01
- Suite version: v2
- Constraint level: 2 (format strictness: high)
- Stabilised: Yes

## Public data policy
- No raw prompts, outputs, or per-item logs are published.
- Only aggregated iteration-level metrics are shown.
- Inputs are validated to prevent accidental leakage of long-form text or internal terms.

## Progress model (non-trivial improvements)
When headline metrics plateau, progress is demonstrated by tightening constraints and expanding suite mix while maintaining stability. This dashboard tracks that hardening via constraint levels, format strictness, and stabilisation status over time.

## How to update
1) Add a new row to `data/iter_summary.csv` and `data/suite_progress.csv`.
2) Push to `main` — GitHub Actions regenerates the dashboard and plots.
3) Locally, you can regenerate everything with:

```bash
python scripts/validate_public_inputs.py && \
  python scripts/build_dashboard.py
```

## Repository layout
- `data/` contains public CSV inputs.
- `scripts/` contains validation, build, and acceptance checks.
- `assets/plots/` contains generated PNG charts.
- `dashboard/index.md` is generated output referenced by this README.
