# 09 — Proposed Method: Confidence-Gated Transparent Hybrid (CGTH)

Notebook: `projects/cgth_hybrid_study.ipynb`. This replaces the larger benchmark design in docs 05–06 as the main study; those docs remain as background.

## Idea
1. Logistic Regression (LR) is fully transparent: each decision can be explained by its odds ratios.
2. Random Forest (RF) is more accurate but harder to explain.
3. **CGTH:** LR decides every case where its probability is far from 0.5 (|p − 0.5| ≥ δ). Only uncertain cases are passed to RF.

Goal: keep RF-level decision accuracy while most decisions stay explainable by a simple model.

## Why it is a reasonable hybrid for this data
The audit showed LR is reliable when confident and weak near 0.5, which is where RF does better. This is measured in the notebook (Task 13).

## Novelty, stated honestly
Model cascades and "defer when uncertain" designs already exist in machine learning. The contribution here is applying a transparent-first cascade to postpartum survey screening and reporting **coverage** (the share of decisions made by the transparent model) next to accuracy. None of the postpartum depression ML studies reviewed in doc 03 report this.

## Hypotheses (primary metric: balanced accuracy)
- **H1:** CGTH is non-inferior to RF (margin 0.03).
- **H2:** CGTH is better than LR.

## First-run results (50 folds, corrected 95% CI)
| Model | Balanced accuracy | ROC-AUC | Decided by LR |
|---|---|---|---|
| Logistic Regression | 0.730 [0.667, 0.794] | 0.800 | 100 % |
| Random Forest | 0.761 [0.706, 0.816] | 0.835 | 0 % |
| Soft Voting (LR + RF) | 0.741 [0.678, 0.804] | 0.820 | — |
| **CGTH, δ = 0.2** | **0.757 [0.700, 0.813]** | 0.809 | **68 %** |

- **H1 supported:** −0.005 vs RF, one-sided p < 0.001.
- **H2 not supported:** +0.026 vs LR, p = 0.08. Report this as "no significant evidence".
- **Why the gate works:** LR accuracy is 0.81 on confident cases vs 0.61 on uncertain ones; RF reaches 0.71 on the uncertain ones.
- **Leakage:** keeping duplicates inflates balanced accuracy to 0.84–0.86 for every model.
- **Guilt dependence:** without the guilt item, every model falls to about 0.60.

## Added results (Tasks 16–18)
- **δ chosen inside each training fold (Task 17):** balanced accuracy 0.750 [0.687, 0.813], LR coverage 77%. The chosen δ ranged 0–0.30, mostly 0.10–0.20.
- **Screening at 90% sensitivity (Task 18):** specificity LR 0.496, RF 0.558, CGTH 0.509. At this operating point RF gives the fewest false alarms.
- **Performance ceiling:** tuned RF, Extra Trees, SVM, HistGradientBoosting, categorical naive Bayes, k-NN and class balancing all reached 0.69–0.77 balanced accuracy (exploratory runs, not in the notebook). About 0.76 is the ceiling for this dataset without leakage.

## Limitations to state in the thesis
- The main δ = 0.2 was chosen after an exploratory check of δ = 0.1, 0.2 and 0.3. Task 17 addresses this by choosing δ inside each training fold, and the full δ curve (Task 12) is reported.
- ROC-AUC of CGTH (0.809) is lower than RF (0.835), because mixing two models' probabilities blurs the ranking. CGTH is a decision rule, so decision metrics are primary; AUC is still reported.
- The data limitations in doc 01 still apply: a single self-reported item as the label, 78 % duplicates, and an implausible guilt association.
