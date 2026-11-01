# 15 · Research Readiness Review

## 1. Scorecard (current state → state if this blueprint is executed)
| Criterion | Assessment now | Evidence | Remaining work | Projected |
|---|---|---|---|---|
| Scientific relevance | **Good** | Maternal mental health screening is an active field; many ML studies [L1–L15] | Add verified epidemiology & guideline citations | Good |
| Dataset suitability | **Weak–Moderate** | Single undocumented source; 78% duplicate patterns; single-item label; no timing; no validated depression label (`01`) | Provenance; data card; three-arm analysis | Moderate (for methodological work), weak (for clinical claims) |
| Research originality | **Low as titled**; Moderate if re-scoped | Explainable ensembles already published [L13, L15]; same-dataset papers exist [L16, L17] | Execute C1, C3, C5; systematic novelty check | Moderate |
| Methodological rigor | **Weak now** (single 66-case split, test-set selection, arbitrary encoding) | `01` §3 | Whole `07` protocol | Good |
| Model justification | **Partial** | 5 models, no rationale | `05`, `06` justifications + ablations | Good |
| Experimental validity | **Weak now** | Leakage routes; no CIs | Nested CV, groups, locked hold-out | Good |
| Explainability | **Absent in core notebook** | — | `09` incl. stability | Good |
| Clinical relevance | **Limited** | Symptom label; exploratory | Tiers + DCA framed as exploratory; clinician consult | Limited–Moderate |
| Reproducibility | **Weak now** | No env lock, hard-coded strings | `14` | Good |
| Publication potential | **Low now**; Moderate–Good for a leakage-aware benchmark paper | `10` §4 | Provenance, systematic search, second dataset (ideal) | Moderate |

## 2. Critical weaknesses
1. Dataset provenance/duplication unresolved.
2. Construct validity of the label.
3. Evaluation design in current notebook.
4. No external validation possible.

## 3. Necessary corrections (before any thesis claim)
Retitle; remove "depression", "early"; rebuild evaluation; explicit encoding; document data; add CIs; calibrate before tiering; evaluate explanations.

## 4. High-priority experiments
H5 (leakage arms) → H1/H2 (model & ensemble comparison) → H3 + H8 (calibration, tiers) → H6 (stability) → H7 (item reduction).

## 5. Unresolved research questions
- Are the 1,503 rows independent respondents? (Single most consequential unknown.)
- What does "Feeling anxious" correlate with in an independent validated instrument?
- Do findings hold in another population/dataset?
- What cost ratio would clinicians accept for tiers?

## 6. What a Critical Journal Reviewer Would Challenge About This Research

| # | Likely objection | Why it is valid | Defensible response / improvement |
|---|---|---|---|
| 1 | "The outcome is one self-reported item; this is not anxiety screening." | Construct validity | Reframe as symptom-item classification; state limitation in abstract; avoid diagnostic language; propose EPDS/GAD-7 validation as future work |
| 2 | "78% of rows are duplicates; the data may be synthetic or replicated." | Strong evidence in the CSV | Present as a finding; three-arm analysis; label-conflict and timestamp profile; contact source; make conclusions methodological |
| 3 | "No external validation; dataset origin unknown." | True | State explicitly; no generalisation claims; pseudo-external only; seek a second dataset |
| 4 | "Others report AUC > 0.9; yours is lower." | Different outcomes and designs | Explain non-comparability (`03` header); show that high figures on this dataset arise under unvalidated protocols (H5) |
| 5 | "Ensembles are standard; where is the novelty?" | `10` §1 | Emphasise formal tests, diversity analysis, null results, leakage inflation, stability; do not claim a new architecture |
| 6 | "Did the ensemble really beat the best single model?" | Notebook shows no gain | Pre-registered H2, corrected paired test, effect sizes; report null honestly |
| 7 | "Hyperparameter tuning leaked / model selected on test data." | Notebook did it | Nested CV, locked hold-out, frozen config hash |
| 8 | "n is tiny; CIs are huge." | n≈326 | Report CIs; avoid ranking within noise; emphasise effect sizes; learning curve |
| 9 | "SMOTE on categorical codes is invalid / done before CV." | Valid concern | Class weights default; SMOTE-NC only inside folds as ablation |
| 10 | "Ordinal coding of nominal answers distorts results." | Valid | Explicit mapping, one-hot, native categorical, encoding ablation A8 |
| 11 | "Probabilities not calibrated, yet tiers claimed." | Valid | Calibration inside CV; reliability + ICI; tiers exploratory |
| 12 | "SHAP shown without checks; correlated features; causal language." | Common flaw | Stability metrics, grouped permutation, guardrails (`09` §6) |
| 13 | "Decision-curve and cost ratio are arbitrary." | Valid | Sensitivity analysis over ratios; clinician input; label as illustrative |
| 14 | "Suicide item is unreliable and ethically sensitive." | Valid | Ablation A10; ethics paragraph; no prevalence claims |
| 15 | "Multiple testing; fold dependence invalidates p-values." | Valid | Corrected resampled t, Holm, effect sizes first |
| 16 | "Subgroup fairness not assessed." | Only age available | Report age-band results with CIs; state inability for other attributes |
| 17 | "Why not deep learning?" | Common question | Justified exclusion (`05` §2) with optional appendix MLP |
| 18 | "Code/data unavailable." | Reproducibility | Public repo, config, seeds, fold predictions, Zenodo DOI; licence check |
| 19 | "Literature coverage is not systematic." | True so far | PRISMA-style search; verified references only |
| 20 | "Positive-result bias: only best figures reported." | Common | Pre-registration; report all arms, all models, all ablations |

## 7. Ways to strengthen
Obtain provenance; add a second dataset; collaborate with a clinician; add a short expert-elicited cost ratio; run label-noise simulations; release a minimal reproducible package; consider a prospective EPDS/GAD-7 mini-study as a future-work design.

## 8. Final consistency review (done)
- Terminology: PAS / "anxious-feeling item" used consistently; no file claims depression prediction.
- Counts reconcile: 1,503 rows; 326 unique patterns; 1,177 duplicate rows; 65.2% vs 58.0% prevalence.
- Hypotheses H1–H8 in `04` map to ablations A1–A12 (`06`), tables (`08`, `12`) and stages (`14`).
- No experimental result was generated; metrics quoted from the notebook are labelled as single-split outputs.
- References: see `references.md` for verification status; items V2/V3 must be verified before citing.
