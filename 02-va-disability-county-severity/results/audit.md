# Audit of project 02: data, leakage and methods

Date: 2026-11-12. Produced by two independent AI review agents (a data auditor and a skeptical methods reviewer) working read-only on `README.md`, `data/`, the notebook and `results/`. Figures marked *re-derived* were recomputed from the raw CSV by the auditor, not copied from the notebook. This file reports findings; it does not change the analysis. Treat it as a review to be checked, not as ground truth.

## 1. Data and leakage audit: verdict clean

**Reproduced from the raw file:** 3,148 rows, 3,144 counties, 51 states incl. DC, no duplicate FIPS; 470 counties excluded, 2,674 analysed; pooled high-rating share 58.6%; county SD 8.10 vs 2.23 expected under one common rate; between-state variance share 63.3%; quantiles 39.5 / 55.8 / 66.2. A full re-run of the 10 × 5 CV under the pinned library versions gave gradient boosting R² 0.405 random and 0.339 grouped, state average 0.618 random and −0.047 grouped, matching tables 06, 07 and 09.

**Leakage checks passed:** no target leakage (rating bands and the 45–64 share are excluded; features are 17–44 share, 65+ share, female share, log10 total); no preprocessing fitted outside folds (scaler inside the pipeline, no imputation, selection or tuning); state-average predictor built from training rows only; each state sits in exactly one grouped fold; zero duplicate rows; seed 42 everywhere. A shuffled-target run scored R² −0.02 grouped, i.e. chance.

## 2. Findings and status

| # | Severity | Finding | Status |
|---|---|---|---|
| A1 | Medium | The 470 exclusions are not random: 249 are caused by the blank female-share cell alone, and female share correlates with the outcome (ρ ≈ +0.49). The README says conclusions do not cover very small counties, which understates this. 183 of the 470 have no computable outcome; the other 287 (re-derived, reviewer) have a pooled high share of about 49.8% vs 58.6% in the main sample | Quantify in `notebooks/02_robustness_checks` (analysis 6), then reword README Limitations |
| A2 | Medium | `data/DATA_CARD.md` is wrong on two points (see §3) | **Needs the owner's edit** (`data/` is write-protected by `.claude/settings.json`) |
| A3 | Low–medium | README says 470 small counties with median 67 recipients, but `table_02` shows 457: the 13 counties with a blank total have no size. The abstract's 58.6% is over the 2,674-county main sample (99.4% of recipients), not "all counties" | Reword README |
| A4 | Low | The 63.3% between-state share is the raw, county-unweighted η² of 51 groups. It includes the binomial component and has no CI. A noise-adjusted version is about 62.6% (re-derived) | Add CI (robustness notebook, analysis 1); label as unweighted |
| A5 | Low | Library versions recorded in the notebook output (pandas 3.0.5, scipy 1.18.0, scikit-learn 1.9.0, matplotlib 3.11.0) differ from `requirements.txt` (pandas 3.1.1, scipy 1.17.1, scikit-learn 1.9.1, matplotlib 3.11.2). Headline numbers reproduce under the pinned versions anyway | Re-run the main notebook and `pip freeze` from one environment |
| A6 | Low | R² uses pooled out-of-fold predictions. The grouped score varies from 0.31 to 0.36 across repeats; the 10 repeats resample partitions of the same 51 states, so "10 of 10 repeats" shows stability, not significance. Neighbouring counties across state borders stay in training (mild spatial leak) | Robustness notebook, analyses 1 and 4 |
| A7 | Info | README gradient-boosting error 5.2 vs table 5.249 and linear 5.30 vs table 5.304 | Round consistently (5.25 / 5.30) |
| A8 | Info | "Hypotheses written before the results" cannot be verified from the repository (no hypothesis-only commit) | Say so in README |

## 3. Proposed corrections to `data/DATA_CARD.md` (not applied)

1. *Blank cells* row: replace "the smallest value in every column is 10" with "the smallest value is 10 in every column except `male`, whose smallest value is 48 (`results/table_01_blank_cells.csv`)".
2. *Consistency* row: replace "the rating bands, the age bands and male + female each add up exactly to the total" with "in the 2,649 counties with no blank cell the rating bands add up exactly to the total in all of them; the age bands in 98.9% (28 counties short by exactly 1); male + female in 81.8% (481 counties short by 1 to 29, probably unknown sex)" (notebook Task 12 output; confirmed by independent re-derivation).
3. Add a *Sample selection* row: "2,674 counties kept (62 to 98,159 recipients); 470 left out: 457 with a known total (median 67, maximum 285) and 13 with a blank total; 464 counties have a blank male/female cell, so exclusion depends on a predictor".

## 4. Methods review: verdict major revision

Strengths: state-grouped CV next to random CV, state-cluster bootstrap, honest limitations section, no leakage. The reviewer's main concerns:

1. **Hypotheses are weak and the "all supported" wording overstates.** H1 (more variation than binomial) is near-certain with counts up to 98k; H2 names no direction; H3 only says grouped < random. "10 of 10 repeats" is not a test. → Say the expectations held, that they are unsurprising, and that findings are descriptive.
2. **The binomial "noise" argument is a conditional diagnostic.** It assumes independent recipients with one common rate; a census is not a random sample, and rejection means "not homogeneous". The "92% upper limit for R²" is approximate and unweighted. → Use "variance expected under a common rate"; consider a beta-binomial or random-effects variance decomposition.
3. **"Knowing the state beats the features" is over-read.** The state-average predictor equals the baseline in grouped folds by construction, and under random folds it borrows same-state neighbours. The missing fair test is state fixed effects + features vs state alone. → Reword; add the fixed-effects check.
4. **Generalisation design incomplete.** Add leave-one-state-out CV, per-state errors, and region-blocked CV (FIPS prefixes give Census regions).
5. **R² is unweighted by county and the README does not say so.** The reviewer reports recipient-weighted grouped R² of about 0.47 vs 0.34 unweighted (reviewer check, to be reproduced). → Report both, declare the primary one, add RMSE.
6. **No significance tests for model comparisons.** "Not meaningfully better" is informal. → Corrected resampled t-test (Nadeau–Bengio) with Holm, and state-cluster bootstrap of paired differences.
7. **Thin and untuned model set.** Gradient boosting uses fixed settings, the linear model needs none; no random forest or ridge (age shares correlate at −0.81, VIF up to 4.6). → State it, or add a small inner grouped-CV grid.
8. **Selection bias from the 470 left-out counties** (see A1). The prediction claim applies only to counties with at least 62 recipients and complete cells; rural prairie states are under-represented.
9. **RQ2 interpretation.** The two age coefficients are not separately interpretable (collinear); "no effect of its own" is causal wording; percentile CIs from 51 clusters are unstable; state confounding could explain the size result. → A within-state (state fixed effects) version, and "no association" wording.

Minor: label the state ranking's small-state caveat (RI, CT, DE have few counties); flag the unconfirmed source and year in the abstract, not only in Limitations; add to Limitations the unweighted metrics, untuned boosting, no significance tests, no spatial blocking and the recipients-only denominator (selection into compensation is unobserved); fill or remove the README author placeholder; the study has no final held-out test stage (acceptable for a descriptive study, but say so).

## 5. Not checked

Source and licence of the data; whether Minnesota's 37.9% is real or an artefact; the figures by eye; bootstrap CIs in tables 04–05 and the chi-square p-value (only table vs notebook-output consistency was checked); sensitivity rows 2–4; spatial autocorrelation across borders; whether the original notebook executes end to end (the auditor re-implemented its logic instead).

## 6. Follow-up

Robustness analyses requested by the reviewer are implemented in `notebooks/02_robustness_checks.py` (outputs `results/table_10_*` onward). README numbers and wording will be updated only from those executed outputs.
