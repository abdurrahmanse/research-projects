# 06 · Hybrid / Ensemble Research Design

**Principle:** ensembles are a *hypothesis*, not a result. The existing notebook's own soft-voting model equalled its Gradient Boosting member (identical printed metrics), which is a warning that diversity may be low.

## 1. Why ensembles might help here
Ensemble gain requires members that are (i) individually better than chance, (ii) wrong on *different* cases [M: Kuncheva & Whitaker 2003], and (iii) combined without overfitting the combiner. With a finite categorical input space and n≈300, all flexible learners approximate the same pattern→rate table, so (ii) is doubtful. The research question is whether any measurable gain exists beyond noise.

## 2. Candidate architectures
| ID | Architecture | Base learners | Combiner | Rationale for complementarity | Main risk |
|---|---|---|---|---|---|
| E1 | Soft voting (equal) | LR + RF + CatBoost | Mean probability | Linear additive + bagged interactions + ordered boosting | Averages poorly calibrated probabilities |
| E2 | Weighted soft voting | LR + ExtraTrees + CatBoost + XGBoost | Weights learned on **out-of-fold** inner-loop predictions (e.g., constrained non-negative log-loss minimisation) | Down-weights redundant members | Weight overfitting at n≈300 → use few weights/regularise |
| E3 | Heterogeneous stacking | LR, NB, RF, CatBoost, SVM | **LR (L2) meta-learner** on OOF probabilities (logit-transformed) | Meta-learner can correct member miscalibration | Meta overfit; use inner CV for OOF, keep meta simple |
| E4 | Calibration-aware ensemble | E1/E3 + Platt/isotonic on ensemble output | Post-hoc calibrator trained in inner loop | Targets H3 | Calibration data scarcity (isotonic overfits at n<~1000 → prefer Platt/beta) |
| E5 | Feature-selection hybrid | Filter/embedded selection (mutual information, L1) → boosted trees | — | Tests "hybrid = selection + classifier" used in L1/L17-style papers, **selection inside CV** | Selection bias if done outside folds |
| E6 | Blending | As E3 with a fixed hold-out for the meta-learner | Same | Cheaper | Wastes scarce data → **not recommended** |
| E7 | Hard voting | As E1 | Majority | Included only for completeness | Discards probabilities → cannot support tiers |

Recommended minimal set: **E1, E2, E3, E4 (on the winner of E1–E3), E5**; E6/E7 dropped or relegated to an appendix with justification.

## 3. Diversity and complementarity analysis (required)
Computed on out-of-fold predictions, per repeat:
1. **Pairwise error correlation** (phi/Yule's Q) between base learners.
2. **Disagreement rate** and **double-fault rate** [M: Kuncheva & Whitaker 2003].
3. **Probability correlation** (Spearman) and **Brier decomposition** (reliability/resolution).
4. **Oracle upper bound**: fraction of cases at least one learner gets right.
5. **Effective ensemble size** (e.g., from eigenvalues of the error-correlation matrix).
6. Link outcome: plot ΔAUC(ensemble − best member) against mean error correlation.

Interpretation rules:
- Mean pairwise phi > 0.9 ⇒ members redundant; expect no ensemble gain.
- If double-fault ≈ individual error ⇒ ensemble cannot fix errors.
- Report these *even when* the ensemble helps.

## 4. Preventing leakage and meta-overfit
| Step | Rule |
|---|---|
| OOF generation | Within each **outer** training fold, run an **inner** stratified group K-fold to produce OOF probabilities for every training row |
| Meta-learner / weights | Fit only on those OOF probabilities of the outer training fold |
| Base-learner refit | After meta fit, refit each base learner on the full outer training fold; predict outer test fold |
| Test data | Never used for weights, thresholds, calibration or feature selection |
| Meta-learner capacity | L2 logistic regression (≤ k+1 parameters); no tree meta-learner |
| Equal tuning | Same inner-search budget for singles and ensemble components |
| Nested evaluation | Ensemble selection (E1 vs E2 vs E3) happens inside the inner loop, otherwise winner's curse |

Implementation tip: scikit-learn's `StackingClassifier(cv=...)` produces OOF predictions for the meta-learner internally, but **group-awareness must be passed through** (use a `StratifiedGroupKFold` splitter object), and the whole object must sit inside the outer CV.

## 5. Calibration effects
Voting averages probabilities, which typically *shrinks* extremes and may help or hurt calibration; stacking with LR can recalibrate. Compare uncalibrated vs Platt vs isotonic vs beta for each of: best single, E1, E3. Report ICI, slope, Brier, reliability curves (file 08).

## 6. Cost–benefit
For every model record: training time, inference time, number of parameters/trees, model size, number of hyperparameters tuned, and **a performance gain per unit complexity** summary. Decision rule: adopt an ensemble only if H2's support criterion is met *and* the added complexity is acceptable (stated up-front: e.g., training time ≤ 10× the best single learner).

## 7. Mandatory ablation studies
| # | Ablation | Compared arms | What it demonstrates | Metric focus |
|---|---|---|---|---|
| A1 | Individual base learners | All singles | Which family is best; whether complexity helps | AUC, Brier |
| A2 | Simple voting | E1 vs best single | Whether equal averaging helps | ΔAUC, ΔBrier |
| A3 | Weighted voting | E2 vs E1 | Whether learned weights add anything or just overfit | ΔAUC, weight stability |
| A4 | Stacking | E3 vs E2 | Meta-learning vs fixed averaging | ΔAUC, ΔBrier |
| A5 | Feature selection on/off | With vs without (selection inside CV) | Whether fewer items hurt (links to RQ7) | ΔAUC, item count |
| A6 | Imbalance handling | none / class-weight / SMOTE-NC / threshold | H4 | Sens@spec, PR-AUC, MCC |
| A7 | Calibration on/off | raw / Platt / isotonic / beta | H3 | Brier, ICI, slope |
| A8 | Encoding | ordinal vs one-hot vs native categorical | RQ2: robustness to arbitrary coding choice | ΔAUC |
| A9 | Data arm | naive-raw vs group-aware raw vs de-duplicated | H5/RQ6 leakage inflation | ΔAUC, Δacc |
| A10 | Suicide-item on/off | with/without | Dependence on sensitive/low-quality item; screening feasibility | ΔAUC |
| A11 | Proposed pipeline vs strongest simple baseline | Final selected pipeline vs tuned LR | The headline question: was complexity worth it? | ΔAUC with CI |
| A12 | Label-noise injection | flip 5/10/20% labels | Robustness of each model family | AUC decay slope |

Each ablation is a controlled single-factor change; run on identical outer folds to enable paired comparison.

## 8. What to do if the ensemble does not help
State: "Under these data, the ensemble did not improve on X (ΔAUC = …, 95% CI …)." Then use the diversity analysis to explain why (redundant errors, finite input space, label noise). This is a legitimate contribution to the benchmarking literature, particularly since L15/L4 reported ensembles without testing superiority formally.
