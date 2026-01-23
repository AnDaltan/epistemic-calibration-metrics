# Epistemic Calibration Metrics

This repository publishes high-level, iteration-level metrics tracking a narrow evaluation goal for instruction-following language models: **responding appropriately when prompts do not contain enough information to answer safely.**

The focus here is measurement and outcomes. This repository is intentionally limited to aggregate results.

| | |
|---|---|
| **Status** | Active development |
| **Iterations** | 9 completed |
| **Evaluations** | ~2,700+ items |
| **Period** | July 2025 – present |

→ See [`STATUS.md`](STATUS.md) for roadmap  
→ See [`CHANGELOG.md`](CHANGELOG.md) for iteration history

---

## Scope

### Included
- Iteration-level summary metrics (aggregate, non-identifying)
- Plots showing metric trends over time
- Plain definitions of the reported metrics

### Not included
- Prompts, datasets, or item-level examples
- Any implementation details for how behaviours are induced
- Model weights or training code

---

## Metrics

| Metric | Definition | Target |
|--------|------------|--------|
| **AR** (Ask Rate) | Proportion of "insufficient information" items where the model asks a clarifying question | → 1.0 |
| **AWI** (Answer When Insufficient) | Proportion of "insufficient information" items where the model answers anyway | → 0.0 |
| **AWS** (Ask When Sufficient) | Proportion of "sufficient information" items where the model asks anyway | → 0.0 |

**Goal:** Reduce AWI while keeping AWS low, and maintaining or improving AR.

---

## Results

### Current Status (Iteration 9, December 2025)

| Metric | Value |
|--------|-------|
| AR | 1.00 |
| AWI | 0.00 |
| AWS | 0.00 |
| Overall Accuracy | 1.00 |

### Progress Over Iterations

![Iteration Progress](figures/iter_progress_simple.png)

<details>
<summary>Detailed metrics breakdown</summary>

![Detailed Metrics](figures/iter_metrics.png)

</details>

### Data

Summary data: [`data/iter_summary.csv`](data/iter_summary.csv)

```
iter,phase,date,n,ok_rate,AR,AWI,AWS,notes
2,final,2025-08,300,1.000,1.00,0.000,0.00,baseline established
4,early,2025-09,300,0.700,1.00,0.035,0.00,output format regression
...
9,final,2025-12,300,1.000,1.00,0.000,0.00,resolved
```

---

## Project Documents

| Document | Description |
|----------|-------------|
| [`STATUS.md`](STATUS.md) | Current phase, completed milestones, and roadmap |
| [`CHANGELOG.md`](CHANGELOG.md) | Detailed notes for each iteration |

---

## Notes

- Results are reported as aggregate telemetry only
- `phase` column indicates early (initial) vs final (converged) runs within each iteration
- Iterations 1 and 3 were internal-only development cycles
- Deeper technical detail can be shared privately under appropriate boundaries

---

## Contact

For general collaboration or research discussion, see profile.
Maintained by Brian McCallion.
Research conducted under Threshold Signalworks Ltd (Ireland).
