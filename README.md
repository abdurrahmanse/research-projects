# Research Projects

A portfolio of self-contained machine-learning research projects. Each project lives in its own numbered folder with its own data, notebooks, results, plan and environment, so projects never interfere with each other.

**Author:** Abdur Rahman · **Focus:** interpretable machine learning, leakage-aware evaluation, health-related survey data

---

## Projects

| # | Project | Question | Main result | Status |
|---|---|---|---|---|
| 01 | [Explainable hybrid stacking ensemble for postpartum anxiety screening](01-postpartum-anxiety-xai-hybrid/) | Which of seven models predicts a self-reported anxiety item best, and do SHAP and LIME explain the hybrid the same way? | Hybrid Stack: test accuracy 98.67% (95% CI 97.3–99.7%), not significantly different from CatBoost or random forest; 84.7% on unseen answer patterns; SHAP more faithful than LIME | Analysis complete |
| 02 | [County-level severity mix of VA disability compensation](02-va-disability-county-severity/) | How much does the share of recipients rated 70%+ differ between US counties, and can age mix, female share and size predict it in an unseen state? | Pooled share 58.6%; county spread is 92% real, 63% of it between states; R² 0.41 with random folds but 0.34 with state-grouped folds | Analysis complete |

Each project README holds the abstract, method, results, limitations and reproduction steps.

## Repository layout

```
research-projects/
├── README.md                      # this file: portfolio index
├── docs/
│   └── project_template.md        # layout and checklist for a new project
├── 01-postpartum-anxiety-xai-hybrid/    # project 01
│   ├── README.md
│   ├── requirements.txt
│   ├── data/                      # raw data (read-only) and data card
│   ├── notebooks/                 # the study notebook
│   ├── results/                   # tables and figures
│   └── research/                  # literature review and research gaps
├── 02-va-disability-county-severity/    # project 02 (same layout, smaller)
└── 03-…/                          # future projects follow the same layout
```

## Working principles

These apply to every project here.

- **No hidden leakage.** Repeated rows are counted and a duplicate-aware validation is reported next to the standard one. Imputation, encoding and tuning are learned inside training folds only.
- **Hypotheses before results.** Settings, margins and tests are fixed before the main run.
- **Uncertainty is reported.** Repeated cross-validation with corrected confidence intervals, not a single split.
- **Honest scope.** Claims match what the data supports. Negative and weakened results are reported.
- **Raw data is read-only.** Cleaning happens in code, and every dataset has a data card with its source, licence and known issues.
- **Reproducible.** Fixed seeds and pinned library versions per project.

## Running a project

Each project has its own environment. For project 01:

```bash
cd 01-postpartum-anxiety-xai-hybrid
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cd notebooks && jupyter lab postpartum_anxiety_xai_study.ipynb     # Run All
```

## Adding a new project

1. Copy the layout from [docs/project_template.md](docs/project_template.md) into a new folder named `NN-short-topic-name`.
2. Write the `data/DATA_CARD.md` before modelling.
3. Add a row to the project table above.
4. Remove superseded experiments once a final notebook replaces them; they stay recoverable in git history.

## Data and ethics

Some datasets here contain sensitive self-reported health information. Results are research findings, not clinical tools, and must not be used for individual diagnosis. Check each dataset's licence (see its data card) before redistributing it.
