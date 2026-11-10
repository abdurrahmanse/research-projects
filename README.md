# Research Projects

A portfolio of self-contained machine-learning research projects. Each project lives in its own numbered folder with its own data, notebooks, results, plan and environment, so projects never interfere with each other.

**Author:** Abdur Rahman · **Focus:** interpretable machine learning, leakage-aware evaluation, health-related survey data

---

## Projects

| # | Project | Question | Main result | Status |
|---|---|---|---|---|
| 01 | [Interpretable postpartum anxiety symptom screening with a hybrid ensemble and explainable AI](01-postpartum-anxiety-cgth/) | Which of five algorithms predicts a self-reported anxiety item best without leakage, and do SHAP and LIME explain it the same way? | Hybrid Ensemble ranks first: balanced accuracy 77.2%, ROC-AUC 0.843 (not significantly above random forest); SHAP and LIME agree (Spearman 0.98) | Analysis complete |

Each project README holds the abstract, method, results, limitations and reproduction steps.

## Repository layout

```
research-projects/
├── README.md                      # this file: portfolio index
├── docs/
│   └── project_template.md        # layout and checklist for a new project
├── 01-postpartum-anxiety-cgth/    # project 01
│   ├── README.md
│   ├── requirements.txt
│   ├── data/                      # raw data (read-only) and data card
│   ├── notebooks/                 # the study notebook
│   ├── results/                   # tables and figures
│   └── research_plan/             # audit, literature, method, thesis outline
└── 02-…/                          # future projects follow the same layout
```

## Working principles

These apply to every project here.

- **No leakage.** Duplicates are removed before any split. Imputation, encoding and tuning are learned inside training folds only.
- **Hypotheses before results.** Settings, margins and tests are fixed before the main run.
- **Uncertainty is reported.** Repeated cross-validation with corrected confidence intervals, not a single split.
- **Honest scope.** Claims match what the data supports. Negative and weakened results are reported.
- **Raw data is read-only.** Cleaning happens in code, and every dataset has a data card with its source, licence and known issues.
- **Reproducible.** Fixed seeds and pinned library versions per project.

## Running a project

Each project has its own environment. For project 01:

```bash
cd 01-postpartum-anxiety-cgth
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cd notebooks && jupyter lab final_thesis_study.ipynb     # Run All
```

## Adding a new project

1. Copy the layout from [docs/project_template.md](docs/project_template.md) into a new folder named `NN-short-topic-name`.
2. Write the `data/DATA_CARD.md` before modelling.
3. Add a row to the project table above.
4. Remove superseded experiments once a final notebook replaces them; they stay recoverable in git history.

## Data and ethics

Some datasets here contain sensitive self-reported health information. Results are research findings, not clinical tools, and must not be used for individual diagnosis. Check each dataset's licence (see its data card) before redistributing it.
