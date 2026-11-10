# 03 — Literature Review and Research Gaps

Every entry below was located by web search during this session. "Verified" = title, venue, year and DOI/PMC seen in search results. Items marked ⚠ have incomplete metadata — open them before citing. Metrics are reported **only** where the search result stated them.

## 1. Comparison table

| # | Study | Data | Outcome / label | Methods | Reported result | Key limitation (for gap analysis) |
|---|---|---|---|---|---|---|
| 1 | Zhang W, Liu H, Silenzio VMB, Qiu P, Gong W, *JMIR Med Inform* 2020;8(4):e15516, doi 10.2196/15516 — "ML Models for the Prediction of PPD: Application and Comparison Based on a Cohort Study" | Cohort, 508 women (China) | PPD (pregnancy predictors) | SVM, RF + 2 feature-selection methods | Best AUC 0.78, sens 0.69 (accepted version) | Small n; preprint and final disagree on best model |
| 2 | Shin, Lee, Adeluwa, Hur, *J Clin Med* 2020;9(9):2899 | PRAMS 2012–13, 28,755 records (US) | Modified PHQ-2 | 9 ML algorithms, resampling | Not confirmed in search | PHQ-2 label; ~88 % majority class |
| 3 | Hochman et al., *Depress Anxiety* 2021;38(4):400–411 | 214,359 births, Israeli HMO EHR | New-onset PPD (1.9 %) | Gradient boosting | Not confirmed | EHR diagnosis ≠ symptoms; single country |
| 4 | Amit et al., *BMC Pregnancy Childbirth* 2021;21:630 | 266,544 UK primary-care EHR | PPD (dx/treatment, 13.4 %) | ML on EHR | AUC 0.72–0.74; EHR + EPDS 0.805→0.844 | Outcome = documented care, not screening |
| 5 | Zhang Y, Pathak J et al., *J Affect Disord* 2021;279 (online Sept 2020; PMC7738412) ⚠ pages/DOI not confirmed | EHR, US | PPD risk in pregnancy | ML framework | Not confirmed | EHR-based |
| 6 | Andersson, Bathula, Iliadis, Walter, Skalkidou, *Sci Rep* 2021;11:7877 | Swedish cohort | Depressive symptoms 6 wk postpartum | Multiple ML | Not confirmed | Questionnaire data; single cohort |
| 7 | Saqib, Khan, Butt, *JMIR Ment Health* 2021;8(11):e29838 | Scoping review, 14 studies | — | — | AUC 0.78–0.93; SVM, RF most common | Few studies; heterogeneous |
| 8 | Cellini et al., *J Affect Disord* 2022;309 (doi 10.1016/j.jad.2022.04.093) | Review, 11 studies | — | — | All AUC > 0.7; SVM most used | Variable selection inconsistent |
| 9 | Nakamura, Ueno, Takahashi, Ichikawa, Yamauchi, Ozaki, *Psychiatry Clin Neurosci* 2024, doi 10.1111/pcn.13659 | Japanese cohort, questionnaires pregnancy→5 mo | Depression 1 mo postpartum | Balanced gradient boosting, 28 features | AUC 0.83, accuracy 78.6%, sens 71.1%, spec 80.6% (from a secondary summary; check full text) | Single site |
| 10 | Huang, Zhang, Zhang, Li, Li, *Front Med* 2025, doi 10.3389/fmed.2025.1565374 | Clinical cohort | PPD | 8 algorithms + explainability | Mean AUC 0.955 (10-fold CV) | Internal validation only |
| 11 | Xia et al., *Front Public Health* 2025, doi 10.3389/fpubh.2025.1631705 | Systematic review, 11 studies | — | PROBAST | — | Found limited generalisability and risk of bias |
| 12 | Alkhateeb et al., *J Med Internet Res* 2026;28:e77376 | Scoping review, 65 studies | — | — | Classical ML dominant; inconsistent validation; imputation reported in only 44.6 % | — |
| 13 | Ruger-Navarrete et al., *Front Psychiatry* 2026, doi 10.3389/fpsyt.2025.1734102 (PROSPERO CRD420251004175) ⚠ first-author order differs between sources | SR & meta-analysis, 16 studies (2020–2025) | PPD | Random-effects meta-analysis | Many models AUROC 0.80–0.90 (secondary summary) | Few studies compare AI directly with EPDS/PHQ |
| 14 | Kim H, *Healthcare* 2025;13(8):897, doi 10.3390/healthcare13080897 — "Predictive Analysis of PPD Using ML" | Korean early-childhood panel data, cross-sectional | Maternal PPD | ML classifiers | Not confirmed | Cross-sectional |
| 15 | Adhikari & Karki, *Islington J Multidiscip Res* 2026, doi 10.67556/hq2s5x30 | Bangladesh, n = 800 (Mendeley) | 3 EPDS risk tiers | LR, RF, XGB, soft voting; repeated CV, DeLong, McNemar, bootstrap CI, SHAP | Ensemble ≈ XGB (acc 76.5 % vs 77.4 %, AUC 0.91–0.92) | PHQ-9 feature dominates → screen-to-screen redundancy |
| 16 | Raisa JF, Kaiser MS, Mahmud M, *Brain Informatics (BI 2022)*, Springer LNCS, doi 10.1007/978-3-031-15037-1_20 | Bangladesh, 150 women | PPD (EPDS/PHQ-2 items) | RF best | AUC 98 %, acc 89 % | Very small n; optimistic |
| 17 | Nayee N, Shah S, Bhaidasna H, "Machine Learning-Based Diagnosis of Postpartum Depression Methods and Insights", *ICSUMMIT 2026*, Atlantis Press, pp. 254–265, doi 10.2991/978-94-6239-727-9_19 | **Kaggle dataset with 1,503 entries — very likely the same dataset** (not named on the page) | Not stated on the page | SVM, XGBoost, RF, DT, RBFNN/KNN, RFE feature selection | **Accuracy 96.99%** (XGBoost/RF + RFE) | **No duplicate removal mentioned.** Our replication (notebook 02, Task 30): RF + RFE on the raw 1,503 rows gives 95.8%, because 98.3% of test rows copy a training row; on unique rows it gives 74.4% |
| 18 | Collins et al., TRIPOD+AI, *BMJ* 2024;385:e078378 | Guideline | — | — | 27-item checklist | Reporting standard to follow |
| 19 | Riley et al., *BMJ* 2020;368:m441 | Guideline | — | — | Sample-size criteria (`pmsampsize`) | Use for n-justification |

Methodology references to add (well established, but bibliographic details were **not** re-checked in this session): Lundberg & Lee 2017 (SHAP, NeurIPS); Ribeiro et al. 2016 (LIME, KDD); Nadeau & Bengio 2003 (corrected resampled t-test, *Machine Learning*); Varma & Simon 2006 (nested CV bias, *BMC Bioinformatics*); Demšar 2006 (multi-classifier comparison, *JMLR*); Vickers & Elkin 2006 (decision curve analysis, *Med Decis Making*); Grinsztajn et al. 2022 (tree models on tabular data, NeurIPS D&B).

## 2. Patterns in the literature

1. **Data:** large EHR cohorts (rows 2–5) or small single-site questionnaire samples (1, 9, 15, 16). Small studies report the highest AUCs (0.95–0.98), consistent with optimism from internal validation. The only study found on this thesis's dataset (row 17) reports 97% accuracy, which our replication explains by duplicate leakage.
2. **Labels:** EPDS / PHQ / diagnosis codes. Few studies use a single self-reported item as an outcome; none of those verified here audit duplicate rows.
3. **Validation:** reviews (11, 12) flag inconsistent validation and bias. Repeated/nested CV with CIs and statistical tests is the exception (15 is the closest example).
4. **Ensembles:** where tested fairly (15), the ensemble did **not** beat the best single model.
5. **XAI:** SHAP used as one-shot output; stability of explanations across resamples is not reported in the studies seen.

## 3. Gap matrix

| Gap | Evidence | How this thesis addresses it | Testable in |
|---|---|---|---|
| G1 Data-quality auditing (duplicates, replication, label plausibility) is rarely reported for public PPD survey datasets | Rows 12, 17; doc 01 | Quantify duplicate-driven inflation and replicate the 97% claim on this dataset | Notebook 01 Tasks 4, 15; notebook 02 Task 30 |
| G2 Small-n studies report point estimates from single splits | Rows 1, 10, 16 | 50-fold repeated CV, corrected confidence intervals and t-tests | Tasks 9–11 |
| G3 Hybrids blend models for every case, so no single decision stays simple to explain | Rows 10, 15 | **CGTH**: transparent model decides confident cases; stronger model only for uncertain ones | Tasks 7, 9 |
| G4 Explainability is shown as a plot, not measured | Rows 10, 15 | **Coverage**: share of decisions made by the transparent model; transparency–performance curve | Tasks 10, 12 |
| G5 Ensemble superiority is assumed, not tested | Row 15 | Pre-stated non-inferiority (vs RF) and superiority (vs LR) tests | Task 11 |
| G6 Single-feature dominance hidden in headline results | Row 15 (PHQ-9), doc 01 (guilt) | Rerun without the dominant item | Task 15 |
| G7 Explanation methods are used, not compared | Rows 10, 15 | SHAP vs LIME on agreement, stability and speed | Notebook 02 Tasks 20–24 |
