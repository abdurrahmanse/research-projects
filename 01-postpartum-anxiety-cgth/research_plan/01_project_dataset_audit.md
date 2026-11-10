# 01 — Audit of the Existing Project and Dataset

Scope: the original notebook `main-projects.ipynb` (22 cells; now in git history), `data/raw/postpartum_depression.csv`, saved figures. No existing file was modified.

> **Provenance of numbers.** Every figure marked ◆ was computed during this audit with a throw-away script (scikit-learn, fixed seeds) on the CSV as-is. They are *exploratory audit evidence*, not thesis results. Re-derive them in your own seeded, versioned pipeline before citing them.

---

## 1. What the dataset actually is

| Property | Finding | Source |
|---|---|---|
| Files | `Postpartum_depression_data.csv`, `postnataldata.csv`, `post natal data.csv` are **byte-identical** (`cmp`) — three copies of one file | ◆ |
| Origin | Public Kaggle dataset "PostPartum Depression" (uploader `parvezalmuqtadir2348`); mirror descriptions say 1,503 records, collected via **Google Form questionnaire**, "Feeling anxious" named as the target | gts.ai / baselight mirrors (see references.md). Original Kaggle page was **not** opened — verify licence and collection protocol |
| Size | 1,503 rows × 11 columns (Timestamp + Age + 9 questionnaire items) | ◆ |
| Instrument | Unnamed, unvalidated yes/no/sometimes items. **Not** EPDS, PHQ-9, GAD-7 or DASS | ◆ |
| Outcome labels | **None for depression.** No clinical diagnosis, no screening score, no cut-off | ◆ |
| Time structure | Single cross-sectional snapshot (June 2022 timestamps). No gestational/postpartum week, no repeated measures | ◆ |
| Missing | 27 cells (Irritable 6, Concentrating 12, Guilt 9) | ◆ |

## 2. Critical finding #1 — the data are massively replicated

- Only **90 distinct timestamps** for 1,503 rows (mean 16.7 rows/timestamp; one minute has 51 rows, several have 35). A real Google Form does not receive 35–51 independent submissions per minute from postpartum mothers. ◆
- After removing `Timestamp` and exact duplicates only **326 unique response patterns** remain (≈ 21.7 % of rows). Max multiplicity of one pattern: 33. ◆
- 65,610 possible answer combinations exist, so 1,177 coincidental collisions among independent respondents is not credible. ◆
- **Consequence:** the true effective sample size is ≤ 326, possibly less (unique rows still cluster: median 3 unique rows per timestamp, max 17). Any model trained on the raw 1,503 rows is evaluated on near-copies of its training rows. ◆

**Leakage demonstration ◆.** Random Forest, same seed/split logic as the notebook, *without* deduplication: test accuracy **0.993**. With deduplication: **≈ 0.77** (mean over 200 seeds). The 22-point gap is pure duplicate leakage. The notebook correctly deduplicates (cell 5) — good — but the dataset's provenance means even the 326 remaining rows should be treated as possibly synthetic/augmented until proven otherwise (see #3).

## 3. Critical finding #2 — label validity and clinical plausibility

The notebook's target is `Feeling anxious` (Yes = 1, 58 % of 326 unique rows ◆). It is **one self-reported symptom item**, not "anxiety", not "depression", not "risk".

Association of each predictor with the target among the 326 unique rows (Cramér's V ◆):

| Feature | V | Note |
|---|---|---|
| Feeling of guilt | **0.53** (p<0.001) | dominates |
| Problems concentrating | 0.20 | |
| Overeating / appetite | 0.19 | |
| Bonding problems | 0.19 | |
| Irritable | 0.17 | |
| Suicide attempt item | 0.16 | |
| Age | 0.16 (n.s.) | |
| Trouble sleeping | 0.05 (n.s.) | |
| **Feeling sad or tearful** | **0.05 (n.s.)** | |

Red flags a Q1 reviewer will raise immediately:

1. **Inverted guilt relationship ◆.** P(anxious | guilt = No) = **0.81**; P(anxious | guilt = Yes) = **0.20**. Guilt and anxiety are positively comorbid in the perinatal literature; an inverse relationship this strong suggests label/code inversion, unreliable responses, or generated data.
2. **"Sad/tearful" is unrelated to anxiety (V = 0.05).** Core depressive affect carrying no information about anxiety is atypical for real symptom data.
3. **One feature carries the model.** Guilt alone (one-hot LR) gives CV ROC-AUC **0.775**; Random Forest *without* guilt drops from 0.83 to **0.70** ◆.
4. **"Suicide attempt" is not a screening predictor.** It is a sensitive past-behaviour/ideation item with a third response "Not interested to say" (29 % of unique rows ◆) — an informative-missingness category that is being encoded as a number.
5. **Item semantics are inconsistent:** "Trouble sleeping" has levels {No, Yes, *Two or more days a week*}; "Overeating or loss of appetite" has {No, Yes, *Not at all*}; "Concentrating" has {No, Yes, *Often*}. Different frequency scales are mixed inside nominal columns, and "Overeating *or* loss of appetite" is a double-barrelled item.
6. **Age bins 25–50 only** (no <25, none >50) with 45–50 as a bin — unusual for a postpartum sample; no parity, delivery mode, time since birth, social support, or history. Postpartum timing is unknown, so "early screening" cannot be tested at all.
7. **No site, country, or ethics statement** is recorded in the file.

## 4. Does the dataset support the three claims in the title?

| Claim in title | Supported? | Why |
|---|---|---|
| "Early" screening | **No** | No time variable; no prospective outcome; cross-sectional symptoms reported *concurrently with* the label |
| Postpartum **depression** | **No** | No depression instrument/label. A "Feeling sad" item is a *feature*, not an outcome |
| Postpartum **anxiety** | **Weakly / only as a single item** | The target is one self-reported item, not a validated anxiety construct (GAD-7/STAI/PASS) |
| **Risk stratification** | **Not clinically** | Tiers could only be probability bands for *"answers Yes to the anxious item"*. No outcome exists against which tiers can be validated |
| "Explainable ensemble" | Yes, technically | But explanations are explanations of an item-to-item association, not of clinical risk |
| "Comparative benchmark" | **Yes — this is the defensible part** | Provided uncertainty is honestly quantified at n ≈ 326 |

## 5. Notebook audit (cell-level)

| # | Issue | Severity | Evidence |
|---|---|---|---|
| N1 | **Mode imputation on the full data before the train/test split** (cell 5) | Low–medium (leakage of a global statistic; 27 cells) | cell 5 |
| N2 | Imputation happens *before* deduplication, so imputed values create/merge duplicate patterns | Low | cell 5 |
| N3 | **`astype('category').cat.codes` on every column** (cell 6) imposes arbitrary *alphabetical* ordinal codes on nominal categories (e.g. "Maybe"<"No"<"Yes"; "No"<"Not interested to say"<"Yes"). Linear/SVM/LR models read these as ordered distances | **High** for LR/SVM; moderate for trees. One-hot LR AUC (0.805) vs ordinal-code LR (0.703) ◆ — the *baseline itself is handicapped by the encoding* | cell 6; ◆ |
| N4 | Target `Feeling anxious` is encoded by the same blanket loop; relies on alphabetical coding (No=0, Yes=1) | Fragile | cell 6–7 |
| N5 | **Single 80/20 split, 66 test rows** (cell 10). RF test accuracy ranges **0.667–0.864 across 200 seeds** (mean 0.765) ◆. One split cannot rank models | **High** | ◆ |
| N6 | "Best model" (Random Forest) is declared **after viewing test-set results** (cells 16, 19, 21) → selection bias | High | cells 16–21 |
| N7 | Hyper-parameters are hand-set (`max_depth=4`, `lr=0.03`, `max_depth=2`) with no documented tuning protocol | Medium | cells 12–15 |
| N8 | Metrics reported as point estimates; **no confidence intervals, no significance tests, no repeated CV** | High | cell 16 |
| N9 | CV (cell 16) is run on `X_train` only but the already-imputed global data; the ensemble re-fits already-fitted base models (harmless) | Low | cell 15–16 |
| N10 | "Recall 37/38" for RF (cell 21) coupled with accuracy ≈ 0.77 implies the model predicts the majority class ("Yes") for almost everyone at threshold 0.5; high recall here is a **base-rate artefact**, not discriminative skill. *Verify in a clean run: report specificity.* | High (interpretation) | cell 21 |
| N11 | No specificity, MCC, PR-AUC, Brier, calibration, or decision curves in the notebook (calibration and SHAP plots existed only in the other notebooks `c_project`, `1-project`, `2-project`) | Medium | cell 16 |
| N12 | "Test patients" cell (20) reports a single "confidence %" from an uncalibrated RF — presented as patient-level risk | Medium (clinical over-claim) | cell 20 |
| N13 | Title/markdown language ("Early Screening and Risk Stratification of Postpartum Anxiety and Depression") is not supported by the code, which only predicts one anxiety item | **High** | cell 0 |
| N14 | No SHAP, no LIME, no ablation in `main-projects.ipynb`; no seeds for libraries beyond `random_state=42`; no environment pin | Medium | whole notebook |
| N15 | Three duplicate CSVs and four notebooks with overlapping content — risk of reporting results from the wrong version | Housekeeping | file tree |

## 6. Class imbalance

58 % positive / 42 % negative among unique rows (189 vs 137 ◆). This is **mild** imbalance. SMOTE/ADASYN is **not justified**; with n = 326 and categorical features, synthetic oversampling would mostly manufacture more near-duplicates. Use stratification, class weights, and threshold analysis; treat resampling as a *sensitivity analysis* only (and only inside training folds).

## 7. Sample-size sanity check

137 minority-class events versus ≈ 18–20 one-hot parameters → events-per-parameter ≈ 7, below the ≥ 10 rule of thumb and below what Riley et al.'s criteria (BMJ 2020) would typically demand for stable development. Formal calculation (R `pmsampsize` or equivalent) should be reported. The conclusion to expect: **the dataset is too small to support confident model *ranking*, which is itself a publishable finding if quantified.**

## 8. Sanity checks that *passed*

- Shuffled-label control: Random Forest ROC-AUC **0.435** (≈ chance) ◆ — the pipeline is not leaking a label by construction after deduplication.
- Grouping CV by timestamp gives RF AUC 0.834 ± 0.073 vs 0.830 ± 0.058 for random CV ◆ — timestamp clustering did not obviously inflate the *deduplicated* result, but this does not exclude replicated-with-perturbation rows.
- Dedup-only dummy classifier accuracy 0.58 (majority rate) ◆; real models beat it (RF CV AUC ≈ 0.83) — **there is genuine item-to-item signal, but it is concentrated in one inverted-looking item.**

## 9. Bottom line

The strongest honest reading: *"a small, replicated, unvalidated symptom-checklist dataset in which one symptom item (anxiety) can be predicted from the others, mainly through a single, clinically counter-intuitive item (guilt)."* It supports a **methodological** thesis (rigorous benchmarking, uncertainty, calibration, XAI stability, data-validity auditing). It does **not** support clinical claims about depression, early screening, or risk tiers. See `02_title_and_research_direction.md`.
