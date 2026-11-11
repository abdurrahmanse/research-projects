# Explainable Hybrid Stacking Ensemble for Postpartum Anxiety Screening

**Status:** analysis complete · **Last run:** 2026-11-11 · **Author:** _your name, supervisor, institution_

## Abstract

This project predicts a self-reported *Feeling anxious* answer (Yes / No) from eight other survey answers and age band in the public Kaggle *PostPartum Depression* dataset (1,503 responses). Seven models compete: logistic regression, random forest, XGBoost, LightGBM, CatBoost, an MLP neural network, and a proposed **Hybrid Stack** (CatBoost, XGBoost, random forest and MLP combined by a logistic-regression meta-learner). On a held-out 20% test set the Hybrid Stack reaches **98.67% accuracy (95% CI 97.34–99.67%), F1 98.97%, ROC-AUC 1.000**; six of the seven models exceed 97%, and their differences are not statistically significant. The Hybrid Stack is explained with SHAP and LIME, which are compared on agreement, faithfulness, stability and speed. Conformal prediction, a counterfactual example and an age-group fairness check are added. A duplicate-aware validation shows that accuracy on answer patterns the model has never seen is about 85%.

## Results

### Model competition

| Model | 10-fold CV accuracy | Test accuracy | F1 | ROC-AUC |
|---|---|---|---|---|
| CatBoost | 98.25% | 100.00% | 100.00% | 1.000 |
| Random Forest | 97.92% | 99.34% | 99.49% | 1.000 |
| **Hybrid Stack (proposed)** | **98.00%** | **98.67%** | **98.97%** | **1.000** |
| MLP Neural Net | 97.59% | 98.67% | 98.97% | 0.997 |
| LightGBM | 98.08% | 97.67% | 98.18% | 1.000 |
| XGBoost | 97.83% | 97.01% | 97.65% | 0.995 |
| Logistic Regression | 82.70% | 81.73% | 86.35% | 0.895 |

- The seven models differ overall (Friedman p < 0.001), but only because logistic regression is far behind.
- The Hybrid Stack is significantly better than logistic regression (Holm-corrected p = 0.012). It is **not** significantly different from CatBoost, random forest, LightGBM, XGBoost or MLP (all corrected p = 1.0; McNemar p ≥ 0.06).
- The Hybrid Stack has the second-best Brier score (0.006), i.e. well-calibrated probabilities.

### SHAP vs LIME (Hybrid Stack, 100 test people)

| | SHAP | LIME |
|---|---|---|
| Most important question | Feeling of guilt (37%) | Feeling of guilt (38%) |
| Faithfulness, top-1 question removed (random = 0.098) | 0.301 | 0.237 |
| Faithfulness, top-3 questions removed (random = 0.241) | 0.472 | 0.387 |
| Stability (Spearman between two runs) | 0.908 | 0.903 |
| Seconds per person | 0.14 | 0.03 |
| Contributions add up to the prediction | Yes | No |

Agreement between the two: global rank correlation 0.917; per-person rank correlation 0.534; same top question for 71% of people; same direction for 78% of contributions. They agree on the big picture and differ in individual explanations; SHAP is more faithful, LIME is about five times faster.

### Trustworthy-AI checks

| Check | Result |
|---|---|
| Conformal prediction, 95% target | 97.0% actual coverage; 97% of people get a single answer |
| Counterfactual example | One changed answer (irritability Yes → Sometimes) moves a 0.99 anxious prediction to 0.13 |
| Fairness by age group | 94.9% (25–30) to 100% |

### Comparison with published work on the same dataset

| Study | Accuracy | Tests / CI | XAI compared | Uncertainty |
|---|---|---|---|---|
| JISEM study (CatBoost) | 95.68% | – | – | – |
| Nayee et al. 2026 | 96.99% | – | – | – |
| Raza et al. 2024 (MDKR) | 99.0% | – | – | – |
| Lilhore et al. 2024 (BiLSTM + CNN) | 99.6% | – | – | – |
| **This study, Hybrid Stack** | **98.67%** | Yes | Yes | Yes |

Details, references and unconfirmed items are in [research/01_literature_review.md](research/01_literature_review.md).

## Important limitation: repeated answer patterns

Of the 1,503 responses, 1,177 repeat an earlier answer pattern (326 patterns are unique). In the random split, 93.4% of test people have an identical "twin" in the training set. The Hybrid Stack scores 100% on those and 80% on the 20 test people without a twin. With grouped cross-validation, where no pattern is shared between training and test, accuracy is **84.7%** for the Hybrid Stack (random forest 86.0%, CatBoost 85.2%).

The 98–100% figures are therefore accuracy under the same random-split protocol the earlier papers used. The ~85% figure is the estimate for a genuinely new answer pattern. Both are reported in the notebook (Part I).

Other limits: the label is one self-reported question, not a clinical diagnosis; the data source is undocumented; there is no external validation set.

## Method

| Step | What is done |
|---|---|
| Data | All 1,503 responses; timestamp dropped; missing answers kept as a "No answer" category |
| Split | Stratified 80% train / 20% test, seed 42 |
| Encoding | One-hot, inside each model pipeline |
| Tuning | Optuna, 25 trials, 3-fold CV on the training set (XGBoost, LightGBM) |
| Hybrid | Stacking: CatBoost + XGBoost + random forest + MLP → logistic regression, out-of-fold (cv = 5) |
| Validation | 10-fold stratified CV on the training set, then one final test |
| Statistics | Friedman, Wilcoxon with Holm correction, McNemar, bootstrap 95% CI |
| XAI | Exact SHAP and LIME; agreement, deletion-based faithfulness, stability, time |
| Trustworthy AI | Calibration, conformal prediction, counterfactual, fairness by age |
| Robustness | Grouped 5-fold CV by answer pattern |

## Structure

```
01-postpartum-anxiety-xai-hybrid/
├── README.md
├── requirements.txt
├── data/            raw CSV (read-only) and DATA_CARD.md
├── notebooks/       postpartum_anxiety_xai_study.ipynb  (57 small tasks, one per cell)
├── results/         21 figures (PNG) and 17 tables (CSV) written by the notebook
├── research/        literature review and research gaps
└── book/            the project book (PDF), its template and build script
```

## Reproduce

```bash
cd 01-postpartum-anxiety-xai-hybrid
python3.11 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cd notebooks && jupyter lab postpartum_anxiety_xai_study.ipynb     # Run All, about 3 minutes
```

## Ethics

The data contain self-reported mental-health answers, including a suicide-related question. The model is a research result, not a diagnostic tool.
