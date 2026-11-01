# 02 · Data Audit (findings from inspecting the files and notebooks)

All numbers below were computed directly from `projects/post natal data.csv`.

## 1. Dataset facts
- 3 identical CSV copies exist (`post natal data.csv`, `postnataldata.csv`, `Postpartum_depression_data.csv`; same MD5). Keep one, record the original source/URL (e.g., Kaggle) and licence, delete the others.
- 1,503 rows × 11 columns; June 2022 survey (Timestamp 6/14/2022 20:02 onward).
- Age bands only 25–50 (no <25; no continuous age).
- Missing values: Irritable 6, Concentration 12, Guilt 9 (27 cells total, <2%). Mode imputation is acceptable at this rate but do it **inside** CV folds.

## 2. Class and answer distributions (raw, n = 1,503)
| Item | Distribution |
|---|---|
| Feeling anxious (target) | Yes 980 (65.2%) / No 523 (34.8%) |
| Suicide attempt | No 709 / Yes 459 (30.5%) / Not interested to say 335 |
| Feeling sad | Yes 536 / No 524 / Sometimes 443 |
| Sleep trouble | Two+ days/week 640 / Yes 445 / No 418 |
| Appetite | No 841 / Yes 343 / Not at all 319 |

After de-duplication (n = 326): anxious = 189 (58.0%) / 137. De-duplication **shifts class prevalence** from 65.2% to 58.0%.

## 3. Red flags
| # | Finding | Why it matters | Action |
|---|---|---|---|
| D1 | Only **326 unique answer patterns** among 1,503 rows (78% repeats); largest pattern occurs 33 times | With 9 mostly 3-level items, 326 unique patterns is low for 1,503 independent people | Establish provenance; report as limitation |
| D2 | Only 90 distinct timestamps (minute resolution); groups of 14, 21, 28, 35 rows are common (multiples of 7); up to 51 submissions in a single minute | Pattern suggests bulk entry, replication or augmentation, not independent respondents. *This is an inference, not proof.* | Contact dataset owner / check source description; run raw vs. de-duplicated analyses |
| D3 | Suicide item: 30.5% "Yes" and item says "attempt" | Implausible for a general postpartum population; probably a mislabeled or low-quality item | Treat with caution; do not present as clinical prevalence |
| D4 | Identical rows in train and test if raw data are split randomly | Data leakage → inflated scores | Use **group-aware splitting** (group = unique response pattern) on raw data, or analyse de-duplicated data |
| D5 | Timestamp is dropped before de-dup | Rows with different timestamps were treated as the same record | Document that "duplicates" = identical answers, not identical submissions |

Note: dropping identical answer patterns is not obviously "right". If the 1,503 are real independent respondents, de-duplication throws away legitimate information and biases prevalence. If they are replicated, raw data inflate performance. **You cannot know which without provenance**, which is why the plan runs both and reports both.

## 4. Issues in `main-projects.ipynb`
| # | Issue | Evidence | Fix |
|---|---|---|---|
| N1 | Arbitrary ordinal encoding | `astype('category').cat.codes` sorts alphabetically: Suicide `No=0, Not interested=1, Yes=2`; Sleep `No=0, Two+ days=1, Yes=2`; Appetite `No=0, Not at all=1, Yes=2` ("Not at all" is semantically *No*) | Explicit mapping per item; one-hot for nominal answers; run encoding sensitivity analysis (ordinal vs one-hot) |
| N2 | Encoding applied to the **target** with cat.codes | Works (No=0, Yes=1) but implicit | Explicit `{'No':0,'Yes':1}` |
| N3 | Single 80/20 split | n_test = 66; RF 53/66 correct → 95% CI ≈ 80.3% ± 9.6 | Repeated stratified k-fold (e.g., 5×10) |
| N4 | Model chosen using test results; mode imputation and encoding done before split | Optimistic bias | Nested CV; pipeline with imputer/encoder inside folds |
| N5 | Hyperparameters hand-set | e.g., RF depth 4, GB lr .03 | Tune in inner CV; report search spaces |
| N6 | Ensemble ≈ GB exactly (78.8%/83.7/94.7 identical) | Ensemble adds nothing here | Report honestly; analyse diversity (correlation of errors, disagreement) |
| N7 | Accuracy emphasised; no baseline | Majority-class accuracy = 58% on this split | Add dummy baselines, balanced accuracy, MCC, PR-AUC |
| N8 | Probabilities quoted as "confidence" | `predict_proba` of RF is uncalibrated | Calibrate; call it "estimated risk" |
| N9 | Notebook "best model" text hard-coded | Cell 21 prints strings | Compute from results |
| N10 | No explainability, no stratification | — | See `04`, `07` |
| N11 | Hard-coded patient examples in `c_project.ipynb` using manual codes | Easy to mis-encode | Use the same fitted pipeline on raw-text input |

## 5. `c_project.ipynb` (56 steps): reusable ideas
Contains SMOTE, class weights, grid search, ROC, 10-fold CV, calibration, Brier, learning curve, SHAP, McNemar, majority baseline, and feature engineering. Good checklist, but caution: **SMOTE is applied before evaluation on training data and metrics like "train accuracy on SMOTE data" are not comparable**; with all-categorical survey features, SMOTE interpolation produces non-existent answer combinations. Prefer class weights / threshold tuning; if SMOTE-NC is kept, apply it only inside CV training folds and report as a sensitivity analysis.
