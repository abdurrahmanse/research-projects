# Data card: postpartum_depression.csv

| | |
|---|---|
| Source | Kaggle, *PostPartum Depression* (uploader `parvezalmuqtadir2348`) |
| Size | 1,503 rows, 11 columns (timestamp, age band, 9 survey items) |
| Target used | `Feeling anxious` |
| Provenance | Undocumented; a third-party listing describes a hospital questionnaire collected via Google Forms |
| Licence / ethics | **Unverified.** Checked 2026-11-10: the Baselight mirror has shut down and gts.ai does not state a licence. Open the Kaggle page itself and record the licence here before redistributing |
| Prior use | Nayee et al. 2026 (ICSUMMIT, doi 10.2991/978-94-6239-727-9_19) report 96.99% accuracy on a 1,503-entry Kaggle dataset, very likely this one; the final notebook (Tasks 30–32) shows random forest reaches 98.8% only when duplicates are kept, and 76.0% on unique rows |
| Known issues | 27 missing cells; 78% duplicate rows (326 unique answer patterns); only 90 distinct timestamps; implausible inverse guilt-anxiety association |
| Handling | Raw file is never modified. Deduplication happens in the notebook, before any split |
| Sensitivity | Contains self-reported mental-health items, including a suicide-related question. Not for individual clinical use |

Full audit: `../research_plan/01_project_dataset_audit.md`.
