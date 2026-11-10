# 10 — TRIPOD+AI Reporting Checklist (draft)

TRIPOD+AI (Collins et al., *BMJ* 2024;385:e078378) is the reporting guideline for prediction models built with regression or machine learning. This draft maps the guideline's main reporting areas to where this project answers them. **Before submission, fill in the official 27-item checklist from the BMJ paper**; the item grouping below follows its sections but is not a copy of the official wording.

Status: ✅ done · 🟡 partly done · ❌ missing

| Section | What must be reported | Where in this project | Status |
|---|---|---|---|
| **Title** | Prediction model study, target population, outcome | Title says "symptom screening" and "hybrid machine learning"; add "development and internal validation" in the paper title or subtitle | 🟡 |
| **Abstract** | Objective, data, outcome, models, validation, key results with uncertainty | README abstract | 🟡 rewrite with notebook 02 results |
| **Background and objectives** | Clinical context, why a model is needed, development vs validation | `research_plan/04`, README | ✅ |
| **Data source** | Origin, dates, setting, licence | `data/DATA_CARD.md`: Kaggle, Google Form, June 2022 timestamps | 🟡 licence and setting unverified |
| **Participants** | Eligibility, recruitment, number of participants | Unknown from the source; 1,503 rows, 326 unique | ❌ not available from the data provider |
| **Data preparation** | Cleaning, duplicates, encoding | Final notebook Tasks 3–6 | ✅ |
| **Outcome** | Definition, how and when measured, blinding | `Feeling anxious` = Yes; self-reported, same time as predictors | 🟡 state that it is a single unvalidated item |
| **Predictors** | Definition, measurement, timing | 9 survey items, same time as outcome | ✅ |
| **Sample size** | How the size was justified | Final notebook Task 29: minimum Riley criterion needs 374 rows; 326 available | ✅ reported as a limitation |
| **Missing data** | Amount and handling | 27 raw cells (9 in unique rows); most-frequent imputation inside each training fold | ✅ |
| **Analysis: model building** | Model types, hyperparameters, tuning | Final notebook Tasks 8–14; hybrid chosen on seeds 7 and 2026, confirmed on seed 42 | ✅ |
| **Analysis: class imbalance** | Whether and how handled | 58/42 split; stratified folds; balanced accuracy as the primary metric; no resampling | ✅ |
| **Analysis: fairness** | Performance in subgroups | Final notebook Task 28: by age band (only demographic available) | ✅ |
| **Analysis: performance measures** | Discrimination, calibration, clinical utility | Balanced accuracy, AUC, sensitivity, specificity, MCC, calibration curve and Brier score (final notebook Tasks 17, 27) | 🟡 decision curve not included |
| **Analysis: validation** | Internal validation method | 5-fold CV repeated 10 times, corrected 95% CIs and tests | ✅ |
| **Model output** | What the model returns, thresholds | Probability; threshold 0.5 (final notebook Tasks 24–26) | ✅ |
| **Training vs evaluation data** | Differences between them | Same source, cross-validation only; no external data | ✅ state as a limitation |
| **Explainability** | How the model's decisions are explained | SHAP vs LIME, final notebook Tasks 33–44 | ✅ |
| **Open science** | Code, data, protocol availability, registration, funding, conflicts | Code and results in the repository; no registration | 🟡 add funding and conflict statements; consider sharing on Zenodo |
| **Patient and public involvement** | Whether they were involved | Not involved | 🟡 state "none" |
| **Results: participants** | Flow of data, characteristics | 1,503 → 326 unique rows; positive rate 58% | 🟡 add a flow diagram and characteristics table |
| **Results: performance** | Estimates with confidence intervals | Final notebook Tasks 16–23 | ✅ |
| **Discussion: interpretation and limitations** | Overall interpretation, limitations, comparison with previous studies | `research_plan/09`, literature table row 17 and leakage check (Tasks 30–32) | ✅ |
| **Discussion: usability** | Intended use, next steps (external validation) | Screening support only, not diagnosis; second dataset needed | ✅ |

## Still missing before a journal submission
1. Verify the dataset licence on the Kaggle page itself (mirror sites are shut down or do not show it).
2. ~~Add a calibration curve~~ (done: Task 27).
3. Add a data-flow diagram (1,503 → 326 rows) and a characteristics table.
4. Add funding, conflict-of-interest and patient-involvement statements.
5. Fill in the official 27-item checklist with page numbers.
