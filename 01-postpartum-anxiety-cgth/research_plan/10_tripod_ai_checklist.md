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
| **Data preparation** | Cleaning, duplicates, encoding | Notebook 02 Tasks 4–6 | ✅ |
| **Outcome** | Definition, how and when measured, blinding | `Feeling anxious` = Yes; self-reported, same time as predictors | 🟡 state that it is a single unvalidated item |
| **Predictors** | Definition, measurement, timing | 9 survey items, same time as outcome | ✅ |
| **Sample size** | How the size was justified | Notebook 02 Task 31: Riley criteria need 429–1,512 rows; 326 available | ✅ reported as a limitation |
| **Missing data** | Amount and handling | 27 raw cells (9 in unique rows); most-frequent imputation inside each training fold | ✅ |
| **Analysis: model building** | Model types, hyperparameters, tuning | Notebook 02 Tasks 7–10; hybrids chosen on seeds 7 and 2026, confirmed on seed 42 | ✅ |
| **Analysis: class imbalance** | Whether and how handled | 58/42 split; stratified folds; balanced accuracy as the primary metric; no resampling | ✅ |
| **Analysis: fairness** | Performance in subgroups | Notebook 01 Task 20: by age band (only demographic available) | ✅ |
| **Analysis: performance measures** | Discrimination, calibration, clinical utility | Balanced accuracy, AUC, sensitivity, specificity, MCC (notebook 02 Task 13) | 🟡 add a calibration curve for HE and CG-HE |
| **Analysis: validation** | Internal validation method | 5-fold CV repeated 10 times, corrected 95% CIs and tests | ✅ |
| **Model output** | What the model returns, thresholds | Probability; threshold 0.5; 90% sensitivity point in notebook 01 Task 18 | ✅ |
| **Training vs evaluation data** | Differences between them | Same source, cross-validation only; no external data | ✅ state as a limitation |
| **Explainability** | How the model's decisions are explained | SHAP vs LIME, notebook 02 Tasks 19–27; LR decides 68% of cases directly | ✅ |
| **Open science** | Code, data, protocol availability, registration, funding, conflicts | Code and results in the repository; no registration | 🟡 add funding and conflict statements; consider sharing on Zenodo |
| **Patient and public involvement** | Whether they were involved | Not involved | 🟡 state "none" |
| **Results: participants** | Flow of data, characteristics | 1,503 → 326 unique rows; positive rate 58% | 🟡 add a flow diagram and characteristics table |
| **Results: performance** | Estimates with confidence intervals | Notebook 02 Tasks 13–16 | ✅ |
| **Discussion: interpretation and limitations** | Overall interpretation, limitations, comparison with previous studies | `research_plan/07`, literature table row 17 and replication (Task 30) | ✅ |
| **Discussion: usability** | Intended use, next steps (external validation) | Screening support only, not diagnosis; second dataset needed | ✅ |

## Still missing before a journal submission
1. Verify the dataset licence on the Kaggle page itself (mirror sites are shut down or do not show it).
2. Add a calibration curve for the two proposed hybrids.
3. Add a data-flow diagram (1,503 → 326 rows) and a characteristics table.
4. Add funding, conflict-of-interest and patient-involvement statements.
5. Fill in the official 27-item checklist with page numbers.
