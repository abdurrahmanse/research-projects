# 12 · Figures and Tables Plan

Rule: every figure answers a stated question. None is decorative. All figures show uncertainty where a statistic is plotted. Use colour-blind-safe palettes; consistent model colours across all figures; vector (PDF/SVG) output.

## Figures
| ID | Figure | Scientific purpose | Input data | Type | Should demonstrate | Interpretation pitfalls | Placement |
|---|---|---|---|---|---|---|---|
| F1 | Study workflow | Methods transparency | — | Flow diagram (use the Mermaid in `07`) | Where each decision sits relative to CV loops | Looks like a pipeline for deployment, which it is not | Ch.3 / paper Fig.1 |
| F2 | Nested CV + data-arm design | Prove leakage control | — | Schematic | Outer/inner folds, group handling, locked hold-out | — | Ch.3 |
| F3 | Dataset characteristics | Describe sample | Raw CSV | Stacked horizontal bars per item (counts, %) | Distribution of answers; Age bands | Not representative of any population | Ch.3 |
| F4 | Duplication profile | Quantify data issue | Pattern counts | (a) rank–frequency plot of patterns; (b) submissions per minute | 326 unique/1,503; clustering of identical rows | Do not assert fabrication; state hypotheses | Ch.3 (or Appendix) |
| F5 | Missingness | Justify imputation | Raw CSV | Matrix/bar | <2%, 3 items | — | Appendix |
| F6 | Class distribution (raw vs de-dup) | Show prevalence shift | Counts | Paired bars | 65.2% → 58.0% | — | Ch.3 |
| F7 | Association structure | Redundancy | All items | Cramér's V / MI heat map (not Pearson on codes) | Which items overlap | Association ≠ causation | Ch.3 |
| F8 | Leakage inflation | RQ6/H5 | Metrics per arm × model | Dumbbell/slope plot with CIs | Gap between naive and group-aware | Different n across arms | Ch.4 |
| F9 | Model comparison | RQ1 | Outer-fold AUC per model | **Forest plot** (point + 95% CI), sorted, with baselines marked | Which models are distinguishable from LR | Overlapping CIs ≠ equality | Ch.4 |
| F10 | ROC curves | Discrimination | Pooled OOF predictions | ROC with bootstrap band, top models + baseline | Operating-point trade-offs | Pooled curve mixes fold models | Ch.4 |
| F11 | Precision–recall curves | Minority/screening performance | Pooled OOF | PR with prevalence line | Precision at high recall | Baseline = prevalence, not 0.5 | Ch.4 |
| F12 | Confusion matrices at pre-set thresholds | Error profile | Pooled OOF at t₁/t₂ | Normalised matrices (top 3 models only) | FN/FP counts | Threshold-dependent | Ch.4 / Appendix |
| F13 | Calibration plots | RQ/H3 | Pooled OOF probs | Reliability curves (quantile bins + smooth), histogram of predictions beneath; before/after calibration | Over/under-confidence | Few points per bin at n≈326 | Ch.4 |
| F14 | Decision curves | G11 | Calibrated OOF probs | Net benefit vs threshold (model, treat-all, treat-none) | Where model adds value | Optimistic; depends on harm assumptions | Ch.4 |
| F15 | Risk distribution & tiers | RQ4 | Calibrated probs | Histogram/violin by true class with tier cut-offs; observed rate per tier with CIs | Separation; tier monotonicity | Cut-offs chosen on inner data | Ch.4 |
| F16 | Ablation summary | RQ3/ablations | A1–A12 deltas | Forest of Δ with CI | Which design choices matter | Multiple comparisons | Ch.4 |
| F17 | Ensemble diversity | Why ensembles do/don't help | OOF predictions | Error-correlation heat map; ΔAUC vs mean correlation | Redundancy of members | Few models → noisy relation | Ch.4 / Ch.5 |
| F18 | Complexity vs performance | Cost–benefit | Time, params, AUC | Scatter with CI whiskers | Whether complexity pays | Hardware-dependent times | Ch.4 |
| F19 | Statistical comparison matrix | Paired tests | Δ and Holm-adjusted p | Matrix heat map of ΔAUC with significance marks | Which pairs differ | Dependence of folds | Ch.4 / Appendix |
| F20 | SHAP global (bar + beeswarm) | RQ5 | SHAP values (OOF) | Bar with fold-variation bars; beeswarm | Ranked reliance | Not causal | Ch.4 |
| F21 | SHAP dependence / interaction | Non-additive structure | SHAP | Dependence plots | Interactions | Correlated items | Appendix |
| F22 | Local explanations | Case-level reasoning | SHAP | Waterfalls (TP, TN, FN, FP, boundary) | How model reasons | Cherry-picking: choose cases by pre-set rule | Ch.4 |
| F23 | Explanation stability | H6 | Fold-wise rankings | Rank distribution (strip/box) per item; τ matrix | Consistency | Stability ≠ validity | Ch.4 |
| F24 | Cross-model attribution agreement | RQ5 | Rankings per model | τ heat map | Agreement across families | — | Ch.4 |
| F25 | Item-reduction curve | RQ7/H7 | Reduced models | AUC vs #items with CI and non-inferiority margin | Minimal screener | Selection optimism if done outside CV | Ch.4 |
| F26 | Subgroup performance | Fairness | Age-band metrics | Dot-plot with CIs; calibration slope by group | Heterogeneity | Low n | Ch.4 / Appendix |
| F27 | PPV vs prevalence | Transferability caveat | Sens/spec | Curves | PPV in lower-prevalence settings | Assumes constant sens/spec | Ch.5 |
| F28 | Learning curve | Is more data useful? | CV at varied n | AUC vs n | Variance vs bias | — | Ch.5 |

Suggested **paper** main set: F1/F2 (combined), F4, F8, F9, F13, F14, F20, F23 (8 figures); rest in supplement.

## Tables
| ID | Table | Placement |
|---|---|---|
| T1 | Dataset description + answer-scale mapping | Ch.3 |
| T2 | Data-quality audit (duplicates, label conflict, missingness) | Ch.3 |
| T3 | Literature matrix (condensed from file 03) | Ch.2 |
| T4 | Research-gap matrix (G1–G12) | Ch.2 |
| T5 | Model selection and hyperparameter search spaces | Ch.3 |
| T6 | Baseline comparison (T-A in file 08) | Ch.4 |
| T7 | Advanced model comparison (T-B) | Ch.4 |
| T8 | Ensemble comparison (T-C) | Ch.4 |
| T9 | Ablation results (T-D) | Ch.4 |
| T10 | Leakage arms (T-F) | Ch.4 |
| T11 | Calibration (T-E) | Ch.4 |
| T12 | Tier performance + net benefit (T-G) | Ch.4 |
| T13 | Complexity (T-H) | Ch.4 |
| T14 | Subgroups (T-I) | Ch.4 |
| T15 | Explanation stability (T-J) | Ch.4 |
| T16 | Statistical test summary (test, assumption, result) | Ch.4 |
| T17 | TRIPOD+AI checklist | Appendix |
| T18 | Software/versions, seeds, compute | Appendix |
| T19 | Limitations ↔ mitigation | Ch.5 |
