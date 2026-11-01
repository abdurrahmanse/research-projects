# 06 — Experimental Methodology, Evaluation and Explainability

Everything below is implemented in `projects/cgth_hybrid_study.ipynb`; task numbers refer to its cells.

## Pipeline (leakage-free)
1. Load `post natal data.csv` read-only. Drop `Timestamp`. Remove exact duplicate rows before any split (Tasks 3–5).
2. Target: `Feeling anxious` = Yes → 1.
3. Most-frequent imputation and one-hot encoding are fitted inside each training fold only (Task 6).
4. Settings are fixed before the run (Task 2): seed 42, δ = 0.2, non-inferiority margin 0.03, δ grid 0–0.5.
5. Validation: 5-fold stratified cross-validation repeated 10 times (50 folds). All models use the same folds, so results are paired (Task 9).
6. No separate hold-out set: at n = 326 a 66-row test set is too noisy (accuracy ranged 0.67–0.86 across seeds in the audit).
7. Hyperparameters are fixed in advance (RF: 300 trees, depth 4; LR: default L2). This is a limitation to state.

## Metrics (Task 8)
Balanced accuracy (primary), accuracy, sensitivity, specificity, F1, MCC, ROC-AUC, and LR coverage for CGTH. The threshold is 0.5 throughout.

## Statistics (Tasks 10–11)
- **Confidence intervals:** mean ± t × corrected standard error. The Nadeau–Bengio correction widens the interval because cross-validation training sets overlap. (This replaces the fold-percentile ranges used earlier, which were not confidence intervals.)
- **H1 (non-inferiority vs RF):** t = (mean difference + 0.03) / corrected SE, one-sided.
- **H2 (superiority vs LR):** t = mean difference / corrected SE, one-sided.
- A non-significant result is reported as "no significant evidence", not as "equal".

## Imbalance
58/42 is mild. Stratified folds and balanced accuracy handle it. No SMOTE: on categorical data with 326 rows it mainly creates more near-duplicates.

## Explainability
- **Transparent decisions:** LR odds ratios (Task 14) explain about two-thirds of all decisions directly.
- **Transparency–performance curve (Task 12):** balanced accuracy against coverage for every δ.
- **Gate check (Task 13):** accuracy of LR on confident vs uncertain cases, and RF on uncertain cases.
- Odds ratios describe associations between survey answers; they are not causal and not clinical risk factors.

## Robustness (Task 15)
The whole experiment is rerun (a) with duplicates kept and (b) without the guilt item.

## Figures and tables for the thesis
| Item | Content | Task |
|---|---|---|
| Table 1 | Data audit (rows, duplicates, missing values, positive rate) | 4–5 |
| Table 2 | Results with corrected 95% CI | 10 |
| Table 3 | Hypothesis tests | 11 |
| Table 4 | Gate check | 13 |
| Table 5 | Top odds ratios | 14 |
| Table 6 | Robustness | 15 |
| Fig 1 | Architecture diagram (doc 05) | — |
| Fig 2 | Transparency vs performance curve | 12 |
