# Data card: postpartum_depression.csv

| | |
|---|---|
| Source | Kaggle, *PostPartum Depression* (uploader `parvezalmuqtadir2348`), https://www.kaggle.com/datasets/parvezalmuqtadir2348/postpartum-depression |
| Collection | Per the Kaggle listing: questionnaire given through a Google Form at a medical hospital |
| Size | 1,503 rows, 11 columns (timestamp, age band, 9 survey items) |
| Target used | `Feeling anxious` (Yes / No) — the target named on the Kaggle listing |
| Licence | Listed as MIT in a web search result for the Kaggle page (checked 2026-11-11). **Open the Kaggle page yourself and confirm before submission** |
| Missing values | 27 cells (Irritable 6, Concentration 12, Guilt 9); treated as their own "No answer" category |
| Repeated rows | 1,177 of the 1,503 rows repeat an earlier answer pattern; 326 patterns are unique. See notebook Tasks 6, 54 and 55 |
| Prior use | Lilhore et al. 2024 (99.6%), Raza et al. 2024 (99%), Nayee et al. 2026 (96.99%); see `research/01_literature_review.md` |
| Sensitivity | Self-reported mental-health items, including a suicide-related question. Not for individual clinical use |
| Handling | The raw file is never modified; all cleaning happens in the notebook |
