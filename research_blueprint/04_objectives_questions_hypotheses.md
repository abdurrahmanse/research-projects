# 04 — Problem, Objectives, Questions, Hypotheses

## Research problem
In mental-health screening, simple models are easy to explain but less accurate, and complex models are more accurate but harder to explain. Usual hybrids such as voting and stacking blend both models for every person, so no individual decision stays simple to explain. It is unknown whether a hybrid that lets a transparent model decide most cases can keep the accuracy of a complex model on postpartum survey data.

## Objectives
- **O1** Audit the dataset for duplicates, missing values and label plausibility.
- **O2** Build the Confidence-Gated Transparent Hybrid (CGTH) from logistic regression and random forest.
- **O3** Compare CGTH with LR, RF and soft voting under leakage-free repeated cross-validation.
- **O4** Measure how many decisions the transparent model makes (coverage) and how this trades off against accuracy.
- **O5** Explain the transparent decisions with odds ratios.
- **O6** Test robustness to duplicate leakage and to removing the dominant question.

## Questions and hypotheses (fixed before the main run)

| ID | Question | Hypothesis | Test | Notebook task |
|---|---|---|---|---|
| H1 | Is CGTH as good as RF? | CGTH balanced accuracy is non-inferior to RF (margin 0.03) | One-sided corrected paired t-test | 11 |
| H2 | Is CGTH better than LR? | CGTH balanced accuracy > LR | One-sided corrected paired t-test | 11 |
| RQ3 | How much transparency can be kept? | Coverage of LR at δ = 0.2 is reported with accuracy | Descriptive, δ curve | 10, 12 |
| RQ4 | Why does the gate work? | LR accuracy is lower on uncertain cases than RF accuracy on those cases | Descriptive | 13 |
| RQ5 | Do duplicates inflate results? | Balanced accuracy is higher when duplicates are kept | Rerun with duplicates | 15 |
| RQ6 | How much do models rely on the guilt item? | Removing guilt lowers balanced accuracy for all models | Rerun without the item | 15 |

Primary metric: **balanced accuracy**, because CGTH is a yes/no decision rule and the classes are 58/42. ROC-AUC is reported as a secondary metric.

## First-run answers
H1 supported (−0.005, p < 0.001). H2 not supported (+0.026, p = 0.08). Coverage 68%. Gate check: LR 0.81 on confident cases, 0.61 on uncertain ones; RF 0.71 on uncertain ones. Duplicates kept: 0.84–0.86. Without guilt: about 0.60 for all models.
