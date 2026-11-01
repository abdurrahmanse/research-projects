# 02 · Research Title Evaluation and Problem Statement

## 1. Evaluation of the current title
> "Early Screening and Risk Stratification of Postpartum Depression and Anxiety Using Explainable Ensemble Machine Learning: A Comparative Benchmark"

| Criterion | Assessment |
|---|---|
| Scientific accuracy | **Low.** Depression: no label. Early: cross-sectional. Risk stratification: not implemented. Explainable: not in core notebook. Ensemble: no demonstrated benefit |
| Originality | Low as worded: "explainable ensemble ML for PPD" is a crowded phrase [L10, L13, L9, L15] |
| Specificity | Poor: names five concepts, none operationalised |
| Clinical relevance | Good topic; claims exceed evidence |
| Dataset compatibility | **Incompatible** with "depression" and "early" |
| Methodological clarity | "Comparative Benchmark" is the strongest, honest part |
| Publication potential | Moderate if re-scoped; low if kept (reviewers will notice the mismatch) |
| Overstates contribution? | **Yes** |

## 2. Which concepts to emphasise
| Concept | Include? | Reason |
|---|---|---|
| Early screening | **No** | No timing information |
| Symptom screening | **Yes** | What the data support |
| Risk stratification | **Yes, as "calibrated risk tiers"** | Feasible; fills a gap (calibration rarely reported, see file 03 G4/G5) |
| Explainable AI | **Yes, evaluated** | Stability analysis differentiates from [L9, L10, L13, L15] |
| Hybrid/ensemble | **Yes, as hypothesis under test** | Not assumed beneficial |
| Comparative benchmark | **Yes** | Core |
| Multi-outcome | No | No validated second outcome |
| Calibration | **Yes** | Needed for tiers |
| Clinical decision support | **No** | Cannot be claimed |
| Robustness | **Yes, data-duplication robustness** | Unusual, honest |

## 3. Five improved titles (ranked)

Scoring: 1–5 on Relevance (R), Novelty potential (N), Feasibility (F), Clarity (C), Publication potential (P).

| Rank | Title | R | N | F | C | P | Total |
|---|---|---|---|---|---|---|---|
| **1** | **Calibrated and Explainable Ensemble Learning for Symptom-Based Screening of Postpartum Anxiety: A Leakage-Aware Comparative Benchmark** | 5 | 4 | 5 | 4 | 4 | **22** |
| 2 | How Much Does Duplication Inflate Postpartum Mental-Health Classifiers? A Leakage-Aware Benchmark of Ensemble Models on a Public Survey Dataset | 4 | 5 | 5 | 4 | 4 | 22 |
| 3 | Towards a Minimal, Explainable Self-Report Screener for Postpartum Anxiety Symptoms: Benchmarking Machine-Learning and Ensemble Models | 5 | 3 | 5 | 5 | 4 | 22 |
| 4 | Risk-Tiered Screening of Postpartum Anxiety Symptoms from Self-Reported Questionnaires: Calibration and Decision-Curve Evaluation of Tree-Ensemble and Stacked Models | 4 | 4 | 4 | 3 | 4 | 19 |
| 5 | Explainable Ensemble Machine Learning for Postpartum Anxiety Symptom Screening and Risk Stratification: A Comparative Benchmark (original, narrowed) | 4 | 2 | 5 | 4 | 3 | 18 |

## 4. Recommendation
**Retitle to #1:**
> *Calibrated and Explainable Ensemble Learning for Symptom-Based Screening of Postpartum Anxiety: A Leakage-Aware Comparative Benchmark*

Rationale:
- "**Symptom-based screening**" matches the data (current symptoms, no timing).
- "**Postpartum anxiety**" is acceptable in a title if the abstract states it means a *self-reported anxious-feeling item*; if your supervisor demands precision use "anxiety symptoms".
- "**Calibrated**" and "**Leakage-aware**" are the actual methodological differentiators (see `10`).
- "**Explainable**" is retained because file 09 *evaluates* explanations.
- "**Ensemble**" stays because ensembles are the object of comparison, not asserted superior.
- "**Comparative Benchmark**" is retained from the original title.
- It removes: depression, early, clinical-decision-support.

Alternative: if provenance investigation shows the 1,503 rows are genuine independent responses, title #3 becomes more attractive (minimal screener). If they prove to be replicated, title #2 becomes the strongest honest story.

**Do not** adopt any title that includes "depression" unless you obtain a validated depression label (e.g., EPDS), which this dataset lacks.

## 5. Research problem statement (draft)
Postpartum mood and anxiety symptoms are common, under-detected, and screened by brief self-report instruments. Published machine-learning studies report high discrimination for postpartum depression, but (i) most use internal validation only, (ii) calibration and clinical utility are rarely reported, (iii) explanation methods are typically presented without any test of their stability, and (iv) public survey datasets are sometimes analysed without examining duplication or provenance, which can inflate reported accuracy [L2, L10, L11, L17; see file 03 for evidence per claim]. Using a public self-report survey of 1,503 responses, this research asks whether tree-based, linear and ensemble learners can screen for a self-reported anxious-feeling item from eight other symptoms and age band, **under evaluation conditions that control duplication-driven leakage, quantify uncertainty, calibrate probabilities for tiered use, and test whether explanations are stable**, and whether any ensemble provides gains over the strongest simple baseline.

## 6. Positioning
**Chosen:** *Comparative methodological benchmarking with exploratory retrospective screening-model development.*
Not: clinical prediction-model development; not clinical decision support. Rationale in `11` §2.
