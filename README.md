# A Confidence-Gated Transparent Hybrid of Logistic Regression and Random Forest for Explainable Screening Support of Self-Reported Postpartum Anxiety Symptoms

> **Working title.** The project began as *"Early Screening and Risk Stratification of Postpartum Depression and Anxiety Using Explainable Ensemble Machine Learning: A Comparative Benchmark"*. After auditing the data, the scope was narrowed to what the dataset supports (see [Scope and claims](#scope-and-claims)).

**Status:** exploratory thesis project, in progress · **Author:** _your name, supervisor, institution_ · **Last updated:** 2026-11-01

---

## Abstract

Simple models are easy to explain but often less accurate. Complex models are more accurate but harder to explain. This project proposes a small hybrid, the **Confidence-Gated Transparent Hybrid (CGTH)**. A logistic regression makes every decision it is confident about, and only uncertain cases (predicted probability close to 0.5) are passed to a random forest. The task is to predict a self-reported *Feeling anxious* item from eight other survey items in a public Kaggle dataset of postpartum responses.

On 326 distinct responses, evaluated with 5-fold cross-validation repeated 10 times, CGTH reached a **balanced accuracy of 0.757 (95% CI 0.700–0.813)**. That is statistically non-inferior to the random forest (0.761), while **68% of decisions were made by the transparent logistic regression**. CGTH was not significantly better than logistic regression alone (0.730, p = 0.08). The dataset has serious limitations (78% duplicate rows, a single-item label, heavy reliance on one question), so the results are methodological and exploratory. This is not a clinical tool.

## Research questions and hypotheses

| | Question | Result |
|---|---|---|
| H1 | Is CGTH non-inferior to random forest (margin 0.03 balanced accuracy)? | **Supported** (difference −0.005, one-sided p < 0.001) |
| H2 | Is CGTH better than logistic regression? | Not supported (+0.026, p = 0.08) |
| RQ3 | Why does the gate work? | LR is 81% accurate on confident cases but 61% on uncertain ones; RF reaches 71% on the uncertain ones |
| RQ4 | How much do duplicate rows inflate results? | Balanced accuracy rises from about 0.76 to 0.84–0.86 when duplicates are kept |
| RQ5 | How much do models rely on one question? | Without *Feeling of guilt*, every model drops to about 0.60 |

## Dataset

| | |
|---|---|
| Source | Kaggle, *PostPartum Depression* (uploader `parvezalmuqtadir2348`) |
| Size | 1,503 rows, 11 columns (timestamp, age band, 9 survey items including the target) |
| Target | `Feeling anxious` (Yes = 58.0% of unique rows) |
| Provenance | **Undocumented.** A third-party listing describes a hospital questionnaire collected via Google Forms. Licence, ethics approval and eligibility are unverified |
| Quality findings | 27 missing cells; only 90 distinct timestamps; only 326 distinct answer patterns, so 78% of rows are duplicates; *guilt* is inversely related to anxiety, which is clinically implausible |

The three CSV files in `projects/` are byte-identical copies of the same dataset. The notebook only reads `post natal data.csv` and never changes it.

## Method in brief

| Step | What is done |
|---|---|
| Data | Remove exact duplicate rows; the target is `Feeling anxious = Yes` |
| Preprocessing | Most-frequent imputation and one-hot encoding, learned inside each training fold (no leakage) |
| Base models | Logistic regression (transparent); random forest (300 trees, depth 4) |
| Proposed hybrid | CGTH: use the LR probability when \|p − 0.5\| ≥ δ (δ = 0.2), otherwise use the RF probability |
| Comparators | LR alone, RF alone, soft voting (average of LR and RF) |
| Validation | 5-fold stratified cross-validation repeated 10 times (50 folds), fixed seed |
| Metrics | Balanced accuracy (primary), accuracy, sensitivity, specificity, F1, MCC, ROC-AUC, LR coverage |
| Statistics | Nadeau–Bengio corrected confidence intervals and paired t-tests (non-inferiority vs RF, superiority vs LR) |
| Explainability | LR odds ratios for the transparent decisions; transparency-vs-performance curve across δ |
| Robustness | Rerun with duplicates kept, and without the guilt item |

## Key results

| Model | Balanced accuracy (95% CI) | ROC-AUC | Decided by LR |
|---|---|---|---|
| Logistic regression | 0.730 [0.667, 0.794] | 0.800 | 100% |
| Random forest | 0.761 [0.706, 0.816] | 0.835 | 0% |
| Soft voting (LR + RF) | 0.741 [0.678, 0.804] | 0.820 | — |
| **CGTH (proposed)** | **0.757 [0.700, 0.813]** | 0.809 | **68%** |

Points to report honestly:
- δ = 0.2 was chosen after an exploratory check of a few values. The full δ curve (notebook Task 12) is reported so the choice is visible.
- The ROC-AUC of CGTH is lower than RF's, because mixing two models' probabilities blurs the ranking. CGTH is a decision rule, so decision metrics are primary.
- Gating to a stronger model when uncertain is an existing idea in machine learning. The contribution here is applying a transparent-first version to postpartum survey screening and reporting coverage.

All tables and the figure are saved to `projects/results_cgth/`.

## Scope and claims

| The project does | The project does **not** |
|---|---|
| Predict a self-reported anxious-feeling item from other self-reported items | Diagnose postpartum anxiety or depression (no validated EPDS / GAD-7 label) |
| Test a simple, explainable hybrid under leakage-free validation | Predict *early* or future onset (all items are concurrent; there is no timing data) |
| Report how many decisions a transparent model can make | Provide clinically validated risk categories |
| Report odds ratios as associations | Make causal claims |

Other limits: unknown data origin, small sample (326 unique rows), no external validation, and the duplicated rows may reflect copied data.

## Repository structure

```
research-projects/
├── README.md                       # this file
├── projects/
│   ├── cgth_hybrid_study.ipynb     # ★ main study, one task per cell (run this)
│   ├── results_cgth/               # tables and figure written by the notebook
│   ├── main-projects.ipynb         # original notebook (kept unchanged)
│   ├── c_project.ipynb             # earlier experiments (kept unchanged)
│   ├── 1-project.ipynb, 2-project.ipynb
│   └── post natal data.csv         # dataset (two identical copies also present)
└── research_blueprint/             # research plan: audit, literature, hypotheses,
                                    # methodology, thesis outline (start at its README.md)
```

`research_blueprint/09_cgth_hybrid_methodology.md` describes the proposed method in detail. The literature table in `03_literature_review_and_gaps.md` marks entries with incomplete metadata (⚠); check those before citing.

## Reproducing the results

Tested with Python 3.11, NumPy 2.4.6, pandas 3.1.0 and scikit-learn 1.9.1 (SciPy and matplotlib also required).

```bash
cd projects
python -m venv .venv && source .venv/bin/activate
pip install pandas numpy scikit-learn scipy matplotlib jupyter
jupyter lab cgth_hybrid_study.ipynb     # Run All
```

All random seeds are fixed (`SEED = 42`). Different library versions can change the numbers slightly.

## Roadmap

- [x] Data audit and leakage check
- [x] Proposed hybrid (CGTH) with hypothesis tests and robustness checks
- [ ] Choose δ inside each training fold (removes the exploratory-selection concern)
- [ ] Performance by age band (the only fairness check this data allows)
- [ ] Resolve dataset provenance and licence
- [ ] Verify every citation marked ⚠ in the literature table
- [ ] Seek a second dataset with a validated label (e.g. EPDS) for external validation
- [ ] Ethics declaration for secondary data use

## Data, ethics and citation

The data contain sensitive self-reported mental-health items, including a suicide-related question. Never present its rates as clinical prevalence. The model is not for individual clinical use. The dataset licence is unverified, so check Kaggle's terms before redistributing the CSV.

```
Author (2026). A Confidence-Gated Transparent Hybrid of Logistic Regression and Random Forest
for Explainable Screening Support of Self-Reported Postpartum Anxiety Symptoms.
Unpublished thesis project. GitHub repository: research-projects.
```
