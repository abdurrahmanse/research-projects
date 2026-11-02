# Research Projects

A collection of self-contained research projects. Each project lives in its own numbered folder with its own README, data, notebooks, results and environment, so projects never interfere with each other.

## Projects

| # | Project | Topic | Status |
|---|---|---|---|
| 01 | [postpartum-anxiety-cgth](01-postpartum-anxiety-cgth/) | Interpretable postpartum anxiety symptom screening with a confidence-gated hybrid (logistic regression + random forest) | Exploratory, in progress |

## Conventions

- One folder per project, named `NN-short-topic-name`.
- Every project follows the layout in [docs/project_template.md](docs/project_template.md).
- Raw data in `data/raw/` is read-only; cleaning happens in code.
- Each project pins its own library versions in `requirements.txt` and creates its own `.venv` (git-ignored).
- Earlier or abandoned experiments go to the project's `archive/`, not deleted.
