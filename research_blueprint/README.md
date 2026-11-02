# Research Blueprint

**Title:** Interpretable Postpartum Anxiety Symptom Screening Using Confidence-Gated Hybrid Machine Learning

**Main notebook:** `projects/cgth_hybrid_study.ipynb` (22 tasks, one per cell; the dataset is only read). Outputs go to `projects/results_cgth/`.

**Method in one sentence:** logistic regression decides every case it is confident about (|p − 0.5| ≥ 0.2); only uncertain cases go to a random forest.

| File | Content |
|---|---|
| 01_project_dataset_audit.md | Dataset and original notebook audit |
| 02_title_and_research_direction.md | Title critique, alternatives, chosen direction |
| 03_literature_review_and_gaps.md | Verified sources and gap matrix |
| 04_objectives_questions_hypotheses.md | Problem, objectives, H1–H2, research questions |
| 05_models_and_hybrid_architecture.md | Models, CGTH architecture, rejected hybrid ideas |
| 06_methodology_evaluation_xai.md | Pipeline, metrics, statistics, explainability, figures |
| 07_contributions_limitations.md | Contributions, limitations, fairness, publication potential |
| 08_thesis_outline_roadmap_reviewers.md | Chapters, timeline, reviewer responses |
| 09_cgth_hybrid_methodology.md | One-page summary of the method and first-run results |

## First-run results (seed 42, 50 folds, 326 unique rows)

| Model | Balanced accuracy (95% CI) | ROC-AUC | Decided by LR |
|---|---|---|---|
| Logistic Regression | 0.730 [0.667, 0.794] | 0.800 | 100% |
| Random Forest | 0.761 [0.706, 0.816] | 0.835 | 0% |
| Soft Voting (LR + RF) | 0.741 [0.678, 0.804] | 0.820 | — |
| **CGTH (proposed)** | **0.757 [0.700, 0.813]** | 0.809 | **68%** |

H1 (non-inferior to RF): supported at fixed δ = 0.2, not established with δ chosen inside training folds (0.750, 77% decided by LR, p = 0.06). H2 (better than LR): not supported (p = 0.08).
