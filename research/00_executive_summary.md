# 00 · Executive Summary

## Verdict
The notebook is a solid **starting benchmark** (5 models, 8 metrics, confusion matrices), but as it stands it does **not yet support the title**, and several results would not survive examiner or reviewer scrutiny. All fixes are feasible with the data you have.

## Title vs. what the notebook actually does

| Title promises | Notebook delivers | Gap |
|---|---|---|
| "Postpartum **Depression** and Anxiety" | Only one target: the self-reported item *Feeling anxious* | No depression target at all |
| "**Early** screening" | Predicts one symptom from other concurrent symptoms (cross-sectional) | Not early / not prospective. "Symptom-based screening" is accurate |
| "**Risk stratification**" | Binary class output only | No risk tiers, thresholds, or calibration |
| "**Explainable**" | No SHAP/LIME/importance in `main-projects.ipynb` (SHAP exists only in `c_project.ipynb`) | Must be added and evaluated |
| "**Ensemble**" | Soft-voting model, which does **not beat** Random Forest (78.8% vs 80.3%) | Ensemble benefit unproven; needs honest analysis |
| "Comparative **benchmark**" | Single 80/20 split, n_test = 66, tuned on test | Not a reliable benchmark yet |

## Top 6 issues to fix (details in `02_data_audit.md`)
1. **1,503 → 326 rows after de-duplication (78% removed).** Timestamps are minute-level, many with 14/21/28/35 rows each. This pattern suggests replicated or augmented data. Provenance must be established and reported, and results shown on both raw and de-duplicated data.
2. **Label is one survey item, not a clinical outcome.** No EPDS / GAD-7 reference standard. Must be framed as *symptom screening*, with this as a stated limitation.
3. **`cat.codes` encoding is alphabetical, not clinical.** e.g. Suicide item: No=0, *Not interested to say*=1, Yes=2; sleeping: No=0, *Two or more days/week*=1, Yes=2. Ordinal order is arbitrary and distorts LR/SVM.
4. **Test set of 66** → 80.3% accuracy has roughly a ±10-point 95% CI. Differences between models (1–3 points = 1–2 patients) are statistically meaningless. Use repeated stratified CV and report CIs.
5. **Model selection on the test set** ("best model = RF" is chosen after viewing test results). Use nested CV.
6. **Suicide-attempt item (30% "Yes") used as an input feature** with implausible prevalence for a general cohort; treat as a data-quality red flag and as a candidate *secondary safety outcome*, not a routine predictor.

## Recommended direction
- **Primary task:** binary postpartum-anxiety-symptom screening (keep).
- **Add:** calibrated three-tier risk stratification (low/medium/high) with cost-sensitive thresholds.
- **Add:** explainability that is *evaluated*, not just plotted (SHAP stability across folds, agreement across models).
- **Add:** a **minimal-item screener** (smallest question subset retaining performance), which is the most practically useful and publishable contribution of this dataset.
- **Add:** hybrid-method ablation (voting vs stacking vs feature-selection hybrids) with paired statistical tests; report a *null result honestly* if ensembles don't help.
- **Retitle** (see `01`). Suggested: *Explainable Ensemble Machine Learning for Symptom-Based Screening and Risk Stratification of Postpartum Anxiety: A Leakage-Controlled Comparative Benchmark*.

## What you can honestly claim as "better than existing work"
Not higher accuracy: different datasets are not comparable. Claim **methodological rigor and transparency** (leakage control, nested CV, CIs, calibration, explanation stability, data-provenance audit), which the literature review in `03` shows is often missing. See `06`.
