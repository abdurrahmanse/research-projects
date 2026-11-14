# Academic defense notes

## One-minute opening

This study forecasts the next month's number of incidents reported in each of 21 LAPD areas. I deliberately chose an aggregate forecasting target instead of predicting individuals or crime labels. The design preserves time order: every 2022 validation month is predicted only from earlier months, and 2023 is evaluated after model selection. I compared transparent history rules with Ridge, Poisson regression, random forest, histogram boosting and XGBoost under equal tuning budgets. The key result is that the trailing 3-month mean outperformed every complex candidate. Its 2023 MAE was 48.98 incidents per area-month and WAPE was 5.26%. A known March 2024 records-system change then caused a large distribution shift, demonstrating why data provenance and monitoring matter as much as model choice.

## Slide-ready storyline

1. **Problem:** next-month reported-count forecasting for 21 LAPD areas, not individual-risk prediction.
2. **Data audit:** 1,004,894 incident rows; unique IDs; report dates extend 94 rows into 2025; known 2024 system transition.
3. **Ethical scope:** no victim, race/descent, weapon, precise location, crime type or arrest/status feature.
4. **Leakage control:** lag and rolling features are shifted; all validation is future-to-past.
5. **Fair comparison:** four configurations per trainable family plus transparent history rules.
6. **Validation result:** 3-month mean 57.93 MAE; Ridge 60.11; XGBoost 61.11.
7. **2023 evaluation:** MAE 48.98, WAPE 5.26%, RMSE 61.58.
8. **Uncertainty:** improvement over seasonal naive 21.83; bootstrap CI 12.41–32.95.
9. **System shift:** 2024 MAE 122.01; legacy-file continuity breaks after the RMS transition.
10. **Conclusion:** prefer the simplest validated model; never confuse police reports with true crime.

## Likely examiner questions

### Why did you not use a random 80/20 split?

A random split lets later months teach the model about earlier months and exaggerates real forecasting performance. Expanding-window validation preserves the information set that would have existed at each forecast date.

### Why is the target based on report date rather than occurrence date?

Report date is the time at which a record becomes operationally observable. Occurrence date can be backfilled by delayed reports, so an occurrence-month dataset reconstructed later may contain information unavailable at the original forecast date.

### Why did a simple mean beat XGBoost?

After the 12-month lag is constructed, only 24 pre-test months remain. Counts are locally stable, so a recent mean has low variance. Flexible models have limited independent temporal history and can fit noise. Model complexity is not evidence of better generalization.

### Is 5.26% WAPE proof that the model is ready for policing?

No. It describes error against recorded reports at a coarse area-month scale. Reports are affected by under-reporting and enforcement, and operational patrol use could create feedback loops. External validation, governance and current NIBRS data would be prerequisites even for considering deployment.

### Why is 2024 not another test year?

The measurement system changed on 7 March 2024. The legacy dataset's post-transition decline mixes crime, reporting and database coverage. I use it as a distribution-shift stress test, not as an ordinary forecast-performance period.

### Is the 90% interval formally valid?

It is an approximate residual interval calibrated from rolling 2022 errors. Coverage was 95.24% in 2023, but 12 calibration months and dependence among areas limit any formal exchangeability claim.

### Did the machine-learning models receive a fair comparison?

Yes within the declared scope: the same features, forecast origins and primary metric were used, and each trainable family received four configurations. The full table reports all configurations, not only the winner.

### Why not use an LSTM or GRU?

There are too few independent monthly time points for a defensible deep sequence model, and this dataset lacks the fine grid, mobility and long history used by published deep-learning studies. Adding a large neural model would increase variance without creating information.

### Can MAE be compared with published crime papers?

Not directly. Published studies use different spatial grids, time horizons, crime subsets and metrics. This study therefore maps methods to literature but does not claim a cross-paper performance rank.

## Terms to define clearly

- **Lag:** a past value used as a predictor; `lag_1` is the previous month.
- **Rolling-origin validation:** repeatedly train on the past and validate on the next time point.
- **MAE:** average absolute difference between predicted and actual counts, in incident units.
- **WAPE:** total absolute error divided by total actual counts.
- **Data leakage:** information unavailable at forecast time entering training or features.
- **Distribution shift:** the future data-generating process differs from training data.
