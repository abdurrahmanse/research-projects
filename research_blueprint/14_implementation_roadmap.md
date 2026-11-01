# 14 · Implementation Roadmap (for later coding by you)

Difficulty: E=easy, M=medium, H=hard. Priority: P0 must, P1 should, P2 optional.

## Stages
| # | Stage | Objective | Inputs | Algorithms / tools | Outputs | Validation checks | Depends on | Diff. | Pri. |
|---|---|---|---|---|---|---|---|---|---|
| 0 | Project setup | Reproducible environment | Repo | `uv`/`pip-tools` lock, `pre-commit`, config.yaml, seed utils | `pyproject.toml`, lock, `src/` skeleton | Fresh-clone run passes | — | E | P0 |
| 1 | Data card & provenance | Document source, hash, licence, answers | CSV; Kaggle page; uploader contact | `hashlib`, markdown | `DATA_CARD.md`; single canonical CSV | Hash matches; 3 CSV copies reconciled | 0 | E | P0 |
| 2 | Data audit | Duplicates, label conflict, missingness, timestamp profile | CSV | pandas | audit tables F3–F7 | Counts equal numbers in `01` (1,503/326/1,177) | 1 | E | P0 |
| 3 | Pre-registration | Freeze hypotheses/thresholds | `04`, `08` | Markdown + git tag | `PREREG.md` (dated commit) | Committed **before** stage 6 | 2 | E | P0 |
| 4 | Preprocessing module | Explicit mappings, pipelines | Mapping table | `ColumnTransformer`, `OrdinalEncoder`, `OneHotEncoder`, `SimpleImputer` | `preprocess.py` | Unit tests: mapping bijective; no unseen-level crash; fit only on train | 2 | M | P0 |
| 5 | Split framework | Arms N/G/D; outer/inner CV; locked hold-out | Data | `RepeatedStratifiedKFold`, `StratifiedGroupKFold`, group = pattern | `splits.py`, saved fold indices | Test asserting no shared pattern across train/test in arms G, D; class balance per fold | 4 | M | P0 |
| 6 | Baselines | Dummy, pattern-lookup, LR, NB, DT | Folds | scikit-learn | T-A | Dummy AUC≈0.5; pattern-lookup computed OOF only | 5 | E | P0 |
| 7 | Advanced learners + tuning | SVM, RF, ET, GB, XGB, CatBoost (± LightGBM) | Folds | scikit-learn, xgboost, catboost, (lightgbm), `optuna` or `RandomizedSearchCV` | T-B; tuning logs | Same budget per model; tuned params logged; no outer-fold peeking | 6 | M | P0 |
| 8 | Leakage experiment | H5 / RQ6 | Raw data | Same pipelines under arms N, G, D | T-F; F8 | N≥G expected but not assumed; CIs | 7 | M | P0 |
| 9 | Ensembles | E1–E5 | OOF predictions | `VotingClassifier`, `StackingClassifier` (group-aware inner CV), custom weighted vote | T-C; diversity (F17) | Meta-learner trained only on inner OOF; ensemble ≠ member check | 7 | H | P0 |
| 10 | Calibration & tiers | H3, H8, DCA | OOF probs | `CalibratedClassifierCV`, betacal (or custom), statsmodels, custom DCA | T-E, T-G; F13–F15 | Calibrators fit inner only; thresholds frozen from inner data | 9 | H | P0 |
| 11 | Statistics | Tests & CIs | Fold-level metrics | scipy, statsmodels, custom corrected t-test, DeLong implementation (verify against a reference, e.g., R `pROC`) | T-16; F19 | Re-implementations validated on synthetic data; Holm applied | 9 | M | P0 |
| 12 | Explainability | X1–X10 | Final/fold models | `shap`, `sklearn.inspection` (permutation, PDP/ICE), (optional `lime`) | F20–F24, T-J | Additivity check; stable seeds; background data from train fold | 9 | M | P1 |
| 13 | Ablations | A1–A12 | All above | Config-driven runner | T-D; F16 | Each ablation changes one factor; same folds | 7–12 | M | P1 |
| 14 | Item reduction | H7 | Models | SHAP-ranked forward selection / L1 inside CV | F25 | Selection inside outer folds | 12 | M | P1 |
| 15 | Subgroups & robustness | Fairness, label noise | Models | Age-band metrics, noise injection | T-I; F26; A12 | Report n per cell; flag underpowered | 9 | M | P1 |
| 16 | Locked hold-out evaluation | Final single estimate | Frozen final pipeline | — | Final table | Run once; hash of frozen config logged | all | E | P0 |
| 17 | Figures & tables | Publication assets | Results store | matplotlib, seaborn (dataviz skill available if desired) | F*, T* | Regenerate from one command | 6–16 | M | P1 |
| 18 | Systematic search & verification | Literature | — | PubMed/IEEE/Scopus + Zotero | PRISMA flow; verified refs | All cited numbers re-read in source | parallel | M | P0 |
| 19 | Release | Archive code/results | Repo | GitHub + Zenodo | DOI, README | Fresh-clone reproduces tables | all | E | P2 |

## Libraries (only those the methodology uses)
pandas, NumPy, scikit-learn (pipelines, CV, calibration, inspection), imbalanced-learn (SMOTE-NC ablation only, via its pipeline), XGBoost, CatBoost, LightGBM (optional), SHAP, Optuna (optional; `RandomizedSearchCV` is sufficient), SciPy and statsmodels (tests, bootstrap, trend test), matplotlib/seaborn (figures), `pyyaml`/`hydra` (config), `joblib`, `pytest`, `nbstripout` (clean notebooks), `mlflow` or plain CSV logs (optional). Not needed: deep-learning frameworks.
The existing `.venv` has pandas 3.1.0 and scikit-learn 1.9.1; pin the exact versions you use. **Check that shap/xgboost/catboost versions support these**, because very new pandas/scikit-learn releases may lag behind third-party packages.

## Suggested directory structure
```
research-projects/
├── research_blueprint/            # this planning package
├── projects/
│   ├── main-projects.ipynb        # preserved original
│   └── c_project.ipynb            # preserved
├── data/
│   ├── raw/postpartum_survey.csv  # single canonical copy + SHA256
│   └── DATA_CARD.md
├── configs/                       # experiment.yaml, search_spaces.yaml, mappings.yaml
├── src/ppa/
│   ├── data.py, mappings.py, audit.py
│   ├── splits.py                  # arms N/G/D, nested CV
│   ├── models.py, ensembles.py
│   ├── tuning.py, calibration.py, tiers.py
│   ├── metrics.py, stats.py       # bootstrap, corrected t, DeLong, DCA
│   ├── explain.py                 # SHAP, stability
│   └── plots.py
├── experiments/                   # one script/notebook per hypothesis H1–H8
├── results/                       # fold predictions, tables (parquet/CSV), run manifests
├── figures/
├── tests/                         # leakage, mapping, metric unit tests
├── PREREG.md
├── pyproject.toml + lock
└── README.md
```

## Notebook migration map (current → new)
| Current cell(s) | Keep? | New home |
|---|---|---|
| 0–4 imports, load, info | Keep idea | `data.py`, audit script |
| 5 impute/dedupe | Replace | `audit.py` + pipeline imputer; arms in `splits.py` |
| 6 `cat.codes` | Replace | `mappings.py` + encoders |
| 7–8 target plot, Pearson heatmap | Replace | F6, F7 (Cramér's V) |
| 9–10 split | Replace | `splits.py` |
| 11–15 five models | Keep as baselines/ensemble prototype | `models.py`, `ensembles.py` with tuning |
| 16 comparison table | Replace | `metrics.py` + T-A..T-C with CIs |
| 17–18 plots | Replace | `plots.py` (forest plots, ROC/PR) |
| 19–21 reports and hard-coded summary | Remove | auto-generated tables |
| 20 patient examples | Replace | `explain.py` local explanations from raw text input |
