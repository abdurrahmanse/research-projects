# Literature review and method map

## What the literature supports

The official LAPD portal describes the file as incident records dating from 2020 and warns that paper-report transcription may introduce inaccuracies. It also records a transition on 7 March 2024 from the legacy UCR-oriented records system to a NIBRS-aligned system. That transition makes post-change counts in the legacy file a measurement-shift problem, not a normal continuation of the earlier series.

Time-ordered evaluation is essential. Tashman (2000) explains rolling-origin evaluation and the value of forecasts from multiple origins. Cerqueira, Torgo and Mozetič (2020) show that random cross-validation can be unrealistic for dependent data and find out-of-sample procedures particularly suitable for non-stationary real-world series. This project therefore uses expanding monthly origins, never random row splits.

Crime forecasting research shows that incident reports contain forecastable spatiotemporal structure, but it also makes the scope problem explicit. Rotaru et al. (2022) forecast weekly crime at fine spatial resolution while emphasizing that reports reflect crime, policing and society together. Albors Zumel, Tizzoni and Campedelli (2026; published online in 2025) compare deep and conventional models for several US cities, including Los Angeles, using incident, mobility and sociodemographic data. Their much finer grid and 12-hour horizon are not a benchmark for this monthly, 21-area dataset.

Wu et al. (2023) find fairness problems across place-based deep-learning crime forecasts and trace part of them to incident-data bias. This study therefore avoids patrol-allocation claims and person-level predictors. Area-wise error is reported only as a diagnostic, not a fairness guarantee.

Chen and Guestrin (2016) motivate XGBoost as a strong nonlinear tabular candidate. It is included under the same tuning and temporal-validation rules as simpler models; it is not assumed to win. Stankevičiūtė, Alaa and van der Schaar (2021) motivate uncertainty intervals for time-series forecasts. The residual interval here is deliberately labelled approximate because only 12 validation months and dependent area observations are available.

## Research gap addressed

The contribution is not a new policing algorithm. It is a leakage-resistant, beginner-reproducible comparison showing whether complex machine learning improves on transparent history rules for coarse LAPD area-month reporting, and how a known administrative system change breaks apparent forecast continuity. No opened paper supplied a directly comparable benchmark with the same target, spatial unit, horizon and legacy-file cutoff, so cross-paper accuracy rankings would be invalid.

## Claims that are out of scope

- The model does not estimate unreported crime or personal victimization risk.
- Forecast associations are not causes.
- An accurate area forecast would not justify patrol deployment.
- The 2024 stress result cannot be read as evidence of a real crime decline.
- Deep-learning results at grid/hour scale cannot be compared numerically with area/month MAE.
