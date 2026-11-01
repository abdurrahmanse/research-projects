# 10 · Originality and Novel Contributions

## 1. Honest starting point
- "Explainable ensemble ML for PPD" is **not novel**: stacking/voting + SHAP + calibration curves exist for EPDS-defined PPD [L15]; SHAP + tiering + temporal validation exist [L13]; SHAP + XGBoost are common [L9, L10].
- Same-dataset work [L16, L17] exists, so even the dataset is not new.
- No source I verified evaluates: duplicate-driven leakage on this kind of survey data; explanation **stability**; formal tests of ensemble gain vs best single learner; a minimal-item screener — for an anxiety-symptom label.
- Absence of evidence in a limited, non-systematic search is not proof of novelty. Confirm with the systematic search in `14`.

## 2. Contribution assessment

| Proposed contribution | Research gap | Existing work | Methodological difference | Required evidence | Feasibility | Novelty confidence |
|---|---|---|---|---|---|---|
| **C1. Leakage-aware benchmark quantifying duplication inflation** | G9 | [L10] CV on whole dataset; [L17] 96.99% with no validation described on the same data | Three arms (naive / group-aware / de-duplicated), identical models, paired inflation estimates | ΔAUC (naive − group) with CI across models; label-conflict statistics | **High** | **Medium** (leakage is known; quantifying it on this dataset family is unreported to my knowledge) |
| **C2. Calibration-aware risk-tier evaluation with DCA** | G4, G5, G11 | [L15] calibration; [L13] K-means tiers; [L9, L10] DCA | Calibrate inside CV, pre-specify tier cut-offs by sensitivity/PPV targets, test monotone observed risk, DCA | Tier table with CIs; DCA plot; calibration table | **High** | **Low–Medium** (new application of established techniques) |
| **C3. Explanation-stability analysis across folds and model families** | G6 | SHAP shown once per paper [L5, L9, L10, L13, L15] | Rank-stability metrics, cross-model agreement, grouped importance for correlated items | τ and Jaccard distributions meeting pre-set thresholds, or demonstration of instability | **High** | **Medium** (new combination; stability for tabular health data discussed in XAI literature generally, not for PPD in my search) |
| **C4. Minimal-item screener** | Practical gap (workload) | Not found for this label | Nested-CV item-reduction with non-inferiority test (H7) | Reduction curve; non-inferiority CI | **High** | **Low–Medium** |
| **C5. Formal test of ensemble benefit vs strongest simple baseline, with diversity and complexity analysis** | G1, G8 | [L4] stacked ensemble not chosen; [L15] ensembles reported | Corrected paired tests, diversity diagnostics, cost–benefit; null result allowed | ΔAUC CIs, diversity metrics | **High** | **Medium** |
| C6. Robustness to label noise and encoding | RQ2, RQ8 | Rare | Noise injection, encoding sensitivity | Decay curves | Medium | Low–Medium |
| ~~C7. New hybrid architecture~~ | — | — | — | — | — | **Not claimed.** Combining standard learners is a *new combination at best*, and without superiority evidence it is not a contribution |

## 3. Classification of contributions
| Category | Items |
|---|---|
| Established techniques | LR, RF, GB, SVM, SHAP, Platt/isotonic, DCA, nested CV |
| New application of established techniques | C2, C4 on this label/data type |
| New combination of established techniques | C1 (3-arm leakage design), C3, C5 |
| Genuinely novel methodological contribution | **None claimed** |

## 4. Positioning of the work
The strongest potential is as a **benchmark/methodological study** ("what do you actually learn from this kind of public survey dataset, and how reliable is it?"), with C1 + C3 + C5 as the core. A clinical-application framing is not defensible (single undocumented source, symptom-item label, no external validation).

## 5. Claims you may and may not make
| May | May not |
|---|---|
| "We provide a leakage-aware benchmark …" | "First study to …" without systematic search evidence |
| "Ensembles did / did not improve over X (Δ, CI)" | "Our hybrid model outperforms existing studies" |
| "Calibrated probabilities enabled exploratory tiers" | "Clinically validated risk categories" |
| "Top items were stable/unstable across folds" | "These symptoms cause / predict postpartum anxiety clinically" |
| "Accuracy on this dataset ranged …" | Comparing your accuracy with [L10]'s 0.955 AUC or [L17]'s 96.99% as if equivalent |

## 6. What would make the contribution stronger
1. Resolve provenance (changes everything).
2. Add a second public dataset with similar items for pseudo-external validation (even a different population, if documented).
3. Pre-register hypotheses and thresholds (dated commit).
4. Release code, config, and fold-level predictions.
5. Systematic literature search with PRISMA flow.
6. Collaboration with a perinatal clinician to justify the cost ratio and tier definitions.
