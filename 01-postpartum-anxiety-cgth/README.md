# Interpretable Postpartum Anxiety Symptom Screening Using Confidence-Gated Hybrid Machine Learning

> **Working title.** The project began as *"Early Screening and Risk Stratification of Postpartum Depression and Anxiety Using Explainable Ensemble Machine Learning: A Comparative Benchmark"*. After auditing the data, the scope was narrowed to what the dataset supports (see [Scope and claims](#scope-and-claims)).

**Status:** exploratory thesis project, in progress · **Author:** _your name, supervisor, institution_ · **Last updated:** 2026-11-01

---

## Abstract

Simple models are easy to explain but often less accurate. Complex models are more accurate but harder to explain. This project proposes a small hybrid, the **Confidence-Gated Transparent Hybrid (CGTH)**. A logistic regression makes every decision it is confident about, and only uncertain cases (predicted probability close to 0.5) are passed to a random forest. The task is to predict a self-reported *Feeling anxious* item from eight other survey items in a public Kaggle dataset of postpartum responses.

On 326 distinct responses, evaluated with 5-fold cross-validation repeated 10 times, CGTH reached a **balanced accuracy of 0.757 (95% CI 0.700–0.813)**. That is statistically non-inferior to the random forest (0.761), while **68% of decisions were made by the transparent logistic regression**. CGTH was not significantly better than logistic regression alone (0.730, p = 0.08). When δ was chosen inside each training fold, the stricter version reached 0.750 (0.687–0.813) with 77% of decisions made by logistic regression, but non-inferiority to the random forest was not established (p = 0.06). The dataset has serious limitations (78% duplicate rows, a single-item label, heavy reliance on one question), so the results are methodological and exploratory. This is not a clinical tool.

## Research questions and hypotheses

| | Question | Result |
|---|---|---|
| H1 | Is CGTH non-inferior to random forest (margin 0.03 balanced accuracy)? | Supported at fixed δ = 0.2 (−0.005, p < 0.001); **not established with δ chosen inside training folds** (−0.011, p = 0.06) |
| H2 | Is CGTH better than logistic regression? | Not supported (+0.026, p = 0.08; stricter version +0.020, p = 0.13) |
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

The original download contained three byte-identical copies of the same CSV; only one is kept, as `data/raw/postpartum_depression.csv`. The notebook only reads it and never changes it.

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

**Stricter version (Task 17):** with δ chosen inside each training fold, CGTH reaches balanced accuracy 0.750 [0.687, 0.813] with **77% of decisions made by LR**. The chosen δ was mostly 0.10–0.20, which supports δ = 0.2 as a reasonable default. However, the formal test (Task 19) no longer establishes non-inferiority to random forest at the 0.03 margin (difference −0.011, p = 0.06).

**Screening operating point (Task 18):** with the threshold chosen on training data to catch 90% of anxious answers:

| Model | Sensitivity | Specificity |
|---|---|---|
| Logistic regression | 0.902 | 0.496 |
| Random forest | 0.897 | 0.558 |
| CGTH (δ in fold) | 0.897 | 0.509 |

At 90% sensitivity, random forest gives the fewest false alarms; CGTH sits close to LR.

**Results by age band (Task 20, CGTH at δ = 0.2):**

| Age band | Unique rows | Balanced accuracy | Sensitivity | Specificity |
|---|---|---|---|---|
| 25–30 | 49 | 0.664 | 0.748 | 0.581 |
| 30–35 | 71 | 0.824 | 0.967 | 0.681 |
| 35–40 | 76 | 0.760 | 0.826 | 0.693 |
| 40–45 | 73 | 0.755 | 0.878 | 0.633 |
| 45–50 | 57 | 0.726 | 0.927 | 0.525 |

Performance is weakest for the youngest band. Each band is small, so treat these differences as descriptive.

**Training vs testing (Task 21):** CGTH balanced accuracy 0.792 vs 0.757 (gap 0.036), ROC-AUC 0.881 vs 0.809 (gap 0.071). The other models show similar gaps, so overfitting is mild.

Points to report honestly:
- The main δ = 0.2 was chosen after an exploratory check. With δ chosen inside each training fold (Tasks 17, 19), the difference from RF grows to −0.011 and non-inferiority is no longer significant (p = 0.06). Treat H1 as suggestive, not proven.
- Tested alternatives (Task 22: tuned RF, Extra Trees, SVM, gradient boosting, naive Bayes, k-NN, LR) reached 0.69–0.76 balanced accuracy; class balancing in an exploratory run reached at most 0.765. About 0.76 is the ceiling for this dataset without leakage.
- The ROC-AUC of CGTH is lower than RF's, because mixing two models' probabilities blurs the ranking. CGTH is a decision rule, so decision metrics are primary.
- Gating to a stronger model when uncertain is an existing idea in machine learning. The contribution here is applying a transparent-first version to postpartum survey screening and reporting coverage.

All tables and the figures are saved to `results/`.

### Notebook 02: hybrid models and explainable AI

`notebooks/02_hybrid_xai_study.ipynb` compares 10 models on the same 50 folds (seed 42). The two hybrid designs were chosen beforehand on separate development runs (seeds 7 and 2026).

| Model | Test balanced accuracy | Test ROC-AUC | Train balanced accuracy |
|---|---|---|---|
| **HE: Hybrid Ensemble (RF + ET + SVM soft voting)** | **77.2%** | 84.3% | 87.4% |
| Random Forest | 77.1% | 84.3% | 84.6% |
| SVM | 76.7% | 82.2% | 86.2% |
| Stacking (RF + ET + NB) | 76.6% | 84.3% | 85.9% |
| Extra Trees | 76.0% | 84.8% | 93.1% |
| **CG-HE: Gated Hybrid (LR gate → HE)** | 75.9% | 81.2% | 85.0% |
| Logistic Regression | 73.0% | 80.0% | 77.6% |

HE ranks first on balanced accuracy and ROC-AUC together, but no model differs significantly from another after Holm correction. CG-HE lets Logistic Regression make 68% of decisions.

**SHAP vs LIME (CG-HE, 66 hold-out respondents):** both rank *Feeling of guilt* first (about 40% of total importance) and agree on the top three questions; global rank agreement is Spearman 0.98, per-person agreement 0.87. SHAP (exact) was slightly more stable across reruns (0.92 vs 0.91); LIME was about 5 times faster per person (0.08 s vs 0.42 s). Results are saved to `results/hybrid_xai/`.

**Prior study on this dataset (Task 30):** Nayee et al. (ICSUMMIT 2026) report 96.99% accuracy on a 1,503-entry Kaggle dataset, very likely this one, with no duplicate removal mentioned. A Random Forest with RFE on the raw 1,503 rows reproduces 96.2% (20 splits, range 94.4–98.0%), because about 96% of test rows are exact copies of training rows. On the 326 unique rows, the same method gives 74.2%. The published figure is therefore very likely inflated by duplicate leakage.

**Sample size (Task 31):** Riley et al. (2020) criteria call for 429–1,512 rows for a stable 20-parameter model; this study has 326 unique rows. Results should be read as exploratory until confirmed on a larger dataset.

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
01-postpartum-anxiety-cgth/
├── README.md                          # this file
├── requirements.txt                   # pinned library versions
├── data/raw/postpartum_depression.csv # dataset (read-only)
├── notebooks/
│   ├── 01_cgth_hybrid_study.ipynb     # CGTH study, one task per cell
│   └── 02_hybrid_xai_study.ipynb      # ★ hybrid models, all-model comparison, SHAP vs LIME
├── results/                           # tables and figures written by the notebook
├── research_plan/                     # audit, literature, hypotheses, methodology,
│                                      # thesis outline (start at its README.md)
├── reports/                           # Updated Bengali PDF and build script
└── archive/                           # earlier experiments, kept unchanged
    ├── stage1_baseline.ipynb          # was 1-project
    ├── stage2_ensembles.ipynb         # was 2-project
    ├── benchmark_original.ipynb       # was main-projects
    └── extended_experiments.ipynb     # was c_project
```

`research_plan/09_cgth_hybrid_methodology.md` describes the proposed method in detail. The literature table in `research_plan/03_literature_review_and_gaps.md` marks entries with incomplete metadata (⚠); check those before citing.

## Reproducing the results

Tested with Python 3.11, NumPy 2.4.6, pandas 3.1.0, SciPy 1.17.1, scikit-learn 1.9.1 and matplotlib 3.11.2 (also saved to `results_cgth/library_versions.txt`).

```bash
cd 01-postpartum-anxiety-cgth
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cd notebooks && jupyter lab 01_cgth_hybrid_study.ipynb     # Run All
```

All random seeds are fixed (`SEED = 42`). Different library versions can change the numbers slightly.

## Building the Bengali project report

The complete A-to-Z report is `reports/CGTH_Project_Report_bn.pdf`. To regenerate it after changing the report content, run:

```bash
python reports/build_report.py
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-sandbox \
  --print-to-pdf=reports/CGTH_Project_Report_bn.pdf \
  --print-to-pdf-no-header "file://$(pwd)/reports/CGTH_Project_Report_bn.html"
rm reports/CGTH_Project_Report_bn.html
```

The renderer uses the installed Hind Siliguri Bengali font so conjuncts and Bengali shaping remain readable in the PDF.

## Roadmap

- [x] Data audit and leakage check
- [x] Proposed hybrid (CGTH) with hypothesis tests and robustness checks
- [x] Choose δ inside each training fold (Task 17)
- [x] Screening threshold at 90% sensitivity (Task 18)
- [x] Performance by age band (Task 20)
- [x] Training vs testing check and performance ceiling (Tasks 21–22)
- [ ] Resolve dataset provenance and licence
- [x] Verify citations marked ⚠ (5 of 7 resolved; Zhang 2021 page numbers and one author order remain)
- [x] Replicate the prior 97% result on this dataset (notebook 02, Task 30)
- [x] Sample-size justification (notebook 02, Task 31)
- [x] TRIPOD+AI checklist draft (`research_plan/10_tripod_ai_checklist.md`)
- [ ] Calibration curves for the two proposed hybrids
- [ ] Seek a second dataset with a validated label (e.g. EPDS) for external validation
- [ ] Ethics declaration for secondary data use

## Data, ethics and citation

The data contain sensitive self-reported mental-health items, including a suicide-related question. Never present its rates as clinical prevalence. The model is not for individual clinical use. The dataset licence is unverified, so check Kaggle's terms before redistributing the CSV.

```
Author (2026). Interpretable Postpartum Anxiety Symptom Screening Using Confidence-Gated Hybrid Machine Learning.
Unpublished thesis project. GitHub repository: research-projects.
```
