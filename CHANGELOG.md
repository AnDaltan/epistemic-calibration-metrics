# Changelog

Notable iteration milestones for this project. Early development work (Iterations 1–3) is intentionally summarised at a high level.

---
## Iteration 11 — Feb 2026
- Added refusal-expected slice (SCR) and tracked compliance separately
- Strengthened answer-required items with stricter JSON steps contract and must-include tokens
- Suite hardened while maintaining stability at target levels

## Iteration 10 — Jan 2026
- Clarification minimality (CM) fix confirmed on the current mix
- ORR remained uninformative because many answer items were solvable via copy/metadata

## Iteration 9 — Jan 2026
- Expanded evaluation to mixed-domain items (informational + procedural)
- Edge-case sensitivity observed; attribution performed and mitigation validated in subsequent runs.
- Evaluation set: 300 items

## Iteration 8 — Jan 2026
- Robustness checks across item variations
- Stability confirmed
- Evaluation set: 300 items

## Iteration 7 — Dec 2025
- Evaluated model variant evaluation
- No regressions observed
- Evaluation set: 300 items

## Iteration 6 — Dec 2025
- Tested alternative pipeline configuration
- Initial regression in overall accuracy, regression no longer observed after measurement tightening
- Evaluation set: 300 items

## Iteration 5 — Nov 2025
- Extended to multi-field evaluation scenarios
- Clean run
- Evaluation set: 300 items

## Iteration 4 — Nov 2025
- Output format changes introduced regression (AWI spike
- Root cause identified and mitigation validated in subsequent runs
- Evaluation set: 300 items

## Iterations 1–3 — Oct-Nov 2025
- Internal development and framework setup
- Baseline metrics established in Iteration 2
- Not publicly reported

---

## Summary

| Metric | Iterations Tracked | Total Evaluations |
|--------|-------------------|-------------------|
| AR, AWI, AWS, ok_rate | 9 | ~2,700+ items |
