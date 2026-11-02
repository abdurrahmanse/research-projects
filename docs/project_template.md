# Project template

Copy this layout when starting a new project (`NN-short-topic-name/`).

```
NN-short-topic-name/
├── README.md          # abstract, research questions, method, results, limits, how to reproduce
├── requirements.txt   # pinned library versions
├── data/
│   ├── raw/           # original files, never edited
│   ├── processed/     # (optional) generated, can be rebuilt
│   └── DATA_CARD.md   # source, licence, ethics, known issues
├── notebooks/         # numbered: 01_..., 02_...; paths relative to this folder
├── src/               # (optional) reusable .py code once notebooks grow
├── results/           # tables and figures written by the notebooks
├── research_plan/     # audit, literature review, hypotheses, methodology, thesis outline
├── reports/           # PDF or Word summaries
└── archive/           # earlier experiments, kept unchanged
```

Checklist for a new project: add its row to the root README table, fix random seeds, record library versions, write the DATA_CARD before modelling.
