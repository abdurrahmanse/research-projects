# Reproducibility and claims audit

**Audit date:** 2026-11-14

## Delivery checklist

- [x] Question, hypotheses, primary metric and validation written before the notebook's model cells
- [x] Raw CSV unchanged; local SHA-256 recorded in the data card
- [x] Shape, types, missingness, incident-ID duplicates, areas and date ranges printed before modelling
- [x] Aggregation uses report date; 94 reports dated after 2024 are explicitly excluded
- [x] All lag and rolling features shifted by at least one month
- [x] Validation preserves time order; no random split
- [x] Transparent baseline/simple models and nonlinear candidates compared
- [x] Four configurations for every trainable family; all configurations retained
- [x] Primary selection uses only 2022 rolling-origin MAE
- [x] 2023 predictions stored once, then reused for plots and diagnostics
- [x] Uncertainty comparison resamples whole test months, not individual area rows
- [x] 2024 labelled as reporting-system shift stress test
- [x] Notebook contains 49 code cells, zero markdown cells, and passes the repository linter
- [x] Notebook executed top to bottom without a cell error
- [x] Requirements pinned and citations opened/verified

## Claim-to-artifact map

| Claim | Evidence |
|---|---|
| 3-month mean won validation | `table_04_model_comparison.csv` |
| 2023 MAE 48.98 and WAPE 5.26% | `table_06_test_metrics.csv` |
| Area/month errors | `table_07_test_error_by_area.csv`, `table_08_test_error_by_month.csv` |
| Approximate interval coverage 95.24% | `table_06_test_metrics.csv` |
| Seasonal-naive improvement and CI | executed notebook, paired-month bootstrap cell |
| 2024 MAE 122.01 and WAPE 22.93% | `table_10_2024_stress_metrics.csv` |
| Visible post-transition discontinuity | `table_11_2024_monthly_shift.csv`, `fig_06_2024_system_shift.png` |

## Qualifications

The project was not externally preregistered. The bootstrap has only 12 month blocks. The residual interval is approximate rather than a formal guarantee under spatial/temporal dependence. No external city or current NIBRS dataset is evaluated. Accordingly, the results support an internal historical forecasting comparison, not deployment or a general claim about crime.
