# 09 — Final Method and Results

Notebook: `notebooks/final_thesis_study.ipynb` (47 short tasks, simple figures). This is the final study design; docs 04–08 describe the earlier confidence-gated design (CGTH), whose notebook remains in git history.

## Why the design changed
The confidence-gated hybrid (logistic regression deciding confident cases, random forest the rest) kept most decisions transparent but ranked below random forest, and its non-inferiority was not established under a stricter test. The final study therefore uses a small, conventional set of five algorithms, makes the hybrid the performance-oriented model, and moves interpretability to SHAP and LIME, which explain every prediction of any model.

## The five algorithms

| Algorithm | Role |
|---|---|
| Logistic regression | Simple, transparent baseline |
| Random forest | Bagged trees |
| Extra trees | Randomised trees |
| SVM (calibrated) | Margin-based kernel model |
| **Hybrid Ensemble (proposed)** | Soft voting of random forest, extra trees and SVM |

The hybrid combination was selected among 55 candidate hybrids (50 soft-voting combinations of 2–4 of six base models, and 5 stacking models) on two development runs (seeds 7 and 2026) and then confirmed on a separate final run (seed 42), so the final ranking is not tuned to the reported folds.

## Main results (seed 42, 50 test folds)

| Model | Balanced accuracy (95% CI) | ROC-AUC | Rank |
|---|---|---|---|
| **Hybrid Ensemble** | **0.772 [0.721, 0.823]** | 0.843 | **1** |
| Random forest | 0.771 [0.719, 0.823] | 0.843 | 2 |
| Extra trees | 0.760 [0.711, 0.809] | 0.848 | 3 |
| SVM | 0.767 [0.716, 0.818] | 0.822 | 4 |
| Logistic regression | 0.730 [0.668, 0.792] | 0.800 | 5 |

- No difference is significant after Bonferroni correction (largest: Hybrid Ensemble vs logistic regression, +4.2 points, p = 0.038, corrected p = 0.15).
- Train–test gap in balanced accuracy: Hybrid Ensemble 10.2 points, extra trees 17.1, logistic regression 4.5.
- Out-of-fold Brier score of the Hybrid Ensemble: 0.163; its calibration curve follows the diagonal closely.

## Explainable AI (Hybrid Ensemble, 66 held-out respondents)
- **Global:** guilt 42.4% (SHAP) / 47.6% (LIME) of total importance; then appetite and irritability in both.
- **Agreement:** global Spearman 0.983; per-person 0.734; same top question for 84.8% of respondents.
- **Speed:** SHAP 0.41 s, LIME 0.08 s per respondent.

## Validity checks
- **Leakage check:** random forest 98.8% accuracy with duplicates kept (about 94% of test rows copy a training row) vs 76.0% on unique rows (Nayee et al. 2026 report 96.99%).
- **Sample size:** at least 374 rows needed by the minimum Riley et al. (2020) criterion; 326 available.
- **Fairness by age band:** Hybrid Ensemble 65.6% (25–30) to 83.7% (30–35).

## Limitations
- Single self-reported item as the label; no clinical reference standard.
- Small sample below the recommended size; wide confidence intervals.
- One question (guilt) dominates, with a clinically implausible direction.
- Unknown data provenance and unverified licence; no external validation.
