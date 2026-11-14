<div align="center">

# Research Projects

**Reproducible, leakage-aware machine-learning studies for health and public-sector data**

Every project is designed to be inspectable, reproducible, and honest about uncertainty.

<a href="https://github.com/abdurrahmanse/research-projects">
  <img src="https://img.shields.io/badge/research-reproducible-2563eb?style=for-the-badge" alt="Reproducible research">
</a>
<a href="https://github.com/abdurrahmanse/research-projects/blob/main/docs/CONSTITUTION.md">
  <img src="https://img.shields.io/badge/evaluation-leakage--aware-0f766e?style=for-the-badge" alt="Leakage-aware evaluation">
</a>

</div>

---

## About

This repository is a portfolio of self-contained research projects by **[Abdur Rahman](https://github.com/abdurrahmanse)**. The work focuses on interpretable machine learning, leakage-resistant evaluation, and responsible analysis of health-related survey and public-sector data.

The goal is not to produce impressive-looking scores. The goal is to make each result traceable to code, uncertainty-aware, and appropriately scoped.

## Projects

| # | Project | Research question | Key result |
|:--:|---|---|---|
| 01 | [Postpartum anxiety screening with an explainable hybrid ensemble](01-postpartum-anxiety-xai-hybrid/) | Which of seven models predicts a self-reported anxiety item best, and do SHAP and LIME explain the hybrid in the same way? | **98.67%** test accuracy (95% CI **97.3–99.7%**); **84.7%** on unseen answer patterns |
| 02 | [County-level severity mix of VA disability compensation](02-va-disability-county-severity/) | How much does the share of recipients rated 70%+ vary across US counties, and can it be predicted in an unseen state? | **R² 0.41** with random folds; **0.34** with state-grouped folds |
| 03 | [Monthly crime-report forecasting for LAPD areas](03-lapd-area-crime-forecasting/) | Can past reports forecast next-month area counts without temporal leakage, and what happens at the 2024 reporting-system transition? | Transparent 3-month mean wins; 2023 **MAE 48.98**, **WAPE 5.26%**; 2024 shift more than doubles MAE |

Each project contains its own abstract, research plan, data card, notebooks, results, limitations, and reproduction instructions.

## Research standards

These projects follow the repository's [Research Tutor Constitution](docs/CONSTITUTION.md):

- **Leakage-aware evaluation** — duplicates are counted, and duplicate-aware validation is reported beside standard validation.
- **Hypotheses before results** — settings, margins, and statistical tests are specified before the main run.
- **Uncertainty, not single splits** — repeated cross-validation and corrected confidence intervals are preferred.
- **Honest scope** — negative, weakened, and inconclusive results remain visible.
- **Read-only raw data** — cleaning happens in code; every dataset has a data card.
- **Reproducibility by default** — fixed seeds and pinned dependencies are maintained per project.

## Quick start

Each project is isolated and has its own environment:

```bash
cd 01-postpartum-anxiety-xai-hybrid
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Open the project's notebook in `notebooks/` and run it from top to bottom. For the autonomous evidence workflow, see the [agent guide](agent/README.md).

## Repository layout

```text
research-projects/
├── 01-postpartum-anxiety-xai-hybrid/
├── 02-va-disability-county-severity/
├── 03-lapd-area-crime-forecasting/
├── agent/                 # autonomous literature and evidence workflow
├── docs/                  # constitution, templates, and notebook guidance
└── tools/                 # notebook builders and source checks
```

Every project follows the same core structure:

```text
project/
├── README.md
├── requirements.txt
├── data/                  # read-only raw data and DATA_CARD.md
├── notebooks/
├── results/
└── research/
```

## Start a new project

1. Copy the structure from [`docs/project_template.md`](docs/project_template.md).
2. Write the dataset data card before modelling.
3. Define the research question, hypotheses, metric, and validation strategy.
4. Add the project to the table above.
5. Keep all project-specific code, data documentation, and results inside its project directory.

## Responsible use

Some datasets contain sensitive self-reported health information. These studies are for research and education, not clinical decision-making or individual diagnosis. Review the relevant data card and licence before using or redistributing any project data.

## Contributing

Issues and pull requests are welcome. Please keep changes focused, preserve reproducibility, and follow the research standards above. For substantial changes, open an issue first so the intended research or engineering scope is clear.

## Contact

Review each project's data card before using or redistributing its data. If this work is useful, a ⭐ on [GitHub](https://github.com/abdurrahmanse/research-projects) helps others discover it.
