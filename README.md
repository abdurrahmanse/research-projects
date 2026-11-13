# Research Projects

Self-contained, leakage-aware machine-learning studies on health-related survey data, built to be reproduced and honestly scoped. Every number in a project README traces to code output or a results file.

**Author:** Abdur Rahman

## Projects

| # | Project | Question | Headline result |
| --- | --- | --- | --- |
| 01 | [Postpartum anxiety screening with an explainable hybrid ensemble](01-postpartum-anxiety-xai-hybrid/) | Which of seven models predicts a self-reported anxiety item best, and do SHAP and LIME explain the hybrid the same way? | 98.67% test accuracy (95% CI 97.3–99.7%), but 84.7% on unseen answer patterns |
| 02 | [County-level severity mix of VA disability compensation](02-va-disability-county-severity/) | How much does the share of recipients rated 70%+ vary across US counties, and can it be predicted in an unseen state? | R² 0.41 with random folds, 0.34 with state-grouped folds |

Each project README has the abstract, method, results, limitations and reproduction steps.

## Principles

- **No hidden leakage:** duplicates are counted, and duplicate-aware validation is reported beside the standard one.
- **Hypotheses first:** settings, margins and tests are fixed before the main run.
- **Uncertainty reported:** repeated cross-validation with corrected confidence intervals, never a single split.
- **Honest scope:** negative and weakened results are reported.
- **Read-only raw data:** cleaning happens in code, and each dataset has a data card.
- **Reproducible:** fixed seeds and pinned versions per project.

Full rules: [docs/CONSTITUTION.md](docs/CONSTITUTION.md).

## Quick start

```bash
cd 01-postpartum-anxiety-xai-hybrid
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Then open the notebook in `notebooks/` and Run All. Each project has its own environment.

## Layout

```text
research-projects/
├── NN-short-topic-name/   # one folder per project
│   ├── README.md · requirements.txt
│   ├── data/              # read-only raw data + DATA_CARD.md
│   ├── notebooks/ · results/ · research/
├── agent/                 # autonomous research agent (see agent/README.md)
├── docs/                  # constitution, project template, notebook skeletons
└── tools/                 # notebook builder and source-check hooks
```

## Contributing

Issues and pull requests are welcome. For a new project, copy the layout in [docs/project_template.md](docs/project_template.md), write the data card before modelling, and follow the principles above. Keep changes within one project per pull request.

## Data and ethics

Some datasets contain sensitive self-reported health information. Results are research findings, not clinical tools, and must not be used for individual diagnosis. Check each data card's licence before redistributing data.

## Support

If you find this work useful, a ⭐ on [GitHub](https://github.com/abdurrahmanse/research-projects) helps others discover it.
