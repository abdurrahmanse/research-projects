# County-Level Severity Mix of VA Disability Compensation

**Status:** analysis complete, revised after an independent audit and methods review ([results/audit.md](results/audit.md)) · **Last run:** 2026-11-12 · **Author:** Abdur Rahman

## Abstract

This small project uses a county-level table of US veterans' disability compensation recipients (3,144 counties, 6.2 million recipients), split by disability rating band, age band and sex. The source and year of the file are unconfirmed (see [data/DATA_CARD.md](data/DATA_CARD.md)), so every statement about VA ratings is conditional on that. It studies one outcome: the **high-rating share** of a county, i.e. the proportion of its recipients rated 70% or higher. In the 2,674 counties kept for analysis (99.4% of recipients; counties with fewer than 62 recipients or hidden cells are left out) the pooled share is **58.6%**, but it ranges from about 40% to 66% between counties (5th to 95th percentile). This spread is much larger than the variance expected if every county shared one rate (standard deviation 8.1 points against 2.2). About 63% of the variance lies between states (95% CI 50% to 71%; Minnesota 37.9%, North Carolina 66.0%). A county's age mix, female share and size predict the share with **R² = 0.41 under random cross-validation and 0.34 when whole states are held out** (both counting every county equally; weighting counties by recipients gives 0.53 and 0.47). The gap of 0.07 (95% CI 0.05 to 0.09) is the part of the apparent accuracy that comes from having neighbouring counties of the same state in training. When a whole Census region is held out, accuracy falls much further (gradient boosting R² −0.13 counting counties equally, 0.22 recipient-weighted). The findings are descriptive: they are associations between county-level shares, not explanations of why states differ.

## Research questions

| | Question | Answer |
|---|---|---|
| RQ1 | How much does the high-rating share differ between counties and states? | A lot. County SD is 8.1 points against 2.2 expected if all counties shared one rate (chi-square p < 0.001). 63% of the variance is between states |
| RQ2 | Is it related to age mix, female share and county size? | Yes for age mix and female share; no association with size once the others are held fixed. The signs survive within states, with smaller coefficients |
| RQ3 | Can those features predict the share in an unseen state? | Partly: R² 0.34 (0.47 recipient-weighted), mean error 5.25 points against 6.53 for the baseline. Random folds overstate this (R² 0.41). Held-out Census regions are predicted much worse |

The three expectations stated in the notebook before the results were produced (more variation than chance, at least one feature related to the share, grouped folds scoring lower than random folds) all held. They are weak and unsurprising expectations, and the repository has no timestamp proving they were written first, so the findings below should be read as descriptive. No hypothesis test was pre-registered.

## Results

### RQ1 — Variation

| | |
|---|---|
| Pooled high-rating share | 58.6% |
| County shares: 5th percentile / median / 95th percentile | 39.5% / 55.8% / 66.2% |
| Observed SD of county shares | 8.1 points |
| SD expected from chance alone | 2.2 points |
| Variance beyond what one common rate would give (a rough ceiling for R²; unweighted, approximate) | 92.4% |
| Variance lying between states (unweighted η² of 51 states, includes binomial noise) | 63.3% (95% CI 49.9% to 71.2%, [table_11](results/table_11_bootstrap_ci.csv)) |
| Lowest states | Minnesota 37.9%, Nebraska 44.9%, Indiana 45.4% |
| Highest states | North Carolina 66.0%, Texas 65.4%, Nevada 65.1% |

![County distribution](results/fig_01_county_distribution.png)

All states are ranked in [results/fig_02_state_ranking.png](results/fig_02_state_ranking.png) and [results/table_03_state_high_share.csv](results/table_03_state_high_share.csv).

### RQ2 — Related features

| County feature | Spearman ρ (95% CI) | Linear model: points per 1 SD, other features fixed (95% CI) |
|---|---|---|
| Share aged 17–44 | +0.18 (0.04 to 0.30) | −3.5 (−4.9 to −2.2) |
| Share aged 65 or older | −0.44 (−0.54 to −0.32) | −5.7 (−8.0 to −3.3) |
| Share female | +0.49 (0.36 to 0.59) | +2.0 (1.0 to 3.1) |
| County size (log recipients) | +0.17 (0.06 to 0.28) | 0.0 (−0.7 to 0.9) |

Confidence intervals resample whole states (2,000 cluster-bootstrap resamples).

- Counties with an older recipient population have a lower high-rating share; counties with more female recipients have a higher one.
- The 17–44 share changes sign between the two columns. Alone it is weakly positive; with the 65+ share held fixed, a higher 17–44 share means a lower 45–64 share, and the result is negative. Read together, the two age coefficients say the high-rating share is highest where the **45–64 group** is largest.
- County size has no association with the share once age and sex mix are accounted for.
- The two age shares are strongly correlated, so their coefficients should be read together, not one at a time.
- **Within states** (outcome and features de-meaned by state, [table_19](results/table_19_within_state_coefficients.csv)) the signs are unchanged and the effects smaller: 17–44 share −1.9 (−2.6 to −1.2), 65+ share −3.2 (−3.9 to −2.3), female share +1.3 (0.8 to 1.7), county size +0.3 (−0.1 to 0.7) points per 1 SD. Part of the pooled association therefore runs through which states have which age and sex mix.

![Feature scatter](results/fig_03_feature_scatter.png)

### RQ3 — Prediction and fold design

| Predictor | R², random folds | R², state-grouped folds | Mean error, state-grouped (points) |
|---|---|---|---|
| Overall average (baseline) | 0.00 | −0.05 | 6.53 |
| State average (no county feature) | 0.62 | −0.05 | 6.53 |
| Linear regression | 0.38 | 0.33 | 5.30 |
| Gradient boosting | 0.41 | 0.34 | 5.25 |

Mean of 10 repeats of 5-fold cross-validation. The grouped score was lower than the random score in all 10 repeats for both models.

- A state-average lookup scores R² 0.62 under random folds only because other counties of the same state are in training. For an unseen state it falls back to the overall mean and equals the baseline. This shows strong clustering by state; it does not show that the state carries more information than the features. With state indicators in the model (random folds), adding the four features raises R² from 0.62 to 0.72 (recipient-weighted: 0.41 to 0.76), so the features add information within states ([table_18](results/table_18_fixed_effects_cv.csv)).
- Gradient boosting is not distinguishable from linear regression: the grouped R² difference is 0.010 (95% CI −0.032 to 0.048, state bootstrap; corrected paired t-test p = 0.70 after Holm). Both beat the overall average (difference 0.41 for gradient boosting, p = 0.0002; [table_12](results/table_12_nadeau_bengio.csv)). These tests use the 50 per-fold scores, which are not independent, so the correction is approximate.
- The two models above use fixed settings; a tuned comparison is in the next section. The "10 of 10 repeats" above shows that the result is stable across partitions of the same 51 states, not that it is statistically significant.

![Random vs grouped folds](results/fig_04_cv_random_vs_grouped.png)

### Sensitivity checks (gradient boosting, state-grouped R²)

| Check | Counties | R² |
|---|---|---|
| Main analysis | 2,674 | 0.34 |
| Without female share, larger sample | 2,923 | 0.29 |
| Only counties with 500+ recipients | 1,638 | 0.36 |
| Outcome = share rated 100% | 2,674 | 0.36 |

### Robustness checks (Part 2 of the notebook)

[notebooks/va_disability_county_severity.ipynb](notebooks/va_disability_county_severity.ipynb) re-checks the results after review. It reproduces the headline numbers above first.

| Held-out unit | Model | R², counties equal | R², recipient-weighted | RMSE (points), counties equal |
|---|---|---|---|---|
| 5 state-grouped folds | Gradient boosting | 0.34 | 0.47 | 6.59 |
| Leave one state out | Gradient boosting | 0.35 | 0.47 | 6.56 |
| Leave one state out | Linear regression | 0.33 | 0.47 | 6.62 |
| Census region (4 blocks) | Gradient boosting | −0.13 | 0.22 | 8.62 |
| Census region (4 blocks) | Linear regression | −0.10 | 0.31 | 8.49 |
| Census region (4 blocks) | Overall average (baseline) | −0.75 | −1.13 | 10.72 |

- Weighting by recipients raises R² for every model because small, noisy counties count less. Neither weighting is a better headline; both are shown. Models are fitted without weights.
- Leave-one-state-out matches the 5-fold grouped result. Region blocking is much harder: models beat the baseline but are poor, with strong bias (gradient boosting: Midwest +7.6 points too high, South −6.7 too low; [table_17](results/table_17_region_blocked_error.csv)). The state-to-region map was written from general knowledge and needs a check ([table_14](results/table_14_fips_region_map.csv)).
- Largest leave-one-state-out errors: South Dakota, Indiana, Minnesota, Nebraska and Alaska (RMSE 9.9 to 12.9 points, all over-predicted; [table_16](results/table_16_loso_per_state_error.csv)).
- **Left-out counties.** Of the 470, 287 have a computable outcome but a blank feature cell, so the model could not score them; they hold 29,749 recipients with a pooled high share of 49.8%, against 58.6% in the main sample. Given their states, 54.7% would be expected, so about half of the gap is state composition ([table_20](results/table_20_selection_check.csv)). The other 183 have no computable outcome.

### Tuned models and literature comparison (Parts 3 and 4 of the notebook)

[notebooks/va_disability_county_severity.ipynb](notebooks/va_disability_county_severity.ipynb) tunes six candidates and an ensemble with inner state-grouped CV inside each outer training set, on the same 50 outer folds.

| Model | Grouped R² | Paired R² difference vs gradient boosting (95% state bootstrap CI) |
|---|---|---|
| Gradient boosting (reference) | 0.339 | n/a |
| Ridge (tuned) | 0.326 | −0.013 (−0.053 to 0.031) |
| Random forest (tuned) | 0.325 | −0.014 (−0.028 to 0.004) |
| HistGB (tuned) | 0.338 | −0.001 (−0.011 to 0.014) |
| Ensemble linear + tree | 0.347 | +0.008 (−0.009 to 0.029) |

No candidate improves on the reference by the pre-set rule (lower CI bound above 0; Holm-adjusted p = 1.0 for all, [table_25](results/table_25_paired_vs_reference.csv)). Distance to the nearest training county does not explain which held-out states are predicted badly (Spearman 0.04, p = 0.81, [table_26](results/table_26_area_of_applicability.csv)).

[notebooks/va_disability_county_severity.ipynb](notebooks/va_disability_county_severity.ipynb) compares this project with published work. No published benchmark exists for this outcome, so absolute R² is not compared. The random-to-grouped drop is 0.07 here (gradient boosting) against 0.39 in Ploton et al. (2020, random forest, forest biomass; R² 0.53 to 0.14), a different domain used only to illustrate the same effect ([table_27](results/table_27_validation_gap_comparison.csv), [fig_11](results/fig_11_validation_gap_vs_published.png)). Methods are mapped to the cited guidance in [table_28](results/table_28_method_comparison.csv).

## Limitations

- **No denominators.** The file has no population or veteran counts, so nothing here is a rate per resident or per veteran. Every result is about the mix of people who already receive compensation.
- **Counties, not people.** These are associations between county-level shares. They do not show that older or female veterans individually receive lower or higher ratings (ecological fallacy).
- **Hidden small cells and selection.** Counts below 10 are blank in the source. 470 counties are left out of the main analysis (457 with a known total, median 67 recipients; 13 with a blank total). They hold 0.6% of recipients, so pooled figures barely move, but the exclusion is not random: it is driven largely by a blank male/female cell, a predictor, and the left-out counties with a computable outcome have a lower high-rating share (see Robustness checks). Conclusions do not cover very small counties or the rural states where they are concentrated.
- **Source and year not confirmed.** The file arrived without documentation. See [data/DATA_CARD.md](data/DATA_CARD.md).
- **No explanation of the state differences.** The gap between states is large (Minnesota is 7 points below the next state) and this dataset cannot say why. It deserves a check against the original source before being quoted.
- **One snapshot.** No time dimension, no external validation set, and no final held-out test stage: all evaluation is cross-validation, which is acceptable for a descriptive study.
- **Metrics count counties equally.** The headline R² gives a 62-recipient county the same weight as a 98,000-recipient one; recipient-weighted values are given next to it.
- **Small feature set.** Four county features only; tuned ridge, random forest and boosting (Part 3) add nothing, so the limit is the features, not the model.
- **Spatial leakage is only partly removed.** State-grouped folds keep neighbouring counties of different states in training; region blocking is a stricter check but the folds are few and unequal.
- **Recipients only.** There is no veteran or resident population, so selection into compensation is unobserved.
- **"Noise" is a model assumption.** The 2.2-point expected SD assumes independent recipients sharing one national rate; a rejection means counties are not homogeneous, not that every difference is a real effect of the county.

## Background and research gaps

A literature review with 16 sources and 6 unverified leads is in [research/](research/): [literature_review.md](research/literature_review.md), [research_gaps.md](research/research_gaps.md) and [references.md](research/references.md). It was drafted by an AI agent that opened each source; 11 sources were read on the opened page, 5 were matched by bibliographic record only (flagged in the table), and the six leads it could not open are kept out of the synthesis. Check the sources before citing them.

- No peer-reviewed study of the geography of VA ratings turned up. The verified VA-specific sources are government reports from 2004 to 2010 on consistency of decisions, not on the county share rated 70% or more, so the project cannot yet say why states differ.
- The methodological literature disagrees on spatial validation (block cross-validation versus the view that it has no theoretical basis). This project holds out whole states because predicting an unseen state is the stated aim of RQ3.
- Top gaps this data could address, not yet done: shrinkage of noisy county shares and bounds for the hidden small cells; a multilevel model (county within state); and separating leakage from extrapolation in the random-versus-grouped gap.

## Method

| Step | What is done |
|---|---|
| Data | 3,144 county rows; 4 non-county rows (Puerto Rico total, other territories, foreign, unknown) excluded |
| Cleaning | Thousands separators removed; blank cells kept as missing, never filled in |
| Outcome | (rated 70–90% + rated 100%) ÷ total recipients |
| Features | Share aged 17–44, share aged 65+, share female, log10 of total recipients |
| Leakage control | Other rating bands and the 45–64 share are not used as features (they sum to 100% with the outcome or with other features) |
| Variation | Observed variance against binomial variance; chi-square test of equal shares |
| Association | Spearman correlation and standardised linear coefficients; state cluster bootstrap for 95% CIs |
| Prediction | Baseline, state average, linear regression, gradient boosting (fixed); Part 3 of the notebook adds tuned ridge, random forest, HistGB and an ensemble |
| Validation | 5-fold CV × 10 repeats, random folds and state-grouped folds reported side by side; leave-one-state-out and Census-region blocks in the robustness notebook |
| Comparison tests | State-cluster bootstrap (2,000 resamples of states, stored out-of-fold predictions, no refit) and Nadeau–Bengio corrected paired t-test with Holm correction |
| Seed | 42 |

## Structure

```
02-va-disability-county-severity/
├── README.md
├── requirements.txt
├── data/            raw CSV (read-only) and DATA_CARD.md
├── notebooks/       va_disability_county_severity.ipynb  (one notebook: main analysis, robustness, tuned models, literature comparison)
├── research/        literature review, research gaps, references (AI-drafted, to be checked)
└── results/         11 figures (PNG), 28 tables (CSV) and audit.md written by or about the notebooks
```

## Reproduce

```bash
cd 02-va-disability-county-severity
python3.11 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cd notebooks && jupyter lab va_disability_county_severity.ipynb     # Run All, about 5 minutes
```

The recorded notebook outputs were produced with slightly different library versions than those pinned in `requirements.txt`; an independent re-run under the pinned versions gave the same headline numbers.

## Ethics

The data are aggregate counts with small cells already suppressed; no individual can be identified. Results describe counties and must not be used to judge individual claims or veterans.
