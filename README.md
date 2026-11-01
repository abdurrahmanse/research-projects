# Symptom-Based Screening for Postpartum Anxiety: A Leakage-Aware Comparison of Machine-Learning Models

> **Working title.** The project began as *"Early Screening and Risk Stratification of Postpartum Depression and Anxiety Using Explainable Ensemble Machine Learning: A Comparative Benchmark"*. After auditing the data, the scope was narrowed to what the dataset supports (see [Scope and claims](#scope-and-claims)).

**Status:** exploratory thesis project, in progress · **Author:** _your name, supervisor, institution_ · **Last updated:** 2026-11-01

---

## Abstract

Postpartum mood and anxiety symptoms are common and often missed, and many published machine-learning studies report high accuracy without checking for data leakage, calibration or stability of explanations. This project benchmarks nine models (from a dummy baseline and logistic regression to random forests, boosting, and voting and stacking ensembles) on a public Kaggle survey of 1,503 postpartum responses. The task is to predict a self-reported *Feeling anxious* item from eight other symptom items and age band. The evaluation is designed to avoid leakage: identical answer patterns are never split between training and test data, models are compared with repeated cross-validation, and a locked test set is used once.

On 326 distinct responses, the selected random forest reached a **test ROC-AUC of 0.768 (95% CI 0.65–0.87)** against 0.50 for a no-skill baseline, with clear overfitting (training AUC 0.997). Ensembles did not outperform the best single model. About 78% of the raw rows repeat an earlier answer pattern, and evaluating on the raw rows with an ordinary split inflated AUC by roughly 0.04–0.08 (0.999 for an unrestricted forest). The results are methodological and exploratory; they are not a clinical tool.

## Research questions

1. How well can symptom items screen for the self-reported anxious-feeling item, compared with a no-skill baseline?
2. Do ensemble (voting, stacking) models improve on the best single model?
3. How much do repeated answer patterns inflate reported performance?
4. Can calibrated probabilities support exploratory low / medium / high tiers?
5. Which questions does the model rely on?

## Dataset

| | |
|---|---|
| Source | Kaggle, *PostPartum Depression* (uploader `parvezalmuqtadir2348`) |
| Size | 1,503 rows, 11 columns (timestamp, age band, 8 symptom items incl. the target, 1 suicide-related item) |
| Target | `Feeling anxious` (Yes = 65.2% raw, 58.0% after removing repeats) |
| Provenance | **Undocumented.** A third-party listing describes a hospital questionnaire collected via Google Forms; licence, ethics approval and eligibility are unverified |
| Quality findings | 27 missing cells (<2%); 90 distinct timestamps; only 326 distinct answer patterns, so 78% of rows repeat an earlier one |

The three CSV files in `projects/` are byte-identical copies of the same dataset.

## Method in brief

| Step | What is done |
|---|---|
| Data | Remove repeated rows (primary analysis); group rows by answer pattern |
| Split | 80/20 stratified, grouped by pattern; test set used once |
| Preprocessing | Most-frequent imputation and one-hot encoding inside the model pipeline (no leakage) |
| Models | Dummy, logistic regression, naive Bayes, decision tree, SVM, random forest, gradient boosting, soft-voting ensemble, stacking ensemble |
| Comparison | 5-fold × 3 repeated grouped cross-validation on training data; train vs validation AUC to detect overfitting |
| Selection | Exclude models with train–validation gap > 0.10, keep those within 1 SE of the best, take the simplest; tuning kept only if nested CV improves on untuned |
| Final test | Test AUC with 95% group-bootstrap CI, confusion matrix, dummy baseline |
| Statistics | Nadeau–Bengio corrected paired t-tests with Holm adjustment; ensemble error-correlation analysis |
| Extras | SHAP and fold-to-fold explanation stability; shortest useful questionnaire; label-noise robustness; age-group results; Platt calibration, exploratory risk tiers and decision curve; permutation importance; leakage check (ordinary vs grouped split) |

## Key results

Cross-validation on the training data (mean over 15 folds):

| Model | Train AUC | Validation AUC |
|---|---|---|
| Dummy | 0.500 | 0.500 |
| Logistic regression | 0.871 | 0.805 |
| Naive Bayes | 0.859 | 0.817 |
| Decision tree | 0.842 | 0.771 |
| SVM (RBF) | 0.978 | 0.840 |
| **Random forest (selected)** | 0.938 | 0.842 |
| Gradient boosting | 0.952 | 0.825 |
| Soft-voting ensemble | 0.929 | 0.830 |
| Stacking ensemble | 0.937 | 0.832 |

Held-out test set (66 responses, 38 anxious):

| Metric | Random forest | Dummy |
|---|---|---|
| ROC-AUC | **0.768** (95% CI 0.645–0.874) | 0.500 |
| Sensitivity / specificity at 0.5 | 0.76 / 0.68 | 1.00 / 0.00 |
| Training AUC | 0.997 | — |

Other findings:
- Ensembles did not beat the best single model; no model differs clearly from logistic regression after Holm adjustment.
- *Feeling of guilt* carries most of the predictive signal. Explanation rankings are only moderately stable across folds (median Kendall τ 0.67).
- Seven of the nine questions are enough to stay within one standard error of the full set.
- The forest is more robust than logistic regression up to 20% label noise; discrimination is weakest for ages 25–30.
- The leakage check shows ordinary splits overstating AUC.

Full tables and plots are in the notebook; result tables are saved to `projects/results/`. With only 66 test cases, model rankings from this single split are not reliable.

## Scope and claims

| The project does | The project does **not** |
|---|---|
| Classify a self-reported anxious-feeling item from other self-reported symptoms | Diagnose postpartum anxiety or depression (no validated EPDS / GAD-7 label) |
| Benchmark models under leakage-aware validation | Predict *early* or future onset (all items are concurrent, no timing data) |
| Produce exploratory model-based tiers | Provide clinically validated risk categories |
| Report attributions as model reliance | Make causal claims |

Other limits: unknown data origin, small test set, no external validation, repeated rows may reflect copied data.

## Repository structure

```
research-projects/
├── README.md                       # this file
├── projects/
│   ├── main-projects-final.ipynb   # ★ complete, step-by-step analysis (run this)
│   ├── main-projects.ipynb         # original notebook (kept unchanged)
│   ├── c_project.ipynb             # earlier extended experiment (kept unchanged)
│   └── post natal data.csv         # dataset (two identical copies also present)
└── research_blueprint/             # research plan: audit, literature matrix,
                                    # hypotheses, methodology, evaluation, XAI,
                                    # ethics, thesis outline (start at its README.md)
```

`research_blueprint/` contains the research planning documents: a verified literature matrix (20 sources with verification status), gap analysis, hypotheses with statistical tests, ablation design, thesis chapter outline and a reviewer-objection checklist. Items marked unverified there must be checked before citing.

## Reproducing the results

Tested with Python 3.11 and pandas 3.1.0, NumPy 2.4.6, scikit-learn 1.9.1, SciPy 1.17.1, matplotlib 3.11.2, seaborn 0.13.2.

```bash
cd projects
python -m venv .venv && source .venv/bin/activate
pip install pandas numpy scikit-learn scipy matplotlib seaborn shap jupyter
jupyter lab main-projects-final.ipynb     # Run All (about 5 minutes)
```

All random seeds are fixed (`SEED = 42`). Different library versions can change numbers slightly.

## Roadmap

- [ ] Resolve dataset provenance and licence (contact the uploader or source hospital)
- [ ] Systematic literature search (PRISMA) and verification of every citation
- [x] SHAP, explanation stability, shortest questionnaire, label noise, age groups, decision curve
- [ ] Add XGBoost / CatBoost comparison (not installed in this environment)
- [ ] Weighted voting and a locked second hold-out
- [ ] Seek a second dataset for external validation
- [ ] Ethics declaration for secondary data use

## Data, ethics and citation

The data contain sensitive self-reported mental-health items, including a suicide-related question whose prevalence is implausibly high; treat it with care and never present it as a clinical prevalence. The model is not for individual clinical use. The dataset licence is unverified, so check Kaggle's terms before redistributing the CSV.

```
Author (2026). Symptom-Based Screening for Postpartum Anxiety: A Leakage-Aware Comparison
of Machine-Learning Models. Unpublished thesis project. GitHub repository: research-projects.
```
