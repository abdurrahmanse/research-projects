# 01 · Project and Dataset Audit

Evidence base: direct inspection of `projects/post natal data.csv`, `projects/main-projects.ipynb` (22 cells, outputs as saved), `projects/c_project.ipynb` (56 steps), and web sources listed in `references.md`.
Tags: **[C]** confirmed · **[H]** hypothesis requiring verification · **[U]** unsupported.

## 1. Files in the project
| File | Finding |
|---|---|
| `post natal data.csv`, `postnataldata.csv`, `Postpartum_depression_data.csv` | **[C]** Byte-identical (same MD5). Keep one canonical copy; record its hash. |
| `main-projects.ipynb` | Core work (5 models, 80/20 split). |
| `c_project.ipynb` | Extended variant (SMOTE, tuning, calibration, SHAP, McNemar). Reusable ideas, but see §5. |
| `.venv/` | Contains pandas 3.1.0 and scikit-learn 1.9.1 (as imported by the venv). Pin versions in a lock file. |

## 2. Dataset investigation (§1.1 of the brief)

### 2.1 Origin and documentation
| Item | Status |
|---|---|
| Public name | "PostPartum Depression", Kaggle user `parvezalmuqtadir2348` **[C]** (cited by [L16]); the Kaggle page could not be rendered by my fetch tool, so licence, column description and file notes are **not verified** |
| Collection description | A commercial data-listing page (GTS) states: *1,503 records from a medical hospital using a questionnaire administered through a Google form*; *"has not yet been published"*; *"15 attributes, 10 selected, 9 for analysis and 1 target"*; target *"Feeling Anxious"* chosen *"as a predictor of postpartum depression"* **[C that the text exists; its truth is unverified]** |
| Peer-reviewed documentation | None found **[C]** |
| Licence | Not found **[C]** |
| Hospital, country, ethics approval, language of survey, respondent eligibility, time since delivery | Not stated anywhere I could access **[C]** |
| Studies using it | [L16] arXiv preprint (GenAI/real-time detection); [L17] ICSUMMIT 2026 proceedings, 1,503 entries, accuracy 96.99% with RFE (validation method not stated) |

### 2.2 Structure (computed from the CSV)
| Property | Value | Tag |
|---|---|---|
| Rows × columns | 1,503 × 11 (Timestamp + Age + 8 symptom items + Suicide attempt) | C |
| Feature types | All categorical text. Age: 5 bands (25–50). Others: 2–3 categories with **inconsistent vocabularies** (Yes/No/Sometimes; Yes/No/Maybe; Yes/No/Often; Yes/No/"Two or more days a week"; Yes/No/"Not at all"; Yes/No/"Not interested to say") | C |
| Missing | Irritable 6, Concentration 12, Guilt 9 (27 cells, <2%); no other column | C |
| Distinct timestamps | **90** (minute resolution), 14–15 June 2022 | C |
| Rows per timestamp | typically 14, 21, 28, 35 (multiples of 7); maximum 51 in one minute | C |
| Distinct 10-column answer patterns (excluding timestamp) | **326** (largest pattern appears 33×) | C |
| Duplicate rows (excl. timestamp) | **1,177 (78.3%)** | C |
| Possible predictor patterns | 5 × 3⁸ = 32,805 (65,610 with target). With n = 1,503 independent respondents spread over this space, ~17 coincident pairs would be expected under *uniform* answers. Real answers are skewed so more collisions are expected, but 1,177 duplicate rows is far beyond plausible chance. | H (heuristic argument, not proof) |

### 2.3 Targets and clinical meaning
| Question | Answer |
|---|---|
| Target in notebook | `Feeling anxious` (Yes/No). **[C]** |
| Is it a validated anxiety measure (GAD-7, STAI, EPDS-3A)? | **No.** Single self-report item **[C]**. Clinical meaning = *self-reported anxious feeling*, not anxiety disorder |
| Is depression separately measured? | **No validated depression label.** "Feeling sad or tearful", "guilt", "sleep", "appetite", "concentration" are depressive-symptom items, but there is no EPDS/PHQ-9 total or diagnosis **[C]** |
| Is "Suicide attempt" usable as an outcome? | Item is an **[U]**-quality outcome: wording ("attempt") and 30.5% Yes (459/1,503) are implausible for a general postpartum survey; "Not interested to say" = 335 |
| Task types supported | Single-label binary classification (anxiety symptom) **[C]**. Multi-output over symptom items is *technically* possible but clinically meaningless without validated constructs |
| Another group's use of the same label | GTS description frames "Feeling Anxious" as a *predictor* of PPD, and [L16] reports 968 vs 523 for the equivalent label on 1,491 rows, consistent with the 980/523 here **[C]**; this confirms the label is used as a PPD proxy elsewhere, which is not a validated proxy **[U]** |

### 2.4 Class prevalence
| Version | Anxious = Yes | No | Prevalence |
|---|---|---|---|
| Raw (n=1,503) | 980 | 523 | 65.2% |
| De-duplicated (n=326) | 189 | 137 | 58.0% |

De-duplication changes the prevalence by 7 points **[C]**, so it is not neutral.

### 2.5 Other required checks
| Check | Finding |
|---|---|
| Outliers / measurement error | N/A (categorical). Inconsistent answer vocabularies are the measurement problem: e.g., "Sometimes" vs "Maybe" vs "Often" vs "Two or more days a week" are different scales **[C]** |
| Correlated/redundant features | Not yet computed. Use Cramér's V / mutual information (not Pearson on arbitrary codes as in the notebook) **[H]** that symptom items are moderately associated |
| Leakage | (i) Identical rows across a random train/test split inflate scores [H, test via RQ6]; (ii) mode imputation and encoding before split; (iii) model chosen on test set |
| Label noise | Unknown. **Computable:** fraction of answer patterns appearing with both target values in raw data. A high fraction = irreducible error ceiling [H] |
| Sensitive variables | Age band only. Suicide item is sensitive. No ethnicity/SES/parity |
| Availability at screening time | Items describe *current* symptoms; "Suicide attempt" and "Feeling anxious" co-occur in time → not a prospective predictor [C by design] |
| Temporal information | Timestamps are survey submission times, not postpartum time, delivery date, or follow-up → **no support for "early" prediction** [C] |
| Supports meaningful risk stratification? | Only as *model-estimated symptom-burden tiers*, not clinically validated risk. Needs calibrated probabilities and a stated cost ratio |

### 2.6 Claims the dataset does and does not support
| Claim | Supported? |
|---|---|
| "Predicts postpartum depression" | **No** |
| "Predicts postpartum anxiety (disorder)" | **No** |
| "Classifies self-reported anxious feeling from other self-reported symptoms" | **Yes** |
| "Early" prediction | **No** (cross-sectional) |
| "Risk stratification" | **Conditionally** — as calibrated model-based tiers, exploratory only |
| "Explainable" | Yes, as post-hoc attribution (not causal) |
| Generalises to other populations | **No** evidence; single unidentified source |

## 3. Existing notebook audit (§1.2)

Quoted numbers are the notebook's own saved outputs on its single 80/20 split (n_train = 260, n_test = 66).

| Component | Existing Approach | Identified Limitation | Proposed Improvement | Scientific Justification |
|---|---|---|---|---|
| Duplicate handling | Drop Timestamp, `drop_duplicates()` → 326 rows | Silently deletes 78% of data; alters prevalence; provenance unknown | Three analysis arms: naive split on raw (leakage demo), group-aware CV on raw, de-duplicated; report all | Makes the leakage effect itself a result (RQ6); avoids hiding a data issue |
| Missing values | Mode imputation on full data before split | Leaks distribution; ignores that missing = no response | Impute inside CV pipeline; add missing-indicator sensitivity run | Prevents optimistic bias; <2% missing so low impact |
| Encoding | `astype('category').cat.codes` for every column | Alphabetical order → e.g., Suicide: No=0, "Not interested"=1, Yes=2; Sleep: No=0, "Two+ days/week"=1, Yes=2; Appetite "Not at all" coded above "No" | Explicit documented mapping (ordinal where defensible) vs one-hot; run both as a sensitivity analysis | Linear/kernel models depend on code geometry; invalid ordinality adds artificial structure |
| Target | Encoded `Feeling anxious`: No=0, Yes=1 | Implicit; single-item label | Explicit mapping; document as symptom label | Construct validity |
| EDA | Target bar chart; Pearson heatmap on codes | Pearson on arbitrary codes is not meaningful | Cramér's V / MI heatmap; per-item stacked bars; missingness plot | Appropriate association for categorical data |
| Split | One stratified 80/20, seed 42 | n_test = 66; RF 53/66 correct ⇒ 95% CI ≈ ±10 pts; luck of one split | Repeated (stratified, group-aware) CV + a final locked hold-out | Variance of estimate dominates model differences |
| Models | LR, RF (depth 4), SVM-RBF, GB (lr 0.03, depth 2), soft voting | Hand-set hyperparameters; no strong modern baselines; no dummy baseline | Dummy + LR baselines, tuned RF/ExtraTrees/GB/XGBoost/LightGBM/CatBoost, nested CV | Fair comparison requires equal tuning budget |
| Hyperparameters | Fixed | Different tuning effort per model not documented | Same search budget per model, inner CV, fixed seeds | Fairness |
| Ensemble | `VotingClassifier(soft)` of the 4 models | Not better than members (78.8% = GB 78.8%); identical GB/ensemble metrics; no diversity analysis | Diversity diagnostics; stacking with OOF predictions; report null result if no gain | Ensembles help only with diverse, individually competent members |
| Metrics | Accuracy, precision, recall, F1, ROC-AUC, CV accuracy, FN count | Single-split point estimates; no CI; no PR-AUC, MCC, Brier, calibration, utility | Full metric suite with bootstrap/CV CIs (file 08) | Reporting standards (TRIPOD+AI) |
| Model selection | "Best = RF" read from test results | Selection on test data → optimistic | Select in inner loop; lock test set | Avoid winner's curse |
| Comparison tests | None | Differences of 1–2 patients are noise | Corrected resampled t-test, McNemar (single test set), DeLong (paired AUC), Holm | Valid inference (file 08) |
| Interpretability | None in `main-projects.ipynb` | Title claims explainability | SHAP + permutation importance + stability analysis (file 09) | Evaluated, not decorative |
| Probabilities | Printed as "confidence" | Uncalibrated RF/GB probabilities ≠ confidence | Calibrate (Platt/isotonic/beta) in inner CV; reliability plots | Needed for any tiering |
| Risk stratification | Absent | Title claim unfulfilled | Tiers by pre-specified thresholds + DCA | File 08 §6 |
| Visualisation | Grouped bar chart of Acc/F1/AUC; five confusion matrices | Bars hide uncertainty; y-axis truncated at 50 | Forest plots with CIs, ROC/PR with bands | Communicates uncertainty |
| Reproducibility | `random_state=42` mostly; relative CSV path; no env lock; hard-coded patient examples | Different seeds/packages change numbers | `pyproject`/lock file, config file, seed list, run-manifest | Replicability |
| Hard-coded text | Summary cell prints "Random Forest" / "37/38 detected" as strings | Will go stale if rerun | Generate summaries from results objects | Integrity |

**Retain:** problem framing, the 5-model idea, class-aware metrics (recall/FN), stratified split, pipeline for SVM.
**Improve:** everything in the table above.
**Replace:** encoding, split, model selection, comparison method.
**Remove:** test-set model selection; Pearson heatmap on codes; "confidence" wording.

## 4. Observed results in the notebook (for the record, not to be reused as findings)
Test accuracy: LR 69.7, RF 80.3, SVM 78.8, GB 78.8, Ensemble 78.8 (%). RF recall 97.4% but specificity ≈ 57% (classification report: "No Anxiety" recall 0.57). These are single-split values on 66 patients and **must not be quoted in the thesis as results**; they only demonstrate that a pipeline runs.

## 5. Notes on `c_project.ipynb`
Useful: duplicate/leakage checks (steps 7, 19), calibration and Brier (45–46), learning curve (47), SHAP (49–50), McNemar (51), majority baseline (52). Cautions: SMOTE is applied before the split's training use and "train accuracy on SMOTE data" is reported; SMOTE on all-categorical survey codes creates non-existent answer combinations; 10-fold CV is run on all of `X, y` (check that resampling is inside folds). Treat as a source of ideas, not as validated code.

## 6. Data-quality verification plan (do before any modelling)
1. Hash the CSV; store `DATA_CARD.md` with source URL, retrieval date, licence (or "unknown").
2. Contact the Kaggle uploader / hospital; ask: eligibility, delivery-to-survey interval, whether rows were replicated/augmented, the survey instrument, language.
3. Compute: pattern-level label-conflict rate; effective sample size; per-minute submission profile.
4. Decide the *primary analysis dataset* before seeing model results (see `07` §2).
5. If provenance cannot be resolved, state in thesis: *"the dataset's origin is undocumented; findings are methodological, not epidemiological."*
