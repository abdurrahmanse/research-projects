# 03 — Literature Review and Research Gaps

Every entry below was located by web search during this session. "Verified" = title, venue, year and DOI/PMC seen in search results. Items marked ⚠ have incomplete metadata — open them before citing. Metrics are reported **only** where the search result stated them.

## 1. Comparison table

| # | Study | Data | Outcome / label | Methods | Reported result | Key limitation (for gap analysis) |
|---|---|---|---|---|---|---|
| 1 | Zhang et al., *JMIR Med Inform* 2020;8(4):e15516 — "ML Models for the Prediction of PPD: Application and Comparison Based on a Cohort Study" ⚠ authors not confirmed | Cohort, 508 women (China) | PPD (pregnancy predictors) | SVM, RF + 2 feature-selection methods | Best AUC 0.78, sens 0.69 (accepted version) | Small n; preprint and final disagree on best model |
| 2 | Shin, Lee, Adeluwa, Hur, *J Clin Med* 2020;9(9):2899 | PRAMS 2012–13, 28,755 records (US) | Modified PHQ-2 | 9 ML algorithms, resampling | Not confirmed in search | PHQ-2 label; ~88 % majority class |
| 3 | Hochman et al., *Depress Anxiety* 2021;38(4):400–411 | 214,359 births, Israeli HMO EHR | New-onset PPD (1.9 %) | Gradient boosting | Not confirmed | EHR diagnosis ≠ symptoms; single country |
| 4 | Amit et al., *BMC Pregnancy Childbirth* 2021;21:630 | 266,544 UK primary-care EHR | PPD (dx/treatment, 13.4 %) | ML on EHR | AUC 0.72–0.74; EHR + EPDS 0.805→0.844 | Outcome = documented care, not screening |
| 5 | Zhang Y, Pathak J et al., *J Affect Disord* 2021 ⚠ volume/DOI not confirmed | EHR, US | PPD risk in pregnancy | ML framework | Not confirmed | EHR-based |
| 6 | Andersson, Bathula, Iliadis, Walter, Skalkidou, *Sci Rep* 2021;11:7877 | Swedish cohort | Depressive symptoms 6 wk postpartum | Multiple ML | Not confirmed | Questionnaire data; single cohort |
| 7 | Saqib, Khan, Butt, *JMIR Ment Health* 2021;8(11):e29838 | Scoping review, 14 studies | — | — | AUC 0.78–0.93; SVM, RF most common | Few studies; heterogeneous |
| 8 | Cellini et al., *J Affect Disord* 2022;309 (doi 10.1016/j.jad.2022.04.093) | Review, 11 studies | — | — | All AUC > 0.7; SVM most used | Variable selection inconsistent |
| 9 | Nakamura, Ueno, Takahashi, Ichikawa, Yamauchi, Ozaki, 2024, doi 10.1111/pcn.13659 ⚠ journal inferred | Japanese cohort, questionnaires pregnancy→5 mo | Depression 1 mo postpartum | ML | Not confirmed | Single site |
| 10 | Huang, Zhang, Zhang, Li, Li, *Front Med* 2025, doi 10.3389/fmed.2025.1565374 | Clinical cohort | PPD | 8 algorithms + explainability | Mean AUC 0.955 (10-fold CV) | Internal validation only |
| 11 | Xia et al., *Front Public Health* 2025, doi 10.3389/fpubh.2025.1631705 | Systematic review, 11 studies | — | PROBAST | — | Found limited generalisability and risk of bias |
| 12 | Alkhateeb et al., *J Med Internet Res* 2026;28:e77376 | Scoping review, 65 studies | — | — | Classical ML dominant; inconsistent validation; imputation reported in only 44.6 % | — |
| 13 | ⚠ SR & meta-analysis, "AI in the prevention and early detection of PPD", PMC12864048 (2026) | Meta-analysis | — | — | Not confirmed | Read before citing |
| 14 | ⚠ "Predictive Analysis of PPD Using ML", PMC12026879 | — | — | — | Not confirmed | Read before citing |
| 15 | Adhikari & Karki, *Islington J Multidiscip Res* 2026, doi 10.67556/hq2s5x30 | Bangladesh, n = 800 (Mendeley) | 3 EPDS risk tiers | LR, RF, XGB, soft voting; repeated CV, DeLong, McNemar, bootstrap CI, SHAP | Ensemble ≈ XGB (acc 76.5 % vs 77.4 %, AUC 0.91–0.92) | PHQ-9 feature dominates → screen-to-screen redundancy |
| 16 | ⚠ Raisa, Kaiser, Mahmud — Bangladesh, 150 women | 150 | PPD | RF best | AUC 98 %, acc 89 % | Very small n; optimistic |
| 17 | ⚠ ICSUMMIT 2026 (Atlantis Press), analysis of the 1,503-row Kaggle dataset | **Same dataset as this thesis** | — | — | Not confirmed | **Must read**: direct prior work on your data |
| 18 | Collins et al., TRIPOD+AI, *BMJ* 2024;385:e078378 | Guideline | — | — | 27-item checklist | Reporting standard to follow |
| 19 | Riley et al., *BMJ* 2020;368:m441 | Guideline | — | — | Sample-size criteria (`pmsampsize`) | Use for n-justification |

Methodology references to add (well established, but bibliographic details were **not** re-checked in this session): Lundberg & Lee 2017 (SHAP, NeurIPS); Ribeiro et al. 2016 (LIME, KDD); Nadeau & Bengio 2003 (corrected resampled t-test, *Machine Learning*); Varma & Simon 2006 (nested CV bias, *BMC Bioinformatics*); Demšar 2006 (multi-classifier comparison, *JMLR*); Vickers & Elkin 2006 (decision curve analysis, *Med Decis Making*); Grinsztajn et al. 2022 (tree models on tabular data, NeurIPS D&B).

## 2. Patterns in the literature

1. **Data:** large EHR cohorts (rows 2–5) or small single-site questionnaire samples (1, 9, 15, 16). Small studies report the highest AUCs (0.95–0.98), consistent with optimism from internal validation.
2. **Labels:** EPDS / PHQ / diagnosis codes. Few studies use a single self-reported item as an outcome; none of those verified here audit duplicate rows.
3. **Validation:** reviews (11, 12) flag inconsistent validation and bias. Repeated/nested CV with CIs and statistical tests is the exception (15 is the closest example).
4. **Ensembles:** where tested fairly (15), the ensemble did **not** beat the best single model.
5. **XAI:** SHAP used as one-shot output; stability of explanations across resamples is not reported in the studies seen.

## 3. Gap matrix

| Gap | Evidence | How this thesis addresses it | Testable in |
|---|---|---|---|
| G1 Data-quality auditing (duplicates, replication, label plausibility) is rarely reported for public PPD survey datasets | Rows 12, 17; doc 01 | Quantify duplicate-driven inflation and label anomalies | Notebook Tasks 4, 15 |
| G2 Small-n studies report point estimates from single splits | Rows 1, 10, 16 | 50-fold repeated CV, corrected confidence intervals and t-tests | Tasks 9–11 |
| G3 Hybrids blend models for every case, so no single decision stays simple to explain | Rows 10, 15 | **CGTH**: transparent model decides confident cases; stronger model only for uncertain ones | Tasks 7, 9 |
| G4 Explainability is shown as a plot, not measured | Rows 10, 15 | **Coverage**: share of decisions made by the transparent model; transparency–performance curve | Tasks 10, 12 |
| G5 Ensemble superiority is assumed, not tested | Row 15 | Pre-stated non-inferiority (vs RF) and superiority (vs LR) tests | Task 11 |
| G6 Single-feature dominance hidden in headline results | Row 15 (PHQ-9), doc 01 (guilt) | Rerun without the dominant item | Task 15 |
