# 09 · Explainable AI Framework

**Core caution:** attributions describe *what the fitted model uses*, not what causes anxiety. They are not evidence of clinical validity, and in this dataset every predictor is a concurrent symptom (a co-symptom, not a risk factor).

## 1. Methods and suitability
| Method | Explains | Suitable models | Suitability notes |
|---|---|---|---|
| **SHAP – TreeSHAP** [M: Lundberg & Lee 2017; Lundberg 2020] | Exact additive attributions for tree models (log-odds output by default) | RF, ET, GB, XGBoost, CatBoost, LightGBM | Primary method; correlated features share credit unpredictably; interventional vs path-dependent choice must be stated |
| SHAP – Kernel/Permutation explainer | Model-agnostic approximation | SVM, NB, ensembles (voting/stacking) | Slow but feasible at n≈326; use background set from training fold |
| SHAP – Linear | LR coefficients × feature values | LR | Equivalent to coefficient-based explanation; also report odds ratios |
| **Permutation importance** [M: Breiman 2001; Fisher et al. 2019] | Drop in a chosen score when a feature is shuffled | Any model | Computed on held-out fold; misleading with correlated features (shuffling creates impossible patterns) — use grouped permutation for related items |
| LIME | Local surrogate | Any | Unstable (sampling); **use only as a cross-check** on a few cases and report its instability; not for main claims |
| PDP | Average effect of one feature | Any | Assumes independence; with categorical items it is just the per-level mean prediction |
| ICE | Per-instance curves | Any | Shows heterogeneity hidden by PDP |
| Model-native (LR coefficients, tree rules) | Direct | LR, DT | Reference for sanity checks |

## 2. What is being explained (required clarification)
| Object | How to explain | Note |
|---|---|---|
| A single base learner | TreeSHAP / linear SHAP | Faithful to that model |
| The soft-voting ensemble | Kernel/Permutation SHAP on `predict_proba`, or the mean of member SHAP values (valid for linear averaging of probabilities only approximately, because SHAP is on log-odds for trees) | State which; verify additivity numerically |
| A stacked model | Explain the **full stack** via model-agnostic SHAP (inputs = original items), not the meta-learner on member probabilities | Meta-learner SHAP explains the meta features, not the symptoms |
| A calibrated prediction | Explain the pre-calibration score and note calibration is a monotone map; attributions on probability scale need the calibrated function | Report which scale |
| The final tier output | Explain the underlying probability; tiers are a threshold step | Do not attribute to tiers directly |

## 3. Required analyses
| # | Analysis | Procedure | Output |
|---|---|---|---|
| X1 | Global importance | Mean \|SHAP\| (log-odds) per item, per model, on out-of-fold data | Bar + beeswarm |
| X2 | Local explanations | SHAP waterfall for ~6 cases: confident TP, confident TN, borderline, FN, FP, tier-boundary case | Waterfalls |
| X3 | Cross-model comparison | Rank agreement (Spearman/Kendall) of importance across LR, RF, CatBoost, ensemble | Heat map of τ; rank-by-model plot |
| X4 | **Stability across resampling** | For each outer fold/repeat, compute importance on the *trained-fold model evaluated on its test fold*; compute pairwise Kendall τ between folds; top-k Jaccard; rank-1 frequency; bootstrap CIs of mean \|SHAP\| | Stability plot (rank distribution per item) |
| X5 | Correlated predictors | Cramér's V among items; compare ungrouped vs **grouped** permutation importance (e.g., group {sad, guilt, bonding} vs {sleep, appetite, concentration}); check SHAP split across correlated items | Table + discussion |
| X6 | Subgroup differences | SHAP distributions by age band; mean attribution differences with CIs | Small-multiples (flag low n) |
| X7 | Base vs ensemble | Compare attributions of ensemble to those of members; check whether ensemble dilutes or concentrates reliance | Scatter of |SHAP|ensemble vs member |
| X8 | Faithfulness sanity | Delete/mask top-k attributed items and measure AUC drop vs random items | Deletion curve |
| X9 | Consistency with domain knowledge | Qualitative comparison with literature on symptom–anxiety associations; **association only** | Discussion table |
| X10 | Interaction check | SHAP interaction values (trees) for top pairs | Dependence plots |

## 4. Quantitative stability metrics
- Kendall τ-b between importance rankings (fold pairs): median, IQR.
- Top-k Jaccard (k=3,5).
- Rank-1 consistency: proportion of folds in which the same item is #1.
- Coefficient of variation of mean |SHAP| per item.
- Optionally: rank-biased overlap.
Pre-specified thresholds (H6): median τ ≥ 0.7, top-3 Jaccard ≥ 0.6.

## 5. Figures recommended for thesis/paper
Main text: (a) global SHAP bar for the final model with fold-variation error bars; (b) beeswarm for the final model; (c) stability plot (X4); (d) one two-panel local explanation (TP and FN); (e) cross-model agreement heat map.
Supplement: SHAP dependence/interaction, grouped permutation, deletion curves, LIME cross-check.

## 6. Interpretation guardrails (put in the thesis)
1. SHAP values are model-conditional associations; they say nothing about causal influence.
2. With correlated items, attribution among them is partly arbitrary.
3. Items such as "Suicide attempt" could dominate for non-causal or data-quality reasons; test with ablation A10.
4. Stability ≠ validity: an item can be consistently selected and still be a proxy for survey artefacts.
5. Explanations do not prove clinical validity or trustworthiness; clinicians' usability is untested.
6. Report the exact SHAP configuration (explainer, background data, output scale, versions).
