# 08 · Evaluation and Statistical Analysis

**All result tables below are empty templates. No performance value has been generated.**

## 1. Metric suite
| Family | Metric | Notes / caveats |
|---|---|---|
| Discrimination | ROC-AUC (primary) | Prevalence-insensitive; can mask poor performance at the operating point |
| | PR-AUC / average precision | Prevalence-dependent; compare against the prevalence baseline (58%/65%), not 0.5 |
| Threshold-based | Accuracy, balanced accuracy, sensitivity, specificity, precision (PPV), NPV, F1, macro-F1 (reported for completeness; binary task), MCC [M: Chicco & Jurman 2020] | Report at pre-specified thresholds (§4). Accuracy only with majority baseline beside it |
| Counts | Confusion matrix (pooled out-of-fold) | Include false-negative count/rate |
| Probability quality | Brier score (+ skill vs prevalence-only Brier), log-loss | Proper scoring rules |
| | Calibration curve (reliability diagram, quantile bins) | Bins are arbitrary; add smoothed (LOESS) curve |
| | Calibration intercept & slope (logistic recalibration) [M: Van Calster 2019] | Ideal 0 and 1 |
| | Integrated Calibration Index (ICI) | Prefer over ECE for small n |
| | ECE | Report only with bin-count sensitivity; sensitive to binning and unstable at n≈300 |
| Utility | Net benefit / DCA | §6 |

## 2. Uncertainty
| Method | Use | Limitation |
|---|---|---|
| Fold-wise mean ± SD over repeated CV | Descriptive | Folds overlap → SD understates true variance |
| **Bootstrap CI on pooled out-of-fold predictions** (percentile or BCa; resample *groups* in Arm G) | Main CI for every metric | Treats OOF predictions as independent test data; slightly optimistic; models trained on different folds |
| **Corrected resampled variance** (Nadeau & Bengio) | CI/test for CV differences | Assumes the 1/J + n_test/n_train correction is adequate [M: Nadeau & Bengio 2003] |
| Wilson / exact CI | Single proportions (sens, spec) | n small ⇒ wide |
| Repeated nested CV with fresh seeds | Variance of the whole procedure | Cost |

Always display CIs on the main figure; do not rank models whose CIs overlap without a paired test.

## 3. Statistical comparison — which test, when
| Situation | Appropriate test | Why / assumptions | Avoid |
|---|---|---|---|
| Compare two models across repeated-CV folds (**primary**) | **Corrected resampled t-test** on paired per-fold differences [M: Nadeau & Bengio 2003]; or Wilcoxon signed-rank on per-repeat means as a sensitivity check | Accounts for training-set overlap; paired by identical folds | Uncorrected paired t-test across CV folds (inflates type-I error) [M: Dietterich 1998] |
| Compare two classifiers' errors on **one fixed test set** (locked hold-out) | **McNemar** (exact binomial if discordant pairs < 25) [M: Dietterich 1998] | Paired, same test cases; ignores training variability | Applying across pooled OOF predictions as if independent without noting dependence |
| Compare **AUCs from the same cases** (hold-out or pooled OOF) | **DeLong** test [M: DeLong 1988] | Correlated ROC curves on identical subjects; large-sample | With few cases (n≈65 hold-out is borderline); combine with paired bootstrap |
| Differences in any metric | **Paired bootstrap** of the difference (resample cases or groups) | Distribution-free, covers Brier/PR-AUC/net benefit | Resampling rows when groups exist (leakage into CI) |
| Many models vs one baseline | Holm–Bonferroni across the family | Controls family-wise error | Reporting 40 uncorrected p-values |
| Ranking many models | Friedman + Nemenyi / Conover [M: Demšar 2006] | Needs multiple *datasets*; with one dataset, repeated-fold ranks are dependent → use only descriptively | Treating folds as independent datasets |
| Calibration difference | Paired bootstrap on Brier / ICI | Proper-score difference | Hosmer–Lemeshow (binning, low power) |

Report effect size (Δ with 95% CI) first and p-value second. State "no evidence of difference" rather than "equal" for non-significant results; use equivalence/non-inferiority (TOST or CI within margin) when claiming parity (H7).

## 4. Decision thresholds and risk stratification
**Principle:** tiers are *model-estimated symptom-burden strata*, not clinically validated risk categories.

1. Calibrate probabilities first (inner OOF).
2. Pre-specify two cut-offs **before** looking at outer-fold performance, using one of:
   - Screening-priority rule: low-tier cut-off t₁ = highest probability at which inner-OOF **sensitivity ≥ 0.90** for the remainder (i.e., "rule-out" zone, NPV high); high-tier cut-off t₂ = lowest probability at which inner-OOF **PPV ≥ 0.80** ("rule-in" zone); the rest = medium.
   - Cost-ratio rule: threshold probability p_t = 1/(1 + C_FN/C_FP). A cost ratio is a *stated assumption* (e.g., missing a case is 3–5× worse than a false alarm → p_t ≈ 0.17–0.25). Show a sensitivity analysis over ratios.
3. Apply unchanged to outer-test folds; report per tier: n, observed event rate (95% CI), share of all positives captured, false-positive burden.
4. Trend test (Cochran–Armitage) for monotone observed rate across tiers (H8).
5. False-negative analysis: describe patterns of missed cases (e.g., all low symptom burden?) with SHAP local explanations.
6. Future validation: tiers/thresholds must be re-estimated and prospectively validated against EPDS/GAD-7 or a structured clinical interview in an independent cohort.

## 5. Calibration protocol
- Methods: none; Platt (sigmoid); isotonic (guard against overfit: n small); beta calibration; for ensembles also stacking as recalibrator.
- Fit calibrators only on inner OOF predictions; assess on outer-test.
- Report intercept, slope, ICI, Brier (+ Brier skill), reliability plots with CI band.
- Caveat: calibration within the *dataset's prevalence* (58–65%) does not transfer to a population with lower prevalence; state this explicitly and show PPV as a function of prevalence.

## 6. Decision-curve analysis [M: Vickers & Elkin 2006]
- Plot net benefit vs threshold probability from 0.1–0.8 for: model(s), treat-all, treat-none. Use out-of-fold calibrated probabilities.
- Interpretation: net benefit above both references indicates added value *at that threshold*. High prevalence (~58–65%) makes treat-all strong at low thresholds; discuss.
- Limits: assumes the model's probabilities are calibrated; benefit units depend on the assumed harm of a false positive; no clinical cost data exist here; DCA on the development data is optimistic.

## 7. Required result tables (empty templates)

**T-A Baseline comparison** (primary arm D, nested CV, mean [95% CI])
| Model | ROC-AUC | PR-AUC | Bal. Acc | Sens | Spec | MCC | Brier | ICI | Slope |
|---|---|---|---|---|---|---|---|---|---|
| Dummy | | | | | | | | | |
| Pattern-lookup | | | | | | | | | |
| LR | | | | | | | | | |
| NB | | | | | | | | | |
| DT | | | | | | | | | |

**T-B Advanced models**: same columns for SVM, RF, ET, GB, XGB, CatBoost (+ LightGBM if run).

**T-C Ensemble comparison**
| Model | ROC-AUC | Δ vs best single [95% CI] | Corrected-t p (Holm) | Brier | ICI | Train time | #params/trees |
|---|---|---|---|---|---|---|---|

**T-D Ablations** (A1–A12): columns = arms; rows = metric; Δ with CI.

**T-E Calibration**: model × {raw, Platt, isotonic, beta} × {Brier, ICI, slope, intercept}.

**T-F Uncertainty/leakage**: arm {naive-raw, group-raw, de-dup} × model × AUC/accuracy; Δ(naive − group) with CI.

**T-G Clinical utility**: tier × {n, observed rate [CI], sens captured, PPV, FP count}; plus net benefit at p_t ∈ {0.2, 0.3, 0.4, 0.5, 0.6}.

**T-H Model complexity**: model × {params/trees, train s, predict ms, #tuned hyperparameters, ΔAUC vs LR}.

**T-I Subgroups**: Age band × {n, prevalence, AUC [CI], sensitivity, calibration slope}; mark underpowered cells.

**T-J Explanation stability**: model × {median Kendall τ, top-3 Jaccard, rank-1 consistency}.

## 8. Sample-size and power notes
- Use Riley et al. criteria for prediction-model sample size [M: Riley 2020] to compute the minimum n for LR with ~20 one-hot parameters; compare to n=326 (events 137). If the criteria are not met, state that estimates (esp. calibration slope) are expected to be unstable and shrinkage (L2) is used.
- Precision of sensitivity at n_pos=189: Wilson 95% half-width ≈ ±5–7 pts at 0.8; at n=65 hold-out far wider. Report intervals.
