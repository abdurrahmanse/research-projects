# 05 · Model Selection and Scientific Justification

## 1. Dataset properties that drive model choice
- n ≈ 326 unique patterns (1,503 raw rows); events ≈ 137–189 per class.
- 9 **categorical** predictors with 2–5 levels; the **entire input space is finite** (≤ 32,805 combinations). Any flexible model effectively learns a table of *pattern → label rate*. Therefore expect models to **converge to similar performance**, bounded by label noise.
- Mild imbalance (58–65% positive).
- Inputs contain a mix of nominal and (arguably) ordinal answers.
- Small n ⇒ high variance, so low-variance / regularised models and repeated CV matter more than architectural sophistication.

Implication: model complexity beyond a few interactions is unlikely to help; the scientific value is in *demonstrating* that, with calibrated uncertainty.

## 2. Candidate assessment

Legend — Imb: sensitivity to imbalance; Over: overfitting risk at n≈300; Int: interpretability; Role: B=baseline, P=primary candidate, E=ensemble component, X=excluded/optional.

| Model | How it works (brief) | Why it may suit | Strengths | Weaknesses | Complexity | Imb | Over | Int | Clinical applicability | Role |
|---|---|---|---|---|---|---|---|---|---|---|
| **Dummy (prior/stratified)** | Predicts class prior | Floor | Defines "no skill" | — | O(1) | — | — | High | — | **B** |
| **Pattern-lookup baseline** | Empirical label rate per exact answer pattern (with Laplace smoothing) | Finite input space; gives an *oracle-style ceiling* for what any learner can extract | Shows irreducible noise; makes "ML beats chance" meaningful | Cannot generalise to unseen patterns (back off to LR) | O(n) | Low | High in-sample, evaluate out-of-fold only | High | — | **B** |
| **Logistic Regression (L2/elastic net)** | Linear log-odds over one-hot items | Small n, categorical, transparent; well-calibrated by construction; standard in screening scores | Stable, calibrated, coefficients = odds ratios | No interactions | O(nd) | Medium (class weights) | Low | **Very high** | Highest (can become a score) | **B / E** |
| **Decision Tree** | Recursive partitions | Interpretable rules | Rules clinicians can read | High variance | O(nd log n) | Medium | High | High | Rule display | **B (interpretability reference)** |
| **Naive Bayes (categorical)** | Conditional independence of items | Natural for questionnaire items; often competitive at small n (to be tested, not assumed) | Fast, robust | Independence violated by correlated symptoms; probabilities extreme | O(nd) | Low | Low | High | Fair | **B / E** (diverse) |
| **k-Nearest Neighbours (Hamming/Gower)** | Votes of nearest patterns | Finite discrete space | Simple | Distance on mixed ordinals arbitrary; poor scaling | O(n) predict | Medium | Medium | Medium | Low | **X (optional)** |
| **SVM-RBF** | Max-margin in kernel space | Used in most PPD papers [L1, L2, L6] | Handles non-linearity | Scale/encoding sensitive; needs probability calibration; opaque | O(n²–n³) | Medium | Medium | Low | Low | **P (benchmark continuity)** |
| **Random Forest** | Bagged randomised trees | Non-linear, robust, repeated top performer in reviews [L11, L6] | Low tuning burden; OOB estimate | Probabilities biased toward 0.5 → needs calibration | O(T·n log n) | Medium (balanced RF) | Low–Med | Medium | Good | **P / E** |
| **Extra Trees** | Randomised-threshold forests | Even lower variance on small n | Fast; smooth probabilities | Same calibration issue | O(T·n) | Medium | Low | Medium | Good | **P / E (diversity vs RF)** |
| **Gradient Boosting (sklearn HistGB/GB)** | Sequential additive trees | Standard strong tabular learner | Strong accuracy | Needs shallow depth/early stopping at n≈300 | O(T·n·d) | Medium | **Med–High** | Medium | Good | **P** |
| **XGBoost** | Regularised gradient boosting | Used in best-reported PPD studies [L9, L10] | Regularisation, missing-value handling | Many hyperparameters; one-hot needed | O(T·n·d) | Medium (scale_pos_weight) | Medium | Medium + SHAP | Good | **P (literature-comparable)** |
| **LightGBM** | Histogram boosting, leaf-wise | Fast; categorical support | Speed | Leaf-wise growth overfits tiny data | O(T·n·d) | Medium | **High at n≈300** | Medium | Good | **Optional** (test whether it adds anything beyond XGBoost) |
| **CatBoost** | Ordered boosting, native categorical handling | Pure-categorical inputs; ordered target statistics reduce leakage and small-data overfit | Best-in-class for small categorical data; strong defaults | Slower; tooling heavier | O(T·n·d) | Medium | Low–Med | Medium + SHAP | Good | **P (best-motivated advanced model for this data)** |
| **MLP** | Feedforward NN | Only to complete the literature comparison [L7 includes MLP] | — | n≈300, finite input space: no representational need; unstable | O(epochs·n·params) | Medium | **High** | Low | Low | **X** (explicitly excluded; justify in text; optional appendix) |
| Deep tabular (TabNet etc.) | Attention-based | — | — | Data-hungry | — | — | Very high | Low | Low | **X** |

## 3. Selected set (manageable and purposeful)

| Group | Models | Experimental purpose |
|---|---|---|
| Reference | Dummy; Pattern-lookup | Skill floor; ceiling/noise |
| Interpretable baselines | LR (L2 and elastic net); Decision Tree; Categorical NB | RQ1/H1 baselines; transparency; diversity |
| Classical ML (literature continuity) | SVM-RBF; Random Forest; Extra Trees | Comparable to [L1, L2, L6, L11] |
| Boosting | sklearn GB / HistGB; XGBoost; CatBoost | Modern strong learners; H1 |
| Optional | LightGBM | Only if adding no cost; else exclude and say why |
| Ensembles | Soft vote; weighted soft vote; stacking (LR meta) | H2; see file 06 |
| Excluded | kNN, MLP, deep tabular | Not justified by data; state reasons |

That is **~10 individual + 3 ensemble models**, a manageable count. Every one maps to a hypothesis or to continuity with the literature.

## 4. Encoding strategy (affects model choice)
| Encoding | Models | Notes |
|---|---|---|
| One-hot | LR, SVM, NB (via CategoricalNB can use ordinal codes), XGBoost | Default for linear/kernel models |
| Ordinal (explicit mapping) | Trees, GB | Only where order is defensible (e.g., No < Sometimes/Maybe < Yes) |
| Native categorical | CatBoost, LightGBM | Avoids arbitrary codes |
| Sensitivity analysis | All | Re-run main table with alternative encodings; report change (RQ2) |

Define the answer-scale mapping table once in the data card, e.g.: Feeling sad: No=0, Sometimes=1, Yes=2; Sleep: No=0, "Two or more days a week"=1, Yes=2 (**assumption** — "Yes" vs "Two or more days a week" ordering is ambiguous; test both orders and one-hot). "Not interested to say" in the Suicide item should be its **own nominal category**, not an ordinal midpoint.

## 5. Role of each class of metrics in model choice
Choose the **final** model by nested-CV outer-fold AUC, with ties (within 1 SE) resolved in favour of the simpler/more interpretable model (one-standard-error rule). This operationalises "simplicity unless proven otherwise".
