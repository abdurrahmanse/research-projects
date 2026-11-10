# Interpretable Postpartum Anxiety Symptom Screening Using a Hybrid Ensemble and Explainable AI

**Status:** thesis project, analysis complete · **Author:** _your name, supervisor, institution_ · **Last updated:** 2026-11-10

> The project began as *"Early Screening and Risk Stratification of Postpartum Depression and Anxiety Using Explainable Ensemble Machine Learning"*. A data audit narrowed it to what the dataset supports (see [Scope and claims](#scope-and-claims)). An earlier confidence-gated design (CGTH) is kept in git history and summarised in `research_plan/`.

---

## Abstract

Machine-learning studies of postpartum mental health often report very high accuracy on small public survey datasets, without checking for data leakage or explaining their models. This project predicts a self-reported *Feeling anxious* item from eight other survey items and age band in a public Kaggle dataset (1,503 rows, of which only 326 are unique). Five algorithms are compared under leakage-free 5-fold cross-validation repeated 10 times: logistic regression, random forest, extra trees, SVM, and a proposed **Hybrid Ensemble** (soft voting of random forest, extra trees and SVM). The Hybrid Ensemble ranked first overall, with **balanced accuracy 77.2% (95% CI 72.1–82.3%) and ROC-AUC 0.843**, although its lead over random forest was not statistically significant. Its predictions were explained with SHAP and LIME: both identified *Feeling of guilt* as the dominant question and agreed closely on the global ranking (Spearman 0.98). A leakage check explains the 96.99% accuracy previously reported on a 1,503-row Kaggle dataset, very likely this one: with duplicate rows kept, random forest reaches 98.8%, but only 76.0% on unique rows. The results are exploratory screening support, not a diagnostic tool.

## Research questions

| | Question | Answer |
|---|---|---|
| RQ1 | Which of five algorithms predicts the self-reported anxiety item best without leakage? | The Hybrid Ensemble ranks first (balanced accuracy 77.2%, ROC-AUC 0.843), but differences from random forest, SVM and extra trees are not significant |
| RQ2 | Is any model overfitting? | All tree-based models show a train–test gap; extra trees is largest (17.1 points), the Hybrid Ensemble 10.2, logistic regression 4.5 |
| RQ3 | Which questions drive the predictions, and do SHAP and LIME agree? | Guilt (about 42–48% of importance), then appetite and irritability; SHAP and LIME agree globally (Spearman 0.98) and on the top question for 85% of respondents |
| RQ4 | How much do duplicate rows inflate published results on this dataset? | Accuracy rises from 76.0% to 98.8% when duplicates are kept, because about 94% of test rows are copies of training rows |

## Dataset

| | |
|---|---|
| Source | Kaggle, *PostPartum Depression* (uploader `parvezalmuqtadir2348`), file `data/raw/postpartum_depression.csv` |
| Size | 1,503 rows, 11 columns (timestamp, age band, 9 survey items including the target) |
| Target | `Feeling anxious` (Yes = 58.0% of unique rows) |
| Provenance and licence | **Unverified** (see `data/DATA_CARD.md`) |
| Quality | 1,177 exact duplicate rows (78%); 326 unique answer patterns; 90 distinct timestamps; 9 missing cells in unique rows |

## Method

| Step | What is done |
|---|---|
| Data | Remove exact duplicates before any split; target `Feeling anxious = Yes` |
| Preprocessing | Most-frequent imputation and one-hot encoding, learned inside each training fold |
| Algorithms (5) | Logistic regression, random forest, extra trees, SVM (calibrated), **Hybrid Ensemble** (soft voting of RF, ET and SVM) |
| Hybrid design | Chosen on separate development runs (seeds 7 and 2026) before the final run (seed 42) |
| Validation | 5-fold stratified cross-validation repeated 10 times (50 folds); train and test scores |
| Metrics | Balanced accuracy (primary), accuracy, sensitivity, specificity, F1, MCC, ROC-AUC |
| Statistics | Nadeau–Bengio corrected 95% CIs and paired t-tests with Bonferroni correction |
| Figures | Class balance, model comparison, train vs test, ROC curves, confusion matrix, calibration, leakage, SHAP, LIME, SHAP vs LIME (11 simple figures) |
| Checks | Fairness by age band, Riley sample-size criterion, leakage check of a published 97% result |
| Explainable AI | Exact SHAP and LIME on a held-out 20%; importance comparison, agreement and speed |

## Results

### Model comparison (50 test folds)

| Model | Balanced accuracy | Accuracy | Sensitivity | Specificity | F1 | MCC | ROC-AUC | Train–test gap | Rank |
|---|---|---|---|---|---|---|---|---|---|
| **Hybrid Ensemble (proposed)** | **77.2%** | **78.5%** | 85.4% | 69.0% | 82.1% | **0.558** | 0.843 | 10.2 | **1** |
| Random forest | 77.1% | 78.5% | 86.1% | 68.1% | 82.3% | 0.558 | 0.843 | 7.5 | 2 |
| Extra trees | 76.0% | 77.0% | 82.5% | 69.5% | 80.6% | 0.529 | 0.848 | 17.1 | 3 |
| SVM | 76.7% | 78.1% | 85.3% | 68.0% | 81.8% | 0.549 | 0.822 | 9.6 | 4 |
| Logistic regression | 73.0% | 74.5% | 82.1% | 63.9% | 78.8% | 0.473 | 0.800 | 4.5 | 5 |

Rank is the pre-specified average of the balanced-accuracy and ROC-AUC ranks (Hybrid Ensemble 1.75, random forest 2.25). The Hybrid Ensemble is 4.2 points above logistic regression (p = 0.038, Bonferroni-corrected p = 0.15) and 0.1–1.2 points above the other models; none of these differences is significant after correction. The ROC figure uses one 5-fold run, so its AUC values (about 0.83) are slightly lower than the 50-fold means in this table.

### Explainable AI: SHAP vs LIME

| | SHAP | LIME |
|---|---|---|
| Top three questions | Guilt, appetite, irritability | Guilt, appetite, irritability |
| Share of importance for guilt | 42.4% | 47.6% |
| Global rank agreement | Spearman 0.983 | |
| Per-person rank agreement | mean Spearman 0.734 | |
| Same top question per respondent | 84.8% | |
| Time per respondent | 0.41 s | 0.08 s |

Both methods tell the same story. SHAP values add up exactly to each prediction; LIME is about five times faster.

### Validity checks

- **Leakage check:** Nayee et al. (ICSUMMIT 2026) report 96.99% accuracy on a 1,503-entry Kaggle dataset, very likely this one. Random forest reaches 98.8% with duplicates kept (about 94% of test rows copy a training row) and 76.0% on unique rows (20 random 80/20 splits).
- **Sample size:** the minimum Riley et al. (2020) criterion alone needs 374 rows; 326 are available, so results are exploratory.
- **Fairness:** the Hybrid Ensemble's balanced accuracy ranges from 65.6% (age 25–30) to 83.7% (age 30–35); bands have 49–76 respondents.
- **Calibration:** the Hybrid Ensemble's probabilities follow the observed rates closely (Brier score 0.163).

All tables and the 11 figures are saved in `results/final/`.

## Scope and claims

| The project does | The project does **not** |
|---|---|
| Predict a self-reported anxious-feeling item from other self-reported items | Diagnose postpartum anxiety or depression (no validated EPDS / GAD-7 label) |
| Compare five algorithms under leakage-free validation | Predict *early* or future onset (all items are concurrent) |
| Explain predictions with SHAP and LIME | Make causal claims about the questions |
| Show how duplicate rows inflate published accuracy | Provide clinically validated risk categories |

Other limits: unknown data origin, small sample, a single dominant question, no external validation.

## Repository structure

```
01-postpartum-anxiety-cgth/
├── README.md                          # this file
├── requirements.txt                   # pinned library versions
├── data/
│   ├── DATA_CARD.md                   # source, licence status, known issues
│   └── raw/postpartum_depression.csv  # dataset (read-only)
├── notebooks/
│   └── final_thesis_study.ipynb       # ★ the complete study, one task per cell (47 tasks)
├── results/final/                     # tables (CSV) and figures (PNG) written by the notebook
└── research_plan/                     # audit, literature, method, thesis outline, TRIPOD+AI checklist
```

## Reproducing the results

Tested with Python 3.11, NumPy 2.4.6, pandas 3.1.0, SciPy 1.17.1, scikit-learn 1.9.1, matplotlib 3.11.2, SHAP 0.51.0 and LIME 0.2.0.1.

```bash
cd 01-postpartum-anxiety-cgth
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cd notebooks && jupyter lab final_thesis_study.ipynb     # Run All (about 1 minute)
```

All random seeds are fixed (`SEED = 42`).

## Roadmap

- [x] Data audit and leakage check
- [x] Five-algorithm comparison with corrected statistics
- [x] SHAP vs LIME comparison
- [x] Calibration, fairness and sample-size checks
- [x] Leakage check of the prior 97% result on this dataset
- [ ] Verify the dataset licence on the Kaggle page
- [ ] External validation on a second dataset with a validated label (e.g. EPDS)
- [ ] Ethics declaration for secondary data use

## Data, ethics and citation

The data contain sensitive self-reported mental-health items, including a suicide-related question. The model is not for individual clinical use. Check the dataset licence before redistributing the CSV.

```
Author (2026). Interpretable Postpartum Anxiety Symptom Screening Using a Hybrid Ensemble
and Explainable AI. Unpublished thesis project. GitHub repository: research-projects.
```
