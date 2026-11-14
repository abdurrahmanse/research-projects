# Pre-specified research plan

## Question

Can historical monthly counts forecast the next month's number of crime incidents reported in each of the 21 LAPD areas?

## Hypotheses

- H1: at least one candidate will have lower mean 2022 rolling-origin MAE than a 12-month seasonal-naive forecast.
- H2: forecast MAE will be higher in the 2024 legacy-file stress period than in the 2023 evaluation because the reporting system changed in March 2024.

These are predictive hypotheses. They do not assert that the model measures true crime or that any feature causes crime.

## Outcome and metrics

- Unit: LAPD area-month
- Outcome: count of rows grouped by `Date Rptd`, area and calendar month
- Primary metric: MAE, averaged first across 21 areas and then across forecast months
- Secondary metrics: WAPE, RMSE and mean Poisson deviance
- Approximate uncertainty: 90% residual interval calibrated from rolling 2022 errors

## Validation and selection

The first 12 months are consumed by lag construction. Each month of 2022 is predicted from all earlier months, giving 12 expanding-window origins. Every trainable family receives four configurations. The family/configuration with the lowest mean monthly validation MAE is selected. January–December 2023 is evaluated after selection. The year 2024 is a separate reporting-shift stress test, not ordinary evidence of crime-forecast performance.

## Candidates

- Historical rules: previous month, trailing 3-month mean, trailing 6-month mean, seasonal naive
- Ridge regression
- Poisson regression
- Random forest
- Histogram gradient boosting with Poisson loss
- XGBoost with Poisson objective

All trainable models see the same area indicator, trend, month sine/cosine terms, five past lags, three past-only rolling means and one past-only rolling standard deviation. No future month, incident outcome, crime label, victim attribute or resolution status is a feature.

## Improvement and interpretation rules

All candidates are reported, including weak models. The validation winner remains the headline model even if a more complex model is more fashionable. A month-block bootstrap interval compares its 2023 MAE with seasonal naive. If the interval includes zero, the paper will not claim a statistically clear improvement. The 2024 decline will be described as a dataset/reporting discontinuity.
