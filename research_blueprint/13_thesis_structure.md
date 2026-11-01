# 13 · Thesis Structure and Publication Roadmap

(Outline only. No chapter text drafted.)

| Chapter | Content | Evidence / analyses needed | Outputs |
|---|---|---|---|
| **1 Introduction** | Postpartum mood/anxiety burden; screening practice (EPDS [L20]); ML promise; problem statement (`02` §5); gaps G1–G12 summary; aim, objectives, RQs; contributions (`10`); scope & positioning | Verified epidemiology citations (**not yet gathered**: do a targeted search for postpartum anxiety prevalence/guidelines) | Problem statement, contribution list |
| **2 Literature review** | 2.1 Postpartum mental health screening (EPDS, GAD-7, limits); 2.2 ML for PPD/PPA (L1–L19); 2.3 Ensemble learning & stacking theory; 2.4 Calibration and decision-curve analysis; 2.5 XAI in health ML; 2.6 Methodological quality (PROBAST/TRIPOD+AI, leakage); 2.7 Same-dataset studies (L16, L17); 2.8 Gap synthesis | Systematic search with PRISMA flow; full-text verification of all cited numbers | T3, T4 |
| **3 Methodology** | Dataset & data card; audit; outcome construct; arms; preprocessing; models; ensembles; nested CV; tuning; metrics; calibration; tiers; DCA; XAI; statistics; ethics; reproducibility | Frozen protocol & hypotheses file (dated) | F1–F7, T1, T2, T5 |
| **4 Results** | 4.1 Data audit results; 4.2 Leakage arms (H5); 4.3 Baselines & advanced models (H1); 4.4 Ensembles (H2) & diversity; 4.5 Ablations; 4.6 Calibration (H3); 4.7 Tiers & DCA (H8); 4.8 Explainability & stability (H6); 4.9 Item reduction (H7); 4.10 Subgroup/robustness | All experiments run once, results saved with manifest | F8–F28, T6–T16 |
| **5 Discussion** | Interpretation vs hypotheses (including null results); why ensembles did/didn't help (diversity); comparison with literature **qualitatively** (never numerically across different outcomes); contributions revisited; limitations (`11` §8); practical implications; threats to validity | Literature table; limitations ledger | T19 |
| **6 Conclusion & future work** | Direct answers to RQs; what was learned; future: provenance clarification, external validation, EPDS/GAD-7 reference standard, prospective study, fairness audit | — | — |
| Appendices | TRIPOD+AI checklist; hyperparameter spaces; full results; reproducibility instructions; environment | — | T17, T18 |

## Paper structure (journal / conference)
1. **Title** (`02` option 1 or 2).
2. **Abstract** (structured: Background, Objective, Methods, Results, Conclusions; state the construct limitation).
3. **Introduction** (≈4 paragraphs: burden → ML literature and its weaknesses → gap → contributions).
4. **Related work** (short; L-matrix condensed).
5. **Data and audit** (include duplication findings).
6. **Methods** (arms, nested CV, models, ensembles, calibration, XAI, statistics).
7. **Results** (leakage, benchmark, ensembles, calibration/tiers, XAI stability, minimal screener).
8. **Discussion** (interpretation, limits, ethical considerations).
9. **Conclusion**.
10. **Data/code availability** and **ethics statement**.
11. **Supplement** (ablations, extra plots, TRIPOD+AI).

**Target venues** (suggestions to check for scope, indexing and fees; verify before submitting): open-access applied-AI-in-health journals, biomedical-informatics journals (JMIR family, BMC Medical Informatics and Decision Making, Frontiers in Digital Health), and workshop/conference tracks on trustworthy ML for healthcare. A leakage-focused framing may also suit methodological/reproducibility tracks.

## Thesis-writing timeline suggestion (relative)
Weeks 1–2: provenance, data card, systematic search. 3–4: protocol freeze + implement pipeline. 5–7: experiments. 8–9: XAI/tier/DCA. 10–12: writing. Adjust to your calendar.
