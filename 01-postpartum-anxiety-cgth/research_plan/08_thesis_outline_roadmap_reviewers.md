# 08 — Thesis Outline, Roadmap, Reviewer Criticisms

> **Earlier design.** This document describes the confidence-gated hybrid (CGTH) design. Task numbers refer to its notebook, which is kept in git history. The final study is described in `09_final_method_and_results.md`.

## Chapter outline
1. **Introduction:** postpartum mental health; the accuracy-versus-explainability problem in screening models; H1, H2 and the research questions.
2. **Literature review:** doc 03 table and gap matrix; short section on cascades and selective classification in machine learning.
3. **Data and audit:** source, items, duplicates, label plausibility (doc 01).
4. **Method:** preprocessing, base models, CGTH, validation, statistics (docs 05–06), and hybrid ideas that were tested and rejected.
5. **Results:** Tables 1–6 and the transparency–performance curve.
6. **Discussion:** what CGTH achieves (accuracy close to RF, 68–77% transparent decisions), what it does not (non-inferiority not established under the stricter test, no gain over LR proven, lower AUC), comparison with the literature.
7. **Limitations, ethics, fairness** (doc 07).
8. **Conclusion and future work:** a larger sample to settle non-inferiority, a second dataset, a validated label.
- **Appendix:** TRIPOD+AI checklist, notebook, library versions.

## Roadmap

| Week | Task | Output |
|---|---|---|
| 1 | Read prior work on the same Kaggle dataset (doc 03, row 17); confirm the licence | Notes |
| 1 | Run `cgth_hybrid_study.ipynb` Tasks 1–5 | Data audit table |
| 2 | Run Tasks 6–11 | Results table, hypothesis tests |
| 2 | Run Tasks 12–22 | Transparency curve, gate check, odds ratios, robustness, stricter tests, age bands, train vs test, ceiling |
| 3 | Decide on a second dataset (doc 02 §4) | Go/no-go |
| 4 | Sample-size justification (Riley et al. 2020) | Methods paragraph |
| 5–8 | Writing | Chapters |

## Likely reviewer criticisms and responses

| Criticism | Response |
|---|---|
| "The dataset is unreliable." | Agreed. The audit quantifies this, and robustness checks show its effect (Task 15). |
| "No clinical label, so this is not screening." | Agreed. All wording says "screening support for a self-reported item". |
| "Cascades are not new." | Correct. The contribution is applying and measuring a transparent-first cascade in this setting, including coverage. |
| "δ was tuned on the results." | Disclosed. Tasks 17 and 19 choose δ inside training folds; the result weakens to p = 0.06, and the thesis reports this. |
| "CGTH has lower AUC than RF." | Reported. CGTH is a decision rule, so balanced accuracy is primary; the AUC drop comes from mixing probabilities. |
| "CGTH is not better than LR." | H2 was pre-stated and not supported (p = 0.08); this is reported as a result. |
| "Why only LR and RF?" | The earlier benchmark showed no gain from boosting or stacking (doc 05). |
| "Results not reproducible." | Fixed seed, fixed settings in Task 2, library versions printed, all results saved to CSV. |
