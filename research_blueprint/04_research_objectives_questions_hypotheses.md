# 04 · Aim, Objectives, Research Questions and Hypotheses

## 1. Aim
To benchmark, under leakage-aware and uncertainty-quantified evaluation, whether linear, tree-ensemble and hybrid ensemble learners can screen for a self-reported anxious-feeling item from eight other self-reported postpartum symptoms and age band, and to determine whether calibrated, explainable, tiered outputs can be derived that are stable enough to be worth validating in future clinical studies.

## 2. Objectives (measurable)
| ID | Objective | Output |
|---|---|---|
| O1 | Document provenance and quality of the dataset; quantify duplication and label conflict | Data card; pattern table |
| O2 | Estimate the inflation caused by duplicate-driven leakage across three evaluation arms (naive / group-aware / de-duplicated) | Paired inflation estimates with CIs |
| O3 | Benchmark ≥8 individual learners with equal tuning budgets under nested repeated CV | Table 1 with CIs |
| O4 | Construct soft-voting, weighted-voting and stacking ensembles using out-of-fold predictions; test whether any beats the best single learner | Paired tests, effect sizes |
| O5 | Assess probability calibration; apply and compare calibration methods | Brier, ICI, slope, reliability plots |
| O6 | Define pre-specified risk tiers and evaluate with decision-curve analysis | Tier table, DCA |
| O7 | Evaluate explanations: global, local, cross-model agreement and stability | Stability metrics |
| O8 | Derive a minimal item subset retaining performance within a pre-specified margin | Item-reduction curve |

## 3. Research questions
| RQ | Question |
|---|---|
| RQ1 (performance) | Which model families discriminate the anxiety-symptom label best, relative to dummy, tuned LR and pattern-lookup baselines? |
| RQ2 (model selection) | Does tuning effort or encoding choice change the ranking of models? |
| RQ3 (ensembles) | Does any voting/stacking ensemble improve discrimination, calibration or net benefit over the strongest single learner, and at what complexity cost? |
| RQ4 (risk tiers) | Can calibrated probabilities be mapped to low/medium/high tiers with acceptable and stable sensitivity/PPV? |
| RQ5 (interpretability) | Which items drive predictions, and how stable are attributions across folds, seeds and models? |
| RQ6 (robustness/leakage) | How much do reported metrics change when duplicated answer patterns are or are not controlled? |
| RQ7 (parsimony) | How many questionnaire items are needed to remain within Δ of the full model? |
| RQ8 (generalisability) | How sensitive are conclusions to class-balance handling and label-noise perturbation? (Population generalisability cannot be tested; see `11`.) |

## 4. Hypotheses (specified before running experiments)

Notation: AUC = ROC-AUC; Δ = difference; CV = repeated stratified group k-fold; α = 0.05 with Holm correction over the family of comparisons within each hypothesis.

| H | Statement | Variables / comparison | Outcome | Test | Support criterion | Rejection criterion |
|---|---|---|---|---|---|---|
| **H1** | Non-linear learners (RF/ExtraTrees/boosting/CatBoost) discriminate better than tuned LR | Best non-linear vs tuned LR (same folds) | ΔAUC (primary), ΔBrier | Nadeau–Bengio corrected resampled t-test over repeated CV folds; supplement with paired bootstrap CI | 95% CI of ΔAUC excludes 0 *and* ΔAUC ≥ 0.02 | CI includes 0 or ΔAUC < 0.02 → "no evidence of benefit" |
| **H2** | A heterogeneous ensemble (voting or stacking) improves over the strongest single learner | Ensemble vs best base learner, selected *within* the inner loop | ΔAUC, ΔBrier, ΔPR-AUC | Same as H1; Holm over {soft vote, weighted vote, stack} | CI excludes 0 and ΔAUC ≥ 0.01 and complexity cost reported | Otherwise report null. Pre-register that a null result is an acceptable finding |
| **H3** | Calibration improves probability reliability without losing discrimination | Uncalibrated vs Platt vs isotonic (inside CV) | Brier, ICI, calibration slope; ΔAUC | Paired differences over folds | Brier decreases (CI excludes 0) and |ΔAUC| ≤ 0.01 | No Brier gain or AUC drop > 0.01 |
| **H4** | Class-weighting/threshold tuning matches SMOTE-NC for minority detection | None vs class-weight vs SMOTE-NC (inside folds) | Sensitivity at fixed specificity 0.70; PR-AUC; MCC | Paired differences | SMOTE-NC gain < 0.02 in sens@spec → resampling unnecessary | SMOTE-NC gain ≥ 0.02 with CI excluding 0 |
| **H5** | Duplicate-driven leakage inflates performance | Naive random split on raw data vs group-aware CV | ΔAUC, Δaccuracy per model | Paired difference over repeats; bootstrap CI | Naive > group-aware by ≥ 0.03 AUC | < 0.03 → leakage negligible here |
| **H6** | Top-ranked predictors are stable | SHAP/permutation rankings across 5×10 folds, 3 model families | Kendall τ between fold rankings; top-3 Jaccard | Distribution of pairwise τ; bootstrap | Median τ ≥ 0.7 and top-3 Jaccard ≥ 0.6 | Below thresholds → rankings reported as unstable |
| **H7** | A reduced item set (≤5 items) is non-inferior to all items | Reduced vs full model | ΔAUC with non-inferiority margin 0.03 | Non-inferiority on paired CV differences (one-sided 95% CI lower bound > −0.03) | Lower bound > −0.03 | Otherwise full set required |
| **H8** | Tiered risk output has stable monotone observed risk | Predicted tier vs observed event rate in held-out folds | Observed rate per tier; Cochran–Armitage trend | Trend test + CIs | Monotone increase with CIs separated between low and high | Overlap → tiers not defensible |

**Why these thresholds?** 0.02/0.03 margins are *pre-specified conventions for "worth reporting"*, not clinical standards; justify them in the thesis or replace with supervisor-approved ones **before** analysis. Commit the hypotheses file to git with a date.

## 5. Primary and secondary outcomes
- **Primary:** ROC-AUC of the nested-CV outer folds (group-aware, de-duplicated arm).
- **Secondary:** Brier score, calibration slope/ICI, PR-AUC, MCC, balanced accuracy, sensitivity at fixed specificity 0.70 and 0.80, net benefit at thresholds 0.3–0.7.
- **Multiplicity:** primary comparison families are H1–H3; others exploratory, labelled as such.

## 6. Decision on contingencies
| Situation | Action |
|---|---|
| Ensembles give no gain (likely) | Report as finding; analyse diversity to explain why |
| Labels very noisy (many patterns with both labels) | Reframe: ceiling analysis; emphasise what is irreducible |
| Raw vs de-duplicated differ greatly | Lead with leakage story (title #2) |
| Provenance resolved as independent respondents | Use raw data with respondent-level weights as co-primary |
