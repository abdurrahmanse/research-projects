# Research Projects: Agent Instructions

**Supreme rulebook: [docs/CONSTITUTION.md](docs/CONSTITUTION.md).** Read it before any research or coding task. Learner mode: notebooks are code cells only (no markdown); explain in the chat in Bengali, keep code minimal, never invent results.

Portfolio of self-contained ML research projects (`NN-short-topic-name/`). Author: Abdur Rahman. Focus: interpretable ML, leakage-aware evaluation, health-related survey data.

## Non-negotiable research rules
1. **No hidden leakage.** Count duplicates; report duplicate-aware validation next to the standard one. Imputation, encoding, scaling and tuning are fit inside training folds only (use Pipelines).
2. **Hypotheses before results.** Write settings, margins and tests down before the main run.
3. **Report uncertainty.** Repeated CV with corrected confidence intervals, never a single split.
4. **Honest scope.** Claims must match the data. Report negative and weakened results.
5. **Raw data is read-only.** Never edit files in `data/`. Clean in code. Every dataset needs a data card (source, licence, known issues).
6. **Reproducible.** Fixed seeds, pinned versions in each project's `requirements.txt`.
7. **Never fabricate.** No invented citations, numbers, DOIs or results. Every reference must be verified (search/fetch) and every number traced to code output or a results file. If unverified, say so.

## Project layout
See `docs/project_template.md`. Each project: `README.md`, `requirements.txt`, `data/`, `notebooks/`, `results/`, `research/` (literature + gaps). Do not mix projects.

## Workflow
- Learn-while-researching on a dataset: `/study <dataset path> | <topic>` (uses `research-tutor`)
- New project: `/new-project <topic>`
- Literature: `/lit-review <topic>` (writes to the project's `research/`)
- Before claiming results: `/audit <project>` (leakage + stats + claims check)
- Writing up: `/write-up <project>`

- Autonomous run: `python agent/research_agent.py "<question>" --project <folder>` (see `agent/README.md`)

## Automatic guardrails (`.claude/settings.json` hooks)
- `guard_files.py` (before Write/Edit): blocks edits to `data/` and direct edits of `.ipynb`
- `check_notebook_source.py` (after Write/Edit of `notebooks/*.py`): flags unused imports, swallowed errors, silenced warnings, missing `random_state`, fitting on whole data, oversized cells, markdown cells or more than two comment lines per cell (notebooks are code-only), test set used in more than one cell
- Manual check: `/verify notebooks/<name>.py`
- Tooling environment: `pip install -r tools/requirements.txt`

## Skills (`.claude/skills/`)
`beginner-viz`, `model-selection`, `leakage-and-validation`. Notebook template: `docs/notebook_skeleton.py`.

## Subagents (`.claude/agents/`)
- `research-tutor`: builds beginner-friendly step-by-step notebooks from a dataset
- `literature-researcher`: finds and verifies sources, maps gaps
- `data-auditor`: data quality, leakage, duplicates
- `methods-reviewer`: critiques design and statistics like a hostile reviewer
- `report-writer`: turns verified results into README/paper prose

## Conventions
- Python, pandas/scikit-learn; notebooks run top-to-bottom with Run All.
- Figures saved to `results/`; tables as CSV.
- Cite as Author (Year) with DOI/URL in `research/references.md`.
- Commit only when asked.
