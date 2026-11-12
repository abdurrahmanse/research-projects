---
name: model-selection
description: How to choose models, metrics and comparison methods for tabular data science research (classification, regression, imbalance, small data). Use when planning or justifying which models to train and how to compare them.
---
# Model and metric selection (tabular research)

## Always include, in this order
1. **Trivial baseline**: `DummyClassifier(strategy="most_frequent")` / `DummyRegressor(strategy="mean")`.
2. **Simple interpretable model**: `LogisticRegression` / `Ridge` (`LinearRegression` if features are few).
3. **Tree ensembles**: `RandomForest*` and `HistGradientBoosting*` (handle non-linearity and mixed scales, strong defaults).
4. Optional: XGBoost/LightGBM/CatBoost only if the user's research question names them or the data warrants it; say which version is pinned.

Do **not** use deep learning on small or medium tabular data unless the research question requires it. Justify every extra model with the question it answers.

## Choosing by situation
| Situation | Choice |
|---|---|
| < ~1,000 rows | simple models + regularisation; repeated CV with more repeats; be explicit that estimates are noisy |
| Many categorical features | one-hot in the Pipeline; CatBoost if cardinality is high (document it) |
| Heavy imbalance | stratified splits, `class_weight="balanced"` or resampling **inside** the Pipeline only; metric: PR-AUC, F1 (macro), balanced accuracy; never plain accuracy |
| Grouped rows (same person/site/region) | `GroupKFold` / `StratifiedGroupKFold`; report grouped and ungrouped scores side by side |
| Time-ordered data | `TimeSeriesSplit`; never shuffle |
| Need to explain the model | logistic/linear coefficients, permutation importance, SHAP for tree models; check stability across folds |
| Regression | metrics: RMSE and MAE with R² as context; plot residuals |

## Metrics (decide before training)
- Binary balanced: accuracy, F1, ROC-AUC. Binary imbalanced: PR-AUC, balanced accuracy, F1. Multiclass: macro-F1, balanced accuracy.
- Report one **primary** metric chosen in advance and secondary ones for context.
- Medical/risk screening: report sensitivity and specificity explicitly.

## Fair comparison protocol
1. Same split, same preprocessing Pipeline, same CV object (fixed seed) for every model.
2. Tune hyperparameters only inside the training portion (inner CV or `GridSearchCV` on the training set) with the **same budget** for each model. If untuned defaults are used, say so.
3. Select the model by CV mean (+ spread), then evaluate **once** on the held-out test set.
4. Report mean ± std over repeated CV. For a significance claim, use the corrected resampled t-test (Nadeau & Bengio, 2003) or a Wilcoxon signed-rank test over paired fold scores, and state that fold scores are not independent. If it is not significant, write "no significant difference".
5. Report all models, including those that lost.

## Red flags
- Test score far above CV score, or accuracy near 100%: suspect leakage (duplicates, target-derived feature, ID column).
- A feature that is a near-copy of the target.
- Tuning on the test set, even "just a little".
- Comparing models with different preprocessing or folds.

## Regression recipe and gotchas
- Metrics: RMSE primary (target units), MAE and R² secondary. Lower is better for RMSE/MAE, **higher** for R². Pick the best model with `idxmin` for error metrics and `idxmax` for R² / accuracy-type metrics.
- sklearn scorers named `neg_*` return **negative** values (`neg_root_mean_squared_error`). Flip the sign before putting them in tables or plots.
- `cross_validate(..., scoring={"rmse": "neg_root_mean_squared_error", "mae": "neg_mean_absolute_error", "r2": "r2"})` gives all metrics from the same folds. Build the summary from `test_rmse`, `test_mae`, `test_r2`; the full pattern is in `docs/notebook_skeleton_regression.py`.
- For the test score use `root_mean_squared_error` (sklearn 1.4+; `mean_squared_error(squared=False)` is removed in newer versions). Pin sklearn in `requirements.txt`.
- Use `RepeatedKFold` (no stratify) for regression.
- Simple model: `Ridge`/`LinearRegression`. Untuned defaults for every model are acceptable if stated as a limitation. If tuning, give each model the same budget (e.g. `GridSearchCV` inside the Pipeline on training data; `RidgeCV` for Ridge's alpha).

## Significance recipe (paired, over repeated-CV scores)
Fold scores overlap in training data, so use the Nadeau-Bengio corrected variance. With 5 folds the test/train ratio is 1/4:
```python
from scipy import stats
d = cv_table["Ridge"] - cv_table["Random forest"]  # paired per-fold differences
t = d.mean() / ((1 / len(d) + 1 / 4) * d.var(ddof=1)) ** 0.5
p = 2 * stats.t.sf(abs(t), df=len(d) - 1)
```
Compare only the baseline-vs-best and best-vs-runner-up pairs you planned in advance; with several pairs, correct for multiple comparisons (Holm). Report the p-value and the mean difference with its CI, not just "significant". If a test is skipped, say that box overlap is only a rough guide.
