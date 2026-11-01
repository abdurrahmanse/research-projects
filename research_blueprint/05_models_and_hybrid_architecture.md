# 05 — Models and Hybrid Architecture

## Data facts that drive the choices
326 unique rows, 9 categorical predictors (about 28 one-hot columns), mild imbalance (58/42).

## Models used

| Model | Role | Why |
|---|---|---|
| Logistic regression | Transparent base model | Each decision can be explained with odds ratios; low variance at n = 326 |
| Random forest (300 trees, depth 4) | Strong base model | Best single model in the earlier benchmark (AUC 0.835); captures interactions between answers |
| Soft voting (mean of LR and RF) | Comparator hybrid | The standard way to combine two models; every decision is a blend |
| **CGTH** | **Proposed hybrid** | LR decides when confident; RF decides the rest |

## Why other models were dropped
An earlier, larger benchmark run in this project (same data and cross-validation; its notebook has since been removed) tested gradient boosting, soft voting and stacking; the original `main-projects.ipynb` also used SVM. None beat Random Forest (ROC-AUC 0.835): gradient boosting reached 0.813, voting 0.818 and stacking 0.821. Adding them would make the project larger without adding evidence. XGBoost, LightGBM and CatBoost were left out for the same reason, and deep learning because n is far too small.

## Architecture

```
          answers of one respondent
                     │
     preprocessing (imputation + one-hot, fitted on training fold)
                     │
          Logistic Regression  →  probability p
                     │
          is |p − 0.5| ≥ δ ?  (δ = 0.2)
            ┌────────┴────────┐
           yes                no
            │                  │
   final = LR decision    final = Random Forest decision
   (explained by odds      (uncertain cases only)
    ratios)
```

## Hybrid ideas tested and rejected (exploratory, report in the thesis)

| Idea | Result (ROC-AUC) | Why rejected |
|---|---|---|
| Tree-guided LR (decision-tree leaves added to LR) | 0.799–0.801 | No gain over LR (0.800) |
| LR with guilt interaction terms | 0.797 | No gain |
| Gated hybrid judged by AUC | 0.804–0.817 | Mixing probabilities lowers the ranking quality; decision metrics are the correct measure |

Reporting rejected ideas shows the method was not chosen by luck. It is good practice and costs one table.

## Robustness checks (replace the older ablation list)
| Check | Purpose |
|---|---|
| Duplicates kept | Shows leakage inflation |
| Guilt item removed | Shows dependence on one question |
| δ from 0 to 0.5 | Shows the full transparency–performance trade-off |
