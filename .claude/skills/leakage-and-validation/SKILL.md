---
name: leakage-and-validation
description: Checklist for preventing data leakage and choosing the right validation scheme (random, stratified, grouped, time-based). Use before splitting data and when auditing a notebook.
---
# Leakage and validation

## Leakage sources to check, in order
1. **Preprocessing before split:** imputation, scaling, encoding, feature selection, PCA, resampling fitted on all rows. Fix: Pipeline, fit on train only.
2. **Duplicates / near-duplicates** across train and test. Count with `df.duplicated().sum()`; if present, deduplicate *or* report duplicate-aware validation alongside the standard one.
3. **Target leakage:** columns computed from, or recorded after, the outcome (IDs, timestamps of outcome, derived scores). Inspect every column's meaning in the data card; ask the user if unclear.
4. **Group leakage:** several rows from the same person/site/region split across train and test. Fix: group splits.
5. **Temporal leakage:** training on the future to predict the past. Fix: time-ordered split.
6. **Selection leakage:** choosing features/models/thresholds using the test set. Fix: touch the test set once.
7. **Resampling leakage:** SMOTE/oversampling before CV. Fix: inside the Pipeline (use `imblearn.pipeline.Pipeline`) so only training folds are resampled.

## Which split
| Data structure | Outer split | CV inside training |
|---|---|---|
| iid rows, classification | `train_test_split(stratify=y)` | `RepeatedStratifiedKFold` |
| iid rows, regression | `train_test_split` | `RepeatedKFold` |
| repeated subjects/sites/regions | `GroupShuffleSplit` / hold out whole groups | `StratifiedGroupKFold` / `GroupKFold` |
| time series | last block as test | `TimeSeriesSplit` |

## Sanity checks
- Does test score ≈ CV score? A big gap in either direction needs an explanation.
- Does a shuffled-target run give chance-level score? (`y_train.sample(frac=1, random_state=SEED)` fitted in the same Pipeline; a strong score means leakage.)
- Is the best feature suspiciously strong? Look at its meaning.

## Reporting
State in the notebook: the split, why it fits the data structure, duplicates found, and any leakage risk that could not be ruled out.
