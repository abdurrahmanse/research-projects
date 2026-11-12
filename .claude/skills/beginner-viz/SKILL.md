---
name: beginner-viz
description: Rules and minimal recipes for clear, honest, beginner-friendly research visualizations (matplotlib). Use whenever a notebook needs a chart for EDA, model comparison or evaluation.
---
# Beginner-friendly research visualization

## Rules
1. **One chart answers one question.** State the question in the markdown cell before the chart.
2. Plain matplotlib (pandas `.plot`) first. Add seaborn only if the chart is impossible without it.
3. Always: title, axis labels with units, legend only if more than one series. Readable at paper size (dpi=150, `bbox_inches="tight"`).
4. Save every figure to `results/figures/` with a descriptive name. Do not skip saving.
5. EDA charts use **training data only**. Never look at the test set to choose features or models.
6. Show uncertainty: box plots or error bars for CV results, never bare bars of means.
7. No pie charts, 3D charts, dual axes or decorative styling. Bars start at zero; box/line charts may not.
8. Colour-blind safe: use one hue plus grey, or matplotlib's default cycle. Do not encode meaning by red/green alone.
9. After each chart, the markdown says how to read it in one line (what a good/bad pattern looks like). Numbers in text come from printed output, not from eyeballing.

## Which chart for which question
| Question | Chart | Recipe |
|---|---|---|
| Is the target balanced? | bar of class counts | `y_train.value_counts().plot.bar()` |
| How is a numeric feature distributed? | histogram | `X_train["col"].plot.hist(bins=30)` |
| Which columns have missing data? | horizontal bar | `X_train.isna().mean().sort_values().plot.barh()` |
| Does a feature differ by class? | box plot | `X_train.assign(y=y_train).boxplot(column="col", by="y")` |
| Which features move together? | correlation heatmap (only if ≤ ~15 numeric features) | `plt.imshow(X_train.corr(numeric_only=True), vmin=-1, vmax=1, cmap="coolwarm"); plt.colorbar()` |
| Which model is best, with spread? | horizontal box plot of CV scores | `cv_table.plot.box(vert=False)` |
| Where does a classifier err? | confusion matrix | `ConfusionMatrixDisplay.from_predictions(y_test, y_pred)` |
| Ranking quality (binary) | ROC and precision-recall curves; PR is the primary one under imbalance | `RocCurveDisplay.from_estimator`, `PrecisionRecallDisplay.from_estimator` |
| Are probabilities trustworthy? | calibration curve | `CalibrationDisplay.from_estimator` |
| Regression fit | predicted vs actual with y=x line; residuals vs predicted | `plt.scatter(y_true, y_pred)`; `plt.scatter(y_pred, y_true - y_pred)` |
| More data or more complexity help? | learning curve | `LearningCurveDisplay.from_estimator` |
| What does the model rely on? | permutation importance bar (top 10) | see `docs/notebook_skeleton.py` |

## Pitfalls to warn the learner about
- A heatmap of 50+ columns is unreadable: filter first.
- Truncated bar axes exaggerate differences.
- Tiny differences between box plots that overlap are not evidence of a better model.
- A chart from the test set that influenced a decision is leakage.
