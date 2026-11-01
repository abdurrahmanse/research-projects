# Research Blueprint — Postpartum Anxiety-Symptom Screening with Explainable Ensemble ML

Research-planning package for `projects/main-projects.ipynb`. **Nothing here is an experimental result.** All numbers are either (a) computed directly from the CSV, (b) read from the existing notebook's printed outputs, or (c) quoted from verified papers with their source. Result tables are empty templates.

## Headline conclusions (read this first)
1. **The original title overclaims** (depression, early prediction, risk stratification, explainability are not supported by the current data/notebook). Recommended replacement: see `02`.
2. **The dataset has provenance and duplication problems** (1,503 rows → 326 unique answer patterns; undocumented origin). This is the single largest threat to validity, but also a publishable angle: *quantifying leakage inflation*.
3. **The most defensible positioning** is *comparative methodological benchmarking + exploratory retrospective screening-model development*, **not** clinical prediction-model development.
4. **No claim of superiority over published accuracy figures** is possible (different data/outcomes/validation). Claims must rest on rigor, calibration, explanation stability and honest null results.

## Files
| # | File | Content |
|---|---|---|
| 01 | [project_dataset_audit](01_project_dataset_audit.md) | Dataset + notebook audit; confirmed vs hypothesised vs unsupported |
| 02 | [research_title_and_problem](02_research_title_and_problem.md) | Title evaluation, 5 ranked titles, problem statement |
| 03 | [literature_review_and_research_gaps](03_literature_review_and_research_gaps.md) | 20-paper verified matrix, 12-gap analysis |
| 04 | [research_objectives_questions_hypotheses](04_research_objectives_questions_hypotheses.md) | Aim, objectives, RQs, hypotheses with tests and decision rules |
| 05 | [model_selection_and_justification](05_model_selection_and_justification.md) | Candidate models, selection table |
| 06 | [hybrid_ensemble_architecture](06_hybrid_ensemble_architecture.md) | Ensemble design, diversity analysis, ablations |
| 07 | [experimental_methodology](07_experimental_methodology.md) | Leakage-safe protocol, workflow diagram, tuning |
| 08 | [evaluation_and_statistical_analysis](08_evaluation_and_statistical_analysis.md) | Metrics, calibration, risk tiers, DCA, valid statistical tests, result templates |
| 09 | [explainable_ai_framework](09_explainable_ai_framework.md) | XAI methods, stability analysis, interpretation limits |
| 10 | [novel_contributions](10_novel_contributions.md) | Honest novelty assessment |
| 11 | [clinical_ethics_and_limitations](11_clinical_ethics_and_limitations.md) | Clinical framing, fairness, ethics, TRIPOD+AI |
| 12 | [figures_and_tables_plan](12_figures_and_tables_plan.md) | Figure/table specifications |
| 13 | [thesis_structure](13_thesis_structure.md) | Chapter outline + paper structure |
| 14 | [implementation_roadmap](14_implementation_roadmap.md) | Staged coding plan, libraries, directory layout |
| 15 | [research_readiness_review](15_research_readiness_review.md) | Readiness scorecard + "what a critical reviewer would challenge" |
| — | [references](references.md) | Verification status of every source |

## Conventions
- **[C]** confirmed from data/notebook · **[H]** hypothesis needing verification · **[U]** unsupported assumption.
- **PAS** = *postpartum anxiety symptom* (the self-reported item "Feeling anxious"), deliberately **not** "postpartum anxiety disorder".
- "Unique pattern" = distinct combination of the 9 predictor answers + target.
- Citations use `[L#]` for the verified literature matrix (file 03) and `[M#]` for methodological references (file `references.md`).

## Open questions for you (answers change design decisions)
1. Where did the data come from? Can you contact the uploader/hospital? (determines whether 1,503 or 326 is the "real" N)
2. Do you have ethics approval/exemption language for secondary use of this dataset (university requirement)?
3. Does your supervisor require a depression outcome, or is an anxiety-symptom focus acceptable?
4. Master's or undergraduate thesis, and what is the page/time budget? (determines how many of the optional experiments to run)
5. Are you allowed to collect or obtain a second dataset (for external validation)?
