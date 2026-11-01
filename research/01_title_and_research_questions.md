# 01 · Title, Aims, Research Questions, Hypotheses

## 1. Critique of the current title
> "Early Screening and Risk Stratification of Postpartum Depression and Anxiety Using Explainable Ensemble Machine Learning: A Comparative Benchmark"

| Phrase | Problem | Fix |
|---|---|---|
| Depression **and** Anxiety | Only anxiety is modeled | Either add a depression-proxy target (weak; see §3) or drop |
| Early | Data are cross-sectional and concurrent | "Symptom-based" |
| Risk stratification | Not implemented | Implement calibrated tiers, or drop |
| Explainable | Not in core notebook | Implement SHAP + stability analysis |
| Long (25+ words) | Hard to cite | Aim for ≤ 20 words |

## 2. Alternative titles (pick one after deciding scope)

| Option | Title | Use when |
|---|---|---|
| **A (recommended)** | *Explainable Ensemble Machine Learning for Symptom-Based Screening and Risk Stratification of Postpartum Anxiety: A Leakage-Controlled Comparative Benchmark* | You do anxiety only + tiers + SHAP (all feasible) |
| B | *Towards a Minimal, Explainable Screening Tool for Postpartum Anxiety: Benchmarking Ensemble Learners on Self-Reported Symptoms* | You emphasise the minimal-item screener |
| C | *Postpartum Anxiety and Depression-Related Symptoms: A Multi-Target Explainable Machine Learning Benchmark* | You add the depression-proxy and suicide-item targets as secondary tasks |
| D (keep original) | Original title | Only if you implement depression, early/prospective framing, and tiers. Not recommended |

A short subtitle such as "…on a Survey Cohort of 1,503 Responses" makes the scope honest.

## 3. Better research opportunities in this dataset
Ranked by value/feasibility.

1. **Minimal-item screener (high value).** Nine questions is already short, but you can show the smallest subset (e.g., 3–5 items) that keeps AUC within a margin of the full set. Directly addresses clinical workload.
2. **Calibrated risk tiers (high).** Convert probabilities into low/medium/high with thresholds chosen by decision-curve analysis and a stated cost ratio for missed cases vs. false alarms.
3. **Explanation reliability (high, novel in this niche).** Quantify whether SHAP rankings are stable across folds/seeds and agree across models (Spearman/Kendall, top-k Jaccard).
4. **Safety outcome (medium, sensitive).** "Suicide attempt" item as a secondary target with "Not interested to say" modeled as its own category (informative non-response). Needs strong ethics framing; the item's wording ("attempt") and 30.5% "Yes" rate are anomalous (see `02`).
5. **Data-quality robustness (medium, unusual).** Show how conclusions change between raw (n=1,503), de-duplicated (n=326) and sample-weighted analyses. Few papers expose this.
6. **Depression proxy (low-medium).** "Feeling sad or tearful" can serve as a *proxy* depressive-symptom target, but it is a single item, not a diagnosis. Only include as exploratory and state this clearly.
7. **Label-noise sensitivity (medium).** Flip x% of labels and measure each model's degradation: a justified use of multiple models.

## 4. Aim and objectives
**Aim.** To develop and rigorously benchmark explainable machine-learning models that screen for postpartum anxiety symptoms from self-reported symptom data and assign calibrated risk tiers.

**Objectives**
- O1 Audit and document data provenance and quality; define a reproducible preprocessing protocol.
- O2 Benchmark individual learners (LR, SVM, RF, GB, + optionally XGBoost/LightGBM/Naive Bayes/kNN) under nested stratified CV.
- O3 Construct and compare hybrid/ensemble strategies (soft voting, stacking, feature-selection hybrids).
- O4 Evaluate discrimination, calibration, and clinical utility, not accuracy alone.
- O5 Explain predictions globally and locally, and test explanation stability.
- O6 Derive a minimal-item screener and calibrated risk tiers.

## 5. Research questions and hypotheses

| RQ | Question | Hypothesis | Test |
|---|---|---|---|
| RQ1 | Which model family best discriminates anxiety status from symptoms? | Non-linear models (RF/GB/SVM-RBF) outperform LR in AUC | Repeated CV AUC, corrected resampled t-test / Wilcoxon + Holm |
| RQ2 | Do ensembles/hybrids improve over their best member? | Soft voting/stacking improve AUC and Brier score by a small, possibly non-significant margin (H0: no difference) | Paired tests over identical folds; report effect size + CI |
| RQ3 | Are probabilities trustworthy enough for tiers? | Tree ensembles are miscalibrated; Platt/isotonic calibration lowers ECE and Brier | Reliability curves, ECE, Brier before/after |
| RQ4 | Which symptoms drive predictions, and is that stable? | Guilt, sleep trouble, irritability and bonding are consistently top-ranked | SHAP + rank-stability metrics; compare with clinical literature |
| RQ5 | How few items suffice? | ≤5 items retain AUC within 0.02 of the full model | Backward elimination / SHAP-ranked forward selection with CIs |
| RQ6 | How sensitive are conclusions to data duplication/provenance? | Performance on raw data is inflated vs. de-duplicated | Compare raw vs. group-aware CV vs. de-duplicated |

State hypotheses **before** running experiments (pre-register in a dated file in the repo: cheap and credible).
