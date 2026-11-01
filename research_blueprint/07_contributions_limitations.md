# 07 — Contributions, Clinical Relevance, Limitations

## Contributions

| # | Contribution | Evidence (notebook task) |
|---|---|---|
| C1 | **CGTH**: a confidence-gated hybrid in which a transparent model decides confident cases and a random forest handles uncertain ones | Tasks 7, 9 |
| C2 | Evidence that CGTH is non-inferior to random forest while 68% of decisions stay with logistic regression | Tasks 10–11 |
| C3 | **Coverage** reported next to accuracy, plus a transparency–performance curve across δ | Task 12 |
| C4 | An explanation of why the gate works (LR accuracy on confident vs uncertain cases) | Task 13 |
| C5 | A data-quality audit of a public postpartum survey dataset: 78% duplicates, leakage inflation, single-item dependence | Tasks 4, 15 |

**How this differs from prior work:** the postpartum studies reviewed in doc 03 either use one model or blend models for every case (voting, stacking), and, as far as their abstracts show, none report how many decisions remain explainable by a simple model. Confirm this when reading the full papers.

**What is not new:** deferring uncertain cases to a stronger model (cascades, selective classification) is an existing idea in machine learning. Say so in the thesis; the novelty is its application and evaluation in this setting.

## Clinical relevance (honest)
Low on its own. The output predicts whether a respondent answers Yes to an anxiety item, given their other answers. The value is the design idea: a screening aid where most decisions can be explained in plain terms, which is easier to audit and to trust.

## Limitations
- No validated instrument and no clinical reference standard.
- Cross-sectional data: early screening cannot be tested.
- Provenance unclear; the data may be replicated or synthetic.
- n = 326 gives wide confidence intervals.
- δ = 0.2 was chosen after an exploratory look at a few values; the full δ curve is reported to offset this.
- CGTH has lower ROC-AUC than RF (0.809 vs 0.835) because of the probability mixing.
- Hyperparameters were fixed, not tuned.
- No external validation.

## Fairness
Age band is the only demographic variable. Report balanced accuracy per age band as a descriptive check (each band has about 40–75 unique rows). This is not yet in the notebook; see the roadmap.

## Publication potential
- **Thesis or student project:** strong, if the limitations above are written clearly.
- **Journal:** realistic only for a methods or open-data venue (for example *BMC Medical Informatics and Decision Making*, *PLOS ONE*, *JMIR Formative Research*), following TRIPOD+AI. A second dataset with a validated label is the main step that would strengthen a submission.
