# Literature review and research gaps

How to read this file: every study below was located by web search (November 2026). The publishers' full-text pages could not be opened automatically, so numbers come from abstracts and search summaries. **Open each paper and confirm the numbers before you cite them.** Items marked ⚠ have details that could not be confirmed.

## 1. Studies on the same dataset (Kaggle *PostPartum Depression*, 1,503 rows)

| # | Study | Method | Reported result | XAI | What is missing |
|---|---|---|---|---|---|
| A | Lilhore U, Dalal S, Faujdar N, Simaiya S, Dahiya M, Tomar S, Hashmi A. "Unveiling the prevalence and risk factors of early stage postpartum depression: a hybrid deep learning approach." *Multimedia Tools and Applications* 83, 68281–68315 (2024). doi 10.1007/s11042-024-18182-3 | Hybrid transfer learning + BiLSTM + CNN; compared with DT, RF, AdaBoost, LightGBM, XGBoost, CatBoost | Accuracy 99.6%, precision 99.7% | Not reported in the abstract ⚠ | No explanation of predictions; no uncertainty; repeated answer patterns not discussed in the abstract |
| B | Raza A et al. ⚠ (full author list not confirmed). "Novel Meta Learning Approach for Detecting Postpartum Depression Disorder Using Questionnaire Data." *IEEE Access* 12, 101247–101259 (2024) | MDKR: decision tree + KNN + random forest feeding an MLP meta-learner; 11 algorithms compared; k-fold validation, hyper-parameter tuning | Accuracy 99% | Not reported in the abstract ⚠ | Same as above. Some sources say this paper used the suicide-attempt item as target ⚠ |
| C | Nayee N, Shah S, Bhaidasna H. "Machine Learning-Based Diagnosis of Postpartum Depression Methods and Insights." *ICSUMMIT 2026*, Atlantis Press, pp. 254–265. doi 10.2991/978-94-6239-727-9_19 | SVM, XGBoost, RF, DT, RBFNN/KNN with recursive feature elimination | Accuracy 96.99% | No | No XAI, no statistical tests, no duplicate analysis |
| D | Shivaprasad S, Chadaga K, Sampathila N, Prabhu S, Chadaga PR, Swathi KS. "Explainable machine learning methods to predict postpartum depression risk." *Systems Science & Control Engineering* 12(1) (2024). doi 10.1080/21642583.2024.2427033 | Heterogeneous classifiers; cites a Kaggle PostPartum Depression dataset ⚠ (size not confirmed) | Not confirmed ⚠ | SHAP, LIME, ELI5, Anchor | XAI methods are shown side by side but (to be confirmed in the full text) not compared quantitatively |

**Benchmark to beat on this dataset: 96.99% – 99.6% accuracy** under a random train/test split of all 1,503 rows.

## 2. Wider postpartum-depression ML literature

| Study | Data | Result | Note |
|---|---|---|---|
| Zhang W et al., *JMIR Med Inform* 2020;8(4):e15516 | 508 women, China | AUC 0.78 | Small cohort |
| Shin D et al., *J Clin Med* 2020;9(9):2899 | PRAMS, 28,755 records | — | PHQ-2 label |
| Amit G et al., *BMC Pregnancy Childbirth* 2021;21:630 | 266,544 UK records | AUC 0.72–0.74 (0.84 with EPDS) | EHR outcome |
| Saqib K et al., *JMIR Ment Health* 2021;8(11):e29838 | Scoping review, 14 studies | AUC 0.78–0.93 | SVM and RF most common |
| Nakamura Y et al., *Psychiatry Clin Neurosci* 2024, doi 10.1111/pcn.13659 | Japanese cohort | AUC 0.83 | Single site |
| Huang et al., *Front Med* 2025, doi 10.3389/fmed.2025.1565374 | 1,065 women | AUC 0.955 (10-fold CV) | 8 algorithms + SHAP; internal validation only |
| Alkhateeb et al., *J Med Internet Res* 2026;28:e77376 | Scoping review, 65 studies | — | Classical ML dominant; inconsistent validation |
| Xia et al., *Front Public Health* 2025, doi 10.3389/fpubh.2025.1631705 | Systematic review | — | High risk of bias, limited generalisability |

## 3. Method references

| Topic | Reference |
|---|---|
| SHAP | Lundberg & Lee, NeurIPS 2017 |
| LIME | Ribeiro, Singh & Guestrin, KDD 2016 |
| Disagreement between XAI methods | Krishna et al., "The Disagreement Problem in Explainable Machine Learning", TMLR 2024 |
| SHAP vs LIME in health data | Shah et al., HEALTHINF 2025 (SHAP more faithful and stable on breast-cancer data) ⚠ confirm details |
| Stacking | Wolpert, "Stacked generalization", *Neural Networks* 1992 |
| XGBoost / LightGBM / CatBoost | Chen & Guestrin 2016; Ke et al. 2017; Prokhorenkova et al. 2018 |
| Optuna | Akiba et al., KDD 2019 |
| Conformal prediction | Vovk, Gammerman & Shafer 2005; Angelopoulos & Bates 2023 |
| Counterfactual explanations | Wachter, Mittelstadt & Russell 2017 |
| Comparing many classifiers | Demšar, *JMLR* 2006 (Friedman + post-hoc tests) |
| Data leakage | Kapoor & Narayanan, *Patterns* 2023 |
| Reporting guideline | Collins et al., TRIPOD+AI, *BMJ* 2024;385:e078378 |
| Trustworthy AI in health | Lekadir et al., FUTURE-AI guideline, *BMJ* 2025 ⚠ confirm details |

## 4. Research gaps and how this project fills them

| Gap | Evidence | What this project does | Where |
|---|---|---|---|
| G1. High accuracy but black-box models | Studies A, B, C give no per-person explanation | Explains every prediction of the hybrid with SHAP and LIME | Notebook Part G |
| G2. XAI methods are shown, not compared | Study D shows several XAI outputs | Measures SHAP vs LIME on agreement, faithfulness, stability and speed | Tasks 44–48 |
| G3. No uncertainty: every prediction is given with full confidence | None of A–D reports it | Conformal prediction sets with a coverage guarantee, plus calibration | Tasks 33, 50–51 |
| G4. No actionable explanation | None of A–D | Counterfactual "what would have to change" example | Task 52 |
| G5. Model superiority is claimed without statistical tests | A, B, C report single numbers | Friedman, Wilcoxon–Holm, McNemar, bootstrap confidence interval | Tasks 34–35 |
| G6. Repeated answer patterns in the dataset are not analysed | None of A–D mention them in their abstracts | Reports standard results **and** duplicate-aware grouped validation | Part I |
| G7. No subgroup check | None of A–D | Accuracy per age group | Task 53 |
